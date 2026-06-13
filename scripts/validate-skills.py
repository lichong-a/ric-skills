#!/usr/bin/env python3
"""Validate the RIC skill repository without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from json_schema import check_schema


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
README_SKILL_RE = re.compile(r"`(ric-[a-z0-9]+(?:-[a-z0-9]+)*)`")
POWERSHELL_REGISTRY_RE = re.compile(
    r'^\s*"(?P<name>ric-[a-z0-9-]+)"\s*=\s*'
    r'"skills/(?P<path_name>ric-[a-z0-9-]+)/SKILL\.md"\s*$',
    re.MULTILINE,
)
BASH_REGISTRY_RE = re.compile(
    r"^\s*\[(?P<name>ric-[a-z0-9-]+)]\s*=\s*"
    r'["\']skills/(?P<path_name>ric-[a-z0-9-]+)/SKILL\.md["\']\s*$',
    re.MULTILINE,
)
ROLE_VALUES = {
    "orchestrator",
    "lifecycle-stage",
    "policy",
    "primary-executor",
    "modifier",
    "quality-gate",
    "handoff",
    "runtime",
}
CORE_VISUAL_SKILLS = {
    "ric-design-taste-frontend",
    "ric-image-to-code",
    "ric-imagegen-frontend-web",
    "ric-imagegen-frontend-mobile",
    "ric-brandkit",
}
CORE_VISUAL_WARN_LINES = 500
CORE_VISUAL_ERROR_LINES = 1500
REQUIRED_SCHEMA_FILES = {
    "catalog.schema.json",
    "delivery-run.schema.json",
    "dispatch.schema.json",
    "acceptance.schema.json",
    "traceability.schema.json",
    "risk-register.schema.json",
    "review-result.schema.json",
    "adjudication-result.schema.json",
    "test-plan.schema.json",
    "test-result.schema.json",
    "evidence-manifest.schema.json",
    "live-eval-result.schema.json",
}
REQUIRED_EVAL_FILES = {
    "trigger-selection.json": "trigger-selection",
    "negative-triggers.json": "negative-triggers",
    "composition-conflicts.json": "composition-conflicts",
    "behavioral-scenarios.json": "behavioral-scenarios",
    "end-to-end-delivery.json": "end-to-end-delivery",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: Path
    message: str
    line: int | None = None

    def render(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root).as_posix()
        except ValueError:
            display = self.path.as_posix()
        location = f"{display}:{self.line}" if self.line else display
        return f"{self.severity} [{self.code}] {location}: {self.message}"


@dataclass(frozen=True)
class SkillRecord:
    name: str
    folder: str
    description: str
    skill_path: Path
    line_count: int


class Validator:
    def __init__(self, root: Path, warnings_as_errors: bool = False) -> None:
        self.root = root.resolve()
        self.warnings_as_errors = warnings_as_errors
        self.issues: list[Issue] = []
        self.skills: dict[str, SkillRecord] = {}
        self.catalog_entries: dict[str, dict[str, Any]] = {}

    def add(
        self,
        severity: str,
        code: str,
        path: Path,
        message: str,
        line: int | None = None,
    ) -> None:
        if severity == "WARNING" and self.warnings_as_errors:
            severity = "ERROR"
        self.issues.append(Issue(severity, code, path, message, line))

    def error(self, code: str, path: Path, message: str, line: int | None = None) -> None:
        self.add("ERROR", code, path, message, line)

    def warning(self, code: str, path: Path, message: str, line: int | None = None) -> None:
        self.add("WARNING", code, path, message, line)

    def run(self) -> list[Issue]:
        self.validate_skill_folders()
        self.validate_bundled_resources()
        self.validate_markdown_references()
        self.validate_catalog()
        self.validate_registries()
        self.validate_schemas()
        self.validate_evals()
        self.validate_legacy_conflicts()
        return sorted(
            self.issues,
            key=lambda issue: (
                issue.severity != "ERROR",
                issue.path.as_posix(),
                issue.line or 0,
                issue.code,
            ),
        )

    def validate_skill_folders(self) -> None:
        skills_dir = self.root / "skills"
        if not skills_dir.is_dir():
            self.error("SKILL001", skills_dir, "skills directory is missing")
            return

        for folder in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
            skill_path = folder / "SKILL.md"
            if not skill_path.is_file():
                self.error("SKILL002", skill_path, "skill folder must contain SKILL.md")
                continue

            text = read_text(skill_path, self)
            if text is None:
                continue
            line_count = len(text.splitlines())
            metadata = self.parse_frontmatter(skill_path, text)
            if metadata is None:
                continue

            name = metadata.get("name", "")
            description = metadata.get("description", "")
            if name in self.skills:
                self.error("SKILL003", skill_path, f"duplicate skill name {name!r}")
            else:
                self.skills[name] = SkillRecord(
                    name=name,
                    folder=folder.name,
                    description=description,
                    skill_path=skill_path,
                    line_count=line_count,
                )

            if name != folder.name:
                self.error(
                    "SKILL004",
                    skill_path,
                    f"frontmatter name {name!r} must match folder {folder.name!r}",
                    2,
                )
            if not NAME_RE.fullmatch(name) or len(name) > 64:
                self.error(
                    "SKILL005",
                    skill_path,
                    "name must be lowercase hyphen-case and at most 64 characters",
                    2,
                )
            if not description.startswith("Use when"):
                self.error(
                    "SKILL006",
                    skill_path,
                    "description must start with 'Use when' and contain trigger conditions only",
                    3,
                )
            if len(description) > 500:
                self.warning(
                    "SKILL007",
                    skill_path,
                    f"description is {len(description)} characters; keep it under 500 when possible",
                    3,
                )

            self.validate_openai_metadata(folder)
            self.validate_line_budget(name, skill_path, line_count)

    def parse_frontmatter(self, path: Path, text: str) -> dict[str, str] | None:
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            self.error("FM001", path, "SKILL.md must start with YAML frontmatter", 1)
            return None

        try:
            closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
        except StopIteration:
            self.error("FM002", path, "frontmatter closing delimiter is missing", 1)
            return None

        raw_frontmatter = "\n".join(lines[1:closing])
        if len(raw_frontmatter) > 1024:
            self.error("FM003", path, "frontmatter must be at most 1024 characters", 1)

        metadata: dict[str, str] = {}
        for offset, raw_line in enumerate(lines[1:closing], start=2):
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", raw_line)
            if not match:
                self.error(
                    "FM004",
                    path,
                    "frontmatter must use one-line scalar key/value pairs",
                    offset,
                )
                continue
            key, raw_value = match.groups()
            if key in metadata:
                self.error("FM005", path, f"duplicate frontmatter key {key!r}", offset)
                continue
            metadata[key] = parse_yaml_scalar(raw_value)

        missing = ALLOWED_FRONTMATTER_KEYS - metadata.keys()
        extra = metadata.keys() - ALLOWED_FRONTMATTER_KEYS
        if missing:
            self.error("FM006", path, f"missing frontmatter keys: {sorted(missing)}", 1)
        if extra:
            self.error("FM007", path, f"unsupported frontmatter keys: {sorted(extra)}", 1)
        for key in ALLOWED_FRONTMATTER_KEYS:
            if key in metadata and not metadata[key].strip():
                self.error("FM008", path, f"frontmatter key {key!r} must not be empty", 1)
        return metadata

    def validate_openai_metadata(self, skill_dir: Path) -> None:
        metadata_path = skill_dir / "agents" / "openai.yaml"
        if not metadata_path.is_file():
            self.error(
                "AGENT001",
                metadata_path,
                "every skill must provide agents/openai.yaml",
            )
            return
        text = read_text(metadata_path, self)
        if text is None:
            return
        if not re.search(r"(?m)^interface:\s*$", text):
            self.error("AGENT002", metadata_path, "openai.yaml must contain an interface mapping")
        for key in ("display_name", "short_description", "default_prompt"):
            match = re.search(rf"(?m)^\s{{2,}}{re.escape(key)}:\s*(.+?)\s*$", text)
            if not match or not parse_yaml_scalar(match.group(1)).strip():
                self.error("AGENT003", metadata_path, f"interface.{key} is required")
        if re.search(r"\bTODO\b|placeholder", text, re.IGNORECASE):
            self.error("AGENT004", metadata_path, "openai.yaml must not contain placeholders")

    def validate_line_budget(self, name: str, path: Path, line_count: int) -> None:
        if name not in CORE_VISUAL_SKILLS:
            return
        if line_count > CORE_VISUAL_ERROR_LINES:
            self.error(
                "BUDGET002",
                path,
                f"core visual skill has {line_count} lines; hard limit is {CORE_VISUAL_ERROR_LINES}",
            )
        elif line_count > CORE_VISUAL_WARN_LINES:
            self.warning(
                "BUDGET001",
                path,
                f"core visual skill has {line_count} lines; split details into one-level references",
            )

    def validate_markdown_references(self) -> None:
        skills_dir = self.root / "skills"
        if not skills_dir.is_dir():
            return
        markdown_paths = set(skills_dir.rglob("*.md"))
        markdown_paths.update((self.root / "references").rglob("*.md"))
        if (self.root / "README.md").is_file():
            markdown_paths.add(self.root / "README.md")
        for markdown_path in sorted(markdown_paths):
            text = read_text(markdown_path, self)
            if text is None:
                continue
            stripped = strip_fenced_code(text)
            for match in MARKDOWN_LINK_RE.finditer(stripped):
                target = clean_markdown_target(match.group(1))
                if not target or is_external_target(target):
                    continue
                if re.match(r"^[A-Za-z]:[/\\]", target) or target.lower().startswith("file://"):
                    line = stripped.count("\n", 0, match.start()) + 1
                    self.error("REF002", markdown_path, f"absolute local reference is forbidden: {target}", line)
                    continue
                decoded = unquote(target)
                if decoded.startswith("/"):
                    target_path = (self.root / decoded.lstrip("/")).resolve()
                else:
                    target_path = (markdown_path.parent / decoded).resolve()
                try:
                    target_path.relative_to(self.root)
                except ValueError:
                    line = stripped.count("\n", 0, match.start()) + 1
                    self.error(
                        "REF002",
                        markdown_path,
                        f"local reference escapes repository boundary: {target}",
                        line,
                    )
                    continue
                if not target_path.exists():
                    line = stripped.count("\n", 0, match.start()) + 1
                    self.error(
                        "REF001",
                        markdown_path,
                        f"local reference does not exist: {target}",
                        line,
                    )

    def validate_bundled_resources(self) -> None:
        for record in self.skills.values():
            folder = record.skill_path.parent
            text = read_text(record.skill_path, self)
            if text is None:
                continue
            references = folder / "references"
            if references.is_dir():
                for path in references.rglob("*"):
                    if path.is_file() and path.name not in text:
                        self.error(
                            "RESOURCE001",
                            path,
                            "bundled reference must be linked from its owning SKILL.md",
                        )
            allowed_top_level = {"SKILL.md", "agents", "references", "assets", "scripts"}
            for child in folder.iterdir():
                if child.name not in allowed_top_level:
                    self.error(
                        "RESOURCE002",
                        child,
                        "unexpected top-level bundled resource; move it under references, assets, or scripts",
                    )

    def validate_catalog(self) -> None:
        catalog_path = self.root / "skills" / "catalog.json"
        if not catalog_path.exists():
            self.error("CAT000", catalog_path, "catalog is required and is the registry source of truth")
            return
        data = load_json(catalog_path, self)
        if data is None:
            return
        entries = normalize_catalog_entries(data, catalog_path, self)
        self.catalog_entries = entries
        if not entries:
            return

        self.compare_skill_sets("CAT002", catalog_path, set(entries), "catalog")
        orchestrators: list[str] = []
        handoff_graph: dict[str, set[str]] = {name: set() for name in entries}
        gate_type_owners: dict[str, str] = {}
        capabilities = value_as_names(data.get("capabilities")) if isinstance(data, dict) else set()
        if not capabilities:
            self.error("CAT017", catalog_path, "catalog capabilities must be a non-empty list")

        for name, entry in entries.items():
            description = entry.get("description")
            if not isinstance(description, str) or not description.startswith("Use when"):
                self.error("CAT013", catalog_path, f"{name}: description must be a trigger-oriented 'Use when...' sentence")
            elif name in self.skills and description != self.skills[name].description:
                self.error("CAT014", catalog_path, f"{name}: catalog description must match SKILL.md frontmatter")
            allowed_roles = value_as_names(entry.get("allowed_roles"))
            default_role = entry.get("default_role")
            if not allowed_roles or not allowed_roles <= ROLE_VALUES:
                self.error(
                    "CAT003",
                    catalog_path,
                    f"{name}: allowed_roles must be a non-empty subset of {sorted(ROLE_VALUES)}",
                )
            if default_role not in allowed_roles:
                self.error("CAT012", catalog_path, f"{name}: default_role must be in allowed_roles")
            if "orchestrator" in allowed_roles:
                orchestrators.append(name)

            required = get_name_set(entry, "required_companions", "requiredCompanions", "requires")
            optional = get_name_set(entry, "optional_companions", "optionalCompanions", "optional")
            conflicts = get_name_set(entry, "conflicts", "conflicts_with", "conflictsWith")
            quality_gates = get_name_set(entry, "quality_gates")
            conditional_quality_gates = entry.get("conditional_quality_gates", {})
            gate_types = get_name_set(entry, "gate_types")
            capability_routes = get_name_set(entry, "capability_routes")
            handoffs = get_name_set(entry, "handoffs", "handoff_to", "redirects_to")
            handoff_graph[name].update(handoffs)
            if gate_types and "quality-gate" not in allowed_roles:
                self.error("CAT015", catalog_path, f"{name}: gate_types require the quality-gate role")
            unknown_routes = capability_routes - capabilities
            if unknown_routes:
                self.error("CAT018", catalog_path, f"{name}: unknown capability routes {sorted(unknown_routes)}")
            if not isinstance(conditional_quality_gates, dict):
                self.error("CAT019", catalog_path, f"{name}: conditional_quality_gates must be an object")
                conditional_quality_gates = {}
            for capability, gate_names in conditional_quality_gates.items():
                if capability not in capabilities:
                    self.error("CAT020", catalog_path, f"{name}: unknown conditional gate capability {capability!r}")
                for gate_name in value_as_names(gate_names):
                    if gate_name not in entries:
                        self.error("CAT021", catalog_path, f"{name}: unknown conditional quality gate {gate_name!r}")
            for gate_type in gate_types:
                if gate_type in gate_type_owners:
                    self.error("CAT016", catalog_path, f"gate type {gate_type!r} has multiple owners")
                gate_type_owners[gate_type] = name

            for relation, targets in (
                ("required companion", required),
                ("optional companion", optional),
                ("conflict", conflicts),
                ("quality gate", quality_gates),
                ("handoff", handoffs),
            ):
                for target in targets:
                    if target not in entries:
                        self.error(
                            "CAT004",
                            catalog_path,
                            f"{name}: unknown {relation} skill {target!r}",
                        )
                    if target == name:
                        self.error(
                            "CAT005",
                            catalog_path,
                            f"{name}: {relation} must not point to itself",
                        )

            invalid_relations = conflicts & (required | optional | handoffs)
            if invalid_relations:
                self.error(
                    "CAT006",
                    catalog_path,
                    f"{name}: conflicting skills also appear as companions/handoffs: "
                    f"{sorted(invalid_relations)}",
                )

            if allowed_roles <= {"modifier", "policy", "runtime", "quality-gate"}:
                forbidden_targets = {
                    target
                    for target in handoffs
                    if value_as_names(entries.get(target, {}).get("allowed_roles"))
                    & {"orchestrator", "primary-executor"}
                }
                if forbidden_targets:
                    self.error(
                        "CAT007",
                        catalog_path,
                        f"{name}: non-owner role must not redirect ownership to "
                        f"{sorted(forbidden_targets)}",
                    )

            required_conflicts = {
                pair
                for pair in required
                for other in required
                if pair != other and other in get_name_set(entries.get(pair, {}), "conflicts")
            }
            if required_conflicts:
                self.error(
                    "CAT008",
                    catalog_path,
                    f"{name}: required companions conflict: {sorted(required_conflicts)}",
                )

        if len(orchestrators) != 1:
            self.error(
                "CAT009",
                catalog_path,
                f"catalog must define exactly one orchestrator; found {sorted(orchestrators)}",
            )
        for source, targets in handoff_graph.items():
            for target in targets:
                if target not in entries:
                    continue
                source_conflicts = get_name_set(
                    entries[source], "conflicts", "conflicts_with", "conflictsWith"
                )
                target_conflicts = get_name_set(
                    entries[target], "conflicts", "conflicts_with", "conflictsWith"
                )
                if target in source_conflicts or source in target_conflicts:
                    self.error(
                        "CAT010",
                        catalog_path,
                        f"{source}: handoff target {target!r} is declared conflicting",
                    )
        for cycle in find_cycles(handoff_graph):
            self.error("CAT011", catalog_path, f"circular handoff detected: {' -> '.join(cycle)}")

    def validate_registries(self) -> None:
        expected = set(self.skills)
        registry_specs = (
            (self.root / "skill.ps1", POWERSHELL_REGISTRY_RE, "PowerShell registry"),
            (self.root / "skill.sh", BASH_REGISTRY_RE, "Bash registry"),
        )
        for path, pattern, label in registry_specs:
            if not path.exists():
                continue
            text = read_text(path, self)
            if text is None:
                continue
            matches = list(pattern.finditer(text))
            names = [match.group("name") for match in matches]
            for match in matches:
                if match.group("name") != match.group("path_name"):
                    self.error(
                        "SYNC001",
                        path,
                        f"{label} maps {match.group('name')!r} to "
                        f"{match.group('path_name')!r}",
                    )
            self.report_duplicates(path, names, label)
            self.compare_skill_sets("SYNC001", path, set(names), label)

        llms_path = self.root / "skills" / "llms.txt"
        if llms_path.exists():
            text = read_text(llms_path, self)
            if text is not None:
                names = [
                    line.split(":", 1)[0].strip()
                    for line in text.splitlines()
                    if line.strip() and not line.lstrip().startswith("#") and ":" in line
                ]
                self.report_duplicates(llms_path, names, "skills/llms.txt")
                self.compare_skill_sets("SYNC002", llms_path, set(names), "skills/llms.txt")

        readme_path = self.root / "README.md"
        if readme_path.exists():
            text = read_text(readme_path, self)
            if text is not None:
                actual = set(README_SKILL_RE.findall(text))
                self.compare_skill_sets("SYNC003", readme_path, actual, "README skill mentions")

        if not expected:
            self.error("SYNC004", self.root / "skills", "no valid skills were discovered")

    def report_duplicates(self, path: Path, names: list[str], label: str) -> None:
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        if duplicates:
            self.error("SYNC005", path, f"{label} contains duplicate skills: {duplicates}")

    def compare_skill_sets(self, code: str, path: Path, actual: set[str], label: str) -> None:
        expected = set(self.skills)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            self.error(code, path, f"{label} is missing skills: {missing}")
        if extra:
            self.error(code, path, f"{label} contains unknown skills: {extra}")

    def validate_schemas(self) -> None:
        schemas_dir = self.root / "schemas"
        for filename in sorted(REQUIRED_SCHEMA_FILES):
            path = schemas_dir / filename
            if not path.is_file():
                self.error("SCHEMA001", path, "required JSON Schema is missing")
                continue
            data = load_json(path, self)
            if data is None:
                continue
            if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                self.error("SCHEMA002", path, "schema must declare JSON Schema draft 2020-12")
            if data.get("type") != "object":
                self.error("SCHEMA003", path, "top-level schema type must be object")
            if not data.get("$id"):
                self.error("SCHEMA004", path, "schema must declare a stable $id")
            required = data.get("required")
            if not isinstance(required, list) or not required:
                self.error("SCHEMA005", path, "schema must declare non-empty required fields")
            for message in check_schema(data):
                self.error("SCHEMA006", path, message)

    def validate_evals(self) -> None:
        evals_dir = self.root / "evals"
        for filename, expected_kind in sorted(REQUIRED_EVAL_FILES.items()):
            path = evals_dir / filename
            if not path.is_file():
                self.error("EVAL001", path, "required eval fixture is missing")
                continue
            data = load_json(path, self)
            if data is None:
                continue
            if data.get("version") != 1:
                self.error("EVAL002", path, "fixture version must be 1")
            if data.get("kind") != expected_kind:
                self.error("EVAL003", path, f"fixture kind must be {expected_kind!r}")
            cases = data.get("cases")
            if not isinstance(cases, list) or not cases:
                self.error("EVAL004", path, "fixture must contain at least one case")
                continue
            seen_ids: set[str] = set()
            for index, case in enumerate(cases):
                if not isinstance(case, dict):
                    self.error("EVAL005", path, f"case {index} must be an object")
                    continue
                case_id = case.get("id")
                if not isinstance(case_id, str) or not NAME_RE.fullmatch(case_id):
                    self.error("EVAL006", path, f"case {index} id must be lowercase hyphen-case")
                elif case_id in seen_ids:
                    self.error("EVAL007", path, f"duplicate case id {case_id!r}")
                else:
                    seen_ids.add(case_id)
                prompt = case.get("prompt") or case.get("scenario")
                if not isinstance(prompt, str) or not prompt.strip():
                    self.error("EVAL008", path, f"case {case_id or index} needs prompt or scenario")
                self.validate_eval_case(path, case_id or str(index), case, expected_kind)

    def validate_eval_case(
        self,
        path: Path,
        case_id: str,
        case: dict[str, Any],
        kind: str,
    ) -> None:
        referenced: set[str] = set()
        for key in (
            "primary",
            "expected_primary",
            "skills",
            "required_skills",
            "excluded_skills",
            "composition",
            "required_gates",
        ):
            referenced.update(value_as_names(case.get(key)))
        expected = case.get("expected")
        if isinstance(expected, dict):
            for key in ("primary", "required", "excluded", "gates"):
                referenced.update(value_as_names(expected.get(key)))

        for name in sorted(referenced):
            if name.startswith("ric-") and name not in self.skills:
                self.error("EVAL009", path, f"{case_id}: references unknown skill {name!r}")

        expected_required = set()
        expected_excluded = set()
        if isinstance(expected, dict):
            expected_required = value_as_names(expected.get("required"))
            expected_excluded = value_as_names(expected.get("excluded"))
        overlap = expected_required & expected_excluded
        if overlap:
            self.error("EVAL010", path, f"{case_id}: skills cannot be required and excluded: {sorted(overlap)}")

        if kind == "composition-conflicts":
            composition = value_as_names(case.get("composition"))
            result = case.get("expected_result")
            if len(composition) < 2:
                self.error("EVAL011", path, f"{case_id}: composition requires at least two skills")
            if result not in {"valid", "invalid"}:
                self.error("EVAL012", path, f"{case_id}: expected_result must be valid or invalid")
            if not isinstance(case.get("reason"), str) or not case["reason"].strip():
                self.error("EVAL013", path, f"{case_id}: composition fixture requires a reason")
            if self.catalog_entries and result == "valid":
                active_roles = case.get("active_roles", {})
                primary_count = sum(
                    active_roles.get(name, self.catalog_entries.get(name, {}).get("default_role")) == "primary-executor"
                    for name in composition
                )
                if primary_count != 1:
                    self.error(
                        "EVAL016",
                        path,
                        f"{case_id}: valid composition must contain exactly one primary executor; "
                        f"found {primary_count}",
                    )

        if kind == "end-to-end-delivery":
            for field in ("required_artifacts", "required_gates", "terminal_states"):
                if not isinstance(case.get(field), list) or not case[field]:
                    self.error("EVAL014", path, f"{case_id}: {field} must be a non-empty list")

        if kind == "behavioral-scenarios":
            for field in ("must_include", "must_not_include"):
                if not isinstance(case.get(field), list):
                    self.error("EVAL015", path, f"{case_id}: {field} must be a list")

        if self.catalog_entries:
            primary = case.get("primary") or case.get("expected_primary")
            if isinstance(expected, dict):
                primary = primary or expected.get("primary")
            if (
                isinstance(primary, str)
                and "primary-executor"
                not in value_as_names(self.catalog_entries.get(primary, {}).get("allowed_roles"))
            ):
                self.error(
                    "EVAL017",
                    path,
                    f"{case_id}: expected primary {primary!r} is not cataloged as primary-executor",
                )

    def validate_legacy_conflicts(self) -> None:
        forbidden = {
            "RIC Strengthening Layer": "LEGACY001",
            "simulate Python": "LEGACY002",
            "picsum.photos": "LEGACY003",
            "every card must": "LEGACY004",
            "infinite loop": "LEGACY005",
        }
        for record in self.skills.values():
            text = read_text(record.skill_path, self)
            if text is None:
                continue
            lowered = text.lower()
            for phrase, code in forbidden.items():
                if phrase.lower() in lowered:
                    self.error(code, record.skill_path, f"legacy conflicting rule remains: {phrase!r}")


def read_text(path: Path, validator: Validator) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        validator.error("IO001", path, f"cannot read UTF-8 text: {exc}")
        return None


def load_json(path: Path, validator: Validator) -> Any | None:
    try:
        def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON object key: {key}")
                result[key] = value
            return result

        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        validator.error("JSON001", path, f"invalid JSON: {exc}")
        return None


def parse_yaml_scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.replace(r"\"", '"').replace(r"\'", "'")


def strip_fenced_code(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_char = ""
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
            elif marker[0] == fence_char:
                in_fence = False
                fence_char = ""
            output.append("\n" if line.endswith("\n") else "")
        elif in_fence:
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    return "".join(output)


def clean_markdown_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif re.search(r'\s+["\']', target):
        target = re.split(r'\s+["\']', target, maxsplit=1)[0]
    return target.split("#", 1)[0].split("?", 1)[0].strip()


def is_external_target(target: str) -> bool:
    lowered = target.lower()
    return (
        not target
        or lowered.startswith(("http://", "https://", "mailto:", "data:", "app://"))
        or target.startswith("#")
    )


def normalize_catalog_entries(
    data: Any,
    path: Path,
    validator: Validator,
) -> dict[str, dict[str, Any]]:
    if not isinstance(data, dict) or "skills" not in data:
        validator.error("CAT001", path, "catalog must be an object with a skills property")
        return {}
    raw_entries = data["skills"]
    entries: dict[str, dict[str, Any]] = {}
    if isinstance(raw_entries, dict):
        for name, entry in raw_entries.items():
            if not isinstance(entry, dict):
                validator.error("CAT001", path, f"catalog entry {name!r} must be an object")
                continue
            entries[name] = entry
    elif isinstance(raw_entries, list):
        for index, entry in enumerate(raw_entries):
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
                validator.error("CAT001", path, f"catalog list entry {index} needs a string name")
                continue
            if entry["name"] in entries:
                validator.error("CAT001", path, f"duplicate catalog entry {entry['name']!r}")
                continue
            entries[entry["name"]] = entry
    else:
        validator.error("CAT001", path, "catalog skills must be an object or array")
    return entries


def value_as_names(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {item for item in value if isinstance(item, str)}
    return set()


def get_name_set(entry: dict[str, Any], *keys: str) -> set[str]:
    result: set[str] = set()
    for key in keys:
        result.update(value_as_names(entry.get(key)))
    return result


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: set[tuple[str, ...]] = set()
    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()

    def visit(node: str) -> None:
        if node in active_set:
            start = active.index(node)
            cycle = active[start:] + [node]
            canonical = canonical_cycle(cycle)
            cycles.add(canonical)
            return
        if node in visited:
            return
        active.append(node)
        active_set.add(node)
        for target in sorted(graph.get(node, set())):
            if target in graph:
                visit(target)
        active.pop()
        active_set.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)
    return [list(cycle) for cycle in sorted(cycles)]


def canonical_cycle(cycle: list[str]) -> tuple[str, ...]:
    body = cycle[:-1]
    rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
    best = min(rotations)
    return best + (best[0],)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root; defaults to the parent of scripts/",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="return a failure when warnings are present",
    )
    parser.add_argument("--quiet", action="store_true", help="only print the summary")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    validator = Validator(args.root, warnings_as_errors=args.warnings_as_errors)
    issues = validator.run()
    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    if not args.quiet:
        for issue in issues:
            print(issue.render(validator.root))
    print(
        f"Validated {len(validator.skills)} skills: "
        f"{errors} error(s), {warnings} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

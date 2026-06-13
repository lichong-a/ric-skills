#!/usr/bin/env python3
"""Validate a RIC delivery run using cross-artifact semantic invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from json_schema import validate as validate_schema
from routing_rules import admin_requires_visual_work, request_indicates_visual_work


PASSING = {"PASS", "PASS_WITH_ADVISORIES"}
FAILING_ACCEPTANCE = {"FAIL", "BLOCKED", "NOT_RUN"}
SOURCE_BOUND_GATES = {
    "code-review",
    "security-review",
    "test",
    "visual-review",
    "design-qa",
    "acceptance",
}
BASE_REQUIRED_GATES = {"requirements", "design", "code-review", "security-review", "test", "acceptance"}
REVIEW_RESULT_GATES = {"requirements", "design", "code-review", "security-review", "visual-review", "design-qa", "acceptance"}
SCHEMA_ARTIFACTS = {
    "run.json": "delivery-run.schema.json",
    "acceptance.json": "acceptance.schema.json",
    "traceability.json": "traceability.schema.json",
    "risk-register.json": "risk-register.schema.json",
    "evidence-manifest.json": "evidence-manifest.schema.json",
    "test-plan.json": "test-plan.schema.json",
}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(rb"\b(?:OPENAI_API_KEY|RIC_[A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|KEY))\s*[:=]\s*\S+", re.I),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(rb"\bAuthorization:\s*(?:Bearer|Basic)\s+\S+", re.I),
)
MAX_RUN_FILES = 1000
MAX_RUN_BYTES = 512 * 1024 * 1024
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_JSON_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: Path

    def render(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root).as_posix()
        except ValueError:
            display = self.path.as_posix()
        return f"ERROR [{self.code}] {display}: {self.message}"


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def load_json(path: Path, findings: list[Finding], required: bool = True) -> Any:
    if not path.is_file():
        if required:
            findings.append(Finding("RUN001", f"required artifact is missing: {path.name}", path))
        return None
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            raise ValueError(f"JSON file exceeds {MAX_JSON_BYTES} byte limit")
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-standard JSON constant: {value}")),
        )
    except (OSError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        findings.append(Finding("RUN002", f"invalid JSON: {exc}", path))
        return None


def validate_instance(path: Path, value: Any, schema_path: Path, findings: list[Finding]) -> None:
    schema = load_json(schema_path, findings)
    if not isinstance(schema, dict):
        return
    for message in validate_schema(value, schema):
        findings.append(Finding("SCHEMA100", message, path))


def load_schema_object(
    path: Path,
    schema_path: Path,
    findings: list[Finding],
    required: bool = True,
) -> dict[str, Any] | None:
    value = load_json(path, findings, required=required)
    if value is None:
        return None
    before = len(findings)
    validate_instance(path, value, schema_path, findings)
    if not isinstance(value, dict):
        if len(findings) == before:
            findings.append(Finding("SCHEMA100", "artifact must be a JSON object", path))
        return None
    if len(findings) != before:
        return None
    return value


def git_output(repo: Path, *args: str) -> tuple[int, str]:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.returncode, completed.stdout.strip()


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_ordered_event_chain(events: list[dict[str, Any]], event_types: tuple[str, ...]) -> bool:
    position = 0
    for event in events:
        if event.get("type") == event_types[position]:
            position += 1
            if position == len(event_types):
                return True
    return False


def acceptance_repair_order_is_valid(
    events: list[dict[str, Any]],
    last_failure_sequence: int,
    final_revision: str,
    required_gates: set[str],
    gate_by_type: dict[str, dict[str, Any]],
    fixers: set[str],
    passing_rerun_results: set[tuple[str, str, str]],
) -> bool:
    cursor = last_failure_sequence

    def advance(predicate) -> bool:
        nonlocal cursor
        candidates = [
            event
            for event in events
            if event.get("sequence", 0) > cursor and predicate(event)
        ]
        if not candidates:
            return False
        cursor = min(candidates, key=lambda event: event.get("sequence", 0)).get("sequence", 0)
        return True

    if not advance(
        lambda event: event.get("type") == "fix-applied"
        and event.get("source_revision") == final_revision
        and event.get("actor_id") in fixers
    ):
        return False

    for gate_type in ("code-review", "security-review"):
        reviewers = set(gate_by_type.get(gate_type, {}).get("reviewers", []))
        if gate_type in required_gates and not advance(
            lambda event, gate_type=gate_type, reviewers=reviewers: event.get("type") == "gate-passed"
            and event.get("gate") == gate_type
            and event.get("source_revision") == final_revision
            and event.get("actor_id") in reviewers
        ):
            return False

    test_reviewers = set(gate_by_type.get("test", {}).get("reviewers", []))
    for scope, event_type in (("impacted", "test-impacted-passed"), ("full", "test-full-passed")):
        if not advance(
            lambda event, scope=scope, event_type=event_type: event.get("type") == event_type
            and event.get("gate") == "test"
            and event.get("source_revision") == final_revision
            and event.get("actor_id") in test_reviewers
            and (scope, event.get("suite_id"), event.get("actor_id")) in passing_rerun_results
        ):
            return False

    if not advance(
        lambda event: event.get("type") == "gate-passed"
        and event.get("gate") == "test"
        and event.get("source_revision") == final_revision
        and event.get("actor_id") in test_reviewers
    ):
        return False

    for gate_type in ("visual-review", "design-qa"):
        reviewers = set(gate_by_type.get(gate_type, {}).get("reviewers", []))
        if gate_type in required_gates and not advance(
            lambda event, gate_type=gate_type, reviewers=reviewers: event.get("type") == "gate-passed"
            and event.get("gate") == gate_type
            and event.get("source_revision") == final_revision
            and event.get("actor_id") in reviewers
        ):
            return False

    acceptance_reviewers = set(gate_by_type.get("acceptance", {}).get("reviewers", []))
    return advance(
        lambda event: event.get("type") == "gate-passed"
        and event.get("gate") == "acceptance"
        and event.get("source_revision") == final_revision
        and event.get("actor_id") in acceptance_reviewers
    )


def contains_secret(path: Path) -> bool:
    overlap = b""
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            sample = overlap + chunk
            if any(pattern.search(sample) for pattern in SECRET_PATTERNS):
                return True
            overlap = sample[-512:]
    return False


def validate_run_files(root: Path, findings: list[Finding]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    total = 0
    files: list[Path] = []
    for path in root.rglob("*"):
        is_junction = getattr(path, "is_junction", lambda: False)()
        if path.is_symlink() or is_junction or not inside(root, path):
            findings.append(Finding("EVID014", "run package must not contain links, junctions, or boundary escapes", path))
            continue
        if path.is_file():
            files.append(path)
    if len(files) > MAX_RUN_FILES:
        findings.append(Finding("EVID013", f"run contains more than {MAX_RUN_FILES} files", root))
    for path in files:
        size = path.stat().st_size
        total += size
        if size > MAX_FILE_BYTES:
            findings.append(Finding("EVID015", f"file exceeds {MAX_FILE_BYTES} byte limit", path))
            continue
        if contains_secret(path):
            findings.append(Finding("EVID006", "run artifact appears to contain a secret", path))
        hashes[path.relative_to(root).as_posix()] = sha256(path)
    if total > MAX_RUN_BYTES:
        findings.append(Finding("EVID016", f"run exceeds {MAX_RUN_BYTES} byte limit", root))
    return hashes


def validate_review(
    path: Path,
    review: dict[str, Any],
    run_id: str,
    final_revision: str,
    artifact_versions: dict[str, str],
    findings: list[Finding],
) -> tuple[str | None, str | None]:
    if review.get("run_id") != run_id:
        findings.append(Finding("RUN009", "review result run_id does not match run.json", path))
    decision = review.get("decision")
    if decision not in PASSING:
        return review.get("gate"), review.get("reviewer", {}).get("id")
    reviewer = review.get("reviewer", {})
    reviewer_id = reviewer.get("id")
    if not reviewer_id:
        findings.append(Finding("PASS001", "passing review requires a reviewer identity", path))
    if reviewer_id in set(review.get("artifact_authors", [])) | set(review.get("artifact_fixers", [])):
        findings.append(Finding("PASS002", "reviewer cannot approve an artifact they authored or fixed", path))
    if reviewer.get("fresh_context") is not True:
        findings.append(Finding("PASS003", "passing independent review requires fresh_context=true", path))
    if reviewer.get("read_only") is not True:
        findings.append(Finding("PASS004", "passing independent review requires read_only=true", path))
    gate = review.get("gate")
    if gate in SOURCE_BOUND_GATES and review.get("source_revision") != final_revision:
        findings.append(Finding("REV001", "passing source-bound review is not bound to final source revision", path))
    if gate in {"requirements", "design"}:
        expected_version = artifact_versions.get(gate)
        if not expected_version or review.get("artifact_version") != expected_version:
            findings.append(Finding("REV008", f"passing {gate!r} review is not bound to the current artifact version", path))
    evidence = review.get("evidence", [])
    if not evidence:
        findings.append(Finding("PASS005", "passing review requires non-empty evidence", path))
    for item in review.get("findings", []):
        severity = item.get("severity")
        status = item.get("status", "OPEN")
        if severity in {"S0", "S1"} and status != "RESOLVED":
            findings.append(Finding("PASS006", f"passing review has open {severity} finding", path))
        if severity == "S2" and (
            status not in {"RESOLVED", "ACCEPTED"}
            or not item.get("owner")
            or not item.get("rationale")
            or not item.get("disposition")
        ):
            findings.append(Finding("PASS007", "S2 finding lacks owner, rationale, and disposition", path))
        if decision == "PASS" and status != "RESOLVED":
            findings.append(Finding("PASS021", "plain PASS cannot contain unresolved or accepted findings", path))
        if decision == "PASS_WITH_ADVISORIES" and status != "RESOLVED" and (
            severity not in {"S2", "S3"}
            or status != "ACCEPTED"
            or not item.get("owner")
            or not item.get("rationale")
            or not item.get("disposition")
        ):
            findings.append(Finding("PASS022", "advisory finding lacks accepted status, owner, rationale, or disposition", path))
    visual = review.get("visual_score")
    if gate == "visual-review" and not visual:
        findings.append(Finding("PASS026", "passing visual-review requires a complete visual score", path))
    if visual:
        threshold = 75 if visual.get("surface_class") == "utility" else 82
        if visual.get("total", 0) < threshold:
            findings.append(Finding("PASS008", f"visual score is below required threshold {threshold}", path))
        categories = visual.get("categories", {})
        weighted = (
            categories.get("specificity", 0) * 20
            + categories.get("hierarchy", 0) * 20
            + categories.get("distinctiveness", 0) * 20
            + categories.get("consistency", 0) * 15
            + categories.get("responsive_accessibility", 0) * 15
            + categories.get("asset_fidelity", 0) * 10
        ) / 5
        if abs(visual.get("total", 0) - weighted) > 0.01:
            findings.append(Finding("PASS027", f"visual total does not match weighted category score {weighted:g}", path))
        if visual.get("surface_class") == "utility" and any(score < 3 for score in categories.values()):
            findings.append(Finding("PASS023", "utility visual review has a category below 3/5", path))
        if visual.get("surface_class") == "high-visual" and (
            categories.get("specificity", 0) < 4 or categories.get("distinctiveness", 0) < 4
        ):
            findings.append(Finding("PASS024", "high-visual review requires specificity and distinctiveness of at least 4/5", path))
        if visual.get("surface_class") == "high-visual" and any(
            item.get("severity") == "S2" and item.get("status") != "RESOLVED" for item in review.get("findings", [])
        ):
            findings.append(Finding("PASS025", "high-visual review cannot pass with unresolved actionable S2 findings", path))
    return gate, reviewer_id


def validate_evidence(
    root: Path,
    path: Path,
    manifest: dict[str, Any],
    final_revision: str,
    findings: list[Finding],
) -> set[str]:
    passing = manifest.get("status") in PASSING
    ids: set[str] = set()
    if passing and manifest.get("source_revision") != final_revision:
        findings.append(Finding("REV002", "passing evidence manifest is not bound to final revision", path))
    for item in manifest.get("evidence", []):
        evidence_id = item.get("id")
        if evidence_id:
            if evidence_id in ids:
                findings.append(Finding("EVID007", f"duplicate evidence id: {evidence_id}", path))
            ids.add(evidence_id)
        if passing and item.get("result") != "PASS":
            findings.append(Finding("EVID001", "passing manifest contains failed or unrun evidence", path))
        relative = item.get("path")
        if not relative:
            findings.append(Finding("EVID002", "evidence item is missing path", path))
            continue
        target = root / relative
        if not inside(root, target):
            findings.append(Finding("EVID003", f"evidence path escapes run root: {relative}", path))
            continue
        if not target.is_file():
            findings.append(Finding("EVID004", f"evidence file is missing: {relative}", path))
            continue
        if contains_secret(target):
            findings.append(Finding("EVID006", f"evidence appears to contain a secret: {relative}", path))
        expected = item.get("sha256")
        if not expected or sha256(target) != expected:
            findings.append(Finding("EVID005", f"evidence hash is missing or mismatched: {relative}", path))
        if passing and item.get("source_revision") != final_revision:
            findings.append(Finding("REV003", f"evidence is stale: {relative}", path))
    for criterion in manifest.get("acceptance_coverage", []):
        if passing and criterion.get("status") in FAILING_ACCEPTANCE:
            findings.append(Finding("AC001", "passing manifest contains failed, blocked, or unrun acceptance", path))
        if passing and not criterion.get("evidence_ids"):
            findings.append(Finding("AC002", "passing acceptance criterion requires evidence", path))
        unknown = set(criterion.get("evidence_ids", [])) - ids
        if unknown:
            findings.append(Finding("EVID008", f"acceptance coverage references unknown evidence: {sorted(unknown)}", path))
    return ids


def validate_run(root: Path, repo_root: Path | None = None, require_repo_revision: bool = False) -> list[Finding]:
    root = root.resolve()
    repository = Path(__file__).resolve().parents[1]
    schemas = repository / "schemas"
    findings: list[Finding] = []
    validate_run_files(root, findings)
    run_path = root / "run.json"
    run = load_json(run_path, findings)
    acceptance = load_json(root / "acceptance.json", findings)
    traceability = load_json(root / "traceability.json", findings)
    risk_register = load_json(root / "risk-register.json", findings)
    manifest = load_json(root / "evidence-manifest.json", findings)
    if not all(isinstance(item, dict) for item in (run, acceptance, traceability, risk_register, manifest)):
        return findings
    schema_finding_count = len(findings)
    for filename, value in {
        "run.json": run,
        "acceptance.json": acceptance,
        "traceability.json": traceability,
        "risk-register.json": risk_register,
        "evidence-manifest.json": manifest,
    }.items():
        validate_instance(root / filename, value, schemas / SCHEMA_ARTIFACTS[filename], findings)
    if len(findings) != schema_finding_count:
        return findings
    collections = [
        run.get("selected_skills"),
        run.get("gates"),
        run.get("events"),
        acceptance.get("criteria"),
        traceability.get("links"),
        risk_register.get("risks"),
        manifest.get("acceptance_coverage"),
        manifest.get("evidence"),
    ]
    if any(not isinstance(items, list) or any(not isinstance(item, dict) for item in items) for items in collections):
        return findings
    for human_file in ("requirements.md", "design.md"):
        if not (root / human_file).is_file():
            findings.append(Finding("RUN004", f"required human-readable artifact is missing: {human_file}", root / human_file))

    final_revision = run.get("final_source_revision")
    run_id = run.get("run_id", "")
    for filename, artifact in {
        "acceptance.json": acceptance,
        "traceability.json": traceability,
        "risk-register.json": risk_register,
        "evidence-manifest.json": manifest,
    }.items():
        if artifact.get("run_id") != run_id:
            findings.append(Finding("RUN014", f"{filename} run_id does not match run.json", root / filename))
    if not final_revision:
        findings.append(Finding("RUN003", "final_source_revision is required", run_path))
        final_revision = ""
    if run.get("epoch", 0) > 3:
        findings.append(Finding("LOOP001", "run epoch exceeds the maximum of three", run_path))
    if run.get("degraded_mode") and run.get("status") in PASSING:
        findings.append(Finding("PASS009", "degraded mode must remain BLOCKED", run_path))
    if run.get("status") in PASSING and require_repo_revision:
        if repo_root is None:
            findings.append(Finding("REV011", "passing run requires a repository root for Git revision verification", run_path))
        else:
            code, head = git_output(repo_root.resolve(), "rev-parse", "HEAD")
            if code != 0 or head != final_revision:
                findings.append(Finding("REV012", "final_source_revision does not equal the repository HEAD", run_path))

    live_path = root / "live-eval-result.json"
    if live_path.exists():
        live = load_schema_object(live_path, schemas / "live-eval-result.schema.json", findings)
        if live is not None:
            if live.get("run_id") != run_id or live.get("source_revision") != final_revision:
                findings.append(Finding("LIVE001", "live eval is not bound to this run and final revision", live_path))
            if run.get("status") in PASSING:
                if live.get("status") != "PASS":
                    findings.append(Finding("LIVE002", "a passing delivery run cannot contain a non-passing live eval result", live_path))
                for result in live.get("results", []):
                    if result.get("result") not in ("PASS",):
                        findings.append(Finding("LIVE003", f"live eval scenario {result.get('scenario_id')!r} did not pass", live_path))
                    if result.get("fresh_context") is not True:
                        findings.append(Finding("LIVE004", f"live eval scenario {result.get('scenario_id')!r} lacks fresh_context=true", live_path))
                    if result.get("validation_errors"):
                        findings.append(Finding("LIVE005", f"live eval scenario {result.get('scenario_id')!r} has validation errors", live_path))

    selected = run.get("selected_skills", [])
    catalog_path = repository / "skills" / "catalog.json"
    catalog = load_json(catalog_path, findings)
    if isinstance(catalog, dict):
        before_catalog = len(findings)
        validate_instance(catalog_path, catalog, schemas / "catalog.schema.json", findings)
        if len(findings) != before_catalog:
            findings.append(Finding("CAT001", "catalog instance failed schema validation; semantic checks skipped", catalog_path))
            catalog = {}
    else:
        catalog = {}
    catalog_skills = catalog.get("skills", {}) if isinstance(catalog, dict) else {}
    if not isinstance(catalog_skills, dict):
        catalog_skills = {}
    catalog_capabilities = set()
    raw_capabilities = catalog.get("capabilities", []) if isinstance(catalog, dict) else []
    if isinstance(raw_capabilities, list):
        for cap in raw_capabilities:
            if isinstance(cap, str):
                catalog_capabilities.add(cap)
    unknown_capabilities = set(run.get("capabilities", [])) - catalog_capabilities
    if unknown_capabilities:
        findings.append(Finding("ROLE010", f"run declares unknown capabilities: {sorted(unknown_capabilities)}", run_path))
    gate_skills = {
        gate_type: name
        for name, entry in catalog_skills.items()
        for gate_type in entry.get("gate_types", [])
    }
    selected_names: set[str] = set()
    for item in selected:
        name = item.get("name")
        role = item.get("active_role")
        if name in selected_names:
            findings.append(Finding("ROLE002", f"selected skill is duplicated: {name}", run_path))
        selected_names.add(name)
        if name not in catalog_skills:
            findings.append(Finding("ROLE003", f"selected skill is not in catalog: {name}", run_path))
            continue
        entry_data = catalog_skills.get(name)
        if not isinstance(entry_data, dict):
            findings.append(Finding("CAT002", f"catalog entry for {name!r} is not an object", run_path))
            continue
        if role not in entry_data.get("allowed_roles", []):
            findings.append(Finding("ROLE004", f"skill {name!r} does not allow active role {role!r}", run_path))
    if run.get("status") in PASSING:
        if len([s for s in selected if s.get("active_role") == "orchestrator"]) != 1 or "ric-delivery-loop" not in selected_names:
            findings.append(Finding("ROLE005", "passing run requires exactly one ric-delivery-loop orchestrator", run_path))
        for name in selected_names & set(catalog_skills):
            missing_companions = set(entry_data.get("required_companions", [])) - selected_names
            if missing_companions:
                findings.append(Finding("ROLE006", f"selected skill {name!r} lacks required companions: {sorted(missing_companions)}", run_path))
            selected_conflicts = set(entry_data.get("conflicts", [])) & selected_names
            if selected_conflicts:
                findings.append(Finding("ROLE008", f"selected skill {name!r} conflicts with {sorted(selected_conflicts)}", run_path))
        primary_names = {item.get("name") for item in selected if item.get("active_role") == "primary-executor"}
        required_gate_skills = {
            gate_skill
            for item in selected
            if item.get("active_role") not in {"quality-gate", "policy", "runtime", "handoff"}
            for name in [item.get("name")]
            for gate_skill in catalog_skills.get(name, {}).get("quality_gates", [])
        }
        active_capabilities = set(run.get("capabilities", []))
        required_gate_skills.update(
            gate_skill
            for item in selected
            if item.get("active_role") not in {"quality-gate", "policy", "runtime", "handoff"}
            for name in [item.get("name")]
            for capability, gate_names in catalog_skills.get(name, {}).get("conditional_quality_gates", {}).items()
            if capability in active_capabilities
            for gate_skill in gate_names
        )
        required_gate_types = {
            gate_type
            for gate_skill in required_gate_skills
            for gate_type in catalog_skills.get(gate_skill, {}).get("gate_types", [])
        }
        missing_domain_gates = required_gate_types - set(run.get("required_gates", []))
        if missing_domain_gates:
            findings.append(Finding("ROLE009", f"active skills omit catalog quality gates: {sorted(missing_domain_gates)}", run_path))
        for gate in run.get("required_gates", []):
            gate_skill = gate_skills.get(gate)
            if gate_skill and gate_skill not in selected_names:
                findings.append(Finding("ROLE007", f"required gate {gate!r} lacks selected skill {gate_skill!r}", run_path))
        request_lower = str(run.get("request", "")).lower()
        primary_admin = "ric-admin-console" in primary_names
        if primary_admin and "react" in request_lower and not any(term in request_lower for term in ("existing ant", "ant design", "antd")):
            if "shadcn" not in active_capabilities:
                findings.append(Finding("ROLE011", "new React admin delivery must record the shadcn capability route", run_path))
        if primary_admin and admin_requires_visual_work(str(run.get("request", ""))):
            if "visual-work" not in active_capabilities:
                findings.append(Finding("ROLE012", "visual admin delivery must record visual-work capability", run_path))
            missing_visual = {"visual-review", "design-qa"} - set(run.get("required_gates", []))
            if missing_visual:
                findings.append(Finding("ROLE013", f"visual admin delivery omits visual gates: {sorted(missing_visual)}", run_path))
        visual_modifier_active = any(
            item.get("active_role") == "modifier"
            and catalog_skills.get(item.get("name"), {}).get("default_role") == "modifier"
            and any(gate in catalog_skills.get(item.get("name"), {}).get("quality_gates", []) for gate in ("visual-review", "design-qa"))
            for item in selected
        )
        request_needs_visual = request_indicates_visual_work(str(run.get("request", "")))
        if (visual_modifier_active or request_needs_visual) and run.get("status") in PASSING:
            if "visual-work" not in active_capabilities:
                findings.append(Finding("ROLE014", "visual delivery must record visual-work capability", run_path))
            missing_visual = {"visual-review", "design-qa"} - set(run.get("required_gates", []))
            if missing_visual:
                findings.append(Finding("ROLE015", f"visual delivery omits visual gates: {sorted(missing_visual)}", run_path))
    if len([s for s in selected if s.get("active_role") == "primary-executor"]) != 1:
        findings.append(Finding("ROLE001", "run requires exactly one active primary executor", run_path))

    gate_types: set[str] = set()
    gate_by_type: dict[str, dict[str, Any]] = {}
    artifact_versions = run.get("artifact_versions", {})
    actors = run.get("actors", {})
    authors = set(actors.get("authors", []))
    fixers = set(actors.get("fixers", []))
    events = run.get("events", [])
    if run.get("status") in PASSING and not authors:
        findings.append(Finding("PASS031", "a passing non-trivial delivery run must declare at least one author", run_path))
    known_gate_types = {
        gate.get("type")
        for gate in run.get("gates", [])
        if isinstance(gate.get("type"), str)
    }
    gate_scoped_events = {
        "gate-passed",
        "gate-failed",
        "results-invalidated",
        "test-impacted-passed",
        "test-full-passed",
        "adjudicated",
    }
    for event in events:
        if event.get("type") in gate_scoped_events and event.get("gate") not in known_gate_types:
            findings.append(
                Finding(
                    "LOOP013",
                    "gate-scoped lifecycle event requires a known gate",
                    run_path,
                )
            )
        if event.get("type") == "fix-applied":
            if event.get("gate") is not None and event.get("gate") not in known_gate_types:
                findings.append(Finding("LOOP013", "scoped fix event requires a known gate", run_path))
            if run.get("status") in PASSING and event.get("source_revision") != final_revision:
                findings.append(Finding("LOOP015", "passing run contains a fix that is not bound to final_source_revision", run_path))
            if event.get("actor_id") not in fixers:
                findings.append(Finding("LOOP016", "fix-applied event actor is not a declared fixer", run_path))
    sequences = [event.get("sequence") for event in events]
    if sequences != list(range(1, len(events) + 1)):
        findings.append(Finding("LOOP003", "run event sequence must be contiguous and ordered from 1", run_path))
    passed_event_gates = {event.get("gate") for event in events if event.get("type") == "gate-passed"}
    if run.get("status") in PASSING:
        missing_gate_events = set(run.get("required_gates", [])) - passed_event_gates
        if missing_gate_events:
            findings.append(Finding("LOOP004", f"passing gates lack gate-passed history events: {sorted(missing_gate_events)}", run_path))
    if run.get("epoch", 1) > 1 and not any(event.get("type") in {"return-to-requirements", "return-to-design"} for event in events):
        findings.append(Finding("LOOP005", "multi-epoch run lacks a recorded return to requirements or design", run_path))
    for gate in run.get("gates", []):
        gate_type = gate.get("type")
        if gate_type in gate_types:
            findings.append(Finding("PASS028", f"run contains duplicate current gate type: {gate_type!r}", run_path))
        gate_types.add(gate_type)
        gate_by_type[gate_type] = gate
        if gate.get("iteration", 0) > 3:
            findings.append(Finding("LOOP002", f"gate {gate_type!r} exceeds three iterations", run_path))
        if gate.get("iteration", 1) > 1:
            gate_events = [event for event in events if event.get("gate") == gate_type]
            if not has_ordered_event_chain(gate_events, ("gate-failed", "fix-applied", "results-invalidated", "gate-passed")):
                findings.append(Finding("LOOP006", f"reworked gate {gate_type!r} lacks ordered failure/fix/invalidation/pass history", run_path))
        if gate.get("decision") in PASSING:
            reviewers = gate.get("reviewers", [])
            if not reviewers:
                findings.append(Finding("PASS010", f"passing gate {gate_type!r} has no reviewers", run_path))
            if gate_type in {"requirements", "design"} and len(set(reviewers)) < 2:
                findings.append(Finding("PASS015", f"passing {gate_type!r} gate requires two reviewers", run_path))
            if set(reviewers) & (authors | fixers):
                findings.append(Finding("PASS016", f"passing gate {gate_type!r} includes an author or fixer", run_path))
            if gate.get("source_revision") != final_revision and gate_type in SOURCE_BOUND_GATES:
                findings.append(Finding("REV004", f"passing source-bound gate {gate_type!r} is stale", run_path))
            expected_versions = run.get("artifact_versions", {})
            for artifact, version in gate.get("artifact_versions", {}).items():
                if expected_versions.get(artifact) != version:
                    findings.append(Finding("REV005", f"passing gate {gate_type!r} uses stale {artifact!r}", run_path))
            if gate_type in {"requirements", "design"} and gate.get("artifact_versions", {}).get(gate_type) != expected_versions.get(gate_type):
                findings.append(Finding("REV009", f"passing {gate_type!r} gate is not bound to its current artifact version", run_path))
            pass_events = [
                event
                for event in events
                if event.get("gate") == gate_type and event.get("type") == "gate-passed" and event.get("actor_id") in reviewers
            ]
            if gate_type in SOURCE_BOUND_GATES:
                pass_events = [event for event in pass_events if event.get("source_revision") == final_revision]
            elif gate_type in {"requirements", "design"}:
                pass_events = [
                    event
                    for event in pass_events
                    if event.get("artifact_version") == expected_versions.get(gate_type)
                ]
            if not pass_events:
                findings.append(Finding("PASS029", f"passing gate {gate_type!r} lacks a current reviewer-bound gate-passed event", run_path))
            gate_events = [event for event in events if event.get("gate") == gate_type]
            global_invalidators = [
                event
                for event in events
                if event.get("type") in {"return-to-requirements", "return-to-design"}
                or (gate_type in SOURCE_BOUND_GATES and event.get("type") == "fix-applied")
            ]
            effective_events = gate_events + global_invalidators
            if effective_events:
                terminal = max(effective_events, key=lambda event: event.get("sequence", 0))
                if terminal.get("type") != "gate-passed" or terminal not in pass_events:
                    findings.append(Finding("PASS030", f"passing gate {gate_type!r} is invalidated by its terminal lifecycle event", run_path))

    if run.get("status") in PASSING:
        required = set(run.get("required_gates", []))
        missing_base = BASE_REQUIRED_GATES - required
        if missing_base:
            findings.append(Finding("PASS017", f"passing delivery run omits base required gates: {sorted(missing_base)}", run_path))
        missing = required - gate_types
        if missing:
            findings.append(Finding("PASS011", f"passing run is missing required gates: {sorted(missing)}", run_path))
        for gate in run.get("gates", []):
            if gate.get("type") in required and gate.get("decision") not in PASSING:
                findings.append(Finding("PASS012", f"required gate {gate.get('type')!r} did not pass", run_path))
        acceptance_gate = gate_by_type.get("acceptance", {})
        acceptance_failures = [
            event
            for event in events
            if event.get("gate") == "acceptance" and event.get("type") == "gate-failed"
        ]
        if acceptance_gate.get("iteration", 1) > 1 or acceptance_failures:
            last_failure_event = max(acceptance_failures, key=lambda event: event.get("sequence", 0), default={})
            last_failure = last_failure_event.get("sequence", 0)
            final_revision_fixes = [
                event
                for event in events
                if event.get("sequence", 0) > last_failure
                and event.get("type") == "fix-applied"
                and event.get("source_revision") == final_revision
            ]
            if not last_failure_event.get("source_revision") or last_failure_event.get("source_revision") == final_revision or not final_revision_fixes:
                findings.append(
                    Finding(
                        "LOOP014",
                        "acceptance repair cycle must fail on an older revision and bind the fix to the final revision",
                        run_path,
                    )
                )
            required_source_gates = SOURCE_BOUND_GATES & required
            invalidated_after = {
                event.get("gate")
                for event in events
                if event.get("sequence", 0) > last_failure and event.get("type") == "results-invalidated"
            }
            missing_invalidations = required_source_gates - invalidated_after
            if missing_invalidations:
                findings.append(Finding("LOOP011", f"acceptance repair cycle omits source-bound invalidations: {sorted(missing_invalidations)}", run_path))
    review_dir = root / "review-results"
    reviewed_by_gate: dict[str, set[str]] = {}
    review_evidence_refs: set[str] = set()
    for path in sorted(review_dir.glob("*.json")) if review_dir.is_dir() else []:
        review = load_schema_object(path, schemas / "review-result.schema.json", findings, required=False)
        if review is None:
            continue
        gate, reviewer = validate_review(path, review, run_id, final_revision, artifact_versions, findings)
        if gate and reviewer and review.get("decision") in PASSING:
            reviewed_by_gate.setdefault(gate, set()).add(reviewer)
            review_evidence_refs.update(review.get("evidence", []))

    if run.get("status") in PASSING:
        for gate_type in REVIEW_RESULT_GATES & set(run.get("required_gates", [])):
            expected_reviewers = set(gate_by_type.get(gate_type, {}).get("reviewers", []))
            missing_results = expected_reviewers - reviewed_by_gate.get(gate_type, set())
            if missing_results:
                findings.append(Finding("PASS018", f"gate {gate_type!r} lacks passing review results for {sorted(missing_results)}", run_path))

    test_dir = root / "test-results"
    passing_test_executors: set[str] = set()
    test_evidence_refs: set[str] = set()
    passing_suite_ids: set[str] = set()
    planned_suite_ids: set[str] = set()
    mandatory_suite_ids: set[str] = set()
    passing_rerun_scopes: set[str] = set()
    passing_rerun_results: set[tuple[str, str, str]] = set()
    if "test" in set(run.get("required_gates", [])):
        test_plan = load_schema_object(root / "test-plan.json", schemas / "test-plan.schema.json", findings)
        if test_plan is not None:
            if test_plan.get("run_id") != run_id:
                findings.append(Finding("RUN010", "test plan run_id does not match run.json", root / "test-plan.json"))
            if test_plan.get("source_revision") != final_revision:
                findings.append(Finding("REV007", "test plan is not bound to final source revision", root / "test-plan.json"))
            for suite in test_plan.get("suites", []):
                suite_id = suite.get("id")
                if not suite_id:
                    continue
                if suite_id in planned_suite_ids:
                    findings.append(Finding("TEST002", f"duplicate test suite id: {suite_id}", root / "test-plan.json"))
                planned_suite_ids.add(suite_id)
                if suite.get("mandatory"):
                    mandatory_suite_ids.add(suite_id)
    for path in sorted(test_dir.glob("*.json")) if test_dir.is_dir() else []:
        result = load_schema_object(path, schemas / "test-result.schema.json", findings, required=False)
        if result is None:
            continue
        if result.get("run_id") != run_id:
            findings.append(Finding("RUN011", "test result run_id does not match run.json", path))
        if run.get("status") in PASSING and result.get("result") != "PASS":
            findings.append(Finding("TEST001", "passing run contains a failed, blocked, or unrun test result", path))
        if result.get("source_revision") != final_revision:
            findings.append(Finding("REV006", "test result is not bound to final source revision", path))
        if result.get("result") == "PASS" and result.get("executor"):
            if result.get("fresh_context") is not True:
                findings.append(Finding("TEST006", "passing test result requires fresh_context=true", path))
            if result.get("read_only") is not True:
                findings.append(Finding("TEST007", "passing test executor must be read-only for production code", path))
            if result.get("executor") in authors | fixers:
                findings.append(Finding("TEST008", "author or fixer cannot approve the run as a test executor", path))
            passing_test_executors.add(result["executor"])
            passing_suite_ids.add(result.get("suite_id"))
            passing_rerun_scopes.add(result.get("rerun_scope"))
            passing_rerun_results.add((result.get("rerun_scope"), result.get("suite_id"), result.get("executor")))
            test_evidence_refs.update(result.get("evidence", []))
        if planned_suite_ids and result.get("suite_id") not in planned_suite_ids:
            findings.append(Finding("TEST003", f"test result references unknown suite: {result.get('suite_id')!r}", path))
    if run.get("status") in PASSING and "test" in set(run.get("required_gates", [])):
        expected_testers = set(gate_by_type.get("test", {}).get("reviewers", []))
        if expected_testers - passing_test_executors:
            findings.append(Finding("PASS019", "test gate lacks passing results from its declared executors", run_path))
        if not mandatory_suite_ids:
            findings.append(Finding("TEST010", "passing test gate requires at least one mandatory suite", root / "test-plan.json"))
        missing_mandatory_suites = mandatory_suite_ids - passing_suite_ids
        if missing_mandatory_suites:
            findings.append(Finding("TEST004", f"mandatory test suites lack passing results: {sorted(missing_mandatory_suites)}", root / "test-plan.json"))
        mandatory_acceptance_ids = {
            crit.get("id")
            for crit in acceptance.get("criteria", [])
            if crit.get("id") and crit.get("mandatory") is not False
        }
        acceptance_to_suites: dict[str, set[str]] = {}
        for suite in (test_plan.get("suites", []) if isinstance(test_plan, dict) else []):
            if not suite.get("mandatory"):
                continue
            for acc_id in suite.get("acceptance_ids", []):
                acceptance_to_suites.setdefault(acc_id, set()).add(suite.get("id"))
        for acc_id in sorted(mandatory_acceptance_ids):
            if acc_id not in acceptance_to_suites:
                findings.append(Finding("TEST011", f"mandatory acceptance criterion {acc_id!r} is not mapped to any mandatory test suite", root / "test-plan.json"))
        acceptance_gate = gate_by_type.get("acceptance", {})
        if acceptance_gate.get("iteration", 1) > 1 and not {"impacted", "full"} <= passing_rerun_scopes:
            findings.append(Finding("TEST009", "acceptance repair cycle requires passing impacted and full rerun scopes", root / "test-results"))
        acceptance_failures = [
            event
            for event in events
            if event.get("gate") == "acceptance" and event.get("type") == "gate-failed"
        ]
        if acceptance_gate.get("iteration", 1) > 1 or acceptance_failures:
            last_failure = max((event.get("sequence", 0) for event in acceptance_failures), default=0)
            if not acceptance_repair_order_is_valid(
                events,
                last_failure,
                final_revision,
                set(run.get("required_gates", [])),
                gate_by_type,
                fixers,
                passing_rerun_results,
            ):
                findings.append(
                    Finding(
                        "LOOP012",
                        "acceptance repair cycle lacks final-revision, authorized, evidence-backed re-review, test, visual, and acceptance order",
                        run_path,
                    )
                )

    evidence_ids = validate_evidence(root, root / "evidence-manifest.json", manifest, final_revision, findings)
    unknown_review_evidence = review_evidence_refs - evidence_ids
    if unknown_review_evidence:
        findings.append(Finding("EVID009", f"passing reviews reference unknown evidence: {sorted(unknown_review_evidence)}", root / "review-results"))
    unknown_test_evidence = test_evidence_refs - evidence_ids
    if unknown_test_evidence:
        findings.append(Finding("EVID010", f"passing tests reference unknown evidence: {sorted(unknown_test_evidence)}", root / "test-results"))
    criteria = acceptance.get("criteria", [])
    criterion_ids = [item.get("id") for item in criteria if item.get("id")]
    if len(criterion_ids) != len(set(criterion_ids)):
        findings.append(Finding("AC003", "acceptance criterion IDs must be unique", root / "acceptance.json"))
    traced = {item.get("acceptance_id") for item in traceability.get("links", [])}
    missing_trace = set(criterion_ids) - traced
    if missing_trace:
        findings.append(Finding("TRACE001", f"acceptance criteria lack traceability: {sorted(missing_trace)}", root / "traceability.json"))
    for link in traceability.get("links", []):
        unknown = set(link.get("evidence_refs", [])) - evidence_ids
        if unknown:
            findings.append(Finding("EVID011", f"traceability references unknown evidence: {sorted(unknown)}", root / "traceability.json"))
        unknown_suites = set(link.get("test_refs", [])) - planned_suite_ids
        if planned_suite_ids and unknown_suites:
            findings.append(Finding("TEST005", f"traceability references unknown test suites: {sorted(unknown_suites)}", root / "traceability.json"))
    coverage_by_id: dict[str, dict[str, Any]] = {}
    for coverage in manifest.get("acceptance_coverage", []):
        coverage_id = coverage.get("id")
        if not coverage_id:
            continue
        if coverage_id in coverage_by_id:
            findings.append(Finding("AC006", f"duplicate acceptance coverage id: {coverage_id}", root / "evidence-manifest.json"))
        coverage_by_id.setdefault(coverage_id, coverage)
    for criterion in criteria:
        unknown = set(criterion.get("expected_evidence", [])) - evidence_ids
        if run.get("status") in PASSING and unknown:
            findings.append(Finding("EVID012", f"acceptance criterion {criterion.get('id')!r} expects unknown evidence: {sorted(unknown)}", root / "acceptance.json"))
        coverage = coverage_by_id.get(criterion.get("id"), {})
        missing_expected = set(criterion.get("expected_evidence", [])) - set(coverage.get("evidence_ids", []))
        if run.get("status") in PASSING and missing_expected:
            findings.append(
                Finding(
                    "AC005",
                    f"acceptance criterion {criterion.get('id')!r} coverage omits expected evidence: {sorted(missing_expected)}",
                    root / "evidence-manifest.json",
                )
            )
    covered = {item.get("id") for item in manifest.get("acceptance_coverage", [])}
    if run.get("status") in PASSING and set(criterion_ids) - covered:
        findings.append(Finding("AC004", "passing run lacks evidence coverage for acceptance criteria", root / "evidence-manifest.json"))
    if run.get("status") in PASSING:
        for risk in risk_register.get("risks", []):
            if risk.get("severity") in {"S0", "S1"} and risk.get("status") not in {"MITIGATED", "CLOSED"}:
                findings.append(Finding("RISK001", "passing run contains open S0/S1 risk", root / "risk-register.json"))
            if risk.get("severity") == "S2" and (
                risk.get("status") not in {"MITIGATED", "ACCEPTED", "CLOSED"}
                or not risk.get("owner")
                or not risk.get("disposition")
            ):
                findings.append(Finding("RISK002", "passing run contains undisposed S2 risk", root / "risk-register.json"))
    if run.get("status") in PASSING and manifest.get("status") not in PASSING:
        findings.append(Finding("PASS013", "passing run requires a passing evidence manifest", run_path))
    if run.get("status") in PASSING and not list(review_dir.glob("*.json")):
        findings.append(Finding("PASS014", "passing run requires independent review result files", run_path))
    if run.get("status") in PASSING:
        gate_actor_ids = [actor for gate in run.get("gates", []) if gate.get("type") in set(run.get("required_gates", [])) for actor in gate.get("reviewers", [])]
        if len(gate_actor_ids) != len(set(gate_actor_ids)):
            findings.append(Finding("PASS020", "required gates must use distinct independent actor identities", run_path))
        if not (root / "handoff.md").is_file():
            findings.append(Finding("RUN005", "passing run requires handoff.md", root / "handoff.md"))
        dispatch_dir = root / "dispatch"
        if not dispatch_dir.is_dir() or not list(dispatch_dir.glob("*.json")):
            findings.append(Finding("RUN006", "passing run requires independent dispatch packets", dispatch_dir))
        else:
            dispatched: set[str] = set()
            dispatched_roles: dict[str, str] = {}
            primary_name = next(
                (item.get("name") for item in selected if item.get("active_role") == "primary-executor"),
                None,
            )
            gate_skill_requirements = {
                "requirements": {"ric-independent-review"},
                "design": {"ric-independent-review"},
                "code-review": {"ric-independent-review", "ric-code-review"},
                "security-review": {"ric-independent-review", "ric-security-review"},
                "test": {"ric-testing-quality"},
                "visual-review": {"ric-independent-review", "ric-visual-design-review"},
                "design-qa": {"ric-independent-review", "ric-design-qa"},
                "acceptance": {"ric-independent-review", "ric-acceptance-validation"},
            }
            role_skill_requirements = {
                "requirements-reviewer": {"ric-independent-review", "ric-requirements-engineering"},
                "requirements-security-reviewer": {"ric-independent-review", "ric-security-review"},
                "design-reviewer": {"ric-independent-review", "ric-solution-design"},
                "design-security-reviewer": {"ric-independent-review", "ric-solution-design", "ric-security-review"},
                "code-reviewer": {"ric-independent-review", "ric-code-review"},
                "security-reviewer": {"ric-independent-review", "ric-security-review"},
                "test-executor": {"ric-testing-quality"},
                "visual-reviewer": {"ric-independent-review", "ric-visual-design-review"},
                "design-qa-reviewer": {"ric-independent-review", "ric-design-qa"},
                "acceptance-validator": {"ric-independent-review", "ric-acceptance-validation"},
            }
            role_gate_requirements = {
                "requirements-reviewer": {"requirements"},
                "requirements-security-reviewer": {"requirements"},
                "design-reviewer": {"design"},
                "design-security-reviewer": {"design"},
                "code-reviewer": {"code-review"},
                "security-reviewer": {"security-review"},
                "test-executor": {"test"},
                "visual-reviewer": {"visual-review"},
                "design-qa-reviewer": {"design-qa"},
                "acceptance-validator": {"acceptance"},
            }
            for path in dispatch_dir.glob("*.json"):
                packet = load_schema_object(path, schemas / "dispatch.schema.json", findings, required=False)
                if packet is None:
                    continue
                actor_id = packet.get("actor_id")
                if packet.get("run_id") != run_id:
                    findings.append(Finding("RUN012", "dispatch packet run_id does not match run.json", path))
                if actor_id:
                    dispatched.add(actor_id)
                    dispatched_roles[actor_id] = str(packet.get("role", ""))
                if packet.get("fresh_context") is not True or packet.get("read_only") is not True:
                    findings.append(Finding("RUN007", "independent dispatch packet requires fresh_context=true and read_only=true", path))
                actor_gates = {
                    gate.get("type")
                    for gate in run.get("gates", [])
                    if actor_id in set(gate.get("reviewers", []))
                }
                required_skills = set(packet.get("required_skills", []))
                expected_skills = {
                    skill
                    for gate_type in actor_gates
                    for skill in gate_skill_requirements.get(gate_type, set())
                }
                role = packet.get("role")
                if role in role_skill_requirements:
                    expected_skills.update(role_skill_requirements[role])
                expected_skills.update(
                    item.get("name")
                    for item in selected
                    if item.get("active_role") == "modifier"
                    and any(
                        gate_skills.get(gate_type) in catalog_skills.get(item.get("name"), {}).get("quality_gates", [])
                        for gate_type in actor_gates
                    )
                )
                if actor_gates and role_gate_requirements.get(role) != actor_gates:
                    findings.append(
                        Finding(
                            "RUN019",
                            f"dispatch role {role!r} does not match assigned gates: {sorted(actor_gates)}",
                            path,
                        )
                    )
                if primary_name:
                    expected_skills.add(primary_name)
                missing_dispatch_skills = expected_skills - required_skills
                if missing_dispatch_skills:
                    findings.append(Finding("RUN015", f"dispatch packet omits required skills: {sorted(missing_dispatch_skills)}", path))
                unknown_dispatch_skills = required_skills - set(catalog_skills)
                if unknown_dispatch_skills:
                    findings.append(Finding("RUN016", f"dispatch packet references unknown skills: {sorted(unknown_dispatch_skills)}", path))
                if actor_gates & SOURCE_BOUND_GATES and packet.get("source_revision") != final_revision:
                    findings.append(Finding("REV013", "source-bound dispatch packet is not bound to final revision", path))
                if "requirements" in actor_gates and packet.get("artifact_version") != artifact_versions.get("requirements"):
                    findings.append(Finding("REV014", "requirements reviewer dispatch is not bound to current artifact version", path))
                if "design" in actor_gates and packet.get("artifact_version") != artifact_versions.get("design"):
                    findings.append(Finding("REV015", "design reviewer dispatch is not bound to current artifact version", path))
            missing_dispatch = set(gate_actor_ids) - dispatched
            if missing_dispatch:
                findings.append(Finding("RUN008", f"gate actors lack dispatch packets: {sorted(missing_dispatch)}", dispatch_dir))
            requirements_actors = set(gate_by_type.get("requirements", {}).get("reviewers", []))
            requirement_roles = {dispatched_roles.get(actor) for actor in requirements_actors}
            if requirements_actors and not {"requirements-reviewer", "requirements-security-reviewer"} <= requirement_roles:
                findings.append(Finding("RUN017", "requirements gate needs completeness and security reviewer dispatch roles", dispatch_dir))
            design_actors = set(gate_by_type.get("design", {}).get("reviewers", []))
            design_roles = {dispatched_roles.get(actor) for actor in design_actors}
            if design_actors and "design-security-reviewer" not in design_roles:
                findings.append(Finding("RUN018", "design gate needs a design-security-reviewer dispatch role", dispatch_dir))
        required_adjudication_gates = {
            gate.get("type")
            for gate in run.get("gates", [])
            if gate.get("iteration", 0) >= 3
        } | {
            event.get("gate")
            for event in events
            if event.get("type") == "adjudicated" and event.get("gate") in gate_types
        }
        if actors.get("adjudicators") and not required_adjudication_gates:
            findings.append(Finding("LOOP007", "declared adjudicator requires an exhausted or adjudicated gate", run_path))
        if required_adjudication_gates:
            adjudication_dir = root / "adjudication-results"
            if not adjudication_dir.is_dir() or not list(adjudication_dir.glob("*.json")):
                findings.append(Finding("LOOP007", "adjudication evidence is required for exhausted or adjudicated runs", adjudication_dir))
            else:
                adjudicated_by: set[str] = set()
                passing_adjudicated_gates: set[str] = set()
                for path in adjudication_dir.glob("*.json"):
                    result = load_schema_object(path, schemas / "adjudication-result.schema.json", findings, required=False)
                    if result is None:
                        continue
                    adjudicator = result.get("adjudicator")
                    gate = result.get("gate")
                    valid = True
                    if result.get("run_id") != run_id:
                        findings.append(Finding("RUN013", "adjudication result run_id does not match run.json", path))
                        valid = False
                    adjudicated_by.add(adjudicator)
                    if result.get("fresh_context") is not True or result.get("read_only") is not True:
                        findings.append(Finding("LOOP008", "adjudicator must be fresh-context and read-only", path))
                        valid = False
                    if adjudicator in authors | fixers | set(gate_actor_ids):
                        findings.append(Finding("LOOP009", "adjudicator must be independent from authors, fixers, and gate actors", path))
                        valid = False
                    if adjudicator not in set(actors.get("adjudicators", [])):
                        findings.append(Finding("ADJ003", "adjudication result uses an undeclared adjudicator", path))
                        valid = False
                    if result.get("source_revision") != final_revision:
                        findings.append(Finding("REV010", "adjudication result is not bound to final source revision", path))
                        valid = False
                    if gate not in required_adjudication_gates:
                        findings.append(Finding("ADJ002", "adjudication result does not target a required gate", path))
                        valid = False
                    if run.get("status") in PASSING and result.get("decision") not in PASSING:
                        findings.append(Finding("ADJ005", "passing run requires a passing adjudication decision", path))
                        valid = False
                    if valid and result.get("decision") in PASSING:
                        passing_adjudicated_gates.add(gate)
                missing_adjudicators = set(actors.get("adjudicators", [])) - adjudicated_by
                if missing_adjudicators:
                    findings.append(Finding("LOOP010", f"declared adjudicators lack result files: {sorted(missing_adjudicators)}", adjudication_dir))
                missing_adjudications = required_adjudication_gates - passing_adjudicated_gates
                if run.get("status") in PASSING and missing_adjudications:
                    findings.append(Finding("ADJ001", f"required gates lack passing adjudication: {sorted(missing_adjudications)}", adjudication_dir))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--repo", type=Path)
    args = parser.parse_args()
    repo = args.repo
    if repo is None and args.run_dir.parent.name == ".ric-work":
        repo = args.run_dir.parent.parent
    findings = validate_run(args.run_dir, repo, require_repo_revision=repo is not None)
    for finding in findings:
        print(finding.render(args.run_dir.resolve()))
    print(f"Validated delivery run: {len(findings)} error(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())











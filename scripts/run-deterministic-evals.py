#!/usr/bin/env python3
"""Run deterministic trigger, composition, and lifecycle contract evals."""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path
from typing import Any

from routing_rules import admin_requires_visual_work


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def route_primary(prompt: str) -> str | None:
    lowered = prompt.lower()
    if any(term in lowered for term in ("explain", "review this existing diff", "inspect the existing redis")):
        return None
    if any(term in lowered for term in ("modify an existing skill", "skill repository change", "author a skill")):
        return None
    if any(term in lowered for term in ("admin", "console", "rbac", "audit-log", "back office", "back-office", "crud management", "management workbench")):
        return "ric-admin-console"
    if any(term in lowered for term in ("implement from screenshot", "image to code", "mockup to code", "screenshot to code")):
        return "ric-image-to-code"
    if any(term in lowered for term in ("mobile visual direction", "mobile screen concepts", "mobile imagegen")):
        return "ric-imagegen-frontend-mobile"
    if any(term in lowered for term in ("web visual direction", "web comp concepts", "web imagegen")):
        return "ric-imagegen-frontend-web"
    if any(term in lowered for term in ("brand identity", "brand kit", "logo direction")):
        return "ric-brandkit"
    if any(term in lowered for term in ("redesign the existing", "redesign existing")):
        return "ric-redesign-existing-projects"
    if any(term in lowered for term in ("release rollout", "deploy to production", "deployment rollout")):
        return "ric-deployment-ops"
    if any(term in lowered for term in ("write the runbook", "documentation delivery", "api documentation")):
        return "ric-docs"
    if any(term in lowered for term in ("provision shared", "infrastructure integration", "shared redis integration")):
        return "ric-infra-safety"
    if any(term in lowered for term in ("pnpm workspace", "node dependency", "lockfile migration")):
        return "ric-node-pnpm"
    if any(term in lowered for term in ("api contract", "openapi design", "webhook contract")):
        return "ric-api-design"
    if any(term in lowered for term in ("kafka", "pipeline", "backfill", "dlq")):
        return "ric-data-pipeline"
    if any(term in lowered for term in ("api", "backend", "background email")):
        return "ric-backend-service"
    if any(term in lowered for term in ("landing page", "public product", "portfolio")):
        return "ric-design-taste-frontend"
    return None


def route_skills(prompt: str) -> set[str]:
    lowered = prompt.lower()
    primary = route_primary(prompt)
    if primary is None:
        if any(term in lowered for term in ("modify an existing skill", "skill repository change", "author a skill")):
            return {"ric-skill-quality", "ric-independent-review"}
        if "review this existing diff" in lowered:
            return {"ric-code-review", "ric-independent-review"}
        if "inspect the existing redis" in lowered:
            return {"ric-infra-safety"}
        return set()
    selected = {
        "ric-delivery-loop",
        "ric-requirements-engineering",
        "ric-solution-design",
        "ric-agent-operating-rules",
        "ric-independent-review",
        "ric-code-review",
        "ric-security-review",
        "ric-testing-quality",
        "ric-acceptance-validation",
        primary,
    }
    explicit_modifiers = {
        name
        for name in (
            "ric-design-taste-frontend-v1",
            "ric-gpt-taste",
            "ric-high-end-visual-design",
            "ric-minimalist-ui",
            "ric-industrial-brutalist-ui",
        )
        if name in lowered
    }
    selected.update(explicit_modifiers)
    if primary == "ric-admin-console" and admin_requires_visual_work(prompt):
        selected.update({"ric-visual-design-review", "ric-design-qa"})
    if explicit_modifiers:
        selected.update({"ric-visual-design-review", "ric-design-qa"})
    if primary == "ric-design-taste-frontend":
        selected.update({"ric-imagegen-runtime", "ric-visual-design-review", "ric-design-qa"})
    if primary == "ric-image-to-code":
        selected.update({"ric-visual-design-review", "ric-design-qa"})
    if primary == "ric-backend-service":
        selected.update({"ric-api-design", "ric-infra-safety"})
    if primary == "ric-data-pipeline":
        selected.add("ric-infra-safety")
    if primary in {
        "ric-imagegen-frontend-web",
        "ric-imagegen-frontend-mobile",
        "ric-brandkit",
        "ric-redesign-existing-projects",
    }:
        selected.update({"ric-imagegen-runtime", "ric-visual-design-review", "ric-design-qa"})
    return selected


def run_semantic_negative_tests(root: Path) -> list[str]:
    module_path = root / "scripts" / "test_validate_delivery_run.py"
    scripts_path = str(module_path.parent)
    added_path = scripts_path not in sys.path
    if added_path:
        sys.path.insert(0, scripts_path)
    spec = importlib.util.spec_from_file_location("delivery_negative_tests", module_path)
    if not spec or not spec.loader:
        if added_path:
            sys.path.remove(scripts_path)
        return ["cannot load delivery-run semantic negative tests"]
    try:
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        return [] if result.wasSuccessful() else ["delivery-run semantic negative tests failed"]
    finally:
        if added_path:
            sys.path.remove(scripts_path)


def evaluate(root: Path) -> list[str]:
    errors: list[str] = []
    catalog = load(root / "skills" / "catalog.json")["skills"]

    positive_primaries: set[str] = set()
    negative_or_conflict_coverage: set[str] = set()
    for filename in ("trigger-selection.json", "negative-triggers.json"):
        for case in load(root / "evals" / filename)["cases"]:
            expected = case["expected"]
            primary = expected.get("primary")
            actual_primary = route_primary(case["prompt"])
            selected = route_skills(case["prompt"])
            if actual_primary != primary:
                errors.append(f"{case['id']}: expected primary {primary!r}, routed {actual_primary!r}")
            missing_required = set(expected.get("required", [])) - selected
            included_excluded = set(expected.get("excluded", [])) & selected
            if missing_required:
                errors.append(f"{case['id']}: routed skills omit required {sorted(missing_required)}")
            if included_excluded:
                errors.append(f"{case['id']}: routed skills include excluded {sorted(included_excluded)}")
            if primary and "primary-executor" not in catalog[primary]["allowed_roles"]:
                errors.append(f"{case['id']}: expected primary is not allowed as primary-executor")
            if filename == "trigger-selection.json" and primary:
                positive_primaries.add(primary)
            if filename == "negative-triggers.json":
                negative_or_conflict_coverage.update(expected.get("excluded", []))
            overlap = set(expected.get("required", [])) & set(expected.get("excluded", []))
            if overlap:
                errors.append(f"{case['id']}: required and excluded overlap: {sorted(overlap)}")
            if primary and primary in expected.get("excluded", []):
                errors.append(f"{case['id']}: primary is excluded")

    for case in load(root / "evals" / "composition-conflicts.json")["cases"]:
        active_roles = case.get("active_roles", {})
        primary_count = sum(role == "primary-executor" for role in active_roles.values())
        role_errors = [
            f"{name}:{role}"
            for name, role in active_roles.items()
            if role not in catalog[name]["allowed_roles"]
        ]
        selected_names = set(active_roles)
        if case["expected_result"] == "invalid":
            negative_or_conflict_coverage.update(selected_names)
        missing_companions = {
            f"{name}->{companion}"
            for name in selected_names
            for companion in catalog[name].get("required_companions", [])
            if companion not in selected_names
        }
        conflict_pairs = {
            tuple(sorted((name, conflict)))
            for name in selected_names
            for conflict in catalog[name].get("conflicts", [])
            if conflict in selected_names
        }
        actor_conflict = case.get("author_id") and case.get("author_id") == case.get("reviewer_id")
        orchestrator_count = sum(role == "orchestrator" for role in active_roles.values())
        missing_quality_gates = {
            f"{name}->{gate}"
            for name, role in active_roles.items()
            if role not in {"quality-gate", "policy", "runtime", "handoff"}
            for gate in catalog[name].get("quality_gates", [])
            if gate not in selected_names
        }
        actual = "invalid" if primary_count != 1 or orchestrator_count != 1 or role_errors or missing_companions or conflict_pairs or missing_quality_gates or actor_conflict else "valid"
        if actual != case["expected_result"]:
            errors.append(f"{case['id']}: expected {case['expected_result']}, calculated {actual}")

    primary_capable = {
        name
        for name, entry in catalog.items()
        if "primary-executor" in entry.get("allowed_roles", [])
    }
    missing_positive = primary_capable - positive_primaries
    if missing_positive:
        errors.append(f"primary-capable skills lack positive trigger coverage: {sorted(missing_positive)}")
    missing_negative = primary_capable - negative_or_conflict_coverage
    if missing_negative:
        errors.append(f"primary-capable skills lack negative/conflict coverage: {sorted(missing_negative)}")

    for case in load(root / "evals" / "behavioral-scenarios.json")["cases"]:
        overlap = set(case["must_include"]) & set(case["must_not_include"])
        if overlap:
            errors.append(f"{case['id']}: contradictory behavioral expectations: {sorted(overlap)}")

    required_artifacts = {
        "run.json",
        "requirements.md",
        "acceptance.json",
        "traceability.json",
        "risk-register.json",
        "design.md",
        "dispatch",
        "review-results",
        "test-plan.json",
        "test-results",
        "evidence-manifest.json",
        "handoff.md",
    }
    base_gate_skills = {
        "ric-independent-review",
        "ric-code-review",
        "ric-security-review",
        "ric-testing-quality",
        "ric-acceptance-validation",
    }
    for case in load(root / "evals" / "end-to-end-delivery.json")["cases"]:
        artifacts = set(case["required_artifacts"])
        missing = required_artifacts - artifacts
        if missing:
            errors.append(f"{case['id']}: missing canonical artifacts: {sorted(missing)}")
        if "BLOCKED" not in case["terminal_states"]:
            errors.append(f"{case['id']}: BLOCKED must be a terminal state")
        primary = case["primary"]
        if primary not in catalog:
            errors.append(f"{case['id']}: primary {primary!r} is not in catalog")
            continue
        if "primary-executor" not in catalog[primary]["allowed_roles"]:
            errors.append(f"{case['id']}: primary {primary!r} is not allowed as primary-executor")
        required_gates = set(case["required_gates"])
        missing_base_gates = base_gate_skills - required_gates
        if missing_base_gates:
            errors.append(f"{case['id']}: missing base gate skills: {sorted(missing_base_gates)}")
        missing_domain_gates = set(catalog[primary].get("quality_gates", [])) - required_gates
        if missing_domain_gates:
            errors.append(f"{case['id']}: missing primary catalog quality gates: {sorted(missing_domain_gates)}")
    errors.extend(run_semantic_negative_tests(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = evaluate(args.root.resolve())
    for error in errors:
        print(f"ERROR {error}")
    print(f"Deterministic evals: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

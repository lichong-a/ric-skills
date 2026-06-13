"""Semantic negative tests for delivery-run validation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-delivery-run.py")
SPEC = importlib.util.spec_from_file_location("validate_delivery_run", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


class DeliveryRunValidatorTests(unittest.TestCase):
    gate_actors = {
        "requirements": ["req-1", "req-2"],
        "design": ["design-1", "design-2"],
        "code-review": ["code-1"],
        "security-review": ["security-1"],
        "test": ["tester-1"],
        "acceptance": ["validator-1"],
    }

    gate_skills = {
        "requirements": ["ric-independent-review", "ric-requirements-engineering", "ric-backend-service"],
        "design": ["ric-independent-review", "ric-solution-design", "ric-backend-service"],
        "code-review": ["ric-independent-review", "ric-code-review", "ric-backend-service"],
        "security-review": ["ric-independent-review", "ric-security-review", "ric-backend-service"],
        "test": ["ric-testing-quality", "ric-backend-service"],
        "acceptance": ["ric-independent-review", "ric-acceptance-validation", "ric-backend-service"],
    }

    def make_run(self, root: Path) -> None:
        evidence = root / "evidence" / "result.txt"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("verified", encoding="utf-8")
        digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
        required_gates = list(self.gate_actors)
        events = []
        gates = []
        sequence = 1
        for gate, actors in self.gate_actors.items():
            event = {"sequence": sequence, "type": "gate-passed", "gate": gate, "actor_id": actors[0]}
            if gate in {"requirements", "design"}:
                event["artifact_version"] = "req-v1" if gate == "requirements" else "design-v1"
            else:
                event["source_revision"] = "rev-2"
            events.append(event)
            gates.append(
                {
                    "type": gate,
                    "decision": "PASS",
                    "iteration": 1,
                    "source_revision": "rev-0" if gate in {"requirements", "design"} else "rev-2",
                    "reviewers": actors,
                    **(
                        {"artifact_versions": {gate: "req-v1" if gate == "requirements" else "design-v1"}}
                        if gate in {"requirements", "design"}
                        else {}
                    ),
                }
            )
            sequence += 1
        write_json(
            root / "run.json",
            {
                "run_id": "run-1",
                "request": "Deliver a tested backend change.",
                "scope": ["backend"],
                "non_goals": [],
                "assumptions": [],
                "capabilities": ["subagent"],
                "status": "PASS",
                "epoch": 1,
                "degraded_mode": False,
                "final_source_revision": "rev-2",
                "artifact_versions": {"requirements": "req-v1", "design": "design-v1"},
                "selected_skills": [
                    {"name": "ric-delivery-loop", "active_role": "orchestrator"},
                    {"name": "ric-requirements-engineering", "active_role": "lifecycle-stage"},
                    {"name": "ric-solution-design", "active_role": "lifecycle-stage"},
                    {"name": "ric-agent-operating-rules", "active_role": "policy"},
                    {"name": "ric-independent-review", "active_role": "quality-gate"},
                    {"name": "ric-backend-service", "active_role": "primary-executor"},
                    {"name": "ric-code-review", "active_role": "quality-gate"},
                    {"name": "ric-security-review", "active_role": "quality-gate"},
                    {"name": "ric-testing-quality", "active_role": "quality-gate"},
                    {"name": "ric-acceptance-validation", "active_role": "quality-gate"},
                ],
                "actors": {"authors": ["author-1"], "fixers": ["fixer-1"], "adjudicators": []},
                "required_gates": required_gates,
                "events": events,
                "gates": gates,
            },
        )
        (root / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
        (root / "design.md").write_text("# Design\n", encoding="utf-8")
        (root / "handoff.md").write_text("# Handoff\n", encoding="utf-8")
        for gate, actors in self.gate_actors.items():
            for actor in actors:
                role = {
                    "requirements": "requirements-security-reviewer" if actor == "req-2" else "requirements-reviewer",
                    "design": "design-security-reviewer" if actor == "design-2" else "design-reviewer",
                    "code-review": "code-reviewer",
                    "security-review": "security-reviewer",
                    "test": "test-executor",
                    "acceptance": "acceptance-validator",
                }[gate]
                required_skills = list(self.gate_skills[gate])
                if actor == "req-2":
                    required_skills = ["ric-independent-review", "ric-security-review", "ric-backend-service"]
                if actor == "design-2":
                    required_skills = ["ric-independent-review", "ric-solution-design", "ric-security-review", "ric-backend-service"]
                write_json(
                    root / "dispatch" / f"{actor}.json",
                    {
                        "run_id": "run-1",
                        "actor_id": actor,
                        "role": role,
                        "objective": f"Independently execute {gate}.",
                        "scope": [gate],
                        "non_goals": ["modify implementation"],
                        "source_revision": "rev-2",
                        **(
                            {"artifact_version": "req-v1" if gate == "requirements" else "design-v1"}
                            if gate in {"requirements", "design"}
                            else {}
                        ),
                        "fresh_context": True,
                        "read_only": True,
                        "required_skills": required_skills,
                        "capabilities": ["subagent"],
                        "expected_output": "structured gate result",
                    },
                )
        write_json(root / "acceptance.json", {"run_id": "run-1", "criteria": [{"id": "AC-1", "statement": "Works", "expected_evidence": ["ev-1"]}]})
        write_json(root / "traceability.json", {"run_id": "run-1", "links": [{"requirement_id": "REQ-1", "acceptance_id": "AC-1", "design_refs": ["design.md"], "test_refs": ["unit"], "evidence_refs": ["ev-1"]}]})
        write_json(root / "risk-register.json", {"run_id": "run-1", "risks": []})
        for gate in ("requirements", "design", "code-review", "security-review", "acceptance"):
            for reviewer in self.gate_actors[gate]:
                write_json(
                    root / "review-results" / f"{gate}-{reviewer}.json",
                    {
                        "run_id": "run-1",
                        "gate": gate,
                        "decision": "PASS",
                        "source_revision": "rev-0" if gate in {"requirements", "design"} else "rev-2",
                        **({"artifact_version": "req-v1" if gate == "requirements" else "design-v1"} if gate in {"requirements", "design"} else {}),
                        "reviewer": {"id": reviewer, "fresh_context": True, "read_only": True},
                        "artifact_authors": ["author-1"],
                        "artifact_fixers": ["fixer-1"],
                        "findings": [],
                        "evidence": ["ev-1"],
                    },
                )
        write_json(root / "test-plan.json", {"run_id": "run-1", "source_revision": "rev-2", "suites": [{"id": "unit", "type": "unit", "mandatory": True, "rerun_scope": "baseline", "acceptance_ids": ["AC-1"]}]})
        write_json(root / "test-results" / "unit.json", {"run_id": "run-1", "suite_id": "unit", "rerun_scope": "baseline", "executor": "tester-1", "fresh_context": True, "read_only": True, "source_revision": "rev-2", "result": "PASS", "evidence": ["ev-1"]})
        write_json(
            root / "evidence-manifest.json",
            {
                "run_id": "run-1",
                "status": "PASS",
                "source_revision": "rev-2",
                "acceptance_coverage": [{"id": "AC-1", "status": "PASS", "evidence_ids": ["ev-1"]}],
                "evidence": [{"id": "ev-1", "type": "test-report", "path": "evidence/result.txt", "sha256": digest, "result": "PASS", "source_revision": "rev-2"}],
            },
        )

    def errors(self, root: Path) -> set[str]:
        return {finding.code for finding in validator.validate_run(root)}

    def mutate(self, root: Path, relative: str, callback) -> None:
        path = root / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        callback(value)
        write_json(path, value)

    def test_valid_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.assertEqual(set(), self.errors(root))

    def test_rejects_cross_run_canonical_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            for filename in ("acceptance.json", "traceability.json", "risk-register.json", "evidence-manifest.json"):
                self.mutate(root, filename, lambda value: value.update(run_id="other-run"))
            self.assertIn("RUN014", self.errors(root))

    def test_rejects_unknown_capability_and_two_primaries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["capabilities"].append("invented-capability")
                run["selected_skills"].append({"name": "ric-data-pipeline", "active_role": "primary-executor"})
            self.mutate(root, "run.json", change)
            self.assertTrue({"ROLE001", "ROLE010"} <= self.errors(root))

    def test_visual_modifier_requires_visual_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "run.json", lambda run: run["selected_skills"].append({"name": "ric-high-end-visual-design", "active_role": "modifier"}))
            self.assertIn("ROLE009", self.errors(root))

    def test_visual_gate_dispatches_require_active_visual_modifier(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def add_visual_run(run):
                run["selected_skills"].extend(
                    [
                        {"name": "ric-high-end-visual-design", "active_role": "modifier"},
                        {"name": "ric-visual-design-review", "active_role": "quality-gate"},
                        {"name": "ric-design-qa", "active_role": "quality-gate"},
                    ]
                )
                for gate_type, reviewer in (("visual-review", "visual-1"), ("design-qa", "design-qa-1")):
                    run["required_gates"].append(gate_type)
                    run["gates"].append(
                        {
                            "type": gate_type,
                            "decision": "PASS",
                            "iteration": 1,
                            "source_revision": "rev-2",
                            "reviewers": [reviewer],
                        }
                    )
                    run["events"].append(
                        {
                            "sequence": len(run["events"]) + 1,
                            "type": "gate-passed",
                            "gate": gate_type,
                            "actor_id": reviewer,
                            "source_revision": "rev-2",
                        }
                    )
            self.mutate(root, "run.json", add_visual_run)
            for gate_type, reviewer, role, gate_skill in (
                ("visual-review", "visual-1", "visual-reviewer", "ric-visual-design-review"),
                ("design-qa", "design-qa-1", "design-qa-reviewer", "ric-design-qa"),
            ):
                write_json(
                    root / "dispatch" / f"{reviewer}.json",
                    {
                        "run_id": "run-1",
                        "actor_id": reviewer,
                        "role": role,
                        "objective": f"Independently execute {gate_type}.",
                        "scope": [gate_type],
                        "non_goals": ["modify implementation"],
                        "source_revision": "rev-2",
                        "fresh_context": True,
                        "read_only": True,
                        "required_skills": ["ric-independent-review", gate_skill, "ric-backend-service"],
                        "capabilities": ["subagent"],
                        "expected_output": "structured gate result",
                    },
                )
                review = {
                    "run_id": "run-1",
                    "gate": gate_type,
                    "decision": "PASS",
                    "source_revision": "rev-2",
                    "reviewer": {"id": reviewer, "fresh_context": True, "read_only": True},
                    "artifact_authors": ["author-1"],
                    "artifact_fixers": ["fixer-1"],
                    "findings": [],
                    "evidence": ["ev-1"],
                }
                if gate_type == "visual-review":
                    review["visual_score"] = {
                        "surface_class": "high-visual",
                        "categories": {
                            "specificity": 5,
                            "hierarchy": 5,
                            "distinctiveness": 5,
                            "consistency": 5,
                            "responsive_accessibility": 5,
                            "asset_fidelity": 5,
                        },
                        "total": 100,
                    }
                write_json(root / "review-results" / f"{gate_type}-{reviewer}.json", review)
            self.assertIn("RUN015", self.errors(root))

    def test_react_visual_admin_requires_shadcn_and_visual_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["request"] = "Deliver a React and shadcn admin console with RBAC, actionable breadcrumbs, themes, i18n readiness, and browser evidence."
                for item in run["selected_skills"]:
                    if item["name"] == "ric-backend-service":
                        item["name"] = "ric-admin-console"
            self.mutate(root, "run.json", change)
            errors = self.errors(root)
            self.assertTrue({"ROLE011", "ROLE012", "ROLE013"} <= errors)

    def test_mixed_scope_admin_visual_surfaces_override_utility_terms(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["request"] = "Deliver a React and shadcn admin console with utility-first CRUD pages and a branded login and workbench."
                for item in run["selected_skills"]:
                    if item["name"] == "ric-backend-service":
                        item["name"] = "ric-admin-console"
            self.mutate(root, "run.json", change)
            errors = self.errors(root)
            self.assertTrue({"ROLE012", "ROLE013"} <= errors)

    def test_acceptance_repair_requires_complete_ordered_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                next(gate for gate in run["gates"] if gate["type"] == "acceptance")["iteration"] = 2
                run["events"] = [
                    *run["events"],
                    {"sequence": 7, "type": "gate-failed", "gate": "acceptance", "actor_id": "validator-1", "source_revision": "rev-2"},
                    {"sequence": 8, "type": "fix-applied", "gate": "acceptance", "actor_id": "fixer-1", "source_revision": "rev-2"},
                    {"sequence": 9, "type": "results-invalidated", "gate": "acceptance", "actor_id": "fixer-1", "source_revision": "rev-2"},
                    {"sequence": 10, "type": "gate-passed", "gate": "acceptance", "actor_id": "validator-1", "source_revision": "rev-2"},
                ]
            self.mutate(root, "run.json", change)
            errors = self.errors(root)
            self.assertTrue({"LOOP011", "LOOP012", "LOOP014", "TEST009"} <= errors)

    def test_acceptance_repair_order_rejects_old_events_before_current_rechecks(self) -> None:
        gate_by_type = {
            "code-review": {"reviewers": ["code-1"]},
            "security-review": {"reviewers": ["security-1"]},
            "test": {"reviewers": ["tester-1"]},
            "acceptance": {"reviewers": ["validator-1"]},
        }
        adversarial = [
            {"sequence": 1, "type": "gate-failed", "gate": "acceptance", "actor_id": "validator-1", "source_revision": "rev-2"},
            {"sequence": 2, "type": "fix-applied", "actor_id": "fixer-1", "source_revision": "rev-3"},
            {"sequence": 3, "type": "gate-passed", "gate": "code-review", "actor_id": "code-1", "source_revision": "rev-2"},
            {"sequence": 4, "type": "gate-passed", "gate": "security-review", "actor_id": "security-1", "source_revision": "rev-2"},
            {"sequence": 5, "type": "test-impacted-passed", "gate": "test", "suite_id": "impacted", "actor_id": "tester-1", "source_revision": "rev-2"},
            {"sequence": 6, "type": "test-full-passed", "gate": "test", "suite_id": "full", "actor_id": "tester-1", "source_revision": "rev-2"},
            {"sequence": 7, "type": "gate-passed", "gate": "acceptance", "actor_id": "validator-1", "source_revision": "rev-3"},
            {"sequence": 8, "type": "gate-passed", "gate": "code-review", "actor_id": "code-1", "source_revision": "rev-3"},
            {"sequence": 9, "type": "gate-passed", "gate": "security-review", "actor_id": "security-1", "source_revision": "rev-3"},
        ]
        reruns = {("impacted", "impacted", "tester-1"), ("full", "full", "tester-1")}
        self.assertFalse(
            validator.acceptance_repair_order_is_valid(
                adversarial,
                1,
                "rev-3",
                {"code-review", "security-review", "test", "acceptance"},
                gate_by_type,
                {"fixer-1"},
                reruns,
            )
        )
        valid = [
            adversarial[0],
            adversarial[1],
            {**adversarial[7], "sequence": 3},
            {**adversarial[8], "sequence": 4},
            {**adversarial[4], "sequence": 5, "source_revision": "rev-3"},
            {**adversarial[5], "sequence": 6, "source_revision": "rev-3"},
            {"sequence": 7, "type": "gate-passed", "gate": "test", "actor_id": "tester-1", "source_revision": "rev-3"},
            {**adversarial[6], "sequence": 8},
        ]
        self.assertTrue(
            validator.acceptance_repair_order_is_valid(
                valid,
                1,
                "rev-3",
                {"code-review", "security-review", "test", "acceptance"},
                gate_by_type,
                {"fixer-1"},
                reruns,
            )
        )
        late_test_gate = [*valid[:-2], valid[-1], {**valid[-2], "sequence": 9}]
        self.assertFalse(
            validator.acceptance_repair_order_is_valid(
                late_test_gate,
                1,
                "rev-3",
                {"code-review", "security-review", "test", "acceptance"},
                gate_by_type,
                {"fixer-1"},
                reruns,
            )
        )

    def test_terminal_failure_invalidates_earlier_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["events"].append({"sequence": 7, "type": "results-invalidated", "gate": "code-review", "actor_id": "fixer-1", "source_revision": "rev-2"})
            self.mutate(root, "run.json", change)
            self.assertIn("PASS030", self.errors(root))

    def test_post_pass_fix_invalidates_source_bound_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["events"].append(
                    {
                        "sequence": 7,
                        "type": "fix-applied",
                        "actor_id": "fixer-1",
                        "source_revision": "rev-3",
                    }
                )
            self.mutate(root, "run.json", change)
            errors = self.errors(root)
            self.assertTrue({"LOOP015", "PASS030"} <= errors)

    def test_rejects_unscoped_and_unknown_gate_lifecycle_events(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["events"].extend(
                    [
                        {"sequence": 7, "type": "results-invalidated", "actor_id": "fixer-1", "source_revision": "rev-2"},
                        {"sequence": 8, "type": "gate-failed", "gate": "invented-gate", "actor_id": "reviewer-x", "source_revision": "rev-2"},
                    ]
                )
            self.mutate(root, "run.json", change)
            self.assertIn("LOOP013", self.errors(root))

    def test_rejects_stale_source_and_artifact_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["final_source_revision"] = "rev-3"
                run["artifact_versions"]["design"] = "design-v2"
            self.mutate(root, "run.json", change)
            errors = self.errors(root)
            self.assertTrue({"REV004", "REV009"} <= errors)

    def test_rejects_self_approval_and_non_independent_test_executor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "review-results/code-review-code-1.json", lambda review: review["reviewer"].update(id="author-1"))
            self.mutate(root, "test-results/unit.json", lambda result: result.update(executor="author-1", fresh_context=False))
            self.assertTrue({"PASS002", "TEST006", "TEST008"} <= self.errors(root))

    def test_rejects_dispatch_without_required_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "dispatch/code-1.json", lambda packet: packet.update(required_skills=["ric-code-review"]))
            self.assertIn("RUN015", self.errors(root))

    def test_rejects_dispatch_role_spoofing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(
                root,
                "dispatch/code-1.json",
                lambda packet: packet.update(
                    role="test-executor",
                    required_skills=["ric-testing-quality", "ric-backend-service"],
                ),
            )
            errors = self.errors(root)
            self.assertTrue({"RUN015", "RUN019"} <= errors)

    def test_requirements_dispatch_needs_completeness_and_security_roles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "dispatch/req-2.json", lambda packet: packet.update(role="requirements-reviewer", required_skills=["ric-independent-review", "ric-requirements-engineering", "ric-backend-service"]))
            self.assertIn("RUN017", self.errors(root))

    def test_design_dispatch_needs_security_reviewer_role(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "dispatch/design-2.json", lambda packet: packet.update(role="design-reviewer", required_skills=["ric-independent-review", "ric-solution-design", "ric-backend-service"]))
            self.assertIn("RUN018", self.errors(root))

    def test_design_security_dual_role_requires_solution_design(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(
                root,
                "dispatch/design-2.json",
                lambda packet: packet.update(
                    required_skills=["ric-independent-review", "ric-security-review", "ric-backend-service"]
                ),
            )
            self.assertIn("RUN015", self.errors(root))

    def test_security_review_roles_require_primary_domain_skill(self) -> None:
        cases = (
            ("dispatch/req-2.json", ["ric-independent-review", "ric-security-review"]),
            ("dispatch/design-2.json", ["ric-independent-review", "ric-solution-design", "ric-security-review"]),
            ("dispatch/security-1.json", ["ric-independent-review", "ric-security-review"]),
        )
        for relative, skills in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.make_run(root)
                self.mutate(root, relative, lambda packet, skills=skills: packet.update(required_skills=skills))
                self.assertIn("RUN015", self.errors(root))

    def test_rejects_failed_acceptance_hash_mismatch_and_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(manifest):
                manifest["acceptance_coverage"][0]["status"] = "NOT_RUN"
                manifest["evidence"][0]["sha256"] = "0" * 64
                manifest["evidence"][0]["path"] = "../outside.txt"
            self.mutate(root, "evidence-manifest.json", change)
            self.assertTrue({"AC001", "EVID003"} <= self.errors(root))

    def test_rejects_acceptance_coverage_that_omits_expected_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            other = root / "evidence" / "other.txt"
            other.write_text("other", encoding="utf-8")
            digest = hashlib.sha256(other.read_bytes()).hexdigest()
            def change(manifest):
                manifest["evidence"].append(
                    {
                        "id": "ev-2",
                        "type": "test-report",
                        "path": "evidence/other.txt",
                        "sha256": digest,
                        "result": "PASS",
                        "source_revision": "rev-2",
                    }
                )
                manifest["acceptance_coverage"][0]["evidence_ids"] = ["ev-2"]
                manifest["acceptance_coverage"].append(
                    {"id": "AC-1", "status": "PASS", "evidence_ids": ["ev-1"]}
                )
            self.mutate(root, "evidence-manifest.json", change)
            errors = self.errors(root)
            self.assertTrue({"AC005", "AC006"} <= errors)

    def test_rejects_passing_test_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "test-results/unit.json", lambda result: result.update(evidence=[]))
            errors = self.errors(root)
            self.assertTrue({"SCHEMA100", "TEST010"} & errors)

    def test_rejects_secret_in_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            evidence = root / "evidence" / "result.txt"
            evidence.write_text("OPENAI_API_KEY=secret-value", encoding="utf-8")
            self.mutate(root, "evidence-manifest.json", lambda manifest: manifest["evidence"][0].update(sha256=hashlib.sha256(evidence.read_bytes()).hexdigest()))
            self.assertIn("EVID006", self.errors(root))

    def test_rejects_iteration_budget_and_degraded_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                run["epoch"] = 4
                run["degraded_mode"] = True
                run["gates"][2]["iteration"] = 4
            self.mutate(root, "run.json", change)
            self.assertIn("SCHEMA100", self.errors(root))

    def test_hostile_json_shape_returns_findings_instead_of_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "run.json", lambda run: run.update(selected_skills=["hostile"], events=["hostile"]))
            errors = self.errors(root)
            self.assertIn("SCHEMA100", errors)

    def test_more_hostile_core_shapes_return_findings_instead_of_crashing(self) -> None:
        hostile_updates = (
            {"capabilities": [{}]},
            {"actors": []},
            {"artifact_versions": []},
            {"required_gates": [{}]},
        )
        for update in hostile_updates:
            with self.subTest(update=update), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.make_run(root)
                self.mutate(root, "run.json", lambda run, update=update: run.update(update))
                self.assertIn("SCHEMA100", self.errors(root))

    def test_hostile_auxiliary_artifacts_return_schema_findings(self) -> None:
        cases = (
            ("test-plan.json", []),
            ("test-plan.json", {"run_id": "run-1", "source_revision": "rev-2", "suites": "hostile"}),
            ("review-results/code-review-code-1.json", []),
            ("test-results/unit.json", []),
            ("dispatch/code-1.json", []),
            ("live-eval-result.json", []),
        )
        for relative, value in cases:
            with self.subTest(relative=relative, value_type=type(value).__name__), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.make_run(root)
                write_json(root / relative, value)
                self.assertIn("SCHEMA100", self.errors(root))

    def test_required_adjudication_must_be_valid_declared_and_passing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                next(gate for gate in run["gates"] if gate["type"] == "code-review")["iteration"] = 3
                run["actors"]["adjudicators"] = ["adj-1"]
            self.mutate(root, "run.json", change)
            write_json(
                root / "adjudication-results" / "bad.json",
                {
                    "run_id": "run-1",
                    "gate": "invented-gate",
                    "adjudicator": "adj-x",
                    "fresh_context": True,
                    "read_only": True,
                    "source_revision": "rev-2",
                    "decision": "BLOCKED",
                    "reason": "not a passing adjudication",
                },
            )
            errors = self.errors(root)
            self.assertTrue({"ADJ001", "ADJ002", "ADJ003", "ADJ005"} <= errors)

    def test_non_object_adjudication_cannot_satisfy_required_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def change(run):
                next(gate for gate in run["gates"] if gate["type"] == "code-review")["iteration"] = 3
                run["actors"]["adjudicators"] = ["adj-1"]
            self.mutate(root, "run.json", change)
            write_json(root / "adjudication-results" / "bad.json", [])
            errors = self.errors(root)
            self.assertTrue({"SCHEMA100", "ADJ001"} <= errors)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            path = root / "run.json"
            text = path.read_text(encoding="utf-8").replace(
                '"run_id": "run-1",',
                '"run_id": "run-1",\n  "run_id": "other",',
                1,
            )
            path.write_text(text, encoding="utf-8")
            self.assertIn("RUN002", self.errors(root))

    def test_optional_live_eval_must_bind_to_run_and_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            write_json(
                root / "live-eval-result.json",
                {
                    "run_id": "other",
                    "source_revision": "old",
                    "status": "BLOCKED",
                    "results": [
                        {
                            "scenario_id": "behavior",
                            "adapter": "external-command",
                            "fresh_context": False,
                            "result": "BLOCKED",
                            "transcript_sha256": "0" * 64,
                            "redacted_summary": "not run",
                            "loaded_skills": [],
                            "gate_evidence": [],
                            "validation_errors": ["not run"],
                            "invocation_id": "",
                        }
                    ],
                },
            )
            self.assertIn("LIVE001", self.errors(root))

    def test_matching_failed_live_eval_blocks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            write_json(
                root / "live-eval-result.json",
                {
                    "run_id": "run-1",
                    "source_revision": "rev-2",
                    "status": "BLOCKED",
                    "results": [
                        {
                            "scenario_id": "behavior",
                            "adapter": "external-command",
                            "fresh_context": False,
                            "result": "FAIL",
                            "transcript_sha256": "0" * 64,
                            "redacted_summary": "failed",
                            "loaded_skills": [],
                            "gate_evidence": [],
                            "validation_errors": ["error"],
                            "invocation_id": "",
                        }
                    ],
                },
            )
            errors = self.errors(root)
            self.assertTrue({"LIVE002", "LIVE003", "LIVE004", "LIVE005"} <= errors)

    def test_no_mandatory_suite_blocks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "test-plan.json", lambda plan: plan["suites"][0].update(mandatory=False, acceptance_ids=[]))
            self.assertIn("TEST010", self.errors(root))

    def test_mandatory_acceptance_unmapped_blocks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "test-plan.json", lambda plan: plan["suites"][0].update(acceptance_ids=[]))
            self.assertIn("TEST011", self.errors(root))

    def test_malformed_catalog_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            original = validator.load_json
            def mock_load(path, findings, required=True):
                if "catalog.json" in str(path):
                    return {"version": 1, "capabilities": [{}], "skills": {}}
                return original(path, findings, required)
            validator.load_json = mock_load
            try:
                errors = self.errors(root)
                self.assertIsInstance(errors, set)
                self.assertIn("CAT001", errors)
            finally:
                validator.load_json = original

    def test_backend_primary_with_visual_request_requires_visual_gates(self) -> None:
        """A backend-primary delivery with a React UI request must not skip visual gates."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            self.mutate(root, "run.json", lambda run: run.update(request="Deliver a backend feature with a React admin UI and branded workflow."))
            errors = self.errors(root)
            self.assertTrue({"ROLE014", "ROLE015"} & errors)

    def test_empty_authors_does_not_allow_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_run(root)
            def empty_provenance(run):
                run["actors"]["authors"] = []
                run["actors"]["fixers"] = []
            self.mutate(root, "run.json", empty_provenance)
            for gate in ("requirements", "design", "code-review", "security-review", "acceptance"):
                for reviewer in self.gate_actors[gate]:
                    self.mutate(root, f"review-results/{gate}-{reviewer}.json", lambda review: review.update(artifact_authors=[], artifact_fixers=[]))
            errors = self.errors(root)
            self.assertIn("PASS031", errors)


if __name__ == "__main__":
    unittest.main()





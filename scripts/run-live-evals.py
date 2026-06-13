#!/usr/bin/env python3
"""Run optional fresh-context behavioral evals through an explicit adapter.

This tool validates claimed behavior and retained evidence. It does not create a
cryptographic trust boundary and is never required for ordinary repository
validation, commits, or releases.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import BinaryIO


PASSING = {"PASS", "PASS_WITH_ADVISORIES"}
MAX_TRANSCRIPT_BYTES = 4 * 1024 * 1024
MAX_EVIDENCE_BYTES = 16 * 1024 * 1024


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


class BoundedCollector:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.data = bytearray()
        self.too_large = False

    def drain(self, stream: BinaryIO) -> None:
        try:
            for chunk in iter(lambda: stream.read(65536), b""):
                remaining = self.limit - len(self.data)
                if remaining > 0:
                    self.data.extend(chunk[:remaining])
                if len(chunk) > remaining:
                    self.too_large = True
        finally:
            stream.close()


def terminate_process_tree(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()


def parse_adapter_command(command: str) -> list[str]:
    if command.lstrip().startswith("["):
        value = json.loads(command)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
            raise ValueError("adapter command JSON must be a non-empty string array")
        return value
    if os.name == "nt":
        raise ValueError("Windows external adapter command must be a JSON string array")
    return shlex.split(command)


def scenario_sha256(scenario: dict[str, object]) -> str:
    return hashlib.sha256(json.dumps(scenario, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def validate_adapter_claim(
    scenario: object,
    claim: object,
    evidence_root: Path,
) -> list[str]:
    if not isinstance(scenario, dict):
        return ["dispatched scenario must be one JSON object"]
    if not isinstance(claim, dict):
        return ["adapter stdout must be one JSON object"]

    errors: list[str] = []
    if claim.get("scenario_id") != scenario.get("id"):
        errors.append("scenario_id does not match the dispatched scenario")
    if claim.get("challenge") != scenario.get("_challenge"):
        errors.append("adapter challenge does not match the dispatched one-time challenge")
    if claim.get("scenario_sha256") != scenario_sha256(scenario):
        errors.append("adapter scenario_sha256 does not match the dispatched scenario")
    if claim.get("result") not in PASSING:
        errors.append("adapter did not return a passing scenario result")
    if claim.get("fresh_context") is not True:
        errors.append("adapter did not report fresh_context=true")
    if not isinstance(claim.get("invocation_id"), str) or not claim.get("invocation_id"):
        errors.append("adapter did not provide invocation_id")

    required_skills = {str(item) for item in scenario.get("skills", []) if isinstance(item, str)}
    loaded_skills_raw = claim.get("loaded_skills")
    if not isinstance(loaded_skills_raw, list) or any(not isinstance(item, str) for item in loaded_skills_raw):
        errors.append("loaded_skills must be a string array")
        loaded_skills: set[str] = set()
    else:
        loaded_skills = set(loaded_skills_raw)
    missing_skills = required_skills - loaded_skills
    if missing_skills:
        errors.append(f"adapter omitted required skills: {sorted(missing_skills)}")

    gate_evidence = claim.get("gate_evidence")
    if not isinstance(gate_evidence, list):
        return errors + ["gate_evidence must be an array"]

    passing_gates: set[str] = set()
    actor_ids: list[str] = []
    evidence_texts: list[str] = []
    passing_gate_entries: list[dict[str, object]] = []
    for entry in gate_evidence:
        if not isinstance(entry, dict):
            errors.append("every gate_evidence entry must be an object")
            continue
        gate = entry.get("gate")
        actor_id = entry.get("actor_id")
        role = entry.get("role")
        gate_loaded_skills = entry.get("loaded_skills")
        digest = entry.get("evidence_sha256")
        evidence_path = entry.get("evidence_path")
        if entry.get("result") not in PASSING or entry.get("fresh_context") is not True:
            errors.append(f"gate {gate!r} lacks a passing fresh-context result")
            continue
        if not isinstance(actor_id, str) or not actor_id:
            errors.append(f"gate {gate!r} lacks an actor_id")
            continue
        if not isinstance(role, str) or not role:
            errors.append(f"gate {gate!r} lacks a role")
            continue
        REVIEWER_ROLES = {
            "requirements-reviewer",
            "requirements-security-reviewer",
            "design-reviewer",
            "design-security-reviewer",
            "code-reviewer",
            "security-reviewer",
            "test-executor",
            "visual-reviewer",
            "design-qa-reviewer",
            "acceptance-validator",
            "adjudicator",
            "skill-quality-reviewer",
        }
        if role not in REVIEWER_ROLES:
            errors.append(f"gate {gate!r} role {role!r} is not a recognized independent reviewer role")
            continue
        if entry.get("read_only") is not True:
            errors.append(f"gate {gate!r} lacks read_only=true for an independent reviewer")
            continue
        if not isinstance(gate_loaded_skills, list) or any(not isinstance(item, str) for item in gate_loaded_skills):
            errors.append(f"gate {gate!r} loaded_skills must be a string array")
            continue
        if isinstance(gate, str) and gate.startswith("ric-") and gate not in gate_loaded_skills:
            errors.append(f"gate {gate!r} did not load its required gate skill")
            continue
        primary_skill = scenario.get("primary_skill")
        if isinstance(primary_skill, str) and primary_skill not in gate_loaded_skills:
            errors.append(f"gate {gate!r} did not load primary skill {primary_skill!r}")
            continue
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            errors.append(f"gate {gate!r} lacks a valid evidence_sha256")
            continue
        if not isinstance(evidence_path, str) or not evidence_path:
            errors.append(f"gate {gate!r} lacks evidence_path")
            continue
        target = (evidence_root / evidence_path).resolve(strict=False)
        try:
            target.relative_to(evidence_root.resolve())
        except ValueError:
            errors.append(f"gate {gate!r} evidence_path escapes the evidence root")
            continue
        is_junction = getattr(target, "is_junction", lambda: False)()
        if not target.is_file() or target.is_symlink() or is_junction:
            errors.append(f"gate {gate!r} evidence_path is missing or unsafe")
            continue
        if target.stat().st_size > MAX_EVIDENCE_BYTES:
            errors.append(f"gate {gate!r} evidence_path exceeds {MAX_EVIDENCE_BYTES} bytes")
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            errors.append(f"gate {gate!r} evidence_sha256 does not match evidence_path")
            continue
        evidence_text = target.read_text(encoding="utf-8", errors="replace").lower()
        evidence_texts.append(evidence_text)
        passing_gates.add(str(gate))
        actor_ids.append(actor_id)
        passing_gate_entries.append(
            {
                "gate": str(gate),
                "actor_id": actor_id,
                "loaded_skills": set(gate_loaded_skills),
                "evidence_text": evidence_text,
            }
        )

    required_gates = {str(item) for item in scenario.get("required_gates", []) if isinstance(item, str)}
    missing_gates = required_gates - passing_gates
    if missing_gates:
        errors.append(f"required gates lack passing evidence: {sorted(missing_gates)}")
    if len(actor_ids) != len(set(actor_ids)):
        errors.append("required live-eval gates must use distinct independent actors")
    author_id = scenario.get("author_id")
    if isinstance(author_id, str) and author_id in actor_ids:
        errors.append("live-eval reviewer cannot be the scenario author")
    required_reviewer_skills = {
        str(item)
        for item in scenario.get("required_reviewer_skills", [])
        if isinstance(item, str)
    }
    changed_skill = scenario.get("changed_skill")
    if isinstance(changed_skill, str) and changed_skill:
        required_reviewer_skills = required_reviewer_skills | {changed_skill}
    if required_reviewer_skills:
        qualified_reviewers = [
            entry
            for entry in passing_gate_entries
            if entry["gate"] in required_gates
            and required_reviewer_skills <= entry["loaded_skills"]
        ]
        if not qualified_reviewers:
            errors.append(f"no reviewer loaded required skill bundle: {sorted(required_reviewer_skills)}")
        evidence_texts = [str(entry["evidence_text"]) for entry in qualified_reviewers]

    combined_evidence = "\n".join(evidence_texts)
    for phrase in scenario.get("must_include", []):
        if str(phrase).lower() not in combined_evidence:
            errors.append(f"behavioral evidence omits required phrase: {phrase!r}")
    for phrase in scenario.get("must_not_include", []):
        if str(phrase).lower() in combined_evidence:
            errors.append(f"behavioral evidence contains prohibited phrase: {phrase!r}")
    return errors


def run_external(
    command: str,
    scenario: dict[str, object],
    timeout: int = 900,
    evidence_root: Path | None = None,
) -> dict[str, object]:
    dispatched = dict(scenario)
    dispatched["_challenge"] = secrets.token_hex(32)
    temporary_evidence = tempfile.TemporaryDirectory() if evidence_root is None else None
    evidence_root = Path(temporary_evidence.name) if temporary_evidence else evidence_root
    assert evidence_root is not None
    evidence_root.mkdir(parents=True, exist_ok=True)
    dispatched["_evidence_root"] = str(evidence_root.resolve())

    allowed_env = {
        "PATH", "PATHEXT", "SystemRoot", "WINDIR", "ComSpec", "TEMP", "TMP",
        "HOME", "USERPROFILE", "PYTHONUTF8", "LANG", "LC_ALL",
    }
    child_env = {name: value for name, value in os.environ.items() if name in allowed_env}
    child_env["PYTHONUTF8"] = "1"
    process = subprocess.Popen(
        parse_adapter_command(command),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        env=child_env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        start_new_session=os.name != "nt",
    )
    assert process.stdin and process.stdout and process.stderr
    stdout_collector = BoundedCollector(MAX_TRANSCRIPT_BYTES)
    stderr_collector = BoundedCollector(MAX_TRANSCRIPT_BYTES)
    stdout_thread = threading.Thread(target=stdout_collector.drain, args=(process.stdout,), daemon=True)
    stderr_thread = threading.Thread(target=stderr_collector.drain, args=(process.stderr,), daemon=True)
    stdout_thread.start()
    stderr_thread.start()
    try:
        process.stdin.write(json.dumps(dispatched).encode("utf-8"))
        process.stdin.close()
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        process.wait()
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)
        if temporary_evidence:
            temporary_evidence.cleanup()
        return blocked_result(scenario, b"adapter timed out", [f"adapter timed out after {timeout} seconds"])

    stdout_thread.join(timeout=5)
    stderr_thread.join(timeout=5)
    stdout_bytes = bytes(stdout_collector.data)
    stderr_bytes = bytes(stderr_collector.data)
    transcript = stdout_bytes + stderr_bytes
    try:
        claim: object = json.loads(
            stdout_bytes.decode("utf-8", errors="replace"),
            object_pairs_hook=unique_object,
        )
    except (json.JSONDecodeError, ValueError):
        claim = None
    errors = validate_adapter_claim(dispatched, claim, evidence_root)
    if returncode != 0:
        errors.append(f"external adapter exited with {returncode}")
    if stdout_collector.too_large or stderr_collector.too_large:
        errors.append(f"adapter transcript exceeds {MAX_TRANSCRIPT_BYTES} bytes")
    passed = not errors and isinstance(claim, dict)
    result: dict[str, object] = {
        "scenario_id": scenario["id"],
        "adapter": "external-command",
        "fresh_context": bool(passed and claim.get("fresh_context")),
        "result": "PASS" if passed else "BLOCKED",
        "transcript_sha256": hashlib.sha256(transcript).hexdigest(),
        "redacted_summary": "external adapter behavior contract validated" if passed else "external adapter claim was rejected",
        "loaded_skills": claim.get("loaded_skills", []) if passed else [],
        "gate_evidence": claim.get("gate_evidence", []) if passed else [],
        "validation_errors": errors,
        "invocation_id": claim.get("invocation_id", "") if isinstance(claim, dict) else "",
    }
    if passed:
        result["adapter_claim"] = claim
        result["dispatched_scenario"] = dispatched
    if temporary_evidence:
        temporary_evidence.cleanup()
    return result


def blocked_result(scenario: dict[str, object], transcript: bytes, errors: list[str]) -> dict[str, object]:
    return {
        "scenario_id": scenario["id"],
        "adapter": "external-command",
        "fresh_context": False,
        "result": "BLOCKED",
        "transcript_sha256": hashlib.sha256(transcript).hexdigest(),
        "redacted_summary": "Optional live behavior eval was not completed.",
        "loaded_skills": [],
        "gate_evidence": [],
        "validation_errors": errors,
        "invocation_id": "",
    }


def load_cases(root: Path) -> list[dict[str, object]]:
    e2e = json.loads((root / "evals" / "end-to-end-delivery.json").read_text(encoding="utf-8"))["cases"]
    behavioral = json.loads((root / "evals" / "behavioral-scenarios.json").read_text(encoding="utf-8"))["cases"]
    cases = [
        {
            "id": case["id"],
            "prompt": case["prompt"],
            "skills": [case["primary"], *case["required_gates"]],
            "primary_skill": case["primary"],
            "required_gates": case["required_gates"],
        }
        for case in e2e
    ]
    cases.extend(
        {
            "id": case["id"],
            "prompt": case["scenario"],
            "skills": case["skills"],
            "required_gates": ["behavioral-contract"],
            "must_include": case["must_include"],
            "must_not_include": case["must_not_include"],
            **({"author_id": case["author_id"]} if "author_id" in case else {}),
            **({"changed_skill": case["changed_skill"]} if "changed_skill" in case else {}),
            **({"required_reviewer_skills": case["required_reviewer_skills"]} if "required_reviewer_skills" in case else {}),
        }
        for case in behavioral
    )
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root containing evals/")
    parser.add_argument("--adapter-command", default=os.environ.get("RIC_LIVE_EVAL_COMMAND"))
    parser.add_argument("--allow-external-command", action="store_true")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--run-id", default="repository-live-eval")
    parser.add_argument("--source-revision")
    args = parser.parse_args()
    cases = load_cases(args.root)
    if not args.adapter_command or not args.allow_external_command:
        results = [blocked_result(case, b"adapter unavailable", ["no independent live-eval adapter is available"]) for case in cases]
    else:
        base_evidence_root = args.evidence_root or (
            args.output.parent / "live-eval-evidence" if args.output else args.root / ".ric-work" / "live-eval-evidence"
        )
        results = [
            run_external(args.adapter_command, case, args.timeout, base_evidence_root / str(case["id"]))
            for case in cases
        ]
    source_revision = args.source_revision
    if not source_revision:
        completed = subprocess.run(
            ["git", "-C", str(args.root), "rev-parse", "HEAD"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        source_revision = completed.stdout.strip() if completed.returncode == 0 else "unavailable"
    invocation_ids = [str(result["invocation_id"]) for result in results if result["result"] == "PASS"]
    output = {
        "run_id": args.run_id,
        "source_revision": source_revision,
        "status": "PASS" if all(result["result"] == "PASS" for result in results) and len(invocation_ids) == len(set(invocation_ids)) else "BLOCKED",
        "results": results,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if output["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())




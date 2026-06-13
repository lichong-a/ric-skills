from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("run-live-evals.py")
SPEC = importlib.util.spec_from_file_location("run_live_evals", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def adapter_code(evidence_text: str = "review test", duplicate_actor: bool = False) -> str:
    return (
        "import hashlib,json,sys;from pathlib import Path;s=json.load(sys.stdin);"
        "root=Path(s['_evidence_root']);root.mkdir(parents=True,exist_ok=True);"
        f"text={evidence_text!r};"
        "[(root/(n+'.txt')).write_text(text) for n in s['required_gates']];"
        "g=[{'gate':n,'actor_id':('same' if "
        f"{duplicate_actor!r} else 'actor-'+str(i)),'role':'code-reviewer','loaded_skills':list(dict.fromkeys(([n] if n.startswith('ric-') else s.get('skills',[]))+([s['primary_skill']] if s.get('primary_skill') else []))),'fresh_context':True,'read_only':True,'result':'PASS','evidence_path':n+'.txt',"
        "'evidence_sha256':hashlib.sha256(text.encode()).hexdigest()} for i,n in enumerate(s['required_gates'])];"
        "c={'scenario_id':s['id'],'challenge':s['_challenge'],"
        "'scenario_sha256':hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest(),"
        "'result':'PASS','fresh_context':True,'invocation_id':'inv-1','loaded_skills':s.get('skills',[]),'gate_evidence':g};"
        "print(json.dumps(c))"
    )


def skill_quality_adapter_code(actor_id: str, loaded_skills: list[str]) -> str:
    return (
        "import hashlib,json,sys;from pathlib import Path;s=json.load(sys.stdin);"
        "p=Path(s['_evidence_root'])/'behavior.txt';p.write_text('dispatch a fresh-context skill reviewer load the changed skill and relevant domain skills evaluate trigger negative-trigger conflict and behavioral scenarios');"
        f"g=[{{'gate':'behavioral-contract','actor_id':{actor_id!r},'role':'skill-quality-reviewer','loaded_skills':{loaded_skills!r},'fresh_context':True,'read_only':True,'result':'PASS','evidence_path':'behavior.txt','evidence_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}}];"
        "c={'scenario_id':s['id'],'challenge':s['_challenge'],'scenario_sha256':hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest(),"
        f"'result':'PASS','fresh_context':True,'invocation_id':'inv-skill','loaded_skills':{loaded_skills!r},'gate_evidence':g}};print(json.dumps(c))"
    )


def split_skill_quality_adapter_code() -> str:
    return (
        "import hashlib,json,sys;from pathlib import Path;s=json.load(sys.stdin);"
        "root=Path(s['_evidence_root']);"
        "p1=root/'behavior.txt';p1.write_text('evaluate trigger negative-trigger conflict and behavioral scenarios');"
        "p2=root/'witness.txt';p2.write_text('load the changed skill and relevant domain skills');"
        "g=["
        "{'gate':'behavioral-contract','actor_id':'reviewer-1','role':'skill-quality-reviewer','loaded_skills':['ric-skill-quality','ric-independent-review'],'fresh_context':True,'read_only':True,'result':'PASS','evidence_path':'behavior.txt','evidence_sha256':hashlib.sha256(p1.read_bytes()).hexdigest()},"
        "{'gate':'bundle-witness','actor_id':'reviewer-2','role':'design-qa-reviewer','loaded_skills':['ric-skill-quality','ric-independent-review','ric-admin-console'],'fresh_context':True,'read_only':True,'result':'PASS','evidence_path':'witness.txt','evidence_sha256':hashlib.sha256(p2.read_bytes()).hexdigest()}"
        "];"
        "c={'scenario_id':s['id'],'challenge':s['_challenge'],'scenario_sha256':hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest(),"
        "'result':'PASS','fresh_context':True,'invocation_id':'inv-split','loaded_skills':['ric-skill-quality','ric-independent-review','ric-admin-console'],'gate_evidence':g};print(json.dumps(c))"
    )


class LiveEvalAdapterTests(unittest.TestCase):
    def test_explicit_external_adapter_validates_behavior_contract(self) -> None:
        scenario = {"id": "adapter-smoke", "skills": ["ric-code-review"], "required_gates": ["review", "test"]}
        result = module.run_external(json.dumps([sys.executable, "-c", adapter_code()]), scenario)
        self.assertEqual("PASS", result["result"])
        self.assertEqual(["ric-code-review"], result["loaded_skills"])
        self.assertEqual(2, len(result["gate_evidence"]))

    def test_missing_required_skill_is_blocked(self) -> None:
        code = adapter_code().replace("'loaded_skills':s.get('skills',[])", "'loaded_skills':[]")
        result = module.run_external(
            json.dumps([sys.executable, "-c", code]),
            {"id": "adapter-smoke", "skills": ["ric-code-review"], "required_gates": ["review"]},
        )
        self.assertEqual("BLOCKED", result["result"])
        self.assertIn("omitted required skills", " ".join(result["validation_errors"]))

    def test_missing_evidence_is_blocked(self) -> None:
        code = (
            "import hashlib,json,sys;s=json.load(sys.stdin);"
            "g=[{'gate':'review','actor_id':'actor-1','role':'code-reviewer','loaded_skills':s.get('skills',[]),'fresh_context':True,'read_only':True,'result':'PASS','evidence_path':'missing.txt','evidence_sha256':'a'*64}];"
            "c={'scenario_id':s['id'],'challenge':s['_challenge'],'scenario_sha256':hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest(),"
            "'result':'PASS','fresh_context':True,'invocation_id':'inv-1','loaded_skills':s.get('skills',[]),'gate_evidence':g};print(json.dumps(c))"
        )
        result = module.run_external(
            json.dumps([sys.executable, "-c", code]),
            {"id": "adapter-smoke", "skills": [], "required_gates": ["review"]},
        )
        self.assertEqual("BLOCKED", result["result"])
        self.assertIn("missing or unsafe", " ".join(result["validation_errors"]))

    def test_behavioral_evidence_must_satisfy_assertions(self) -> None:
        scenario = {
            "id": "behavior",
            "skills": ["ric-delivery-loop"],
            "required_gates": ["behavioral-contract"],
            "must_include": ["independent review still runs"],
            "must_not_include": ["shortcut taken"],
        }
        result = module.run_external(json.dumps([sys.executable, "-c", adapter_code("shortcut taken")]), scenario)
        self.assertEqual("BLOCKED", result["result"])
        joined = " ".join(result["validation_errors"])
        self.assertIn("omits required phrase", joined)
        self.assertIn("contains prohibited phrase", joined)

    def test_reused_actor_is_blocked(self) -> None:
        result = module.run_external(
            json.dumps([sys.executable, "-c", adapter_code(duplicate_actor=True)]),
            {"id": "adapter-smoke", "skills": [], "required_gates": ["review", "test"]},
        )
        self.assertEqual("BLOCKED", result["result"])

    def test_skill_quality_rejects_author_self_approval_and_missing_changed_skill(self) -> None:
        scenario = {
            "id": "skill-quality",
            "skills": ["ric-skill-quality", "ric-independent-review"],
            "required_gates": ["behavioral-contract"],
            "author_id": "skill-author-1",
            "changed_skill": "ric-admin-console",
            "required_reviewer_skills": ["ric-skill-quality", "ric-independent-review", "ric-admin-console"],
        }
        author_result = module.run_external(
            json.dumps([sys.executable, "-c", skill_quality_adapter_code("skill-author-1", ["ric-skill-quality", "ric-independent-review", "ric-admin-console"])]),
            scenario,
        )
        self.assertEqual("BLOCKED", author_result["result"])
        missing_result = module.run_external(
            json.dumps([sys.executable, "-c", skill_quality_adapter_code("reviewer-1", ["ric-skill-quality", "ric-independent-review"])]),
            scenario,
        )
        self.assertEqual("BLOCKED", missing_result["result"])

    def test_skill_quality_bundle_and_behavior_must_be_bound_to_required_gate(self) -> None:
        scenario = {
            "id": "skill-quality",
            "skills": ["ric-skill-quality", "ric-independent-review"],
            "required_gates": ["behavioral-contract"],
            "author_id": "skill-author-1",
            "changed_skill": "ric-admin-console",
            "required_reviewer_skills": ["ric-skill-quality", "ric-independent-review", "ric-admin-console"],
            "must_include": ["evaluate trigger negative-trigger conflict and behavioral scenarios"],
        }
        result = module.run_external(
            json.dumps([sys.executable, "-c", split_skill_quality_adapter_code()]),
            scenario,
        )
        self.assertEqual("BLOCKED", result["result"])
        self.assertIn("no reviewer loaded required skill bundle", " ".join(result["validation_errors"]))

    def test_hostile_claim_types_are_blocked_without_crash(self) -> None:
        for value in ('["hostile"]', '{"scenario_id":"adapter-smoke"}'):
            result = module.run_external(
                json.dumps([sys.executable, "-c", f"print({value!r})"]),
                {"id": "adapter-smoke", "skills": [], "required_gates": ["review"]},
            )
            self.assertEqual("BLOCKED", result["result"])

    def test_adapter_receives_only_allowlisted_environment(self) -> None:
        previous = os.environ.get("AWS_SECRET_ACCESS_KEY")
        os.environ["AWS_SECRET_ACCESS_KEY"] = "must-not-leak"
        try:
            result = module.run_external(
                json.dumps([sys.executable, "-c", "import os; print(os.getenv('AWS_SECRET_ACCESS_KEY','missing'))"]),
                {"id": "adapter-smoke", "skills": [], "required_gates": []},
            )
            self.assertEqual("BLOCKED", result["result"])
            self.assertNotIn("must-not-leak", result["redacted_summary"])
        finally:
            if previous is None:
                os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
            else:
                os.environ["AWS_SECRET_ACCESS_KEY"] = previous

    def test_oversized_adapter_output_is_bounded_and_blocked(self) -> None:
        result = module.run_external(
            json.dumps([sys.executable, "-c", "import sys; sys.stdout.write('x' * (5 * 1024 * 1024))"]),
            {"id": "adapter-smoke", "skills": [], "required_gates": []},
        )
        self.assertEqual("BLOCKED", result["result"])
        self.assertIn("adapter transcript exceeds", " ".join(result["validation_errors"]))

    def test_timed_out_adapter_is_blocked(self) -> None:
        result = module.run_external(
            json.dumps([sys.executable, "-c", "import time; time.sleep(30)"]),
            {"id": "adapter-smoke", "skills": [], "required_gates": []},
            timeout=1,
        )
        self.assertEqual("BLOCKED", result["result"])
        self.assertIn("adapter timed out", " ".join(result["validation_errors"]))

    def test_fixer_role_cannot_be_reviewer(self) -> None:
        """A fresh-context claim with role 'fixer' must not pass the independent review gate."""
        code = adapter_code().replace("'role':'code-reviewer'", "'role':'fixer'")
        result = module.run_external(
            json.dumps([sys.executable, "-c", code]),
            {"id": "adapter-smoke", "skills": ["ric-code-review"], "required_gates": ["review"]},
        )
        self.assertEqual("BLOCKED", result["result"])
        joined = " ".join(result["validation_errors"])
        self.assertIn("not a recognized independent reviewer role", joined)

    def test_non_read_only_reviewer_is_blocked(self) -> None:
        """A reviewer without read_only=True must not pass."""
        code = adapter_code().replace("'read_only':True", "'read_only':False")
        result = module.run_external(
            json.dumps([sys.executable, "-c", code]),
            {"id": "adapter-smoke", "skills": ["ric-code-review"], "required_gates": ["review"]},
        )
        self.assertEqual("BLOCKED", result["result"])
        joined = " ".join(result["validation_errors"])
        self.assertIn("read_only=true", joined)

    def test_changed_skill_must_be_loaded(self) -> None:
        """If changed_skill is set, the qualifying reviewer must load it."""
        scenario = {
            "id": "skill-quality-changed",
            "skills": ["ric-skill-quality", "ric-independent-review"],
            "required_gates": ["behavioral-contract"],
            "author_id": "skill-author-1",
            "changed_skill": "ric-admin-console",
            "required_reviewer_skills": ["ric-skill-quality", "ric-independent-review"],
        }
        result = module.run_external(
            json.dumps([sys.executable, "-c", skill_quality_adapter_code("reviewer-1", ["ric-skill-quality", "ric-independent-review"])]),
            scenario,
        )
        self.assertEqual("BLOCKED", result["result"])
        joined = " ".join(result["validation_errors"])
        self.assertIn("ric-admin-console", joined)


if __name__ == "__main__":
    unittest.main()






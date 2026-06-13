"""Focused tests for the repository validator."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
assert SPEC and SPEC.loader
validate_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_skills
SPEC.loader.exec_module(validate_skills)


class ValidatorTests(unittest.TestCase):
    def test_find_cycles_reports_closed_path(self) -> None:
        cycles = validate_skills.find_cycles({"a": {"b"}, "b": {"a"}, "c": set()})
        self.assertEqual([["a", "b", "a"]], cycles)

    def test_strip_fenced_code_preserves_line_count(self) -> None:
        source = "before\n```md\n[bad](missing.md)\n```\nafter\n"
        stripped = validate_skills.strip_fenced_code(source)
        self.assertEqual(source.count("\n"), stripped.count("\n"))
        self.assertNotIn("missing.md", stripped)

    def test_frontmatter_rejects_extra_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            validator = validate_skills.Validator(root)
            text = (
                "---\n"
                "name: ric-example\n"
                "description: Use when testing a validator.\n"
                "metadata: forbidden\n"
                "---\n"
                "# Example\n"
            )
            validator.parse_frontmatter(root / "SKILL.md", text)
            self.assertIn("FM007", {issue.code for issue in validator.issues})

    def test_clean_markdown_target_removes_anchor_and_title(self) -> None:
        self.assertEqual(
            "references/example.md",
            validate_skills.clean_markdown_target(
                'references/example.md#section "Reference title"'
            ),
        )

    def test_external_target_detection_keeps_repo_root_links_local(self) -> None:
        self.assertFalse(validate_skills.is_external_target("/references/example.md"))
        self.assertFalse(validate_skills.is_external_target("C:/outside.md"))
        self.assertTrue(validate_skills.is_external_target("https://example.com/reference.md"))

    def test_catalog_detects_circular_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            catalog_path = root / "skills" / "catalog.json"
            catalog_path.parent.mkdir(parents=True)
            catalog_path.write_text(
                json.dumps(
                    {
                        "skills": {
                            "ric-loop": {
                                "allowed_roles": ["orchestrator"],
                                "default_role": "orchestrator",
                                "handoffs": ["ric-domain"]
                            },
                            "ric-domain": {
                                "allowed_roles": ["primary-executor"],
                                "default_role": "primary-executor",
                                "handoffs": ["ric-loop"]
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            validator = validate_skills.Validator(root)
            validator.skills = {
                name: validate_skills.SkillRecord(name, name, "Use when testing.", root, 1)
                for name in ("ric-loop", "ric-domain")
            }
            validator.validate_catalog()
            self.assertIn("CAT011", {issue.code for issue in validator.issues})

    def test_registry_rejects_name_path_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "skill.ps1").write_text(
                '"ric-example" = "skills/ric-other/SKILL.md"\n',
                encoding="utf-8",
            )
            validator = validate_skills.Validator(root)
            validator.skills = {
                "ric-example": validate_skills.SkillRecord(
                    "ric-example", "ric-example", "Use when testing.", root, 1
                )
            }
            validator.validate_registries()
            self.assertIn("SYNC001", {issue.code for issue in validator.issues})


if __name__ == "__main__":
    unittest.main()

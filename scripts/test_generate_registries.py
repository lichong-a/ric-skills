from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("generate-registries.py")
SPEC = importlib.util.spec_from_file_location("generate_registries", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class GenerateRegistriesTests(unittest.TestCase):
    def test_outputs_are_sorted_and_cover_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "skills").mkdir()
            (root / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": {
                            "ric-z": {"description": "z", "default_role": "modifier"},
                            "ric-a": {"description": "a", "default_role": "modifier"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "before\n<!-- BEGIN GENERATED SKILLS -->\nold\n<!-- END GENERATED SKILLS -->\nafter\n",
                encoding="utf-8",
            )
            values = module.outputs(root)
            llms = values[root / "skills" / "llms.txt"]
            self.assertLess(llms.index("ric-a"), llms.index("ric-z"))
            self.assertIn('"ric-z" = "skills/ric-z/SKILL.md"', values[root / "skill.ps1"])
            self.assertIn("| `ric-a` |", values[root / "README.md"])

    def test_safe_write_rejects_output_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root.parent / f"{root.name}-outside.txt"
            outside.write_text("unchanged", encoding="utf-8")
            link = root / "skill.ps1"
            try:
                link.symlink_to(outside)
            except OSError:
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(ValueError):
                module.safe_write(root, link, "changed")
            self.assertEqual("unchanged", outside.read_text(encoding="utf-8"))
            outside.unlink()


if __name__ == "__main__":
    unittest.main()

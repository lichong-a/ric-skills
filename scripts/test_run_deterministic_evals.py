from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("run-deterministic-evals.py")
SPEC = importlib.util.spec_from_file_location("run_deterministic_evals", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class DeterministicEvalTests(unittest.TestCase):
    def test_repository_fixtures_are_consistent(self) -> None:
        self.assertEqual([], module.evaluate(Path(__file__).resolve().parents[1]))


if __name__ == "__main__":
    unittest.main()

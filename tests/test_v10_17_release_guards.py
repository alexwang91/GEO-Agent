import unittest
from pathlib import Path

from geo_agent.release_guards import evaluate_release_guards

ROOT = Path(__file__).resolve().parents[1]


class V10ReleaseGuardTests(unittest.TestCase):
    def test_release_guards_pass_for_completed_v10(self):
        result = evaluate_release_guards(ROOT).to_dict()

        self.assertTrue(result["passed"])
        self.assertEqual(result["failures"], [])


if __name__ == "__main__":
    unittest.main()

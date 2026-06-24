import json
import tempfile
import unittest
from pathlib import Path

from geo_agent.cli import main


class ExampleFixtureTests(unittest.TestCase):
    def test_canonical_acme_fixture_runs_through_cli(self):
        repo_root = Path(__file__).resolve().parents[1]
        fixture_path = repo_root / "examples" / "acme-fixture.json"
        self.assertTrue(fixture_path.exists())

        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "acme"
            exit_code = main(["audit", str(fixture_path), "--out", str(output_dir)])

            self.assertEqual(exit_code, 0)
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["profile"], {"brand": "Acme AI", "domain": "acme.ai"})
        self.assertEqual(manifest["query_count"], 2)
        self.assertIn("score", report)
        self.assertIn("retest_plan", report)


if __name__ == "__main__":
    unittest.main()

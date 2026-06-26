import json
import tempfile
import unittest
from pathlib import Path

from geo_agent.fixture_package import run_fixture_package


def fixture():
    return {
        "profile": {
            "brand": "Acme AI",
            "aliases": ["Acme"],
            "domain": "acme.ai",
            "competitors": ["Globex"],
            "target_regions": ["US"],
            "target_languages": ["en"],
            "target_customer": "marketing teams",
            "main_product": "AI visibility platform",
            "category": "GEO software",
            "business_goal": "improve AI search visibility",
        },
        "pages": {
            "https://acme.ai/": "<html><head><title>Acme</title><link rel='canonical' href='https://acme.ai/'></head><body><h1>Acme AI</h1></body></html>"
        },
        "audit": {"manual_urls": ["https://acme.ai/"], "sitemap_urls": [], "max_queries": 2},
        "recorded_runs": {
            "engine": "recorded",
            "runs": {
                "What is Acme AI for marketing teams?": {"timestamp": "2026-06-24T00:00:00Z", "raw_answer": "Acme AI is a GEO platform.", "citations": ["https://acme.ai/"], "mentions": ["Acme AI"], "recommendations": ["Acme AI"]},
                "Best GEO software tools for marketing teams in US": {"timestamp": "2026-06-24T00:01:00Z", "raw_answer": "Globex appears in category lists.", "citations": ["https://globex.com/"], "mentions": ["Globex"], "recommendations": ["Globex"]},
            },
        },
        "metadata": {"secret": "SHOULD_NOT_APPEAR"},
    }


class AuditPackageManifestTests(unittest.TestCase):
    def test_manifest_v2_records_metric_to_sample_traceability(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "fixture.json"
            output_dir = root / "out"
            fixture_path.write_text(json.dumps(fixture()), encoding="utf-8")

            run_fixture_package(fixture_path, output_dir)
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(2, manifest["manifest_version"])
            traces = manifest["traceability"]["metric_to_sample_ids"]
            self.assertTrue(traces)
            self.assertIn("sample_ids", traces[0])
            self.assertTrue(traces[0]["sample_ids"])
            self.assertIn("prompt_ids", traces[0])
            self.assertIn("citation_ids", traces[0])

    def test_manifest_report_and_database_do_not_contain_fixture_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "fixture.json"
            output_dir = root / "out"
            fixture_path.write_text(json.dumps(fixture()), encoding="utf-8")

            run_fixture_package(fixture_path, output_dir)
            for filename in ["manifest.json", "report.json", "audit.sqlite"]:
                payload = (output_dir / filename).read_bytes().decode("utf-8", errors="ignore")
                self.assertNotIn("SHOULD_NOT_APPEAR", payload)
                self.assertNotIn("secret", payload.lower())


if __name__ == "__main__":
    unittest.main()

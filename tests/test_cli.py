import json
import tempfile
import unittest
from pathlib import Path

from geo_agent.cli import main
from geo_agent.evidence_store import EvidenceStore


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
                "What is Acme AI for marketing teams?": {
                    "timestamp": "2026-06-24T00:00:00Z",
                    "raw_answer": "Acme AI is a GEO platform.",
                    "citations": ["https://acme.ai/"],
                    "mentions": ["Acme AI"],
                    "recommendations": ["Acme AI"],
                },
                "Best GEO software tools for marketing teams in US": {
                    "timestamp": "2026-06-24T00:01:00Z",
                    "raw_answer": "Globex appears in category lists.",
                    "citations": ["https://globex.com/"],
                    "mentions": ["Globex"],
                    "recommendations": ["Globex"],
                },
            },
        },
        "metadata": {"name": "cli-fixture"},
    }


def capture_fixture():
    return {
        "profile": {
            "brand": "Huawei",
            "aliases": ["Huawei Watch"],
            "domain": "consumer.huawei.com",
            "competitors": ["Apple Watch", "Samsung Galaxy Watch"],
            "target_regions": ["HU"],
            "target_languages": ["en"],
            "target_customer": "Android fitness watch buyers",
            "main_product": "Huawei Watch Fit 5",
            "category": "smartwatches",
            "business_goal": "increase AI visibility",
        },
        "pages": {
            "https://consumer.huawei.com/en/wearables/": "<html><head><title>Huawei Wearables</title><link rel='canonical' href='https://consumer.huawei.com/en/wearables/'></head><body><h1>Huawei Watch</h1></body></html>"
        },
        "audit": {"manual_urls": ["https://consumer.huawei.com/en/wearables/"], "sitemap_urls": []},
        "captures": [
            {
                "engine": "perplexity",
                "query": "best smartwatches for Android",
                "answer_text": "Huawei Watch Fit 5 is mentioned with Apple Watch alternatives.",
                "citations": ["https://example.com/android-watch-guide"],
                "captured_at": "2026-06-29T12:00:00+00:00",
                "region": "HU",
                "language": "en",
                "brand": "Huawei",
                "brand_aliases": ["Huawei Watch Fit 5"],
                "recommendations": ["Huawei Watch Fit 5"],
            },
            {
                "engine": "chatgpt_search",
                "query": "best fitness watches",
                "answer_text": "Apple Watch and Samsung Galaxy Watch are common shortlist items.",
                "citations": ["https://example.com/fitness-watch-guide"],
                "captured_at": "2026-06-29T12:01:00+00:00",
                "region": "HU",
                "language": "en",
                "brand": "Huawei",
                "recommendations": ["Apple Watch", "Samsung Galaxy Watch"],
            },
        ],
        "metadata": {"name": "manual-capture-fixture"},
    }


class CliTests(unittest.TestCase):
    def test_cli_writes_reproducible_audit_package_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "fixture.json"
            output_dir = root / "out"
            fixture_path.write_text(json.dumps(fixture()), encoding="utf-8")

            exit_code = main(["audit", str(fixture_path), "--out", str(output_dir)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertTrue((output_dir / "report.json").exists())
            self.assertTrue((output_dir / "report.md").exists())
            self.assertTrue((output_dir / "audit.sqlite").exists())
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            report_json = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            report_md = (output_dir / "report.md").read_text(encoding="utf-8")
            with EvidenceStore(output_dir / "audit.sqlite") as store:
                self.assertEqual(store.count_runs(), 2)
                self.assertEqual(len(store.list_query_records()), 2)
                self.assertEqual(len(store.list_page_records()), 1)
                self.assertEqual(len(store.list_diagnoses()), 2)
                self.assertEqual(len(store.list_tasks()), 2)
                self.assertEqual(len(store.list_report_artifacts()), 2)

        self.assertEqual(manifest["profile"], {"brand": "Acme AI", "domain": "acme.ai"})
        self.assertEqual(manifest["engine"], "recorded")
        self.assertEqual(manifest["query_count"], 2)
        self.assertEqual(manifest["page_count"], 1)
        self.assertEqual(manifest["run_count"], 2)
        self.assertEqual(manifest["evidence_database"], "audit.sqlite")
        self.assertEqual(manifest["artifacts"], ["manifest.json", "report.json", "report.md", "audit.sqlite"])
        self.assertIn("score", report_json)
        self.assertIn("missing_queries", report_json)
        self.assertIn("competitor_map", report_json)
        self.assertIn("cited_sources", report_json)
        self.assertIn("failures", report_json)
        self.assertIn("recommended_actions", report_json)
        self.assertIn("retest_plan", report_json)
        self.assertIn("# GEO Agent Operational Report", report_md)
        self.assertIn("## Retest Plan", report_md)

    def test_cli_writes_package_from_multi_engine_manual_captures_without_query_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "captures.json"
            output_dir = root / "capture-out"
            fixture_path.write_text(json.dumps(capture_fixture()), encoding="utf-8")

            exit_code = main(["capture-package", str(fixture_path), "--out", str(output_dir)])

            self.assertEqual(exit_code, 0)
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            report_json = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            with EvidenceStore(output_dir / "audit.sqlite") as store:
                runs = store.list_runs()
                queries = store.list_query_records()
                self.assertEqual(store.count_runs(), 2)
                self.assertEqual(len(queries), 2)
                self.assertEqual(len(store.list_runs(engine="perplexity")), 1)
                self.assertEqual(len(store.list_runs(engine="chatgpt_search")), 1)
                self.assertEqual([query.query for query in queries], [run.query for run in runs])
                self.assertEqual([query.target_engine for query in queries], [run.engine for run in runs])

        self.assertEqual(manifest["input_type"], "manual_capture_package")
        self.assertEqual(manifest["engine"], "multi_engine_manual_capture")
        self.assertEqual(manifest["engines"], ["chatgpt_search", "perplexity"])
        self.assertEqual(manifest["capture_count"], 2)
        self.assertEqual(manifest["run_count"], 2)
        self.assertIn("score", report_json)
        self.assertIn("recommended_actions", report_json)


if __name__ == "__main__":
    unittest.main()

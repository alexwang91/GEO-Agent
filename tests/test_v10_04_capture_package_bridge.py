import json
import tempfile
import unittest
from pathlib import Path

from geo_agent.cli import main
from geo_agent.evidence_store import EvidenceStore


class V10CapturePackageBridgeTests(unittest.TestCase):
    def test_multi_engine_manual_captures_build_real_package_without_query_generation(self):
        fixture = {
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
                "https://consumer.huawei.com/en/wearables/": "<html><head><title>Huawei Wearables</title></head><body><h1>Huawei Watch</h1></body></html>"
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
            "metadata": {"name": "v10-capture-package-fixture"},
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "captures.json"
            output_dir = root / "capture-out"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

            exit_code = main(["capture-package", str(fixture_path), "--out", str(output_dir)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertTrue((output_dir / "report.json").exists())
            self.assertTrue((output_dir / "audit.sqlite").exists())
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            with EvidenceStore(output_dir / "audit.sqlite") as store:
                runs = store.list_runs()
                queries = store.list_query_records()
                self.assertEqual(store.count_runs(), 2)
                self.assertEqual(len(store.list_runs(engine="perplexity")), 1)
                self.assertEqual(len(store.list_runs(engine="chatgpt_search")), 1)
                self.assertEqual([query.query for query in queries], [run.query for run in runs])
                self.assertEqual([query.target_engine for query in queries], [run.engine for run in runs])

        self.assertEqual(manifest["input_type"], "manual_capture_package")
        self.assertEqual(manifest["engine"], "multi_engine_manual_capture")
        self.assertEqual(manifest["engines"], ["chatgpt_search", "perplexity"])
        self.assertEqual(manifest["capture_count"], 2)
        self.assertEqual(manifest["run_count"], 2)


if __name__ == "__main__":
    unittest.main()

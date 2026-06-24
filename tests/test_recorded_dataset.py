import tempfile
import unittest
from pathlib import Path

from geo_agent.audit_runner import AuditRunner
from geo_agent.recorded_dataset import RecordedDatasetError, load_recorded_dataset, load_recorded_dataset_from_mapping


def dataset():
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
        "metadata": {"name": "acme-fixture"},
    }


class RecordedDatasetTests(unittest.TestCase):
    def test_valid_dataset_loads_audit_runner_compatible_objects(self):
        loaded = load_recorded_dataset_from_mapping(dataset())
        runner = AuditRunner()

        artifacts = runner.run(
            loaded.profile,
            pages=loaded.pages,
            engine_adapter=loaded.engine_adapter,
            manual_urls=loaded.manual_urls,
            sitemap_urls=loaded.sitemap_urls,
            max_queries=loaded.max_queries,
        )

        self.assertEqual(loaded.profile.brand, "Acme AI")
        self.assertEqual(loaded.engine_adapter.engine, "recorded")
        self.assertEqual(len(artifacts.runs), 2)
        self.assertIn("score", artifacts.report.to_dict())

    def test_loads_from_json_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.json"
            path.write_text(__import__("json").dumps(dataset()), encoding="utf-8")

            loaded = load_recorded_dataset(path)

        self.assertEqual(loaded.metadata, {"name": "acme-fixture"})

    def test_rejects_missing_required_section(self):
        payload = dataset()
        del payload["recorded_runs"]

        with self.assertRaisesRegex(RecordedDatasetError, "missing required"):
            load_recorded_dataset_from_mapping(payload)

    def test_rejects_malformed_urls(self):
        payload = dataset()
        payload["pages"] = {"not-a-url": "<html></html>"}

        with self.assertRaisesRegex(RecordedDatasetError, "Invalid page URL"):
            load_recorded_dataset_from_mapping(payload)

    def test_rejects_malformed_recorded_runs(self):
        payload = dataset()
        query = "What is Acme AI for marketing teams?"
        del payload["recorded_runs"]["runs"][query]["raw_answer"]

        with self.assertRaisesRegex(RecordedDatasetError, "raw_answer"):
            load_recorded_dataset_from_mapping(payload)


if __name__ == "__main__":
    unittest.main()

import unittest

from geo_agent.manual_import import ManualImportError, validate_manual_import


def valid_payload():
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
            "https://acme.ai/": "<html><head><title>Acme</title></head><body><h1>Acme AI</h1></body></html>"
        },
        "audit": {"manual_urls": ["https://acme.ai/"], "sitemap_urls": [], "max_queries": 1},
        "recorded_runs": {
            "engine": "manual_import",
            "runs": {
                "What is Acme AI for marketing teams?": {
                    "timestamp": "2026-06-25T00:00:00Z",
                    "raw_answer": "Acme AI is mentioned with a citation.",
                    "citations": ["https://acme.ai/"],
                    "mentions": ["Acme AI"],
                    "recommendations": ["Acme AI"],
                }
            },
        },
        "metadata": {"name": "manual-import-fixture"},
    }


class ManualImportTests(unittest.TestCase):
    def test_valid_manual_import_returns_safe_summary(self):
        result = validate_manual_import(valid_payload(), source_label="uploaded-json")
        payload = result.to_dict()

        self.assertEqual(payload["source_label"], "uploaded-json")
        self.assertEqual(payload["brand"], "Acme AI")
        self.assertEqual(payload["domain"], "acme.ai")
        self.assertEqual(payload["engine"], "manual_import")
        self.assertEqual(payload["page_count"], 1)
        self.assertEqual(payload["manual_url_count"], 1)
        self.assertEqual(payload["sitemap_url_count"], 0)
        self.assertEqual(payload["max_queries"], 1)
        self.assertNotIn("raw_answer", payload)
        self.assertNotIn("citations", payload)

    def test_manual_import_rejects_unsafe_fields(self):
        payload = valid_payload()
        unsafe_name = "session" + "_" + "token"
        payload["metadata"] = {unsafe_name: "sample-value"}

        with self.assertRaises(ManualImportError) as error:
            validate_manual_import(payload)

        self.assertIn("payload.metadata.session_token", str(error.exception))

    def test_manual_import_rejects_bad_schema_with_safe_error(self):
        payload = valid_payload()
        payload["recorded_runs"]["runs"] = {}

        with self.assertRaises(ManualImportError) as error:
            validate_manual_import(payload)

        self.assertIn("recorded_runs.runs must be a non-empty", str(error.exception))
        self.assertNotIn("Acme AI is mentioned", str(error.exception))

    def test_manual_import_preserves_package_compatibility(self):
        result = validate_manual_import(valid_payload())
        dataset = result.dataset

        self.assertEqual(dataset.profile.brand, "Acme AI")
        self.assertEqual(dataset.engine_adapter.engine, "manual_import")
        self.assertEqual(dataset.manual_urls, ["https://acme.ai/"])
        self.assertEqual(dataset.max_queries, 1)
        self.assertIn("https://acme.ai/", dataset.pages)

    def test_manual_import_warnings_for_low_coverage_dataset(self):
        payload = valid_payload()
        payload["audit"] = {"manual_urls": [], "sitemap_urls": []}

        result = validate_manual_import(payload)

        self.assertIn("No manual or sitemap URLs", result.warnings[0])


if __name__ == "__main__":
    unittest.main()

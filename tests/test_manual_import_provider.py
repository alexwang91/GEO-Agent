import unittest

from geo_agent.manual_import import ManualImportError
from geo_agent.providers.manual_import import ManualImportProvider, ManualImportProviderRequest


def payload():
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
            "engine": "manual-chatgpt",
            "runs": {
                "What is Acme AI for marketing teams?": {"timestamp": "2026-06-24T00:00:00Z", "raw_answer": "Acme AI is a GEO platform.", "citations": ["https://acme.ai/"], "mentions": ["Acme AI"], "recommendations": ["Acme AI"]},
                "Best GEO software tools for marketing teams in US": {"timestamp": "2026-06-24T00:01:00Z", "raw_answer": "Globex appears in category lists.", "citations": ["https://globex.com/"], "mentions": ["Globex"], "recommendations": ["Globex"]},
            },
        },
    }


class ManualImportProviderTests(unittest.TestCase):
    def test_valid_manual_import_feeds_shared_evidence_graph(self):
        result = ManualImportProvider().run(ManualImportProviderRequest(payload(), source_label="chatgpt-manual"))
        graph = result.artifacts.evidence_graph
        self.assertEqual("chatgpt-manual", result.import_result.source_label)
        self.assertEqual("Acme AI", graph.audit_run.brand)
        self.assertEqual(2, len(graph.samples))
        self.assertTrue(graph.citations)
        self.assertTrue(graph.metrics)
        self.assertEqual("manual-chatgpt", graph.samples[0].engine)

    def test_provider_rejects_unsafe_import_fields(self):
        unsafe = payload()
        unsafe["recorded_runs"]["api_key"] = "SHOULD_NOT_BE_ACCEPTED"
        with self.assertRaises(ManualImportError):
            ManualImportProvider().run(ManualImportProviderRequest(unsafe))

    def test_provider_result_serializes_without_raw_payload(self):
        result = ManualImportProvider().run(ManualImportProviderRequest(payload()))
        serialized = result.to_dict()
        self.assertIn("artifacts", serialized)
        self.assertNotIn("payload", serialized)
        self.assertNotIn("recorded_runs", serialized)


if __name__ == "__main__":
    unittest.main()

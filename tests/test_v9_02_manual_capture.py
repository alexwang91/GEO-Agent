import unittest

from geo_agent.engine_sampling import run_from_payload
from geo_agent.manual_capture import import_manual_capture, import_manual_captures, manual_captures_to_engine_runs
from geo_agent.provider_access import ProviderAccessError
from geo_agent.visibility_scoring import compute_visibility_components


class ManualCaptureImportTests(unittest.TestCase):
    def test_import_capture_to_engine_run_with_mentions_and_domains(self):
        record = import_manual_capture(
            {
                "engine": "chatgpt_search",
                "query": "best acme alternative",
                "answer_text": "Acme is cited by https://example.com/acme and is often recommended.",
                "citations": ["https://example.com/acme"],
                "captured_at": "2026-06-27T12:00:00+00:00",
                "region": "US",
                "language": "en",
                "brand": "Acme",
                "brand_aliases": ["ACME Inc"],
            }
        )
        run = record.to_engine_run()
        self.assertEqual("chatgpt_search", run.engine)
        self.assertEqual(("https://example.com/acme",), run.citations)
        self.assertEqual(("example.com",), run.source_domains)
        self.assertIn("Acme", run.mentions)

    def test_import_capture_preserves_recommendations_for_scoring(self):
        record = import_manual_capture(
            {
                "engine": "perplexity",
                "query": "best smartwatches for Android",
                "answer_text": "The answer recommends Huawei and alternatives.",
                "citations": ["https://consumer.huawei.com/en/wearables/"],
                "captured_at": "2026-06-29T12:00:00+00:00",
                "region": "HU",
                "language": "en",
                "brand": "Huawei",
                "recommendations": ["Huawei Watch GT 6 Pro"],
            }
        )

        run = record.to_engine_run()
        components = compute_visibility_components([run], brand="Huawei", brand_domain="consumer.huawei.com")

        self.assertEqual(("Huawei Watch GT 6 Pro",), run.recommendations)
        self.assertEqual(1.0, components.recommendation_share)

    def test_import_capture_requires_known_engine_and_iso_time(self):
        payload = {
            "engine": "unknown",
            "query": "q",
            "answer_text": "answer",
            "captured_at": "not a timestamp",
        }
        with self.assertRaises(ProviderAccessError):
            import_manual_capture(payload)
        payload["engine"] = "gemini"
        with self.assertRaises(ProviderAccessError):
            import_manual_capture(payload)

    def test_capture_rejects_sensitive_keys_before_normalization(self):
        with self.assertRaises(AssertionError):
            import_manual_capture(
                {
                    "engine": "perplexity",
                    "query": "q",
                    "answer_text": "answer",
                    "captured_at": "2026-06-27T12:00:00+00:00",
                    "api_key": "secret",
                }
            )

    def test_batch_import_and_engine_run_conversion(self):
        records = import_manual_captures(
            [
                {
                    "engine": "google_aio",
                    "query": "q1",
                    "answer_text": "Answer with https://source.example/page",
                    "citations": [],
                    "captured_at": "2026-06-27T12:00:00+00:00",
                },
                {
                    "engine": "manual_import",
                    "query": "q2",
                    "answer_text": "Second answer",
                    "captured_at": "2026-06-27T12:01:00+00:00",
                },
            ]
        )
        runs = manual_captures_to_engine_runs(records)
        self.assertEqual(2, len(runs))
        self.assertEqual(("https://source.example/page",), runs[0].citations)
        self.assertEqual("manual_import", runs[1].engine)

    def test_fallback_mentions_are_deduplicated_by_normalized_entity(self):
        run = run_from_payload(
            {
                "raw_answer": "Huawei Watch Fit 5 leads. Huawei Watch Fit 5 also beats generic trackers.",
                "brand": "Huawei",
                "brand_aliases": ["Watch Fit 5", "Huawei Watch Fit 5"],
            },
            engine="manual_import",
            query="best fitness watch",
            region="HU",
            language="en",
            timestamp="2026-06-29T12:01:00+00:00",
        )

        self.assertEqual(("Huawei Watch Fit 5",), run.mentions)


if __name__ == "__main__":
    unittest.main()

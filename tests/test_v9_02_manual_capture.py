import unittest

from geo_agent.manual_capture import import_manual_capture, import_manual_captures, manual_captures_to_engine_runs
from geo_agent.provider_access import ProviderAccessError


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
        self.assertEqual(("Acme",), run.mentions)

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


if __name__ == "__main__":
    unittest.main()

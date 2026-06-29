import unittest

from geo_agent.engine_sampling import run_from_payload
from geo_agent.manual_capture import import_manual_capture
from geo_agent.visibility_scoring import compute_visibility_components


class V10ManualCaptureRecommendationDedupTests(unittest.TestCase):
    def test_manual_capture_recommendations_flow_into_engine_run_scoring(self):
        record = import_manual_capture(
            {
                "engine": "perplexity",
                "query": "best smartwatches for Android",
                "answer_text": "The sampled answer recommends Huawei and alternatives.",
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

    def test_fallback_mentions_are_unique_longest_non_overlapping_matches(self):
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

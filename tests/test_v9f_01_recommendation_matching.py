import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.visibility_scoring import compute_visibility_components


class RecommendationMatchingRegressionTests(unittest.TestCase):
    def _run(self, recommendations: tuple[str, ...]) -> EngineRun:
        return EngineRun(
            engine="fixture",
            query="best smartwatches for Android",
            timestamp="2026-06-29T00:00:00+00:00",
            region="HU",
            language="en",
            raw_answer="A short answer with fixture recommendations.",
            citations=(),
            mentions=(),
            recommendations=recommendations,
            source_domains=(),
        )

    def test_huawei_brand_matches_huawei_product_recommendation(self):
        components = compute_visibility_components(
            [self._run(("Huawei Watch GT 6 Pro",))],
            brand="Huawei",
            brand_domain="consumer.huawei.com",
        )

        self.assertGreater(components.recommendation_share, 0.0)

    def test_apple_watch_exact_label_still_matches_product_recommendation(self):
        components = compute_visibility_components(
            [self._run(("Apple Watch",))],
            brand="Apple Watch",
            brand_domain="apple.com",
        )

        self.assertEqual(components.recommendation_share, 1.0)

    def test_huawei_does_not_match_inside_unrelated_token(self):
        components = compute_visibility_components(
            [self._run(("MegaHuaweiX Fitness Band",))],
            brand="Huawei",
            brand_domain="consumer.huawei.com",
        )

        self.assertEqual(components.recommendation_share, 0.0)


if __name__ == "__main__":
    unittest.main()

import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.visibility_scoring import compute_visibility_components


class V10RecommendationMatchingTests(unittest.TestCase):
    def _run(self, recommendations: tuple[str, ...]) -> EngineRun:
        return EngineRun(
            engine="fixture",
            query="best smartwatches for Android",
            timestamp="2026-06-29T00:00:00+00:00",
            region="HU",
            language="en",
            raw_answer="Fixture answer containing recommendation evidence.",
            citations=(),
            mentions=(),
            recommendations=recommendations,
            source_domains=(),
        )

    def test_brand_entity_matches_product_recommendation(self):
        components = compute_visibility_components(
            [self._run(("Huawei Watch GT 6 Pro",))],
            brand="Huawei",
            brand_domain="consumer.huawei.com",
        )

        self.assertEqual(components.recommendation_share, 1.0)

    def test_multi_token_brand_still_matches_exact_recommendation(self):
        components = compute_visibility_components(
            [self._run(("Apple Watch",))],
            brand="Apple Watch",
            brand_domain="apple.com",
        )

        self.assertEqual(components.recommendation_share, 1.0)

    def test_entity_matching_respects_token_boundaries(self):
        components = compute_visibility_components(
            [self._run(("MegaHuaweiX Fitness Band",))],
            brand="Huawei",
            brand_domain="consumer.huawei.com",
        )

        self.assertEqual(components.recommendation_share, 0.0)


if __name__ == "__main__":
    unittest.main()

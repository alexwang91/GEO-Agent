import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.visibility_scoring import compute_visibility_components


class V10VisibilityMetricTests(unittest.TestCase):
    def test_components_include_new_visibility_fields(self):
        run = EngineRun(
            engine="fixture",
            query="best smartwatches",
            timestamp="2026-06-29T00:00:00+00:00",
            region="HU",
            language="en",
            raw_answer="Huawei leads the category. Other brands follow.",
            citations=(),
            mentions=(),
            recommendations=("Huawei Watch GT 6 Pro",),
            source_domains=("consumer.huawei.com",),
        )

        components = compute_visibility_components([run], brand="Huawei", brand_domain="consumer.huawei.com")

        self.assertEqual(components.position_adjusted_word_count, 4.0)
        self.assertGreater(components.answer_rank_score, 0.0)
        self.assertGreater(components.subjective_impression_score, 0.8)
        self.assertIn("position_adjusted_word_count", components.to_dict())
        self.assertIn("subjective_impression_score", components.to_dict())


if __name__ == "__main__":
    unittest.main()

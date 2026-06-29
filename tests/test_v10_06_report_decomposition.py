import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.report_v2 import build_report_v2_from_runs
from geo_agent.visibility_scoring import score_weighted_visibility


class V10ReportDecompositionTests(unittest.TestCase):
    def test_report_has_per_engine_selection_absorption_attribution_layers(self):
        runs = (
            EngineRun(
                "perplexity",
                "best Android watch",
                "2026-06-29T12:00:00+00:00",
                "HU",
                "en",
                "Huawei Watch Fit 5 is mentioned with Apple Watch alternatives.",
                ("https://example.com/android-watch",),
                ("Huawei Watch Fit 5",),
                ("Huawei Watch Fit 5",),
                ("example.com",),
            ),
            EngineRun(
                "google_aio",
                "Huawei Watch Fit 5",
                "2026-06-29T12:02:00+00:00",
                "HU",
                "en",
                "Huawei Watch Fit 5 is cited from Huawei.",
                ("https://consumer.huawei.com/en/wearables/",),
                ("Huawei Watch Fit 5",),
                ("Huawei Watch Fit 5",),
                ("consumer.huawei.com",),
            ),
        )
        score = score_weighted_visibility(list(runs), brand="Huawei", brand_domain="consumer.huawei.com")

        report = build_report_v2_from_runs(runs, brand="Huawei", brand_domain="consumer.huawei.com", score=score).to_dict()

        titles = [section["title"] for section in report["sections"]]
        self.assertIn("Per-Engine Breakdown", titles)
        self.assertIn("Selection Absorption Attribution", titles)
        self.assertIn("Directional Aggregate", titles)
        decomposition = report["sections"][1]["items"][0]
        self.assertEqual(set(decomposition), {"selection", "absorption", "attribution"})
        self.assertEqual({item["layer"] for item in decomposition["selection"]}, {"selection"})
        self.assertEqual({item["layer"] for item in decomposition["absorption"]}, {"absorption"})
        self.assertEqual({item["layer"] for item in decomposition["attribution"]}, {"attribution"})
        per_engine = report["sections"][0]["items"][0]
        self.assertIn("decomposition", per_engine)
        aggregate = report["sections"][2]["items"][0]["aggregate_score"]
        self.assertEqual(aggregate["label"], "directional_not_verdict")


if __name__ == "__main__":
    unittest.main()

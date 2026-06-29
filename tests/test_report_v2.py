import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.report_v2 import build_engine_component_summary, build_report_v2, build_report_v2_from_runs
from geo_agent.visibility_scoring import score_weighted_visibility


class ReportV2Tests(unittest.TestCase):
    def test_build_report_has_required_sections_and_guardrails(self):
        report = build_report_v2({"visibility": 0.5}, ({"dx": "1"},), ({"task": "1"},), ({"retest": "1"},))
        payload = report.to_dict()
        self.assertEqual("AI Visibility Audit Report", payload["title"])
        self.assertEqual(["Metric Summary", "Diagnoses", "Optimization Tasks", "Retest Plan"], [section["title"] for section in payload["sections"]])
        self.assertIn("Low-sample results are directional.", payload["guardrails"])

    def test_engine_component_summary_leads_with_per_engine_metrics(self):
        runs = (
            EngineRun(
                "perplexity",
                "best Android watch",
                "2026-06-29T12:00:00+00:00",
                "HU",
                "en",
                "Huawei Watch Fit 5 is mentioned, but Apple Watch is also listed.",
                ("https://example.com/android-watch",),
                ("Huawei Watch Fit 5",),
                ("Huawei Watch Fit 5",),
                ("example.com",),
            ),
            EngineRun(
                "chatgpt_search",
                "best fitness watch",
                "2026-06-29T12:01:00+00:00",
                "HU",
                "en",
                "Apple Watch and Samsung Galaxy Watch are listed without Huawei.",
                ("https://example.com/fitness-watch",),
                ("Apple Watch",),
                ("Apple Watch",),
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

        summary = build_engine_component_summary(
            runs,
            brand="Huawei",
            brand_domain="consumer.huawei.com",
            competitors=("Apple Watch", "Samsung Galaxy Watch"),
        )

        self.assertEqual(summary["summary_type"], "per_engine_component_breakdown")
        self.assertEqual(summary["primary_interpretation"], "engine_breakdown_first")
        self.assertEqual(summary["aggregate_label"], "directional_not_verdict")
        by_engine = {item["engine"]: item for item in summary["engines"]}
        self.assertEqual(set(by_engine), {"chatgpt_search", "google_aio", "perplexity"})
        self.assertEqual(by_engine["perplexity"]["components"]["mention_share"], 1.0)
        self.assertEqual(by_engine["perplexity"]["components"]["owned_citation_share"], 0.0)
        self.assertEqual(by_engine["google_aio"]["components"]["owned_citation_share"], 1.0)
        self.assertEqual(by_engine["chatgpt_search"]["components"]["competitor_only_share"], 1.0)
        self.assertEqual(by_engine["chatgpt_search"]["directionality"], "directional_low_sample")

    def test_report_from_runs_has_engine_breakdown_and_directional_aggregate_label(self):
        runs = (
            EngineRun(
                "perplexity",
                "best Android watch",
                "2026-06-29T12:00:00+00:00",
                "HU",
                "en",
                "Huawei Watch Fit 5 is mentioned.",
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

        payload = build_report_v2_from_runs(runs, brand="Huawei", brand_domain="consumer.huawei.com", score=score).to_dict()

        self.assertEqual(["Per-Engine Breakdown", "Directional Aggregate", "Diagnoses", "Optimization Tasks", "Retest Plan"], [section["title"] for section in payload["sections"]])
        self.assertIn("A single aggregate score is directional, not a verdict.", payload["guardrails"])
        aggregate = payload["sections"][1]["items"][0]["aggregate_score"]
        self.assertEqual(aggregate["label"], "directional_not_verdict")
        per_engine = payload["sections"][0]["items"][0]
        self.assertEqual(per_engine["primary_interpretation"], "engine_breakdown_first")
        self.assertEqual(len(per_engine["engines"]), 2)


if __name__ == "__main__":
    unittest.main()

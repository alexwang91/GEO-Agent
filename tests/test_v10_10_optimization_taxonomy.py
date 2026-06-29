import unittest

from geo_agent.failure_debugger import FailureDiagnosis
from geo_agent.optimization_tasks import GEO_OPTIMIZATION_METHODS, generate_task_brief
from geo_agent.query_space import QueryRecord


class V10OptimizationTaxonomyTests(unittest.TestCase):
    def test_nine_methods_are_registered(self):
        self.assertEqual(
            set(GEO_OPTIMIZATION_METHODS),
            {
                "authoritative",
                "statistics_addition",
                "keyword_stuffing",
                "cite_sources",
                "quotation_addition",
                "easy_to_understand",
                "fluency_optimization",
                "unique_words",
                "technical_terms",
            },
        )

    def test_task_brief_carries_required_planning_fields(self):
        query = QueryRecord(
            query="best fitness watch",
            intent_type="category",
            funnel_stage="awareness",
            language="en",
            region="HU",
            target_engine="fixture_ai",
            competitor_entities=("Other Watch",),
            expected_answer_format="shortlist",
            priority_score=1.0,
            cluster="category:fitness-watch",
        )
        diagnosis = FailureDiagnosis(
            failure_types=("trust",),
            explanation="feature gap",
            next_step="Address gap.",
            evidence=("citation:1", "gap:quote"),
        )

        task = generate_task_brief(query, diagnosis, target_page="http://owned.test/acme-watch")
        payload = task.to_planning_dict()

        self.assertEqual(payload["method"], "quotation_addition")
        self.assertEqual(payload["owner"], "content_strategy")
        self.assertEqual(payload["expected_metric"], "claim_fidelity")
        self.assertEqual(payload["risk"], "draft_only_no_auto_publish")
        self.assertIn("citation:1", payload["evidence_ids"])
        self.assertIn("Retest category:fitness-watch", payload["retest_plan"])
        self.assertEqual(payload["confidence_source"], "legacy_default_requires_retest")
        self.assertGreater(payload["confidence"], 0.0)


if __name__ == "__main__":
    unittest.main()

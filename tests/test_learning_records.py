import unittest

from geo_agent.learning_records import (
    OptimizationOutcomeRecord,
    recommended_learning_actions,
    summarize_outcomes,
)


class LearningRecordsTests(unittest.TestCase):
    def test_outcome_record_serializes_required_learning_dimensions(self):
        record = OptimizationOutcomeRecord(
            engine="openai_compatible",
            query_type="comparison",
            vertical="GEO software",
            action="add comparison page evidence",
            confidence=0.75,
            result="improved",
            metric_delta=0.22,
            evidence_package_id="pkg-follow-up-001",
            notes="Citation share improved after page update.",
        )

        payload = record.to_dict()

        self.assertEqual(payload["engine"], "openai_compatible")
        self.assertEqual(payload["query_type"], "comparison")
        self.assertEqual(payload["vertical"], "GEO software")
        self.assertEqual(payload["action"], "add comparison page evidence")
        self.assertEqual(payload["confidence"], 0.75)
        self.assertEqual(payload["result"], "improved")
        self.assertEqual(payload["metric_delta"], 0.22)
        self.assertEqual(payload["evidence_package_id"], "pkg-follow-up-001")

    def test_outcome_record_validates_result_and_confidence(self):
        with self.assertRaises(ValueError):
            OptimizationOutcomeRecord(
                engine="openai_compatible",
                query_type="comparison",
                vertical="GEO software",
                action="add evidence",
                confidence=1.5,
                result="improved",
                metric_delta=0.1,
                evidence_package_id="pkg",
            )
        with self.assertRaises(ValueError):
            OptimizationOutcomeRecord(
                engine="openai_compatible",
                query_type="comparison",
                vertical="GEO software",
                action="add evidence",
                confidence=0.5,
                result="unknown",
                metric_delta=0.1,
                evidence_package_id="pkg",
            )

    def test_summarize_outcomes_groups_by_engine_query_vertical_and_action(self):
        records = [
            OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "add evidence", 0.8, "improved", 0.2, "pkg-1"),
            OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "add evidence", 0.6, "neutral", 0.0, "pkg-2"),
            OptimizationOutcomeRecord("gemini", "informational", "GEO software", "add FAQ", 0.7, "declined", -0.1, "pkg-3"),
        ]

        summaries = summarize_outcomes(records)
        first = summaries[0].to_dict()
        second = summaries[1].to_dict()

        self.assertEqual(len(summaries), 2)
        self.assertEqual(first["engine"], "gemini")
        self.assertEqual(first["declined_count"], 1)
        self.assertEqual(second["engine"], "openai_compatible")
        self.assertEqual(second["count"], 2)
        self.assertEqual(second["improved_count"], 1)
        self.assertEqual(second["neutral_count"], 1)
        self.assertAlmostEqual(second["average_delta"], 0.1)
        self.assertAlmostEqual(second["average_confidence"], 0.7)
        self.assertAlmostEqual(second["success_rate"], 0.5)

    def test_recommended_learning_actions_promote_successful_patterns(self):
        summary = summarize_outcomes(
            [
                OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "add evidence", 0.8, "improved", 0.2, "pkg-1"),
                OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "add evidence", 0.7, "improved", 0.1, "pkg-2"),
            ]
        )[0]

        actions = recommended_learning_actions(summary)

        self.assertIn("Promote this optimization pattern", actions[0])

    def test_recommended_learning_actions_handles_decline_and_inconclusive(self):
        declined = summarize_outcomes(
            [
                OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "thin page rewrite", 0.6, "declined", -0.2, "pkg-1"),
                OptimizationOutcomeRecord("openai_compatible", "comparison", "GEO software", "thin page rewrite", 0.4, "inconclusive", 0.0, "pkg-2"),
            ]
        )[0]

        actions = " ".join(recommended_learning_actions(declined))

        self.assertIn("Avoid repeating", actions)
        self.assertIn("Collect another follow-up package", actions)


if __name__ == "__main__":
    unittest.main()

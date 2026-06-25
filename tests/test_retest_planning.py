import unittest

from geo_agent.retest_planning import compare_retest_reports


def baseline_report():
    return {
        "score": {
            "visibility_score": 0.30,
            "mention_share": 0.40,
            "citation_share": 0.10,
            "recommendation_share": 0.20,
        },
        "missing_queries": ["missing old", "still missing"],
        "competitor_map": {"Globex": 2, "Initech": 1},
    }


def follow_up_report():
    return {
        "score": {
            "visibility_score": 0.55,
            "mention_share": 0.50,
            "citation_share": 0.30,
            "recommendation_share": 0.25,
        },
        "missing_queries": ["still missing", "new missing"],
        "competitor_map": {"Globex": 1, "Initech": 3},
    }


class RetestPlanningTests(unittest.TestCase):
    def test_compare_retest_reports_measures_metric_deltas(self):
        comparison = compare_retest_reports(baseline_report(), follow_up_report())
        deltas = {item.name: item for item in comparison.metric_deltas}

        self.assertAlmostEqual(deltas["visibility_score"].delta, 0.25)
        self.assertAlmostEqual(deltas["citation_share"].delta, 0.20)
        self.assertTrue(deltas["visibility_score"].improved)

    def test_compare_retest_reports_tracks_resolved_and_new_missing_queries(self):
        comparison = compare_retest_reports(baseline_report(), follow_up_report())

        self.assertEqual(comparison.resolved_missing_queries, ("missing old",))
        self.assertEqual(comparison.new_missing_queries, ("new missing",))

    def test_compare_retest_reports_tracks_competitor_deltas(self):
        comparison = compare_retest_reports(baseline_report(), follow_up_report())

        self.assertEqual(comparison.competitor_deltas["Globex"], -1)
        self.assertEqual(comparison.competitor_deltas["Initech"], 2)
        self.assertIn("Review competitor gains", " ".join(comparison.next_actions))

    def test_compare_retest_reports_serializes_plan(self):
        payload = compare_retest_reports(baseline_report(), follow_up_report()).to_dict()

        self.assertIn("metric_deltas", payload)
        self.assertEqual(payload["resolved_missing_queries"], ["missing old"])
        self.assertEqual(payload["new_missing_queries"], ["new missing"])
        self.assertTrue(payload["next_actions"])

    def test_compare_retest_reports_handles_no_improvement(self):
        comparison = compare_retest_reports(follow_up_report(), baseline_report())

        self.assertIn("Create optimization tasks", " ".join(comparison.next_actions))
        self.assertIn("Review competitor gains", " ".join(comparison.next_actions))

    def test_compare_retest_reports_rejects_missing_score_section(self):
        with self.assertRaises(ValueError) as error:
            compare_retest_reports({}, follow_up_report())

        self.assertIn("baseline.score", str(error.exception))


if __name__ == "__main__":
    unittest.main()

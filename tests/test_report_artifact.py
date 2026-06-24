import json
import unittest

from geo_agent.failure_debugger import FailureDiagnosis
from geo_agent.optimization_tasks import OptimizationTaskBrief
from geo_agent.report import build_report_view, render_report_json, render_report_markdown
from geo_agent.visibility_scoring import VisibilityScore


class ReportArtifactTests(unittest.TestCase):
    def test_report_json_has_stable_operational_shape(self):
        report = sample_report()

        payload = json.loads(render_report_json(report))

        self.assertEqual(sorted(payload.keys()), [
            "cited_sources",
            "competitor_map",
            "failures",
            "missing_queries",
            "recommended_actions",
            "retest_plan",
            "score",
        ])
        self.assertEqual(payload["score"]["mention_share"], 0.5)
        self.assertEqual(payload["missing_queries"], ["q missing"])
        self.assertEqual(payload["competitor_map"], {"Globex": 2})
        self.assertEqual(payload["cited_sources"], ["acme.ai", "globex.com"])
        self.assertEqual(payload["failures"], ["attribution"])
        self.assertEqual(payload["recommended_actions"], ["add_citable_claims"])
        self.assertEqual(payload["retest_plan"], ["Retest cluster on mock."])

    def test_report_markdown_contains_required_sections(self):
        markdown = render_report_markdown(sample_report())

        self.assertIn("# GEO Agent Operational Report", markdown)
        self.assertIn("## Score", markdown)
        self.assertIn("## Missing Queries", markdown)
        self.assertIn("## Competitor Map", markdown)
        self.assertIn("## Cited Sources", markdown)
        self.assertIn("## Failures", markdown)
        self.assertIn("## Recommended Actions", markdown)
        self.assertIn("## Retest Plan", markdown)
        self.assertIn("- q missing", markdown)
        self.assertIn("- add_citable_claims", markdown)

    def test_empty_report_sections_are_explicit(self):
        report = build_report_view(
            VisibilityScore(0.0, 0.0, 0.0, 0.0, 0, 0.0),
            missing_queries=[],
            competitor_mentions={},
            cited_sources=[],
            diagnoses=[],
            tasks=[],
        )

        markdown = render_report_markdown(report)

        self.assertIn("- none", markdown)
        self.assertEqual(report.to_dict()["retest_plan"], [])


def sample_report():
    score = VisibilityScore(0.5, 0.25, 0.25, 0.1, 2, 1.0)
    diagnosis = FailureDiagnosis(("attribution",), "brand without owned source", "Inspect page.", ("evidence",))
    task = OptimizationTaskBrief(
        action_type="add_citable_claims",
        target_page="https://acme.ai/page",
        query_cluster="comparison:en:US:mock",
        expected_impact="medium",
        confidence=0.72,
        risk="draft_only_no_auto_publish",
        draft_content="Draft update",
        retest_plan="Retest cluster on mock.",
        failure_type="attribution",
    )
    return build_report_view(
        score,
        missing_queries=["q missing"],
        competitor_mentions={"Globex": 2},
        cited_sources=["globex.com", "acme.ai", "acme.ai"],
        diagnoses=[diagnosis],
        tasks=[task],
    )


if __name__ == "__main__":
    unittest.main()

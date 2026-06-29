import unittest

from geo_agent.plugin_boundary import PluginResult, build_execution_brief, run_plugin


class FakePlugin:
    plugin_name = "fake-rewrite-skill"

    def execute(self, brief):
        return PluginResult(
            plugin_name=self.plugin_name,
            status="draft_ready",
            artifact_ref="artifact://drafts/task-1",
            claimed_method=brief.method,
            evidence_ids=brief.evidence_ids,
            warnings=("external executor",),
        )


class V10PluginBoundaryTests(unittest.TestCase):
    def test_task_plan_hands_off_to_external_plugin_reference(self):
        brief = build_execution_brief(
            {
                "method": "quotation_addition",
                "target_page": "http://owned.test/page",
                "query_cluster": "category:watch",
                "evidence_ids": ["citation:1"],
                "expected_metric": "claim_fidelity",
                "risk": "draft_only_no_auto_publish",
            },
            task_id="task:1",
        )

        result = run_plugin(FakePlugin(), brief).to_dict()

        self.assertEqual(result["claimed_method"], "quotation_addition")
        self.assertEqual(result["artifact_ref"], "artifact://drafts/task-1")
        self.assertEqual(result["evidence_ids"], ["citation:1"])
        self.assertIn("artifact_reference_only", brief.to_dict()["constraints"])


if __name__ == "__main__":
    unittest.main()

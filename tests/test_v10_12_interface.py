import unittest

from geo_agent.geoflow_interface import export_flow_input, import_flow_analytics


class V10InterfaceTests(unittest.TestCase):
    def test_export_plan_and_import_metrics_fixture(self):
        exported = export_flow_input(
            {
                "method": "cite_sources",
                "target_page": "http://owned.test/page",
                "query_cluster": "category:watch",
                "evidence_ids": ["citation:1"],
                "expected_metric": "owned_citation_share",
            },
            task_id="task:1",
        )

        self.assertEqual(exported["task_id"], "task:1")
        self.assertEqual(exported["evidence_ids"], ["citation:1"])
        evidence = import_flow_analytics(
            {
                "task_id": "task:1",
                "crawler": "fixture-crawler",
                "page_url": "http://owned.test/page",
                "ai_visit_count": 3,
                "referring_engine": "fixture_ai",
                "observed_at": "2026-06-29T12:00:00Z",
            }
        ).to_dict()

        self.assertEqual(evidence["source"], "geoflow_fixture")
        self.assertEqual(evidence["ai_visit_count"], 3)
        self.assertEqual(evidence["referring_engine"], "fixture_ai")


if __name__ == "__main__":
    unittest.main()

import json
import unittest

from geo_agent.audit_runner import AuditRunner
from geo_agent.engine_sampling import RecordedRunAdapter
from geo_agent.entity_profile import validate_entity_profile
from geo_agent.evidence_store import EvidenceStore


PROFILE = {
    "brand": "Acme AI",
    "aliases": ["Acme"],
    "domain": "acme.ai",
    "competitors": ["Globex"],
    "target_regions": ["US"],
    "target_languages": ["en"],
    "target_customer": "marketing teams",
    "main_product": "AI visibility platform",
    "category": "GEO software",
    "business_goal": "improve AI search visibility",
}

PAGE = """
<html>
  <head><title>Acme AI</title><link rel='canonical' href='https://acme.ai/'></head>
  <body><h1>Acme AI evidence hub</h1><p>Acme AI helps marketing teams improve AI search visibility.</p></body>
</html>
"""


def recorded_runs():
    profile = validate_entity_profile(PROFILE)
    queries = [
        f"What is {profile.brand} for {profile.target_customer}?",
        f"Best {profile.category} tools for {profile.target_customer} in US",
        f"Compare {profile.brand} with Globex",
    ]
    return {
        queries[0]: {
            "timestamp": "2026-06-24T00:00:00Z",
            "raw_answer": "Acme AI is a GEO platform for marketing teams.",
            "citations": ["https://acme.ai/"],
            "mentions": ["Acme AI"],
            "recommendations": ["Acme AI"],
        },
        queries[1]: {
            "timestamp": "2026-06-24T00:01:00Z",
            "raw_answer": "Globex is often listed for GEO software.",
            "citations": ["https://globex.com/guide"],
            "mentions": ["Globex"],
            "recommendations": ["Globex"],
        },
        queries[2]: {
            "timestamp": "2026-06-24T00:02:00Z",
            "raw_answer": "Acme AI and Globex are both options, but Acme AI has stronger owned evidence.",
            "citations": ["https://acme.ai/compare", "https://globex.com/compare"],
            "mentions": ["Acme AI", "Globex"],
            "recommendations": ["Acme AI"],
        },
    }


class AuditRunnerTests(unittest.TestCase):
    def test_fixture_audit_produces_report_artifacts_and_persists_runs(self):
        profile = validate_entity_profile(PROFILE)
        store = EvidenceStore()
        runner = AuditRunner(store)
        adapter = RecordedRunAdapter("recorded", recorded_runs())

        artifacts = runner.run(
            profile,
            pages={"https://acme.ai/": PAGE},
            engine_adapter=adapter,
            manual_urls=["https://acme.ai/"],
            max_queries=3,
        )

        self.assertEqual(len(artifacts.queries), 3)
        self.assertEqual(len(artifacts.pages), 1)
        self.assertEqual(len(artifacts.runs), 3)
        self.assertEqual(store.count_runs(), 3)

        payload = json.loads(artifacts.report_json)
        self.assertIn("score", payload)
        self.assertIn("missing_queries", payload)
        self.assertIn("competitor_map", payload)
        self.assertIn("cited_sources", payload)
        self.assertIn("failures", payload)
        self.assertIn("recommended_actions", payload)
        self.assertIn("retest_plan", payload)
        self.assertEqual(payload["competitor_map"], {"Globex": 2})
        self.assertIn("globex.com", payload["cited_sources"])
        self.assertIn("acme.ai", payload["cited_sources"])
        self.assertTrue(payload["recommended_actions"])
        self.assertIn("# GEO Agent Operational Report", artifacts.report_markdown)
        self.assertIn("## Retest Plan", artifacts.report_markdown)

    def test_fixture_audit_persists_full_evidence_graph(self):
        profile = validate_entity_profile(PROFILE)
        store = EvidenceStore()
        runner = AuditRunner(store)
        adapter = RecordedRunAdapter("recorded", recorded_runs())

        artifacts = runner.run(
            profile,
            pages={"https://acme.ai/": PAGE},
            engine_adapter=adapter,
            manual_urls=["https://acme.ai/"],
            max_queries=3,
        )

        self.assertEqual(store.list_query_records(), list(artifacts.queries))
        self.assertEqual(store.list_page_records(), list(artifacts.pages))
        self.assertEqual(store.list_runs(), list(artifacts.runs))
        self.assertEqual(store.list_diagnoses(), list(artifacts.diagnoses))
        self.assertEqual(store.list_tasks(), list(artifacts.tasks))
        reports = store.list_report_artifacts()
        self.assertEqual([item.format for item in reports], ["json", "markdown"])
        self.assertEqual(reports[0].content, artifacts.report_json)
        self.assertEqual(reports[1].content, artifacts.report_markdown)

    def test_runner_does_not_require_live_engine_or_network(self):
        profile = validate_entity_profile(PROFILE)
        runner = AuditRunner(EvidenceStore())
        adapter = RecordedRunAdapter("recorded", recorded_runs())

        artifacts = runner.run(
            profile,
            pages={"https://acme.ai/": PAGE},
            engine_adapter=adapter,
            manual_urls=["https://acme.ai/"],
            max_queries=1,
        )

        self.assertEqual(artifacts.runs[0].engine, "recorded")
        self.assertEqual(artifacts.pages[0].url, "https://acme.ai/")


if __name__ == "__main__":
    unittest.main()

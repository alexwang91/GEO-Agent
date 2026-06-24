import unittest

from geo_agent.engine_sampling import MockEngineAdapter, sample_engine
from geo_agent.experiments import create_experiment_plan
from geo_agent.failure_debugger import diagnose_citation_failure
from geo_agent.optimization_tasks import generate_task_brief
from geo_agent.query_space import build_query_space
from geo_agent.report import build_report_view
from geo_agent.visibility_scoring import score_visibility
from geo_agent.entity_profile import validate_entity_profile

PROFILE = validate_entity_profile({
    "brand": "Acme AI", "aliases": ["Acme"], "domain": "acme.ai", "competitors": ["Globex"],
    "target_regions": ["US"], "target_languages": ["en"], "target_customer": "marketing teams",
    "main_product": "visibility platform", "category": "GEO", "business_goal": "more demos",
})

class FinalWorkflowTests(unittest.TestCase):
    def test_m4_run_record_keeps_required_fields(self):
        adapter = MockEngineAdapter("mock", {"q": {"raw_answer": "Acme AI is cited.", "citations": ["https://acme.ai/a"], "mentions": ["Acme AI"], "recommendations": ["Acme AI"]}})
        run = sample_engine(adapter, "q", region="US", language="en", timestamp="2026-06-24T00:00:00Z")
        self.assertEqual(run.engine, "mock")
        self.assertEqual(run.source_domains, ("acme.ai",))
        self.assertEqual(run.to_dict()["recommendations"], ("Acme AI",))

    def test_m5_scores_zero_and_mixed_cases(self):
        self.assertEqual(score_visibility([], brand="Acme AI", brand_domain="acme.ai").mention_share, 0.0)
        adapter = MockEngineAdapter("mock", {"q": {"raw_answer": "Acme AI beats Globex", "citations": ["https://acme.ai/a", "https://globex.com/x"], "mentions": ["Acme AI"], "recommendations": []}})
        mixed = score_visibility([sample_engine(adapter, "q", region="US", language="en")], brand="Acme AI", brand_domain="acme.ai")
        self.assertEqual(mixed.mention_share, 1.0)
        self.assertEqual(mixed.citation_share, 1.0)
        self.assertEqual(mixed.source_diversity, 2)

    def test_m6_diagnosis_returns_type_evidence_and_next_step(self):
        adapter = MockEngineAdapter("mock", {"q": {"raw_answer": "Acme AI appears", "citations": ["https://other.com/a"], "mentions": [], "recommendations": []}})
        diagnosis = diagnose_citation_failure(sample_engine(adapter, "q", region="US", language="en"), brand="Acme AI", brand_domain="acme.ai", query_intent="buying_intent")
        self.assertIn("attribution", diagnosis.failure_types)
        self.assertTrue(diagnosis.next_step)
        self.assertTrue(diagnosis.evidence)

    def test_m7_task_brief_is_draft_only_and_traceable(self):
        query = build_query_space(PROFILE)[0]
        diagnosis = diagnose_citation_failure(sample_engine(MockEngineAdapter("mock", {}), query.query, region="US", language="en"), brand="Acme AI", brand_domain="acme.ai", query_intent=query.intent_type)
        brief = generate_task_brief(query, diagnosis, target_page="https://acme.ai")
        self.assertEqual(brief.query_cluster, query.cluster)
        self.assertIn("draft_only", brief.risk)
        self.assertTrue(brief.draft_content)
        self.assertTrue(brief.retest_plan)

    def test_m8_plan_prevents_holdout_leakage(self):
        records = build_query_space(PROFILE, target_engines=["mock"])
        plan = create_experiment_plan(records, holdout_ratio=0.25)
        self.assertTrue(set(plan.train_clusters).isdisjoint(plan.holdout_clusters))
        self.assertTrue(set(plan.validation_clusters).isdisjoint(plan.holdout_clusters))
        self.assertEqual(plan.retest_pairs[0][1:], ("mock", "en", "US"))

    def test_m9_report_contains_operational_sections(self):
        score = score_visibility([], brand="Acme AI", brand_domain="acme.ai")
        query = build_query_space(PROFILE)[0]
        diagnosis = diagnose_citation_failure(sample_engine(MockEngineAdapter("mock", {}), query.query, region="US", language="en"), brand="Acme AI", brand_domain="acme.ai", query_intent=query.intent_type)
        task = generate_task_brief(query, diagnosis, target_page="https://acme.ai")
        report = build_report_view(score, missing_queries=[query.query], competitor_mentions={"Globex": 2}, cited_sources=["other.com"], diagnoses=[diagnosis], tasks=[task])
        self.assertIn("mention_share", report.score)
        self.assertEqual(report.competitor_map["Globex"], 2)
        self.assertTrue(report.failures)
        self.assertTrue(report.recommended_actions)

if __name__ == "__main__":
    unittest.main()

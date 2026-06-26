import dataclasses
import unittest

from geo_agent.audit_runner import AuditRunner
from geo_agent.engine_sampling import MockEngineAdapter
from geo_agent.entity_profile import EntityProfile
from geo_agent.schema import AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord, EvidenceGraph


def make_artifacts():
    profile = EntityProfile(
        brand="Acme",
        aliases=("Acme",),
        domain="example.com",
        competitors=("Globex",),
        target_regions=("US",),
        target_languages=("en",),
        target_customer="teams",
        main_product="platform",
        category="software",
        business_goal="improve coverage",
    )
    fixtures = {
        "What is Acme for teams?": {
            "timestamp": "2026-06-24T00:00:00Z",
            "raw_answer": "Acme is a platform.",
            "citations": ["https://example.com/"],
            "mentions": ["Acme"],
            "recommendations": ["Acme"],
        },
        "Best software tools for teams in US": {
            "timestamp": "2026-06-24T00:01:00Z",
            "raw_answer": "Globex appears in lists.",
            "citations": ["https://globex.example/"],
            "mentions": ["Globex"],
            "recommendations": ["Globex"],
        },
    }
    pages = {"https://example.com/": "<html><head><title>Acme</title><link rel='canonical' href='https://example.com/'></head><body><h1>Acme</h1></body></html>"}
    return AuditRunner().run(profile, pages=pages, engine_adapter=MockEngineAdapter("recorded", fixtures), manual_urls=["https://example.com/"], max_queries=2)


class EvidenceGraphSchemaTests(unittest.TestCase):
    def test_required_records_are_frozen_dataclasses(self):
        records = [AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord]
        for record in records:
            self.assertTrue(dataclasses.is_dataclass(record), record.__name__)
            self.assertTrue(record.__dataclass_params__.frozen, record.__name__)

    def test_fixture_audit_builds_complete_evidence_graph(self):
        graph = make_artifacts().evidence_graph
        self.assertIsInstance(graph, EvidenceGraph)
        self.assertEqual(2, len(graph.prompts))
        self.assertEqual(2, len(graph.samples))
        self.assertTrue(graph.citations)
        self.assertTrue(graph.pages)
        self.assertTrue(graph.metrics)
        self.assertEqual(1, len(graph.retests))

    def test_metrics_diagnoses_and_tasks_link_to_source_ids(self):
        graph = make_artifacts().evidence_graph
        sample_ids = {item.sample_id for item in graph.samples}
        prompt_ids = {item.prompt_id for item in graph.prompts}
        citation_ids = {item.citation_id for item in graph.citations}
        diagnosis_ids = {item.diagnosis_id for item in graph.diagnoses}
        for metric in graph.metrics:
            self.assertTrue(set(metric.sample_ids) <= sample_ids)
            self.assertTrue(set(metric.prompt_ids) <= prompt_ids)
            self.assertTrue(set(metric.citation_ids) <= citation_ids)
        for diagnosis in graph.diagnoses:
            self.assertIn(diagnosis.sample_id, sample_ids)
            self.assertIn(diagnosis.prompt_id, prompt_ids)
        for task in graph.tasks:
            self.assertIn(task.sample_id, sample_ids)
            self.assertIn(task.prompt_id, prompt_ids)
            self.assertIn(task.diagnosis_id, diagnosis_ids)


if __name__ == "__main__":
    unittest.main()

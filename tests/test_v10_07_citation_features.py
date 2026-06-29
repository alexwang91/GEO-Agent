import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.query_space import QueryRecord
from geo_agent.schema import build_evidence_graph
from geo_agent.visibility_scoring import score_weighted_visibility


class V10CitationFeatureSchemaTests(unittest.TestCase):
    def test_each_citation_carries_feature_record_fields(self):
        run = EngineRun(
            engine="fixture_ai",
            query="Acme Watch",
            timestamp="2026-06-29T12:00:00+00:00",
            region="HU",
            language="en",
            raw_answer="Acme Watch is cited from Acme and recommended for fitness buyers.",
            citations=("http://owned.test/watch",),
            mentions=("Acme Watch",),
            recommendations=("Acme Watch",),
            source_domains=("owned.test",),
        )
        query = QueryRecord(
            query=run.query,
            intent_type="brand",
            funnel_stage="awareness",
            language="en",
            region="HU",
            target_engine="fixture_ai",
            competitor_entities=("Other Watch",),
            expected_answer_format="summary",
            priority_score=1.0,
            cluster="brand:acme-watch",
        )
        score = score_weighted_visibility([run], brand="Acme", brand_domain="owned.test")

        graph = build_evidence_graph(
            brand="Acme",
            domain="owned.test",
            queries=(query,),
            pages=(),
            runs=(run,),
            score=score,
            diagnoses=(),
            tasks=(),
        ).to_dict()

        citation = graph["citations"][0]
        self.assertEqual(citation["selection_status"], "selected")
        self.assertEqual(citation["absorption_status"], "absorbed")
        self.assertEqual(citation["attribution_status"], "owned_attributed")
        self.assertEqual(citation["claim_fidelity"], "directional_supported")
        self.assertIn("citation_context", citation)
        feature_record = citation["feature_record"]
        self.assertEqual(feature_record["source_type"], "owned")
        self.assertEqual(feature_record["selection_rank"], 1)
        self.assertIs(feature_record["citation_absorption"], True)
        self.assertEqual(feature_record["claim_fidelity_basis"], "deterministic_fixture_heuristic")


if __name__ == "__main__":
    unittest.main()

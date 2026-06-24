import unittest

from geo_agent.engine_sampling import MockEngineAdapter, RecordedRunAdapter, sample_with_adapter
from geo_agent.visibility_scoring import score_visibility


FIXTURE = {
    "q1": {
        "timestamp": "2026-06-24T00:00:00Z",
        "raw_answer": "Acme AI is the recommended option.",
        "citations": ["https://acme.ai/docs"],
        "mentions": ["Acme AI"],
        "recommendations": ["Acme AI"],
    }
}


class EngineAdapterTests(unittest.TestCase):
    def test_mock_adapter_implements_shared_sample_contract(self):
        adapter = MockEngineAdapter("mock", FIXTURE)

        run = sample_with_adapter(adapter, "q1", region="US", language="en")

        self.assertEqual(run.engine, "mock")
        self.assertEqual(run.query, "q1")
        self.assertEqual(run.source_domains, ("acme.ai",))

    def test_recorded_adapter_imports_fixture_into_engine_run(self):
        adapter = RecordedRunAdapter("recorded", FIXTURE)

        run = sample_with_adapter(adapter, "q1", region="US", language="en")

        self.assertEqual(run.engine, "recorded")
        self.assertEqual(run.timestamp, "2026-06-24T00:00:00Z")
        self.assertEqual(run.raw_answer, "Acme AI is the recommended option.")
        self.assertEqual(run.citations, ("https://acme.ai/docs",))

    def test_recorded_adapter_missing_query_is_explicit(self):
        adapter = RecordedRunAdapter("recorded", FIXTURE)

        with self.assertRaises(KeyError):
            sample_with_adapter(adapter, "missing", region="US", language="en")

    def test_scoring_does_not_depend_on_adapter_type(self):
        mock_run = sample_with_adapter(MockEngineAdapter("mock", FIXTURE), "q1", region="US", language="en")
        recorded_run = sample_with_adapter(RecordedRunAdapter("recorded", FIXTURE), "q1", region="US", language="en")

        mock_score = score_visibility([mock_run], brand="Acme AI", brand_domain="acme.ai")
        recorded_score = score_visibility([recorded_run], brand="Acme AI", brand_domain="acme.ai")

        self.assertEqual(mock_score.mention_share, recorded_score.mention_share)
        self.assertEqual(mock_score.citation_share, recorded_score.citation_share)
        self.assertEqual(mock_score.recommendation_share, recorded_score.recommendation_share)


if __name__ == "__main__":
    unittest.main()

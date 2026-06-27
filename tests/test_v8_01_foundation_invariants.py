import unittest

from geo_agent.citation_absorption import calculate_citation_absorption_from_urls
from geo_agent.engine_sampling import MockEngineAdapter, RecordedRunAdapter, run_from_payload
from geo_agent.visibility_scoring import score_weighted_visibility


class V801FoundationInvariantTests(unittest.TestCase):
    def test_empty_visibility_input_returns_zero_components(self):
        score = score_weighted_visibility([], brand="Acme", brand_domain="acme.com")

        self.assertEqual(0.0, score.aggregate_score)
        self.assertEqual(0.0, score.components.mention_share)
        self.assertEqual(0.0, score.components.citation_share)
        self.assertEqual(0.0, score.components.recommendation_share)
        self.assertEqual(0.0, score.components.query_coverage)

    def test_visibility_scoring_keeps_competitor_only_penalty_bounded(self):
        run = run_from_payload(
            {
                "raw_answer": "Contoso is the only relevant recommendation.",
                "citations": ["https://contoso.com/pricing"],
                "mentions": ["Contoso"],
                "recommendations": ["Contoso"],
                "timestamp": "2026-06-27T00:00:00Z",
            },
            engine="fixture",
            query="best tools",
            region="US",
            language="en",
        )

        score = score_weighted_visibility([run], brand="Acme", brand_domain="acme.com", competitors=("Contoso",))

        self.assertGreaterEqual(score.aggregate_score, 0.0)
        self.assertEqual(1.0, score.components.competitor_only_share)
        self.assertEqual(0.0, score.components.mention_share)

    def test_citation_absorption_empty_urls_is_no_sample(self):
        metric = calculate_citation_absorption_from_urls([], owned_domains=("acme.com",))

        self.assertEqual(0.0, metric.score)
        self.assertEqual(0, metric.citation_count)
        self.assertEqual("no_sample", metric.directionality)
        self.assertIn("No citations were available.", metric.notes)

    def test_citation_absorption_handles_invalid_urls_as_unknown(self):
        metric = calculate_citation_absorption_from_urls(["not a url"], owned_domains=("acme.com",))

        self.assertEqual(1, metric.citation_count)
        self.assertEqual({"unknown": 1}, metric.source_mix)
        self.assertEqual("directional_low_sample", metric.directionality)

    def test_recorded_adapter_raises_for_missing_query(self):
        adapter = RecordedRunAdapter("fixture", {})

        with self.assertRaises(KeyError):
            adapter.sample("missing", region="US", language="en", timestamp="2026-06-27T00:00:00Z")

    def test_mock_adapter_empty_query_path_is_safe(self):
        adapter = MockEngineAdapter("fixture", {})
        run = adapter.sample("unknown", region="US", language="en", timestamp="2026-06-27T00:00:00Z")

        self.assertEqual("", run.raw_answer)
        self.assertEqual((), run.citations)
        self.assertEqual((), run.mentions)
        self.assertEqual((), run.recommendations)


if __name__ == "__main__":
    unittest.main()

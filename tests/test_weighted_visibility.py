import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.visibility_scoring import compute_visibility_components, score_weighted_visibility


def run(answer, *, domains=(), mentions=(), recommendations=()):
    return EngineRun(
        engine="mock",
        query="q",
        timestamp="2026-06-24T00:00:00Z",
        region="US",
        language="en",
        raw_answer=answer,
        citations=tuple(f"https://{domain}/a" for domain in domains),
        mentions=tuple(mentions),
        recommendations=tuple(recommendations),
        source_domains=tuple(domains),
    )


class WeightedVisibilityTests(unittest.TestCase):
    def test_empty_answer_has_zero_components(self):
        components = compute_visibility_components([], brand="Acme AI", brand_domain="acme.ai")

        self.assertEqual(components.mention_share, 0.0)
        self.assertEqual(components.citation_share, 0.0)
        self.assertEqual(components.query_coverage, 0.0)

    def test_brand_mention_without_citation_is_visible_but_uncited(self):
        components = compute_visibility_components([run("Acme AI appears")], brand="Acme AI", brand_domain="acme.ai")

        self.assertEqual(components.mention_share, 1.0)
        self.assertEqual(components.citation_share, 0.0)
        self.assertEqual(components.recommendation_share, 0.0)

    def test_citation_without_recommendation_is_separate_metric(self):
        components = compute_visibility_components([run("Acme AI appears", domains=("acme.ai",))], brand="Acme AI", brand_domain="acme.ai")

        self.assertEqual(components.citation_share, 1.0)
        self.assertEqual(components.recommendation_share, 0.0)
        self.assertGreater(components.source_diversity_score, 0.0)

    def test_competitor_only_answer_is_penalized_in_weighted_score(self):
        brand = run("Acme AI appears", domains=("acme.ai",), mentions=("Acme AI",), recommendations=("Acme AI",))
        competitor = run("Globex is the best option", domains=("globex.com",))

        score = score_weighted_visibility([brand, competitor], brand="Acme AI", brand_domain="acme.ai", competitors=("Globex",))

        self.assertEqual(score.components.competitor_only_share, 0.5)
        self.assertLess(score.aggregate_score, 1.0)

    def test_weights_are_configurable_and_deterministic(self):
        runs = [run("Acme AI appears", domains=("acme.ai",), recommendations=("Acme AI",))]
        score = score_weighted_visibility(
            runs,
            brand="Acme AI",
            brand_domain="acme.ai",
            weights={"mention_share": 1.0, "citation_share": 0.0},
        )

        self.assertEqual(score.aggregate_score, 1.0)
        self.assertEqual(score.weights, {"mention_share": 1.0, "citation_share": 0.0})


if __name__ == "__main__":
    unittest.main()

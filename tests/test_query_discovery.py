import unittest

from geo_agent.entity_profile import EntityProfile
from geo_agent.query_discovery import DEFAULT_CLUSTERS, DEFAULT_PERSPECTIVES, dedupe_queries, discover_queries_no_llm, rank_queries


def profile():
    return EntityProfile(
        brand="Acme AI",
        aliases=("Acme",),
        domain="acme.ai",
        competitors=("Globex",),
        target_regions=("US",),
        target_languages=("en",),
        target_customer="marketing teams",
        main_product="AI visibility platform",
        category="GEO software",
        business_goal="improve AI search visibility",
    )


class QueryDiscoveryTests(unittest.TestCase):
    def test_default_no_llm_mode_yields_80_queries(self):
        result = discover_queries_no_llm(profile(), target_engine="manual")
        self.assertEqual("no_llm_fixture", result.mode)
        self.assertEqual(80, len(result.queries))
        self.assertEqual({cluster.cluster_id for cluster in DEFAULT_CLUSTERS}, {query.cluster_id for query in result.queries})
        self.assertEqual({perspective.perspective_id for perspective in DEFAULT_PERSPECTIVES}, {query.perspective_id for query in result.queries})

    def test_discovered_queries_have_ranking_metadata(self):
        result = discover_queries_no_llm(profile(), target_engine="manual")
        first = result.queries[0]
        self.assertEqual("manual", first.query.target_engine)
        self.assertTrue(first.seed_source_ids)
        payload = first.to_dict()
        self.assertIn("cluster_id", payload)
        self.assertIn("perspective_id", payload)
        self.assertIn("business_value_score", payload)
        self.assertIn("citation_likelihood_score", payload)
        self.assertIn("priority_score", payload)

    def test_ranker_is_deterministic_and_assigns_rank(self):
        result = discover_queries_no_llm(profile())
        ranked_a = rank_queries(result.queries)
        ranked_b = rank_queries(result.queries)
        self.assertEqual([item.discovered_query.query.query for item in ranked_a], [item.discovered_query.query.query for item in ranked_b])
        self.assertEqual(list(range(1, len(ranked_a) + 1)), [item.rank for item in ranked_a])
        self.assertGreaterEqual(ranked_a[0].priority_score, ranked_a[-1].priority_score)

    def test_dedupe_removes_repeated_query_text(self):
        result = discover_queries_no_llm(profile(), limit=3)
        duplicated = result.queries + (result.queries[0],)
        self.assertEqual(3, len(dedupe_queries(duplicated)))


if __name__ == "__main__":
    unittest.main()

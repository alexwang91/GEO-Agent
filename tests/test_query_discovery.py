import unittest

from geo_agent.entity_profile import EntityProfile
from geo_agent.query_discovery import DEFAULT_CLUSTERS, DEFAULT_PERSPECTIVES, discover_queries_no_llm


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
    def test_no_llm_mode_covers_all_clusters_and_perspectives(self):
        result = discover_queries_no_llm(profile(), target_engine="manual")
        self.assertEqual("no_llm_fixture", result.mode)
        self.assertEqual(len(DEFAULT_CLUSTERS) * len(DEFAULT_PERSPECTIVES), len(result.queries))
        self.assertEqual({cluster.cluster_id for cluster in DEFAULT_CLUSTERS}, {query.cluster_id for query in result.queries})
        self.assertEqual({perspective.perspective_id for perspective in DEFAULT_PERSPECTIVES}, {query.perspective_id for query in result.queries})

    def test_discovered_queries_are_existing_query_records_with_metadata(self):
        result = discover_queries_no_llm(profile(), target_engine="manual")
        first = result.queries[0]
        self.assertEqual("manual", first.query.target_engine)
        self.assertEqual("US", first.query.region)
        self.assertEqual("en", first.query.language)
        self.assertTrue(first.query.query)
        self.assertTrue(first.query.cluster)
        self.assertTrue(first.seed_source_ids)
        payload = first.to_dict()
        self.assertIn("cluster_id", payload)
        self.assertIn("perspective_id", payload)
        self.assertIn("seed_source_ids", payload)

    def test_limit_is_deterministic(self):
        result_a = discover_queries_no_llm(profile(), limit=5)
        result_b = discover_queries_no_llm(profile(), limit=5)
        self.assertEqual([query.query.query for query in result_a.queries], [query.query.query for query in result_b.queries])
        self.assertEqual(5, len(result_a.queries))


if __name__ == "__main__":
    unittest.main()

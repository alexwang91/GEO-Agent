import unittest

from geo_agent import INTENT_TYPES, build_query_space, validate_entity_profile


PROFILE_PAYLOAD = {
    "brand": "Acme AI",
    "aliases": ["Acme"],
    "domain": "acme.ai",
    "competitors": ["Globex AI", "Initech Search"],
    "target_regions": ["US"],
    "target_languages": ["en"],
    "target_customer": "B2B marketing teams",
    "main_product": "AI search visibility platform",
    "category": "Generative Engine Optimization",
    "business_goal": "increase qualified demo requests",
}


class QuerySpaceTests(unittest.TestCase):
    def test_builds_one_record_per_supported_intent_for_engine_region_language(self):
        profile = validate_entity_profile(PROFILE_PAYLOAD)
        records = build_query_space(profile, target_engines=["chatgpt_search"])

        self.assertEqual(len(records), len(INTENT_TYPES))
        self.assertEqual([record.intent_type for record in records], list(INTENT_TYPES))
        self.assertTrue(all(record.region == "US" for record in records))
        self.assertTrue(all(record.language == "en" for record in records))
        self.assertTrue(all(record.target_engine == "chatgpt_search" for record in records))

    def test_records_include_required_sampling_and_clustering_metadata(self):
        profile = validate_entity_profile(PROFILE_PAYLOAD)
        record = build_query_space(profile, target_engines=["perplexity"])[2]

        self.assertEqual(record.intent_type, "comparison")
        self.assertEqual(record.funnel_stage, "consideration")
        self.assertEqual(record.expected_answer_format, "comparison_table")
        self.assertEqual(record.competitor_entities, ("Globex AI", "Initech Search"))
        self.assertEqual(record.priority_score, 0.92)
        self.assertEqual(record.cluster, "comparison:en:US:perplexity")
        self.assertIn("Compare Acme AI vs Globex AI, and Initech Search", record.query)

    def test_multiple_engines_regions_and_languages_are_deterministic(self):
        payload = dict(PROFILE_PAYLOAD)
        payload["target_regions"] = ["US", "GB"]
        payload["target_languages"] = ["en", "fr"]
        profile = validate_entity_profile(payload)

        records = build_query_space(profile, target_engines=["chatgpt_search", "gemini"])

        self.assertEqual(len(records), len(INTENT_TYPES) * 2 * 2 * 2)
        self.assertEqual(records[0].cluster, "brand:en:US:chatgpt_search")
        self.assertEqual(records[-1].cluster, "alternatives:fr:GB:gemini")

    def test_max_queries_limits_output_without_changing_order(self):
        profile = validate_entity_profile(PROFILE_PAYLOAD)
        records = build_query_space(profile, target_engines=["chatgpt_search"], max_queries=3)

        self.assertEqual([record.intent_type for record in records], ["brand", "category", "comparison"])

    def test_empty_target_engines_are_rejected(self):
        profile = validate_entity_profile(PROFILE_PAYLOAD)

        with self.assertRaises(ValueError):
            build_query_space(profile, target_engines=[" "])


if __name__ == "__main__":
    unittest.main()

import unittest

from geo_agent.engine_sampling import run_from_payload
from geo_agent.entity_resolution import extract_urls, has_entity
from geo_agent.visibility_scoring import score_weighted_visibility


class EntityResolutionEvalTests(unittest.TestCase):
    def test_multi_word_brand_and_alias_match(self):
        text = "Acme Cloud is cited by users; ACM is not the same as acmeology."
        self.assertTrue(has_entity(text, "Acme Cloud"))
        self.assertTrue(has_entity(text, "ACM"))
        self.assertFalse(has_entity(text, "Acmeology"))

    def test_diacritics_and_boundaries(self):
        self.assertTrue(has_entity("Café Nova is listed.", "Café Nova"))
        self.assertFalse(has_entity("Cafenova is listed.", "Café Nova"))

    def test_url_extraction_from_raw_answer(self):
        urls = extract_urls("Sources: https://acme.com/docs and example.org/path.")
        self.assertIn("https://acme.com/docs", urls)
        self.assertIn("https://example.org/path", urls)

    def test_run_payload_falls_back_to_mentions_and_citations(self):
        run = run_from_payload(
            {"raw_answer": "Acme Cloud appears at https://acme.com/docs", "brand": "Acme Cloud"},
            engine="fixture",
            query="q",
            region="US",
            language="en",
            timestamp="2026-06-27T00:00:00Z",
        )
        self.assertEqual(("Acme Cloud",), run.mentions)
        self.assertEqual(("acme.com",), run.source_domains)

    def test_visibility_avoids_substring_false_positive(self):
        run = run_from_payload(
            {"raw_answer": "The word acmeology should not count.", "citations": []},
            engine="fixture",
            query="q",
            region="US",
            language="en",
            timestamp="2026-06-27T00:00:00Z",
        )
        score = score_weighted_visibility([run], brand="Acme", brand_domain="acme.com")
        self.assertEqual(0.0, score.components.mention_share)


if __name__ == "__main__":
    unittest.main()

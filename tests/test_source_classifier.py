import unittest

from geo_agent.source_classifier import classify_source, classify_sources


class SourceClassifierTests(unittest.TestCase):
    def test_owned_and_competitor_domains_win_first(self):
        owned = classify_source("https://docs.acme.ai/guide", owned_domains=("acme.ai",))
        competitor = classify_source("https://help.globex.com/a", competitor_domains=("globex.com",))
        self.assertEqual("owned", owned.source_class)
        self.assertEqual("competitor", competitor.source_class)

    def test_classifies_known_source_categories(self):
        cases = {
            "https://www.g2.com/products/acme/reviews": "review",
            "https://www.reddit.com/r/seo/": "community",
            "https://www.crunchbase.com/organization/acme": "directory",
            "https://apps.shopify.com/acme": "marketplace",
            "https://agency.gov/report": "gov",
            "https://www.harvard.edu/research": "academic",
            "https://docs.vendor.com/api": "docs",
            "https://techcrunch.com/story": "earned",
            "https://example.net/page": "unknown",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertEqual(expected, classify_source(url).source_class)

    def test_batch_classification_preserves_order(self):
        values = classify_sources(["https://reddit.com/r/a", "https://example.net"])
        self.assertEqual(["community", "unknown"], [item.source_class for item in values])
        self.assertEqual("reddit.com", values[0].domain)


if __name__ == "__main__":
    unittest.main()

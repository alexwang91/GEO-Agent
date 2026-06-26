import unittest

from geo_agent.citation_absorption import calculate_citation_absorption, calculate_citation_absorption_from_urls
from geo_agent.source_classifier import ClassifiedSource


class CitationAbsorptionTests(unittest.TestCase):
    def test_weighted_score_and_mix_from_classified_sources(self):
        metric = calculate_citation_absorption((
            ClassifiedSource("https://acme.ai", "acme.ai", "owned", "owned"),
            ClassifiedSource("https://g2.com", "g2.com", "review", "review"),
            ClassifiedSource("https://competitor.com", "competitor.com", "competitor", "competitor"),
        ))
        self.assertEqual(3, metric.citation_count)
        self.assertEqual({"owned": 1, "review": 1, "competitor": 1}, metric.source_mix)
        self.assertEqual(1.85, metric.weighted_citation_count)
        self.assertEqual(round(1.85 / 3, 4), metric.score)
        self.assertEqual("directional", metric.directionality)
        self.assertIn("Competitor citations do not add absorption credit.", metric.notes)

    def test_low_sample_and_empty_cases_are_directional(self):
        empty = calculate_citation_absorption(())
        self.assertEqual("no_sample", empty.directionality)
        low = calculate_citation_absorption((ClassifiedSource("https://example.net", "example.net", "unknown", "unknown"),))
        self.assertEqual("directional_low_sample", low.directionality)
        self.assertIn("Unknown sources receive limited absorption credit.", low.notes)

    def test_metric_from_urls_uses_source_classifier(self):
        metric = calculate_citation_absorption_from_urls(
            ["https://docs.acme.ai/guide", "https://techcrunch.com/story", "https://globex.com"],
            owned_domains=("acme.ai",),
            competitor_domains=("globex.com",),
        )
        self.assertEqual({"owned": 1, "earned": 1, "competitor": 1}, metric.source_mix)
        self.assertEqual(round((1.0 + 0.95 + 0.0) / 3, 4), metric.score)


if __name__ == "__main__":
    unittest.main()

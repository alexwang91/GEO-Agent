import unittest

from geo_agent.page_snapshot_extractor import PageSnapshotExtractionError, extract_page_snapshot

HTML = """<html><head><title>Acme AI</title><link rel='canonical' href='/canonical'><meta name='description' content='AI visibility platform'><script type='application/ld+json'>{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is Acme?","acceptedAnswer":{"@type":"Answer","text":"A GEO platform."}}]}</script></head><body><h1>Acme AI</h1><h2>Visibility</h2><p>First paragraph.</p><table><caption>Plans</caption><tr><th>Name</th></tr><tr><td>Starter</td></tr></table></body></html>"""


class PageSnapshotExtractorTests(unittest.TestCase):
    def test_extracts_sections_and_hashes(self):
        snapshot = extract_page_snapshot("https://acme.ai/page", HTML)
        self.assertEqual("https://acme.ai/canonical", snapshot.canonical_url)
        self.assertEqual("Acme AI", snapshot.title)
        self.assertEqual("AI visibility platform", snapshot.meta["description"])
        self.assertEqual(("Acme AI", "Visibility"), snapshot.headings)
        self.assertIn("First paragraph.", snapshot.paragraphs)
        self.assertEqual("Plans", snapshot.tables[0].caption)
        self.assertEqual("What is Acme?", snapshot.faqs[0].question)
        self.assertIn("FAQPage", snapshot.json_ld_types)
        self.assertEqual(64, len(snapshot.html_sha256))
        self.assertEqual(64, len(snapshot.text_sha256))

    def test_digest_is_deterministic(self):
        first = extract_page_snapshot("https://acme.ai/page", HTML)
        second = extract_page_snapshot("https://acme.ai/page", HTML)
        self.assertEqual(first.html_sha256, second.html_sha256)
        self.assertEqual(first.text_sha256, second.text_sha256)

    def test_invalid_input_is_rejected(self):
        with self.assertRaises(PageSnapshotExtractionError):
            extract_page_snapshot("bad-url", HTML)
        with self.assertRaises(PageSnapshotExtractionError):
            extract_page_snapshot("https://acme.ai/page", "plain text")

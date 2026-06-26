import unittest

from geo_agent.citation_parser import CitationParserError, citation_domain, normalize_citation_url, parse_citations


class CitationParserTests(unittest.TestCase):
    def test_normalizes_urls_and_removes_tracking(self):
        url = normalize_citation_url("HTTP://WWW.Example.com/path/?utm_source=x&b=2&a=1#section")
        self.assertEqual("https://www.example.com/path?a=1&b=2", url)

    def test_domain_extraction_removes_www(self):
        self.assertEqual("example.com", citation_domain("https://www.example.com/path"))

    def test_parse_citations_dedupes_and_preserves_positions(self):
        citations = parse_citations((
            "https://example.com/a?utm_campaign=x",
            "https://example.com/a/",
            "https://docs.example.com/guide",
        ), prefix="sample:1:citation")
        self.assertEqual(2, len(citations))
        self.assertEqual("sample:1:citation:1", citations[0].citation_id)
        self.assertEqual(1, citations[0].position)
        self.assertEqual(2, citations[1].position)
        self.assertEqual("docs.example.com", citations[1].domain)

    def test_invalid_url_is_rejected(self):
        with self.assertRaises(CitationParserError):
            normalize_citation_url("not-a-url")


if __name__ == "__main__":
    unittest.main()

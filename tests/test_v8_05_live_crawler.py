import unittest

from geo_agent.crawl_provider_v2 import CrawlerProviderV2Request, LiveCrawlerProviderV2
from geo_agent.provider_access import ProviderAccessError


class FakeFetchClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, *, timeout_seconds):
        self.calls.append((url, timeout_seconds))
        return self.responses[url]


class LiveCrawlerSeamTests(unittest.TestCase):
    def test_live_provider_requires_explicit_opt_in(self):
        provider = LiveCrawlerProviderV2(FakeFetchClient({}))
        request = CrawlerProviderV2Request(provider_id="live_crawler_v2", manual_urls=("https://example.com",))
        with self.assertRaises(ProviderAccessError):
            provider.crawl(request)

    def test_live_provider_uses_fake_client(self):
        html = "<html><head><title>Acme</title></head><body>Evidence page</body></html>"
        client = FakeFetchClient({"https://example.com": (200, html)})
        provider = LiveCrawlerProviderV2(client)
        request = CrawlerProviderV2Request(provider_id="live_crawler_v2", manual_urls=("https://example.com",), allow_live_fetch=True)
        result = provider.crawl(request)
        self.assertEqual(1, len(result.pages))
        self.assertEqual("live", result.page_results[0].source)

    def test_live_provider_records_http_errors(self):
        client = FakeFetchClient({"https://example.com": (500, "")})
        provider = LiveCrawlerProviderV2(client)
        request = CrawlerProviderV2Request(provider_id="live_crawler_v2", manual_urls=("https://example.com",), allow_live_fetch=True)
        result = provider.crawl(request)
        self.assertEqual(0, len(result.pages))
        self.assertIn("HTTP 500", result.page_results[0].message)


if __name__ == "__main__":
    unittest.main()

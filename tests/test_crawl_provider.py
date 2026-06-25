import unittest

from geo_agent.crawl_provider import (
    CrawlProviderRequest,
    StaticCrawlerProvider,
    pages_from_crawl_result,
)
from geo_agent.evidence_store import EvidenceStore
from geo_agent.provider_access import ProviderAccessError, default_provider_registry


HOME = "https://acme.ai/"
ABOUT = "https://acme.ai/about"
SITEMAP = "https://acme.ai/sitemap.xml"


class CrawlProviderTests(unittest.TestCase):
    def test_static_crawler_success_feeds_page_inventory_records(self):
        provider = StaticCrawlerProvider(
            {
                HOME: "<html><head><title>Acme</title><link rel='canonical' href='https://acme.ai/'></head><body><h1>Acme AI</h1><p>Visibility platform for AI search.</p></body></html>",
                ABOUT: "<html><head><title>About Acme</title></head><body><h1>About</h1><p>Acme helps marketing teams.</p></body></html>",
            },
            sitemaps={
                SITEMAP: "<urlset><url><loc>https://acme.ai/</loc></url><url><loc>https://acme.ai/about</loc></url></urlset>",
            },
        )
        request = CrawlProviderRequest(provider_id="static_crawler", sitemap_urls=(SITEMAP,), metadata={"run": "fixture"})

        result = provider.crawl(request)

        self.assertEqual(result.provider_id, "static_crawler")
        self.assertEqual(result.errors, ())
        self.assertEqual(len(result.pages), 2)
        self.assertEqual(result.pages[0].canonical_url, HOME)
        self.assertEqual(result.pages[0].title, "Acme")
        self.assertIn("Visibility platform", result.pages[0].content_chunks[0])
        self.assertEqual(result.metadata, {"mode": "static", "source": "fixture"})

    def test_static_crawler_failure_returns_error_without_network(self):
        provider = StaticCrawlerProvider({})
        request = CrawlProviderRequest(provider_id="static_crawler", manual_urls=(HOME,))

        result = provider.crawl(request)

        self.assertEqual(result.pages, ())
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].error_type, "page_inventory_error")
        self.assertIn("No fixture for URL", result.errors[0].message)

    def test_unsupported_provider_raises_provider_access_error(self):
        provider = StaticCrawlerProvider({HOME: "<html><body><h1>Acme</h1></body></html>"})
        request = CrawlProviderRequest(provider_id="firecrawl", manual_urls=(HOME,))

        with self.assertRaises(ProviderAccessError):
            provider.crawl(request)

    def test_request_validation_rejects_invalid_or_empty_inputs(self):
        with self.assertRaises(ProviderAccessError):
            CrawlProviderRequest(provider_id="static_crawler")
        with self.assertRaises(ProviderAccessError):
            CrawlProviderRequest(provider_id="static_crawler", manual_urls=("not-a-url",))
        with self.assertRaises(ProviderAccessError):
            CrawlProviderRequest(provider_id="static_crawler", manual_urls=(HOME,), chunk_size=0)

    def test_result_serialization_and_redaction_shape(self):
        provider = StaticCrawlerProvider({HOME: "<html><body><h1>Acme</h1><p>Public page.</p></body></html>"})
        result = provider.crawl(CrawlProviderRequest(provider_id="static_crawler", manual_urls=(HOME,)))
        payload = result.to_dict()

        self.assertEqual(payload["provider_id"], "static_crawler")
        self.assertEqual(payload["errors"], [])
        self.assertEqual(payload["metadata"], {"mode": "static", "source": "fixture"})
        self.assertNotIn("api_key", str(payload).lower())
        self.assertNotIn("secret", str(payload).lower())

    def test_crawl_result_feeds_existing_evidence_store(self):
        provider = StaticCrawlerProvider({HOME: "<html><body><h1>Acme</h1><p>Stored page.</p></body></html>"})
        result = provider.crawl(CrawlProviderRequest(provider_id="static_crawler", manual_urls=(HOME,)))

        with EvidenceStore() as store:
            ids = store.save_page_records(pages_from_crawl_result(result))
            stored = store.list_page_records()

        self.assertEqual(len(ids), 1)
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0].url, HOME)
        self.assertEqual(stored[0].h1, "Acme")

    def test_live_crawler_registry_entries_remain_planned(self):
        registry = default_provider_registry()

        self.assertEqual(registry.get("crawl4ai").implementation_status, "planned")
        self.assertEqual(registry.get("firecrawl").implementation_status, "planned")


if __name__ == "__main__":
    unittest.main()
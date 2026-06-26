import unittest

from geo_agent.crawl_provider_v2 import CrawlerProviderV2Request, StaticCrawlerProviderV2
from geo_agent.provider_access import ProviderAccessError


SITEMAP = """<?xml version='1.0' encoding='UTF-8'?>
<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
  <url><loc>https://acme.ai/</loc></url>
  <url><loc>https://acme.ai/rendered</loc></url>
  <url><loc>https://acme.ai/missing</loc></url>
</urlset>
"""


class CrawlerProviderV2Tests(unittest.TestCase):
    def test_sitemap_manual_and_rendered_fallback_have_page_statuses(self):
        provider = StaticCrawlerProviderV2(
            {
                "https://acme.ai/": "<html><head><title>Home</title><link rel='canonical' href='https://acme.ai/'></head><body><h1>Home</h1></body></html>",
                "https://acme.ai/manual": "<html><body><h1>Manual</h1></body></html>",
            },
            sitemaps={"https://acme.ai/sitemap.xml": SITEMAP},
            rendered_pages={"https://acme.ai/rendered": "<html><body><h1>Rendered</h1></body></html>"},
        )
        result = provider.crawl(
            CrawlerProviderV2Request(
                "static_crawler_v2",
                manual_urls=("https://acme.ai/manual",),
                sitemap_urls=("https://acme.ai/sitemap.xml",),
            )
        )
        statuses = {item.url: item.status for item in result.page_results}
        sources = {item.url: item.source for item in result.page_results}
        self.assertEqual("crawled", statuses["https://acme.ai/"])
        self.assertEqual("crawled", statuses["https://acme.ai/manual"])
        self.assertEqual("rendered_fallback", statuses["https://acme.ai/rendered"])
        self.assertEqual("failed", statuses["https://acme.ai/missing"])
        self.assertEqual("sitemap", sources["https://acme.ai/"])
        self.assertEqual("manual", sources["https://acme.ai/manual"])
        self.assertEqual(3, len(result.pages))

    def test_request_accepts_rendered_only_input(self):
        provider = StaticCrawlerProviderV2({}, rendered_pages={"https://acme.ai/app": "<html><body><h1>App</h1></body></html>"})
        result = provider.crawl(CrawlerProviderV2Request("static_crawler_v2", rendered_html={"https://acme.ai/app": "<html><body><h1>App</h1></body></html>"}))
        self.assertEqual("rendered_fallback", result.page_results[0].status)
        self.assertEqual("rendered_fallback", result.page_results[0].source)

    def test_invalid_url_is_rejected(self):
        with self.assertRaises(ProviderAccessError):
            CrawlerProviderV2Request("static_crawler_v2", manual_urls=("ftp://bad",))


if __name__ == "__main__":
    unittest.main()

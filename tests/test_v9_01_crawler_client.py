import unittest
from urllib.error import URLError

from geo_agent.crawl_provider_v2 import CrawlerProviderV2Request, LiveCrawlerProviderV2
from geo_agent.http_fetch_client import FetchClientError, HttpFetchConfig, UrlLibFetchClient
from geo_agent.page_inventory import UrlLibPageFetcher


class Headers:
    def get_content_charset(self):
        return "utf-8"

    def get_content_type(self):
        return "text/html"


class Response:
    def __init__(self, status, body):
        self.status = status
        self.body = body.encode("utf-8")
        self.headers = Headers()

    def read(self):
        return self.body

    def getcode(self):
        return self.status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None


class Opener:
    def __init__(self, routes):
        self.routes = {url: list(values) for url, values in routes.items()}
        self.calls = []

    def __call__(self, request, timeout_seconds):
        url = request.full_url
        self.calls.append((url, timeout_seconds))
        value = self.routes[url].pop(0)
        if isinstance(value, Exception):
            raise value
        status, body = value
        return Response(status, body)


class ErrorClient:
    def get(self, url, *, timeout_seconds):
        raise FetchClientError("denied")


class OkClient:
    def get(self, url, *, timeout_seconds):
        return 200, "<html><head><title>Acme</title></head><body>Evidence page</body></html>"


class V901CrawlerClientTests(unittest.TestCase):
    def test_robots_rules_are_checked_before_page_fetch(self):
        opener = Opener(
            {
                "https://example.com/robots.txt": [(200, "User-agent: *\nDisallow: /private\n")],
                "https://example.com/private/page": [(200, "<html>no</html>")],
            }
        )
        client = UrlLibFetchClient(HttpFetchConfig(retries=0), opener=opener)
        with self.assertRaises(FetchClientError):
            client.get("https://example.com/private/page", timeout_seconds=2.0)
        self.assertEqual([("https://example.com/robots.txt", 2.0)], opener.calls)

    def test_transient_fetch_errors_are_retried(self):
        opener = Opener(
            {
                "https://example.com/page": [
                    URLError("temporary"),
                    (200, "<html><body>ok</body></html>"),
                ]
            }
        )
        config = HttpFetchConfig(retries=1, respect_robots=False)
        status, body = UrlLibFetchClient(config, opener=opener).get("https://example.com/page", timeout_seconds=3.0)
        self.assertEqual(200, status)
        self.assertIn("ok", body)
        self.assertEqual(2, len(opener.calls))

    def test_provider_records_client_errors(self):
        provider = LiveCrawlerProviderV2(ErrorClient())
        request = CrawlerProviderV2Request(
            provider_id="live_crawler_v2",
            manual_urls=("https://example.com/page",),
            allow_live_fetch=True,
        )
        result = provider.crawl(request)
        self.assertEqual(0, len(result.pages))
        self.assertEqual("failed", result.page_results[0].status)
        self.assertIn("denied", result.page_results[0].message)

    def test_page_inventory_fetcher_uses_shared_client(self):
        response = UrlLibPageFetcher(fetch_client=OkClient()).fetch("https://example.com/page")
        self.assertEqual("https://example.com/page", response.url)
        self.assertIn("Evidence page", response.body)


if __name__ == "__main__":
    unittest.main()

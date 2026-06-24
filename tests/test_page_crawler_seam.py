import unittest

from geo_agent.page_inventory import PageInventoryError, StaticPageFetcher, crawl_inventory


OPEN = chr(60)
CLOSE = chr(62)


def tag(name, body="", attrs=""):
    space = f" {attrs}" if attrs else ""
    return f"{OPEN}{name}{space}{CLOSE}{body}{OPEN}/{name}{CLOSE}"


def page(title, canonical):
    head = tag("title", title) + f"{OPEN}link rel='canonical' href='{canonical}'{CLOSE}"
    body = tag("h1", title) + tag("p", f"{title} body text")
    return tag("html", tag("head", head) + tag("body", body))


def urlset(*urls):
    return tag("urlset", "".join(tag("url", tag("loc", url)) for url in urls))


class PageCrawlerSeamTests(unittest.TestCase):
    def test_fetcher_discovers_urls_from_sitemap_fixture(self):
        fetcher = StaticPageFetcher({
            "https://acme.ai/sitemap.xml": urlset("https://acme.ai/a", "https://acme.ai/b"),
            "https://acme.ai/a": page("A", "https://acme.ai/a"),
            "https://acme.ai/b": page("B", "https://acme.ai/b"),
        })

        records = crawl_inventory(fetcher, sitemap_urls=["https://acme.ai/sitemap.xml"])

        self.assertEqual([record.url for record in records], ["https://acme.ai/a", "https://acme.ai/b"])
        self.assertEqual([record.title for record in records], ["A", "B"])

    def test_manual_urls_work_without_network(self):
        fetcher = StaticPageFetcher({"https://acme.ai/a": page("A", "https://acme.ai/a")})

        records = crawl_inventory(fetcher, manual_urls=["https://acme.ai/a"])

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].h1, "A")

    def test_canonical_dedupe_keeps_first_record(self):
        fetcher = StaticPageFetcher({
            "https://acme.ai/a": page("A", "https://acme.ai/canonical"),
            "https://acme.ai/duplicate": page("Duplicate", "https://acme.ai/canonical"),
        })

        records = crawl_inventory(fetcher, manual_urls=["https://acme.ai/a", "https://acme.ai/duplicate"])

        self.assertEqual([record.title for record in records], ["A"])

    def test_malformed_sitemap_and_missing_fixture_are_errors(self):
        fetcher = StaticPageFetcher({"https://acme.ai/sitemap.xml": "broken"})

        with self.assertRaises(PageInventoryError):
            crawl_inventory(fetcher, sitemap_urls=["https://acme.ai/sitemap.xml"])
        with self.assertRaises(PageInventoryError):
            crawl_inventory(StaticPageFetcher({}), manual_urls=["https://acme.ai/missing"])


if __name__ == "__main__":
    unittest.main()

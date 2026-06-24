import unittest

from geo_agent.page_inventory import PageInventoryError, inventory_pages, parse_page


OPEN = chr(60)
CLOSE = chr(62)


def tag(name, body='', attrs=''):
    space = f' {attrs}' if attrs else ''
    return f'{OPEN}{name}{space}{CLOSE}{body}{OPEN}/{name}{CLOSE}'


def sample_html():
    head = tag('title', 'Acme Home') + f"{OPEN}link rel='canonical' href='https://acme.ai/home'{CLOSE}"
    head += f"{OPEN}meta name='last-modified' content='2026-06-01T12:00:00Z'{CLOSE}"
    body = tag('h1', 'AI Visibility') + tag('p', 'Acme measures search visibility.')
    return tag('html', tag('head', head) + tag('body', body, "itemtype='https://schema.org/Organization'"))


class PageInventoryTests(unittest.TestCase):
    def test_parse_page_extracts_inventory_fields(self):
        record = parse_page('https://acme.ai', sample_html(), chunk_size=80)

        self.assertEqual(record.title, 'Acme Home')
        self.assertEqual(record.h1, 'AI Visibility')
        self.assertEqual(record.schema_types, ('Organization',))
        self.assertEqual(record.canonical_url, 'https://acme.ai/home')
        self.assertTrue(record.last_modified.startswith('2026-06-01T12:00:00'))
        self.assertTrue(any('measures search visibility' in chunk for chunk in record.content_chunks))

    def test_inventory_supports_sitemap_and_manual_urls_with_deduplication(self):
        sitemap = tag('urlset', tag('url', tag('loc', 'https://acme.ai')) + tag('url', tag('loc', 'https://acme.ai/about')))
        pages = {'https://acme.ai': sample_html(), 'https://acme.ai/about': sample_html()}

        records = inventory_pages(pages, sitemap_xml=sitemap, manual_urls=['https://acme.ai'])

        self.assertEqual([record.url for record in records], ['https://acme.ai', 'https://acme.ai/about'])

    def test_missing_sitemap_uses_manual_urls_or_pages(self):
        pages = {'https://acme.ai': sample_html()}

        self.assertEqual(len(inventory_pages(pages)), 1)
        self.assertEqual(len(inventory_pages(pages, manual_urls=['https://acme.ai'])), 1)

    def test_malformed_inputs_raise_actionable_errors(self):
        with self.assertRaises(PageInventoryError):
            parse_page('not-a-url', sample_html())
        with self.assertRaises(PageInventoryError):
            parse_page('https://acme.ai', 'plain text')
        with self.assertRaises(PageInventoryError):
            inventory_pages({}, sitemap_xml='broken')


if __name__ == '__main__':
    unittest.main()

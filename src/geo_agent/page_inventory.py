"""Page inventory extraction for GEO Agent."""

from __future__ import annotations

from dataclasses import dataclass
from email.utils import parsedate_to_datetime
import re
from urllib.parse import urlparse
from xml.etree import ElementTree


@dataclass(frozen=True)
class PageInventoryRecord:
    url: str
    title: str | None
    h1: str | None
    schema_types: tuple[str, ...]
    last_modified: str | None
    canonical_url: str
    content_chunks: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "url": self.url,
            "title": self.title,
            "h1": self.h1,
            "schema_types": list(self.schema_types),
            "last_modified": self.last_modified,
            "canonical_url": self.canonical_url,
            "content_chunks": list(self.content_chunks),
        }


class PageInventoryError(ValueError):
    pass


def inventory_pages(
    pages: dict[str, str],
    *,
    sitemap_xml: str | None = None,
    manual_urls: list[str] | None = None,
    chunk_size: int = 240,
) -> list[PageInventoryRecord]:
    urls = _ordered_unique([*_urls_from_sitemap(sitemap_xml), *(manual_urls or [])])
    if not urls:
        urls = list(pages.keys())
    records: list[PageInventoryRecord] = []
    for url in urls:
        if url not in pages:
            continue
        records.append(parse_page(url, pages[url], chunk_size=chunk_size))
    return records


def parse_page(url: str, html: str, *, chunk_size: int = 240) -> PageInventoryRecord:
    if not _valid_url(url):
        raise PageInventoryError(f"Invalid URL: {url}")
    if not isinstance(html, str) or not html.strip() or "<" not in html:
        raise PageInventoryError(f"Malformed HTML for {url}")
    canonical = _first_match(html, r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']') or url
    return PageInventoryRecord(
        url=url,
        title=_clean(_first_match(html, r"<title[^>]*>(.*?)</title>")),
        h1=_clean(_first_match(html, r"<h1[^>]*>(.*?)</h1>")),
        schema_types=tuple(_schema_types(html)),
        last_modified=_last_modified(html),
        canonical_url=canonical,
        content_chunks=tuple(_chunks(_visible_text(html), chunk_size)),
    )


def _urls_from_sitemap(sitemap_xml: str | None) -> list[str]:
    if not sitemap_xml:
        return []
    try:
        root = ElementTree.fromstring(sitemap_xml)
    except ElementTree.ParseError as exc:
        raise PageInventoryError("Malformed sitemap XML") from exc
    urls = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text and element.text.strip():
            urls.append(element.text.strip())
    return urls


def _schema_types(html: str) -> list[str]:
    found = set(re.findall(r'"@type"\s*:\s*"([^"]+)"', html))
    found.update(re.findall(r"itemtype=[\"'][^\"']*/([^/\"']+)[\"']", html))
    return sorted(found)


def _last_modified(html: str) -> str | None:
    value = _first_match(html, r'<meta[^>]+(?:property|name)=["\'](?:article:modified_time|last-modified)["\'][^>]+content=["\']([^"\']+)["\']')
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError):
        return value


def _visible_text(html: str) -> str:
    without_scripts = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.DOTALL | re.I)
    text = re.sub(r"<[^>]+>", " ", without_scripts)
    return re.sub(r"\s+", " ", text).strip()


def _chunks(text: str, chunk_size: int) -> list[str]:
    if chunk_size <= 0:
        raise PageInventoryError("chunk_size must be positive")
    if not text:
        return []
    return [text[index : index + chunk_size].strip() for index in range(0, len(text), chunk_size)]


def _first_match(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.DOTALL | re.I)
    return match.group(1).strip() if match else None


def _clean(value: str | None) -> str | None:
    return re.sub(r"\s+", " ", _visible_text(value)).strip() if value else None


def _ordered_unique(values: list[str]) -> list[str]:
    seen = set()
    unique = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique.append(value)
    return unique


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

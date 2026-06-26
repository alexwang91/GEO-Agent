"""Crawler provider v2: structured status records without live network work."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal
from urllib.parse import urlparse
from xml.etree import ElementTree

from .page_inventory import PageInventoryError, PageInventoryRecord, parse_page
from .provider_access import ProviderAccessError

PageCrawlStatus = Literal["crawled", "rendered_fallback", "failed", "skipped_duplicate"]
PageCrawlSource = Literal["manual", "sitemap", "rendered_fallback"]


@dataclass(frozen=True)
class CrawlerProviderV2Request:
    provider_id: str
    manual_urls: tuple[str, ...] = ()
    sitemap_urls: tuple[str, ...] = ()
    rendered_html: dict[str, str] | None = None
    chunk_size: int = 240

    def __post_init__(self) -> None:
        if not self.manual_urls and not self.sitemap_urls and not self.rendered_html:
            raise ProviderAccessError("At least one crawl input is required.")
        if self.chunk_size <= 0:
            raise ProviderAccessError("chunk_size must be positive.")
        for url in (*self.manual_urls, *self.sitemap_urls, *(self.rendered_html or {}).keys()):
            if not _valid_url(url):
                raise ProviderAccessError(f"Invalid crawl URL: {url}")

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "manual_urls": list(self.manual_urls),
            "sitemap_urls": list(self.sitemap_urls),
            "rendered_html_urls": list((self.rendered_html or {}).keys()),
            "chunk_size": self.chunk_size,
        }


@dataclass(frozen=True)
class PageCrawlResult:
    url: str
    status: PageCrawlStatus
    source: PageCrawlSource
    canonical_url: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CrawlerProviderV2Result:
    provider_id: str
    pages: tuple[PageInventoryRecord, ...]
    page_results: tuple[PageCrawlResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "pages": [page.to_dict() for page in self.pages],
            "page_results": [result.to_dict() for result in self.page_results],
        }


class StaticCrawlerProviderV2:
    provider_id = "static_crawler_v2"

    def __init__(self, pages: dict[str, str], *, sitemaps: dict[str, str] | None = None, rendered_pages: dict[str, str] | None = None) -> None:
        self.pages = dict(pages)
        self.sitemaps = dict(sitemaps or {})
        self.rendered_pages = dict(rendered_pages or {})

    def crawl(self, request: CrawlerProviderV2Request) -> CrawlerProviderV2Result:
        if request.provider_id != self.provider_id:
            raise ProviderAccessError(f"Unsupported crawler provider: {request.provider_id}")
        rendered = {**self.rendered_pages, **(request.rendered_html or {})}
        candidates = _candidate_sources(request, self.sitemaps, rendered)
        pages: list[PageInventoryRecord] = []
        results: list[PageCrawlResult] = []
        canonical_seen: set[str] = set()
        for url, source in candidates.items():
            html = self.pages.get(url)
            status: PageCrawlStatus = "crawled"
            result_source: PageCrawlSource = source
            if html is None:
                html = rendered.get(url)
                if html is None:
                    results.append(PageCrawlResult(url, "failed", source, message="No fixture or rendered HTML for URL."))
                    continue
                status = "rendered_fallback"
                result_source = "rendered_fallback"
            try:
                page = parse_page(url, html, chunk_size=request.chunk_size)
            except PageInventoryError as exc:
                results.append(PageCrawlResult(url, "failed", result_source, message=str(exc)))
                continue
            if page.canonical_url in canonical_seen:
                results.append(PageCrawlResult(url, "skipped_duplicate", result_source, page.canonical_url, "Duplicate canonical URL."))
                continue
            canonical_seen.add(page.canonical_url)
            pages.append(page)
            results.append(PageCrawlResult(url, status, result_source, page.canonical_url))
        return CrawlerProviderV2Result(request.provider_id, tuple(pages), tuple(results))


def _candidate_sources(request: CrawlerProviderV2Request, sitemaps: dict[str, str], rendered: dict[str, str]) -> dict[str, PageCrawlSource]:
    candidates: dict[str, PageCrawlSource] = {}
    for sitemap_url in request.sitemap_urls:
        sitemap_xml = sitemaps.get(sitemap_url)
        if sitemap_xml:
            for url in _urls_from_sitemap(sitemap_xml):
                candidates.setdefault(url, "sitemap")
    for url in request.manual_urls:
        candidates.setdefault(url, "manual")
    for url in rendered:
        candidates.setdefault(url, "rendered_fallback")
    return candidates


def _urls_from_sitemap(sitemap_xml: str) -> tuple[str, ...]:
    try:
        root = ElementTree.fromstring(sitemap_xml)
    except ElementTree.ParseError as exc:
        raise ProviderAccessError("Malformed sitemap XML") from exc
    urls = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text and element.text.strip():
            urls.append(element.text.strip())
    return tuple(urls)


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

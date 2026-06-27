"""Crawler provider v2 with fixture-safe static mode and opt-in live fetch seam."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal, Protocol
from urllib.parse import urlparse
from xml.etree import ElementTree

from .page_inventory import PageInventoryError, PageInventoryRecord, parse_page
from .provider_access import ProviderAccessError

PageCrawlStatus = Literal["crawled", "rendered_fallback", "failed", "skipped_duplicate"]
PageCrawlSource = Literal["manual", "sitemap", "rendered_fallback", "live"]


class FetchClient(Protocol):
    def get(self, url: str, *, timeout_seconds: float) -> tuple[int, str]:
        ...


@dataclass(frozen=True)
class CrawlerProviderV2Request:
    provider_id: str
    manual_urls: tuple[str, ...] = ()
    sitemap_urls: tuple[str, ...] = ()
    rendered_html: dict[str, str] | None = None
    chunk_size: int = 240
    allow_live_fetch: bool = False
    timeout_seconds: float = 10.0

    def __post_init__(self) -> None:
        if not self.manual_urls and not self.sitemap_urls and not self.rendered_html:
            raise ProviderAccessError("At least one crawl input is required.")
        if self.chunk_size <= 0 or self.timeout_seconds <= 0:
            raise ProviderAccessError("chunk_size and timeout_seconds must be positive.")
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
            "allow_live_fetch": self.allow_live_fetch,
            "timeout_seconds": self.timeout_seconds,
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
        return _crawl_candidates(request.provider_id, candidates, self.pages, rendered, request.chunk_size)


class LiveCrawlerProviderV2:
    provider_id = "live_crawler_v2"

    def __init__(self, fetch_client: FetchClient) -> None:
        self.fetch_client = fetch_client

    def crawl(self, request: CrawlerProviderV2Request) -> CrawlerProviderV2Result:
        if request.provider_id != self.provider_id:
            raise ProviderAccessError(f"Unsupported crawler provider: {request.provider_id}")
        if not request.allow_live_fetch:
            raise ProviderAccessError("Live fetch requires allow_live_fetch=True.")
        pages: dict[str, str] = {}
        results: list[PageCrawlResult] = []
        for url in request.manual_urls:
            status_code, html = self.fetch_client.get(url, timeout_seconds=request.timeout_seconds)
            if status_code >= 400:
                results.append(PageCrawlResult(url, "failed", "live", message=f"HTTP {status_code}"))
            else:
                pages[url] = html
        crawled = _crawl_candidates(request.provider_id, {url: "live" for url in request.manual_urls}, pages, {}, request.chunk_size)
        return CrawlerProviderV2Result(request.provider_id, crawled.pages, tuple([*results, *crawled.page_results]))


def _crawl_candidates(provider_id: str, candidates: dict[str, PageCrawlSource], pages_by_url: dict[str, str], rendered: dict[str, str], chunk_size: int) -> CrawlerProviderV2Result:
    pages: list[PageInventoryRecord] = []
    results: list[PageCrawlResult] = []
    canonical_seen: set[str] = set()
    for url, source in candidates.items():
        html = pages_by_url.get(url)
        status: PageCrawlStatus = "crawled"
        result_source: PageCrawlSource = source
        if html is None:
            html = rendered.get(url)
            if html is None:
                results.append(PageCrawlResult(url, "failed", source, message="No fixture, live, or rendered HTML for URL."))
                continue
            status = "rendered_fallback"
            result_source = "rendered_fallback"
        try:
            page = parse_page(url, html, chunk_size=chunk_size)
        except PageInventoryError as exc:
            results.append(PageCrawlResult(url, "failed", result_source, message=str(exc)))
            continue
        if page.canonical_url in canonical_seen:
            results.append(PageCrawlResult(url, "skipped_duplicate", result_source, page.canonical_url, "Duplicate canonical URL."))
            continue
        canonical_seen.add(page.canonical_url)
        pages.append(page)
        results.append(PageCrawlResult(url, status, result_source, page.canonical_url))
    return CrawlerProviderV2Result(provider_id, tuple(pages), tuple(results))


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

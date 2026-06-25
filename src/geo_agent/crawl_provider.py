"""Crawler provider boundary for GEO Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlparse

from .page_inventory import PageInventoryError, PageInventoryRecord, StaticPageFetcher, crawl_inventory
from .provider_access import ProviderAccessError


@dataclass(frozen=True)
class CrawlProviderRequest:
    provider_id: str
    manual_urls: tuple[str, ...] = ()
    sitemap_urls: tuple[str, ...] = ()
    chunk_size: int = 240
    metadata: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.manual_urls and not self.sitemap_urls:
            raise ProviderAccessError("At least one manual URL or sitemap URL is required for crawler providers.")
        if self.chunk_size <= 0:
            raise ProviderAccessError("chunk_size must be positive.")
        for url in (*self.manual_urls, *self.sitemap_urls):
            if not _valid_url(url):
                raise ProviderAccessError(f"Invalid crawl URL: {url}")

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "manual_urls": list(self.manual_urls),
            "sitemap_urls": list(self.sitemap_urls),
            "chunk_size": self.chunk_size,
            "metadata": dict(self.metadata or {}),
        }


@dataclass(frozen=True)
class CrawlProviderError:
    url: str
    message: str
    error_type: str = "crawl_error"

    def to_dict(self) -> dict[str, str]:
        return {"url": self.url, "message": self.message, "error_type": self.error_type}


@dataclass(frozen=True)
class CrawlProviderResult:
    provider_id: str
    pages: tuple[PageInventoryRecord, ...]
    errors: tuple[CrawlProviderError, ...] = ()
    metadata: dict[str, str] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "pages": [page.to_dict() for page in self.pages],
            "errors": [error.to_dict() for error in self.errors],
            "metadata": dict(self.metadata or {}),
        }


class CrawlerProvider(Protocol):
    provider_id: str

    def crawl(self, request: CrawlProviderRequest) -> CrawlProviderResult:
        ...


class StaticCrawlerProvider:
    """Fixture-backed crawler provider for deterministic CI and recorded crawls."""

    provider_id = "static_crawler"

    def __init__(self, pages: dict[str, str], *, sitemaps: dict[str, str] | None = None) -> None:
        self._pages = dict(pages)
        self._sitemaps = dict(sitemaps or {})

    def crawl(self, request: CrawlProviderRequest) -> CrawlProviderResult:
        if request.provider_id not in {self.provider_id, "manual_import"}:
            raise ProviderAccessError(f"Unsupported crawler provider: {request.provider_id}")
        fetcher = StaticPageFetcher({**self._pages, **self._sitemaps})
        try:
            pages = tuple(
                crawl_inventory(
                    fetcher,
                    sitemap_urls=list(request.sitemap_urls),
                    manual_urls=list(request.manual_urls),
                    chunk_size=request.chunk_size,
                )
            )
        except PageInventoryError as exc:
            return CrawlProviderResult(
                provider_id=request.provider_id,
                pages=(),
                errors=(CrawlProviderError(url="", message=str(exc), error_type="page_inventory_error"),),
                metadata={"mode": "static"},
            )
        return CrawlProviderResult(
            provider_id=request.provider_id,
            pages=pages,
            errors=(),
            metadata={"mode": "static", "source": "fixture"},
        )


def pages_from_crawl_result(result: CrawlProviderResult) -> tuple[PageInventoryRecord, ...]:
    return result.pages


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

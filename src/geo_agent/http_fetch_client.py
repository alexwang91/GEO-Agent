"""Concrete stdlib HTTP fetch client for opt-in live crawler use."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser


class FetchClientError(ValueError):
    pass


class UrlOpenResponse(Protocol):
    status: int
    headers: object

    def read(self) -> bytes:
        ...

    def getcode(self) -> int:
        ...

    def __enter__(self) -> "UrlOpenResponse":
        ...

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        ...


UrlOpen = Callable[[Request, float], UrlOpenResponse]


@dataclass(frozen=True)
class HttpFetchConfig:
    user_agent: str = "GEO-Agent/0.1"
    retries: int = 1
    respect_robots: bool = True

    def __post_init__(self) -> None:
        if not self.user_agent.strip():
            raise FetchClientError("user_agent is required.")
        if self.retries < 0:
            raise FetchClientError("retries must be zero or positive.")


class UrlLibFetchClient:
    """Concrete FetchClient using urllib with robots, timeout, retry, and errors.

    This client performs real network access. Callers must keep it behind an
    explicit opt-in gate such as CrawlerProviderV2Request.allow_live_fetch.
    Tests should inject a fake opener and must not use live network access.
    """

    def __init__(self, config: HttpFetchConfig | None = None, *, opener: UrlOpen | None = None) -> None:
        self.config = config or HttpFetchConfig()
        self._opener = opener or _default_open
        self._robots: dict[str, RobotFileParser | None] = {}

    def get(self, url: str, *, timeout_seconds: float) -> tuple[int, str]:
        _validate_url(url)
        if timeout_seconds <= 0:
            raise FetchClientError("timeout_seconds must be positive.")
        if self.config.respect_robots and not self._can_fetch(url, timeout_seconds):
            raise FetchClientError(f"Blocked by robots.txt: {url}")

        last_error: Exception | None = None
        for _attempt in range(self.config.retries + 1):
            try:
                request = self._request(url)
                with self._opener(request, timeout_seconds) as response:
                    return _status(response), _decode_response(response)
            except HTTPError as exc:
                return exc.code, _decode_http_error(exc)
            except (TimeoutError, URLError, OSError) as exc:
                last_error = exc
        raise FetchClientError(f"Fetch failed for {url}: {last_error}")

    def _request(self, url: str) -> Request:
        return Request(url, headers={"User-Agent": self.config.user_agent})

    def _can_fetch(self, url: str, timeout_seconds: float) -> bool:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        if robots_url not in self._robots:
            self._robots[robots_url] = self._load_robots(robots_url, timeout_seconds)
        parser = self._robots[robots_url]
        if parser is None:
            return True
        return parser.can_fetch(self.config.user_agent, url)

    def _load_robots(self, robots_url: str, timeout_seconds: float) -> RobotFileParser | None:
        parser = RobotFileParser()
        parser.set_url(robots_url)
        try:
            with self._opener(self._request(robots_url), timeout_seconds) as response:
                if _status(response) >= 400:
                    return None
                parser.parse(_decode_response(response).splitlines())
                return parser
        except (TimeoutError, URLError, OSError):
            return None


def _default_open(request: Request, timeout_seconds: float) -> UrlOpenResponse:
    return urlopen(request, timeout=timeout_seconds)  # nosec: opt-in live fetch only


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise FetchClientError(f"Invalid fetch URL: {url}")


def _status(response: UrlOpenResponse) -> int:
    status = getattr(response, "status", None)
    if isinstance(status, int):
        return status
    return int(response.getcode())


def _decode_response(response: UrlOpenResponse) -> str:
    charset_getter = getattr(response.headers, "get_content_charset", None)
    charset = charset_getter() if callable(charset_getter) else None
    return response.read().decode(charset or "utf-8", errors="replace")


def _decode_http_error(exc: HTTPError) -> str:
    charset_getter = getattr(exc.headers, "get_content_charset", None)
    charset = charset_getter() if callable(charset_getter) else None
    return exc.read().decode(charset or "utf-8", errors="replace")

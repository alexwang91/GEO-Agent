"""Citation parser v1 for URL normalization, domains, dedupe, and positions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src"}


class CitationParserError(ValueError):
    pass


@dataclass(frozen=True)
class ParsedCitation:
    citation_id: str
    original_url: str
    normalized_url: str
    domain: str
    position: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def normalize_citation_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise CitationParserError(f"Invalid citation URL: {url}")
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if scheme == "http":
        scheme = "https"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    query_items = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered in TRACKING_KEYS or any(lowered.startswith(prefix) for prefix in TRACKING_PREFIXES):
            continue
        query_items.append((key, value))
    query = urlencode(sorted(query_items))
    return urlunparse((scheme, netloc, path, "", query, ""))


def citation_domain(url: str) -> str:
    normalized = normalize_citation_url(url)
    host = urlparse(normalized).hostname or ""
    return host[4:] if host.startswith("www.") else host


def parse_citations(urls: tuple[str, ...] | list[str], *, prefix: str = "citation") -> tuple[ParsedCitation, ...]:
    seen: set[str] = set()
    parsed_items: list[ParsedCitation] = []
    for raw in urls:
        normalized = normalize_citation_url(raw)
        if normalized in seen:
            continue
        seen.add(normalized)
        parsed_items.append(
            ParsedCitation(
                citation_id=f"{prefix}:{len(parsed_items) + 1}",
                original_url=raw,
                normalized_url=normalized,
                domain=citation_domain(normalized),
                position=len(parsed_items) + 1,
            )
        )
    return tuple(parsed_items)

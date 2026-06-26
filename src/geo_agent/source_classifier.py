"""Source classifier for citation and page domains."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal
from urllib.parse import urlparse

SourceClass = Literal[
    "owned",
    "competitor",
    "earned",
    "review",
    "community",
    "directory",
    "docs",
    "marketplace",
    "gov",
    "academic",
    "unknown",
]

REVIEW_DOMAINS = ("g2.com", "capterra.com", "trustpilot.com", "trustradius.com")
COMMUNITY_DOMAINS = ("reddit.com", "quora.com", "stackoverflow.com", "news.ycombinator.com")
DIRECTORY_DOMAINS = ("crunchbase.com", "alternativeto.net", "saasworthy.com", "softwareadvice.com")
MARKETPLACE_DOMAINS = ("apps.shopify.com", "aws.amazon.com", "marketplace.atlassian.com", "appexchange.salesforce.com")
DOC_HINTS = ("docs.", "developer.", "developers.", "help.", "support.")
EARNED_DOMAINS = ("forbes.com", "techcrunch.com", "wired.com", "theverge.com", "businessinsider.com")


@dataclass(frozen=True)
class ClassifiedSource:
    url: str
    domain: str
    source_class: SourceClass
    reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def classify_source(url: str, *, owned_domains: tuple[str, ...] = (), competitor_domains: tuple[str, ...] = ()) -> ClassifiedSource:
    domain = _domain(url)
    owned = tuple(_normalize_domain(item) for item in owned_domains)
    competitors = tuple(_normalize_domain(item) for item in competitor_domains)
    if any(_domain_matches(domain, owned_domain) for owned_domain in owned):
        return ClassifiedSource(url, domain, "owned", "Domain matches an owned property.")
    if any(_domain_matches(domain, competitor_domain) for competitor_domain in competitors):
        return ClassifiedSource(url, domain, "competitor", "Domain matches a competitor property.")
    if domain.endswith(".gov"):
        return ClassifiedSource(url, domain, "gov", "Government top-level domain.")
    if domain.endswith(".edu") or ".ac." in domain:
        return ClassifiedSource(url, domain, "academic", "Academic domain pattern.")
    if _matches(domain, REVIEW_DOMAINS):
        return ClassifiedSource(url, domain, "review", "Known review site domain.")
    if _matches(domain, COMMUNITY_DOMAINS):
        return ClassifiedSource(url, domain, "community", "Known community site domain.")
    if _matches(domain, DIRECTORY_DOMAINS):
        return ClassifiedSource(url, domain, "directory", "Known directory domain.")
    if _matches(domain, MARKETPLACE_DOMAINS):
        return ClassifiedSource(url, domain, "marketplace", "Known marketplace domain.")
    if any(domain.startswith(prefix) for prefix in DOC_HINTS):
        return ClassifiedSource(url, domain, "docs", "Documentation or support subdomain.")
    if _matches(domain, EARNED_DOMAINS):
        return ClassifiedSource(url, domain, "earned", "Known editorial or earned-media domain.")
    return ClassifiedSource(url, domain, "unknown", "No classifier rule matched.")


def classify_sources(urls: tuple[str, ...] | list[str], *, owned_domains: tuple[str, ...] = (), competitor_domains: tuple[str, ...] = ()) -> tuple[ClassifiedSource, ...]:
    return tuple(classify_source(url, owned_domains=owned_domains, competitor_domains=competitor_domains) for url in urls)


def _domain(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.hostname or ""
    return _normalize_domain(host)


def _normalize_domain(domain: str) -> str:
    value = domain.lower().strip().strip("/")
    return value[4:] if value.startswith("www.") else value


def _domain_matches(domain: str, target: str) -> bool:
    return domain == target or domain.endswith(f".{target}")


def _matches(domain: str, candidates: tuple[str, ...]) -> bool:
    return any(_domain_matches(domain, item) for item in candidates)

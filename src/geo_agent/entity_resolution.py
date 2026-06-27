"""Deterministic brand and citation extraction helpers."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from urllib.parse import urlparse

TOKEN_RE = re.compile(r"[\wÀ-ÖØ-öø-ÿ]+", re.UNICODE)
URL_RE = re.compile(r"https?://[^\s)\]}>\"']+|(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s)\]}>\"']*)?", re.I)


@dataclass(frozen=True)
class EntityMatch:
    canonical: str
    matched: str
    start: int
    end: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def normalize_text(value: str) -> str:
    return " ".join(TOKEN_RE.findall(value.lower()))


def normalize_domain(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = parsed.hostname or value
    host = host.lower().strip().strip("/")
    return host[4:] if host.startswith("www.") else host


def domain_matches(domain: str, target: str) -> bool:
    left = normalize_domain(domain)
    right = normalize_domain(target)
    return left == right or left.endswith(f".{right}")


def extract_urls(text: str) -> tuple[str, ...]:
    urls = []
    for match in URL_RE.finditer(text):
        value = match.group(0).rstrip(".,;")
        if "." in value:
            urls.append(value if "://" in value else f"https://{value}")
    return tuple(dict.fromkeys(urls))


def find_entity_matches(text: str, canonical: str, aliases: tuple[str, ...] = ()) -> tuple[EntityMatch, ...]:
    terms = tuple(dict.fromkeys(item for item in (canonical, *aliases) if item.strip()))
    matches: list[EntityMatch] = []
    for term in terms:
        pattern = _term_pattern(term)
        for match in re.finditer(pattern, text, flags=re.I | re.U):
            matches.append(EntityMatch(canonical, match.group(0), match.start(), match.end()))
    matches.sort(key=lambda item: (item.start, -(item.end - item.start)))
    deduped: list[EntityMatch] = []
    seen: set[tuple[int, int, str]] = set()
    for item in matches:
        key = (item.start, item.end, item.matched.lower())
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return tuple(deduped)


def has_entity(text: str, canonical: str, aliases: tuple[str, ...] = ()) -> bool:
    return bool(find_entity_matches(text, canonical, aliases))


def _term_pattern(term: str) -> str:
    tokens = TOKEN_RE.findall(term)
    if not tokens:
        return re.escape(term)
    separator = r"[\s\-_\.]+"
    body = separator.join(re.escape(token) for token in tokens)
    return rf"(?<![\wÀ-ÖØ-öø-ÿ]){body}(?![\wÀ-ÖØ-öø-ÿ])"

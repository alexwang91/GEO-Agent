"""Deterministic query dedupe utilities."""

from __future__ import annotations

import re

from .generator import DiscoveredQuery

_NON_WORD = re.compile(r"[^a-z0-9]+")


def normalize_query_text(value: str) -> str:
    return _NON_WORD.sub(" ", value.lower()).strip()


def dedupe_queries(queries: tuple[DiscoveredQuery, ...]) -> tuple[DiscoveredQuery, ...]:
    seen: set[str] = set()
    result: list[DiscoveredQuery] = []
    for query in queries:
        key = normalize_query_text(query.query.query)
        if key in seen:
            continue
        seen.add(key)
        result.append(query)
    return tuple(result)

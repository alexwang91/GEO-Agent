"""Engine run records and adapter contract."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from urllib.parse import urlparse

from .entity_resolution import extract_urls, find_entity_matches, normalize_domain


@dataclass(frozen=True)
class EngineRun:
    engine: str
    query: str
    timestamp: str
    region: str
    language: str
    raw_answer: str
    citations: tuple[str, ...]
    mentions: tuple[str, ...]
    recommendations: tuple[str, ...]
    source_domains: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return dict(self.__dict__)


class EngineAdapter(Protocol):
    engine: str

    def sample(self, query: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
        ...


class MockEngineAdapter:
    def __init__(self, engine: str, fixtures: dict[str, dict[str, object]]) -> None:
        self.engine = engine
        self.fixtures = fixtures

    def answer(self, text: str, *, region: str, language: str) -> dict[str, object]:
        return self.fixtures.get(text, {"raw_answer": "", "citations": [], "mentions": [], "recommendations": []})

    def sample(self, query: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
        return sample_engine(self, query, region=region, language=language, timestamp=timestamp)


class RecordedRunAdapter:
    """Adapter for recorded answer fixtures exported from real or manual runs."""

    def __init__(self, engine: str, records: dict[str, dict[str, object]]) -> None:
        self.engine = engine
        self.records = records

    def sample(self, query: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
        payload = self.records.get(query)
        if payload is None:
            raise KeyError(f"No recorded run for query: {query}")
        return run_from_payload(
            payload,
            engine=self.engine,
            query=query,
            region=region,
            language=language,
            timestamp=timestamp,
        )


def sample_engine(adapter: MockEngineAdapter, text: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
    payload = adapter.answer(text, region=region, language=language)
    return run_from_payload(payload, engine=adapter.engine, query=text, region=region, language=language, timestamp=timestamp)


def sample_with_adapter(adapter: EngineAdapter, query: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
    return adapter.sample(query, region=region, language=language, timestamp=timestamp)


def run_from_payload(
    payload: dict[str, object], *, engine: str, query: str, region: str, language: str, timestamp: str | None = None
) -> EngineRun:
    raw_answer = str(payload.get("raw_answer", ""))
    citations = _payload_tuple(payload.get("citations", ())) or extract_urls(raw_answer)
    domains = tuple(domain for item in citations if (domain := _domain(item)))
    mentions = _payload_tuple(payload.get("mentions", ()))
    brand = str(payload.get("brand", ""))
    aliases = tuple(str(item) for item in payload.get("brand_aliases", ())) if isinstance(payload.get("brand_aliases", ()), (list, tuple)) else ()
    if not mentions and brand:
        mentions = tuple(match.matched for match in find_entity_matches(raw_answer, brand, aliases))
    return EngineRun(
        engine=engine,
        query=query,
        timestamp=timestamp or str(payload.get("timestamp") or datetime.now(timezone.utc).isoformat()),
        region=region,
        language=language,
        raw_answer=raw_answer,
        citations=citations,
        mentions=mentions,
        recommendations=_payload_tuple(payload.get("recommendations", ())),
        source_domains=domains,
    )


def _payload_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    if value:
        return (str(value),)
    return ()


def _domain(value: str) -> str:
    return normalize_domain(urlparse(value).hostname or value) if value else ""

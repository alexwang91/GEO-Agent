"""Engine run records and adapter contract."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from urllib.parse import urlparse


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
        return {
            "engine": self.engine,
            "query": self.query,
            "timestamp": self.timestamp,
            "region": self.region,
            "language": self.language,
            "raw_answer": self.raw_answer,
            "citations": list(self.citations),
            "mentions": list(self.mentions),
            "recommendations": list(self.recommendations),
            "source_domains": list(self.source_domains),
        }


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
    citations = tuple(str(item) for item in payload.get("citations", []))
    domains = tuple(domain for item in citations if (domain := _domain(item)))
    return EngineRun(
        engine=engine,
        query=query,
        timestamp=timestamp or str(payload.get("timestamp") or datetime.now(timezone.utc).isoformat()),
        region=region,
        language=language,
        raw_answer=str(payload.get("raw_answer", "")),
        citations=citations,
        mentions=tuple(str(item) for item in payload.get("mentions", [])),
        recommendations=tuple(str(item) for item in payload.get("recommendations", [])),
        source_domains=domains,
    )


def _domain(value: str) -> str:
    return (urlparse(value).hostname or "").removeprefix("www.")

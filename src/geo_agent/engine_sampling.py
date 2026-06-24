"""Run records and mock adapter."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
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
        return dict(self.__dict__)


class MockEngineAdapter:
    def __init__(self, engine: str, fixtures: dict[str, dict[str, object]]) -> None:
        self.engine = engine
        self.fixtures = fixtures

    def answer(self, text: str, *, region: str, language: str) -> dict[str, object]:
        return self.fixtures.get(text, {"raw_answer": "", "citations": [], "mentions": [], "recommendations": []})


def sample_engine(adapter: MockEngineAdapter, text: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun:
    payload = adapter.answer(text, region=region, language=language)
    citations = tuple(str(item) for item in payload.get("citations", []))
    domains = tuple(domain for item in citations if (domain := _domain(item)))
    return EngineRun(
        engine=adapter.engine,
        query=text,
        timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
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

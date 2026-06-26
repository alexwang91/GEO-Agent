"""Citation absorption metric for source-quality weighted citation coverage."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .source_classifier import ClassifiedSource, classify_sources

SOURCE_WEIGHTS = {
    "owned": 1.0,
    "earned": 0.95,
    "review": 0.85,
    "docs": 0.8,
    "academic": 0.75,
    "gov": 0.7,
    "directory": 0.6,
    "community": 0.5,
    "marketplace": 0.45,
    "competitor": 0.0,
    "unknown": 0.25,
}


@dataclass(frozen=True)
class CitationAbsorptionMetric:
    score: float
    citation_count: int
    weighted_citation_count: float
    source_mix: dict[str, int]
    directionality: str
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def calculate_citation_absorption(classified_sources: tuple[ClassifiedSource, ...] | list[ClassifiedSource]) -> CitationAbsorptionMetric:
    items = tuple(classified_sources)
    if not items:
        return CitationAbsorptionMetric(0.0, 0, 0.0, {}, "no_sample", ("No citations were available.",))
    source_mix: dict[str, int] = {}
    weighted = 0.0
    for item in items:
        source_mix[item.source_class] = source_mix.get(item.source_class, 0) + 1
        weighted += SOURCE_WEIGHTS[item.source_class]
    score = round(weighted / len(items), 4)
    return CitationAbsorptionMetric(score, len(items), round(weighted, 4), source_mix, _directionality(len(items)), _notes(len(items), source_mix))


def calculate_citation_absorption_from_urls(
    urls: tuple[str, ...] | list[str],
    *,
    owned_domains: tuple[str, ...] = (),
    competitor_domains: tuple[str, ...] = (),
) -> CitationAbsorptionMetric:
    classified = classify_sources(urls, owned_domains=owned_domains, competitor_domains=competitor_domains)
    return calculate_citation_absorption(classified)


def _directionality(count: int) -> str:
    if count < 3:
        return "directional_low_sample"
    if count < 10:
        return "directional"
    return "stable"


def _notes(count: int, source_mix: dict[str, int]) -> tuple[str, ...]:
    notes = []
    if count < 3:
        notes.append("Low citation count; treat the absorption score as directional.")
    if source_mix.get("competitor", 0):
        notes.append("Competitor citations do not add absorption credit.")
    if source_mix.get("unknown", 0):
        notes.append("Unknown sources receive limited absorption credit.")
    return tuple(notes)

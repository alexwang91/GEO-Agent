"""Seed source records used by no-LLM query discovery."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedSource:
    source_id: str
    label: str
    source_type: str
    terms: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "label": self.label,
            "source_type": self.source_type,
            "terms": list(self.terms),
        }


def default_seed_sources(brand: str, category: str, competitors: tuple[str, ...]) -> tuple[SeedSource, ...]:
    competitor_terms = tuple(competitor for competitor in competitors if competitor)
    return (
        SeedSource("brand", "Target brand", "owned", (brand,)),
        SeedSource("category", "Category", "market", (category,)),
        SeedSource("competitors", "Competitors", "competitor", competitor_terms),
        SeedSource("evidence", "Evidence sources", "third_party", ("reviews", "benchmarks", "directories", "case studies")),
    )

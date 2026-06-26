"""Industry templates for GEO audit setup."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class IndustryTemplate:
    template_id: str
    name: str
    query_clusters: tuple[str, ...]
    source_priorities: tuple[str, ...]
    diagnosis_emphasis: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["query_clusters"] = list(self.query_clusters)
        payload["source_priorities"] = list(self.source_priorities)
        payload["diagnosis_emphasis"] = list(self.diagnosis_emphasis)
        return payload


def b2b_saas_template() -> IndustryTemplate:
    return IndustryTemplate(
        "industry:b2b_saas",
        "B2B SaaS",
        ("category alternatives", "integration use cases", "pricing and packaging", "security and compliance", "implementation workflow"),
        ("owned", "earned", "review", "docs", "community"),
        ("weak_citation_absorption", "claim_fidelity_gap", "competitor_displacement", "low_query_coverage"),
    )

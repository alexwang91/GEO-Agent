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


def ecommerce_template() -> IndustryTemplate:
    return IndustryTemplate(
        "industry:ecommerce",
        "Ecommerce",
        ("best product", "product comparison", "price and deals", "reviews and ratings", "shipping and returns"),
        ("owned", "review", "marketplace", "community", "earned"),
        ("weak_citation_absorption", "competitor_displacement", "claim_fidelity_gap", "missing_owned_content"),
    )


def local_service_template() -> IndustryTemplate:
    return IndustryTemplate(
        "industry:local_service",
        "Local Service",
        ("near me intent", "service cost", "booking process", "reviews and reputation", "emergency availability"),
        ("owned", "directory", "review", "community", "earned"),
        ("missing_owned_content", "weak_citation_absorption", "competitor_displacement", "claim_fidelity_gap"),
    )

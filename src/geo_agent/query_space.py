"""Deterministic query space builder for GEO Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .entity_profile import EntityProfile


INTENT_TYPES = (
    "brand",
    "category",
    "comparison",
    "buying_intent",
    "problem_solving",
    "scenario",
    "negative_risk",
    "alternatives",
)

FUNNEL_BY_INTENT = {
    "brand": "awareness",
    "category": "awareness",
    "comparison": "consideration",
    "buying_intent": "conversion",
    "problem_solving": "consideration",
    "scenario": "consideration",
    "negative_risk": "risk_review",
    "alternatives": "consideration",
}

ANSWER_FORMAT_BY_INTENT = {
    "brand": "summary",
    "category": "shortlist",
    "comparison": "comparison_table",
    "buying_intent": "recommendation",
    "problem_solving": "how_to",
    "scenario": "scenario_plan",
    "negative_risk": "risk_review",
    "alternatives": "alternatives_list",
}


@dataclass(frozen=True)
class QueryRecord:
    query: str
    intent_type: str
    funnel_stage: str
    language: str
    region: str
    target_engine: str
    competitor_entities: tuple[str, ...]
    expected_answer_format: str
    priority_score: float
    cluster: str

    def to_dict(self) -> dict[str, object]:
        return {
            "query": self.query,
            "intent_type": self.intent_type,
            "funnel_stage": self.funnel_stage,
            "language": self.language,
            "region": self.region,
            "target_engine": self.target_engine,
            "competitor_entities": list(self.competitor_entities),
            "expected_answer_format": self.expected_answer_format,
            "priority_score": self.priority_score,
            "cluster": self.cluster,
        }


def build_query_space(
    profile: EntityProfile,
    *,
    target_engines: Iterable[str] = ("chatgpt_search",),
    max_queries: int | None = None,
) -> list[QueryRecord]:
    engines = tuple(_normalize_values(target_engines, field="target_engines"))
    records: list[QueryRecord] = []
    for engine in engines:
        for language in profile.target_languages:
            for region in profile.target_regions:
                for intent in INTENT_TYPES:
                    records.append(_record_for_intent(profile, intent, language, region, engine))
                    if max_queries is not None and len(records) >= max_queries:
                        return records
    return records


def _record_for_intent(profile: EntityProfile, intent: str, language: str, region: str, engine: str) -> QueryRecord:
    competitor_text = _competitor_text(profile.competitors)
    query = {
        "brand": f"What is {profile.brand} for {profile.target_customer}?",
        "category": f"Best {profile.category} tools for {profile.target_customer} in {region}",
        "comparison": f"Compare {profile.brand} vs {competitor_text} for {profile.main_product}",
        "buying_intent": f"Should {profile.target_customer} choose {profile.brand} for {profile.business_goal}?",
        "problem_solving": f"How can {profile.target_customer} solve {profile.business_goal} with {profile.category}?",
        "scenario": f"When is {profile.brand} a fit for {profile.main_product} in {region}?",
        "negative_risk": f"Limitations of {profile.brand} for {profile.category}",
        "alternatives": f"Best alternatives to {profile.brand} including {competitor_text}",
    }[intent]
    return QueryRecord(
        query=query,
        intent_type=intent,
        funnel_stage=FUNNEL_BY_INTENT[intent],
        language=language,
        region=region,
        target_engine=engine,
        competitor_entities=profile.competitors,
        expected_answer_format=ANSWER_FORMAT_BY_INTENT[intent],
        priority_score=_priority_score(intent, profile),
        cluster=f"{intent}:{language}:{region}:{engine}",
    )


def _priority_score(intent: str, profile: EntityProfile) -> float:
    base = {
        "buying_intent": 0.95,
        "comparison": 0.9,
        "category": 0.82,
        "alternatives": 0.8,
        "problem_solving": 0.74,
        "scenario": 0.68,
        "negative_risk": 0.58,
        "brand": 0.55,
    }[intent]
    return round(min(base + min(len(profile.competitors) * 0.01, 0.03), 1.0), 2)


def _competitor_text(competitors: tuple[str, ...]) -> str:
    if len(competitors) == 1:
        return competitors[0]
    return ", ".join(competitors[:-1]) + f", and {competitors[-1]}"


def _normalize_values(values: Iterable[str], *, field: str) -> list[str]:
    normalized = [value.strip() for value in values if isinstance(value, str) and value.strip()]
    if not normalized:
        raise ValueError(f"{field} must contain at least one non-empty string")
    return normalized

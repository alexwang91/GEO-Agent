"""Deterministic no-LLM query discovery."""

from __future__ import annotations

from dataclasses import dataclass

from geo_agent.entity_profile import EntityProfile
from geo_agent.query_space import QueryRecord

from .citation_likelihood import citation_likelihood_score
from .cluster_schema import DEFAULT_CLUSTERS, QueryCluster
from .dedupe import dedupe_queries
from .perspectives import DEFAULT_PERSPECTIVES, QueryPerspective
from .seed_sources import SeedSource, default_seed_sources

VARIATIONS = ("baseline", "comparison", "evidence", "risk")


@dataclass(frozen=True)
class DiscoveredQuery:
    query: QueryRecord
    cluster_id: str
    perspective_id: str
    seed_source_ids: tuple[str, ...]
    business_value_score: float
    citation_likelihood_score: float
    priority_score: float

    def to_dict(self) -> dict[str, object]:
        payload = self.query.to_dict()
        payload.update(
            {
                "cluster_id": self.cluster_id,
                "perspective_id": self.perspective_id,
                "seed_source_ids": list(self.seed_source_ids),
                "business_value_score": self.business_value_score,
                "citation_likelihood_score": self.citation_likelihood_score,
                "priority_score": self.priority_score,
            }
        )
        return payload


@dataclass(frozen=True)
class QueryDiscoveryResult:
    mode: str
    queries: tuple[DiscoveredQuery, ...]
    clusters: tuple[QueryCluster, ...]
    perspectives: tuple[QueryPerspective, ...]
    seed_sources: tuple[SeedSource, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "queries": [query.to_dict() for query in self.queries],
            "clusters": [cluster.to_dict() for cluster in self.clusters],
            "perspectives": [perspective.to_dict() for perspective in self.perspectives],
            "seed_sources": [source.to_dict() for source in self.seed_sources],
        }


def discover_queries_no_llm(profile: EntityProfile, *, target_engine: str = "manual", limit: int | None = None) -> QueryDiscoveryResult:
    seeds = default_seed_sources(profile.brand, profile.category, profile.competitors)
    discovered: list[DiscoveredQuery] = []
    for cluster in DEFAULT_CLUSTERS:
        for perspective in DEFAULT_PERSPECTIVES:
            for variation in VARIATIONS:
                text = _query_text(profile, cluster, perspective, variation)
                citation_score = citation_likelihood_score(text, cluster_id=cluster.cluster_id)
                base_priority = _priority(cluster, perspective)
                record = QueryRecord(
                    query=text,
                    intent_type=cluster.intent_type,
                    funnel_stage=cluster.funnel_stage,
                    language=profile.target_languages[0],
                    region=profile.target_regions[0],
                    target_engine=target_engine,
                    competitor_entities=profile.competitors,
                    expected_answer_format="shortlist",
                    priority_score=base_priority,
                    cluster=cluster.cluster_id,
                )
                discovered.append(DiscoveredQuery(record, cluster.cluster_id, perspective.perspective_id, tuple(source.source_id for source in seeds), 0.0, citation_score, base_priority))
    deduped = dedupe_queries(tuple(discovered))
    if limit is not None:
        deduped = deduped[:limit]
    return QueryDiscoveryResult("no_llm_fixture", deduped, DEFAULT_CLUSTERS, DEFAULT_PERSPECTIVES, seeds)


def _query_text(profile: EntityProfile, cluster: QueryCluster, perspective: QueryPerspective, variation: str) -> str:
    category = profile.category or profile.main_product
    competitor = profile.competitors[0] if profile.competitors else "alternatives"
    templates = {
        "baseline": {
            "problem": "What should {role} know before choosing {category} for {customer}?",
            "solution": "How does {brand} compare with {competitor} for {angle}?",
            "brand": "Is {brand} a credible {category} option for {customer}?",
            "source": "Which reviews or benchmarks mention {brand} and {competitor} for {category}?",
            "decision": "Best {category} shortlist for {customer} when {angle} matters",
        },
        "comparison": {
            "problem": "Common {category} problems for {customer} and how {role} evaluates them",
            "solution": "Compare {brand}, {competitor}, and alternatives for {customer}",
            "brand": "What evidence supports choosing {brand} instead of {competitor}?",
            "source": "Top directories or expert roundups for {category} including {brand}",
            "decision": "Which {category} vendor should {customer} choose between {brand} and {competitor}?",
        },
        "evidence": {
            "problem": "What evidence should {role} look for in {category} tools?",
            "solution": "Which {category} tools have case studies for {customer}?",
            "brand": "Does {brand} publish credible proof for {angle}?",
            "source": "What third-party sources cite {brand} for {category}?",
            "decision": "Best evidenced {category} options for {customer}",
        },
        "risk": {
            "problem": "Risks {customer} should check before buying {category}",
            "solution": "Limitations of {brand} versus {competitor} for {angle}",
            "brand": "When is {brand} not a fit for {customer}?",
            "source": "Negative reviews or weak citations for {brand} in {category}",
            "decision": "Safest {category} shortlist for {customer} with risks explained",
        },
    }
    return templates[variation][cluster.cluster_id].format(
        role=perspective.user_role,
        category=category,
        customer=profile.target_customer,
        brand=profile.brand,
        competitor=competitor,
        angle=perspective.prompt_angle,
    )


def _priority(cluster: QueryCluster, perspective: QueryPerspective) -> float:
    cluster_weight = {"decision": 0.9, "solution": 0.82, "brand": 0.78, "source": 0.7, "problem": 0.66}[cluster.cluster_id]
    perspective_weight = {"buyer": 0.04, "technical": 0.04, "operator": 0.02, "pr": 0.02}[perspective.perspective_id]
    return round(min(cluster_weight + perspective_weight, 1.0), 2)

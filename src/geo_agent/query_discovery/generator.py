"""Deterministic no-LLM query discovery."""

from __future__ import annotations

from dataclasses import dataclass

from geo_agent.entity_profile import EntityProfile
from geo_agent.query_space import QueryRecord

from .cluster_schema import DEFAULT_CLUSTERS, QueryCluster
from .perspectives import DEFAULT_PERSPECTIVES, QueryPerspective
from .seed_sources import SeedSource, default_seed_sources


@dataclass(frozen=True)
class DiscoveredQuery:
    query: QueryRecord
    cluster_id: str
    perspective_id: str
    seed_source_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        payload = self.query.to_dict()
        payload.update(
            {
                "cluster_id": self.cluster_id,
                "perspective_id": self.perspective_id,
                "seed_source_ids": list(self.seed_source_ids),
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
            text = _query_text(profile, cluster, perspective)
            record = QueryRecord(
                query=text,
                intent_type=cluster.intent_type,
                funnel_stage=cluster.funnel_stage,
                language=profile.target_languages[0],
                region=profile.target_regions[0],
                target_engine=target_engine,
                competitors=profile.competitors,
                priority=_priority(cluster, perspective),
                cluster=cluster.cluster_id,
            )
            discovered.append(DiscoveredQuery(record, cluster.cluster_id, perspective.perspective_id, tuple(source.source_id for source in seeds)))
    if limit is not None:
        discovered = discovered[:limit]
    return QueryDiscoveryResult("no_llm_fixture", tuple(discovered), DEFAULT_CLUSTERS, DEFAULT_PERSPECTIVES, seeds)


def _query_text(profile: EntityProfile, cluster: QueryCluster, perspective: QueryPerspective) -> str:
    category = profile.category or profile.main_product
    competitor = profile.competitors[0] if profile.competitors else "alternatives"
    templates = {
        "problem": "What should {role} know before choosing {category} for {customer}?",
        "solution": "How does {brand} compare with {competitor} for {angle}?",
        "brand": "Is {brand} a credible {category} option for {customer}?",
        "source": "Which reviews or benchmarks mention {brand} and {competitor} for {category}?",
        "decision": "Best {category} shortlist for {customer} when {angle} matters",
    }
    return templates[cluster.cluster_id].format(
        role=perspective.user_role,
        category=category,
        customer=profile.target_customer,
        brand=profile.brand,
        competitor=competitor,
        angle=perspective.prompt_angle,
    )


def _priority(cluster: QueryCluster, perspective: QueryPerspective) -> int:
    cluster_weight = {"decision": 5, "solution": 4, "brand": 4, "source": 3, "problem": 3}[cluster.cluster_id]
    perspective_weight = {"buyer": 2, "technical": 2, "operator": 1, "pr": 1}[perspective.perspective_id]
    return min(5, cluster_weight + perspective_weight - 1)

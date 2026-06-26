"""Deterministic ranking for discovered queries."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .generator import DiscoveredQuery


@dataclass(frozen=True)
class RankedQuery:
    discovered_query: DiscoveredQuery
    business_value_score: float
    citation_likelihood_score: float
    priority_score: float
    rank: int

    def to_dict(self) -> dict[str, object]:
        payload = self.discovered_query.to_dict()
        payload.update(
            {
                "business_value_score": self.business_value_score,
                "citation_likelihood_score": self.citation_likelihood_score,
                "priority_score": self.priority_score,
                "rank": self.rank,
            }
        )
        return payload


def business_value_score(cluster_id: str, perspective_id: str) -> float:
    cluster = {"decision": 0.92, "solution": 0.86, "brand": 0.78, "source": 0.72, "problem": 0.64}[cluster_id]
    perspective = {"buyer": 0.06, "technical": 0.05, "operator": 0.03, "pr": 0.02}[perspective_id]
    return round(min(cluster + perspective, 1.0), 2)


def rank_queries(queries: tuple[DiscoveredQuery, ...]) -> tuple[RankedQuery, ...]:
    ranked: list[RankedQuery] = []
    for query in queries:
        business = business_value_score(query.cluster_id, query.perspective_id)
        citation = query.citation_likelihood_score
        priority = round((business * 0.55) + (citation * 0.3) + (query.query.priority_score * 0.15), 3)
        updated_record = replace(query.query, priority_score=priority)
        updated_query = replace(query, query=updated_record, business_value_score=business, priority_score=priority)
        ranked.append(RankedQuery(updated_query, business, citation, priority, 0))
    ranked.sort(key=lambda item: (-item.priority_score, item.discovered_query.query.query, item.discovered_query.cluster_id, item.discovered_query.perspective_id))
    return tuple(replace(item, rank=index) for index, item in enumerate(ranked, start=1))

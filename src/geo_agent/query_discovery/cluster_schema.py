"""Cluster schema for multi-perspective query discovery."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryCluster:
    cluster_id: str
    label: str
    intent_type: str
    funnel_stage: str
    description: str

    def to_dict(self) -> dict[str, str]:
        return {
            "cluster_id": self.cluster_id,
            "label": self.label,
            "intent_type": self.intent_type,
            "funnel_stage": self.funnel_stage,
            "description": self.description,
        }


DEFAULT_CLUSTERS: tuple[QueryCluster, ...] = (
    QueryCluster("problem", "Problem framing", "informational", "awareness", "Questions about the user problem and category need."),
    QueryCluster("solution", "Solution comparison", "commercial", "consideration", "Questions that compare solution approaches and vendors."),
    QueryCluster("brand", "Brand validation", "navigational", "consideration", "Questions that validate the target brand and alternatives."),
    QueryCluster("source", "Source discovery", "informational", "consideration", "Questions about reviews, benchmarks, directories, and cited sources."),
    QueryCluster("decision", "Decision support", "transactional", "decision", "Questions about best choices, shortlist criteria, risks, and next actions."),
)


def cluster_by_id(cluster_id: str) -> QueryCluster:
    for cluster in DEFAULT_CLUSTERS:
        if cluster.cluster_id == cluster_id:
            return cluster
    raise KeyError(f"Unknown query cluster: {cluster_id}")

from __future__ import annotations

from dataclasses import dataclass

from .failure_debugger import FailureDiagnosis
from .query_space import QueryRecord

GEO_OPTIMIZATION_METHODS = (
    "authoritative",
    "statistics_addition",
    "keyword_stuffing",
    "cite_sources",
    "quotation_addition",
    "easy_to_understand",
    "fluency_optimization",
    "unique_words",
    "technical_terms",
)

_FAILURE_METHOD_MAP = {
    "retrieval": "cite_sources",
    "reranking": "authoritative",
    "synthesis": "statistics_addition",
    "attribution": "cite_sources",
    "competitor_source": "authoritative",
    "trust": "quotation_addition",
    "entity": "technical_terms",
    "intent_mismatch": "easy_to_understand",
}


@dataclass(frozen=True)
class OptimizationTaskBrief:
    action_type: str
    target_page: str
    query_cluster: str
    expected_impact: str
    confidence: float
    risk: str
    draft_content: str
    retest_plan: str
    failure_type: str
    method: str = "cite_sources"
    owner: str = "content_strategy"
    expected_metric: str = "citation_share"
    evidence_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "action_type": self.action_type,
            "target_page": self.target_page,
            "query_cluster": self.query_cluster,
            "expected_impact": self.expected_impact,
            "confidence": self.confidence,
            "risk": self.risk,
            "draft_content": self.draft_content,
            "retest_plan": self.retest_plan,
            "failure_type": self.failure_type,
            "method": self.method,
            "owner": self.owner,
            "expected_metric": self.expected_metric,
            "evidence_ids": list(self.evidence_ids),
        }


def generate_task_brief(query: QueryRecord, diagnosis: FailureDiagnosis, *, target_page: str) -> OptimizationTaskBrief:
    failure = diagnosis.failure_types[0]
    method = _method_for_failure(failure)
    action = _action_for_method(method)
    expected_metric = _expected_metric_for_method(method)
    evidence_ids = diagnosis.evidence or (query.query,)
    return OptimizationTaskBrief(
        action,
        target_page,
        query.cluster,
        "medium",
        0.0,
        "draft_only_no_auto_publish",
        f"Optimization brief for {query.intent_type}: {query.query}",
        f"Retest {query.cluster} on {query.target_engine} and compare {expected_metric}.",
        failure,
        method,
        "content_strategy",
        expected_metric,
        evidence_ids,
    )


def _method_for_failure(failure: str) -> str:
    return _FAILURE_METHOD_MAP.get(failure, "fluency_optimization")


def _action_for_method(method: str) -> str:
    return {
        "authoritative": "increase_authority_signals",
        "statistics_addition": "add_statistics",
        "keyword_stuffing": "review_keyword_coverage",
        "cite_sources": "add_citable_sources",
        "quotation_addition": "add_quotations",
        "easy_to_understand": "simplify_explanation",
        "fluency_optimization": "improve_fluency",
        "unique_words": "add_distinctive_terms",
        "technical_terms": "clarify_technical_entities",
    }[method]


def _expected_metric_for_method(method: str) -> str:
    return {
        "authoritative": "owned_citation_share",
        "statistics_addition": "citation_absorption",
        "keyword_stuffing": "mention_share",
        "cite_sources": "owned_citation_share",
        "quotation_addition": "claim_fidelity",
        "easy_to_understand": "recommendation_share",
        "fluency_optimization": "subjective_impression_score",
        "unique_words": "citation_selection",
        "technical_terms": "entity_match_rate",
    }[method]

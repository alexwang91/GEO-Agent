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


def generate_task_brief(query: QueryRecord, diagnosis: FailureDiagnosis, *, target_page: str) -> OptimizationTaskBrief:
    failure = diagnosis.failure_types[0]
    action = {
        "retrieval": "strengthen_page_evidence",
        "reranking": "improve_source_authority",
        "synthesis": "add_comparison_context",
        "attribution": "add_citable_claims",
        "trust": "add_third_party_evidence",
        "entity": "clarify_entity_profile",
        "intent_mismatch": "align_page_to_intent",
    }.get(failure, "review_page")
    return OptimizationTaskBrief(action, target_page, query.cluster, "medium", 0.72, "draft_only_no_auto_publish", f"Draft update for {query.intent_type}: {query.query}", f"Retest {query.cluster} on {query.target_engine}.", failure)


def build_task_plan(query: QueryRecord, diagnosis: FailureDiagnosis, *, target_page: str) -> dict[str, object]:
    brief = generate_task_brief(query, diagnosis, target_page=target_page)
    method = _method_for_failure(brief.failure_type)
    expected_metric = _expected_metric_for_method(method)
    return {
        "action_type": brief.action_type,
        "target_page": brief.target_page,
        "query_cluster": brief.query_cluster,
        "method": method,
        "owner": "content_strategy",
        "expected_metric": expected_metric,
        "risk": brief.risk,
        "retest_plan": f"{brief.retest_plan} Compare {expected_metric}.",
        "evidence_ids": list(diagnosis.evidence or (query.query,)),
        "confidence_source": "legacy_default_requires_retest",
    }


def _method_for_failure(failure: str) -> str:
    return _FAILURE_METHOD_MAP.get(failure, "fluency_optimization")


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

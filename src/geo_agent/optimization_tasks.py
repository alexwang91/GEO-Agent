from __future__ import annotations
from dataclasses import dataclass
from .failure_debugger import FailureDiagnosis
from .query_space import QueryRecord

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

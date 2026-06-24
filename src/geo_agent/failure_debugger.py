from __future__ import annotations
from dataclasses import dataclass
from .engine_sampling import EngineRun

FAILURE_TYPES = ("retrieval", "reranking", "synthesis", "attribution", "trust", "entity", "intent_mismatch")

@dataclass(frozen=True)
class FailureDiagnosis:
    failure_types: tuple[str, ...]
    explanation: str
    next_step: str
    evidence: tuple[str, ...]

def diagnose_citation_failure(run: EngineRun, *, brand: str, brand_domain: str, query_intent: str) -> FailureDiagnosis:
    name = brand.lower()
    seen = name in run.raw_answer.lower() or name in {x.lower() for x in run.mentions}
    linked = any(brand_domain in d for d in run.source_domains)
    labels = []
    proof = []
    if not run.raw_answer.strip():
        labels.append("retrieval"); proof.append("empty answer")
    if seen and not linked:
        labels.append("attribution"); proof.append("brand without owned source")
    if not seen and run.source_domains:
        labels.append("reranking"); proof.append("sources exist without brand")
    if name not in {x.lower() for x in run.mentions} and name in run.raw_answer.lower():
        labels.append("entity"); proof.append("text mention not parsed")
    if query_intent == "buying_intent" and seen and name not in {x.lower() for x in run.recommendations}:
        labels.append("synthesis"); proof.append("mentioned but not selected")
    if not labels:
        labels.append("trust" if not linked else "intent_mismatch"); proof.append("fallback classification")
    ordered = tuple(label for label in FAILURE_TYPES if label in set(labels))
    return FailureDiagnosis(ordered, ", ".join(proof), "Inspect page and source evidence for the cluster.", tuple(proof))

from __future__ import annotations
from dataclasses import dataclass
from .engine_sampling import EngineRun
from .page_inventory import PageInventoryRecord
from .query_space import QueryRecord

FAILURE_TYPES = (
    "retrieval",
    "reranking",
    "synthesis",
    "attribution",
    "competitor_source",
    "trust",
    "entity",
    "intent_mismatch",
)

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


def diagnose_failure_v2(
    run: EngineRun,
    query: QueryRecord,
    *,
    pages: tuple[PageInventoryRecord, ...],
    brand: str,
    brand_domain: str,
    competitors: tuple[str, ...] = (),
) -> FailureDiagnosis:
    """Classify a failure using answer, source, query, page, and competitor evidence."""
    name = brand.lower()
    answer = run.raw_answer.lower()
    parsed_mentions = {item.lower() for item in run.mentions}
    parsed_recommendations = {item.lower() for item in run.recommendations}
    seen = name in answer or name in parsed_mentions
    linked = any(brand_domain in domain for domain in run.source_domains)
    competitor_hits = tuple(competitor for competitor in competitors if competitor.lower() in answer)
    owned_page_hits = _owned_page_hits(pages, brand, brand_domain)

    labels: list[str] = []
    proof: list[str] = [
        f"query_cluster={query.cluster}",
        f"query_intent={query.intent_type}",
        f"owned_pages={len(pages)}",
    ]

    if not run.raw_answer.strip():
        labels.append("retrieval")
        proof.append("empty answer")
    if owned_page_hits and not seen:
        labels.append("retrieval")
        proof.append("owned page evidence exists but answer omitted brand")
    if seen and not linked:
        labels.append("attribution")
        proof.append("brand appears without owned citation")
    if competitor_hits and not linked:
        labels.append("competitor_source")
        proof.append("competitor mentioned without owned brand citation: " + ", ".join(competitor_hits))
    if name in answer and name not in parsed_mentions:
        labels.append("entity")
        proof.append("brand text mention was not parsed as entity mention")
    if query.intent_type == "buying_intent" and seen and name not in parsed_recommendations:
        labels.append("intent_mismatch")
        proof.append("buying-intent query did not recommend the brand")
    if run.source_domains and not seen and not competitor_hits:
        labels.append("reranking")
        proof.append("sources exist but answer omits brand and competitors")
    if not labels:
        labels.append("trust" if not linked else "intent_mismatch")
        proof.append("fallback classification with available evidence")

    ordered = tuple(label for label in FAILURE_TYPES if label in set(labels))
    return FailureDiagnosis(
        ordered,
        "; ".join(proof),
        "Inspect the cited source set, owned-page evidence, and query intent before drafting an optimization task.",
        tuple(proof),
    )


def _owned_page_hits(pages: tuple[PageInventoryRecord, ...], brand: str, brand_domain: str) -> tuple[str, ...]:
    name = brand.lower()
    hits: list[str] = []
    for page in pages:
        text = " ".join(page.content_chunks).lower()
        if brand_domain in page.canonical_url or name in text or name in (page.title or "").lower() or name in (page.h1 or "").lower():
            hits.append(page.canonical_url)
    return tuple(hits)

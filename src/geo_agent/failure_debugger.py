from __future__ import annotations
import re
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

CONTENT_FEATURE_TAXONOMY = (
    "statistics",
    "quotations",
    "authoritative_sources",
    "schema",
    "entity_clarity",
    "faq",
    "freshness",
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
    feature_gaps = _content_feature_gaps(pages, brand)

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
    if feature_gaps:
        labels.append("trust")
        proof.extend(f"feature_gap={gap}" for gap in feature_gaps)
    if not labels:
        labels.append("trust" if not linked else "intent_mismatch")
        proof.append("fallback classification with available evidence")

    ordered = tuple(label for label in FAILURE_TYPES if label in set(labels))
    next_step = "Inspect the cited source set, owned-page evidence, and query intent before drafting an optimization task."
    if feature_gaps:
        next_step += " Address content feature gaps: " + ", ".join(feature_gaps) + "."
    return FailureDiagnosis(
        ordered,
        "; ".join(proof),
        next_step,
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


def _content_feature_gaps(pages: tuple[PageInventoryRecord, ...], brand: str) -> tuple[str, ...]:
    if not pages:
        return ()
    text = " ".join(
        item
        for page in pages
        for item in ((page.title or ""), (page.h1 or ""), " ".join(page.content_chunks), " ".join(page.schema_types), page.last_modified or "")
    ).lower()
    gaps: list[str] = []
    if not re.search(r"\b\d+(?:[.,]\d+)?\s*(?:%|percent|hours?|days?|mah|gb|km|meters?|users?|reviews?)\b", text):
        gaps.append("statistics")
    if '"' not in text and "“" not in text and "quote" not in text and "testimonial" not in text:
        gaps.append("quotations")
    if not any(marker in text for marker in ("study", "research", "official", "certified", "source", "citation", "according to")):
        gaps.append("authoritative_sources")
    if not any(schema.lower() in text for schema in ("product", "faqpage", "review", "organization", "breadcrumblist")):
        gaps.append("schema")
    if brand.lower() not in text:
        gaps.append("entity_clarity")
    if "faq" not in text and "question" not in text and "answer" not in text:
        gaps.append("faq")
    if not re.search(r"\b20\d{2}\b", text) and "updated" not in text and "latest" not in text:
        gaps.append("freshness")
    return tuple(gap for gap in CONTENT_FEATURE_TAXONOMY if gap in set(gaps))

"""Deterministic citation-likelihood scoring for discovered queries."""

from __future__ import annotations

SOURCE_TERMS = ("review", "reviews", "benchmark", "benchmarks", "directory", "directories", "case studies", "compare", "comparison")
DECISION_TERMS = ("best", "shortlist", "compare", "credible")


def citation_likelihood_score(query: str, *, cluster_id: str) -> float:
    text = query.lower()
    score = 0.35
    if cluster_id == "source":
        score += 0.35
    if cluster_id in {"solution", "decision"}:
        score += 0.18
    if any(term in text for term in SOURCE_TERMS):
        score += 0.22
    if any(term in text for term in DECISION_TERMS):
        score += 0.08
    return round(min(score, 1.0), 2)

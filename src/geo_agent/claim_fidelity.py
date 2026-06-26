"""Deterministic claim fidelity audit against static evidence text."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Literal

ClaimFidelityStatus = Literal["supported", "partial", "unsupported", "contradicted", "unknown"]

NEGATION_TERMS = ("not", "no", "never", "without", "cannot", "can't", "does not", "is not")


@dataclass(frozen=True)
class ClaimFidelityResult:
    claim_id: str
    claim_text: str
    status: ClaimFidelityStatus
    support_score: float
    matched_evidence_ids: tuple[str, ...]
    missing_terms: tuple[str, ...]
    reason: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["matched_evidence_ids"] = list(self.matched_evidence_ids)
        payload["missing_terms"] = list(self.missing_terms)
        return payload


def audit_claim_fidelity(
    claim_id: str,
    claim_text: str,
    evidence_texts: dict[str, str],
    *,
    contradiction_texts: dict[str, str] | None = None,
) -> ClaimFidelityResult:
    terms = _terms(claim_text)
    if not terms or not evidence_texts:
        return ClaimFidelityResult(claim_id, claim_text, "unknown", 0.0, (), tuple(terms), "Insufficient claim or evidence text.")
    contradiction_ids = _matching_ids(terms, contradiction_texts or {}, min_overlap=0.6)
    if contradiction_ids or _negation_conflict(claim_text, evidence_texts):
        return ClaimFidelityResult(claim_id, claim_text, "contradicted", 0.0, tuple(contradiction_ids), tuple(terms), "Contradictory evidence matched the claim.")
    matched_ids = _matching_ids(terms, evidence_texts, min_overlap=0.35)
    matched_terms = set()
    for evidence_id in matched_ids:
        matched_terms.update(set(terms) & set(_terms(evidence_texts[evidence_id])))
    support_score = round(len(matched_terms) / len(terms), 4)
    missing = tuple(term for term in terms if term not in matched_terms)
    if support_score >= 0.8:
        status: ClaimFidelityStatus = "supported"
        reason = "Most claim terms are present in cited evidence."
    elif support_score >= 0.35:
        status = "partial"
        reason = "Some claim terms are present in cited evidence."
    else:
        status = "unsupported"
        reason = "Claim terms are not materially present in cited evidence."
    return ClaimFidelityResult(claim_id, claim_text, status, support_score, tuple(matched_ids), missing, reason)


def audit_claims_fidelity(claims: dict[str, str], evidence_texts: dict[str, str]) -> tuple[ClaimFidelityResult, ...]:
    return tuple(audit_claim_fidelity(claim_id, claim_text, evidence_texts) for claim_id, claim_text in claims.items())


def _terms(text: str) -> tuple[str, ...]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"the", "a", "an", "and", "or", "to", "for", "of", "in", "on", "with", "is", "are", "it", "that"}
    return tuple(word for word in words if len(word) > 2 and word not in stop)


def _matching_ids(terms: tuple[str, ...], evidence_texts: dict[str, str], *, min_overlap: float) -> list[str]:
    matched = []
    term_set = set(terms)
    for evidence_id, text in evidence_texts.items():
        evidence_terms = set(_terms(text))
        if not evidence_terms:
            continue
        overlap = len(term_set & evidence_terms) / len(term_set)
        if overlap >= min_overlap:
            matched.append(evidence_id)
    return matched


def _negation_conflict(claim_text: str, evidence_texts: dict[str, str]) -> bool:
    claim_negated = any(term in claim_text.lower() for term in NEGATION_TERMS)
    for text in evidence_texts.values():
        evidence_negated = any(term in text.lower() for term in NEGATION_TERMS)
        if claim_negated != evidence_negated and len(set(_terms(claim_text)) & set(_terms(text))) >= 3:
            return True
    return False

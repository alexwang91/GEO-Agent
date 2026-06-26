"""Diagnosis taxonomy v3 records and helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

DiagnosisType = Literal[
    "missing_owned_content",
    "weak_citation_absorption",
    "claim_fidelity_gap",
    "competitor_displacement",
    "low_query_coverage",
    "unstable_sampling",
    "provider_unavailable",
]
Severity = Literal["low", "medium", "high", "critical"]

DEFAULT_ACTIONS = {
    "missing_owned_content": "Create or improve owned content for the affected query cluster.",
    "weak_citation_absorption": "Increase citation-quality sources and reinforce owned/earned evidence.",
    "claim_fidelity_gap": "Align claims with evidence-backed page content.",
    "competitor_displacement": "Map competitor-cited sources and close content/source gaps.",
    "low_query_coverage": "Expand query coverage before drawing conclusions.",
    "unstable_sampling": "Increase repeated samples and use directional language.",
    "provider_unavailable": "Resolve provider access or use manual import.",
}


@dataclass(frozen=True)
class DiagnosisV3:
    diagnosis_id: str
    diagnosis_type: DiagnosisType
    severity: Severity
    evidence_ids: tuple[str, ...]
    summary: str
    recommended_action: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["evidence_ids"] = list(self.evidence_ids)
        return payload


def create_diagnosis_v3(diagnosis_id: str, diagnosis_type: DiagnosisType, severity: Severity, evidence_ids: tuple[str, ...], summary: str, recommended_action: str | None = None) -> DiagnosisV3:
    if not diagnosis_id.strip():
        raise ValueError("diagnosis_id is required")
    if not evidence_ids:
        raise ValueError("at least one evidence id is required")
    action = recommended_action or DEFAULT_ACTIONS[diagnosis_type]
    return DiagnosisV3(diagnosis_id, diagnosis_type, severity, evidence_ids, summary, action)


def severity_rank(severity: Severity) -> int:
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}[severity]

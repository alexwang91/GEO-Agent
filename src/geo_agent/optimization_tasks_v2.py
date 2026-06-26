"""Optimization task engine v2."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .diagnosis_taxonomy_v3 import DiagnosisV3, severity_rank

OWNER_HINTS = {
    "missing_owned_content": "content",
    "weak_citation_absorption": "digital_pr",
    "claim_fidelity_gap": "product_marketing",
    "competitor_displacement": "seo",
    "low_query_coverage": "research",
    "unstable_sampling": "analytics",
    "provider_unavailable": "ops",
}

EFFORT = {
    "missing_owned_content": 3,
    "weak_citation_absorption": 4,
    "claim_fidelity_gap": 2,
    "competitor_displacement": 4,
    "low_query_coverage": 2,
    "unstable_sampling": 1,
    "provider_unavailable": 1,
}


@dataclass(frozen=True)
class OptimizationTaskV2:
    task_id: str
    title: str
    diagnosis_id: str
    owner_hint: str
    impact: int
    effort: int
    priority_score: float
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["evidence_ids"] = list(self.evidence_ids)
        return payload


def tasks_from_diagnoses(diagnoses: tuple[DiagnosisV3, ...] | list[DiagnosisV3]) -> tuple[OptimizationTaskV2, ...]:
    tasks = []
    for index, diagnosis in enumerate(diagnoses, start=1):
        impact = severity_rank(diagnosis.severity)
        effort = EFFORT[diagnosis.diagnosis_type]
        priority = round((impact * 2) / effort, 4)
        tasks.append(
            OptimizationTaskV2(
                task_id=f"task:v2:{index}",
                title=diagnosis.recommended_action,
                diagnosis_id=diagnosis.diagnosis_id,
                owner_hint=OWNER_HINTS[diagnosis.diagnosis_type],
                impact=impact,
                effort=effort,
                priority_score=priority,
                evidence_ids=diagnosis.evidence_ids,
            )
        )
    return tuple(sorted(tasks, key=lambda item: (-item.priority_score, item.task_id)))

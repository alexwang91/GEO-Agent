"""Optimization outcome records for skill learning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


VALID_RESULTS = {"improved", "declined", "neutral", "inconclusive"}


@dataclass(frozen=True)
class OptimizationOutcomeRecord:
    engine: str
    query_type: str
    vertical: str
    action: str
    confidence: float
    result: str
    metric_delta: float
    evidence_package_id: str
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.engine:
            raise ValueError("engine is required")
        if not self.query_type:
            raise ValueError("query_type is required")
        if not self.vertical:
            raise ValueError("vertical is required")
        if not self.action:
            raise ValueError("action is required")
        if self.result not in VALID_RESULTS:
            raise ValueError(f"result must be one of: {', '.join(sorted(VALID_RESULTS))}")
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("confidence must be between 0 and 1")
        if not self.evidence_package_id:
            raise ValueError("evidence_package_id is required")

    def key(self) -> tuple[str, str, str, str]:
        return (self.engine, self.query_type, self.vertical, self.action)

    def to_dict(self) -> dict[str, object]:
        return {
            "engine": self.engine,
            "query_type": self.query_type,
            "vertical": self.vertical,
            "action": self.action,
            "confidence": self.confidence,
            "result": self.result,
            "metric_delta": self.metric_delta,
            "evidence_package_id": self.evidence_package_id,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class OptimizationOutcomeSummary:
    key: tuple[str, str, str, str]
    count: int
    improved_count: int
    declined_count: int
    neutral_count: int
    inconclusive_count: int
    average_delta: float
    average_confidence: float

    @property
    def success_rate(self) -> float:
        if not self.count:
            return 0.0
        return round(self.improved_count / self.count, 4)

    def to_dict(self) -> dict[str, object]:
        engine, query_type, vertical, action = self.key
        return {
            "engine": engine,
            "query_type": query_type,
            "vertical": vertical,
            "action": action,
            "count": self.count,
            "improved_count": self.improved_count,
            "declined_count": self.declined_count,
            "neutral_count": self.neutral_count,
            "inconclusive_count": self.inconclusive_count,
            "average_delta": self.average_delta,
            "average_confidence": self.average_confidence,
            "success_rate": self.success_rate,
        }


def summarize_outcomes(records: Iterable[OptimizationOutcomeRecord]) -> tuple[OptimizationOutcomeSummary, ...]:
    groups: dict[tuple[str, str, str, str], list[OptimizationOutcomeRecord]] = {}
    for record in records:
        groups.setdefault(record.key(), []).append(record)
    summaries = []
    for key in sorted(groups):
        group = groups[key]
        summaries.append(
            OptimizationOutcomeSummary(
                key=key,
                count=len(group),
                improved_count=sum(1 for record in group if record.result == "improved"),
                declined_count=sum(1 for record in group if record.result == "declined"),
                neutral_count=sum(1 for record in group if record.result == "neutral"),
                inconclusive_count=sum(1 for record in group if record.result == "inconclusive"),
                average_delta=round(sum(record.metric_delta for record in group) / len(group), 4),
                average_confidence=round(sum(record.confidence for record in group) / len(group), 4),
            )
        )
    return tuple(summaries)


def recommended_learning_actions(summary: OptimizationOutcomeSummary) -> tuple[str, ...]:
    actions: list[str] = []
    if summary.success_rate >= 0.5 and summary.average_delta > 0:
        actions.append("Promote this optimization pattern for similar query clusters.")
    if summary.declined_count > summary.improved_count:
        actions.append("Avoid repeating this optimization pattern until evidence quality improves.")
    if summary.inconclusive_count:
        actions.append("Collect another follow-up package before changing confidence for this pattern.")
    if not actions:
        actions.append("Keep this pattern in observation until more outcomes are recorded.")
    return tuple(actions)

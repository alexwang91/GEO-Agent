"""Skill-learning layer v2 for static optimization outcome signals."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SkillLearningSignal:
    signal_id: str
    source_task_id: str
    outcome: str
    metric_delta: float
    recommendation: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_learning_signal(signal_id: str, source_task_id: str, metric_delta: float) -> SkillLearningSignal:
    if metric_delta > 0:
        outcome = "positive"
        recommendation = "Promote this pattern into future task templates."
    elif metric_delta < 0:
        outcome = "negative"
        recommendation = "Review this pattern before reuse."
    else:
        outcome = "neutral"
        recommendation = "Keep as directional evidence only."
    return SkillLearningSignal(signal_id, source_task_id, outcome, metric_delta, recommendation)


def summarize_learning_signals(signals: tuple[SkillLearningSignal, ...] | list[SkillLearningSignal]) -> dict[str, int]:
    summary = {"positive": 0, "negative": 0, "neutral": 0}
    for signal in signals:
        summary[signal.outcome] += 1
    return summary

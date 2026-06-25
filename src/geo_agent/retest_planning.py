"""Retest planning workflow for baseline and follow-up audit packages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class RetestMetricDelta:
    name: str
    baseline: float
    follow_up: float
    delta: float

    @property
    def improved(self) -> bool:
        return self.delta > 0

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "baseline": self.baseline,
            "follow_up": self.follow_up,
            "delta": self.delta,
            "improved": self.improved,
        }


@dataclass(frozen=True)
class RetestComparison:
    metric_deltas: tuple[RetestMetricDelta, ...]
    resolved_missing_queries: tuple[str, ...]
    new_missing_queries: tuple[str, ...]
    competitor_deltas: dict[str, int]
    next_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "metric_deltas": [delta.to_dict() for delta in self.metric_deltas],
            "resolved_missing_queries": list(self.resolved_missing_queries),
            "new_missing_queries": list(self.new_missing_queries),
            "competitor_deltas": self.competitor_deltas.copy(),
            "next_actions": list(self.next_actions),
        }


def compare_retest_reports(baseline: Mapping[str, object], follow_up: Mapping[str, object]) -> RetestComparison:
    baseline_score = _mapping(baseline.get("score"), "baseline.score")
    follow_up_score = _mapping(follow_up.get("score"), "follow_up.score")
    metric_names = sorted(set(baseline_score) | set(follow_up_score))
    metric_deltas = tuple(
        RetestMetricDelta(
            name=name,
            baseline=_number(baseline_score.get(name)),
            follow_up=_number(follow_up_score.get(name)),
            delta=round(_number(follow_up_score.get(name)) - _number(baseline_score.get(name)), 4),
        )
        for name in metric_names
    )
    baseline_missing = set(_string_list(baseline.get("missing_queries")))
    follow_up_missing = set(_string_list(follow_up.get("missing_queries")))
    baseline_competitors = _int_map(baseline.get("competitor_map"))
    follow_up_competitors = _int_map(follow_up.get("competitor_map"))
    competitor_names = sorted(set(baseline_competitors) | set(follow_up_competitors))
    competitor_deltas = {
        name: follow_up_competitors.get(name, 0) - baseline_competitors.get(name, 0) for name in competitor_names
    }
    resolved = tuple(sorted(baseline_missing - follow_up_missing))
    new_missing = tuple(sorted(follow_up_missing - baseline_missing))
    return RetestComparison(
        metric_deltas=metric_deltas,
        resolved_missing_queries=resolved,
        new_missing_queries=new_missing,
        competitor_deltas=competitor_deltas,
        next_actions=_next_actions(metric_deltas, resolved, new_missing, competitor_deltas),
    )


def _next_actions(
    metric_deltas: tuple[RetestMetricDelta, ...],
    resolved: tuple[str, ...],
    new_missing: tuple[str, ...],
    competitor_deltas: dict[str, int],
) -> tuple[str, ...]:
    actions: list[str] = []
    if any(delta.improved for delta in metric_deltas):
        actions.append("Keep changes that improved visibility metrics and retest the same query set again.")
    if resolved:
        actions.append("Mark resolved missing queries as improved and preserve the evidence trail.")
    if new_missing:
        actions.append("Create optimization tasks for newly missing queries before the next retest.")
    if any(delta > 0 for delta in competitor_deltas.values()):
        actions.append("Review competitor gains and add comparison evidence to priority pages.")
    if not actions:
        actions.append("No measurable improvement detected; revisit evidence quality and rerun the baseline query set.")
    return tuple(actions)


def _mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be a mapping/object.")
    return value


def _number(value: object) -> float:
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, int) or isinstance(value, float):
        return float(value)
    return 0.0


def _string_list(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("expected a list of strings")
    return tuple(item for item in value if isinstance(item, str))


def _int_map(value: object) -> dict[str, int]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError("competitor_map must be a mapping/object.")
    return {str(key): int(count) for key, count in value.items() if isinstance(count, int)}

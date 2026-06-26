"""Retest plan v2 helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .optimization_tasks_v2 import OptimizationTaskV2


@dataclass(frozen=True)
class RetestPlanItemV2:
    task_id: str
    query_count: int
    sample_count: int
    provider_count: int
    earliest_retest_day: int
    success_condition: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_retest_plan_v2(tasks: tuple[OptimizationTaskV2, ...] | list[OptimizationTaskV2], *, base_queries: int = 10) -> tuple[RetestPlanItemV2, ...]:
    if base_queries <= 0:
        raise ValueError("base_queries must be positive")
    items = []
    for task in tasks:
        query_count = max(3, min(base_queries, task.impact * 3))
        sample_count = 3 if task.priority_score < 4 else 5
        provider_count = 1 if task.owner_hint == "ops" else 2
        earliest_day = max(7, task.effort * 7)
        items.append(RetestPlanItemV2(task.task_id, query_count, sample_count, provider_count, earliest_day, "metric improves beyond noise floor"))
    return tuple(sorted(items, key=lambda item: (item.earliest_retest_day, item.task_id)))

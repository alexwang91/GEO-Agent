"""Task owner mapping and export helpers."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict, dataclass

from .optimization_tasks_v2 import OptimizationTaskV2


@dataclass(frozen=True)
class TaskOwnerGroup:
    owner_hint: str
    tasks: tuple[OptimizationTaskV2, ...]

    def to_dict(self) -> dict[str, object]:
        return {"owner_hint": self.owner_hint, "tasks": [task.to_dict() for task in self.tasks]}


def group_tasks_by_owner(tasks: tuple[OptimizationTaskV2, ...] | list[OptimizationTaskV2]) -> tuple[TaskOwnerGroup, ...]:
    groups: dict[str, list[OptimizationTaskV2]] = {}
    for task in tasks:
        groups.setdefault(task.owner_hint, []).append(task)
    return tuple(TaskOwnerGroup(owner, tuple(sorted(values, key=lambda item: (-item.priority_score, item.task_id)))) for owner, values in sorted(groups.items()))


def export_tasks_json(tasks: tuple[OptimizationTaskV2, ...] | list[OptimizationTaskV2]) -> str:
    return json.dumps([task.to_dict() for task in tasks], sort_keys=True, indent=2)


def export_tasks_csv(tasks: tuple[OptimizationTaskV2, ...] | list[OptimizationTaskV2]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["task_id", "owner_hint", "priority_score", "impact", "effort", "diagnosis_id", "evidence_ids", "title"])
    writer.writeheader()
    for task in tasks:
        writer.writerow({
            "task_id": task.task_id,
            "owner_hint": task.owner_hint,
            "priority_score": task.priority_score,
            "impact": task.impact,
            "effort": task.effort,
            "diagnosis_id": task.diagnosis_id,
            "evidence_ids": ";".join(task.evidence_ids),
            "title": task.title,
        })
    return buffer.getvalue()

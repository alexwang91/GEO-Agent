from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExecutionBrief:
    task_id: str
    method: str
    target_page: str
    query_cluster: str
    evidence_ids: tuple[str, ...]
    expected_metric: str
    risk: str
    constraints: tuple[str, ...] = ("external_executor_required", "artifact_reference_only")

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["evidence_ids"] = list(self.evidence_ids)
        data["constraints"] = list(self.constraints)
        return data


@dataclass(frozen=True)
class PluginResult:
    plugin_name: str
    status: str
    artifact_ref: str
    claimed_method: str
    evidence_ids: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["evidence_ids"] = list(self.evidence_ids)
        data["warnings"] = list(self.warnings)
        return data


class ExecutorPlugin(Protocol):
    plugin_name: str

    def execute(self, brief: ExecutionBrief) -> PluginResult:
        ...


def build_execution_brief(task_plan: dict[str, object], *, task_id: str) -> ExecutionBrief:
    return ExecutionBrief(
        task_id=task_id,
        method=str(task_plan["method"]),
        target_page=str(task_plan["target_page"]),
        query_cluster=str(task_plan["query_cluster"]),
        evidence_ids=tuple(str(item) for item in task_plan.get("evidence_ids", ())),
        expected_metric=str(task_plan["expected_metric"]),
        risk=str(task_plan["risk"]),
    )


def run_plugin(plugin: ExecutorPlugin, brief: ExecutionBrief) -> PluginResult:
    result = plugin.execute(brief)
    if result.claimed_method != brief.method:
        raise ValueError("method mismatch")
    if not set(brief.evidence_ids).issubset(set(result.evidence_ids)):
        raise ValueError("missing evidence ids")
    if not result.artifact_ref:
        raise ValueError("artifact_ref is required")
    return result

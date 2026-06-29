"""Fixture-only interface for external flow tools."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FlowTaskInput:
    task_id: str
    method: str
    target_page: str
    query_cluster: str
    evidence_ids: tuple[str, ...]
    expected_metric: str

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["evidence_ids"] = list(self.evidence_ids)
        return data


@dataclass(frozen=True)
class FlowAnalyticsEvidence:
    source: str
    task_id: str
    crawler: str
    page_url: str
    ai_visit_count: int
    referring_engine: str
    observed_at: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def export_flow_input(task_plan: dict[str, object], *, task_id: str) -> dict[str, object]:
    return FlowTaskInput(
        task_id=task_id,
        method=str(task_plan["method"]),
        target_page=str(task_plan["target_page"]),
        query_cluster=str(task_plan["query_cluster"]),
        evidence_ids=tuple(str(item) for item in task_plan.get("evidence_ids", ())),
        expected_metric=str(task_plan["expected_metric"]),
    ).to_dict()


def import_flow_analytics(payload: dict[str, object]) -> FlowAnalyticsEvidence:
    return FlowAnalyticsEvidence(
        source="geoflow_fixture",
        task_id=str(payload["task_id"]),
        crawler=str(payload["crawler"]),
        page_url=str(payload["page_url"]),
        ai_visit_count=int(payload["ai_visit_count"]),
        referring_engine=str(payload["referring_engine"]),
        observed_at=str(payload["observed_at"]),
    )

from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any

@dataclass(frozen=True)
class ReportView:
    score: dict
    missing_queries: tuple[str, ...]
    competitor_map: dict[str, int]
    cited_sources: tuple[str, ...]
    failures: tuple[str, ...]
    recommended_actions: tuple[str, ...]
    retest_plan: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "missing_queries": list(self.missing_queries),
            "competitor_map": self.competitor_map.copy(),
            "cited_sources": list(self.cited_sources),
            "failures": list(self.failures),
            "recommended_actions": list(self.recommended_actions),
            "retest_plan": list(self.retest_plan),
        }


def build_report_view(score, *, missing_queries, competitor_mentions, cited_sources, diagnoses, tasks) -> ReportView:
    return ReportView(
        score=score.to_dict(),
        missing_queries=tuple(missing_queries),
        competitor_map=dict(sorted(competitor_mentions.items())),
        cited_sources=tuple(sorted(set(cited_sources))),
        failures=tuple(",".join(item.failure_types) for item in diagnoses),
        recommended_actions=tuple(item.action_type for item in tasks),
        retest_plan=tuple(item.retest_plan for item in tasks),
    )


def render_report_json(report: ReportView) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)


def render_report_markdown(report: ReportView) -> str:
    data = report.to_dict()
    lines = [
        "# GEO Agent Operational Report",
        "",
        "## Score",
        _bullets(data["score"]),
        "",
        "## Missing Queries",
        _list(data["missing_queries"]),
        "",
        "## Competitor Map",
        _bullets(data["competitor_map"]),
        "",
        "## Cited Sources",
        _list(data["cited_sources"]),
        "",
        "## Failures",
        _list(data["failures"]),
        "",
        "## Recommended Actions",
        _list(data["recommended_actions"]),
        "",
        "## Retest Plan",
        _list(data["retest_plan"]),
    ]
    return "\n".join(lines).rstrip() + "\n"


def _bullets(mapping: dict) -> str:
    if not mapping:
        return "- none"
    return "\n".join(f"- {key}: {value}" for key, value in mapping.items())


def _list(values: list[str]) -> str:
    if not values:
        return "- none"
    return "\n".join(f"- {value}" for value in values)

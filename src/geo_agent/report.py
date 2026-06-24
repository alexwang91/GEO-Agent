from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ReportView:
    score: dict
    missing_queries: tuple[str, ...]
    competitor_map: dict[str, int]
    cited_sources: tuple[str, ...]
    failures: tuple[str, ...]
    recommended_actions: tuple[str, ...]

def build_report_view(score, *, missing_queries, competitor_mentions, cited_sources, diagnoses, tasks) -> ReportView:
    return ReportView(
        score=score.to_dict(),
        missing_queries=tuple(missing_queries),
        competitor_map=dict(sorted(competitor_mentions.items())),
        cited_sources=tuple(sorted(set(cited_sources))),
        failures=tuple(",".join(item.failure_types) for item in diagnoses),
        recommended_actions=tuple(item.action_type for item in tasks),
    )

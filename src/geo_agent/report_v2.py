"""Report system v2 structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ReportSectionV2:
    title: str
    summary: str
    items: tuple[dict[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ReportV2:
    title: str
    sections: tuple[ReportSectionV2, ...]
    guardrails: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "sections": [section.to_dict() for section in self.sections],
            "guardrails": list(self.guardrails),
        }


def build_report_v2(metric_summary: dict[str, object], diagnoses: tuple[dict[str, object], ...], tasks: tuple[dict[str, object], ...], retests: tuple[dict[str, object], ...]) -> ReportV2:
    return ReportV2(
        "AI Visibility Audit Report",
        (
            ReportSectionV2("Metric Summary", "Visibility and evidence quality metrics.", (metric_summary,)),
            ReportSectionV2("Diagnoses", "Evidence-backed diagnosis records.", diagnoses),
            ReportSectionV2("Optimization Tasks", "Prioritized action plan.", tasks),
            ReportSectionV2("Retest Plan", "Follow-up measurement plan.", retests),
        ),
        ("Low-sample results are directional.", "Planned providers remain planned."),
    )

"""Report system v2 structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .bootstrap_stats import BootstrapSummary, bootstrap_mean_interval
from .engine_sampling import EngineRun
from .visibility_scoring import WeightedVisibilityScore, compute_visibility_components


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


def summarize_metric_samples(samples: dict[str, tuple[float, ...] | list[float]], *, seed: int = 13) -> dict[str, object]:
    summary: dict[str, object] = {}
    for name, values in samples.items():
        item = bootstrap_mean_interval(values, iterations=200, seed=seed).to_dict()
        item["interpretation"] = _interpretation(item)
        summary[name] = item
    return summary


def build_engine_component_summary(
    runs: tuple[EngineRun, ...] | list[EngineRun], *, brand: str, brand_domain: str, competitors: tuple[str, ...] = ()
) -> dict[str, object]:
    """Summarize visibility by engine before showing aggregate direction."""

    engines = sorted({run.engine for run in runs})
    return {
        "summary_type": "per_engine_component_breakdown",
        "primary_interpretation": "engine_breakdown_first",
        "aggregate_label": "directional_not_verdict",
        "aggregate_warning": "A single aggregate score can hide engine-level differences; use it only as directional context.",
        "engines": [_engine_item(engine, tuple(run for run in runs if run.engine == engine), brand, brand_domain, competitors) for engine in engines],
    }


def build_report_v2(
    metric_summary: dict[str, object], diagnoses: tuple[dict[str, object], ...], tasks: tuple[dict[str, object], ...], retests: tuple[dict[str, object], ...]
) -> ReportV2:
    return ReportV2(
        "AI Visibility Audit Report",
        (
            ReportSectionV2("Metric Summary", "Visibility and evidence quality metrics with sample directionality.", (metric_summary,)),
            ReportSectionV2("Diagnoses", "Evidence-backed diagnosis records.", diagnoses),
            ReportSectionV2("Optimization Tasks", "Prioritized action plan.", tasks),
            ReportSectionV2("Retest Plan", "Follow-up measurement plan.", retests),
        ),
        ("Low-sample results are directional.", "Deltas below the noise floor are inconclusive.", "Planned providers remain planned."),
    )


def build_report_v2_from_runs(
    runs: tuple[EngineRun, ...] | list[EngineRun], *, brand: str, brand_domain: str, score: WeightedVisibilityScore, competitors: tuple[str, ...] = (), diagnoses: tuple[dict[str, object], ...] = (), tasks: tuple[dict[str, object], ...] = (), retests: tuple[dict[str, object], ...] = ()
) -> ReportV2:
    engine_summary = build_engine_component_summary(runs, brand=brand, brand_domain=brand_domain, competitors=competitors)
    metric_summary = {
        "aggregate_score": {
            "value": score.aggregate_score,
            "label": "directional_not_verdict",
            "interpretation": "directional context only; inspect per-engine components first",
        },
        "components": score.components.to_dict(),
        "per_engine": engine_summary,
    }
    return ReportV2(
        "AI Visibility Audit Report",
        (
            ReportSectionV2("Per-Engine Breakdown", "Per-engine component metrics lead the report.", (engine_summary,)),
            ReportSectionV2("Directional Aggregate", "Single aggregate score is directional context, not a verdict.", (metric_summary,)),
            ReportSectionV2("Diagnoses", "Evidence-backed diagnosis records.", diagnoses),
            ReportSectionV2("Optimization Tasks", "Prioritized action plan.", tasks),
            ReportSectionV2("Retest Plan", "Follow-up measurement plan.", retests),
        ),
        (
            "Per-engine component results lead the report.",
            "A single aggregate score is directional, not a verdict.",
            "Low-sample results are directional.",
            "Deltas below the noise floor are inconclusive.",
            "Planned providers remain planned.",
        ),
    )


def compare_metric_delta(before: BootstrapSummary, after: BootstrapSummary) -> dict[str, object]:
    delta = round(after.mean - before.mean, 4)
    noise_floor = round(max(before.noise_floor, after.noise_floor), 4)
    return {
        "before": before.to_dict(),
        "after": after.to_dict(),
        "delta": delta,
        "noise_floor": noise_floor,
        "conclusion": "inconclusive_below_noise_floor" if abs(delta) <= noise_floor else "directional_change",
    }


def _engine_item(engine: str, runs: tuple[EngineRun, ...], brand: str, brand_domain: str, competitors: tuple[str, ...]) -> dict[str, object]:
    components = compute_visibility_components(list(runs), brand=brand, brand_domain=brand_domain, competitors=competitors)
    return {
        "engine": engine,
        "sample_count": len(runs),
        "components": {
            "mention_share": components.mention_share,
            "owned_citation_share": components.citation_share,
            "recommendation_share": components.recommendation_share,
            "competitor_only_share": components.competitor_only_share,
        },
        "directionality": "directional_low_sample" if len(runs) < 10 else "directional",
    }


def _interpretation(item: dict[str, object]) -> str:
    directionality = str(item.get("directionality", ""))
    if directionality == "directional_low_sample":
        return "single or low-sample result; treat as directional only"
    if directionality == "directional":
        return "directional repeated-sample estimate"
    return "stable repeated-sample estimate"

"""End-to-end fixture audit runner for GEO Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .engine_sampling import EngineAdapter, EngineRun, sample_with_adapter
from .entity_profile import EntityProfile
from .evidence_store import EvidenceStore
from .failure_debugger import FailureDiagnosis, diagnose_failure_v2
from .optimization_tasks import OptimizationTaskBrief, generate_task_brief
from .page_inventory import PageInventoryRecord, StaticPageFetcher, crawl_inventory
from .query_space import QueryRecord, build_query_space
from .report import ReportView, build_report_view, render_report_json, render_report_markdown
from .visibility_scoring import WeightedVisibilityScore, score_weighted_visibility


@dataclass(frozen=True)
class AuditArtifacts:
    profile: EntityProfile
    queries: tuple[QueryRecord, ...]
    pages: tuple[PageInventoryRecord, ...]
    runs: tuple[EngineRun, ...]
    score: WeightedVisibilityScore
    diagnoses: tuple[FailureDiagnosis, ...]
    tasks: tuple[OptimizationTaskBrief, ...]
    report: ReportView
    report_json: str
    report_markdown: str

    def to_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile.to_dict(),
            "queries": [query.to_dict() for query in self.queries],
            "pages": [page.to_dict() for page in self.pages],
            "runs": [run.to_dict() for run in self.runs],
            "score": self.score.to_dict(),
            "diagnoses": [diagnosis.__dict__.copy() for diagnosis in self.diagnoses],
            "tasks": [task.__dict__.copy() for task in self.tasks],
            "report": self.report.to_dict(),
        }


class AuditRunner:
    """Runs a deterministic audit from fixture evidence without live engine claims."""

    def __init__(self, store: EvidenceStore | None = None) -> None:
        self.store = store or EvidenceStore()

    def run(
        self,
        profile: EntityProfile,
        *,
        pages: Mapping[str, str],
        engine_adapter: EngineAdapter,
        sitemap_urls: list[str] | None = None,
        manual_urls: list[str] | None = None,
        max_queries: int | None = None,
    ) -> AuditArtifacts:
        queries = tuple(build_query_space(profile, target_engines=(engine_adapter.engine,), max_queries=max_queries))
        page_records = tuple(
            crawl_inventory(StaticPageFetcher(dict(pages)), sitemap_urls=sitemap_urls, manual_urls=manual_urls)
        )
        runs = tuple(
            sample_with_adapter(
                engine_adapter,
                query.query,
                region=query.region,
                language=query.language,
            )
            for query in queries
        )
        self.store.save_runs(runs)
        score = score_weighted_visibility(
            list(runs),
            brand=profile.brand,
            brand_domain=profile.domain,
            competitors=profile.competitors,
        )
        diagnoses = tuple(
            diagnose_failure_v2(
                run,
                query,
                pages=page_records,
                brand=profile.brand,
                brand_domain=profile.domain,
                competitors=profile.competitors,
            )
            for run, query in zip(runs, queries)
        )
        target_page = _first_page_url(page_records, profile)
        tasks = tuple(generate_task_brief(query, diagnosis, target_page=target_page) for query, diagnosis in zip(queries, diagnoses))
        report = build_report_view(
            score,
            missing_queries=[query.query for query, run in zip(queries, runs) if not _has_brand(run, profile.brand)],
            competitor_mentions=_competitor_mentions(runs, profile.competitors),
            cited_sources=[domain for run in runs for domain in run.source_domains],
            diagnoses=diagnoses,
            tasks=tasks,
        )
        return AuditArtifacts(
            profile=profile,
            queries=queries,
            pages=page_records,
            runs=runs,
            score=score,
            diagnoses=diagnoses,
            tasks=tasks,
            report=report,
            report_json=render_report_json(report),
            report_markdown=render_report_markdown(report),
        )


def _first_page_url(pages: tuple[PageInventoryRecord, ...], profile: EntityProfile) -> str:
    if pages:
        return pages[0].canonical_url
    return f"https://{profile.domain}/"


def _has_brand(run: EngineRun, brand: str) -> bool:
    name = brand.lower()
    return name in run.raw_answer.lower() or name in {item.lower() for item in run.mentions}


def _competitor_mentions(runs: tuple[EngineRun, ...], competitors: tuple[str, ...]) -> dict[str, int]:
    counts = {competitor: 0 for competitor in competitors}
    for run in runs:
        answer = run.raw_answer.lower()
        for competitor in competitors:
            if competitor.lower() in answer:
                counts[competitor] += 1
    return {competitor: count for competitor, count in counts.items() if count}

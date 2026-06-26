"""Evidence graph schema for traceable AI visibility audits."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from .engine_sampling import EngineRun
from .failure_debugger import FailureDiagnosis
from .optimization_tasks import OptimizationTaskBrief
from .page_inventory import PageInventoryRecord
from .query_space import QueryRecord
from .visibility_scoring import WeightedVisibilityScore


@dataclass(frozen=True)
class AuditRun:
    audit_id: str
    brand: str
    domain: str
    engine_ids: tuple[str, ...]
    sample_ids: tuple[str, ...]
    prompt_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class PromptRecord:
    prompt_id: str
    query: str
    cluster: str
    intent_type: str
    funnel_stage: str
    language: str
    region: str
    target_engine: str

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class EngineSample:
    sample_id: str
    prompt_id: str
    engine: str
    query: str
    timestamp: str
    region: str
    language: str
    raw_answer: str
    citation_ids: tuple[str, ...]
    mention_ids: tuple[str, ...]
    recommendation_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class CitationRecord:
    citation_id: str
    sample_id: str
    prompt_id: str
    url: str
    domain: str
    position: int

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class MentionRecord:
    mention_id: str
    sample_id: str
    prompt_id: str
    text: str
    position: int

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class RecommendationRecord:
    recommendation_id: str
    sample_id: str
    prompt_id: str
    text: str
    position: int

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class PageSnapshot:
    page_id: str
    url: str
    canonical_url: str
    title: str | None
    h1: str | None
    schema_types: tuple[str, ...]
    content_chunk_count: int

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    sample_id: str
    prompt_id: str
    text: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class DiagnosisRecord:
    diagnosis_id: str
    prompt_id: str
    sample_id: str
    failure_types: tuple[str, ...]
    explanation: str
    next_step: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class OptimizationTask:
    task_id: str
    diagnosis_id: str
    prompt_id: str
    sample_id: str
    action_type: str
    target_page: str
    query_cluster: str
    expected_impact: str
    confidence: float
    risk: str
    retest_plan: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class RetestRecord:
    retest_id: str
    baseline_sample_ids: tuple[str, ...]
    prompt_ids: tuple[str, ...]
    engine_ids: tuple[str, ...]
    status: str = "planned"

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class SkillOutcomeRecord:
    outcome_id: str
    task_id: str
    result_label: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class MetricTrace:
    metric_id: str
    name: str
    value: float
    sample_ids: tuple[str, ...]
    prompt_ids: tuple[str, ...]
    citation_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return _asdict(self)


@dataclass(frozen=True)
class EvidenceGraph:
    audit_run: AuditRun
    prompts: tuple[PromptRecord, ...]
    samples: tuple[EngineSample, ...]
    citations: tuple[CitationRecord, ...]
    mentions: tuple[MentionRecord, ...]
    recommendations: tuple[RecommendationRecord, ...]
    pages: tuple[PageSnapshot, ...]
    claims: tuple[ClaimRecord, ...]
    diagnoses: tuple[DiagnosisRecord, ...]
    tasks: tuple[OptimizationTask, ...]
    retests: tuple[RetestRecord, ...]
    skill_outcomes: tuple[SkillOutcomeRecord, ...]
    metrics: tuple[MetricTrace, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "audit_run": self.audit_run.to_dict(),
            "prompts": [item.to_dict() for item in self.prompts],
            "samples": [item.to_dict() for item in self.samples],
            "citations": [item.to_dict() for item in self.citations],
            "mentions": [item.to_dict() for item in self.mentions],
            "recommendations": [item.to_dict() for item in self.recommendations],
            "pages": [item.to_dict() for item in self.pages],
            "claims": [item.to_dict() for item in self.claims],
            "diagnoses": [item.to_dict() for item in self.diagnoses],
            "tasks": [item.to_dict() for item in self.tasks],
            "retests": [item.to_dict() for item in self.retests],
            "skill_outcomes": [item.to_dict() for item in self.skill_outcomes],
            "metrics": [item.to_dict() for item in self.metrics],
        }


def build_evidence_graph(
    *,
    brand: str,
    domain: str,
    queries: tuple[QueryRecord, ...],
    pages: tuple[PageInventoryRecord, ...],
    runs: tuple[EngineRun, ...],
    score: WeightedVisibilityScore,
    diagnoses: tuple[FailureDiagnosis, ...],
    tasks: tuple[OptimizationTaskBrief, ...],
) -> EvidenceGraph:
    prompt_records = tuple(_prompt_record(index, query) for index, query in enumerate(queries, start=1))
    prompt_ids = tuple(prompt.prompt_id for prompt in prompt_records)

    citation_records: list[CitationRecord] = []
    mention_records: list[MentionRecord] = []
    recommendation_records: list[RecommendationRecord] = []
    sample_records: list[EngineSample] = []
    claim_records: list[ClaimRecord] = []

    for index, run in enumerate(runs, start=1):
        prompt_id = prompt_ids[index - 1]
        sample_id = _id("sample", index)
        citations = tuple(
            CitationRecord(_id("citation", index, position), sample_id, prompt_id, url, _domain(url), position)
            for position, url in enumerate(run.citations, start=1)
        )
        mentions = tuple(
            MentionRecord(_id("mention", index, position), sample_id, prompt_id, text, position)
            for position, text in enumerate(run.mentions, start=1)
        )
        recommendations = tuple(
            RecommendationRecord(_id("recommendation", index, position), sample_id, prompt_id, text, position)
            for position, text in enumerate(run.recommendations, start=1)
        )
        citation_records.extend(citations)
        mention_records.extend(mentions)
        recommendation_records.extend(recommendations)
        sample_records.append(
            EngineSample(
                sample_id,
                prompt_id,
                run.engine,
                run.query,
                run.timestamp,
                run.region,
                run.language,
                run.raw_answer,
                tuple(item.citation_id for item in citations),
                tuple(item.mention_id for item in mentions),
                tuple(item.recommendation_id for item in recommendations),
            )
        )
        if run.raw_answer.strip():
            claim_records.append(ClaimRecord(_id("claim", index), sample_id, prompt_id, run.raw_answer, (sample_id,)))

    sample_ids = tuple(sample.sample_id for sample in sample_records)
    page_records = tuple(_page_snapshot(index, page) for index, page in enumerate(pages, start=1))
    diagnosis_records = tuple(
        _diagnosis_record(index, diagnosis, prompt_ids, sample_ids)
        for index, diagnosis in enumerate(diagnoses, start=1)
    )
    task_records = tuple(
        _task_record(index, task, diagnosis_records, prompt_ids, sample_ids)
        for index, task in enumerate(tasks, start=1)
    )
    retests = (RetestRecord(_id("retest", 1), sample_ids, prompt_ids, tuple(sorted({run.engine for run in runs}))),)
    metrics = _metric_traces(score, sample_ids, prompt_ids, tuple(item.citation_id for item in citation_records))
    audit = AuditRun(_id("audit", brand, domain), brand, domain, tuple(sorted({run.engine for run in runs})), sample_ids, prompt_ids)
    return EvidenceGraph(
        audit,
        prompt_records,
        tuple(sample_records),
        tuple(citation_records),
        tuple(mention_records),
        tuple(recommendation_records),
        page_records,
        tuple(claim_records),
        diagnosis_records,
        task_records,
        retests,
        (),
        metrics,
    )


def _prompt_record(index: int, query: QueryRecord) -> PromptRecord:
    return PromptRecord(
        _id("prompt", index),
        query.query,
        query.cluster,
        query.intent_type,
        query.funnel_stage,
        query.language,
        query.region,
        query.target_engine,
    )


def _page_snapshot(index: int, page: PageInventoryRecord) -> PageSnapshot:
    return PageSnapshot(
        _id("page", index),
        page.url,
        page.canonical_url,
        page.title,
        page.h1,
        page.schema_types,
        len(page.content_chunks),
    )


def _diagnosis_record(index: int, diagnosis: FailureDiagnosis, prompt_ids: tuple[str, ...], sample_ids: tuple[str, ...]) -> DiagnosisRecord:
    prompt_id = prompt_ids[index - 1] if index <= len(prompt_ids) else ""
    sample_id = sample_ids[index - 1] if index <= len(sample_ids) else ""
    evidence_ids = tuple(item for item in (prompt_id, sample_id, *diagnosis.evidence) if item)
    return DiagnosisRecord(_id("diagnosis", index), prompt_id, sample_id, diagnosis.failure_types, diagnosis.explanation, diagnosis.next_step, evidence_ids)


def _task_record(index: int, task: OptimizationTaskBrief, diagnoses: tuple[DiagnosisRecord, ...], prompt_ids: tuple[str, ...], sample_ids: tuple[str, ...]) -> OptimizationTask:
    diagnosis = diagnoses[index - 1] if index <= len(diagnoses) else None
    prompt_id = prompt_ids[index - 1] if index <= len(prompt_ids) else ""
    sample_id = sample_ids[index - 1] if index <= len(sample_ids) else ""
    diagnosis_id = diagnosis.diagnosis_id if diagnosis else ""
    evidence_ids = tuple(item for item in (diagnosis_id, prompt_id, sample_id) if item)
    return OptimizationTask(
        _id("task", index),
        diagnosis_id,
        prompt_id,
        sample_id,
        task.action_type,
        task.target_page,
        task.query_cluster,
        task.expected_impact,
        task.confidence,
        task.risk,
        task.retest_plan,
        evidence_ids,
    )


def _metric_traces(score: WeightedVisibilityScore, sample_ids: tuple[str, ...], prompt_ids: tuple[str, ...], citation_ids: tuple[str, ...]) -> tuple[MetricTrace, ...]:
    values = {"aggregate_score": score.aggregate_score, **score.components.to_dict()}
    return tuple(MetricTrace(_id("metric", name), name, float(value), sample_ids, prompt_ids, citation_ids) for name, value in values.items())


def _id(prefix: str, *parts: object) -> str:
    safe = "-".join(str(part).strip().lower().replace(" ", "-").replace(":", "-") for part in parts if str(part).strip())
    return f"{prefix}:{safe}" if safe else prefix


def _domain(value: str) -> str:
    return (urlparse(value).hostname or "").removeprefix("www.")


def _asdict(record: object) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in record.__dict__.items():
        result[key] = list(value) if isinstance(value, tuple) else value
    return result

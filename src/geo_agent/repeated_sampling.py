"""Repeated sampling plan records and probability summaries for reproducible GEO audits."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass

from .bootstrap_stats import bootstrap_mean_interval
from .engine_sampling import EngineRun
from .entity_resolution import has_entity


@dataclass(frozen=True)
class SamplingPlanItem:
    query: str
    provider_id: str
    sample_index: int
    seed: int
    time_window: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RepeatedSamplingPlan:
    plan_id: str
    sample_count: int
    items: tuple[SamplingPlanItem, ...]
    directionality: str

    def to_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "sample_count": self.sample_count,
            "items": [item.to_dict() for item in self.items],
            "directionality": self.directionality,
        }


@dataclass(frozen=True)
class RepeatedSamplingSummary:
    engine: str
    query_cluster: str
    sample_count: int
    positive_count: int
    probability: float
    lower: float
    upper: float
    confidence_label: str
    collection_method: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_repeated_sampling_plan(
    queries: tuple[str, ...] | list[str],
    provider_ids: tuple[str, ...] | list[str],
    *,
    sample_count: int,
    seed: int,
    time_window: str = "single_run",
) -> RepeatedSamplingPlan:
    if sample_count <= 0:
        raise ValueError("sample_count must be positive")
    if not queries or not provider_ids:
        raise ValueError("queries and provider_ids are required")
    items = []
    for query in queries:
        for provider_id in provider_ids:
            for sample_index in range(sample_count):
                item_seed = _stable_seed(seed, query, provider_id, sample_index)
                items.append(SamplingPlanItem(query, provider_id, sample_index + 1, item_seed, time_window))
    plan_id = _plan_id(queries, provider_ids, sample_count, seed, time_window)
    return RepeatedSamplingPlan(plan_id, sample_count, tuple(items), _directionality(sample_count))


def summarize_brand_probability(
    runs: tuple[EngineRun, ...] | list[EngineRun], *, brand: str, query_cluster: str, collection_method: str = "manual_or_recorded"
) -> RepeatedSamplingSummary:
    if not runs:
        raise ValueError("runs are required")
    engines = {run.engine for run in runs}
    engine = next(iter(engines)) if len(engines) == 1 else "multi_engine"
    values = tuple(1.0 if _has_brand(run, brand) else 0.0 for run in runs)
    interval = bootstrap_mean_interval(values, iterations=200, seed=17)
    return RepeatedSamplingSummary(
        engine=engine,
        query_cluster=query_cluster,
        sample_count=interval.sample_count,
        positive_count=int(sum(values)),
        probability=interval.mean,
        lower=interval.lower,
        upper=interval.upper,
        confidence_label=interval.directionality,
        collection_method=collection_method,
    )


def _has_brand(run: EngineRun, brand: str) -> bool:
    return has_entity(run.raw_answer, brand) or any(has_entity(item, brand) for item in run.mentions)


def _stable_seed(seed: int, query: str, provider_id: str, sample_index: int) -> int:
    digest = hashlib.sha256(f"{seed}|{query}|{provider_id}|{sample_index}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _plan_id(queries, provider_ids, sample_count: int, seed: int, time_window: str) -> str:
    payload = "|".join([*queries, *provider_ids, str(sample_count), str(seed), time_window])
    return "sampling:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def _directionality(sample_count: int) -> str:
    if sample_count < 3:
        return "directional_low_sample"
    if sample_count < 10:
        return "directional"
    return "stable"

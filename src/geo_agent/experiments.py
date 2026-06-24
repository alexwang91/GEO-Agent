from __future__ import annotations
from dataclasses import dataclass
from .query_space import QueryRecord

@dataclass(frozen=True)
class ExperimentPlan:
    train_clusters: tuple[str, ...]
    validation_clusters: tuple[str, ...]
    holdout_clusters: tuple[str, ...]
    retest_pairs: tuple[tuple[str, str, str, str], ...]

def create_experiment_plan(records: list[QueryRecord], *, holdout_ratio: float = 0.25) -> ExperimentPlan:
    clusters = sorted({record.cluster for record in records})
    holdout_count = max(1, int(len(clusters) * holdout_ratio)) if clusters else 0
    holdout = tuple(clusters[-holdout_count:]) if holdout_count else tuple()
    remaining = [cluster for cluster in clusters if cluster not in holdout]
    split = max(1, len(remaining) // 2) if remaining else 0
    train = tuple(remaining[:split])
    validation = tuple(remaining[split:])
    assert set(train).isdisjoint(holdout)
    assert set(validation).isdisjoint(holdout)
    pairs = tuple((record.cluster, record.target_engine, record.language, record.region) for record in records)
    return ExperimentPlan(train, validation, holdout, pairs)

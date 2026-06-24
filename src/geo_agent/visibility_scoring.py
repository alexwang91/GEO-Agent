from __future__ import annotations
from dataclasses import dataclass
from .engine_sampling import EngineRun

@dataclass(frozen=True)
class VisibilityScore:
    mention_share: float
    citation_share: float
    recommendation_share: float
    average_answer_rank: float
    source_diversity: int
    query_coverage: float

    def to_dict(self):
        return self.__dict__.copy()

def score_visibility(runs: list[EngineRun], *, brand: str, brand_domain: str) -> VisibilityScore:
    if not runs:
        return VisibilityScore(0.0, 0.0, 0.0, 0.0, 0, 0.0)
    name = brand.lower()
    m = [r for r in runs if name in r.raw_answer.lower() or name in {x.lower() for x in r.mentions}]
    c = [r for r in runs if any(brand_domain in d for d in r.source_domains)]
    rec = [r for r in runs if name in {x.lower() for x in r.recommendations}]
    domains = {d for r in runs for d in r.source_domains}
    answered = [r for r in runs if r.raw_answer.strip()]
    total = len(runs)
    return VisibilityScore(round(len(m)/total, 4), round(len(c)/total, 4), round(len(rec)/total, 4), _avg_rank(m, brand), len(domains), round(len(answered)/total, 4))

def _avg_rank(runs: list[EngineRun], brand: str) -> float:
    ranks = []
    for run in runs:
        index = run.raw_answer.lower().find(brand.lower())
        if index >= 0:
            ranks.append(1 / (1 + index))
    return round(sum(ranks) / len(ranks), 4) if ranks else 0.0

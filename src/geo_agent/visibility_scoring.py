from __future__ import annotations
from dataclasses import dataclass
from .engine_sampling import EngineRun
from .entity_resolution import domain_matches, find_entity_matches, has_entity

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

@dataclass(frozen=True)
class VisibilityComponents:
    mention_share: float
    citation_share: float
    recommendation_share: float
    answer_rank_score: float
    source_diversity_score: float
    query_coverage: float
    competitor_only_share: float

    def to_dict(self):
        return self.__dict__.copy()

@dataclass(frozen=True)
class WeightedVisibilityScore:
    aggregate_score: float
    components: VisibilityComponents
    weights: dict[str, float]

    def to_dict(self):
        return {"aggregate_score": self.aggregate_score, "components": self.components.to_dict(), "weights": self.weights.copy()}

DEFAULT_WEIGHTS = {
    "mention_share": 0.22,
    "citation_share": 0.22,
    "recommendation_share": 0.18,
    "answer_rank_score": 0.14,
    "source_diversity_score": 0.12,
    "query_coverage": 0.12,
}


def score_visibility(runs: list[EngineRun], *, brand: str, brand_domain: str) -> VisibilityScore:
    components = compute_visibility_components(runs, brand=brand, brand_domain=brand_domain)
    avg_rank = _legacy_avg_rank(runs, brand)
    domains = {d for r in runs for d in r.source_domains}
    return VisibilityScore(
        mention_share=components.mention_share,
        citation_share=components.citation_share,
        recommendation_share=components.recommendation_share,
        average_answer_rank=avg_rank,
        source_diversity=len(domains),
        query_coverage=components.query_coverage,
    )


def score_weighted_visibility(
    runs: list[EngineRun], *, brand: str, brand_domain: str, competitors: tuple[str, ...] = (), weights: dict[str, float] | None = None
) -> WeightedVisibilityScore:
    active_weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    components = compute_visibility_components(runs, brand=brand, brand_domain=brand_domain, competitors=competitors)
    total_weight = sum(active_weights.values()) or 1.0
    value = sum(getattr(components, name) * weight for name, weight in active_weights.items()) / total_weight
    penalty = components.competitor_only_share * 0.15
    return WeightedVisibilityScore(round(max(value - penalty, 0.0), 4), components, active_weights)


def compute_visibility_components(
    runs: list[EngineRun], *, brand: str, brand_domain: str, competitors: tuple[str, ...] = ()
) -> VisibilityComponents:
    if not runs:
        return VisibilityComponents(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    total = len(runs)
    mentioned = [run for run in runs if _has_brand(run, brand)]
    cited = [run for run in runs if any(domain_matches(domain, brand_domain) for domain in run.source_domains)]
    recommended = [run for run in runs if any(_same_entity(item, brand) for item in run.recommendations)]
    answered = [run for run in runs if run.raw_answer.strip()]
    competitor_only = [run for run in runs if not _has_brand(run, brand) and any(has_entity(run.raw_answer, item) for item in competitors)]
    return VisibilityComponents(
        mention_share=round(len(mentioned) / total, 4),
        citation_share=round(len(cited) / total, 4),
        recommendation_share=round(len(recommended) / total, 4),
        answer_rank_score=_answer_rank_score(mentioned, brand),
        source_diversity_score=_source_diversity_score({domain for run in runs for domain in run.source_domains}),
        query_coverage=round(len(answered) / total, 4),
        competitor_only_share=round(len(competitor_only) / total, 4),
    )


def _has_brand(run: EngineRun, name: str) -> bool:
    return has_entity(run.raw_answer, name) or any(_same_entity(item, name) for item in run.mentions)


def _same_entity(value: str, name: str) -> bool:
    return has_entity(value, name)


def _answer_rank_score(runs: list[EngineRun], brand: str) -> float:
    if not runs:
        return 0.0
    scores = []
    for run in runs:
        matches = find_entity_matches(run.raw_answer, brand)
        index = matches[0].start if matches else -1
        scores.append(0.0 if index < 0 else min(1.0, 1 / (1 + index / 20)))
    return round(sum(scores) / len(scores), 4)



def _source_diversity_score(domains: set[str]) -> float:
    return round(min(len(domains) / 5, 1.0), 4)



def _legacy_avg_rank(runs: list[EngineRun], brand: str) -> float:
    ranks = []
    for run in runs:
        matches = find_entity_matches(run.raw_answer, brand)
        if matches:
            ranks.append(1 / (1 + matches[0].start))
    return round(sum(ranks) / len(ranks), 4) if ranks else 0.0

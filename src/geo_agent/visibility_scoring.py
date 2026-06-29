from __future__ import annotations
import re
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
    position_adjusted_word_count: float = 0.0
    subjective_impression_score: float = 0.0

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
    "mention_share": 0.20,
    "citation_share": 0.20,
    "recommendation_share": 0.16,
    "answer_rank_score": 0.10,
    "subjective_impression_score": 0.10,
    "source_diversity_score": 0.12,
    "query_coverage": 0.12,
}


_WORD_RE = re.compile(r"[\wÀ-ÖØ-öø-ÿ]+")
_SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?")


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
        answer_rank_score=_answer_rank_score(runs, brand),
        source_diversity_score=_source_diversity_score({domain for run in runs for domain in run.source_domains}),
        query_coverage=round(len(answered) / total, 4),
        competitor_only_share=round(len(competitor_only) / total, 4),
        position_adjusted_word_count=_position_adjusted_word_count_average(runs, brand),
        subjective_impression_score=_subjective_impression_score(runs, brand, brand_domain),
    )


def _has_brand(run: EngineRun, name: str) -> bool:
    return has_entity(run.raw_answer, name) or any(_same_entity(item, name) for item in run.mentions)


def _same_entity(value: str, name: str) -> bool:
    return has_entity(value, name)


def _answer_rank_score(runs: list[EngineRun], brand: str) -> float:
    if not runs:
        return 0.0
    scores = [_position_adjusted_visibility_score(run, brand) for run in runs]
    return round(sum(scores) / len(scores), 4)


def _position_adjusted_word_count_average(runs: list[EngineRun], brand: str) -> float:
    if not runs:
        return 0.0
    values = [_position_adjusted_word_count(run.raw_answer, brand) for run in runs]
    return round(sum(values) / len(values), 4)


def _position_adjusted_visibility_score(run: EngineRun, brand: str) -> float:
    words = _words(run.raw_answer)
    if not words:
        return 0.0
    return round(min(_position_adjusted_word_count(run.raw_answer, brand) / len(words), 1.0), 4)


def _position_adjusted_word_count(text: str, brand: str) -> float:
    """Count brand-bearing answer words with earlier sentences receiving more weight."""

    if not text.strip() or not brand.strip():
        return 0.0
    adjusted = 0.0
    for index, sentence in enumerate(_sentences(text), start=1):
        if has_entity(sentence, brand):
            adjusted += len(_words(sentence)) / index
    return round(adjusted, 4)


def _subjective_impression_score(runs: list[EngineRun], brand: str, brand_domain: str) -> float:
    if not runs:
        return 0.0
    values = [_subjective_impression_for_run(run, brand, brand_domain) for run in runs]
    return round(sum(values) / len(values), 4)


def _subjective_impression_for_run(run: EngineRun, brand: str, brand_domain: str) -> float:
    mention = 1.0 if _has_brand(run, brand) else 0.0
    citation = 1.0 if any(domain_matches(domain, brand_domain) for domain in run.source_domains) else 0.0
    recommendation = 1.0 if any(_same_entity(item, brand) for item in run.recommendations) else 0.0
    prominence = _position_adjusted_visibility_score(run, brand)
    return round(min(mention * 0.4 + citation * 0.25 + recommendation * 0.2 + prominence * 0.15, 1.0), 4)


def _sentences(text: str) -> tuple[str, ...]:
    return tuple(sentence.strip() for sentence in _SENTENCE_RE.findall(text) if sentence.strip())


def _words(text: str) -> tuple[str, ...]:
    return tuple(match.group(0) for match in _WORD_RE.finditer(text))


def _source_diversity_score(domains: set[str]) -> float:
    return round(min(len(domains) / 5, 1.0), 4)


def _legacy_avg_rank(runs: list[EngineRun], brand: str) -> float:
    ranks = []
    for run in runs:
        matches = find_entity_matches(run.raw_answer, brand)
        if matches:
            ranks.append(1 / (1 + matches[0].start))
    return round(sum(ranks) / len(ranks), 4) if ranks else 0.0

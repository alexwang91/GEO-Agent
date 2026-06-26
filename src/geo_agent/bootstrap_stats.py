"""Bootstrap confidence intervals and noise-floor helpers."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BootstrapSummary:
    mean: float
    lower: float
    upper: float
    noise_floor: float
    sample_count: int
    directionality: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def bootstrap_mean_interval(values: tuple[float, ...] | list[float], *, iterations: int = 1000, seed: int = 13, confidence: float = 0.95) -> BootstrapSummary:
    if not values:
        raise ValueError("values are required")
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    data = [float(value) for value in values]
    rng = random.Random(seed)
    estimates = []
    for _ in range(iterations):
        sample = [rng.choice(data) for _ in data]
        estimates.append(sum(sample) / len(sample))
    estimates.sort()
    alpha = (1 - confidence) / 2
    lower = estimates[int(alpha * (iterations - 1))]
    upper = estimates[int((1 - alpha) * (iterations - 1))]
    mean = sum(data) / len(data)
    return BootstrapSummary(round(mean, 4), round(lower, 4), round(upper, 4), round(upper - lower, 4), len(data), _directionality(len(data)))


def _directionality(sample_count: int) -> str:
    if sample_count < 3:
        return "directional_low_sample"
    if sample_count < 10:
        return "directional"
    return "stable"

"""Retest comparison stats and attribution helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

ChangeStatus = Literal["improved", "regressed", "unchanged"]


@dataclass(frozen=True)
class RetestComparisonV2:
    metric_name: str
    before: float
    after: float
    delta: float
    noise_floor: float
    status: ChangeStatus
    attribution: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def compare_retest_metric(metric_name: str, before: float, after: float, *, noise_floor: float, task_id: str | None = None) -> RetestComparisonV2:
    if noise_floor < 0:
        raise ValueError("noise_floor must be non-negative")
    delta = round(after - before, 4)
    if delta > noise_floor:
        status: ChangeStatus = "improved"
    elif delta < -noise_floor:
        status = "regressed"
    else:
        status = "unchanged"
    attribution = f"attributed_to:{task_id}" if task_id else "unattributed"
    return RetestComparisonV2(metric_name, before, after, delta, noise_floor, status, attribution)


def compare_retest_metrics(before: dict[str, float], after: dict[str, float], *, noise_floor: float) -> tuple[RetestComparisonV2, ...]:
    keys = sorted(set(before) & set(after))
    return tuple(compare_retest_metric(key, before[key], after[key], noise_floor=noise_floor) for key in keys)

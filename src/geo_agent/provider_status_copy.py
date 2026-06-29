"""User-facing provider status copy helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

ProviderRuntimeStatus = Literal["implemented", "manual", "simulated", "planned", "unavailable"]


@dataclass(frozen=True)
class ProviderStatusCopy:
    status: ProviderRuntimeStatus
    label: str
    summary: str
    report_note: str
    action_label: str
    can_execute: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_PROVIDER_STATUS_COPY: dict[ProviderRuntimeStatus, ProviderStatusCopy] = {
    "implemented": ProviderStatusCopy(
        "implemented",
        "Implemented",
        "Provider boundary is implemented and can run when explicitly configured.",
        "Implemented provider boundary; evidence depends on the configured run.",
        "Configure",
        True,
    ),
    "manual": ProviderStatusCopy(
        "manual",
        "Manual import",
        "Manual or recorded evidence path is implemented; it is not automated live coverage.",
        "Manual import evidence; results reflect the imported records.",
        "Import evidence",
        True,
    ),
    "simulated": ProviderStatusCopy(
        "simulated",
        "Simulated",
        "Fixture or fake-provider path for deterministic tests only.",
        "Simulated evidence; use for validation, not live market conclusions.",
        "View test path",
        False,
    ),
    "planned": ProviderStatusCopy(
        "planned",
        "Planned",
        "Roadmap provider; not available for audit execution yet.",
        "Planned provider; no evidence was collected from this provider.",
        "Coming soon",
        False,
    ),
    "unavailable": ProviderStatusCopy(
        "unavailable",
        "Unavailable",
        "Provider cannot run until the blocking configuration or access issue is resolved.",
        "Unavailable provider; evidence was not collected for this run.",
        "Resolve issue",
        False,
    ),
}


def provider_status_copy(status: ProviderRuntimeStatus) -> ProviderStatusCopy:
    return _PROVIDER_STATUS_COPY[status]


def provider_report_status_line(provider_name: str, status: ProviderRuntimeStatus) -> str:
    copy = provider_status_copy(status)
    return f"{provider_name}: {copy.report_note}"

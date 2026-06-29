"""Manual-only AI search provider matrix."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ManualOnlyProvider:
    provider_id: str
    display_name: str
    evidence_boundary: str
    access_method: str = "manual_import"
    implementation_status: str = "manual_only"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def manual_only_provider_matrix() -> tuple[ManualOnlyProvider, ...]:
    return (
        ManualOnlyProvider("google_aio", "Google AIO", "AIO share links are gated and not auto-capturable."),
        ManualOnlyProvider("deepseek", "DeepSeek", "Use explicit pasted or recorded capture only."),
        ManualOnlyProvider("kimi", "Kimi", "Use explicit pasted or recorded capture only."),
        ManualOnlyProvider("qianwen", "Qianwen", "Use explicit pasted or recorded capture only."),
    )

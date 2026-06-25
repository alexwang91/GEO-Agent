"""Manual import boundary for recorded GEO evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .recorded_dataset import RecordedAuditDataset, RecordedDatasetError, load_recorded_dataset_from_mapping

UNSAFE_FIELD_NAMES = {
    "api_key",
    "authorization",
    "cookie",
    "password",
    "secret",
    "token",
}


class ManualImportError(ValueError):
    pass


@dataclass(frozen=True)
class ManualImportResult:
    dataset: RecordedAuditDataset
    source_label: str
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "source_label": self.source_label,
            "brand": self.dataset.profile.brand,
            "domain": self.dataset.profile.domain,
            "engine": self.dataset.engine_adapter.engine,
            "page_count": len(self.dataset.pages),
            "manual_url_count": len(self.dataset.manual_urls),
            "sitemap_url_count": len(self.dataset.sitemap_urls),
            "max_queries": self.dataset.max_queries,
            "warnings": list(self.warnings),
        }


def validate_manual_import(payload: Mapping[str, Any], *, source_label: str = "manual-import") -> ManualImportResult:
    if not isinstance(payload, Mapping):
        raise ManualImportError("Manual import payload must be a mapping/object.")
    unsafe_paths = _unsafe_paths(payload)
    if unsafe_paths:
        raise ManualImportError(f"Manual import contains unsafe field(s): {', '.join(unsafe_paths)}")
    try:
        dataset = load_recorded_dataset_from_mapping(payload)
    except RecordedDatasetError as exc:
        raise ManualImportError(str(exc)) from exc
    warnings = _warnings(dataset)
    return ManualImportResult(dataset=dataset, source_label=source_label, warnings=tuple(warnings))


def _warnings(dataset: RecordedAuditDataset) -> list[str]:
    warnings: list[str] = []
    if not dataset.manual_urls and not dataset.sitemap_urls:
        warnings.append("No manual or sitemap URLs were provided; page coverage comes from imported pages only.")
    if dataset.max_queries is None:
        warnings.append("No max_queries limit was provided for the imported dataset.")
    return warnings


def _unsafe_paths(value: object, *, path: str = "payload") -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            current = f"{path}.{key_text}"
            if _unsafe_key(key_text):
                found.append(current)
            found.extend(_unsafe_paths(nested, path=current))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found.extend(_unsafe_paths(nested, path=f"{path}[{index}]"))
    return found


def _unsafe_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return normalized in UNSAFE_FIELD_NAMES or normalized.endswith("_token") or normalized.endswith("_secret")

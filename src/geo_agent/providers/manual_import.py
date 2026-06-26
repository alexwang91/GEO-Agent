"""Manual-import provider that feeds recorded evidence into AuditRunner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from geo_agent.audit_runner import AuditArtifacts, AuditRunner
from geo_agent.manual_import import ManualImportResult, validate_manual_import


@dataclass(frozen=True)
class ManualImportProviderRequest:
    payload: Mapping[str, Any]
    source_label: str = "manual-import"


@dataclass(frozen=True)
class ManualImportProviderResult:
    import_result: ManualImportResult
    artifacts: AuditArtifacts

    def to_dict(self) -> dict[str, object]:
        return {
            "source_label": self.import_result.source_label,
            "warnings": list(self.import_result.warnings),
            "artifacts": self.artifacts.to_dict(),
        }


class ManualImportProvider:
    provider_id = "manual_import"
    status = "manual_only"

    def run(self, request: ManualImportProviderRequest, *, runner: AuditRunner | None = None) -> ManualImportProviderResult:
        import_result = validate_manual_import(request.payload, source_label=request.source_label)
        dataset = import_result.dataset
        active_runner = runner or AuditRunner()
        artifacts = active_runner.run(
            dataset.profile,
            pages=dataset.pages,
            engine_adapter=dataset.engine_adapter,
            manual_urls=dataset.manual_urls,
            sitemap_urls=dataset.sitemap_urls,
            max_queries=dataset.max_queries,
        )
        return ManualImportProviderResult(import_result=import_result, artifacts=artifacts)

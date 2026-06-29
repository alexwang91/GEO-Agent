"""Command-line interface for fixture-based GEO audits."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .artifact_safety import assert_artifacts_safe
from .audit_runner import AuditArtifacts, AuditRunner
from .entity_profile import validate_entity_profile
from .evidence_store import EvidenceStore
from .manual_capture import import_manual_captures, manual_captures_to_engine_runs
from .recorded_dataset import load_recorded_dataset


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="geo-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Run a fixture-based GEO audit.")
    audit.add_argument("fixture", help="Path to a recorded audit dataset JSON file.")
    audit.add_argument("--out", required=True, help="Directory where audit package artifacts will be written.")

    captures = subparsers.add_parser("capture-package", help="Build a package from manual multi-engine captures.")
    captures.add_argument("fixture", help="Path to a manual capture package JSON file.")
    captures.add_argument("--out", required=True, help="Directory where audit package artifacts will be written.")

    args = parser.parse_args(argv)
    if args.command == "audit":
        return run_fixture_audit(Path(args.fixture), Path(args.out))
    if args.command == "capture-package":
        return run_capture_package(Path(args.fixture), Path(args.out))
    parser.error(f"Unknown command: {args.command}")
    return 2


def run_fixture_audit(fixture_path: Path, output_dir: Path) -> int:
    dataset = load_recorded_dataset(fixture_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = output_dir / "audit.sqlite"
    with EvidenceStore(db_path) as store:
        artifacts = AuditRunner(store).run(
            dataset.profile,
            pages=dataset.pages,
            engine_adapter=dataset.engine_adapter,
            manual_urls=dataset.manual_urls,
            sitemap_urls=dataset.sitemap_urls,
            max_queries=dataset.max_queries,
        )
    manifest = _manifest(fixture_path, db_path, dataset, artifacts)
    _write_package(output_dir, db_path, manifest, artifacts)
    return 0


def run_capture_package(fixture_path: Path, output_dir: Path) -> int:
    with fixture_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    profile = validate_entity_profile(_mapping(payload, "profile"))
    captures = import_manual_captures(list(_sequence(payload, "captures")))
    runs = manual_captures_to_engine_runs(captures)
    pages = _pages(payload.get("pages", {}))
    audit = _capture_audit(payload.get("audit", {}))
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = output_dir / "audit.sqlite"
    with EvidenceStore(db_path) as store:
        artifacts = AuditRunner(store).run_with_captured_runs(
            profile,
            pages=pages,
            runs=runs,
            manual_urls=audit["manual_urls"],
            sitemap_urls=audit["sitemap_urls"],
        )
    manifest = _capture_manifest(fixture_path, db_path, payload, artifacts)
    _write_package(output_dir, db_path, manifest, artifacts)
    return 0


def _write_package(output_dir: Path, db_path: Path, manifest: dict[str, object], artifacts: AuditArtifacts) -> None:
    _assert_package_artifacts_safe(manifest, artifacts.report_json, db_path)
    (output_dir / "report.json").write_text(artifacts.report_json, encoding="utf-8")
    (output_dir / "report.md").write_text(artifacts.report_markdown, encoding="utf-8")
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _manifest(fixture_path: Path, db_path: Path, dataset, artifacts: AuditArtifacts) -> dict[str, object]:
    metric_traces = _metric_traces(artifacts)
    return {
        "manifest_version": 2,
        "fixture": fixture_path.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile": {"brand": dataset.profile.brand, "domain": dataset.profile.domain},
        "engine": dataset.engine_adapter.engine,
        "query_count": len(artifacts.queries),
        "page_count": len(artifacts.pages),
        "run_count": len(artifacts.runs),
        "artifacts": ["manifest.json", "report.json", "report.md", "audit.sqlite"],
        "evidence_database": db_path.name,
        "traceability": {
            "metric_to_sample_ids": metric_traces,
            "sample_ids": list(artifacts.evidence_graph.audit_run.sample_ids),
            "prompt_ids": list(artifacts.evidence_graph.audit_run.prompt_ids),
        },
    }


def _capture_manifest(fixture_path: Path, db_path: Path, payload: Mapping[str, Any], artifacts: AuditArtifacts) -> dict[str, object]:
    engines = sorted({run.engine for run in artifacts.runs})
    return {
        "manifest_version": 2,
        "fixture": fixture_path.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile": {"brand": artifacts.profile.brand, "domain": artifacts.profile.domain},
        "engine": "multi_engine_manual_capture" if len(engines) > 1 else engines[0],
        "engines": engines,
        "capture_count": len(artifacts.runs),
        "query_count": len(artifacts.queries),
        "page_count": len(artifacts.pages),
        "run_count": len(artifacts.runs),
        "artifacts": ["manifest.json", "report.json", "report.md", "audit.sqlite"],
        "evidence_database": db_path.name,
        "input_type": "manual_capture_package",
        "metadata": dict(payload.get("metadata", {})) if isinstance(payload.get("metadata", {}), Mapping) else {},
        "traceability": {
            "metric_to_sample_ids": _metric_traces(artifacts),
            "sample_ids": list(artifacts.evidence_graph.audit_run.sample_ids),
            "prompt_ids": list(artifacts.evidence_graph.audit_run.prompt_ids),
        },
    }


def _metric_traces(artifacts: AuditArtifacts) -> list[dict[str, object]]:
    return [
        {
            "metric_id": metric.metric_id,
            "name": metric.name,
            "value": metric.value,
            "sample_ids": list(metric.sample_ids),
            "prompt_ids": list(metric.prompt_ids),
            "citation_ids": list(metric.citation_ids),
        }
        for metric in artifacts.evidence_graph.metrics
    ]


def _assert_package_artifacts_safe(manifest: dict[str, object], report_json: str, db_path: Path) -> None:
    sqlite_text = db_path.read_bytes().decode("utf-8", errors="ignore")
    assert_artifacts_safe(
        {
            "manifest.json": manifest,
            "report.json": json.loads(report_json),
            "audit.sqlite": sqlite_text,
        }
    )


def _mapping(payload: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    value = payload.get(field)
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(payload: Mapping[str, Any], field: str) -> list[Mapping[str, Any]]:
    value = payload.get(field)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty list")
    if any(not isinstance(item, Mapping) for item in value):
        raise ValueError(f"{field} must contain only objects")
    return value


def _pages(value: object) -> dict[str, str]:
    if value in (None, {}):
        return {}
    if not isinstance(value, Mapping):
        raise ValueError("pages must be an object")
    return {str(url): str(html) for url, html in value.items()}


def _capture_audit(value: object) -> dict[str, list[str]]:
    if value in (None, {}):
        return {"manual_urls": [], "sitemap_urls": []}
    if not isinstance(value, Mapping):
        raise ValueError("audit must be an object")
    return {
        "manual_urls": [str(item) for item in value.get("manual_urls", [])],
        "sitemap_urls": [str(item) for item in value.get("sitemap_urls", [])],
    }


if __name__ == "__main__":
    raise SystemExit(main())

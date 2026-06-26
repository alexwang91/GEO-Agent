"""Command-line interface for fixture-based GEO audits."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .artifact_safety import assert_artifacts_safe
from .audit_runner import AuditRunner
from .evidence_store import EvidenceStore
from .recorded_dataset import load_recorded_dataset


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="geo-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Run a fixture-based GEO audit.")
    audit.add_argument("fixture", help="Path to a recorded audit dataset JSON file.")
    audit.add_argument("--out", required=True, help="Directory where audit package artifacts will be written.")

    args = parser.parse_args(argv)
    if args.command == "audit":
        return run_fixture_audit(Path(args.fixture), Path(args.out))
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
    _assert_package_artifacts_safe(manifest, artifacts.report_json, db_path)
    (output_dir / "report.json").write_text(artifacts.report_json, encoding="utf-8")
    (output_dir / "report.md").write_text(artifacts.report_markdown, encoding="utf-8")
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return 0


def _manifest(fixture_path: Path, db_path: Path, dataset, artifacts) -> dict[str, object]:
    metric_traces = [
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


def _assert_package_artifacts_safe(manifest: dict[str, object], report_json: str, db_path: Path) -> None:
    sqlite_text = db_path.read_bytes().decode("utf-8", errors="ignore")
    assert_artifacts_safe(
        {
            "manifest.json": manifest,
            "report.json": json.loads(report_json),
            "audit.sqlite": sqlite_text,
        }
    )


if __name__ == "__main__":
    raise SystemExit(main())

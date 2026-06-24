"""Command-line interface for fixture-based GEO audits."""

from __future__ import annotations

import argparse
from pathlib import Path

from .audit_runner import AuditRunner
from .recorded_dataset import load_recorded_dataset


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="geo-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Run a fixture-based GEO audit.")
    audit.add_argument("fixture", help="Path to a recorded audit dataset JSON file.")
    audit.add_argument("--out", required=True, help="Directory where report artifacts will be written.")

    args = parser.parse_args(argv)
    if args.command == "audit":
        return _run_audit(Path(args.fixture), Path(args.out))
    parser.error(f"Unknown command: {args.command}")
    return 2


def _run_audit(fixture_path: Path, output_dir: Path) -> int:
    dataset = load_recorded_dataset(fixture_path)
    artifacts = AuditRunner().run(
        dataset.profile,
        pages=dataset.pages,
        engine_adapter=dataset.engine_adapter,
        manual_urls=dataset.manual_urls,
        sitemap_urls=dataset.sitemap_urls,
        max_queries=dataset.max_queries,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(artifacts.report_json, encoding="utf-8")
    (output_dir / "report.md").write_text(artifacts.report_markdown, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

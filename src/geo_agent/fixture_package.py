"""Fixture package wrapper for desktop command boundaries."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .cli import run_fixture_audit


@dataclass(frozen=True)
class FixturePackageResult:
    status: str
    fixture_path: str
    output_dir: str
    manifest_path: str
    report_json_path: str
    report_markdown_path: str
    data_file_path: str
    brand: str
    domain: str
    engine: str
    query_count: int
    page_count: int
    run_count: int
    artifacts: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "fixture_path": self.fixture_path,
            "output_dir": self.output_dir,
            "manifest_path": self.manifest_path,
            "report_json_path": self.report_json_path,
            "report_markdown_path": self.report_markdown_path,
            "data_file_path": self.data_file_path,
            "brand": self.brand,
            "domain": self.domain,
            "engine": self.engine,
            "query_count": self.query_count,
            "page_count": self.page_count,
            "run_count": self.run_count,
            "artifacts": list(self.artifacts),
        }


def run_fixture_package(fixture_path: str | Path, output_dir: str | Path) -> FixturePackageResult:
    fixture = Path(fixture_path)
    output = Path(output_dir)
    run_fixture_audit(fixture, output)
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    profile = manifest.get("profile", {})
    return FixturePackageResult(
        status="completed",
        fixture_path=str(fixture),
        output_dir=str(output),
        manifest_path=str(manifest_path),
        report_json_path=str(output / "report.json"),
        report_markdown_path=str(output / "report.md"),
        data_file_path=str(output / "audit.sqlite"),
        brand=str(profile.get("brand", "")),
        domain=str(profile.get("domain", "")),
        engine=str(manifest.get("engine", "")),
        query_count=int(manifest.get("query_count", 0)),
        page_count=int(manifest.get("page_count", 0)),
        run_count=int(manifest.get("run_count", 0)),
        artifacts=tuple(str(item) for item in manifest.get("artifacts", [])),
    )
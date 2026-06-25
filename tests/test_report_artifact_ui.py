from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"
ARTIFACTS = ROOT / "apps" / "desktop" / "src" / "reportArtifacts.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_report_artifact_view_model_loads_manifest_and_report_shapes():
    artifact_source = read(ARTIFACTS)

    for label in [
        "sampleManifestArtifact",
        "sampleReportArtifact",
        "buildReportArtifactView",
        "manifest?.package_id",
        "safeReport.score",
        "safeReport.missing_queries",
        "safeReport.competitor_map",
        "safeReport.cited_sources",
        "safeReport.failures",
        "safeReport.recommended_actions",
        "safeReport.retest_plan",
    ]:
        assert label in artifact_source


def test_report_ui_uses_artifact_view_model_instead_of_inline_report_preview():
    app = read(APP)

    assert "buildReportArtifactView(sampleManifestArtifact, sampleReportArtifact)" in app
    assert "const reportPreview" not in app
    assert "Generated package artifact: {reportView.source}" in app
    assert "Package: {reportView.packageId} generated at {reportView.generatedAt}" in app


def test_report_ui_renders_artifact_sections_from_view_model():
    app = read(APP)

    for label in [
        "reportView.score.visibility_score",
        "reportView.score.mention_share",
        "reportView.score.citation_share",
        "reportView.score.recommendation_share",
        "reportView.missingQueries",
        "reportView.competitorMap",
        "reportView.citedSources",
        "reportView.failures",
        "reportView.recommendedActions",
        "reportView.retestPlan",
    ]:
        assert label in app


def test_partial_artifact_warnings_are_explicit():
    artifact_source = read(ARTIFACTS)
    app = read(APP)

    assert "Missing manifest.json; package provenance is unavailable." in artifact_source
    assert "Missing report.json; report sections cannot be rendered." in artifact_source
    assert "reportView.warnings.map" in app
    assert "No evidence in this artifact section." in app


def test_evidence_package_file_list_comes_from_manifest_view():
    app = read(APP)
    artifact_source = read(ARTIFACTS)

    assert "const packageFiles = ['manifest.json', ...reportView.files]" in app
    assert "files.report_json" in artifact_source
    assert "files.report_markdown" in artifact_source
    assert "files.audit_database" in artifact_source

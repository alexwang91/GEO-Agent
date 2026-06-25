from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"
STYLES = ROOT / "apps" / "desktop" / "src" / "styles.css"


def read_app() -> str:
    return APP.read_text(encoding="utf-8")


def test_ui_exposes_fixture_manual_and_fake_provider_paths():
    app = read_app()

    for label in [
        "Fixture package audit",
        "Manual import path",
        "Fake provider path",
        "run_fixture_audit(fixture_path, output_dir)",
        "manual_import(recorded_dataset)",
        "static_crawler + recorded answer adapter",
    ]:
        assert label in app


def test_ui_displays_report_artifact_sections():
    app = read_app()

    for label in [
        "Generated package artifact: report.json",
        "Visibility score",
        "Mention share",
        "Citation share",
        "Recommendation share",
        "Missing queries",
        "Competitor map",
        "Cited sources",
        "Failure diagnoses",
        "Recommended tasks",
        "Retest plan",
    ]:
        assert label in app


def test_ui_has_truthful_provider_statuses_and_no_live_success_claim():
    app = read_app()

    for status in [
        "Configured boundary",
        "Fake/test available",
        "Planned",
        "Available",
        "Fake/test only",
    ]:
        assert status in app

    forbidden_claims = [
        "Live provider enabled",
        "Real-time AI search connected",
        "Production crawler active",
        "Live provider execution is ready",
        "Provider-backed audit succeeded",
    ]
    for claim in forbidden_claims:
        assert claim not in app


def test_ui_represents_download_actions_as_disabled_until_artifacts_are_wired():
    app = read_app()

    assert "Download report.json" in app
    assert "Download report.md" in app
    assert "Download audit package" in app
    assert "<button disabled>Download report.json</button>" in app
    assert "<button disabled>Download report.md</button>" in app
    assert "<button disabled>Download audit package</button>" in app


def test_styles_include_report_and_run_path_layouts():
    styles = STYLES.read_text(encoding="utf-8")

    for selector in [
        ".run-path-grid",
        ".metric-grid",
        ".report-grid",
        ".run-path-card",
        ".metric-card",
        ".evidence-block",
        ".download-actions",
    ]:
        assert selector in styles

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_desktop_report_artifacts_parse_per_engine_sections():
    source = (ROOT / "apps" / "desktop" / "src" / "reportArtifacts.js").read_text(encoding="utf-8")

    assert "extractPerEngineBreakdown" in source
    assert "Per-Engine Breakdown" in source
    assert "engineBreakdown" in source
    assert "aggregateLabel" in source
    assert "directional_not_verdict" not in source or "aggregate_label" in source
    assert "Demo fixture artifact" in source


def test_desktop_app_renders_per_engine_before_legacy_score_cards():
    source = (ROOT / "apps" / "desktop" / "src" / "App.jsx").read_text(encoding="utf-8")

    per_engine_index = source.index("Per-engine breakdown")
    score_index = source.index("Visibility score")
    assert per_engine_index < score_index
    assert "EngineBreakdown" in source
    assert "Owned citation share" in source
    assert "Competitor-only share" in source
    assert "aggregate score is directional context, not a verdict" in source

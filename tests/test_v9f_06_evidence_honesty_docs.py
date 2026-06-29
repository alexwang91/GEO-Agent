from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_google_aio_manual_only_status_is_consistent_across_docs_and_ui():
    provider_doc = read("docs/provider-status-language.md")
    readme = read("README.md")
    app = read("apps/desktop/src/App.jsx")
    status_copy = read("src/geo_agent/provider_status_copy.py")

    for content in (provider_doc, readme, app, status_copy):
        assert "manual_only" in content or "Manual only" in content
    assert "google_aio" in provider_doc
    assert "Google AIO" in readme
    assert "Google AIO" in app
    assert "AIO share links are gated and not auto-capturable" in provider_doc
    assert "AIO share links are gated and not auto-capturable" in readme
    assert "AIO share links are gated and not auto-capturable" in app


def test_real_case_and_limitations_preserve_directional_boundaries():
    real_case = read("docs/v9-real-case.md")
    limitations = read("docs/limitations.md")

    for content in (real_case, limitations):
        assert "single aggregate score" in content
        assert "directional" in content
        assert "manual capture" in content
    assert "manual-only capture" in real_case
    assert "per-engine and per-component" in limitations
    assert "not a verdict" in limitations

from pathlib import Path


def test_tauri_react_shell_structure_exists():
    root = Path(__file__).resolve().parents[1]
    desktop = root / "apps" / "desktop"

    assert (desktop / "package.json").exists()
    assert (desktop / "index.html").exists()
    assert (desktop / "src" / "main.jsx").exists()
    assert (desktop / "src" / "App.jsx").exists()
    assert (desktop / "src" / "styles.css").exists()
    assert (desktop / "src-tauri" / "tauri.conf.json").exists()
    assert (desktop / "src-tauri" / "Cargo.toml").exists()
    assert (desktop / "src-tauri" / "src" / "main.rs").exists()


def test_react_shell_contains_required_workflow_sections():
    root = Path(__file__).resolve().parents[1]
    app = (root / "apps" / "desktop" / "src" / "App.jsx").read_text(encoding="utf-8")

    for label in ["Providers", "Brand Profile", "Queries", "Audit Run", "Report", "Evidence Package"]:
        assert label in app

    for provider in ["OpenAI-compatible", "Perplexity", "Gemini", "Crawl4AI", "Firecrawl", "Google Search Console", "Manual Import"]:
        assert provider in app

    assert "Coming soon" in app
    assert "Credentials are used only to run your audit" in app
    assert "No audit report yet" in app


def test_tauri_shell_does_not_claim_live_provider_support():
    root = Path(__file__).resolve().parents[1]
    app = (root / "apps" / "desktop" / "src" / "App.jsx").read_text(encoding="utf-8")
    forbidden_claims = [
        "Live provider enabled",
        "Real-time AI search connected",
        "Production crawler active",
    ]

    for claim in forbidden_claims:
        assert claim not in app

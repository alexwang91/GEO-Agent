from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_python_package_entrypoint_and_exports_are_release_ready():
    pyproject = read("pyproject.toml")
    init_py = read("src/geo_agent/__init__.py")

    assert 'name = "geo-agent"' in pyproject
    assert 'requires-python = ">=3.11"' in pyproject
    assert 'geo-agent = "geo_agent.cli:main"' in pyproject
    for exported_name in [
        "AuditRunner",
        "OpenAICompatibleAnswerProvider",
        "validate_manual_import",
        "evaluate_provider_output_cases",
        "scan_artifacts_for_access_leaks",
        "compare_retest_reports",
    ]:
        assert f'"{exported_name}"' in init_py


def test_desktop_app_structure_and_command_boundary_are_present():
    app = read("apps/desktop/src/App.jsx")
    styles = read("apps/desktop/src/styles.css")
    tauri_main = read("apps/desktop/src-tauri/src/main.rs")
    package_json = read("apps/desktop/package.json")

    for path_label in ["Providers", "Audit Run", "Report", "Evidence Package"]:
        assert path_label in app
    for selector in [".app-shell", ".provider-grid", ".report-grid", ".download-actions"]:
        assert selector in styles
    assert "fn list_providers()" in tauri_main
    assert "fn run_fixture_audit(fixture_path: String, output_dir: String)" in tauri_main
    assert "geo_agent.cli" in tauri_main
    assert "generate_handler![list_providers, run_fixture_audit]" in tauri_main
    assert '"dev"' in package_json
    assert '"build"' in package_json


def test_required_docs_and_loop_state_are_present():
    for doc_path in [
        "AGENTS.md",
        "docs/progress.md",
        "docs/next-steps-plan.md",
        "docs/runner-prompt.md",
        "docs/loop-v6.md",
        "docs/provider-access-architecture.md",
        "docs/recorded-dataset-schema.md",
        "docs/crawl-provider.md",
    ]:
        assert (ROOT / doc_path).is_file(), doc_path

    progress = read("docs/progress.md")
    assert "V6-7 | Add release-readiness packaging checks" in progress
    assert "V6-8 | Add skill-learning record" in progress


def test_ci_release_readiness_guards_are_present():
    workflow = read(".github/workflows/verify.yml")

    assert "Run unit tests" in workflow
    assert "python -m unittest discover -s tests -v" in workflow
    assert "Verify runner docs" in workflow
    assert "! find . -maxdepth 4 -type f" in workflow
    assert "dummy" in workflow


def test_no_placeholder_or_dummy_files_in_release_scope():
    forbidden_names = {"noop", "dummy", "x", "y"}
    offenders = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.name in forbidden_names:
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []

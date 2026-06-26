import json
import tempfile
import unittest
from pathlib import Path

from geo_agent.fixture_package import FixturePackageResult, run_fixture_package


def fixture():
    return {
        "profile": {
            "brand": "Acme AI",
            "aliases": ["Acme"],
            "domain": "acme.ai",
            "competitors": ["Globex"],
            "target_regions": ["US"],
            "target_languages": ["en"],
            "target_customer": "marketing teams",
            "main_product": "AI visibility platform",
            "category": "GEO software",
            "business_goal": "improve AI search visibility",
        },
        "pages": {
            "https://acme.ai/": "<html><head><title>Acme</title><link rel='canonical' href='https://acme.ai/'></head><body><h1>Acme AI</h1></body></html>"
        },
        "audit": {"manual_urls": ["https://acme.ai/"], "sitemap_urls": [], "max_queries": 2},
        "recorded_runs": {
            "engine": "recorded",
            "runs": {
                "What is Acme AI for marketing teams?": {
                    "timestamp": "2026-06-24T00:00:00Z",
                    "raw_answer": "Acme AI is a GEO platform.",
                    "citations": ["https://acme.ai/"],
                    "mentions": ["Acme AI"],
                    "recommendations": ["Acme AI"],
                },
                "Best GEO software tools for marketing teams in US": {
                    "timestamp": "2026-06-24T00:01:00Z",
                    "raw_answer": "Globex appears in category lists.",
                    "citations": ["https://globex.com/"],
                    "mentions": ["Globex"],
                    "recommendations": ["Globex"],
                },
            },
        },
        "metadata": {"name": "fixture-command"},
    }


class TauriFixtureAuditCommandTests(unittest.TestCase):
    def test_fixture_package_wrapper_returns_redacted_package_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "fixture.json"
            output_dir = root / "out"
            fixture_path.write_text(json.dumps(fixture()), encoding="utf-8")

            result = run_fixture_package(fixture_path, output_dir)

            self.assertIsInstance(result, FixturePackageResult)
            payload = result.to_dict()
            self.assertEqual(payload["status"], "completed")
            self.assertEqual(payload["brand"], "Acme AI")
            self.assertEqual(payload["domain"], "acme.ai")
            self.assertEqual(payload["engine"], "recorded")
            self.assertEqual(payload["query_count"], 2)
            self.assertEqual(payload["page_count"], 1)
            self.assertEqual(payload["run_count"], 2)
            self.assertEqual(payload["artifacts"], ["manifest.json", "report.json", "report.md", "audit.sqlite"])
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertTrue((output_dir / "report.json").exists())
            self.assertTrue((output_dir / "report.md").exists())
            self.assertTrue((output_dir / "audit.sqlite").exists())

    def test_tauri_command_shape_is_present_without_compiling_tauri(self):
        root = Path(__file__).resolve().parents[1]
        main_rs = (root / "apps" / "desktop" / "src-tauri" / "src" / "main.rs").read_text(encoding="utf-8")

        self.assertIn("fn run_fixture_audit(fixture_path: String, output_dir: String)", main_rs)
        self.assertIn("geo_agent.cli", main_rs)
        self.assertIn("manifest.json", main_rs)
        self.assertIn("report.json", main_rs)
        self.assertIn("report.md", main_rs)
        self.assertIn("audit.sqlite", main_rs)
        self.assertIn("generate_handler![list_providers, run_fixture_audit]", main_rs)

    def test_react_ui_represents_provider_boundary_truthfully(self):
        root = Path(__file__).resolve().parents[1]
        app = (root / "apps" / "desktop" / "src" / "App.jsx").read_text(encoding="utf-8")

        self.assertIn("Fixture-only audit path", app)
        self.assertIn("run_fixture_audit(fixture_path, output_dir)", app)
        self.assertIn("Provider-backed audit execution uses implemented fixture/manual boundaries only unless a provider is explicitly configured and verified", app)
        self.assertIn("Planned providers remain planned and unavailable for live audits", app)
        self.assertIn("Run fixture audit from local file", app)
        self.assertNotIn("Live provider enabled", app)
        self.assertNotIn("Provider-backed audit is ready", app)


if __name__ == "__main__":
    unittest.main()

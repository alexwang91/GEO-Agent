import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class EvidenceHonestyDocsTests(unittest.TestCase):
    def test_google_aio_manual_only_status_is_consistent_across_docs_and_ui(self):
        provider_doc = read("docs/provider-status-language.md")
        readme = read("README.md")
        app = read("apps/desktop/src/App.jsx")
        status_copy = read("src/geo_agent/provider_status_copy.py")

        for content in (provider_doc, readme, app, status_copy):
            self.assertTrue("manual_only" in content or "Manual only" in content)
        self.assertIn("google_aio", provider_doc)
        self.assertIn("Google AIO", readme)
        self.assertIn("Google AIO", app)
        self.assertIn("AIO share links are gated and not auto-capturable", provider_doc)
        self.assertIn("AIO share links are gated and not auto-capturable", readme)
        self.assertIn("AIO share links are gated and not auto-capturable", app)

    def test_real_case_and_limitations_preserve_directional_boundaries(self):
        real_case = read("docs/v9-real-case.md")
        limitations = read("docs/limitations.md")

        for content in (real_case, limitations):
            self.assertIn("single aggregate score", content)
            self.assertIn("directional", content)
            self.assertIn("manual capture", content)
        self.assertIn("manual-only capture", real_case)
        self.assertIn("per-engine and per-component", limitations)
        self.assertIn("not a verdict", limitations)


if __name__ == "__main__":
    unittest.main()

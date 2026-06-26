import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


class ProviderStatusUICopyTests(unittest.TestCase):
    def test_desktop_copy_names_all_runtime_statuses(self):
        app = read("apps/desktop/src/App.jsx")
        for phrase in ["implemented", "manual import", "simulated", "planned", "unavailable"]:
            self.assertIn(phrase, app)

    def test_report_copy_preserves_non_overclaim_statuses(self):
        app = read("apps/desktop/src/App.jsx")
        self.assertIn("planned providers collect no evidence", app)
        self.assertIn("unavailable providers did not run", app)
        self.assertIn("not chatgpt search", app)

    def test_provider_status_doc_defines_richer_runtime_vocabulary(self):
        doc = read("docs/provider-status-language.md")
        for literal in ["`implemented`", "`manual`", "`simulated`", "`planned`", "`unavailable`"]:
            self.assertIn(literal, doc)


if __name__ == "__main__":
    unittest.main()

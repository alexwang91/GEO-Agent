import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/ux-contract.md",
    "docs/user-journeys.md",
    "docs/personas.md",
    "docs/report-copy-guidelines.md",
    "docs/error-state-taxonomy.md",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


class UXCopyContractTest(unittest.TestCase):
    def test_required_ux_docs_exist(self):
        for path in REQUIRED_DOCS:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_ux_docs_distinguish_provider_modes(self):
        copy = "\n".join(read(path) for path in REQUIRED_DOCS)
        for term in ["manual", "simulated", "live configured", "planned", "directional"]:
            self.assertIn(term, copy)

    def test_report_guidelines_include_non_overclaim_rules(self):
        guidelines = read("docs/report-copy-guidelines.md")
        self.assertIn("one sample is not enough", guidelines)
        self.assertIn("not chatgpt search", guidelines)
        self.assertIn("planned provider", guidelines)

    def test_error_taxonomy_has_recovery_actions(self):
        taxonomy = read("docs/error-state-taxonomy.md")
        self.assertIn("provider_planned", taxonomy)
        self.assertIn("sample_budget_too_low", taxonomy)
        self.assertIn("recovery action", taxonomy)


if __name__ == "__main__":
    unittest.main()

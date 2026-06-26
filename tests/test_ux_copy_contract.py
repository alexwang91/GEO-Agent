import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COPY_SURFACES = [
    "README.md",
    "apps/desktop/src/App.jsx",
    "docs/ux-contract.md",
    "docs/user-journeys.md",
    "docs/personas.md",
    "docs/report-copy-guidelines.md",
    "docs/error-state-taxonomy.md",
]

REQUIRED_DOCS = [
    "docs/ux-contract.md",
    "docs/user-journeys.md",
    "docs/personas.md",
    "docs/report-copy-guidelines.md",
    "docs/error-state-taxonomy.md",
]

FORBIDDEN_PHRASES = [
    "guarantees ranking improvement",
    "guarantees citation improvement",
    "proves engine behavior",
    "planned provider is live",
    "planned providers are live",
    "definitive visibility conclusion",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def combined_copy():
    return "\n".join(read(path) for path in COPY_SURFACES).lower()


class UXCopyContractTest(unittest.TestCase):
    def test_required_ux_docs_exist(self):
        for path in REQUIRED_DOCS:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_provider_evidence_modes_are_distinguished(self):
        copy = combined_copy()
        required_terms = [
            "manual",
            "simulated",
            "live configured",
            "planned",
            "directional",
            "not chatgpt search",
        ]
        for term in required_terms:
            self.assertIn(term, copy)

    def test_low_sample_and_provider_overclaims_are_absent(self):
        copy = combined_copy()
        for phrase in FORBIDDEN_PHRASES:
            self.assertNotRegex(copy, re.compile(re.escape(phrase), re.IGNORECASE), phrase)

    def test_journey_has_ten_numbered_steps(self):
        journey = read("docs/user-journeys.md")
        steps = re.findall(r"^\d+\. \*\*", journey, flags=re.MULTILINE)
        self.assertEqual(10, len(steps))

    def test_error_taxonomy_has_recovery_actions(self):
        taxonomy = read("docs/error-state-taxonomy.md")
        for code in [
            "provider_planned",
            "provider_not_configured",
            "manual_import_invalid",
            "sample_budget_too_low",
            "package_redaction_failed",
        ]:
            self.assertIn(f"`{code}`", taxonomy)
        self.assertIn("Recovery action", taxonomy)


if __name__ == "__main__":
    unittest.main()

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


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def combined(paths):
    return "\n".join(read(path) for path in paths).lower()


class UXCopyContractTest(unittest.TestCase):
    def test_required_ux_docs_exist(self):
        for path in REQUIRED_DOCS:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_provider_evidence_modes_are_distinguished(self):
        copy = combined(COPY_SURFACES)
        for term in ["manual", "simulated", "live configured", "planned", "directional", "not chatgpt search"]:
            self.assertIn(term, copy)

    def test_user_copy_uses_safe_low_sample_and_provider_language(self):
        user_copy = combined(["README.md", "apps/desktop/src/App.jsx"])
        for phrase in [
            "does not guarantee ranking improvement",
            "directional only",
            "planned providers are not live",
            "not chatgpt search",
        ]:
            self.assertIn(phrase, user_copy)

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

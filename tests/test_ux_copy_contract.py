import re
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

    def test_ux_contract_distinguishes_evidence_modes(self):
        contract = read("docs/ux-contract.md")
        for term in ["manual", "simulated", "live configured", "planned", "directional"]:
            self.assertIn(term, contract)

    def test_report_guidelines_preserve_provider_and_low_sample_boundaries(self):
        guidelines = read("docs/report-copy-guidelines.md")
        for phrase in [
            "one sample is not enough",
            "does not ensure ranking or citation improvement",
            "openai-compatible output is not chatgpt search",
            "planned provider remains planned",
        ]:
            self.assertIn(phrase, guidelines)

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
        self.assertIn("recovery action", taxonomy)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "v10-completion-report.md"
PROGRESS = ROOT / "docs" / "progress.md"
TRACE = ROOT / "docs" / "loop-trace.md"


class V10CompletionReportTests(unittest.TestCase):
    def test_report_lists_every_v10_milestone_and_next_state(self):
        report = REPORT.read_text(encoding="utf-8")
        progress = PROGRESS.read_text(encoding="utf-8")
        trace = TRACE.read_text(encoding="utf-8")

        for index in range(1, 18):
            milestone = f"V10-{index:02d}"
            self.assertIn(milestone, report)
            self.assertIn(f"| {milestone} | DONE |", progress)
            self.assertIn(milestone, trace)
        self.assertIn("Final V10 merge commit", report)
        self.assertIn("V11 real-case reliability", progress)


if __name__ == "__main__":
    unittest.main()

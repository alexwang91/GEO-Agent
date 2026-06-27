import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DocsStateConsistencyTest(unittest.TestCase):
    def test_progress_marks_current_next_state(self):
        progress = read("docs/progress.md")
        self.assertIn("V7-38", progress)
        self.assertIn("V8-01", progress)

    def test_runner_docs_name_current_first_todo(self):
        paths = ["AGENTS.md", "docs/handoff-decision.md", "docs/runner-prompt.md", "docs/state-audit.md"]
        for path in paths:
            self.assertIn("V8-01", read(path), path)

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DocsStateConsistencyTest(unittest.TestCase):
    def test_progress_marks_current_next_state(self):
        progress = read("docs/progress.md")
        self.assertIn("V7-08", progress)
        self.assertIn("V7-09", progress)

    def test_runner_docs_name_v7_09_as_next(self):
        for path in ["AGENTS.md", "docs/handoff-decision.md", "docs/runner-prompt.md", "docs/state-audit.md"]:
            self.assertIn("V7-09", read(path), path)


if __name__ == "__main__":
    unittest.main()

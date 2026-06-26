import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DocsStateConsistencyTest(unittest.TestCase):
    def test_progress_marks_current_next_state(self):
        progress = read("docs/progress.md")
        self.assertIn("V7-04", progress)
        self.assertIn("V7-05", progress)
        self.assertIn("DONE", progress)
        self.assertIn("TODO", progress)

    def test_runner_docs_name_v7_05_as_next(self):
        for path in ["AGENTS.md", "docs/next-steps-plan.md", "docs/handoff-decision.md", "docs/runner-prompt.md", "docs/state-audit.md"]:
            self.assertIn("V7-05", read(path), path)

    def test_handoff_keeps_current_agent_mode(self):
        handoff = read("docs/handoff-decision.md")
        self.assertIn("current_agent_development", handoff)
        self.assertIn("V7-05", handoff)


if __name__ == "__main__":
    unittest.main()

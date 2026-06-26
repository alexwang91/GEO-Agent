import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_ROW_RE = re.compile(
    r"^\|\s*(?P<milestone>(?:M\d+|PLAN-0|V\d+(?:-\d+(?:\.\d+)?)?))\s*\|[^\n|]*\|\s*(?P<status>TODO|IN_PROGRESS|DONE|BLOCKED|DEFERRED|CANCELLED)\s*\|",
    re.MULTILINE,
)
FIRST_TODO_RE = re.compile(r"first(?: product)? TODO(?: milestone)?[^`\n]*`(?P<milestone>[^`]+)`", re.IGNORECASE)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def progress_statuses():
    return {m.group("milestone"): m.group("status") for m in STATUS_ROW_RE.finditer(read("docs/progress.md"))}


def first_progress_todo():
    for milestone, status in progress_statuses().items():
        if status == "TODO":
            return milestone
    raise AssertionError("docs/progress.md has no TODO milestone")


def declared_first_todos(path):
    return [m.group("milestone") for m in FIRST_TODO_RE.finditer(read(path))]


class DocsStateConsistencyTest(unittest.TestCase):
    def test_declared_first_todo_matches_progress(self):
        first_todo = first_progress_todo()
        self.assertEqual("V7-02", first_todo)
        for path in ["AGENTS.md", "docs/next-steps-plan.md", "docs/handoff-decision.md", "docs/runner-prompt.md", "docs/state-audit.md"]:
            declarations = declared_first_todos(path)
            self.assertTrue(declarations, path)
            self.assertIn(first_todo, declarations, path)
            self.assertNotIn("V7-01", declarations, path)

    def test_no_status_conflicts_with_progress(self):
        canonical = progress_statuses()
        for path in ["docs/next-steps-plan.md", "docs/state-audit.md"]:
            for match in STATUS_ROW_RE.finditer(read(path)):
                milestone = match.group("milestone")
                if milestone in canonical:
                    self.assertEqual(canonical[milestone], match.group("status"), f"{path}: {milestone}")

    def test_handoff_and_workflow_target_current_state(self):
        self.assertIn("chosen_mode: current_agent_development", read("docs/handoff-decision.md"))
        self.assertIn("first_todo_after_v7_01_merge: V7-02", read("docs/handoff-decision.md"))
        workflow = read(".github/workflows/verify.yml")
        self.assertIn("docs/state-audit.md", workflow)
        self.assertIn("tests/test_docs_state_consistency.py", workflow)
        self.assertIn("V7-02", workflow)
        self.assertIn("current_agent_development", workflow)

    def test_readme_states_technical_preview_boundary(self):
        readme = read("README.md")
        self.assertIn("Technical preview status", readme)
        self.assertIn("alpha/technical preview", readme)
        self.assertIn("not ChatGPT Search", readme)
        self.assertIn("not guarantee ranking improvement", readme)


if __name__ == "__main__":
    unittest.main()

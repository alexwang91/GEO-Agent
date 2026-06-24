import unittest
from pathlib import Path


class LiveAdapterBoundaryDocsTests(unittest.TestCase):
    def test_live_adapter_boundary_documents_stopper_rules_without_live_code(self):
        repo_root = Path(__file__).resolve().parents[1]
        docs = (repo_root / "docs" / "live-adapter-boundary.md").read_text(encoding="utf-8")

        self.assertIn("No live AI search calls", docs)
        self.assertIn("No secrets in tests", docs)
        self.assertIn("sample(query: str", docs)
        self.assertIn("request ID", docs)
        self.assertIn("Rate limits and retries", docs)
        self.assertIn("Stopper rules", docs)
        self.assertIn("CI would require external network calls", docs)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'docs/public-technical-preview.md').read_text(encoding='utf-8')


class PublicTechnicalPreviewDocsTests(unittest.TestCase):
    def test_preview_docs_cover_scope_guardrails_and_status(self):
        self.assertIn('Public Technical Preview', CONTENT)
        self.assertIn('Manual-import and fixture-safe evidence workflows', CONTENT)
        self.assertIn('No live provider credentials are required', CONTENT)
        self.assertIn('Low-sample conclusions are directional', CONTENT)
        self.assertIn('V7-01 through V7-38 are complete', CONTENT)


if __name__ == '__main__':
    unittest.main()

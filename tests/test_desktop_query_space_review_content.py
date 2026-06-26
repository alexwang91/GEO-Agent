import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/querySpaceReviewContent.js').read_text(encoding='utf-8')


class DesktopQuerySpaceReviewContentTests(unittest.TestCase):
    def test_query_review_copy_has_core_controls(self):
        for phrase in ['Query Space Review', 'Citation likelihood', 'Business value', 'Dedupe status', 'Approve query', 'Reject duplicate']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('Small query sets are directional', CONTENT)


if __name__ == '__main__':
    unittest.main()

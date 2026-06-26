import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/dashboardContent.js').read_text(encoding='utf-8')


class DesktopDashboardContentTests(unittest.TestCase):
    def test_dashboard_cards_and_filters_exist(self):
        for phrase in ['Visibility Dashboard', 'Citation absorption', 'Claim fidelity', 'Open optimization tasks', 'Retest status']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('Low-sample results are directional', CONTENT)
        self.assertIn('Source class', CONTENT)


if __name__ == '__main__':
    unittest.main()

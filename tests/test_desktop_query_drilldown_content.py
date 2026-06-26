import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/queryDrilldownContent.js').read_text(encoding='utf-8')


class DesktopQueryDrilldownContentTests(unittest.TestCase):
    def test_query_drilldown_copy_has_citation_map_fields(self):
        for phrase in ['Query Drilldown', 'Citation URL', 'Source class', 'Claim support', 'View citation map']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('Create optimization task', CONTENT)


if __name__ == '__main__':
    unittest.main()

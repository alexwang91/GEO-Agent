import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AlphaScaffoldingTests(unittest.TestCase):
    def test_sample_package_and_checklist_exist(self):
        package = json.loads((ROOT / 'samples/alpha/sample_audit_package.json').read_text(encoding='utf-8'))
        checklist = (ROOT / 'docs/alpha-checklist.md').read_text(encoding='utf-8')
        self.assertEqual('sample:alpha:fixture', package['package_id'])
        self.assertIn('no live provider calls', package['guardrails'])
        self.assertIn('report_v2', package['artifacts'])
        self.assertIn('low-sample conclusions as directional', checklist)


if __name__ == '__main__':
    unittest.main()

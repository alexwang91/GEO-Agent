import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/runAuditContent.js').read_text(encoding='utf-8')


class DesktopRunAuditContentTests(unittest.TestCase):
    def test_run_audit_copy_has_safe_controls(self):
        for phrase in ['Run Audit', 'Set sample count', 'Run fixture audit', 'Run manual import audit', 'Provider unavailable']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('do not make live provider, crawler, or browser calls', CONTENT)


if __name__ == '__main__':
    unittest.main()

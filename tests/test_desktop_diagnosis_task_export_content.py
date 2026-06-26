import unittest
from pathlib import Path

CONTENT = (Path(__file__).resolve().parents[1] / 'apps/desktop/src/diagnosisTaskExportContent.js').read_text(encoding='utf-8')

class DesktopDiagnosisTaskExportContentTests(unittest.TestCase):
    def test_required_copy_exists(self):
        self.assertIn('Diagnosis and Task Plan', CONTENT)
        self.assertIn('Priority score', CONTENT)
        self.assertIn('Export JSON', CONTENT)
        self.assertIn('Create retest plan', CONTENT)

if __name__ == '__main__':
    unittest.main()

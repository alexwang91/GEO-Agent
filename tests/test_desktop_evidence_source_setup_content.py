import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/evidenceSourceSetupContent.js').read_text(encoding='utf-8')


class DesktopEvidenceSourceSetupContentTests(unittest.TestCase):
    def test_evidence_setup_guardrails_exist(self):
        for phrase in ['Evidence Source Setup', 'Manual import', 'Browser capture artifact', 'Rendered HTML fallback']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('Do not add live credentials', CONTENT)
        self.assertIn('Planned providers remain planned', CONTENT)


if __name__ == '__main__':
    unittest.main()

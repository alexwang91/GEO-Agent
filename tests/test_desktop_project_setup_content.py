import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / 'apps/desktop/src/projectSetupContent.js').read_text(encoding='utf-8')


class DesktopProjectSetupContentTests(unittest.TestCase):
    def test_project_setup_fields_and_validation_copy_exist(self):
        for phrase in ['Project Setup', 'Brand name', 'Domain', 'Competitors', 'Business goal']:
            self.assertIn(phrase, CONTENT)
        self.assertIn('planned providers are not live coverage', CONTENT)
        self.assertIn('Save project profile', CONTENT)


if __name__ == '__main__':
    unittest.main()

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"


class V10UIBrandPreviewTests(unittest.TestCase):
    def test_brand_form_has_nine_fields_and_preview(self):
        source = APP.read_text(encoding="utf-8")

        fields_match = re.search(r"const brandProfileFields = \[(.*?)\];", source, re.S)
        self.assertIsNotNone(fields_match)
        self.assertEqual(fields_match.group(1).count("["), 9)
        self.assertIn("Generate query preview", source)
        self.assertIn("queryPreview.map", source)
        self.assertIn("This step does not run providers", source)
        self.assertIn("No per-engine breakdown found", source)
        self.assertIn("Owned citation share", source)


if __name__ == "__main__":
    unittest.main()

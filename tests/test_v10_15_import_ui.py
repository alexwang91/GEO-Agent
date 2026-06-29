import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"
HELPER = ROOT / "apps" / "desktop" / "src" / "manualCaptureArtifacts.js"


class V10ImportUITests(unittest.TestCase):
    def test_capture_import_ui_has_validation_and_engine_summary(self):
        helper = HELPER.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")

        self.assertIn("Manual Capture", app)
        self.assertIn("Load manual capture JSON", app)
        self.assertIn("Validation error", app)
        self.assertIn("Evidence note", app)
        self.assertIn("does not run live providers", app)
        self.assertIn("not auto-capturable", helper)
        self.assertIn("Multi-engine manual capture package detected", helper)
        self.assertIn("engines", helper)
        self.assertIn("geo-agent capture-package", helper)


if __name__ == "__main__":
    unittest.main()

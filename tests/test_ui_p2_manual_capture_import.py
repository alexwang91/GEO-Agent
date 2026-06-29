import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"
HELPER = ROOT / "apps" / "desktop" / "src" / "manualCaptureArtifacts.js"
STYLES = ROOT / "apps" / "desktop" / "src" / "styles.css"


class UIP2ManualCaptureImportTests(unittest.TestCase):
    def test_manual_capture_helper_validates_package_boundaries(self):
        source = HELPER.read_text(encoding="utf-8")

        self.assertIn("emptyManualCaptureView", source)
        self.assertIn("loadManualCaptureViewFromFile", source)
        self.assertIn("buildManualCaptureView", source)
        self.assertIn("Missing profile object", source)
        self.assertIn("Missing captures array", source)
        self.assertIn("answer_text/raw_answer", source)
        self.assertIn("Google AIO is manual-only", source)
        self.assertIn("not auto-capturable", source)
        self.assertIn("geo-agent capture-package captures.json --out out/manual-package", source)

    def test_app_exposes_manual_capture_as_first_class_workflow(self):
        source = APP.read_text(encoding="utf-8")

        self.assertIn("Manual Capture", source)
        self.assertIn("id=\"manual-capture\"", source)
        self.assertIn("loadManualCaptureViewFromFile", source)
        self.assertIn("handleManualCaptureFile", source)
        self.assertIn("ManualCaptureSummary", source)
        self.assertIn("Load manual capture JSON", source)
        self.assertIn("Google AIO remains manual-only", source)
        self.assertIn("does not run live providers", source)
        self.assertIn("Validation error", source)
        self.assertIn("Evidence note", source)

    def test_manual_capture_styles_are_present(self):
        styles = STYLES.read_text(encoding="utf-8")

        self.assertIn("code", styles)
        self.assertIn(".status.manual-import", styles)


if __name__ == "__main__":
    unittest.main()

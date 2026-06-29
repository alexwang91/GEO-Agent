import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "desktop" / "src" / "App.jsx"
STYLES = ROOT / "apps" / "desktop" / "src" / "styles.css"


class UIP1BrandQueryPreviewTests(unittest.TestCase):
    def test_app_contains_editable_brand_profile_state_and_fields(self):
        source = APP.read_text(encoding="utf-8")

        self.assertIn("defaultBrandProfile", source)
        self.assertIn("brandProfileFields", source)
        self.assertIn("handleBrandProfileChange", source)
        self.assertIn("handleGenerateQueries", source)
        self.assertIn("setQueryPreview(buildQueryPreview(brandProfile))", source)
        for field in ["brand", "domain", "competitors", "region", "language", "targetCustomer", "mainProduct", "category", "businessGoal"]:
            self.assertIn(field, source)

    def test_query_preview_uses_natural_comparison_and_alternatives_copy(self):
        source = APP.read_text(encoding="utf-8")

        self.assertIn("Compare ${profile.brand} with ${competitors}", source)
        self.assertIn("Best alternatives to ${profile.brand}: ${competitors}", source)
        self.assertIn("Generate query preview", source)
        self.assertIn("Reset Huawei example", source)
        self.assertIn("queryPreview.map", source)
        self.assertNotIn("vs ${competitors} for ${profile.mainProduct}", source)

    def test_desktop_styles_support_profile_form_and_query_cards(self):
        styles = STYLES.read_text(encoding="utf-8")

        self.assertIn(".form-grid", styles)
        self.assertIn(".field", styles)
        self.assertIn(".query-list", styles)
        self.assertIn(".query-card", styles)
        self.assertIn("input", styles)


if __name__ == "__main__":
    unittest.main()

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_ACCESS = ROOT / "src" / "geo_agent" / "provider_access.py"
STATUS_RE = re.compile(r"implementation_status=\"(?P<status>[a-z_]+)\"")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def provider_status_literal_values():
    tree = ast.parse(PROVIDER_ACCESS.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "ProviderStatus":
                    literal = node.value.slice if isinstance(node.value, ast.Subscript) else None
                    return {value.value for value in literal.elts if isinstance(value, ast.Constant)}
    raise AssertionError("ProviderStatus literal not found")


def registry_status_values():
    text = PROVIDER_ACCESS.read_text(encoding="utf-8")
    return set(re.findall(r'ProviderDefinition\([^\n]+, "(?P<status>[a-z_]+)"\)', text))


class ProductContractDocsTest(unittest.TestCase):
    def test_required_docs_exist(self):
        for path in ["docs/product-contract.md", "docs/provider-status-language.md", "docs/limitations.md"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_provider_status_docs_match_registry(self):
        literal_values = provider_status_literal_values()
        registry_values = registry_status_values()
        status_doc = read("docs/provider-status-language.md")

        self.assertEqual({"implemented", "planned"}, literal_values)
        self.assertTrue(registry_values <= literal_values)
        for status in literal_values:
            self.assertIn(f"`{status}`", status_doc)
        for status in registry_values:
            self.assertIn(f"`{status}`", status_doc)

    def test_readme_docs_and_ui_use_consistent_status_language(self):
        readme = read("README.md")
        status_doc = read("docs/provider-status-language.md")
        ui = read("apps/desktop/src/App.jsx")

        for phrase in ["OpenAI-compatible API output is not ChatGPT Search", "Planned providers"]:
            self.assertIn(phrase, readme)
        for phrase in ["OpenAI-compatible", "not ChatGPT Search", "implemented", "planned"]:
            self.assertIn(phrase, status_doc)
        for phrase in ["Implemented", "Planned", "not ChatGPT Search"]:
            self.assertIn(phrase, ui)

        forbidden_ui_statuses = ["Configured boundary", "Fake/test available", "Available"]
        for phrase in forbidden_ui_statuses:
            self.assertNotIn(f"status: '{phrase}'", ui)

    def test_product_contract_and_limitations_prevent_overclaims(self):
        product_contract = read("docs/product-contract.md")
        limitations = read("docs/limitations.md")
        combined = product_contract + "\n" + limitations

        required_phrases = [
            "does not guarantee ranking improvement",
            "OpenAI-compatible API output is not ChatGPT Search",
            "single-sample",
            "Planned providers must remain labeled planned",
            "Raw API keys",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, combined)


if __name__ == "__main__":
    unittest.main()

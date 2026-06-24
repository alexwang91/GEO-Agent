import json
import unittest
from pathlib import Path


class RecordedDatasetSchemaTests(unittest.TestCase):
    def test_schema_and_canonical_example_align_on_required_sections(self):
        repo_root = Path(__file__).resolve().parents[1]
        schema = json.loads((repo_root / "schemas" / "recorded-dataset.schema.json").read_text(encoding="utf-8"))
        example = json.loads((repo_root / "examples" / "acme-fixture.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["title"], "Recorded GEO Audit Dataset")
        self.assertEqual(schema["required"], ["profile", "pages", "audit", "recorded_runs"])
        for section in schema["required"]:
            self.assertIn(section, example)

        profile_required = schema["properties"]["profile"]["required"]
        for field in profile_required:
            self.assertIn(field, example["profile"])

        recorded_required = schema["properties"]["recorded_runs"]["required"]
        for field in recorded_required:
            self.assertIn(field, example["recorded_runs"])

    def test_schema_docs_reference_canonical_fixture(self):
        repo_root = Path(__file__).resolve().parents[1]
        docs = (repo_root / "docs" / "recorded-dataset-schema.md").read_text(encoding="utf-8")

        self.assertIn("schemas/recorded-dataset.schema.json", docs)
        self.assertIn("examples/acme-fixture.json", docs)
        self.assertIn("profile", docs)
        self.assertIn("recorded_runs", docs)


if __name__ == "__main__":
    unittest.main()

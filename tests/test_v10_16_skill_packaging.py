import unittest
from pathlib import Path

from geo_agent.skill_packaging import validate_skill_package

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "geo-rewrite-skill"


class V10SkillPackagingTests(unittest.TestCase):
    def test_skill_package_manifest_is_valid(self):
        result = validate_skill_package(SKILL).to_dict()

        self.assertEqual(result["name"], "geo-rewrite-skill")
        self.assertEqual(result["version"], "0.1.0")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()

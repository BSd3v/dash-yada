from pathlib import Path
import unittest


class TestChangelog(unittest.TestCase):
    def test_changelog_has_unreleased_entry(self):
        changelog_path = Path(__file__).resolve().parents[1] / "CHANGELOG.md"
        self.assertTrue(changelog_path.exists(), "CHANGELOG.md is missing")

        changelog = changelog_path.read_text(encoding="utf-8")
        self.assertIn("## [Unreleased]", changelog)
        self.assertIn("Add baseline `unittest` coverage for `YadaAIO`", changelog)


if __name__ == "__main__":
    unittest.main()

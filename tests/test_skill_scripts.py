from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
FIXTURES = ROOT / "tests" / "fixtures"


def run_python(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, *args],
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillScriptTests(unittest.TestCase):
    def test_discover_skills_detects_formats_and_filters_hidden_duplicates(self) -> None:
        fixture_root = FIXTURES / "skill-sources"

        result = run_python(
            "scripts/discover-skills.py",
            "--agent-dir",
            str(fixture_root),
            "--format",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        sources = {entry["name"]: entry["format"] for entry in json.loads(result.stdout)}
        self.assertEqual(sources["catalog-root"], "CATALOG")
        self.assertEqual(sources["planning-pack"], "FOLDER")
        self.assertEqual(sources["workflow-skill"], "WORKFLOW")
        self.assertEqual(sources["readme-root"], "README")
        self.assertEqual(sources["search-root"], "SEARCH_ENGINE")
        self.assertNotIn("workflows", sources)

        search_result = run_python(
            "scripts/discover-skills.py",
            "--agent-dir",
            str(fixture_root),
            "--keywords",
            "python",
            "planning",
            "workflow",
            "docs",
        )
        self.assertEqual(search_result.returncode, 0, search_result.stderr)

        matches = json.loads(search_result.stdout)
        paths = {Path(item["path"]) for item in matches}

        self.assertIn(
            fixture_root / "catalog-root" / "skills" / "nested" / "python-pro" / "SKILL.md",
            paths,
        )
        self.assertIn(
            fixture_root / "planning-pack" / "skills" / "planning-with-files" / "SKILL.md",
            paths,
        )
        self.assertNotIn(
            fixture_root
            / "planning-pack"
            / ".codex"
            / "skills"
            / "planning-with-files"
            / "SKILL.md",
            paths,
        )
        self.assertIn(fixture_root / "workflow-skill" / "CLAUDE.md", paths)
        self.assertIn(fixture_root / "readme-root" / "README.md", paths)
        self.assertIn(fixture_root / "search-root" / "found" / "SKILL.md", paths)

        search_hit = next(
            item for item in matches if item["path"].endswith("search-root\\found\\SKILL.md")
        )
        self.assertGreater(search_hit["score"], 0)
        self.assertEqual(search_hit["matched_keywords"], ["workflow"])

    def test_extract_capabilities_parses_frontmatter_lists(self) -> None:
        skill_path = FIXTURES / "sample-skill" / "SKILL.md"

        result = run_python("scripts/extract-capabilities.py", str(skill_path))
        self.assertEqual(result.returncode, 0, result.stderr)

        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["title"], "Sample Skill")
        self.assertEqual(payload[0]["capability"], "Capability summary")
        self.assertEqual(payload[0]["tools"], ["Read", "Edit", "claude", "cursor"])

    def test_wizard_generates_rules_file_without_unicode_console_issues(self) -> None:
        wizard_module = load_module(ROOT / "scripts" / "wizard.py", "wizard_module")
        wizard = wizard_module.ConfigWizard()
        answers = iter(["1,5", "2", "", "1,4", "3", "y", "42"])
        captured_yaml: dict[str, str] = {}

        def fake_write_text(self, content: str, encoding: str = "utf-8") -> int:
            captured_yaml[str(self)] = content
            return len(content)

        with mock.patch("builtins.input", side_effect=lambda _prompt="": next(answers)):
            with mock.patch.object(Path, "write_text", autospec=True, side_effect=fake_write_text):
                with mock.patch("sys.stdout", new=io.StringIO()) as stdout:
                    wizard.run()
                    output = stdout.getvalue()

        self.assertTrue(output.isascii())
        config_text = captured_yaml[".rulesrc.yaml"]
        self.assertIn("  - cursor", config_text)
        self.assertIn("  - codex", config_text)
        self.assertIn("    - security", config_text)
        self.assertIn("    - performance", config_text)
        self.assertIn("template_style: minimal", config_text)
        self.assertIn("quality_threshold: 42", config_text)
        self.assertIn("preview_mode: true", config_text)


if __name__ == "__main__":
    unittest.main()

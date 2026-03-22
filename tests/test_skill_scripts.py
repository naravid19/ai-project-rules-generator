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

        sources = {entry["name"]: entry for entry in json.loads(result.stdout)}
        self.assertEqual(sources["catalog-root"]["format"], "CATALOG")
        self.assertEqual(sources["planning-pack"]["format"], "FOLDER")
        self.assertEqual(sources["workflow-skill"]["format"], "WORKFLOW")
        self.assertEqual(sources["readme-root"]["format"], "README")
        self.assertEqual(sources["search-root"]["format"], "SEARCH_ENGINE")
        self.assertEqual(sources["agents-only-root"]["format"], "FOLDER")
        self.assertEqual(sources["hybrid-root"]["format"], "FOLDER")
        self.assertNotIn("workflows", sources)
        self.assertEqual(sources["planning-pack"]["source_root"], str(fixture_root))

        search_result = run_python(
            "scripts/discover-skills.py",
            "--agent-dir",
            str(fixture_root),
            "--keywords",
            "python",
            "planning",
            "workflow",
            "react",
            "quality",
            "docs",
        )
        self.assertEqual(search_result.returncode, 0, search_result.stderr)

        matches = json.loads(search_result.stdout)
        by_path = {Path(item["path"]): item for item in matches}

        catalog_path = fixture_root / "catalog-root" / "skills" / "nested" / "python-pro" / "SKILL.md"
        planning_path = (
            fixture_root / "planning-pack" / "skills" / "planning-with-files" / "SKILL.md"
        )
        agents_only_path = (
            fixture_root / "agents-only-root" / "skills" / "react-quality" / "AGENTS.md"
        )
        hybrid_path = (
            fixture_root / "hybrid-root" / "skills" / "react-composition" / "SKILL.md"
        )
        workflow_path = fixture_root / "workflow-skill" / "CLAUDE.md"
        readme_path = fixture_root / "readme-root" / "README.md"
        search_path = fixture_root / "search-root" / "found" / "SKILL.md"

        self.assertIn(catalog_path, by_path)
        self.assertIn(planning_path, by_path)
        self.assertIn(agents_only_path, by_path)
        self.assertIn(hybrid_path, by_path)
        self.assertIn(workflow_path, by_path)
        self.assertIn(readme_path, by_path)
        self.assertIn(search_path, by_path)
        self.assertNotIn(
            fixture_root / "planning-pack" / ".codex" / "skills" / "planning-with-files" / "SKILL.md",
            by_path,
        )

        planning_match = by_path[planning_path]
        self.assertEqual(planning_match["instruction_type"], "SKILL.md")
        self.assertEqual(planning_match["source_root"], str(fixture_root))
        self.assertEqual(
            {Path(path).name for path in planning_match["companion_docs"]},
            {"AGENTS.md", "README.md"},
        )

        agents_only_match = by_path[agents_only_path]
        self.assertEqual(agents_only_match["instruction_type"], "AGENTS.md")
        self.assertEqual(agents_only_match["companion_docs"], [])

        hybrid_match = by_path[hybrid_path]
        self.assertEqual(hybrid_match["instruction_type"], "SKILL.md")
        self.assertEqual(
            {Path(path).name for path in hybrid_match["companion_docs"]},
            {"AGENTS.md", "README.md"},
        )

        planning_matches = [item for item in matches if "planning-pack" in item["path"]]
        self.assertEqual(len(planning_matches), 1)

        search_hit = next(item for item in matches if item["path"].endswith("search-root\\found\\SKILL.md"))
        self.assertGreater(search_hit["score"], 0)
        self.assertEqual(search_hit["matched_keywords"], ["workflow"])

    def test_discover_skills_honors_multiple_agent_dirs_and_root_precedence(self) -> None:
        secondary_root = FIXTURES / "skill-sources-secondary"
        primary_root = FIXTURES / "skill-sources"

        result = run_python(
            "scripts/discover-skills.py",
            "--agent-dir",
            str(secondary_root),
            "--agent-dir",
            str(primary_root),
            "--format",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        sources = {entry["name"]: entry for entry in json.loads(result.stdout)}
        self.assertEqual(sources["planning-pack"]["source_root"], str(secondary_root))
        self.assertEqual(sources["secondary-only"]["source_root"], str(secondary_root))
        self.assertEqual(sources["catalog-root"]["source_root"], str(primary_root))

        search_result = run_python(
            "scripts/discover-skills.py",
            "--agent-dir",
            str(secondary_root),
            "--agent-dir",
            str(primary_root),
            "--keywords",
            "planning",
            "api",
            "quality",
        )
        self.assertEqual(search_result.returncode, 0, search_result.stderr)

        matches = json.loads(search_result.stdout)
        paths = {Path(item["path"]) for item in matches}
        self.assertIn(
            secondary_root / "planning-pack" / "skills" / "planning-with-files" / "SKILL.md",
            paths,
        )
        self.assertNotIn(
            primary_root / "planning-pack" / "skills" / "planning-with-files" / "SKILL.md",
            paths,
        )
        self.assertIn(
            secondary_root / "secondary-only" / "skills" / "api-quality" / "AGENTS.md",
            paths,
        )

    def test_extract_capabilities_supports_directory_inputs_and_companion_metadata(self) -> None:
        result = run_python(
            "scripts/extract-capabilities.py",
            str(FIXTURES / "sample-skill"),
            str(FIXTURES / "skill-sources" / "agents-only-root" / "skills" / "react-quality" / "AGENTS.md"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        payload = json.loads(result.stdout)
        sample_capability = next(
            item for item in payload if item["path"].endswith("tests\\fixtures\\sample-skill\\SKILL.md")
        )
        self.assertEqual(sample_capability["title"], "Sample Skill")
        self.assertEqual(sample_capability["capability"], "Capability summary")
        self.assertEqual(sample_capability["tools"], ["Read", "Edit", "claude", "cursor"])
        self.assertEqual({Path(path).name for path in sample_capability["companion_docs"]}, {"AGENTS.md"})
        self.assertEqual(
            {Path(path).name for path in sample_capability["reference_dirs"]},
            {"references", "rules"},
        )

        agents_only_capability = next(
            item for item in payload if item["path"].endswith("react-quality\\AGENTS.md")
        )
        self.assertEqual(agents_only_capability["title"], "React Quality Guardrails")
        self.assertIn("React code", agents_only_capability["capability"])
        self.assertEqual(agents_only_capability["companion_docs"], [])
        self.assertEqual(agents_only_capability["reference_dirs"], [])

    def test_wizard_generates_rules_file_without_unicode_console_issues(self) -> None:
        wizard_module = load_module(ROOT / "scripts" / "wizard.py", "wizard_module")
        wizard = wizard_module.ConfigWizard()
        answers = iter(
            [
                "1,5",
                "2",
                "",
                "1,4",
                "3",
                "y",
                "y",
                r"C:\Users\narav\Desktop\CE code\Tools\.agent",
                "42",
            ]
        )
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
        self.assertIn('  - path: "C:/Users/narav/Desktop/CE code/Tools/.agent"', config_text)
        self.assertIn("  - path: .agent", config_text)


if __name__ == "__main__":
    unittest.main()

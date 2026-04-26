from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SCRIPTS_DIR = ROOT / "scripts"


def load_module(module_path: Path, module_name: str):
    module_dir = str(module_path.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RuntimeFeatureTests(unittest.TestCase):
    def test_rules_config_parses_confirmed_skill_sources_and_thresholds(self) -> None:
        rules_config = load_module(SCRIPTS_DIR / "rules_config.py", "rules_config_module")

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / ".rulesrc.yaml"
            config_path.write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: "C:/skills/shared"
                        format: FOLDER
                        confirmed: true
                      - path: .agent
                        confirmed: false
                    quality_threshold: 42
                    confidence_threshold: 80
                    skill_match_limit: 5
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            payload = rules_config.load_rules_config(config_path)
            sources = payload["skill_sources"]

            self.assertEqual(len(sources), 2)
            self.assertEqual(sources[0].path, "C:/skills/shared")
            self.assertEqual(sources[0].format, "FOLDER")
            self.assertTrue(sources[0].confirmed)
            self.assertFalse(sources[1].confirmed)
            self.assertEqual(payload["quality_threshold"], 42)
            self.assertEqual(payload["confidence_threshold"], 80)
            self.assertEqual(payload["skill_match_limit"], 5)

    def test_project_runtime_requires_one_existing_confirmed_skill_source(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py",
            "project_rules_runtime_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            skill_root = project_root / ".agent"
            skill_root.mkdir(parents=True)
            (project_root / ".rulesrc.yaml").write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: .agent
                        confirmed: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            confirmed = runtime_module.resolve_confirmed_skill_source(project_root)
            self.assertEqual(confirmed.configured_path, ".agent")
            self.assertEqual(confirmed.resolved_path, skill_root.resolve())
            self.assertIn(".agent", runtime_module.build_context_injection(".agent"))

            (project_root / ".rulesrc.yaml").write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: missing-root
                        confirmed: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(runtime_module.ProjectRulesRuntimeError):
                runtime_module.resolve_confirmed_skill_source(project_root)

    def test_confidence_gate_flags_ambiguous_projects(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py",
            "project_rules_runtime_confidence_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "package.json").write_text('{"dependencies":{"react":"18.0.0"}}', encoding="utf-8")
            (project_root / "pyproject.toml").write_text("[project]\nname='mixed'\n", encoding="utf-8")
            (project_root / "App.tsx").write_text("export function App() { return null; }\n", encoding="utf-8")
            (project_root / "app.py").write_text("print('hi')\n", encoding="utf-8")

            result = runtime_module.score_project_confidence(project_root, threshold=80)
            self.assertTrue(result.requires_clarification)
            self.assertGreater(len(result.clarification_options), 0)

    def test_audit_logger_writes_project_local_log_and_memory_summary(self) -> None:
        audit_module = load_module(SCRIPTS_DIR / "audit.py", "audit_module")

        @audit_module.audit_logger(action="generate-rules", platform="codex")
        def fake_generation(**_kwargs):
            return {
                "matched_skill_paths": [".agent/skills/testing/SKILL.md"],
                "output_files": [".cursorrules", "AGENTS.md"],
                "verification_status": "pending",
            }

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            fake_generation(
                project_root=project_root,
                confirmed_skill_source_path=".agent",
                selected_keywords=["testing", "memory"],
                confidence_score=88,
            )

            log_files = list((project_root / ".agent" / "logs").glob("log_*.json"))
            self.assertEqual(len(log_files), 1)

            payload = json.loads(log_files[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["action"], "generate-rules")
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["confirmed_skill_source_path"], ".agent")
            self.assertEqual(payload["matched_skill_paths"], [".agent/skills/testing/SKILL.md"])

            summary_path = project_root / ".agent" / "memory" / "project_state.md"
            self.assertTrue(summary_path.exists())
            summary = summary_path.read_text(encoding="utf-8")
            self.assertIn("Project State", summary)
            self.assertIn("generate-rules", summary)
            self.assertNotIn('"action"', summary)

    def test_traceability_helper_rejects_fake_paths(self) -> None:
        traceability_module = load_module(SCRIPTS_DIR / "traceability.py", "traceability_module")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / ".agent").mkdir()
            (project_root / ".rulesrc.yaml").write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: .agent
                        confirmed: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            metadata = traceability_module.extract_traceability_metadata(
                "<!-- Skill_Source_Path: .agent -->\n<!-- Confirmed_Skill_Source: true -->\n"
            )
            self.assertEqual(
                traceability_module.validate_traceability_metadata(project_root, metadata),
                [],
            )

            fake_metadata = traceability_module.extract_traceability_metadata(
                "<!-- Skill_Source_Path: fake-root -->\n<!-- Confirmed_Skill_Source: true -->\n"
            )
            errors = traceability_module.validate_traceability_metadata(project_root, fake_metadata)
            self.assertIn("Traceability path does not exist in the filesystem.", errors)

    def test_powershell_validator_rejects_missing_traceability_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / ".rulesrc.yaml").write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: .agent
                        confirmed: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            (project_root / ".cursorrules").write_text(
                textwrap.dedent(
                    """
                    <!-- Skill_Source_Path: fake-root -->
                    <!-- Confirmed_Skill_Source: true -->
                    # Project Rules: Sample

                    ## Project Identity
                    - **Type**: CLI

                    ## Project Structure
                    | Path | Purpose |
                    | --- | --- |
                    | `scripts/` | utilities |

                    ## Coding Standards
                    Example.

                    ## Critical Rules
                    Good / Bad.

                    ## Code Smells
                    | Smell | Instead Do |
                    | --- | --- |
                    | bad | good |
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            (project_root / "AGENTS.md").write_text(
                textwrap.dedent(
                    """
                    <!-- Skill_Source_Path: fake-root -->
                    <!-- Confirmed_Skill_Source: true -->
                    # AI Agent Guidelines - Sample

                    ## Quick Context
                    Example context.

                    ## Skills
                    Example.

                    ## Output
                    Example.

                    ## Patterns
                    Example.

                    ## Constraints
                    Example.

                    [Native MCP Servers]
                    None

                    [Local Agent Skills]
                    Use the confirmed directory only.
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ROOT / "scripts" / "validate-output.ps1"),
                    "-Path",
                    str(project_root),
                    "-Threshold",
                    "0",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            combined = f"{completed.stdout}\n{completed.stderr}"
            self.assertNotEqual(completed.returncode, 0, combined)
            self.assertIn("traceability path does not exist on disk", combined)

    def test_extract_design_tokens_parses_tailwind_and_css(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py",
            "project_rules_runtime_design_tokens_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Create tailwind.config.js
            (project_root / "tailwind.config.js").write_text(
                textwrap.dedent(
                    """
                    module.exports = {
                      theme: {
                        extend: {
                          colors: {
                            "primary": "#496559",
                            "secondary": "rgba(255, 0, 0, 0.5)",
                          },
                          fontFamily: {
                            "sans": ["Inter", "sans-serif"],
                          }
                        }
                      }
                    }
                    """
                ).strip(),
                encoding="utf-8",
            )
            
            # Create a CSS file
            src_dir = project_root / "src"
            src_dir.mkdir()
            (src_dir / "globals.css").write_text(
                textwrap.dedent(
                    """
                    :root {
                      --brand-color: #00ff00;
                      --spacing-unit: 1rem;
                    }
                    """
                ).strip(),
                encoding="utf-8",
            )
            
            tokens = runtime_module.extract_design_tokens(project_root)
            
            self.assertEqual(tokens["colors"]["primary"], "#496559")
            self.assertEqual(tokens["colors"]["secondary"], "rgba(255, 0, 0, 0.5)")
            self.assertEqual(tokens["fonts"]["sans"], ["Inter", "sans-serif"])
            self.assertEqual(tokens["colors"]["--brand-color"], "#00ff00")
            self.assertEqual(tokens["spacing"]["--spacing-unit"], "1rem")


if __name__ == "__main__":
    unittest.main()

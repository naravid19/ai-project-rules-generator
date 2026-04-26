from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


class ArchitectureTests(unittest.TestCase):
    def test_indexer_writes_lightweight_catalog(self) -> None:
        indexer_module = load_module(SCRIPTS_DIR / "indexer.py", "indexer_module")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            shared_root = project_root / ".agent"
            skill_dir = shared_root / "planning-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                textwrap.dedent(
                    """
                    ---
                    name: planning-skill
                    description: Planning workflow for API projects
                    ---

                    # Planning Skill

                    Use for planning, workflow design, and API architecture.
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
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

            catalog_path = indexer_module.build_skill_catalog(project_root)
            self.assertEqual(catalog_path, project_root / ".agent" / "memory" / "skill_catalog.json")

            payload = json.loads(catalog_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload), 1)
            item = payload[0]
            self.assertEqual(set(item.keys()), {"id", "path", "tags", "description"})
            self.assertEqual(item["id"], "planning-skill")
            self.assertEqual(item["path"], ".agent/planning-skill/SKILL.md")
            self.assertIn("planning", item["tags"])
            self.assertIn("workflow", item["tags"])
            self.assertTrue(item["description"])

    def test_indexer_supports_confirmed_shared_root_outside_project(self) -> None:
        indexer_module = load_module(SCRIPTS_DIR / "indexer.py", "indexer_shared_module")

        with tempfile.TemporaryDirectory() as project_dir, tempfile.TemporaryDirectory() as shared_dir:
            project_root = Path(project_dir)
            shared_root = Path(shared_dir)
            skill_dir = shared_root / "security-skill"
            skill_dir.mkdir(parents=True)
            skill_path = skill_dir / "SKILL.md"
            skill_path.write_text(
                textwrap.dedent(
                    """
                    ---
                    name: security-skill
                    description: Security reviews for API and audit workflows
                    ---
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            (project_root / ".rulesrc.yaml").write_text(
                textwrap.dedent(
                    f"""
                    skill_sources:
                      - path: "{shared_root.as_posix()}"
                        confirmed: true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            catalog_path = indexer_module.build_skill_catalog(project_root)
            payload = json.loads(catalog_path.read_text(encoding="utf-8"))
            self.assertEqual(payload[0]["path"], skill_path.resolve().as_posix())

    def test_lib_wrappers_expose_runtime_helpers(self) -> None:
        config_runtime = load_module(
            SCRIPTS_DIR / "lib" / "config_runtime.py",
            "config_runtime_module",
        )
        confidence_module = load_module(
            SCRIPTS_DIR / "lib" / "confidence.py",
            "confidence_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / ".agent").mkdir()
            config_path = project_root / ".rulesrc.yaml"
            config_path.write_text(
                textwrap.dedent(
                    """
                    skill_sources:
                      - path: .agent
                        confirmed: true
                    confidence_threshold: 80
                    skill_match_limit: 5
                    project_intent_override: frontend
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            payload = config_runtime.load_runtime_config(config_path)
            self.assertEqual(payload["confidence_threshold"], 80)
            self.assertEqual(payload["skill_match_limit"], 5)
            self.assertEqual(payload["project_intent_override"], "frontend")

            result = confidence_module.score_project_confidence(project_root, threshold=80)
            self.assertLess(result.score, 80)

    def test_config_runtime_detects_mcp_servers_and_registry_routes(self) -> None:
        config_runtime = load_module(
            SCRIPTS_DIR / "config_runtime.py",
            "config_runtime_root_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            cursor_dir = project_root / ".cursor"
            cursor_dir.mkdir()
            (cursor_dir / "mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "github-mcp": {"command": "github"},
                            "terminal-mcp": {"command": "terminal"},
                        }
                    }
                ),
                encoding="utf-8",
            )

            detected = config_runtime.detect_native_mcp_servers(project_root)
            self.assertEqual(detected, ["github-mcp", "terminal-mcp"])

            registry = config_runtime.load_mcp_registry(ROOT / "templates" / "mcp_registry.yaml")
            routed = config_runtime.route_mcp_servers(
                "Need github automation and terminal access",
                ["python", "api"],
                registry=registry,
            )
            self.assertIn("github-mcp", routed)
            self.assertIn("terminal-mcp", routed)

    def test_jit_loader_only_accepts_catalog_paths_inside_confirmed_root(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py",
            "project_rules_runtime_jit_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            skill_root = project_root / ".agent"
            skill_dir = skill_root / "memory-skill"
            skill_dir.mkdir(parents=True)
            skill_path = skill_dir / "SKILL.md"
            skill_path.write_text("# Memory Skill\n", encoding="utf-8")
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
            catalog_dir = project_root / ".agent" / "memory"
            catalog_dir.mkdir(parents=True)
            catalog_path = catalog_dir / "skill_catalog.json"
            catalog_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "memory-skill",
                            "path": ".agent/memory-skill/SKILL.md",
                            "tags": ["memory"],
                            "description": "Memory support.",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            payload = runtime_module.load_jit_skill_contents(
                project_root,
                [".agent/memory-skill/SKILL.md"],
                limit=5,
            )
            self.assertEqual(payload[0]["path"], skill_path.resolve().as_posix())

            with self.assertRaises(runtime_module.ProjectRulesRuntimeError):
                runtime_module.load_jit_skill_contents(
                    project_root,
                    [".agent/memory-skill/SKILL.md", ".agent/memory-skill/SKILL.md", ".agent/memory-skill/SKILL.md", ".agent/memory-skill/SKILL.md", ".agent/memory-skill/SKILL.md", ".agent/memory-skill/SKILL.md"],
                    limit=5,
                )

    def test_stage1_prompt_and_intent_routing_include_mcp_and_skill_paths(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py",
            "project_rules_runtime_stage1_module",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / ".agent" / "memory").mkdir(parents=True)
            (project_root / ".cursor").mkdir()
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
            (project_root / ".cursor" / "mcp.json").write_text(
                json.dumps({"mcpServers": {"github-mcp": {}, "filesystem-mcp": {}}}),
                encoding="utf-8",
            )
            catalog_path = project_root / ".agent" / "memory" / "skill_catalog.json"
            catalog_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "planning",
                            "path": ".agent/planning/SKILL.md",
                            "tags": ["planning", "workflow"],
                            "description": "Planning workflow guidance.",
                        },
                        {
                            "id": "github",
                            "path": ".agent/github/SKILL.md",
                            "tags": ["github", "api"],
                            "description": "GitHub automation guidance.",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            prompt = runtime_module.build_stage1_selection_prompt(
                "Need github workflow help",
                ["python", "api"],
                catalog_path,
                limit=5,
            )
            self.assertIn("strict JSON array", prompt)
            self.assertIn(".agent/github/SKILL.md", prompt)

            routed = runtime_module.route_intent_resources(
                project_root,
                "Need github workflow help",
                ["python", "api"],
                catalog_path=catalog_path,
                registry_path=ROOT / "templates" / "mcp_registry.yaml",
                limit=5,
            )
            self.assertIn(".agent/github/SKILL.md", routed["selected_skill_paths"])
            self.assertIn("github-mcp", routed["recommended_mcp_servers"])


    def test_merge_monorepo_rules_auto_detects_sub_dirs_and_merges(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py", "runtime_monorepo_module"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create monorepo sub-dirs
            (project_root / "frontend").mkdir()
            (project_root / "backend").mkdir()

            # Add local rules only to frontend
            (project_root / "frontend" / ".cursorrules").write_text(
                "# Frontend rules\nUse React patterns.\n", encoding="utf-8"
            )

            root_rules = "# Universal Rules\nAlways use TypeScript strict mode."

            result = runtime_module.merge_monorepo_rules(project_root, root_rules)

            # Both sub-dirs should be in the output
            self.assertIn("frontend", result)
            self.assertIn("backend", result)

            # frontend should contain both universal AND local rules
            frontend_output = result["frontend"]
            self.assertIn("UNIVERSAL RULES", frontend_output)
            self.assertIn("Always use TypeScript strict mode", frontend_output)
            self.assertIn("LOCAL RULES", frontend_output)
            self.assertIn("Use React patterns", frontend_output)

            # backend should have universal rules only (no local rules file)
            backend_output = result["backend"]
            self.assertIn("UNIVERSAL RULES", backend_output)
            self.assertIn("Always use TypeScript strict mode", backend_output)
            self.assertNotIn("LOCAL RULES", backend_output)

    def test_merge_monorepo_rules_with_apps_packages_containers(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py", "runtime_monorepo_apps_module"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create apps/ container with sub-projects
            (project_root / "apps" / "web").mkdir(parents=True)
            (project_root / "apps" / "api").mkdir(parents=True)
            (project_root / "packages" / "shared").mkdir(parents=True)

            # Add local AGENTS.md to apps/web
            (project_root / "apps" / "web" / "AGENTS.md").write_text(
                "# Web App Rules\nUse Next.js conventions.\n", encoding="utf-8"
            )

            root_rules = "# Root Rules\nEnforce ESLint."

            result = runtime_module.merge_monorepo_rules(project_root, root_rules)

            self.assertIn("apps/web", result)
            self.assertIn("apps/api", result)
            self.assertIn("packages/shared", result)

            # apps/web should have merged content
            web_output = result["apps/web"]
            self.assertIn("UNIVERSAL RULES", web_output)
            self.assertIn("Enforce ESLint", web_output)
            self.assertIn("LOCAL RULES", web_output)
            self.assertIn("Use Next.js conventions", web_output)

    def test_merge_monorepo_rules_returns_empty_for_non_monorepo(self) -> None:
        runtime_module = load_module(
            SCRIPTS_DIR / "project_rules_runtime.py", "runtime_monorepo_empty_module"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            # No sub-project directories at all
            root_rules = "# Root Rules"
            result = runtime_module.merge_monorepo_rules(project_root, root_rules)
            self.assertEqual(result, {})

    def test_audit_log_rotation(self) -> None:
        audit_module = load_module(SCRIPTS_DIR / "audit.py", "audit_module")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            log_dir = project_root / ".agent" / "logs"
            log_dir.mkdir(parents=True)
            for i in range(15):
                (log_dir / f"log_{i:02d}.json").write_text("{}", encoding="utf-8")
            
            audit_module.rotate_audit_logs(log_dir, max_logs=10)
            remaining_logs = list(log_dir.glob("log_*.json"))
            self.assertEqual(len(remaining_logs), 10)

    def test_memory_diff_computation(self) -> None:
        memory_module = load_module(SCRIPTS_DIR / "memory_manager.py", "memory_module")
        old_state = {"action": "plan", "status": "pending", "output_files": ["A"]}
        new_state = {"action": "plan", "status": "success", "output_files": ["A", "B"]}
        
        diff = memory_module.compute_state_diff(old_state, new_state)
        self.assertIn("status", diff)
        self.assertEqual(diff["status"]["old"], "pending")
        self.assertEqual(diff["status"]["new"], "success")
        self.assertIn("output_files", diff)
        self.assertEqual(diff["output_files"]["new"], ["A", "B"])

    def test_indexer_incremental_and_validate(self) -> None:
        indexer_module = load_module(SCRIPTS_DIR / "indexer.py", "indexer_module_inc")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            shared_root = project_root / ".agent"
            skill_dir = shared_root / "test-skill"
            skill_dir.mkdir(parents=True)
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("---\nname: test-skill\n---\n", encoding="utf-8")
            
            (project_root / ".rulesrc.yaml").write_text(
                "skill_sources:\n  - path: .agent\n    confirmed: true\n", encoding="utf-8"
            )
            
            # Initial index
            catalog_path = indexer_module.build_skill_catalog(project_root)
            payload = json.loads(catalog_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload), 1)
            
            # Incremental index with a new skill
            skill2_dir = shared_root / "test-skill-2"
            skill2_dir.mkdir(parents=True)
            (skill2_dir / "SKILL.md").write_text("---\nname: test-skill-2\n---\n", encoding="utf-8")
            
            # This should add the new skill
            indexer_module.build_skill_catalog(project_root, incremental=True)
            payload = json.loads(catalog_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload), 2)
            
            # Delete first skill, validate should remove it
            skill_md.unlink()
            indexer_module.validate_catalog(catalog_path)
            payload = json.loads(catalog_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload), 1)
            self.assertEqual(payload[0]["id"], "test-skill-2")


if __name__ == "__main__":
    unittest.main()

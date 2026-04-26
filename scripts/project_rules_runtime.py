from __future__ import annotations

import importlib.util
import os
import re
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from config_runtime import detect_native_mcp_servers, load_mcp_registry, route_mcp_servers
from rules_config import SkillSourceConfig, load_confirmed_skill_sources

PRIMARY_MANIFESTS = {
    "package.json": ("javascript", "node"),
    "pyproject.toml": ("python", "python"),
    "requirements.txt": ("python", "python"),
    "Cargo.toml": ("rust", "rust"),
    "go.mod": ("go", "go"),
    "pom.xml": ("java", "java"),
    "Gemfile": ("ruby", "ruby"),
}
ENTRYPOINTS = {
    "main.py": "cli",
    "app.py": "backend",
    "manage.py": "backend",
    "index.js": "frontend",
    "index.ts": "frontend",
    "main.ts": "frontend",
    "App.tsx": "frontend",
    "main.go": "backend",
    "lib.rs": "library",
}
TEST_SIGNALS = {
    "pytest.ini": "pytest",
    "jest.config.js": "jest",
    "playwright.config.ts": "playwright",
    "vitest.config.ts": "vitest",
}
WORKFLOW_HIDDEN_DIR_MARKERS = {
    ".adal",
    ".agent",
    ".claude",
    ".codex",
    ".cursor",
    ".gemini",
    ".kiro",
    ".opencode",
}
PRIMARY_ENTRY_FILES = {"SKILL.md", "AGENTS.md", "CLAUDE.md"}
SEARCH_TOOL_CANDIDATES = (
    Path("search.py"),
    Path("scripts") / "search.py",
)


class ProjectRulesRuntimeError(RuntimeError):
    """Raised when enforced runtime constraints fail."""


@dataclass(frozen=True)
class ConfirmedSkillSource:
    configured_path: str
    resolved_path: Path


@dataclass(frozen=True)
class ConfidenceResult:
    score: int
    threshold: int
    reasons: tuple[str, ...]
    clarification_options: tuple[str, ...]
    detected_manifests: tuple[str, ...] = ()
    detected_frameworks: tuple[str, ...] = ()

    @property
    def requires_clarification(self) -> bool:
        return self.score < self.threshold


def resolve_confirmed_skill_source(project_root: Path, config_path: Path | None = None) -> ConfirmedSkillSource:
    root = Path(project_root).resolve()
    rules_config_path = config_path or (root / ".rulesrc.yaml")
    confirmed = load_confirmed_skill_sources(rules_config_path)

    if not confirmed:
        raise ProjectRulesRuntimeError(
            "No confirmed skill source is configured. Confirm one skill source root before generation."
        )

    if len(confirmed) > 1:
        raise ProjectRulesRuntimeError(
            "Multiple confirmed skill sources are configured. Keep exactly one confirmed root."
        )

    entry = confirmed[0]
    resolved = entry.resolved_path(root)
    if not resolved.exists():
        raise ProjectRulesRuntimeError(
            f"Confirmed skill source does not exist: {entry.path}"
        )

    return ConfirmedSkillSource(
        configured_path=entry.path,
        resolved_path=resolved,
    )


def build_context_injection(confirmed_path: Path | str) -> str:
    normalized = _normalize_path_text(confirmed_path)
    return f"CONSTRAINT: You must ONLY retrieve skills from the confirmed directory: {normalized}"


def detect_source_format(source_path: Path) -> str:
    source = Path(source_path)
    if not source.exists():
        return "UNKNOWN"

    if (source / "CATALOG.md").exists() or any(
        candidate.exists()
        for candidate in (
            source / "skills_index.json",
            source / "data" / "skills_index.json",
            source / "catalog.json",
        )
    ):
        return "CATALOG"

    if any((source / candidate).exists() for candidate in SEARCH_TOOL_CANDIDATES):
        return "SEARCH_ENGINE"

    if _has_visible_skill_entities(source):
        return "FOLDER"

    if _is_workflow_root(source):
        return "WORKFLOW"

    if (source / "README.md").exists():
        return "README"

    return "UNKNOWN"


def route_skills(
    project_root: Path,
    keywords: list[str],
    limit: int = 5,
    config_path: Path | None = None,
) -> dict[str, Any]:
    confirmed = resolve_confirmed_skill_source(project_root, config_path=config_path)
    if limit <= 0:
        raise ProjectRulesRuntimeError("skill_match_limit must be greater than zero.")

    discovery_class = _load_skill_discovery_class(Path(__file__).with_name("discover-skills.py"))
    discovery = discovery_class([str(confirmed.resolved_path)])
    matches = discovery.search(keywords, limit=limit)

    return {
        "confirmed_skill_source": _normalize_path_text(confirmed.resolved_path),
        "context_injection": build_context_injection(confirmed.resolved_path),
        "sources": discovery.sources,
        "matches": matches,
    }


def build_stage1_selection_prompt(
    user_intent: str,
    tech_stack: list[str] | tuple[str, ...] | str,
    catalog_path: Path,
    limit: int = 5,
) -> str:
    catalog_entries = _load_catalog_entries(Path(catalog_path))
    tech_stack_line = ", ".join(_normalize_sequence(tech_stack))
    catalog_json = json.dumps(catalog_entries, indent=2)
    return (
        "You are matching user intent against a lightweight skill catalog.\n"
        f"User intent: {user_intent}\n"
        f"Tech stack: {tech_stack_line}\n"
        f"Hard limit: return a strict JSON array of at most {limit} skill paths.\n"
        "Return only JSON, for example: [\"path/one\", \"path/two\"].\n"
        "Do not include explanations.\n"
        f"Catalog:\n{catalog_json}\n"
    )


def parse_stage1_selection_response(raw_response: str, limit: int = 5) -> list[str]:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ProjectRulesRuntimeError("Stage 1 response must be a strict JSON array of paths.") from exc

    if not isinstance(payload, list) or any(not isinstance(item, str) for item in payload):
        raise ProjectRulesRuntimeError("Stage 1 response must be a JSON array of string paths.")
    if len(payload) > limit:
        raise ProjectRulesRuntimeError(f"Stage 1 selected more than {limit} paths.")
    return payload


def route_intent_resources(
    project_root: Path,
    user_intent: str,
    tech_stack: list[str] | tuple[str, ...] | str,
    catalog_path: Path | None = None,
    registry_path: Path | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    effective_catalog = catalog_path or (root / ".agent" / "memory" / "skill_catalog.json")
    catalog_entries = _load_catalog_entries(effective_catalog)
    haystack = " ".join([user_intent.lower(), *(_normalize_sequence(tech_stack))])

    scored_catalog: list[tuple[int, dict[str, Any]]] = []
    for entry in catalog_entries:
        tags = [str(tag).lower() for tag in entry.get("tags", [])]
        description = str(entry.get("description", "")).lower()
        score = sum(1 for tag in tags if tag.replace("-", " ") in haystack)
        if description and any(token in description for token in haystack.split()):
            score += 1
        if score > 0:
            scored_catalog.append((score, entry))

    scored_catalog.sort(key=lambda item: (-item[0], str(item[1].get("path", "")).lower()))
    selected_paths = [str(entry["path"]) for _, entry in scored_catalog[:limit]]

    detected_mcps = detect_native_mcp_servers(root)
    routed_mcps = route_mcp_servers(user_intent, tech_stack, registry=load_mcp_registry(registry_path))
    available_mcps = []
    for server in detected_mcps:
        if server not in available_mcps:
            available_mcps.append(server)

    recommended_mcps = [server for server in routed_mcps if server in available_mcps]

    return {
        "context_injection": build_context_injection(resolve_confirmed_skill_source(root).resolved_path),
        "selected_skill_paths": selected_paths,
        "detected_mcp_servers": available_mcps,
        "recommended_mcp_servers": recommended_mcps,
        "stage1_prompt": build_stage1_selection_prompt(
            user_intent,
            tech_stack,
            effective_catalog,
            limit=limit,
        ),
    }


def select_jit_skill_paths(
    project_root: Path,
    selected_paths: list[str],
    limit: int = 5,
    catalog_path: Path | None = None,
) -> list[Path]:
    root = Path(project_root).resolve()
    if len(selected_paths) > limit:
        raise ProjectRulesRuntimeError(
            f"Selected skill paths exceed the limit {limit}. Reduce the list before loading full content."
        )

    confirmed = resolve_confirmed_skill_source(root)
    effective_catalog_path = catalog_path or (root / ".agent" / "memory" / "skill_catalog.json")
    catalog_entries = _load_catalog_entries(effective_catalog_path)
    allowed_paths = {str(entry.get("path", "")) for entry in catalog_entries}

    resolved: list[Path] = []
    for raw_path in selected_paths:
        if raw_path not in allowed_paths:
            raise ProjectRulesRuntimeError(
                f"Selected path is not present in skill_catalog.json: {raw_path}"
            )

        candidate = Path(raw_path)
        full_path = candidate if candidate.is_absolute() else (root / candidate).resolve()
        if not full_path.exists():
            raise ProjectRulesRuntimeError(f"Selected skill path does not exist: {raw_path}")

        try:
            full_path.relative_to(confirmed.resolved_path)
        except ValueError:
            raise ProjectRulesRuntimeError(
                f"Selected skill path is outside the confirmed skill root: {raw_path}"
            ) from None

        resolved.append(full_path)

    return resolved


def load_jit_skill_contents(
    project_root: Path,
    selected_paths: list[str],
    limit: int = 5,
    catalog_path: Path | None = None,
) -> list[dict[str, str]]:
    resolved_paths = select_jit_skill_paths(
        project_root,
        selected_paths,
        limit=limit,
        catalog_path=catalog_path,
    )
    payload: list[dict[str, str]] = []
    for path in resolved_paths:
        payload.append(
            {
                "path": _normalize_path_text(path),
                "content": path.read_text(encoding="utf-8", errors="ignore"),
            }
        )
    return payload


def score_project_confidence(project_root: Path, threshold: int = 80) -> ConfidenceResult:
    root = Path(project_root).resolve()
    reasons: list[str] = []
    score = 0

    manifests = _find_named_paths(root, PRIMARY_MANIFESTS)
    manifest_names = tuple(path.name for path in manifests)
    if manifests:
        score += 25
        reasons.append(f"Detected manifest files: {', '.join(manifest_names)}")
    else:
        reasons.append("No supported manifest files detected.")

    languages = {PRIMARY_MANIFESTS[path.name][0] for path in manifests if path.name in PRIMARY_MANIFESTS}
    if len(languages) == 1:
        score += 20
        reasons.append(f"Single primary language detected: {next(iter(languages))}.")
    elif len(languages) > 1:
        score += 8
        reasons.append("Multiple primary language signals detected; classification is ambiguous.")
    else:
        reasons.append("No clear primary language detected.")

    entrypoints = _find_named_paths(root, ENTRYPOINTS)
    if entrypoints:
        score += 15
        reasons.append(f"Detected entrypoints: {', '.join(path.name for path in entrypoints[:3])}.")
    else:
        reasons.append("No standard entrypoints detected.")

    frameworks = _detect_framework_signals(root, manifests)
    if frameworks:
        score += 20
        reasons.append(f"Detected frameworks/tools: {', '.join(frameworks)}.")
    else:
        reasons.append("No strong framework/tool signals detected.")

    tests = _find_named_paths(root, TEST_SIGNALS)
    if tests:
        score += 10
        reasons.append(f"Detected test configuration: {', '.join(path.name for path in tests)}.")
    else:
        reasons.append("No test configuration detected.")

    architecture_tags = _detect_architecture_tags(root)
    if architecture_tags:
        score += 10
        reasons.append(f"Detected architecture signals: {', '.join(architecture_tags)}.")

    env_files = []
    for env_name in (".env", ".env.local", "docker-compose.yml", "docker-compose.yaml"):
        if (root / env_name).exists():
            env_files.append(env_name)
    if env_files:
        score += 10
        reasons.append(f"Detected environment/deployment configs: {', '.join(env_files)}.")

    config_files = []
    for cfg in ("tailwind.config.js", "tailwind.config.ts", "next.config.js", "next.config.mjs", "tsconfig.json", "svelte.config.js", "vite.config.ts", "vite.config.js"):
        if (root / cfg).exists():
            config_files.append(cfg)
    if config_files:
        score += 15
        reasons.append(f"Detected project configuration files: {', '.join(config_files)}.")

    # Intent detection (Pattern-based)
    intent_keywords = ("readme", "spec", "instruction", "requirement", "architecture", "plan")
    intent_files = [
        f.name for f in root.iterdir()
        if f.is_file() and any(k in f.name.lower() for k in intent_keywords)
    ]
    if intent_files:
        score += 15
        reasons.append(f"Detected project intent/requirement files: {', '.join(intent_files)}.")

    if len(languages) > 1:
        score -= 10
    if len({ENTRYPOINTS[path.name] for path in entrypoints if path.name in ENTRYPOINTS}) > 1:
        score -= 10

    bounded_score = max(0, min(100, score))
    clarification_options = _build_clarification_options(root, languages, entrypoints, architecture_tags)

    return ConfidenceResult(
        score=bounded_score,
        threshold=threshold,
        reasons=tuple(reasons),
        clarification_options=tuple(clarification_options),
        detected_manifests=manifest_names,
        detected_frameworks=tuple(frameworks),
    )


def enforce_confidence_threshold(project_root: Path, threshold: int = 80) -> ConfidenceResult:
    result = score_project_confidence(project_root, threshold=threshold)
    if result.requires_clarification:
        options = ", ".join(result.clarification_options) or "frontend, backend, cli, ai, monorepo"
        raise ProjectRulesRuntimeError(
            f"Confidence score {result.score} is below the threshold {result.threshold}. "
            f"Pause and ask the user to clarify the project intent. Suggested options: {options}"
        )
    return result


def _normalize_path_text(path_value: Path | str) -> str:
    return str(path_value).replace("\\", "/")


def _find_named_paths(root: Path, candidates: dict[str, Any]) -> list[Path]:
    found: list[Path] = []
    for name in candidates:
        matches = list(root.rglob(name))
        if matches:
            found.extend(matches[:1])
    return found


def _detect_framework_signals(root: Path, manifests: list[Path]) -> list[str]:
    found: list[str] = []
    manifest_names = {path.name for path in manifests}

    package_json = next((path for path in manifests if path.name == "package.json"), None)
    if package_json is not None:
        content = package_json.read_text(encoding="utf-8", errors="ignore").lower()
        for token in ("react", "next", "express", "vite", "playwright", "typescript"):
            if f'"{token}"' in content or f"'{token}'" in content or token in content:
                found.append(token)

    pyproject = next((path for path in manifests if path.name == "pyproject.toml"), None)
    if pyproject is not None:
        content = pyproject.read_text(encoding="utf-8", errors="ignore").lower()
        for token in ("fastapi", "pytest", "django", "flask"):
            if token in content:
                found.append(token)

    if (root / "pnpm-workspace.yaml").exists() or (root / "turbo.json").exists():
        found.append("monorepo")

    if (root / "Dockerfile").exists():
        found.append("docker")

    unique: list[str] = []
    for item in found:
        if item not in unique:
            unique.append(item)
    return unique


def _detect_architecture_tags(root: Path) -> list[str]:
    found: list[str] = []
    if (root / "apps").is_dir() or (root / "packages").is_dir() or (root / "services").is_dir():
        found.append("monorepo")
    if (root / "frontend").is_dir():
        found.append("frontend")
    if (root / "backend").is_dir():
        found.append("backend")
    return found


def _build_clarification_options(
    root: Path,
    languages: set[str],
    entrypoints: list[Path],
    architecture_tags: list[str],
) -> list[str]:
    options: list[str] = []
    if "monorepo" in architecture_tags:
        options.append("monorepo")
    if any(ENTRYPOINTS.get(path.name) == "frontend" for path in entrypoints):
        options.append("frontend")
    if any(ENTRYPOINTS.get(path.name) == "backend" for path in entrypoints):
        options.append("backend")
    if any(ENTRYPOINTS.get(path.name) == "cli" for path in entrypoints):
        options.append("cli")
    if "python" in languages and (root / "notebooks").is_dir():
        options.append("ai")
    if not options:
        options.extend(["frontend", "backend", "cli", "ai"])
    return options


def _load_skill_discovery_class(module_path: Path):
    spec = importlib.util.spec_from_file_location("discover_skills_runtime", module_path)
    if spec is None or spec.loader is None:
        raise ProjectRulesRuntimeError("Unable to load format-based discovery runtime.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SkillDiscovery


def _load_catalog_entries(catalog_path: Path) -> list[dict[str, Any]]:
    if not catalog_path.exists():
        raise ProjectRulesRuntimeError(
            f"Missing skill catalog. Run scripts/indexer.py first: {catalog_path}"
        )

    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProjectRulesRuntimeError(f"Invalid skill catalog JSON: {catalog_path}") from exc

    if not isinstance(payload, list):
        raise ProjectRulesRuntimeError("skill_catalog.json must contain a JSON array.")

    normalized: list[dict[str, Any]] = []
    for entry in payload:
        if isinstance(entry, dict):
            normalized.append(entry)
    return normalized


def _normalize_sequence(value: list[str] | tuple[str, ...] | str) -> list[str]:
    if isinstance(value, str):
        return [value.lower()]
    return [str(item).lower() for item in value]


def _has_visible_skill_entities(source_path: Path) -> bool:
    for root, dirnames, filenames in os.walk(source_path):
        dirnames[:] = [name for name in dirnames if not name.startswith(".")]
        if PRIMARY_ENTRY_FILES & set(filenames):
            return True
    return False


def merge_monorepo_rules(
    project_root: Path,
    root_rules: str,
    *,
    local_rules_map: dict[str, str] | None = None,
    separator: str = "\n\n---\n\n",
) -> dict[str, str]:
    """Merge root-level universal rules with per-directory local rules for monorepo structures.

    Args:
        project_root: Absolute path to the repository root.
        root_rules: The universal rule content (from root AGENTS.md or .cursorrules).
        local_rules_map: Optional mapping of {relative_dir: local_rule_content}.
            If None, the function auto-detects sub-project directories and reads
            any existing .cursorrules or AGENTS.md found within them.
        separator: Markdown separator inserted between universal and local sections.

    Returns:
        A dict mapping each sub-project relative directory to its merged rule content.
        If no sub-projects are detected, returns an empty dict.
    """
    root = Path(project_root).resolve()
    architecture_tags = _detect_architecture_tags(root)

    if "monorepo" not in architecture_tags and not local_rules_map:
        sub_dirs = _collect_sub_project_dirs(root)
        if not sub_dirs:
            return {}
    else:
        sub_dirs = _collect_sub_project_dirs(root)

    if local_rules_map is None:
        local_rules_map = _auto_detect_local_rules(root, sub_dirs)

    merged: dict[str, str] = {}
    for rel_dir, local_content in local_rules_map.items():
        universal_section = (
            f"<!-- [UNIVERSAL RULES — inherited from root] -->\n"
            f"{root_rules}"
        )
        local_section = (
            f"<!-- [LOCAL RULES — {rel_dir}] -->\n"
            f"{local_content}"
        )
        merged[rel_dir] = f"{universal_section}{separator}{local_section}\n"

    for rel_dir in sub_dirs:
        if rel_dir not in merged:
            merged[rel_dir] = (
                f"<!-- [UNIVERSAL RULES — inherited from root] -->\n"
                f"{root_rules}\n"
            )

    return merged


def _collect_sub_project_dirs(root: Path) -> list[str]:
    """Collect relative paths of sub-project directories in a monorepo."""
    sub_dirs: list[str] = []

    for direct_name in ("frontend", "backend"):
        candidate = root / direct_name
        if candidate.is_dir():
            sub_dirs.append(direct_name)

    for container_name in ("apps", "packages", "services"):
        container = root / container_name
        if container.is_dir():
            try:
                for child in sorted(container.iterdir()):
                    if child.is_dir() and not child.name.startswith("."):
                        sub_dirs.append(f"{container_name}/{child.name}")
            except OSError:
                pass

    return sub_dirs


def _auto_detect_local_rules(root: Path, sub_dirs: list[str]) -> dict[str, str]:
    """Read existing local rule files (.cursorrules or AGENTS.md) from sub-project dirs."""
    local_map: dict[str, str] = {}
    for rel_dir in sub_dirs:
        dir_path = root / rel_dir
        for filename in (".cursorrules", "AGENTS.md", "CLAUDE.md"):
            candidate = dir_path / filename
            if candidate.exists():
                try:
                    local_map[rel_dir] = candidate.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    pass
                break
    return local_map


def _is_workflow_root(source_path: Path) -> bool:
    if (source_path / ".shared").exists():
        return True

    root_docs = any((source_path / name).exists() for name in ("AGENTS.md", "CLAUDE.md"))
    if not root_docs:
        return False

    try:
        return any(
            child.is_dir() and (child.name in WORKFLOW_HIDDEN_DIR_MARKERS or child.name.endswith("-plugin"))    
            for child in source_path.iterdir()
        )
    except OSError:
        return False

def extract_design_tokens(project_root: Path) -> dict:
    """Parse tailwind.config.ts/js or CSS custom properties 
    to extract actual design tokens."""
    tokens = {
        "colors": {},
        "fonts": {},
        "spacing": {}
    }
    
    # 1. Search for Tailwind config
    tailwind_files = list(project_root.glob("tailwind.config.*"))
    for tf in tailwind_files:
        try:
            content = tf.read_text(encoding="utf-8", errors="ignore")
            
            # Simple regex for colors: "primary": "#hex"
            color_matches = re.findall(r'[\'"]([a-zA-Z0-9-]+)[\'"]\s*:\s*[\'"](#[a-fA-F0-9]{3,8}|(?:rgb|hsl)a?\([^)]+\))[\'"]', content)
            for name, value in color_matches:
                if name not in tokens["colors"]:
                    tokens["colors"][name] = value
            
            # Fonts: "sans": ["Inter", "sans-serif"]
            font_matches = re.findall(r'[\'"]([a-zA-Z0-9-]+)[\'"]\s*:\s*\[\s*([^\]]+)\s*\]', content)
            for name, value_list in font_matches:
                items = [v.strip().strip("'\"") for v in value_list.split(",")]
                tokens["fonts"][name] = items
        except Exception:
            pass

    # 2. Search for CSS custom properties
    # Scan root and src for CSS files, but limit depth to avoid deep scans
    css_files = []
    for ext in ["*.css", "*.scss"]:
        css_files.extend(list(project_root.glob(ext)))
        css_files.extend(list((project_root / "src").glob(f"**/{ext}")))
    
    for cf in css_files:
        if "node_modules" in cf.parts:
            continue
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
            # --var: value;
            props = re.findall(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', content)
            for name, value in props:
                v = value.strip()
                if v.startswith("#") or v.startswith("rgb") or v.startswith("hsl"):
                    tokens["colors"][name] = v
                elif "font" in name.lower():
                    tokens["fonts"][name] = v
                elif any(k in name.lower() for k in ["spacing", "gap", "padding", "margin"]):
                    tokens["spacing"][name] = v
        except Exception:
            pass

    return tokens

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Project Rules Runtime Helpers")
    parser.add_argument("--root", type=str, default=".", help="Project root directory")
    parser.add_argument("--extract-tokens", action="store_true", help="Extract design tokens")
    
    args = parser.parse_args()
    root_path = Path(args.root)
    
    if args.extract_tokens:
        tokens = extract_design_tokens(root_path)
        print(json.dumps(tokens, indent=2))

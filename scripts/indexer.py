from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import sys
from pathlib import Path

# Ensure local imports work when imported from tests/
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from audit import audit_logger
from project_rules_runtime import ProjectRulesRuntimeError, resolve_confirmed_skill_source
from skill_metadata import extract_summary, parse_frontmatter, resolve_skill_entry


@dataclass
class CatalogEntry:
    id: str
    path: str
    tags: list[str]
    description: str
    mtime: float = 0.0
    source_type: str = "local"   # local | global | remote
    source_name: str = ""        # human-readable source label

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

PREDEFINED_TAGS = (
    "react",
    "nextjs",
    "tailwind",
    "ui",
    "api",
    "database",
    "testing",
    "security",
    "performance",
    "clean-code",
    "audit",
    "planning",
    "memory",
    "mcp",
    "workflow",
    "github",
    "terminal",
)


def build_skill_catalog(project_root: Path, output_path: Path | None = None, incremental: bool = False) -> Path:
    root = Path(project_root).resolve()
    confirmed = resolve_confirmed_skill_source(root)
    catalog_path = output_path or (root / ".agent" / "memory" / "skill_catalog.json")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)

    existing_catalog: list[dict[str, Any]] = []
    if incremental and catalog_path.exists():
        try:
            existing_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse existing catalog JSON at {catalog_path}: {e}")

    entries = _collect_catalog_entries(root, confirmed.resolved_path, existing_catalog)
    catalog_path.write_text(json.dumps([e.to_dict() for e in entries], indent=2), encoding="utf-8")
    return catalog_path


def build_unified_catalog(
    project_root: Path,
    sources: list | None = None,
    output_path: Path | None = None,
    incremental: bool = False,
) -> Path:
    """Build a single unified catalog from multiple skill sources.

    If sources is None, loads all sources from .rulesrc.yaml.
    Each entry is tagged with source_type and source_name.
    """
    root = Path(project_root).resolve()
    catalog_path = output_path or (root / ".agent" / "memory" / "skill_catalog.json")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)

    if sources is None:
        from rules_config import load_all_skill_sources
        config_path = root / ".rulesrc.yaml"
        sources = load_all_skill_sources(config_path)

    existing_catalog: list[dict[str, Any]] = []
    if incremental and catalog_path.exists():
        try:
            existing_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    all_entries: list[CatalogEntry] = []
    for source in sources:
        resolved = _resolve_source_path(root, source)
        if resolved is None or not resolved.exists():
            continue

        entries = _collect_catalog_entries(
            root,
            resolved,
            existing_catalog,
            source_type=source.type,
            source_name=source.source_name or resolved.name,
        )
        all_entries.extend(entries)

    all_entries.sort(key=lambda item: (item.source_type, item.id.lower(), item.path.lower()))
    catalog_path.write_text(
        json.dumps([e.to_dict() for e in all_entries], indent=2),
        encoding="utf-8",
    )
    return catalog_path


def _resolve_source_path(project_root: Path, source: Any) -> Path | None:
    """Resolve a SkillSourceConfig to a local filesystem path."""
    import os

    if source.type == "remote":
        try:
            from remote_source import resolve_remote_source
            cache_dir = project_root / ".agent" / ".cache" / "remote-skills"
            return resolve_remote_source(source.path, cache_dir)
        except RuntimeError:
            return None

    candidate = Path(os.path.expanduser(source.path))
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()




def generate_skill_map_md(
    catalog_path: Path,
    output_path: Path | None = None,
) -> Path:
    """Generate a human+AI-readable Markdown skill map from the catalog.

    Groups skills by source_type (local → global → remote) and writes
    a Markdown table to output_path (defaults to catalog_path/../skill_map.md).
    """
    catalog_path = Path(catalog_path)
    md_path = output_path or catalog_path.with_name("skill_map.md")

    try:
        entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        entries = []

    # Group by source_type
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        source_type = entry.get("source_type", "local")
        groups.setdefault(source_type, []).append(entry)

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = len(entries)
    source_count = len(groups)

    lines = [
        "# 🗺️ Skill Map (Auto-Generated)",
        f"> Generated: {now} | Total: {total} skills | Sources: {source_count}",
        "",
    ]

    type_labels = {
        "local": "Local Skills",
        "global": "Global Skills",
        "remote": "Remote Skills",
    }

    for source_type in ("local", "global", "remote"):
        group = groups.pop(source_type, [])
        label = type_labels[source_type]
        source_names = sorted({e.get("source_name", "") for e in group} - {""})
        source_suffix = f" — `{'`, `'.join(source_names)}`" if source_names else ""

        lines.append(f"## {label} ({len(group)}){source_suffix}")
        lines.append("")

        if not group:
            lines.append(f"_No {source_type} skill sources configured._")
            lines.append("")
            continue

        lines.append("| ID | Description | Tags |")
        lines.append("|----|-------------|------|")
        for entry in sorted(group, key=lambda e: e.get("id", "").lower()):
            skill_id = entry.get("id", "")
            description = entry.get("description", "").replace("|", "\\|")
            tags = ", ".join(entry.get("tags", []))
            lines.append(f"| {skill_id} | {description} | {tags} |")
        lines.append("")

    # Handle any unexpected source_types not in the predefined order
    for source_type, group in sorted(groups.items()):
        lines.append(f"## {source_type.title()} Skills ({len(group)})")
        lines.append("")
        lines.append("| ID | Description | Tags |")
        lines.append("|----|-------------|------|")
        for entry in sorted(group, key=lambda e: e.get("id", "").lower()):
            skill_id = entry.get("id", "")
            description = entry.get("description", "").replace("|", "\\|")
            tags = ", ".join(entry.get("tags", []))
            lines.append(f"| {skill_id} | {description} | {tags} |")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def validate_catalog(project_root: Path, output_path: Path | None = None) -> tuple[bool, list[str], list[str]]:

    root = Path(project_root).resolve()
    confirmed = resolve_confirmed_skill_source(root)
    catalog_path = output_path or (root / ".agent" / "memory" / "skill_catalog.json")
    
    if not catalog_path.exists():
        return False, [], []
        
    try:
        existing_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception:
        return False, [], []

    existing_map = {entry["path"]: entry for entry in existing_catalog}
    stale_entries = []
    current_paths = []
    
    for entrypoint in _iter_entrypoints(confirmed.resolved_path):
        resolved = resolve_skill_entry(entrypoint.parent if entrypoint.is_file() else entrypoint)
        if resolved is None:
            continue
        rel_path = _serialize_catalog_path(root, resolved.primary_path)
        current_paths.append(rel_path)
        
        if rel_path not in existing_map:
            continue
            
        mtime = resolved.primary_path.stat().st_mtime
        if mtime > existing_map[rel_path].get("mtime", 0.0):
            stale_entries.append(rel_path)
            
    missing_entries = [p for p in current_paths if p not in existing_map]
    is_valid = len(stale_entries) == 0 and len(missing_entries) == 0 and len(existing_map) == len(current_paths)
    return is_valid, stale_entries, missing_entries


def _process_single_entrypoint(args):
    entrypoint, project_root, existing_map, source_type, source_name = args
    from skill_metadata import resolve_skill_entry, parse_frontmatter, extract_summary
    from indexer import CatalogEntry, _serialize_catalog_path, _one_sentence, _extract_tags, PREDEFINED_TAGS
    resolved = resolve_skill_entry(entrypoint.parent if entrypoint.is_file() else entrypoint)
    if resolved is None:
        return None

    relative_path = _serialize_catalog_path(project_root, resolved.primary_path)
    mtime = resolved.primary_path.stat().st_mtime

    if existing_map is not None and relative_path in existing_map:
        existing = existing_map[relative_path]
        if existing.get("mtime", 0.0) >= mtime:
            return CatalogEntry(
                id=existing.get("id", ""),
                path=existing.get("path", ""),
                tags=existing.get("tags", []),
                description=existing.get("description", ""),
                mtime=existing.get("mtime", 0.0),
                source_type=existing.get("source_type", source_type),
                source_name=existing.get("source_name", source_name),
            )

    content = resolved.primary_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(content)
    description = (
        str(frontmatter.get("description") or "").strip()
        or extract_summary(content)
        or "No description available."
    )
    description = _one_sentence(description)
    tags = _extract_tags(description, content, resolved.primary_path)
    skill_id = str(frontmatter.get("name") or resolved.directory.name).strip() or resolved.primary_path.stem

    return CatalogEntry(
        id=skill_id,
        path=relative_path,
        tags=tags,
        description=description,
        mtime=mtime,
        source_type=source_type,
        source_name=source_name,
    )


def _collect_catalog_entries(
    project_root: Path,
    confirmed_root: Path,
    existing_catalog: list[dict[str, Any]] | None = None,
    source_type: str = "local",
    source_name: str = "",
) -> list[CatalogEntry]:
    import concurrent.futures
    entries: list[CatalogEntry] = []
    existing_map = {e["path"]: e for e in (existing_catalog or [])}

    entrypoints = list(_iter_entrypoints(confirmed_root))

    # Prepare arguments for multiprocessing/threading
    args_list = [(ep, project_root, existing_map, source_type, source_name) for ep in entrypoints]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(_process_single_entrypoint, args_list)
        for res in results:
            if res is not None:
                entries.append(res)

    return sorted(entries, key=lambda item: (item.id.lower(), item.path.lower()))


def _iter_entrypoints(confirmed_root: Path):
    for file_name in ("SKILL.md", "AGENTS.md", "CLAUDE.md"):
        for path in confirmed_root.rglob(file_name):
            try:
                rel_parts = path.relative_to(confirmed_root).parts
            except ValueError:
                rel_parts = path.parts
            if any(part.startswith(".") and part != ".agent" for part in rel_parts):
                continue
            yield path


def _extract_tags(description: str, content: str, primary_path: Path) -> list[str]:
    import re
    haystack = " ".join(
        [
            description.lower(),
            content.lower(),
            primary_path.as_posix().lower().replace("-", " "),
        ]
    )
    # Use word boundaries to prevent false positives (e.g., 'c"api"tal' matching 'api')
    haystack_words = set(re.findall(r'\b[\w-]+\b', haystack))
    tags = [tag for tag in PREDEFINED_TAGS if tag in haystack_words]
    return tags[:17]


def _one_sentence(text: str) -> str:
    compact = " ".join(text.split())
    if not compact:
        return "No description available."

    match = re.match(r"(.+?[.!?])(?:\s|$)", compact)
    if match:
        return match.group(1).strip()
    return compact


def _serialize_catalog_path(project_root: Path, primary_path: Path) -> str:
    try:
        return primary_path.relative_to(project_root).as_posix()
    except ValueError:
        return primary_path.resolve().as_posix()


@audit_logger(action="generate-index", platform="cli")
def _run_indexer(project_root: Path, output_path: Path | None, validate: bool, incremental: bool) -> dict[str, Any]:
    root = Path(project_root).resolve()
    confirmed = resolve_confirmed_skill_source(root)
    
    if validate:
        is_valid, stale, missing = validate_catalog(project_root, output_path)
        print(json.dumps({"valid": is_valid, "stale": stale, "missing": missing}))
        if not is_valid:
            raise SystemExit(1)
        return {
            "verification_status": "success",
            "confirmed_skill_source_path": str(confirmed.resolved_path)
        }

    final_path = build_skill_catalog(
        project_root,
        output_path=output_path,
        incremental=incremental
    )
    print(final_path)
    return {
        "output_files": [str(final_path)], 
        "verification_status": "success",
        "confirmed_skill_source_path": str(confirmed.resolved_path)
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a lightweight JSON skill catalog for the confirmed skill root.")
    parser.add_argument("--project-root", default=".", help="Project root containing .rulesrc.yaml")
    parser.add_argument("--output", help="Optional output path override for skill_catalog.json")
    parser.add_argument("--validate", action="store_true", help="Validate existing catalog against filesystem")
    parser.add_argument("--incremental", action="store_true", help="Only index changed files based on mtime")
    parser.add_argument("--skill-map", action="store_true", help="Also generate skill_map.md human+AI readable summary")
    parser.add_argument("--unified", action="store_true", help="Scan all skill_sources from .rulesrc.yaml (not just confirmed)")
    args = parser.parse_args()

    try:
        project_root = Path(args.project_root)
        output_path = Path(args.output).resolve() if args.output else None

        if args.unified:
            root = project_root.resolve()
            catalog_path = build_unified_catalog(
                project_root=root,
                output_path=output_path,
                incremental=args.incremental,
            )
            print(catalog_path)
        else:
            _run_indexer(project_root, output_path, args.validate, args.incremental)
            catalog_path = output_path or (project_root.resolve() / ".agent" / "memory" / "skill_catalog.json")

        if args.skill_map:
            md_path = generate_skill_map_md(catalog_path)
            print(f"Skill map: {md_path}")

    except ProjectRulesRuntimeError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()

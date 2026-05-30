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
            if any(part.startswith(".") and part != ".agent" for part in path.parts):
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
    args = parser.parse_args()

    try:
        project_root = Path(args.project_root)
        output_path = Path(args.output).resolve() if args.output else None

        _run_indexer(project_root, output_path, args.validate, args.incremental)
    except ProjectRulesRuntimeError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()

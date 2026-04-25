from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from project_rules_runtime import ProjectRulesRuntimeError, resolve_confirmed_skill_source
from skill_metadata import extract_summary, parse_frontmatter, resolve_skill_entry

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


def build_skill_catalog(project_root: Path, output_path: Path | None = None) -> Path:
    root = Path(project_root).resolve()
    confirmed = resolve_confirmed_skill_source(root)
    catalog_path = output_path or (root / ".agent" / "memory" / "skill_catalog.json")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)

    entries = _collect_catalog_entries(root, confirmed.resolved_path)
    catalog_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    return catalog_path


def _collect_catalog_entries(project_root: Path, confirmed_root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for entrypoint in _iter_entrypoints(confirmed_root):
        resolved = resolve_skill_entry(entrypoint.parent if entrypoint.is_file() else entrypoint)
        if resolved is None:
            continue

        content = resolved.primary_path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(content)
        description = (
            str(frontmatter.get("description") or "").strip()
            or extract_summary(content)
            or "No description available."
        )
        description = _one_sentence(description)
        relative_path = _serialize_catalog_path(project_root, resolved.primary_path)
        tags = _extract_tags(description, content, resolved.primary_path)
        skill_id = str(frontmatter.get("name") or resolved.directory.name).strip() or resolved.primary_path.stem

        entries.append(
            {
                "id": skill_id,
                "path": relative_path,
                "tags": tags,
                "description": description,
            }
        )

    return sorted(entries, key=lambda item: (item["id"].lower(), item["path"].lower()))


def _iter_entrypoints(confirmed_root: Path):
    for file_name in ("SKILL.md", "AGENTS.md", "CLAUDE.md"):
        for path in confirmed_root.rglob(file_name):
            if any(part.startswith(".") and part != ".agent" for part in path.parts):
                continue
            yield path


def _extract_tags(description: str, content: str, primary_path: Path) -> list[str]:
    haystack = " ".join(
        [
            description.lower(),
            content.lower(),
            primary_path.as_posix().lower().replace("-", " "),
        ]
    )
    tags = [tag for tag in PREDEFINED_TAGS if tag in haystack]
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a lightweight JSON skill catalog for the confirmed skill root.")
    parser.add_argument("--project-root", default=".", help="Project root containing .rulesrc.yaml")
    parser.add_argument("--output", help="Optional output path override for skill_catalog.json")
    args = parser.parse_args()

    try:
        output_path = build_skill_catalog(
            Path(args.project_root),
            output_path=Path(args.output).resolve() if args.output else None,
        )
    except ProjectRulesRuntimeError as exc:
        raise SystemExit(str(exc))

    print(output_path)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_metadata import (
    PRIMARY_ENTRY_SET,
    REFERENCE_DIR_NAMES,
    extract_heading,
    extract_summary,
    first_matching_line,
    normalize_text,
    parse_frontmatter,
    resolve_skill_entry,
)

IGNORED_DIR_NAMES = {
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".git",
}
SEARCH_TOOL_CANDIDATES = (
    Path("search.py"),
    Path("scripts") / "search.py",
)
ROOT_WORKFLOW_DOCS = ("CLAUDE.md", "AGENTS.md")
WORKFLOW_HIDDEN_DIR_MARKERS = {
    ".adal",
    ".agent",
    ".claude",
    ".codebuddy",
    ".codex",
    ".continue",
    ".cursor",
    ".factory",
    ".gemini",
    ".kiro",
    ".kilocode",
    ".mastracode",
    ".opencode",
    ".openclaw",
    ".pi",
}


@dataclass(frozen=True)
class SkillEntity:
    directory: Path
    relative_dir: str
    primary_path: Path
    instruction_type: str
    companion_docs: tuple[Path, ...]


class SkillDiscovery:
    """Discover and search agent skills using format-aware rules."""

    def __init__(self, agent_dirs: list[str] | str | None = None):
        if agent_dirs is None:
            requested_roots = [".agent"]
        elif isinstance(agent_dirs, str):
            requested_roots = [agent_dirs]
        else:
            requested_roots = agent_dirs or [".agent"]

        self.agent_dirs = [Path(path) for path in requested_roots]
        self._entity_cache: dict[str, list[SkillEntity]] = {}
        self._entry_metadata_cache: dict[str, dict[str, str]] = {}
        self._visible_entity_cache: dict[str, tuple[bool, bool]] = {}
        self.sources = self._discover_sources()

    def _discover_sources(self) -> list[dict[str, str]]:
        """Scan each configured root and classify the first instance of each source."""
        sources: list[dict[str, str]] = []
        seen_source_names: set[str] = set()

        for agent_dir in self.agent_dirs:
            if not agent_dir.exists():
                continue

            for item in sorted(agent_dir.iterdir(), key=lambda path: path.name.lower()):
                if not item.is_dir():
                    continue
                if self._is_reserved_output_dir(item):
                    continue

                source_key = item.name.lower()
                if source_key in seen_source_names:
                    continue

                sources.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "format": self._detect_format(item),
                        "source_root": str(agent_dir),
                    }
                )
                seen_source_names.add(source_key)

        return sources

    def _detect_format(self, source_path: Path) -> str:
        """Detect the skill source format using explicit filesystem markers."""
        if self._has_catalog(source_path):
            return "CATALOG"

        if self._find_search_tool(source_path) is not None:
            return "SEARCH_ENGINE"

        if self._has_visible_skill_entities(source_path):
            return "FOLDER"

        if self._is_workflow_root(source_path):
            return "WORKFLOW"

        if (source_path / "README.md").exists():
            return "README"

        return "UNKNOWN"

    def search(self, keywords: list[str], limit: int | None = None) -> list[dict[str, Any]]:
        """Search all discovered sources for keyword matches."""
        normalized_keywords = [normalize_text(keyword) for keyword in keywords if keyword.strip()]
        matches: list[dict[str, Any]] = []

        for source in self.sources:
            if source["format"] == "CATALOG":
                matches.extend(self._search_catalog(source, normalized_keywords))
            elif source["format"] in {"FOLDER", "WORKFLOW"}:
                matches.extend(self._search_instruction_tree(source, normalized_keywords))
            elif source["format"] == "README":
                matches.extend(self._search_readme(source, normalized_keywords))
            elif source["format"] == "SEARCH_ENGINE":
                matches.extend(self._search_engine(source, normalized_keywords))

        deduplicated = self._deduplicate(matches)
        if limit is not None and limit >= 0:
            return deduplicated[:limit]
        return deduplicated

    def _search_catalog(self, source: dict[str, str], keywords: list[str]) -> list[dict[str, Any]]:
        """Search a catalog source using `skills_index.json` data."""
        source_path = Path(source["path"])
        index_path = self._find_catalog_index(source_path)
        if index_path is None:
            return []

        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

        if isinstance(data, list):
            skill_list = data
        elif isinstance(data, dict):
            skill_list = data.get("skills", [])
        else:
            skill_list = []

        matches: list[dict[str, Any]] = []
        for skill in skill_list:
            if not isinstance(skill, dict):
                continue

            score, matched_keywords = self._score_texts(
                keywords,
                skill.get("id", ""),
                skill.get("name", ""),
                skill.get("category", ""),
                skill.get("description", ""),
                skill.get("path", ""),
                skill.get("tags", ""),
            )
            if score <= 0:
                continue

            skill_path = self._resolve_catalog_skill_path(source_path, skill)
            metadata = self._extract_entry_metadata(
                skill_path.parent if skill_path.suffix else skill_path,
                source,
                preferred_name=str(skill.get("name") or "").strip(),
                preferred_description=str(skill.get("description") or "").strip(),
            )
            metadata["matched_keywords"] = matched_keywords
            metadata["score"] = score
            matches.append(metadata)

        return matches

    def _search_instruction_tree(
        self, source: dict[str, str], keywords: list[str]
    ) -> list[dict[str, Any]]:
        """Search visible skill entities by metadata."""
        matches: list[dict[str, Any]] = []
        entities = self._collect_skill_entities(source)
        read_all_entities = len(entities) <= 50

        for entity in entities:
            quick_score, _ = self._score_texts(
                keywords,
                entity.directory.name,
                entity.relative_dir,
            )
            if quick_score <= 0 and not read_all_entities:
                continue

            metadata = self._extract_entry_metadata(entity.directory, source)
            score, matched_keywords = self._score_texts(
                keywords,
                entity.directory.name,
                entity.relative_dir,
                metadata["name"],
                metadata.get("description", ""),
                metadata.get("title", ""),
            )
            if score <= 0:
                continue

            metadata["matched_keywords"] = matched_keywords
            metadata["score"] = score
            matches.append(metadata)

        if source["format"] == "WORKFLOW":
            readme_path = Path(source["path"]) / "README.md"
            if readme_path.exists():
                matches.extend(self._search_readme(source, keywords))

        return matches

    def _search_readme(self, source: dict[str, str], keywords: list[str]) -> list[dict[str, Any]]:
        """Search a README-only source for keyword matches."""
        readme_path = Path(source["path"]) / "README.md"
        if not readme_path.exists():
            return []

        try:
            content = readme_path.read_text(encoding="utf-8")
        except OSError:
            return []

        score, matched_keywords = self._score_texts(keywords, source["name"], content)
        if score <= 0:
            return []

        return [
            {
                "name": source["name"],
                "path": str(readme_path),
                "source": source["name"],
                "source_root": source["source_root"],
                "description": first_matching_line(content, keywords),
                "matched_keywords": matched_keywords,
                "score": score,
                "instruction_type": "README.md",
                "companion_docs": [],
                "_entity_key": f'{source["name"].lower()}::README',
            }
        ]

    def _search_engine(self, source: dict[str, str], keywords: list[str]) -> list[dict[str, Any]]:
        """Run a top-level search tool when the source exposes one."""
        source_path = Path(source["path"])
        search_tool = self._find_search_tool(source_path)
        if search_tool is None or not keywords:
            return []

        tool_argument = str(search_tool.relative_to(source_path))
        command = [sys.executable, tool_argument, "--keywords", *keywords]
        try:
            completed = subprocess.run(
                command,
                cwd=source_path,
                capture_output=True,
                check=False,
                text=True,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            return []

        if completed.returncode != 0 or not completed.stdout.strip():
            return []

        return self._parse_search_output(source, source_path, completed.stdout, keywords)

    def _parse_search_output(
        self,
        source: dict[str, str],
        source_path: Path,
        stdout: str,
        keywords: list[str],
    ) -> list[dict[str, Any]]:
        """Normalize JSON or line-based search output into a shared result shape."""
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = [line.strip() for line in stdout.splitlines() if line.strip()]

        if isinstance(payload, dict):
            payload = payload.get("results", [])
        if not isinstance(payload, list):
            return []

        matches: list[dict[str, Any]] = []
        for item in payload:
            explicit_score: int | None = None
            if isinstance(item, str):
                raw_path = item
                description = ""
                name = Path(raw_path).stem
            elif isinstance(item, dict):
                raw_path = item.get("path") or item.get("file") or ""
                description = str(item.get("description") or "")
                name = str(item.get("name") or Path(raw_path).stem)
                if isinstance(item.get("score"), (int, float)):
                    explicit_score = int(item["score"])
            else:
                continue

            if not raw_path:
                continue

            resolved_path = Path(raw_path)
            if not resolved_path.is_absolute():
                resolved_path = source_path / resolved_path

            resolved_entry = self._resolve_search_entry(resolved_path)
            if resolved_entry is not None:
                metadata = self._extract_entry_metadata(
                    resolved_entry.directory,
                    source,
                    preferred_name=name,
                    preferred_description=description,
                )
                score, matched_keywords = self._score_texts(
                    keywords,
                    metadata["name"],
                    metadata.get("description", ""),
                    metadata.get("title", ""),
                    raw_path,
                )
            else:
                score, matched_keywords = self._score_texts(keywords, name, description, raw_path)
                metadata = {
                    "name": name,
                    "path": str(resolved_path),
                    "source": source["name"],
                    "source_root": source["source_root"],
                    "description": description,
                    "instruction_type": resolved_path.name if resolved_path.is_file() else "",
                    "companion_docs": [],
                    "_entity_key": f'{source["name"].lower()}::{str(resolved_path).lower()}',
                }

            if explicit_score is not None:
                score = explicit_score
            if keywords and score <= 0:
                score = 1

            metadata["matched_keywords"] = matched_keywords
            metadata["score"] = score
            matches.append(metadata)

        return matches

    def _resolve_catalog_skill_path(self, source_path: Path, skill: dict[str, Any]) -> Path:
        """Resolve the on-disk primary path for a catalog entry."""
        relative_path = Path(str(skill.get("path") or ""))
        if relative_path.parts:
            candidate = source_path / relative_path
            if candidate.exists():
                if candidate.is_dir():
                    entry = resolve_skill_entry(candidate)
                    if entry is not None:
                        return entry.primary_path
                return candidate

            candidate_dir = source_path / relative_path
            entry = resolve_skill_entry(candidate_dir)
            if entry is not None:
                return entry.primary_path

            candidate_skill = candidate_dir / "SKILL.md"
            if candidate_skill.exists():
                return candidate_skill

        fallback_name = str(skill.get("name") or "").strip()
        fallback_dir = source_path / "skills" / fallback_name
        entry = resolve_skill_entry(fallback_dir)
        if entry is not None:
            return entry.primary_path
        return fallback_dir / "SKILL.md"

    def _extract_entry_metadata(
        self,
        target: Path,
        source: dict[str, str],
        preferred_name: str = "",
        preferred_description: str = "",
    ) -> dict[str, Any]:
        """Resolve a skill entity and extract lightweight metadata for matching."""
        entry = resolve_skill_entry(target)
        if entry is None:
            return {
                "name": preferred_name or target.name,
                "path": str(target),
                "source": source["name"],
                "source_root": source["source_root"],
                "description": preferred_description,
                "instruction_type": target.name if target.is_file() else "",
                "companion_docs": [],
                "_entity_key": f'{source["name"].lower()}::{str(target).lower()}',
            }

        try:
            base_metadata = self._load_entry_metadata(entry.primary_path, entry.directory)
        except OSError:
            base_metadata = {
                "name": entry.directory.name or entry.primary_path.stem,
                "description": "",
                "title": "",
            }

        description = preferred_description or base_metadata["description"]
        title = base_metadata["title"]
        name = preferred_name or base_metadata["name"]
        relative_dir = self._relative_directory(Path(source["path"]), entry.directory)

        return {
            "name": name,
            "path": str(entry.primary_path),
            "source": source["name"],
            "source_root": source["source_root"],
            "description": description,
            "title": title,
            "instruction_type": entry.instruction_type,
            "companion_docs": [str(path) for path in entry.companion_docs],
            "_entity_key": f'{source["name"].lower()}::{relative_dir.lower()}',
        }

    def _collect_skill_entities(self, source: dict[str, str]) -> list[SkillEntity]:
        cache_key = str(source["path"])
        cached = self._entity_cache.get(cache_key)
        if cached is not None:
            return cached

        source_path = Path(source["path"])
        candidate_dirs = list(self._iter_visible_instruction_dirs(source_path))
        entities: list[SkillEntity] = []

        for directory in candidate_dirs:
            entry = resolve_skill_entry(directory)
            if entry is None:
                continue

            entities.append(
                SkillEntity(
                    directory=entry.directory,
                    relative_dir=self._relative_directory(source_path, entry.directory),
                    primary_path=entry.primary_path,
                    instruction_type=entry.instruction_type,
                    companion_docs=entry.companion_docs,
                )
            )

        if source["format"] != "WORKFLOW":
            has_nested_entities = any(entity.directory != source_path for entity in entities)
            if has_nested_entities:
                entities = [entity for entity in entities if entity.directory != source_path]
        elif not entities:
            entry = resolve_skill_entry(source_path)
            if entry is not None:
                entities.append(
                    SkillEntity(
                        directory=entry.directory,
                        relative_dir=".",
                        primary_path=entry.primary_path,
                        instruction_type=entry.instruction_type,
                        companion_docs=entry.companion_docs,
                    )
                )

        entities = sorted(entities, key=lambda entity: (entity.relative_dir.lower(), entity.primary_path.name))
        self._entity_cache[cache_key] = entities
        return entities

    def _iter_visible_instruction_dirs(self, source_path: Path):
        for root, dirnames, filenames in os.walk(source_path):
            dirnames[:] = [name for name in dirnames if not self._is_ignored_dir(name)]
            directory = Path(root)
            visible_files = set(filenames)
            if PRIMARY_ENTRY_SET & visible_files:
                yield directory
                dirnames[:] = [name for name in dirnames if name not in REFERENCE_DIR_NAMES]

    def _has_catalog(self, source_path: Path) -> bool:
        return self._find_catalog_index(source_path) is not None or (source_path / "CATALOG.md").exists()

    def _find_catalog_index(self, source_path: Path) -> Path | None:
        candidates = (
            source_path / "skills_index.json",
            source_path / "data" / "skills_index.json",
            source_path / "catalog.json",
        )
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def _find_search_tool(self, source_path: Path) -> Path | None:
        for candidate in SEARCH_TOOL_CANDIDATES:
            tool_path = source_path / candidate
            if tool_path.exists():
                return tool_path
        return None

    def _has_visible_skill_entities(self, source_path: Path) -> bool:
        has_root_entity, has_nested_entities = self._get_visible_entity_stats(source_path)
        if has_nested_entities:
            return True
        return has_root_entity and not self._has_root_workflow_doc(source_path)

    def _is_reserved_output_dir(self, source_path: Path) -> bool:
        """Skip project output folders that are not external skill sources."""
        if source_path.name != "workflows":
            return False

        if self._has_catalog(source_path):
            return False
        if self._find_search_tool(source_path) is not None:
            return False
        if (source_path / "README.md").exists():
            return False
        if self._is_workflow_root(source_path):
            return False
        if self._has_visible_skill_entities(source_path):
            return False

        try:
            return any(child.is_file() and child.suffix.lower() == ".md" for child in source_path.iterdir())
        except OSError:
            return False

    def _is_workflow_root(self, source_path: Path) -> bool:
        if (source_path / ".shared").exists():
            return True

        if self._has_visible_nested_entities(source_path):
            return False

        return self._has_root_workflow_doc(source_path) and self._has_workflow_integration_dir(source_path)

    def _has_visible_nested_entities(self, source_path: Path) -> bool:
        _, has_nested_entities = self._get_visible_entity_stats(source_path)
        return has_nested_entities

    def _has_root_workflow_doc(self, source_path: Path) -> bool:
        return any((source_path / doc_name).exists() for doc_name in ROOT_WORKFLOW_DOCS)

    def _has_workflow_integration_dir(self, source_path: Path) -> bool:
        try:
            for child in source_path.iterdir():
                if not child.is_dir() or not child.name.startswith("."):
                    continue
                if child.name in WORKFLOW_HIDDEN_DIR_MARKERS or child.name.endswith("-plugin"):
                    return True
        except OSError:
            return False
        return False

    def _resolve_search_entry(self, path: Path):
        if path.is_dir():
            return resolve_skill_entry(path)

        if path.name in PRIMARY_ENTRY_SET:
            return resolve_skill_entry(path)

        if path.name == "README.md":
            return resolve_skill_entry(path.parent)

        return None

    def _relative_directory(self, source_path: Path, directory: Path) -> str:
        if directory == source_path:
            return "."
        try:
            return str(directory.relative_to(source_path)).replace("\\", "/")
        except ValueError:
            return str(directory).replace("\\", "/")

    def _is_ignored_dir(self, directory_name: str) -> bool:
        return directory_name.startswith(".") or directory_name in IGNORED_DIR_NAMES

    def _get_visible_entity_stats(self, source_path: Path) -> tuple[bool, bool]:
        cache_key = str(source_path)
        cached = self._visible_entity_cache.get(cache_key)
        if cached is not None:
            return cached

        has_root_entity = False
        has_nested_entities = False

        for root, dirnames, filenames in os.walk(source_path):
            dirnames[:] = [name for name in dirnames if not self._is_ignored_dir(name)]
            directory = Path(root)
            visible_files = set(filenames)
            if PRIMARY_ENTRY_SET & visible_files:
                if directory == source_path:
                    has_root_entity = True
                else:
                    has_nested_entities = True
                    break
                dirnames[:] = [name for name in dirnames if name not in REFERENCE_DIR_NAMES]

        result = (has_root_entity, has_nested_entities)
        self._visible_entity_cache[cache_key] = result
        return result

    def _load_entry_metadata(self, entry_path: Path, directory: Path) -> dict[str, str]:
        cache_key = str(entry_path)
        cached = self._entry_metadata_cache.get(cache_key)
        if cached is not None:
            return cached

        content = self._read_preview_text(entry_path)
        frontmatter = parse_frontmatter(content)
        description = str(frontmatter.get("description") or "").strip()
        if not description:
            description = extract_summary(content)

        metadata = {
            "name": str(frontmatter.get("name") or directory.name or entry_path.stem),
            "description": description,
            "title": extract_heading(content),
        }
        self._entry_metadata_cache[cache_key] = metadata
        return metadata

    def _read_preview_text(self, file_path: Path, max_chars: int = 12000) -> str:
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                return handle.read(max_chars)
        except OSError:
            return ""

    def _score_texts(self, keywords: list[str], *texts: Any) -> tuple[int, list[str]]:
        hit_counts: dict[str, int] = {}
        total_score = 0

        for text in texts:
            normalized_text = normalize_text(text)
            if not normalized_text:
                continue

            for keyword in keywords:
                if keyword and keyword in normalized_text:
                    hit_counts[keyword] = hit_counts.get(keyword, 0) + 1

        for count in hit_counts.values():
            total_score += count

        matched_keywords = sorted(hit_counts.keys())
        return total_score, matched_keywords

    def _deduplicate(self, matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove duplicate results while keeping the most informative entry."""
        unique: dict[str, dict[str, Any]] = {}
        for match in matches:
            entity_key = str(match.get("_entity_key") or match["path"])
            current = unique.get(entity_key)
            if current is None:
                unique[entity_key] = match
                continue

            current_score = int(current.get("score", 0))
            new_score = int(match.get("score", 0))
            if new_score > current_score:
                unique[entity_key] = match
                continue

            if new_score == current_score and len(match.get("description", "")) > len(
                current.get("description", "")
            ):
                unique[entity_key] = match

        cleaned_results = []
        for match in unique.values():
            cleaned = dict(match)
            cleaned.pop("_entity_key", None)
            cleaned_results.append(cleaned)

        return sorted(
            cleaned_results,
            key=lambda item: (
                -int(item.get("score", 0)),
                str(item.get("source", "")).lower(),
                str(item.get("name", "")).lower(),
                str(item.get("path", "")).lower(),
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Format-aware agent skill discovery")
    parser.add_argument("--keywords", nargs="+", help="Keywords to search for")
    parser.add_argument(
        "--agent-dir",
        action="append",
        dest="agent_dirs",
        help="Directory that contains skill sources. Can be provided multiple times.",
    )
    parser.add_argument("--limit", type=int, help="Maximum number of results to return")
    parser.add_argument(
        "--format",
        action="store_true",
        help="List discovered sources and their detected formats",
    )
    args = parser.parse_args()

    discovery = SkillDiscovery(args.agent_dirs)

    if args.format:
        print(json.dumps(discovery.sources, indent=2))
        return

    if args.keywords:
        print(json.dumps(discovery.search(args.keywords, limit=args.limit), indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()

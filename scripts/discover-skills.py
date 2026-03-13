from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


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
WORKFLOW_HIDDEN_DIRS = (
    ".claude",
    ".cursor",
    ".agent",
    ".codex",
    ".continue",
    ".gemini",
    ".kiro",
    ".opencode",
)
ROOT_WORKFLOW_DOCS = ("CLAUDE.md", "AGENTS.md")
INSTRUCTION_FILE_NAMES = {"SKILL.md", "CLAUDE.md"}


class SkillDiscovery:
    """Discover and search agent skills using format-aware rules."""

    def __init__(self, agent_dir: str = ".agent"):
        self.agent_dir = Path(agent_dir)
        self.sources = self._discover_sources()

    def _discover_sources(self) -> list[dict[str, str]]:
        """Scan the root directory and classify each visible child source."""
        if not self.agent_dir.exists():
            return []

        sources: list[dict[str, str]] = []
        for item in sorted(self.agent_dir.iterdir(), key=lambda path: path.name.lower()):
            if not item.is_dir():
                continue
            if self._is_reserved_output_dir(item):
                continue

            sources.append(
                {
                    "name": item.name,
                    "path": str(item),
                    "format": self._detect_format(item),
                }
            )

        return sources

    def _detect_format(self, source_path: Path) -> str:
        """Detect the skill source format using explicit filesystem markers."""
        if self._has_catalog(source_path):
            return "CATALOG"

        if self._is_workflow_root(source_path):
            return "WORKFLOW"

        if self._find_search_tool(source_path) is not None:
            return "SEARCH_ENGINE"

        if self._has_instruction_tree(source_path):
            return "FOLDER"

        if (source_path / "README.md").exists():
            return "README"

        return "UNKNOWN"

    def search(self, keywords: list[str], limit: int | None = None) -> list[dict[str, Any]]:
        """Search all discovered sources for keyword matches."""
        normalized_keywords = [self._normalize_text(keyword) for keyword in keywords if keyword.strip()]
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

    def _search_catalog(
        self, source: dict[str, str], keywords: list[str]
    ) -> list[dict[str, Any]]:
        """Search a catalog source using `skills_index.json` data."""
        index_path = self._find_catalog_index(Path(source["path"]))
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

            skill_path = self._resolve_catalog_skill_path(Path(source["path"]), skill)
            matches.append(
                {
                    "name": skill.get("name") or Path(skill_path).parent.name,
                    "path": str(skill_path),
                    "source": source["name"],
                    "description": skill.get("description", ""),
                    "matched_keywords": matched_keywords,
                    "score": score,
                }
            )

        return matches

    def _search_instruction_tree(
        self, source: dict[str, str], keywords: list[str]
    ) -> list[dict[str, Any]]:
        """Search visible instruction files by name and extracted metadata."""
        source_path = Path(source["path"])
        matches: list[dict[str, Any]] = []

        for file_path in self._iter_instruction_files(source_path):
            metadata = self._extract_instruction_metadata(file_path, source["name"])
            haystack = " ".join(
                (
                    metadata["name"],
                    metadata.get("description", ""),
                    metadata.get("title", ""),
                )
            )
            score, matched_keywords = self._score_texts(
                keywords,
                metadata["name"],
                metadata.get("description", ""),
                metadata.get("title", ""),
            )
            if score > 0:
                metadata["matched_keywords"] = matched_keywords
                metadata["score"] = score
                matches.append(metadata)

        if source["format"] == "WORKFLOW":
            readme_path = source_path / "README.md"
            if readme_path.exists():
                matches.extend(self._search_readme(source, keywords))

        return matches

    def _search_readme(
        self, source: dict[str, str], keywords: list[str]
    ) -> list[dict[str, Any]]:
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
                "description": self._first_matching_line(content, keywords),
                "matched_keywords": matched_keywords,
                "score": score,
            }
        ]

    def _search_engine(
        self, source: dict[str, str], keywords: list[str]
    ) -> list[dict[str, Any]]:
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
            if isinstance(item, str):
                raw_path = item
                description = ""
                name = Path(raw_path).stem
            elif isinstance(item, dict):
                raw_path = item.get("path") or item.get("file") or ""
                description = item.get("description", "")
                name = item.get("name") or Path(raw_path).stem
            else:
                continue

            if not raw_path:
                continue

            resolved_path = Path(raw_path)
            if not resolved_path.is_absolute():
                resolved_path = source_path / resolved_path

            score, matched_keywords = self._score_texts(
                keywords,
                name,
                description,
                raw_path,
            )
            if isinstance(item, dict):
                explicit_score = item.get("score")
                if isinstance(explicit_score, (int, float)):
                    score = int(explicit_score)
            if keywords and score <= 0:
                score = 1

            matches.append(
                {
                    "name": name,
                    "path": str(resolved_path),
                    "source": source["name"],
                    "description": description,
                    "matched_keywords": matched_keywords,
                    "score": score,
                }
            )

        return matches

    def _resolve_catalog_skill_path(self, source_path: Path, skill: dict[str, Any]) -> Path:
        """Resolve the on-disk SKILL.md path for a catalog entry."""
        relative_path = Path(str(skill.get("path") or ""))
        if relative_path.parts:
            candidate = source_path / relative_path
            if candidate.name != "SKILL.md":
                candidate = candidate / "SKILL.md"
            return candidate

        fallback_name = str(skill.get("name") or "").strip()
        return source_path / "skills" / fallback_name / "SKILL.md"

    def _extract_instruction_metadata(
        self, file_path: Path, source_name: str
    ) -> dict[str, Any]:
        """Read a skill file and extract lightweight metadata for matching."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError:
            content = ""

        frontmatter = self._parse_frontmatter(content)
        description = str(frontmatter.get("description", "")).strip()
        title = self._extract_heading(content)
        name = str(frontmatter.get("name") or file_path.parent.name or file_path.stem)

        return {
            "name": name,
            "path": str(file_path),
            "source": source_name,
            "description": description,
            "title": title,
        }

    def _first_matching_line(self, content: str, keywords: list[str]) -> str:
        """Return the first README line that matches any keyword."""
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if line and self._matches_keywords(line, keywords):
                return line
        return ""

    def _deduplicate(self, matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove duplicate results while keeping the most informative entry."""
        unique: dict[str, dict[str, Any]] = {}
        for match in matches:
            path_key = str(match["path"])
            current = unique.get(path_key)
            if current is None:
                unique[path_key] = match
                continue

            current_score = int(current.get("score", 0))
            new_score = int(match.get("score", 0))
            if new_score > current_score:
                unique[path_key] = match
                continue

            if new_score == current_score and len(match.get("description", "")) > len(
                current.get("description", "")
            ):
                unique[path_key] = match

        return sorted(
            unique.values(),
            key=lambda item: (
                -int(item.get("score", 0)),
                str(item.get("source", "")).lower(),
                str(item.get("name", "")).lower(),
                str(item.get("path", "")).lower(),
            ),
        )

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
        if self._has_instruction_tree(source_path):
            return False

        try:
            return any(child.is_file() and child.suffix.lower() == ".md" for child in source_path.iterdir())
        except OSError:
            return False

    def _is_workflow_root(self, source_path: Path) -> bool:
        if (source_path / ".shared").exists():
            return True

        has_root_doc = any((source_path / doc_name).exists() for doc_name in ROOT_WORKFLOW_DOCS)
        has_hidden_integration = any(
            (source_path / directory_name).exists() for directory_name in WORKFLOW_HIDDEN_DIRS
        )
        name_is_workflowish = source_path.name.endswith(("-skill", "-workflow"))

        return has_root_doc and has_hidden_integration and name_is_workflowish

    def _has_instruction_tree(self, source_path: Path) -> bool:
        return any(True for _ in self._iter_instruction_files(source_path))

    def _iter_instruction_files(self, source_path: Path):
        for root, dirnames, filenames in os.walk(source_path):
            dirnames[:] = [
                directory_name
                for directory_name in dirnames
                if not self._is_ignored_dir(directory_name)
            ]
            visible_files = set(filenames)
            for file_name in sorted(INSTRUCTION_FILE_NAMES & visible_files):
                yield Path(root) / file_name

    def _is_ignored_dir(self, directory_name: str) -> bool:
        return directory_name.startswith(".") or directory_name in IGNORED_DIR_NAMES

    def _matches_keywords(self, text: str, keywords: list[str]) -> bool:
        normalized_text = self._normalize_text(text)
        return any(keyword in normalized_text for keyword in keywords)

    def _score_texts(self, keywords: list[str], *texts: Any) -> tuple[int, list[str]]:
        hit_counts: dict[str, int] = {}
        total_score = 0

        for text in texts:
            normalized_text = self._normalize_text(text)
            if not normalized_text:
                continue

            for keyword in keywords:
                if keyword and keyword in normalized_text:
                    hit_counts[keyword] = hit_counts.get(keyword, 0) + 1

        for count in hit_counts.values():
            total_score += count

        matched_keywords = sorted(hit_counts.keys())
        return total_score, matched_keywords

    def _collect_keyword_hits(self, text: str, keywords: list[str]) -> list[str]:
        if not keywords:
            return []
        normalized_text = self._normalize_text(text)
        return sorted({keyword for keyword in keywords if keyword in normalized_text})

    def _normalize_text(self, value: str) -> str:
        return " ".join(
            str(value).lower().replace("-", " ").replace("_", " ").split()
        )

    def _parse_frontmatter(self, content: str) -> dict[str, Any]:
        lines = content.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}

        frontmatter: dict[str, Any] = {}
        current_key: str | None = None
        current_items: list[str] = []

        for line in lines[1:]:
            stripped = line.strip()
            if stripped == "---":
                break

            if current_key and stripped.startswith("- "):
                current_items.append(self._strip_quotes(stripped[2:].strip()))
                continue

            if current_key:
                frontmatter[current_key] = current_items
                current_key = None
                current_items = []

            if ":" not in line:
                continue

            key, raw_value = line.split(":", 1)
            key = key.strip().lower()
            value = raw_value.strip()

            if not value:
                current_key = key
                continue

            frontmatter[key] = self._parse_frontmatter_value(value)

        if current_key:
            frontmatter[current_key] = current_items

        return frontmatter

    def _parse_frontmatter_value(self, raw_value: str) -> Any:
        value = raw_value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [
                self._strip_quotes(item.strip())
                for item in value[1:-1].split(",")
                if item.strip()
            ]
            return items
        return self._strip_quotes(value)

    def _extract_heading(self, content: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""

    def _strip_quotes(self, value: str) -> str:
        return value.strip().strip('"').strip("'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Format-aware agent skill discovery")
    parser.add_argument("--keywords", nargs="+", help="Keywords to search for")
    parser.add_argument("--agent-dir", default=".agent", help="Directory that contains skill sources")
    parser.add_argument("--limit", type=int, help="Maximum number of results to return")
    parser.add_argument(
        "--format",
        action="store_true",
        help="List discovered sources and their detected formats",
    )
    args = parser.parse_args()

    discovery = SkillDiscovery(args.agent_dir)

    if args.format:
        print(json.dumps(discovery.sources, indent=2))
        return

    if args.keywords:
        print(json.dumps(discovery.search(args.keywords, limit=args.limit), indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()

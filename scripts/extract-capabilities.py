from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class CapabilityExtractor:
    """Extract lightweight capability summaries from skill files."""

    def extract(self, skill_path: str) -> dict[str, Any] | None:
        path = Path(skill_path)
        if not path.exists():
            return None

        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            return {"error": str(exc), "path": str(path)}

        frontmatter = self._parse_frontmatter(content)
        title = self._extract_title(content) or str(frontmatter.get("name") or path.parent.name)
        capability = str(frontmatter.get("description") or "").strip()

        return {
            "title": title,
            "capability": capability,
            "tools": self._extract_tools(frontmatter),
            "path": str(path),
        }

    def _extract_title(self, content: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""

    def _extract_tools(self, frontmatter: dict[str, Any]) -> list[str]:
        collected: list[str] = []
        for key in ("allowed-tools", "tools"):
            value = frontmatter.get(key)
            if isinstance(value, list):
                collected.extend(str(item).strip() for item in value if str(item).strip())
            elif isinstance(value, str):
                collected.extend(
                    part.strip()
                    for part in value.split(",")
                    if part.strip()
                )

        unique: list[str] = []
        for tool in collected:
            if tool not in unique:
                unique.append(tool)
        return unique

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

            frontmatter[key] = self._parse_value(value)

        if current_key:
            frontmatter[current_key] = current_items

        return frontmatter

    def _parse_value(self, raw_value: str) -> Any:
        value = raw_value.strip()
        if value.startswith("[") and value.endswith("]"):
            return [
                self._strip_quotes(item.strip())
                for item in value[1:-1].split(",")
                if item.strip()
            ]
        return self._strip_quotes(value)

    def _strip_quotes(self, value: str) -> str:
        return value.strip().strip('"').strip("'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract capability summaries from SKILL files")
    parser.add_argument("paths", nargs="+", help="Paths to SKILL.md files")
    args = parser.parse_args()

    extractor = CapabilityExtractor()
    results = []
    for path in args.paths:
        capability = extractor.extract(path)
        if capability is not None:
            results.append(capability)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_metadata import extract_heading, extract_summary, extract_tools, parse_frontmatter, resolve_skill_entry


class CapabilityExtractor:
    """Extract lightweight capability summaries from skill entries."""

    def extract(self, skill_path: str) -> dict[str, Any] | None:
        requested_path = Path(skill_path)
        if not requested_path.exists():
            return None

        entry = resolve_skill_entry(requested_path)
        if entry is None:
            return None

        try:
            content = entry.primary_path.read_text(encoding="utf-8")
        except OSError as exc:
            return {"error": str(exc), "path": str(entry.primary_path)}

        frontmatter = parse_frontmatter(content)
        title = extract_heading(content) or str(frontmatter.get("name") or entry.directory.name)
        capability = str(frontmatter.get("description") or "").strip() or extract_summary(content)

        return {
            "title": title,
            "capability": capability,
            "tools": extract_tools(frontmatter),
            "path": str(entry.primary_path),
            "companion_docs": [str(path) for path in entry.companion_docs],
            "reference_dirs": [str(path) for path in entry.reference_dirs],
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract capability summaries from skill directories or instruction files"
    )
    parser.add_argument("paths", nargs="+", help="Paths to skill directories or SKILL/AGENTS/CLAUDE files")
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

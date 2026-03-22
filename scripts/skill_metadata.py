from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

PRIMARY_ENTRY_FILES = ("SKILL.md", "AGENTS.md", "CLAUDE.md")
PRIMARY_ENTRY_SET = set(PRIMARY_ENTRY_FILES)
COMPANION_DOC_FILES = (*PRIMARY_ENTRY_FILES, "README.md")
REFERENCE_DIR_NAMES = ("references", "rules")
SUMMARY_SECTION_NAMES = {"overview", "abstract", "summary"}


@dataclass(frozen=True)
class ResolvedSkillEntry:
    directory: Path
    primary_path: Path
    instruction_type: str
    companion_docs: tuple[Path, ...]
    reference_dirs: tuple[Path, ...]


def resolve_skill_entry(target: Path) -> ResolvedSkillEntry | None:
    candidate = Path(target)
    if not candidate.exists():
        return None

    if candidate.is_file():
        if candidate.name not in PRIMARY_ENTRY_SET:
            return None
        directory = candidate.parent
    else:
        directory = candidate

    primary_path = _find_primary_entry(directory)
    if primary_path is None:
        return None

    companion_docs = tuple(
        path
        for path in (directory / file_name for file_name in COMPANION_DOC_FILES)
        if path.exists() and path != primary_path
    )
    reference_dirs = tuple(
        path for path in (directory / name for name in REFERENCE_DIR_NAMES) if path.is_dir()
    )

    return ResolvedSkillEntry(
        directory=directory,
        primary_path=primary_path,
        instruction_type=primary_path.name,
        companion_docs=companion_docs,
        reference_dirs=reference_dirs,
    )


def parse_frontmatter(content: str) -> dict[str, Any]:
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
            current_items.append(_strip_quotes(stripped[2:].strip()))
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

        frontmatter[key] = _parse_frontmatter_value(value)

    if current_key:
        frontmatter[current_key] = current_items

    return frontmatter


def extract_heading(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_summary(content: str) -> str:
    preferred = _extract_named_section_summary(content, SUMMARY_SECTION_NAMES)
    if preferred:
        return preferred

    paragraphs = list(_iter_text_paragraphs(_strip_frontmatter_block(content)))
    return paragraphs[0] if paragraphs else ""


def extract_tools(frontmatter: dict[str, Any]) -> list[str]:
    collected: list[str] = []
    for key in ("allowed-tools", "tools"):
        value = frontmatter.get(key)
        if isinstance(value, list):
            collected.extend(str(item).strip() for item in value if str(item).strip())
        elif isinstance(value, str):
            collected.extend(part.strip() for part in value.split(",") if part.strip())

    unique: list[str] = []
    for tool in collected:
        if tool not in unique:
            unique.append(tool)
    return unique


def normalize_text(value: Any) -> str:
    return " ".join(str(value).lower().replace("-", " ").replace("_", " ").split())


def first_matching_line(content: str, keywords: list[str]) -> str:
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line and any(keyword in normalize_text(line) for keyword in keywords):
            return line
    return ""


def _find_primary_entry(directory: Path) -> Path | None:
    for file_name in PRIMARY_ENTRY_FILES:
        candidate = directory / file_name
        if candidate.exists():
            return candidate
    return None


def _strip_frontmatter_block(content: str) -> str:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return content

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])
    return content


def _extract_named_section_summary(content: str, section_names: set[str]) -> str:
    body_lines = _strip_frontmatter_block(content).splitlines()

    for index, line in enumerate(body_lines):
        match = re.match(r"^#{1,6}\s+(.*)$", line.strip())
        if not match:
            continue

        heading = match.group(1).strip().lower()
        if heading not in section_names:
            continue

        collected: list[str] = []
        for next_line in body_lines[index + 1 :]:
            stripped = next_line.strip()
            if re.match(r"^#{1,6}\s+", stripped):
                break
            collected.append(next_line)

        paragraphs = list(_iter_text_paragraphs(collected))
        if paragraphs:
            return paragraphs[0]

    return ""


def _iter_text_paragraphs(lines: str | Iterable[str]):
    if isinstance(lines, str):
        iterable = lines.splitlines()
    else:
        iterable = list(lines)

    paragraph_lines: list[str] = []
    in_code_block = False

    for raw_line in iterable:
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if paragraph_lines:
                yield " ".join(paragraph_lines)
                paragraph_lines = []
            continue

        if in_code_block:
            continue

        if not stripped:
            if paragraph_lines:
                yield " ".join(paragraph_lines)
                paragraph_lines = []
            continue

        if _is_separator_line(stripped):
            if paragraph_lines:
                yield " ".join(paragraph_lines)
                paragraph_lines = []
            continue

        cleaned = _clean_text_line(stripped)
        if cleaned:
            paragraph_lines.append(cleaned)

    if paragraph_lines:
        yield " ".join(paragraph_lines)


def _is_separator_line(line: str) -> bool:
    if line.startswith("#"):
        return True
    if line.startswith("|"):
        return True
    if set(line) <= {"-", ":", "|", " "}:
        return True
    return False


def _clean_text_line(line: str) -> str:
    cleaned = line
    if cleaned.startswith(">"):
        cleaned = cleaned[1:].strip()

    cleaned = re.sub(r"^[-*+]\s+", "", cleaned)
    cleaned = re.sub(r"^\d+\.\s+", "", cleaned)
    cleaned = cleaned.strip()

    if not cleaned or cleaned.startswith("```"):
        return ""
    return cleaned


def _parse_frontmatter_value(raw_value: str) -> Any:
    value = raw_value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [
            _strip_quotes(item.strip()) for item in value[1:-1].split(",") if item.strip()
        ]
    return _strip_quotes(value)


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOP_LEVEL_SCALAR_PATTERN = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<value>.+?)\s*$")
SKILL_SOURCES_KEY = "skill_sources"


@dataclass(frozen=True)
class SkillSourceConfig:
    path: str
    format: str = ""
    confirmed: bool = False

    def resolved_path(self, project_root: Path) -> Path:
        candidate = Path(self.path)
        if candidate.is_absolute():
            return candidate
        return (project_root / candidate).resolve()


def load_rules_config(config_path: Path) -> dict[str, Any]:
    config_file = Path(config_path)
    if not config_file.exists():
        return {}

    lines = config_file.read_text(encoding="utf-8").splitlines()
    return {
        "skill_sources": load_skill_sources(config_file),
        "quality_threshold": _load_top_level_int(lines, "quality_threshold"),
        "confidence_threshold": _load_top_level_int(lines, "confidence_threshold"),
        "skill_match_limit": _load_top_level_int(lines, "skill_match_limit"),
        "agentic_match_limit": _load_top_level_int(lines, "agentic_match_limit"),
        "project_intent_override": _load_top_level_string(lines, "project_intent_override"),
    }


def load_skill_sources(config_path: Path) -> list[SkillSourceConfig]:
    config_file = Path(config_path)
    if not config_file.exists():
        return []

    lines = config_file.read_text(encoding="utf-8").splitlines()
    source_index = _find_section_index(lines, SKILL_SOURCES_KEY)
    if source_index is None:
        return []

    entries: list[SkillSourceConfig] = []
    current: dict[str, Any] | None = None

    for raw_line in lines[source_index + 1 :]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if _is_new_top_level_key(raw_line):
            break

        stripped = raw_line.strip()
        if stripped.startswith("- "):
            if current is not None:
                entries.append(_build_skill_source(current))
            current = _parse_skill_source_item(stripped[2:])
            continue

        if current is None or ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        current[key.strip()] = _parse_scalar(raw_value.strip())

    if current is not None:
        entries.append(_build_skill_source(current))

    return [entry for entry in entries if entry.path]


def load_confirmed_skill_sources(config_path: Path) -> list[SkillSourceConfig]:
    return [entry for entry in load_skill_sources(config_path) if entry.confirmed]


def normalize_config_path(path_value: str) -> str:
    normalized = path_value.replace("\\", "/")
    return normalized.rstrip("/") or normalized


def format_yaml_path(path_value: str) -> str:
    normalized = normalize_config_path(path_value)
    if any(character in normalized for character in (":", " ")):
        return f'"{normalized}"'
    return normalized


def _find_section_index(lines: list[str], key: str) -> int | None:
    for index, raw_line in enumerate(lines):
        if raw_line.lstrip().startswith("#"):
            continue
        if re.match(rf"^\s*{re.escape(key)}\s*:\s*$", raw_line):
            return index
    return None


def _is_new_top_level_key(raw_line: str) -> bool:
    return bool(raw_line and not raw_line.startswith((" ", "\t")) and ":" in raw_line)


def _parse_skill_source_item(raw_item: str) -> dict[str, Any]:
    stripped = raw_item.strip()
    if ":" in stripped:
        key, raw_value = stripped.split(":", 1)
        return {key.strip(): _parse_scalar(raw_value.strip())}
    return {"path": _parse_scalar(stripped)}


def _build_skill_source(raw_entry: dict[str, Any]) -> SkillSourceConfig:
    return SkillSourceConfig(
        path=str(raw_entry.get("path") or "").strip(),
        format=str(raw_entry.get("format") or "").strip(),
        confirmed=bool(raw_entry.get("confirmed") is True),
    )


def _load_top_level_int(lines: list[str], key: str) -> int | None:
    for raw_line in lines:
        if raw_line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_SCALAR_PATTERN.match(raw_line.strip())
        if match is None or match.group("key") != key:
            continue

        value = _parse_scalar(match.group("value"))
        if isinstance(value, int):
            return value
    return None


def _load_top_level_string(lines: list[str], key: str) -> str | None:
    for raw_line in lines:
        if raw_line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_SCALAR_PATTERN.match(raw_line.strip())
        if match is None or match.group("key") != key:
            continue

        value = _parse_scalar(match.group("value"))
        if isinstance(value, str):
            return value
    return None


def _parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        return ""

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)

    return value

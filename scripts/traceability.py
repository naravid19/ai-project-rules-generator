from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from rules_config import load_confirmed_skill_sources, load_skill_sources

SKILL_SOURCE_PATH_PATTERN = re.compile(r"<!--\s*Skill_Source_Path:\s*(?P<path>.+?)\s*-->")
CONFIRMED_SOURCE_PATTERN = re.compile(
    r"<!--\s*Confirmed_Skill_Source:\s*(?P<value>true|false)\s*-->",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TraceabilityMetadata:
    skill_source_path: str = ""
    confirmed_skill_source: bool = False


def extract_traceability_metadata(content: str) -> TraceabilityMetadata:
    path_match = SKILL_SOURCE_PATH_PATTERN.search(content)
    confirmed_match = CONFIRMED_SOURCE_PATTERN.search(content)
    return TraceabilityMetadata(
        skill_source_path=(path_match.group("path").strip() if path_match else ""),
        confirmed_skill_source=bool(
            confirmed_match and confirmed_match.group("value").lower() == "true"
        ),
    )


def validate_traceability_file(project_root: Path, file_path: Path) -> list[str]:
    content = Path(file_path).read_text(encoding="utf-8")
    metadata = extract_traceability_metadata(content)
    return validate_traceability_metadata(project_root, metadata)


def validate_traceability_metadata(
    project_root: Path,
    metadata: TraceabilityMetadata,
) -> list[str]:
    root = Path(project_root).resolve()
    errors: list[str] = []

    if not metadata.skill_source_path:
        errors.append("Missing Skill_Source_Path metadata comment.")
        return errors

    resolved_path = _resolve_metadata_path(root, metadata.skill_source_path)
    if not resolved_path.exists():
        errors.append("Traceability path does not exist in the filesystem.")

    if not metadata.confirmed_skill_source:
        errors.append("Confirmed_Skill_Source metadata must be true.")

    configured_sources = load_skill_sources(root / ".rulesrc.yaml")
    if configured_sources and not _matches_configured_source(root, metadata.skill_source_path, configured_sources):
        errors.append("Traceability path is not listed in .rulesrc.yaml skill_sources.")

    confirmed_sources = load_confirmed_skill_sources(root / ".rulesrc.yaml")
    if confirmed_sources and not _matches_configured_source(root, metadata.skill_source_path, confirmed_sources):
        errors.append("Traceability path is not one of the confirmed skill sources.")

    return errors


def _resolve_metadata_path(project_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def _matches_configured_source(project_root: Path, raw_metadata_path: str, sources) -> bool:
    resolved_metadata = _resolve_metadata_path(project_root, raw_metadata_path)
    for source in sources:
        if source.path == raw_metadata_path:
            return True
        if source.resolved_path(project_root) == resolved_metadata:
            return True
    return False

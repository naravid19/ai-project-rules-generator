from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from rules_config import (
    SkillSourceConfig,
    format_yaml_path,
    load_confirmed_skill_sources,
    load_rules_config,
    load_skill_sources,
    normalize_config_path,
)
from config_runtime import (
    detect_native_mcp_servers,
    load_mcp_registry,
    load_runtime_defaults,
    route_mcp_servers,
)
from project_rules_runtime import (
    ConfirmedSkillSource,
    ProjectRulesRuntimeError,
    resolve_confirmed_skill_source,
)


def load_runtime_config(config_path: Path) -> dict[str, Any]:
    return load_runtime_defaults(config_path)


__all__ = [
    "ConfirmedSkillSource",
    "ProjectRulesRuntimeError",
    "SkillSourceConfig",
    "detect_native_mcp_servers",
    "format_yaml_path",
    "load_confirmed_skill_sources",
    "load_mcp_registry",
    "load_rules_config",
    "load_runtime_config",
    "load_skill_sources",
    "normalize_config_path",
    "resolve_confirmed_skill_source",
    "route_mcp_servers",
]

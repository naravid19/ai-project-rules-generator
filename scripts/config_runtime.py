from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from rules_config import load_rules_config

DEFAULT_MCP_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "templates" / "mcp_registry.yaml"
MCP_CONFIG_CANDIDATES = (
    Path(".cursor") / "mcp.json",
    Path(".cursor") / "mcp.jsonc",
    Path(".claude") / "mcp.json",
    Path(".mcp.json"),
)
HOME_MCP_CONFIG_CANDIDATES = (
    Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",
    Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
    Path.home() / ".config" / "Claude" / "claude_desktop_config.json",
    Path.home() / ".claude.json",
)
YAML_LIST_ITEM_PATTERN = re.compile(r"^\s*-\s*(.+?)\s*$")
YAML_SECTION_PATTERN = re.compile(r"^(?P<key>[A-Za-z0-9_-]+)\s*:\s*$")


def load_mcp_registry(registry_path: Path | None = None) -> dict[str, list[str]]:
    path = registry_path or DEFAULT_MCP_REGISTRY_PATH
    if not path.exists():
        return {}

    lines = path.read_text(encoding="utf-8").splitlines()
    registry: dict[str, list[str]] = {}
    current_key = ""

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        section_match = YAML_SECTION_PATTERN.match(raw_line)
        if section_match:
            current_key = section_match.group("key")
            registry.setdefault(current_key, [])
            continue

        if not current_key:
            continue

        item_match = YAML_LIST_ITEM_PATTERN.match(raw_line)
        if item_match:
            registry[current_key].append(_strip_yaml_scalar(item_match.group(1)))

    return registry


def detect_native_mcp_servers(project_root: Path) -> list[str]:
    root = Path(project_root).resolve()
    detected: list[str] = []

    for candidate in list(MCP_CONFIG_CANDIDATES) + list(HOME_MCP_CONFIG_CANDIDATES):
        config_path = candidate if candidate.is_absolute() else root / candidate
        if not config_path.exists():
            continue

        payload = _load_jsonc_file(config_path)
        if not isinstance(payload, dict):
            continue

        servers = payload.get("mcpServers") or payload.get("servers") or {}
        if isinstance(servers, dict):
            for server_name in servers:
                if server_name not in detected:
                    detected.append(str(server_name))

    return detected


def route_mcp_servers(
    user_intent: str,
    tech_stack: list[str] | tuple[str, ...] | str,
    registry: dict[str, list[str]] | None = None,
) -> list[str]:
    effective_registry = registry or load_mcp_registry()
    haystack = " ".join(
        [user_intent.lower(), *(_normalize_sequence(tech_stack))]
    )
    matched: list[str] = []

    for intent_key, servers in effective_registry.items():
        if intent_key.lower().replace("-", " ") not in haystack:
            continue
        for server in servers:
            if server not in matched:
                matched.append(server)

    return matched


def load_runtime_defaults(config_path: Path) -> dict[str, Any]:
    payload = load_rules_config(config_path)
    if payload.get("confidence_threshold") is None:
        payload["confidence_threshold"] = 80
    if payload.get("skill_match_limit") is None:
        payload["skill_match_limit"] = 5
    if payload.get("agentic_match_limit") is None:
        payload["agentic_match_limit"] = 3
    return payload


def _load_jsonc_file(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    sanitized = re.sub(r"//.*?$", "", raw, flags=re.MULTILINE)
    sanitized = re.sub(r"/\*.*?\*/", "", sanitized, flags=re.DOTALL)
    try:
        return json.loads(sanitized)
    except json.JSONDecodeError:
        return {}


def _normalize_sequence(value: list[str] | tuple[str, ...] | str) -> list[str]:
    if isinstance(value, str):
        return [value.lower()]
    return [str(item).lower() for item in value]


def _strip_yaml_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")

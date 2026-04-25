from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar
from uuid import uuid4

from memory_manager import refresh_project_state

P = ParamSpec("P")
R = TypeVar("R")


class AuditLoggingError(RuntimeError):
    """Raised when project-local audit logging fails."""


@dataclass(frozen=True)
class AuditSession:
    project_root: Path
    platform: str
    session_id: str

    @property
    def log_directory(self) -> Path:
        return self.project_root / ".agent" / "logs"

    def build_log_path(self) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return self.log_directory / f"log_{timestamp}_{self.platform}_{self.session_id}.json"


def audit_logger(action: str, platform: str = "generic") -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            project_root = Path(kwargs.get("project_root", ".")).resolve()
            session = AuditSession(
                project_root=project_root,
                platform=str(kwargs.get("platform", platform)),
                session_id=str(kwargs.get("session_id") or uuid4().hex[:8]),
            )
            event = {
                "session_id": session.session_id,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "project_root": str(project_root),
                "confirmed_skill_source_path": str(kwargs.get("confirmed_skill_source_path", "")),
                "platform_targets": _listify(kwargs.get("platform_targets", session.platform)),
                "action": action,
                "status": "started",
                "confidence_score": kwargs.get("confidence_score"),
                "selected_keywords": _listify(kwargs.get("selected_keywords", [])),
                "matched_skill_paths": [],
                "output_files": [],
                "verification_status": kwargs.get("verification_status", ""),
                "error_code": "",
                "error_message": "",
            }

            print(f"[audit] {action} -> starting ({session.platform}, session={session.session_id})")

            try:
                result = func(*args, **kwargs)
                _merge_result_metadata(event, result)
                event["status"] = "success"
                return result
            except Exception as exc:
                event["status"] = "error"
                event["error_code"] = exc.__class__.__name__
                event["error_message"] = str(exc)
                raise
            finally:
                _write_audit_log(session, event)
                refresh_project_state(project_root)
                print(f"[audit] {action} -> {event['status']}")

        return wrapper

    return decorator


def _merge_result_metadata(event: dict[str, Any], result: Any) -> None:
    if not isinstance(result, dict):
        return

    for key in ("matched_skill_paths", "output_files", "verification_status"):
        value = result.get(key)
        if value is None:
            continue
        if key == "verification_status":
            event[key] = str(value)
        else:
            event[key] = _listify(value)


def _write_audit_log(session: AuditSession, event: dict[str, Any]) -> None:
    try:
        session.log_directory.mkdir(parents=True, exist_ok=True)
        session.build_log_path().write_text(json.dumps(event, indent=2), encoding="utf-8")
    except OSError as exc:
        raise AuditLoggingError(
            "Failed to write the project-local audit log. Pause and ask the user before continuing."
        ) from exc


def _listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return [str(value)]

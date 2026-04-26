from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def compute_state_diff(old_state: dict[str, Any], new_state: dict[str, Any]) -> dict[str, Any]:
    diff = {}
    ignore_keys = {"session_id", "timestamp_utc", "project_root"}
    for key in new_state:
        if key in ignore_keys:
            continue
        old_val = old_state.get(key)
        new_val = new_state.get(key)
        if isinstance(new_val, list) and isinstance(old_val, list):
            if sorted(map(str, new_val)) != sorted(map(str, old_val)):
                diff[key] = {"old": old_val, "new": new_val}
        elif new_val != old_val:
            diff[key] = {"old": old_val, "new": new_val}
    return diff


def format_state_change_notice(diff: dict[str, Any]) -> str:
    if not diff:
        return "No significant state changes detected."
    lines = []
    for key, values in diff.items():
        lines.append(f"- **{key}**: `{values['old']}` -> `{values['new']}`")
    return "\n".join(lines)


def summarize_recent_logs(project_root: Path, max_logs: int = 10) -> str:
    root = Path(project_root).resolve()
    log_dir = root / ".agent" / "logs"
    events = _load_recent_events(log_dir, max_logs=max_logs)

    lines = [
        "# Project State",
        "",
        f"- Project root: `{root}`",
    ]

    if not events:
        lines.extend(
            [
                "- Latest phase: No audited execution has been recorded yet.",
                "- Confirmed skill source: Unknown",
                "- Recently used skills: None",
                "- Latest verification: Unknown",
            ]
        )
        return "\n".join(lines) + "\n"

    latest = events[-1]
    matched_skills = _flatten_unique(events, "matched_skill_paths")
    outputs = _flatten_unique(events, "output_files")

    lines.extend(
        [
            f"- Latest phase: `{latest.get('action', 'unknown')}`",
            f"- Latest status: `{latest.get('status', 'unknown')}`",
            f"- Confirmed skill source: `{latest.get('confirmed_skill_source_path', 'unknown')}`",
            f"- Latest confidence score: `{latest.get('confidence_score', 'unknown')}`",
            f"- Recently selected keywords: `{', '.join(latest.get('selected_keywords', [])) or 'none'}`",
            f"- Recently used skills: `{', '.join(matched_skills) or 'none'}`",
            f"- Latest output files: `{', '.join(outputs) or 'none'}`",
            f"- Latest verification: `{latest.get('verification_status', latest.get('status', 'unknown'))}`",
        ]
    )

    recent_errors = [event for event in events if event.get("status") == "error"]
    if recent_errors:
        last_error = recent_errors[-1]
        lines.append(
            f"- Last error: `{last_error.get('error_code', 'unknown')}: {last_error.get('error_message', 'unknown')}`"
        )

    lines.append("\n## Change Log\n")
    if len(events) >= 2:
        # Show diffs for the last 5 events
        for i in range(max(0, len(events) - 5), len(events)):
            if i == 0:
                continue
            old = events[i - 1]
            new = events[i]
            diff = compute_state_diff(old, new)
            if diff:
                timestamp = new.get('timestamp_utc', 'unknown')
                action = new.get('action', 'unknown')
                lines.append(f"### {timestamp} ({action})")
                lines.append(format_state_change_notice(diff))
                lines.append("")
    else:
        lines.append("Not enough history to generate a change log.")

    return "\n".join(lines) + "\n"


def refresh_project_state(project_root: Path, max_logs: int = 10) -> Path:
    root = Path(project_root).resolve()
    memory_dir = root / ".agent" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    summary_path = memory_dir / "project_state.md"
    summary_path.write_text(summarize_recent_logs(root, max_logs=max_logs), encoding="utf-8")
    return summary_path


def _load_recent_events(log_dir: Path, max_logs: int) -> list[dict[str, Any]]:
    if not log_dir.exists():
        return []

    log_files = sorted(
        log_dir.glob("log_*.json"),
        key=lambda path: path.name,
    )[-max_logs:]

    events: list[dict[str, Any]] = []
    for log_file in log_files:
        try:
            payload = json.loads(log_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _flatten_unique(events: list[dict[str, Any]], key: str) -> list[str]:
    unique: list[str] = []
    for event in events:
        raw_value = event.get(key, [])
        if not isinstance(raw_value, list):
            continue
        for item in raw_value:
            text = str(item).strip()
            if text and text not in unique:
                unique.append(text)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize project-local audit logs into project state memory.")
    parser.add_argument("--project-root", default=".", help="Project root that owns .agent/logs")
    parser.add_argument("--max-logs", type=int, default=10, help="Number of recent logs to summarize")
    args = parser.parse_args()

    output_path = refresh_project_state(Path(args.project_root), max_logs=args.max_logs)
    print(output_path)


if __name__ == "__main__":
    main()

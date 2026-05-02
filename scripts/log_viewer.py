from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

def format_timestamp(ts_str: str) -> str:
    try:
        return ts_str[:19].replace("T", " ")
    except Exception:
        return "N/A"

def view_logs(log_dir: Path, limit: int = 10, detail_id: str | None = None):
    if not log_dir.exists():
        print(f"Error: Log directory not found at {log_dir}")
        return

    logs = sorted(log_dir.glob("log_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if detail_id:
        _show_detail(logs, detail_id)
        return

    print(f"\n--- Recent Audit Logs (showing top {min(len(logs), limit)}) ---")
    header = f"{'Timestamp':<20} | {'Action':<15} | {'Status':<8} | {'Score':<5} | {'Reasoning'}"
    print(header)
    print("-" * len(header))
    
    for log_path in logs[:limit]:
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
            ts = format_timestamp(data.get("timestamp_utc", ""))
            action = data.get("action", "unknown")
            status = data.get("status", "unknown")
            score = str(data.get("confidence_score", "-"))
            reasoning = str(data.get("reasoning") or "")
            if len(reasoning) > 45:
                reasoning = reasoning[:42] + "..."
            
            color_code = ""
            if status == "error": color_code = "\033[91m" # Red
            elif status == "success": color_code = "\033[92m" # Green
            
            reset = "\033[0m"
            print(f"{ts:<20} | {action:<15} | {color_code}{status:<8}{reset} | {score:<5} | {reasoning}")
        except Exception:
            continue
    
    print(f"\nTip: Use --session <id> to see full details of a specific log.")

def _show_detail(logs: list[Path], session_id: str):
    target = None
    for log in logs:
        if session_id in log.name:
            target = log
            break
    
    if not target:
        print(f"Error: Session '{session_id}' not found.")
        return

    data = json.loads(target.read_text(encoding="utf-8"))
    print(f"\n=== Detailed Audit Log: {session_id} ===")
    print(json.dumps(data, indent=2))

def main():
    parser = argparse.ArgumentParser(description="AI Project Rules Generator - Log Viewer")
    parser.add_argument("--dir", default=".agent/logs", help="Directory containing JSON logs")
    parser.add_argument("--limit", type=int, default=15, help="Number of logs to show")
    parser.add_argument("--session", help="Show full JSON for a specific session ID")
    
    args = parser.parse_args()
    view_logs(Path(args.dir), limit=args.limit, detail_id=args.session)

if __name__ == "__main__":
    main()

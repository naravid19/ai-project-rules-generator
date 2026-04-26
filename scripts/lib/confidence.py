from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from project_rules_runtime import (
    ConfidenceResult,
    ProjectRulesRuntimeError,
    enforce_confidence_threshold,
    score_project_confidence,
)
from typing import Any


def compute_confidence_report(project_root: Path | str, threshold: int = 80) -> dict[str, Any]:
    result = score_project_confidence(Path(project_root), threshold=threshold)
    return {
        "score": result.score,
        "threshold": result.threshold,
        "requires_clarification": result.requires_clarification,
        "reasons": list(result.reasons),
        "clarification_options": list(result.clarification_options),
        "detected_manifests": list(result.detected_manifests),
        "detected_frameworks": list(result.detected_frameworks),
    }


def format_confidence_summary(report: dict[str, Any]) -> str:
    score = report["score"]
    status = "PASS" if not report["requires_clarification"] else "FAIL"
    lines = [
        f"Confidence Score: {score}/100 ({status})",
        "Reasons:"
    ]
    for reason in report["reasons"]:
        lines.append(f"  - {reason}")
    if report["detected_frameworks"]:
        lines.append(f"Frameworks: {', '.join(report['detected_frameworks'])}")
    if report["requires_clarification"]:
        options = ", ".join(report["clarification_options"])
        lines.append(f"\nClarification Needed! Options: {options}")
    return "\n".join(lines)


__all__ = [
    "ConfidenceResult",
    "ProjectRulesRuntimeError",
    "enforce_confidence_threshold",
    "score_project_confidence",
    "compute_confidence_report",
    "format_confidence_summary",
]

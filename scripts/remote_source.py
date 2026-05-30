"""Minimal git-based remote skill source resolver."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


def resolve_remote_source(
    url: str,
    cache_root: Path,
    offline: bool = False,
) -> Path:
    """Clone or pull a remote git repo into cache_root and return the local path.

    Args:
        url: Git-compatible URL (https or ssh).
        cache_root: Directory to store cloned repos.
        offline: If True, use existing cache without network access.

    Returns:
        Path to the cloned/cached repo directory.

    Raises:
        RuntimeError: If clone/pull fails and no cached copy exists.
    """
    repo_name = _extract_repo_name(url)
    target_dir = cache_root / repo_name

    if target_dir.exists() and any(target_dir.iterdir()):
        if offline:
            return target_dir
        try:
            subprocess.run(
                ["git", "-C", str(target_dir), "pull", "--ff-only"],
                capture_output=True,
                check=True,
                timeout=30,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass  # Use existing cache on pull failure
        return target_dir

    if offline:
        raise RuntimeError(
            f"No cached copy and offline mode is enabled: {url}"
        )

    cache_root.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target_dir)],
            capture_output=True,
            check=True,
            timeout=60,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        raise RuntimeError(
            f"Failed to clone remote skill source: {url}"
        ) from exc

    return target_dir


def _extract_repo_name(url: str) -> str:
    """Extract a safe directory name from a git URL."""
    cleaned = url.rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    name = cleaned.rsplit("/", 1)[-1]
    return re.sub(r"[^\w\-.]", "_", name) or "remote-skills"

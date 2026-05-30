"""Tests for Multi-Source Skill Map feature."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure scripts/ is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))


# ---------------------------------------------------------------------------
# Task 1: SkillSourceConfig extensions
# ---------------------------------------------------------------------------


def test_skill_source_config_has_type_and_source_name():
    """SkillSourceConfig should have type and source_name fields."""
    from rules_config import SkillSourceConfig

    config = SkillSourceConfig(path=".agent", type="local", source_name="project-local")
    assert config.type == "local"
    assert config.source_name == "project-local"


def test_skill_source_config_defaults():
    """type defaults to 'local', source_name defaults to empty string."""
    from rules_config import SkillSourceConfig

    config = SkillSourceConfig(path=".agent")
    assert config.type == "local"
    assert config.source_name == ""


def test_load_skill_sources_parses_type(tmp_path):
    """load_skill_sources should parse type and source_name fields from yaml."""
    from rules_config import load_skill_sources

    config_file = tmp_path / ".rulesrc.yaml"
    config_file.write_text(
        "skill_sources:\n"
        "  - path: .agent\n"
        "    confirmed: true\n"
        "    type: local\n"
        "  - path: ~/.gemini/config/skills\n"
        "    type: global\n"
        "    source_name: gemini-skills\n",
        encoding="utf-8",
    )
    sources = load_skill_sources(config_file)
    assert len(sources) == 2
    assert sources[0].type == "local"
    assert sources[1].type == "global"
    assert sources[1].source_name == "gemini-skills"


def test_load_all_skill_sources(tmp_path):
    """load_all_skill_sources should return all sources including non-confirmed."""
    from rules_config import load_all_skill_sources

    config_file = tmp_path / ".rulesrc.yaml"
    config_file.write_text(
        "skill_sources:\n"
        "  - path: .agent\n"
        "    confirmed: true\n"
        "    type: local\n"
        "  - path: ~/.gemini/config/skills\n"
        "    type: global\n",
        encoding="utf-8",
    )
    sources = load_all_skill_sources(config_file)
    assert len(sources) == 2


# ---------------------------------------------------------------------------
# Task 2: CatalogEntry extensions
# ---------------------------------------------------------------------------


def test_catalog_entry_has_source_fields():
    """CatalogEntry should include source_type and source_name."""
    from indexer import CatalogEntry

    entry = CatalogEntry(
        id="test-skill",
        path="skills/test/SKILL.md",
        tags=["testing"],
        description="A test skill.",
        source_type="global",
        source_name="gemini-skills",
    )
    d = entry.to_dict()
    assert d["source_type"] == "global"
    assert d["source_name"] == "gemini-skills"


def test_catalog_entry_defaults():
    """source_type defaults to 'local', source_name to empty string."""
    from indexer import CatalogEntry

    entry = CatalogEntry(id="x", path="x", tags=[], description="x")
    assert entry.source_type == "local"
    assert entry.source_name == ""


# ---------------------------------------------------------------------------
# Task 3: remote_source.py
# ---------------------------------------------------------------------------


def test_resolve_remote_source_local_fallback(tmp_path):
    """If cache dir already has content, use it without network (offline=True)."""
    from remote_source import resolve_remote_source

    cache_dir = tmp_path / "cache"
    repo_dir = cache_dir / "my-skills"
    repo_dir.mkdir(parents=True)
    (repo_dir / "SKILL.md").write_text("# Test", encoding="utf-8")

    result = resolve_remote_source(
        "https://example.com/user/my-skills.git",
        cache_dir,
        offline=True,
    )
    assert result == repo_dir


def test_resolve_remote_source_offline_no_cache(tmp_path):
    """Should raise RuntimeError if offline=True and no cached copy exists."""
    from remote_source import resolve_remote_source

    with pytest.raises(RuntimeError, match="offline"):
        resolve_remote_source(
            "https://example.com/user/my-skills.git",
            tmp_path / "cache",
            offline=True,
        )


def test_extract_repo_name_from_url():
    """_extract_repo_name should strip .git and return safe name."""
    from remote_source import _extract_repo_name

    assert _extract_repo_name("https://github.com/user/my-skills.git") == "my-skills"
    assert _extract_repo_name("https://github.com/user/my-skills") == "my-skills"
    assert _extract_repo_name("git@github.com:user/my-skills.git") == "my-skills"


# ---------------------------------------------------------------------------
# Task 4: build_unified_catalog()
# ---------------------------------------------------------------------------


def _make_skill_dir(parent: Path, name: str, description: str) -> Path:
    """Helper: create a minimal skill directory with SKILL.md."""
    skill_dir = parent / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n# {name.title()}\n",
        encoding="utf-8",
    )
    return skill_dir


def test_build_unified_catalog(tmp_path):
    """build_unified_catalog merges entries from multiple sources with source_type tags."""
    from indexer import build_unified_catalog
    from rules_config import SkillSourceConfig

    local_root = tmp_path / ".agent"
    _make_skill_dir(local_root, "skill-a", "Local skill A.")

    global_root = tmp_path / "global-skills"
    _make_skill_dir(global_root, "skill-b", "Global skill B.")

    sources = [
        SkillSourceConfig(
            path=str(local_root),
            confirmed=True,
            type="local",
            source_name="project",
        ),
        SkillSourceConfig(
            path=str(global_root),
            type="global",
            source_name="gemini",
        ),
    ]

    catalog_path = build_unified_catalog(
        project_root=tmp_path,
        sources=sources,
        output_path=tmp_path / "catalog.json",
    )

    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert len(entries) == 2

    types = {e["source_type"] for e in entries}
    assert "local" in types
    assert "global" in types

    names = {e["source_name"] for e in entries}
    assert "project" in names
    assert "gemini" in names


def test_build_unified_catalog_backward_compat(tmp_path):
    """With a single source (no type), catalog still works correctly."""
    from indexer import build_unified_catalog
    from rules_config import SkillSourceConfig

    local_root = tmp_path / ".agent"
    _make_skill_dir(local_root, "skill-c", "A backward-compat skill.")

    sources = [
        SkillSourceConfig(path=str(local_root), confirmed=True),
    ]
    catalog_path = build_unified_catalog(
        project_root=tmp_path,
        sources=sources,
        output_path=tmp_path / "catalog.json",
    )
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert len(entries) == 1
    # Default type should be "local"
    assert entries[0]["source_type"] == "local"


# ---------------------------------------------------------------------------
# Task 5: generate_skill_map_md()
# ---------------------------------------------------------------------------


def test_generate_skill_map_md(tmp_path):
    """generate_skill_map_md creates a readable Markdown summary."""
    from indexer import generate_skill_map_md, CatalogEntry

    entries = [
        CatalogEntry(
            id="brainstorming",
            path=".agent/skills/brainstorming/SKILL.md",
            tags=["planning"],
            description="Explores user intent.",
            source_type="local",
            source_name="project",
        ),
        CatalogEntry(
            id="chrome-devtools",
            path="global/chrome-devtools/SKILL.md",
            tags=["mcp", "testing"],
            description="Chrome DevTools debugging.",
            source_type="global",
            source_name="gemini",
        ),
    ]

    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(
        json.dumps([e.to_dict() for e in entries], indent=2), encoding="utf-8"
    )

    md_path = generate_skill_map_md(catalog_path, output_path=tmp_path / "skill_map.md")
    content = md_path.read_text(encoding="utf-8")

    assert "# 🗺️ Skill Map" in content
    assert "Local Skills" in content
    assert "Global Skills" in content
    assert "brainstorming" in content
    assert "chrome-devtools" in content
    assert "Total:" in content or "Total" in content


def test_generate_skill_map_md_no_remote_section_when_empty(tmp_path):
    """Remote section should show 'no remote sources' when there are none."""
    from indexer import generate_skill_map_md, CatalogEntry

    entries = [
        CatalogEntry(
            id="skill-a",
            path=".agent/skill-a/SKILL.md",
            tags=[],
            description="Only local.",
            source_type="local",
            source_name="project",
        ),
    ]
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps([e.to_dict() for e in entries]), encoding="utf-8")

    md_path = generate_skill_map_md(catalog_path, output_path=tmp_path / "skill_map.md")
    content = md_path.read_text(encoding="utf-8")

    assert "Remote Skills (0)" in content


# ---------------------------------------------------------------------------
# Task 6: source-priority weighting
# ---------------------------------------------------------------------------


def test_source_priority_weighting():
    """Local skills should outrank global/remote with equal base score."""
    SOURCE_PRIORITY_WEIGHTS = {"local": 1.2, "global": 1.0, "remote": 0.8}
    base = 1.0
    local_score = base * SOURCE_PRIORITY_WEIGHTS["local"]
    global_score = base * SOURCE_PRIORITY_WEIGHTS["global"]
    remote_score = base * SOURCE_PRIORITY_WEIGHTS["remote"]
    assert local_score > global_score > remote_score


# ---------------------------------------------------------------------------
# Edge Cases & Fault Tolerance
# ---------------------------------------------------------------------------


def test_generate_skill_map_md_invalid_json(tmp_path):
    """If catalog.json is corrupted, generate_skill_map_md should default to empty list."""
    from indexer import generate_skill_map_md

    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text("{ invalid json ", encoding="utf-8")

    md_path = generate_skill_map_md(catalog_path, output_path=tmp_path / "skill_map.md")
    content = md_path.read_text(encoding="utf-8")
    
    assert "Total: 0 skills" in content
    assert "Local Skills" in content


def test_generate_skill_map_md_unknown_source_type(tmp_path):
    """Unknown source_type should be grouped and titled correctly (capitalized)."""
    from indexer import generate_skill_map_md, CatalogEntry

    entries = [
        CatalogEntry(
            id="weird-skill",
            path="skills/weird/SKILL.md",
            tags=[],
            description="Unknown scope.",
            source_type="enterprise",
            source_name="corp",
        )
    ]
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps([e.to_dict() for e in entries]), encoding="utf-8")

    md_path = generate_skill_map_md(catalog_path, output_path=tmp_path / "skill_map.md")
    content = md_path.read_text(encoding="utf-8")

    assert "## Enterprise Skills (1)" in content
    assert "weird-skill" in content


def test_resolve_remote_source_pull_failure_fallback(tmp_path, monkeypatch):
    """If a cached repo exists but git pull fails, it should fallback to using the cache."""
    from remote_source import resolve_remote_source
    import subprocess

    cache_dir = tmp_path / "cache"
    repo_dir = cache_dir / "my-skills"
    repo_dir.mkdir(parents=True)
    (repo_dir / "SKILL.md").write_text("# Test", encoding="utf-8")

    # Mock subprocess.run to simulate network timeout on pull
    def mock_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="git pull", timeout=30)
    
    monkeypatch.setattr(subprocess, "run", mock_run)

    result = resolve_remote_source(
        "https://example.com/user/my-skills.git",
        cache_dir,
        offline=False,
    )
    assert result == repo_dir


def test_resolve_remote_source_clone_failure(tmp_path, monkeypatch):
    """If clone fails (no cache exists), it should raise RuntimeError."""
    from remote_source import resolve_remote_source
    import subprocess

    cache_dir = tmp_path / "cache"
    
    def mock_run(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=128, cmd="git clone")
    
    monkeypatch.setattr(subprocess, "run", mock_run)

    with pytest.raises(RuntimeError, match="Failed to clone remote skill source"):
        resolve_remote_source(
            "https://example.com/user/my-skills.git",
            cache_dir,
            offline=False,
        )


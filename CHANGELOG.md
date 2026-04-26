# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.9.2][1.9.2] - 2026-04-26

### Added

- **Integrated Audit Logging (Pillar 4)**: Added `@audit_logger` decoration to core Python modules (`wizard.py`, `indexer.py`). Every configuration and indexing action now produces a project-local JSON log at `.agent/logs/` for traceability and error tracking.
- **System Memory Injection (Pillar 5)**: Implemented automated memory management via `memory_manager.py`. AI agents are now instructed to silently read `.agent/memory/project_state.md` to maintain cross-session context and project profile awareness.
- **Tiered Skill Orchestration**: Implemented "Double Search" logic to separate skill discovery into two tiers: `agentic_match_limit` (for functional skills like Planning and Memory) and `skill_match_limit` (for technical implementation skills). This ensures AI agents always load foundational reasoning capabilities alongside coding capabilities without exhausting context windows.
- **Flexible Agentic Execution**: Implemented a Dual-Mode Strategy (Enhanced Scripted vs. Autonomous Fallback) to support zero-install users. AI now automatically evaluates the workspace and uses native capabilities if Python scripts are missing.
- **Full Design Token Extraction**: Upgraded `extract_design_tokens()` from a stub to a functional regex-based parser that handles `tailwind.config.*` files and CSS custom properties.
- **Anti-Overload Rule**: Strict constraints for manual skill discovery (list first, filter, read max 3-5 relevant files) to prevent context window saturation.
- **Unit Testing**: Added regression coverage for design token parsing and catalog validation fixes.

## [1.9.1][1.9.1] - 2026-04-26

### Added

- **Enterprise-Grade Runtime Hardening**: Fully functional incremental indexing and catalog validation (Pillars 1 & 3), plus an enhanced memory manager with log rotation and automated state diff summaries (Pillars 4 & 5).
- **Stage 1.5 Runtime Bootstrapping**: Embedded into `workflows/create-project-rules.md` to automatically trigger incremental catalog updates and state memory refreshes prior to generation.
- **Accuracy Hardening & Constraint Verification**: New internal safeguards including §1.2b source-of-truth design token parsing, §1.3 deep directory & dependency scan, §1.3b constraint verification, and §4.5 pre-write accuracy gate.
- **Expanded Testing**: Added unit tests to `tests/test_architecture.py` covering audit log rotation, state diff computation, and incremental indexing.
- **`extract_design_tokens()` Stub**: Runtime stub for processing visual constraints.

### Changed

- **Workflow AI Self-Sufficiency**: Refactored `workflows/create-project-rules.md` so that quick-start users can rely entirely on native AI capabilities without needing to execute Python scripts.
- **Documentation Qualifiers**: Explicitly marked script-dependent features (CLI examples, benchmarks, local smoke checks, and output validation) as "Full Repo Clone Only" in the `README.md` to prevent confusion for quick-start users.

## [1.9.0][1.9.0] - 2026-04-25

### Added

- **Native MCP Auto-Discovery**: Automatically discovers and loads Model Context Protocol (MCP) servers, giving your AI agents seamless access to external tools and context.
- **Audit Logging & Memory**: Introduced project-local audit trails and memory summarization. Your agents can now retain context and remember past decisions across different sessions.
- **Confidence Gating**: New runtime protections that evaluate skill relevance, ensuring only highly confident, appropriate skills are included in your generated rules.
- **Skill Catalog Indexing**: Lightweight indexing for faster and more reliable skill discovery.
- **Comprehensive Testing**: Extensive regression coverage for architecture, MCP routing, audit logs, and validators.

### Changed

- **Interactive Configuration (`wizard.py`)**: Now strictly enforces a single confirmed skill source root to prevent conflicts, while retaining your previous `.rulesrc.yaml` settings.
- **Enhanced Output Validation**: The validator scripts now strictly enforce traceability metadata, verify physical skill source paths, and mandate dedicated `[Native MCP Servers]` and `[Local Agent Skills]` sections in `AGENTS.md`.
- **Documentation Overhaul**: Updated `README.md`, `AGENTS.md`, and templates to provide clear, easy-to-understand guidance on the new features.

## [1.8.0][1.8.0] - 2026-03-22

### Added

- Multi-root discovery support in `scripts/discover-skills.py`, including repeated `--agent-dir` handling, ordered root precedence, and deterministic deduplication across shared and local `.agent` roots
- Companion skill metadata in discovery and extraction output via `source_root`, `instruction_type`, `companion_docs`, and `reference_dirs`
- Regression fixtures and tests for hybrid skill folders, `AGENTS.md`-only fallback packages, workflow/plugin roots, and duplicate source precedence handling
- Setup script support for `multica-ai/andrej-karpathy-skills` to provide Andrej Karpathy's skills and workflows alongside other recommended sources
- Setup script support for `K-Dense-AI/claude-scientific-skills` so the scientific skill collection can be installed into local or shared roots with the same optional-source flow as the other recommended repositories

### Changed

- Skill discovery now indexes one skill entity per directory, prefers `SKILL.md` as the canonical entry when available, and treats `AGENTS.md`, `CLAUDE.md`, and `README.md` as companion documents
- Source format classification now recognizes newer hybrid layouts, gives FOLDER precedence over workflow-style root docs when visible skill trees exist, and treats hidden plugin/integration markers as WORKFLOW signals only when no visible skill tree is present
- `scripts/extract-capabilities.py` now accepts either a skill directory or a supported instruction file path while preserving the existing JSON contract
- `scripts/wizard.py` now supports writing ordered `skill_sources` entries so a shared root can be configured ahead of the repo-local `.agent` fallback
- `README.md` and `workflows/create-project-rules.md` now document hybrid skill packages, ordered root precedence, companion docs, local smoke-check commands against shared and repo-local roots, and the new scientific/research-focused recommended source
- The README now includes single-source installer examples for `scientific` plus an isolated temp-root verification note for the real `claude-scientific-skills` clone/discovery/extraction flow

### Fixed

- Discovery no longer emits separate matches for companion `AGENTS.md`, `CLAUDE.md`, or `README.md` files that belong to the same skill directory
- Multi-root searches now prefer the first matching source name consistently instead of surfacing duplicate shared/local copies
- Capability extraction now resolves modern skill packages that expose guidance through adjacent docs and `references/` or `rules/` directories
- `scripts/validate-output.sh` now treats `claude-scientific-skills` and `andrej-karpathy-skills` as known source names when checking generated outputs for Rule 1 hardcoding regressions

## [1.7.0][1.7.0] - 2026-03-13

### Added

- Script-level regression coverage in `tests/test_skill_scripts.py` with committed fixtures for discovery, extraction, and wizard flows
- README compatibility and benchmark snapshot for the mixed `.agent/` layout installed by the setup scripts

### Changed

- `scripts/discover-skills.py` now skips the local `.agent/workflows/` output folder when enumerating skill sources, ranks search-engine results alongside other formats, and keeps large-catalog searches easier to trim with `--limit`
- `README.md` and `workflows/create-project-rules.md` now document reserved output paths, measured discovery performance, and the recommended discovery/extraction commands for real `.agent/` roots

### Fixed

- `scripts/discover-skills.py` no longer reports the generated workflow storage directory as an unsupported skill source
- `scripts/extract-capabilities.py` no longer crashes on `Any` import/frontmatter parsing paths and now emits stable merged tool metadata
- `scripts/wizard.py` no longer fails on Windows console encoding or malformed YAML generation paths

## [1.6.0][1.6.0] - 2026-03-06

### Added

- Active `.rulesrc.yaml` semantics for `skill_sources`, `custom_keywords`, `template_style`, and `quality_threshold`
- Shared skill root support in setup scripts via `-SkillRoot` (PowerShell) and `--skill-root` (Bash)

### Changed

- `README.md`, `AGENTS.md`, `.cursorrules`, and `workflows/create-project-rules.md` now align with the documented validator model and required section names
- Setup scripts keep the workflow local at `.agent/workflows/create-project-rules.md` while allowing optional skill repositories to install into an external/shared root
- Quick Reference cards and current-version documentation now reflect the `1.6.0` release state

### Fixed

- `scripts/validate-output.ps1` now parses on Windows PowerShell 5.1 and mirrors the documented 50-point heuristic scoring model
- `scripts/validate-output.ps1` and `scripts/validate-output.sh` now read `quality_threshold` from `.rulesrc.yaml`, print raw checks plus scorecards, and ignore anti-pattern examples when checking for hardcoded skill names

## [1.5.0][1.5.0] - 2026-03-05

### Added

- **Stage 0: User Preferences (Interactive Mode)** — Optional interactive prompts for target platforms, severity level, output language, section selection, preview mode, and existing file action
- **Configuration File (`.rulesrc.yaml`)** — Persistent config file for workflow customization; auto-detected at project root; template at `templates/rulesrc-template.yaml`
- **Multi-Language Output Support** — Generate `.cursorrules` and `AGENTS.md` in 9 languages (en, th, ja, zh, ko, es, fr, de, pt); see `i18n/README.md`
- **Preview Mode (Dry Run)** — Review planned output structure before generating files; shows estimated lines, sections, matched skills
- **Incremental Update / Diff Mode** — Update existing files without full regeneration; preserves user customizations; shows diff before applying
- **Generation Statistics Dashboard** — Post-generation summary showing skills scanned/matched/applied, lines generated, quality scores, total time, platforms, language
- **7 new template examples**: `nodejs-express`, `chrome-extension`, `nextjs-fullstack`, `go-microservice`, `unity-game`, `cli-tool`, `langchain-rag` (total: 10 templates)
- **Validation Scripts** — Initial `scripts/validate-output.ps1` and `scripts/validate-output.sh` scaffolding for automated output checks
- **5 new keyword categories**: Monorepo, Microservices, Serverless, Database, Package/Library (total: 17 categories)
- **5 new recommended skill sources**: `anthropics/skills` (official), `tech-leads-club/agent-skills` (curated), `Jeffallan/claude-skills` (full-stack), `nextlevelbuilder/ui-ux-pro-max-skill` (UI/UX workflow), `OthmanAdi/planning-with-files` (Manus-style persistence)
- **Agentic Capability Keywords** — Added `planning`, `memory`, `mcp`, `reasoning`, `workflow` keywords to trigger advanced AI orchestration skills in `create-project-rules.md` and `AGENTS.md`.
- `i18n/README.md` — Multi-language support guidelines with translation patterns

### Fixed

- **Validation Script Follow-Up Deferred** — The v1.5.0 release introduced validator scripts, but the full Windows PowerShell 5.1 parser repair and heuristic-scoring alignment are tracked in [Unreleased][Unreleased].

### Changed

- **Workflow expanded to 6 stages** (Stage 0–5) with optional Preview step between Stage 3 and 4
- **Setup scripts rewritten** (`setup.ps1`, `setup.sh`) with:
  - Git and internet prerequisite checks
  - `--NonInteractive` / `--non-interactive` mode for CI/CD
  - `--SkillSource` / `--skill-source` direct skill selection (antigravity, claude, all)
  - `--Uninstall` / `--uninstall` cleanup
  - `--Verbose` / `--verbose` debug output
  - Better error messages and backup on update
- **Quick Reference Card** updated to v1.5 with Stage 0, Preview, and update mode entries
- **README.md** — Updated feature table (13 features), supported project types (17), workflow stages table, template gallery (10), roadmap (all items completed)
- **AGENTS.md** — Updated to reference 6-stage workflow, added new Key Files entries
- **`.cursorrules`** — Updated Key Files table with new files
- **`templates/README.md`** — Expanded to 10 templates with coverage-by-category table

## [1.4.0][1.4.0] - 2026-03-03

### Added

- **WORKFLOW format support (5th format)** across `workflows/create-project-rules.md`, `.cursorrules`, `AGENTS.md`, and `README.md`
- **Quick Start Scripts**: `setup.sh` (Linux/macOS) and `setup.ps1` (Windows)
- **Template Gallery**: `templates/README.md` and 3 reference templates (`react-typescript`, `python-fastapi`, `flutter-mobile`)

### Changed

- Example output updated from Chrome Extension to Python FastAPI in `workflows/create-project-rules.md` and `README.md`
- `README.md` installation flow now includes Quick Start Script (Option A) and Manual setup (Option B)

## [1.3.0][1.3.0] - 2026-03-03

### Added

- **Format-Based Auto-Detect** skill discovery - workflow auto-detects skill sources by format (CATALOG, FOLDER, SEARCH_ENGINE, README) instead of hardcoding specific repositories
- **Multi-platform AI tool support** - generates correct files for 9 AI tools: Cursor, Claude Code, Antigravity IDE, Gemini CLI, Codex CLI, Kiro IDE/CLI, GitHub Copilot, OpenCode, AdaL CLI
- **Quality scoring system** in verification stage - 5 dimensions scored 0-10, minimum >=38/50 to pass
- **Content smell detection** checklist - identifies hardcoded names, vague rules, walls of text, duplicated content, missing time estimates, abstract examples, platform assumptions
- **Cross-file consistency check** - ensures `.cursorrules`, `AGENTS.md`, and `README.md` do not contradict each other
- **Severity levels** for rules - Critical (BLOCK), Important (HIGH), Note
- **Progressive disclosure** templates - generated files follow overview -> details structure
- **Autonomous project analysis** - AI scans codebase automatically without asking user for information
- **AI tool auto-detection** - scans project root for existing AI config files to detect which tools are in use
- **Source Format Detection table** - documents how to detect and search each skill source format
- 7 new keyword categories: Security, Testing, DevOps, Architecture, Documentation, Performance, CLI Tool (total: 12 categories)
- `.cursorrules` project rules file for this project
- `AGENTS.md` AI agent guidelines file for this project
- `CHANGELOG.md` (this file)

### Changed

- **Workflow rewrite** (`workflows/create-project-rules.md`) - major restructure of all 5 stages
- **Stage 1** now includes autonomous codebase discovery and AI tool detection
- **Stage 2** uses format-based auto-detect instead of referencing specific repositories
- **Stage 3** template now includes severity levels, progressive disclosure, and content smells table
- **Stage 4** now includes multi-platform output mapping and format-based skill section pattern
- **Stage 5** upgraded from simple checklist to quality scoring (>=38/50) with content smell detection
- Quick Reference Card updated to reflect v1.3 features
- Keyword table expanded from 5 to 12 categories
- Example output updated with severity levels and anti-patterns table
- `README.md` updated with Format-Based Skill Discovery section and Multi-Platform Support table
- All `example/` directory references replaced with GitHub links (example/ excluded from git)

### Removed

- Hardcoded skill source table ("Supported Skill Sources") - replaced with format-based detection
- Hardcoded CATALOG.md-only references in pipeline diagram - replaced with format branching

## [1.2.0][1.2.0] - 2026-02-07

### Added

- Time estimates for each workflow stage (⏱️)
- Mini example outputs (Chrome Extension project)
- Quick reference card (ASCII art)
- Architecture keywords in keyword table

## [1.1.0][1.1.0] - 2026-02-07

### Added

- Skill integration instructions in Stage 2
- Verification checklist in Stage 5
- Keyword reference table for skill discovery
- Reader test in verification stage

## [1.0.0][1.0.0] - 2026-02-07

### Added

- Initial 5-stage workflow structure
- Stage 1: Project Analysis
- Stage 2: Skill Discovery
- Stage 3: Create .cursorrules
- Stage 4: Create AGENTS.md
- Stage 5: Verification
- `.cursorrules` and `AGENTS.md` templates
- Tips for effective rules (Do's and Don'ts)

[1.9.2]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.9.1...v1.9.2
[1.9.1]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/naravid19/ai-project-rules-generator/releases/tag/v1.0.0

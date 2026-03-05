# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.5.0] - 2026-03-05

### Added

- **Stage 0: User Preferences (Interactive Mode)** — Optional interactive prompts for target platforms, severity level, output language, section selection, preview mode, and existing file action
- **Configuration File (`.rulesrc.yaml`)** — Persistent config file for workflow customization; auto-detected at project root; template at `templates/rulesrc-template.yaml`
- **Multi-Language Output Support** — Generate `.cursorrules` and `AGENTS.md` in 9 languages (en, th, ja, zh, ko, es, fr, de, pt); see `i18n/README.md`
- **Preview Mode (Dry Run)** — Review planned output structure before generating files; shows estimated lines, sections, matched skills
- **Incremental Update / Diff Mode** — Update existing files without full regeneration; preserves user customizations; shows diff before applying
- **Generation Statistics Dashboard** — Post-generation summary showing skills scanned/matched/applied, lines generated, quality scores, total time, platforms, language
- **7 new template examples**: `nodejs-express`, `chrome-extension`, `nextjs-fullstack`, `go-microservice`, `unity-game`, `cli-tool`, `langchain-rag` (total: 10 templates)
- **Validation Scripts** — `scripts/validate-output.ps1` and `scripts/validate-output.sh` for automated quality checks (file existence, section structure, content smells, cross-file consistency)
- **5 new keyword categories**: Monorepo, Microservices, Serverless, Database, Package/Library (total: 17 categories)
- **3 new recommended skill sources**: `anthropics/skills` (official), `tech-leads-club/agent-skills` (curated), `Jeffallan/claude-skills` (full-stack)
- `i18n/README.md` — Multi-language support guidelines with translation patterns

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

## [1.4.0] - 2026-03-03

### Added

- **WORKFLOW format support (5th format)** across `workflows/create-project-rules.md`, `.cursorrules`, `AGENTS.md`, and `README.md`
- **Quick Start Scripts**: `setup.sh` (Linux/macOS) and `setup.ps1` (Windows)
- **Template Gallery**: `templates/README.md` and 3 reference templates (`react-typescript`, `python-fastapi`, `flutter-mobile`)

### Changed

- Example output updated from Chrome Extension to Python FastAPI in `workflows/create-project-rules.md` and `README.md`
- `README.md` installation flow now includes Quick Start Script (Option A) and Manual setup (Option B)

## [1.3.0] - 2026-03-03

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

## [1.2.0] - 2026-02-07

### Added

- Time estimates for each workflow stage (⏱️)
- Mini example outputs (Chrome Extension project)
- Quick reference card (ASCII art)
- Architecture keywords in keyword table

## [1.1.0] - 2026-02-07

### Added

- Skill integration instructions in Stage 2
- Verification checklist in Stage 5
- Keyword reference table for skill discovery
- Reader test in verification stage

## [1.0.0] - 2026-02-07

### Added

- Initial 5-stage workflow structure
- Stage 1: Project Analysis
- Stage 2: Skill Discovery
- Stage 3: Create .cursorrules
- Stage 4: Create AGENTS.md
- Stage 5: Verification
- `.cursorrules` and `AGENTS.md` templates
- Tips for effective rules (Do's and Don'ts)

[Unreleased]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/naravid19/ai-project-rules-generator/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/naravid19/ai-project-rules-generator/releases/tag/v1.0.0

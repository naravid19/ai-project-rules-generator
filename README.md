<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/naravid19/ai-project-rules-generator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">🤖 AI Project Rules Generator</h3>

<p align="center">
    🚀 Generate .cursorrules and AGENTS.md with automatic, format-based skill discovery across mixed .agent sources
    <br />
    <a href="https://github.com/naravid19/ai-project-rules-generator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/naravid19/ai-project-rules-generator">View Demo</a>
    ·
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#supported-project-types">Supported Project Types</a></li>
        <li><a href="#multi-platform-support">Multi-Platform Support</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#workflow-stages">Workflow Stages</a></li>
        <li><a href="#format-based-skill-discovery">Format-Based Skill Discovery</a></li>
        <li><a href="#example-output">Example Output</a></li>
        <li><a href="#validation">Validation</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A structured 6-stage workflow (Stage 0–5) for creating professional project rules (`.cursorrules`) and AI agent guidelines (`AGENTS.md`). This workflow **automatically discovers and integrates** relevant AI skills from any compatible skill source — users never have to manually browse or select skills.

### Why Use This?

- ✅ **Automatic Skill Selection** — AI analyzes your project and finds relevant skills for you
- ✅ **Format-Based Discovery** — Works with CATALOG, FOLDER, SEARCH_ENGINE, README, and WORKFLOW sources
- ✅ **Multi-Platform** — Generates files for 9+ AI tools (Cursor, Claude, Gemini, Copilot, etc.)
- ✅ **Quality Scoring** — Built-in verification with a default 38/50 pass threshold and config-aware overrides
- ✅ **Time-Saving** — Complete in 30-60 minutes
- ✅ **Verified on Mixed `.agent/` Layouts** — Current release is checked against the same combined skill setup documented below
- ✅ **Never Outdated** — Dynamic skill discovery, no hardcoded skill names

> Release details are tracked in [CHANGELOG.md](CHANGELOG.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![PowerShell][PowerShell-badge]][PowerShell-url]
- [![Bash][Bash-badge]][Bash-url]
- [![Python][Python-badge]][Python-url]
- [![Markdown][Markdown-badge]][Markdown-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

| Feature                      | Description                                                                              |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **6-Stage Workflow**         | Structured process: Preferences → Analyze → Discover → .cursorrules → AGENTS.md → Verify |
| **Format-Based Auto-Detect** | Automatically detects skill sources by format (CATALOG/FOLDER/SEARCH_ENGINE/README/WORKFLOW) |
| **Multi-Platform Output**    | Generates correct files for Cursor, Claude, Antigravity, Gemini, Copilot, and more       |
| **17 Keyword Categories**    | Comprehensive mapping from project types to skill search terms                           |
| **Relevance-Ranked Search**  | Scores matches across catalogs, folders, READMEs, and search tools; supports `--limit` for large roots |
| **Quality Scoring**          | Heuristic verification with a default `38/50` pass threshold and config-aware overrides  |
| **Interactive Wizard**       | CLI-based configuration generator (`scripts/wizard.py`) for surgical rule customization  |
| **Interactive Mode**         | Optional preferences system with config file (`.rulesrc.yaml`) support                   |
| **Multi-Language**           | Output generation in 9 languages (en, th, ja, zh, ko, es, fr, de, pt)                    |
| **Preview Mode**             | Review planned output structure before generation begins                                 |
| **Incremental Update**       | Diff-based update mode for existing files — preserves user customizations                |
| **Generation Statistics**    | Dashboard showing skills scanned, lines generated, quality scores                        |
| **Shared Skill Roots**       | Supports project-local `.agent/` plus configured external/shared skill directories       |
| **10 Template Gallery**      | Pre-made examples for React, Express, Next.js, Go, Unity, CLI, LangChain, and more       |
| **Validation Scripts**       | Config-aware PowerShell/Bash validators with heuristic scorecards and threshold output   |

### Supported Project Types

- 🌐 **Web Frontend** — React, Vue, Angular, Svelte, Next.js
- ⚙️ **Backend API** — Node.js, Python, Go, Rust, Express, FastAPI
- 🧩 **Browser Extensions** — Chrome/Firefox Manifest V3
- 📱 **Mobile Apps** — React Native, Flutter, SwiftUI
- 💻 **CLI Tools** — Bash, PowerShell, Commander
- 🤖 **AI/ML Projects** — LLM, RAG, Agents, LangChain
- 🎮 **Game Development** — Unity, Godot, Unreal, Bevy
- 🔒 **Security** — Auth, OAuth, JWT, OWASP
- 📄 **Documentation** — API docs, Architecture docs
- 🧪 **Testing** — Jest, Pytest, Playwright, TDD
- ☁️ **DevOps** — Docker, Kubernetes, CI/CD, Terraform
- 🏗️ **Architecture** — Design patterns, Clean code, SOLID
- 🏢 **Monorepo** — Turborepo, Nx, Lerna, Workspaces
- 🔄 **Microservices** — Event-driven, CQRS, gRPC, Saga
- ☁️ **Serverless** — Lambda, Cloud Functions, Edge
- 🗄️ **Database** — PostgreSQL, MongoDB, Redis, ORM
- 📦 **Package/Library** — npm, PyPI, SDK publishing

### Multi-Platform Support

| AI Tool             | Icon | Output File(s)                                         |
| ------------------- | ---- | ------------------------------------------------------ |
| **Cursor**          | 🟠   | `.cursorrules` or `.cursor/rules/*.mdc`                |
| **Claude Code**     | 🟤   | `CLAUDE.md` + `.claude/skills/`                        |
| **Antigravity IDE** | 🔴   | `.agent/skills/*/SKILL.md` + `.agent/workflows/`       |
| **Gemini CLI**      | 🔵   | `GEMINI.md`                                            |
| **Codex CLI**       | 🟢   | `AGENTS.md`                                            |
| **Kiro IDE/CLI**    | 🟠   | `AGENTS.md` + `.kiro/steering/`                        |
| **GitHub Copilot**  | 🩵   | `.github/copilot-instructions.md` + `.github/prompts/` |
| **OpenCode**        | ⚪   | `AGENTS.md`                                            |
| **AdaL CLI**        | 🌸   | `AGENTS.md`                                            |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- An AI assistant that supports workflows or skills (Cursor, Claude Code, Antigravity, etc.)
- At least one AI skill source installed in your project-local `.agent/` directory or a configured shared skill root
- Your project source code

> **Don't have skills yet?** Clone one of these recommended collections into your `.agent/` directory:
>
> - [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — large `CATALOG.md`-driven index
> - [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — community skill packs
> - [anthropic-skills](https://github.com/anthropics/skills) — official Anthropic skills
> - [techleads-agent-skills](https://github.com/tech-leads-club/agent-skills) — curated registry layout
> - [jeffallan-claude-skills](https://github.com/Jeffallan/claude-skills) — broad full-stack developer set
> - [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — UI/UX design intelligence
> - [othman-planning-with-files](https://github.com/OthmanAdi/planning-with-files) — Manus-style persistent memory planning
> - [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — scientific and research-focused workflows

### Installation

#### Option A: Quick Start Script (recommended)

Local project setup:

**Linux/macOS:**

```sh
curl -sL https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.ps1 | iex
```

Shared skill root setup:

**Linux/macOS:**

```sh
curl -sL https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.sh -o setup.sh
bash setup.sh --skill-source all --skill-root /shared/.agent
```

**Windows (PowerShell):**

```powershell
iwr https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.ps1 -OutFile setup.ps1
.\setup.ps1 -SkillSource all -SkillRoot "C:\Users\narav\Desktop\CE code\Tools\.agent"
```

> The workflow file still installs locally at `.agent/workflows/create-project-rules.md`. `SkillRoot` only changes where optional skill repositories are cloned. The `workflows/` folder is reserved for installed workflow files and is intentionally ignored by `scripts/discover-skills.py` when enumerating external skill sources.

Single scientific-source setup:

**Linux/macOS:**

```sh
bash setup.sh --skill-source scientific --skill-root /shared/.agent
```

**Windows (PowerShell):**

```powershell
.\setup.ps1 -SkillSource scientific -SkillRoot "C:\Users\narav\Desktop\CE code\Tools\.agent"
```

#### Option B: Manual

1. Download the workflow file to your project:
   ```sh
   mkdir -p .agent/workflows
   curl -o .agent/workflows/create-project-rules.md https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/workflows/create-project-rules.md
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### Quick Start

1. **Customize your preferences** (optional):
   ```bash
   python scripts/wizard.py
   ```
2. **Run the workflow** with your AI assistant:
   ```
   /create-project-rules
   ```

Or simply ask:

> "Create professional project rules for this project"

### Manual Execution

1. Open `.agent/workflows/create-project-rules.md`
2. Follow the 6 stages step by step (Stage 0 is optional)
3. Get `.cursorrules` and `AGENTS.md` tailored to your project

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONFIGURATION -->

### Configuration

Use `.rulesrc.yaml` when you want deterministic output instead of interactive prompts.

#### Minimal Example

```yaml
target_platforms:
  - Cursor
  - Codex
  - Antigravity IDE
severity_level: balanced
output_language: en
template_style: progressive
quality_threshold: 38
preview_mode: false
existing_files: ask
```

#### Advanced Example with Shared Skill Roots

```yaml
target_platforms:
  - codex
severity_level: strict
template_style: minimal
quality_threshold: 42
skill_sources:
  - path: "C:/Users/Desktop/.agent"
  - path: .agent
custom_keywords:
  - planning
  - memory
  - workflow
```

#### Field Semantics

| Field                                   | Behavior                                                         |
| --------------------------------------- | ---------------------------------------------------------------- |
| `target_platforms`                      | Overrides AI-tool auto-detection when set                        |
| `severity_level`                        | Changes the density of critical vs advisory rules                |
| `sections.include` / `sections.exclude` | Filters optional sections before generation                      |
| `skill_sources`                         | Discovery roots scanned in order; duplicate source names prefer the first root |
| `custom_keywords`                       | Merged with auto-detected keywords using case-insensitive dedupe |
| `template_style`                        | `progressive`, `flat`, or `minimal` formatting density           |
| `quality_threshold`                     | Default validator threshold unless a CLI threshold overrides it  |
| `preview_mode`                          | Enables the preview step before writing files                    |
| `existing_files`                        | Chooses ask / overwrite / merge / skip behavior                  |

#### Path Rules

- Relative `skill_sources` paths resolve from the project root.
- Absolute paths are allowed.
- Roots are searched in the order listed, so shared roots should appear before `.agent` when they should win.
- Companion docs next to a skill entry (`AGENTS.md`, `CLAUDE.md`, `README.md`) are indexed with that skill instead of treated as separate matches.
- Capability extraction prefers `SKILL.md`, then `AGENTS.md`, then `CLAUDE.md`, and reports adjacent `references/` and `rules/` directories when present.
- If a `format` value is supplied for a root, the workflow trusts it and skips format inference for that root.
- `.agent/skills` remains the default Antigravity CATALOG directory for backward compatibility.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- WORKFLOW STAGES -->

## Workflow Stages

| Stage / Step                 | Description                     | Time Estimate     |
| ---------------------------- | ------------------------------- | ----------------- |
| **Stage 0: Preferences**     | Config file / interactive       | 2-5 min           |
| **Stage 1: Analyze**         | Autonomous scan, tech stack     | 10-15 min         |
| **Stage 2: Skill Discovery** | Auto-detect by FORMAT & 17 cats | 5-10 min          |
| **Stage 3: .cursorrules**    | Progressive disclosure + rules  | 10-20 min         |
| **Preview** (optional)       | Review before writing files     | 2-3 min           |
| **Stage 4: AGENTS.md**       | Multi-platform output           | 10-15 min         |
| **Stage 5: Verify**          | Quality scoring + statistics    | 5-10 min          |
| **Total Time**               |                                 | **30-60 minutes** |

> **Latest compatibility update (2026-03-22):** Discovery now supports repeated `--agent-dir` roots, prefers the first matching source across shared and local `.agent` trees, collapses hybrid skill packages into one entity per directory, and documents the current shared-root smoke-check baseline alongside the repo-local sample.

| Stage                      | Time      | Description                                                             |
| -------------------------- | --------- | ----------------------------------------------------------------------- |
| **0. User Preferences**    | 2-5 min   | Config file or interactive: platforms, severity, language, preview      |
| **1. Project Analysis**    | 10-15 min | Autonomous scan: structure, tech stack, patterns, AI tool detection     |
| **2. Skill Discovery**     | 5-10 min  | Auto-detect sources by format, search all by 17 keyword categories      |
| **3. Create .cursorrules** | 10-20 min | Coding standards with severity levels and progressive disclosure        |
| **Preview** (optional)     | 2-3 min   | Review planned structure before writing files                           |
| **4. Create AGENTS.md**    | 10-15 min | AI guidelines with multi-platform output and dynamic skill section      |
| **5. Verification**        | 5-10 min  | Quality scoring (default 38/50), smell detection, generation statistics |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FORMAT-BASED SKILL DISCOVERY -->

### Format-Based Skill Discovery

The key innovation: instead of hardcoding specific skill repositories, the workflow resolves skill roots in this order and classifies each discovered source by **format**. The current release has been rechecked against the same mixed `.agent/` layout installed by the setup scripts.

1. `skill_sources` from `.rulesrc.yaml`, scanned in the order listed
2. Project-local `.agent/` when no explicit roots are configured
3. A user-provided shared root can be listed before `.agent` to become the preferred baseline

> `.agent/skills` remains the default Antigravity CATALOG path for backward compatibility. Add shared roots through configuration or setup flags instead of renaming the legacy directory.

Examples:

- Local root: `.agent/`
- Shared root: `C:/Users/Desktop/.agent`
- Reserved local output: `.agent/workflows/` (workflow storage, not a skill source)

#### How It Works

```
Resolve configured roots
  │
  ├── Found CATALOG.md?
  │     → Format: CATALOG (keyword search in table)
  │
  ├── Found visible skill directories with SKILL.md / AGENTS.md / CLAUDE.md?
  │     → Format: FOLDER (one skill entity per directory; companion docs stay attached)
  │
  ├── Found search.py or search engine?
  │     → Format: SEARCH_ENGINE (run search with keywords)
  │
  ├── Found README.md with skill listing?
  │     → Format: README (browse categorized list)
  │
  └── Found root CLAUDE.md / AGENTS.md plus hidden integrations such as .claude-plugin?
        → Format: WORKFLOW (read the workflow entrypoint and follow its instructions)
```

#### Supported Formats

| Format            | Detection Signal                               | Search Method                           |
| ----------------- | ---------------------------------------------- | --------------------------------------- |
| **CATALOG**       | Contains `CATALOG.md` with skill table         | Search table rows by keywords           |
| **FOLDER**        | Contains visible skill directories with `SKILL.md`, `AGENTS.md`, or `CLAUDE.md` | Build one skill entity per directory, then read the primary entry plus companion docs |
| **SEARCH_ENGINE** | Contains `search.py` or similar tool           | Run search tool with keywords           |
| **README**        | Contains `README.md` with categorized list     | Browse category headings                |
| **WORKFLOW**      | Root `CLAUDE.md`/`AGENTS.md` plus hidden integrations or `.shared/`, with no visible skill tree | Read workflow, follow its instructions  |

#### Recommended Skill Sources

Clone these into your project-local `.agent/` directory or a shared skill root referenced from `.rulesrc.yaml`:

| Source                     | Format   | Notes                     | Link                                                              |
| -------------------------- | -------- | ------------------------- | ----------------------------------------------------------------- |
| antigravity-awesome-skills | CATALOG  | Large catalog-style index | [GitHub](https://github.com/sickn33/antigravity-awesome-skills)   |
| awesome-claude-skills      | FOLDER   | Community skill packs     | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills)     |
| anthropic-skills           | FOLDER   | Official skill collection | [GitHub](https://github.com/anthropics/skills)                    |
| techleads-agent-skills     | FOLDER   | Curated registry layout   | [GitHub](https://github.com/tech-leads-club/agent-skills)         |
| jeffallan-claude-skills    | FOLDER   | Broad full-stack set      | [GitHub](https://github.com/Jeffallan/claude-skills)              |
| claude-scientific-skills   | FOLDER   | Scientific/research workflows | [GitHub](https://github.com/K-Dense-AI/claude-scientific-skills)  |
| ui-ux-pro-max-skill        | WORKFLOW | Workflow-first package    | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| othman-planning-with-files | FOLDER   | Planning/persistence set  | [GitHub](https://github.com/OthmanAdi/planning-with-files)        |

> **You can use any skill source** — as long as it matches one of the supported formats, the workflow will auto-detect and search it.

#### Compatibility Snapshot (2026-03-22)

| Check | Result | Notes |
| ----- | ------ | ----- |
| Repo-local `.agent/` sample | Supported | The committed sample root still resolves the mixed-format layout used in tests and documentation. |
| Shared-root baseline | Supported | The live shared root at `C:/Users/narav/Desktop/CE code/Tools/.agent` was rechecked as the compatibility baseline for the current implementation. |
| Hybrid skill folders | Supported | Skill directories can now keep `SKILL.md` as the primary entry while surfacing companion `AGENTS.md`, `CLAUDE.md`, and `README.md` files. |
| `claude-scientific-skills` temp install | Supported | An isolated installer run cloned the scientific source into a temp shared root, discovery classified it as `FOLDER`, and capability extraction succeeded against a real skill directory. |
| Root precedence | Ordered | Multi-root discovery prefers the first matching source name, so shared roots should be listed before `.agent` when they should win. |
| Reserved output handling | Passed | Local `.agent/workflows/` is skipped because it stores installed workflows rather than skill libraries. |
| Format scan benchmark | ~280 ms per root | Measured with `python scripts/discover-skills.py --agent-dir <root> --format` on the local Windows sample. |
| Limited keyword search benchmark | ~1.3-1.9 s depending on source mix | Measured with `python scripts/discover-skills.py --agent-dir <root> [--agent-dir <root> ...] --keywords planning workflow python testing --limit 25`. |
| Wide search volume | Still broad on large catalogs | Use `--limit` for large CATALOG sources to keep downstream rule generation focused. |

#### Discovery CLI Examples

```bash
python scripts/discover-skills.py --agent-dir "C:/Users/narav/Desktop/CE code/Tools/.agent" --agent-dir .agent --format
python scripts/discover-skills.py --agent-dir "C:/Users/narav/Desktop/CE code/Tools/.agent" --agent-dir .agent --keywords planning workflow python testing --limit 25
python scripts/extract-capabilities.py .agent/othman-planning-with-files/skills/planning-with-files
```

Use `--limit` whenever broad keywords can hit the large CATALOG source. The discovery script still searches all sources first, but the trimmed output is easier for agents to rank and summarize correctly.

#### Local Smoke Check Flow

```bash
python scripts/discover-skills.py --agent-dir "C:/Users/narav/Desktop/CE code/Tools/.agent" --agent-dir .agent --format
python scripts/discover-skills.py --agent-dir "C:/Users/narav/Desktop/CE code/Tools/.agent" --agent-dir .agent --keywords planning workflow python testing --limit 25
python scripts/extract-capabilities.py .agent/skills/skills/dbos-python
python -m unittest discover -s tests -v
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLE OUTPUT -->

### Example Output

#### .cursorrules (excerpt)

```markdown
# Project Rules: TaskFlow API

> RESTful API for task management with FastAPI.

## Project Identity

- **Type**: Backend API
- **Language**: Python 3.11+
- **Framework**: FastAPI + SQLAlchemy + Alembic

## Critical Rules (🔴)

1. ❌ Never commit `.env` — use `app/core/config.py` with `pydantic-settings`
2. ✅ Always validate input with Pydantic schemas

## Code Smells

| ❌ Smell                 | ✅ Instead Do                          |
| ------------------------ | -------------------------------------- |
| `db = SessionLocal()`    | `Depends(get_db)` injection            |
| `import os; os.getenv()` | `from app.core.config import settings` |
```

#### AGENTS.md (excerpt)

```markdown
# AI Agent Guidelines — TaskFlow API

## 🎯 Available Skills

> [!IMPORTANT]
> Scan configured skill roots before starting work!

### How to Find Skills

| If You Find         | Search Method                |
| ------------------- | ---------------------------- |
| `CATALOG.md`        | Search table by keywords     |
| `SKILL.md` folders  | Browse folder names          |
| Workflow `.md` file | Read and follow instructions |

### Helpful Keywords

- Backend: `api`, `fastapi`, `rest`, `backend`
- Testing: `testing`, `pytest`, `unit`, `tdd`
```

#### 📄 Template Gallery

Pre-made `.cursorrules` examples for common project types are available in [`templates/`](templates/):

| Template           | Directory                     |
| ------------------ | ----------------------------- |
| React + TypeScript | `templates/react-typescript/` |
| Python FastAPI     | `templates/python-fastapi/`   |
| Flutter Mobile     | `templates/flutter-mobile/`   |
| Node.js Express    | `templates/nodejs-express/`   |
| Chrome Extension   | `templates/chrome-extension/` |
| Next.js Full-Stack | `templates/nextjs-fullstack/` |
| Go Microservice    | `templates/go-microservice/`  |
| Unity Game         | `templates/unity-game/`       |
| CLI Tool           | `templates/cli-tool/`         |
| LangChain RAG      | `templates/langchain-rag/`    |

> These are **references only** — the workflow generates custom versions tailored to your specific project.
> Use `templates/rulesrc-template.yaml` to configure workflow behavior for your project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- VALIDATION -->

### Validation

Validation is **heuristic scoring**, not semantic proof. The scripts check structure, placeholders, formatting quality, repo-local path references, and cross-file consistency signals. They do **not** guarantee that generated rules are perfect for every downstream project.

#### PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-output.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate-output.ps1 -Threshold 42
```

#### Bash

```sh
./scripts/validate-output.sh
./scripts/validate-output.sh --threshold 42
```

#### Threshold Resolution

The validators use this order:

1. CLI threshold (`-Threshold` / `--threshold`)
2. `.rulesrc.yaml` → `quality_threshold`
3. Default `38/50`

#### What the Score Covers

Each file is scored across five 0-10 dimensions:

- Completeness
- Accuracy
- Specificity
- Scannability
- Consistency

The scripts print both raw checks and final scorecards so you can see why a file passed or failed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Core workflow with 6 stages (Stage 0–5)
- [x] Time estimates for each stage
- [x] Example outputs
- [x] Quick reference card
- [x] Format-Based Auto-Detect skill discovery
- [x] Multi-platform AI tool support (9 tools)
- [x] Quality scoring verification (≥38/50)
- [x] Content smell detection
- [x] Severity levels (🔴/🟠/🟡)
- [x] 17 keyword categories (expanded from 12)
- [x] WORKFLOW format support
- [x] Quick Start Scripts (`setup.sh` / `setup.ps1`)
- [x] Template Gallery (10 templates)
- [x] Python FastAPI example (replacing Chrome Extension)
- [x] Interactive mode with config file (`.rulesrc.yaml`)
- [x] Multi-language output support (9 languages)
- [x] Preview mode (dry run before writing)
- [x] Incremental update / diff mode
- [x] Generation statistics dashboard
- [x] Validation scripts (`scripts/validate-output.ps1` / `.sh`)
- [x] Setup script improvements (`--non-interactive`, `--uninstall`, `--verbose`)
- [ ] Plugin system for custom skill formats
- [ ] Web UI for workflow configuration

See the [open issues](https://github.com/naravid19/ai-project-rules-generator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/naravid19/ai-project-rules-generator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=naravid19/ai-project-rules-generator" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

naravid19 - [GitHub Profile](https://github.com/naravid19)

Project Link: [https://github.com/naravid19/ai-project-rules-generator](https://github.com/naravid19/ai-project-rules-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Keep a Changelog](https://keepachangelog.com/)
- [Img Shields](https://shields.io)
- [Cursor IDE](https://cursor.sh)
- [Anthropic Claude](https://anthropic.com)
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [anthropic-skills](https://github.com/anthropics/skills)
- [techleads-agent-skills](https://github.com/tech-leads-club/agent-skills)
- [jeffallan-claude-skills](https://github.com/Jeffallan/claude-skills)
- [othman-planning-with-files](https://github.com/OthmanAdi/planning-with-files)
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)
- [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[contributors-url]: https://github.com/naravid19/ai-project-rules-generator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[forks-url]: https://github.com/naravid19/ai-project-rules-generator/network/members
[stars-shield]: https://img.shields.io/github/stars/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[stars-url]: https://github.com/naravid19/ai-project-rules-generator/stargazers
[issues-shield]: https://img.shields.io/github/issues/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[issues-url]: https://github.com/naravid19/ai-project-rules-generator/issues
[license-shield]: https://img.shields.io/github/license/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[license-url]: https://github.com/naravid19/ai-project-rules-generator/blob/master/LICENSE
[PowerShell-badge]: https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white
[PowerShell-url]: https://microsoft.com/PowerShell
[Bash-badge]: https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white
[Bash-url]: https://www.gnu.org/software/bash/
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Markdown-badge]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white
[Markdown-url]: https://www.markdownguide.org/
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/naravidd/

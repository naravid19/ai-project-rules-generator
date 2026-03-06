<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

`<a id="readme-top"></a>`

<!-- PROJECT SHIELDS -->

[Contributors][contributors-url]
[Forks][forks-url]
[Stargazers][stars-url]
[Issues][issues-url]
[MIT License][license-url]
[LinkedIn][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/naravid19/ai-project-rules-generator">
    <img src="https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/assets/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">🤖 AI Project Rules Generator</h3>

<p align="center">
    🚀 Generate .cursorrules and AGENTS.md with automatic, format-based skill discovery from 1000+ curated AI skills
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#workflow-stages">Workflow Stages</a></li>
    <li><a href="#format-based-skill-discovery">Format-Based Skill Discovery</a></li>
    <li><a href="#example-output">Example Output</a></li>
    <li><a href="#validation">Validation</a></li>
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
- ✅ **Format-Based Discovery** — Works with any skill source (CATALOG, FOLDER, SEARCH_ENGINE, README)
- ✅ **Multi-Platform** — Generates files for 9+ AI tools (Cursor, Claude, Gemini, Copilot, etc.)
- ✅ **Quality Scoring** — Built-in verification with a default 38/50 pass threshold and config-aware overrides
- ✅ **Time-Saving** — Complete in 30-60 minutes
- ✅ **Never Outdated** — Dynamic skill discovery, no hardcoded skill names

> Release details are tracked in [CHANGELOG.md](CHANGELOG.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [Markdown][Markdown-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

| Feature                      | Description                                                                              |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **6-Stage Workflow**         | Structured process: Preferences → Analyze → Discover → .cursorrules → AGENTS.md → Verify |
| **Format-Based Auto-Detect** | Automatically detects skill sources by format (CATALOG/FOLDER/SEARCH_ENGINE/README)      |
| **Multi-Platform Output**    | Generates correct files for Cursor, Claude, Antigravity, Gemini, Copilot, and more       |
| **17 Keyword Categories**    | Comprehensive mapping from project types to skill search terms                           |
| **Quality Scoring**          | Heuristic verification with a default `38/50` pass threshold and config-aware overrides  |
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
> - [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — 968+ skills with `CATALOG.md`
> - [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 30+ curated skills
> - [anthropic-skills](https://github.com/anthropics/skills) — 50+ official Anthropic skills
> - [techleads-agent-skills](https://github.com/tech-leads-club/agent-skills) — curated & human-reviewed
> - [jeffallan-claude-skills](https://github.com/Jeffallan/claude-skills) — 66 full-stack developer skills
> - [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — UI/UX design intelligence
> - [othman-planning-with-files](https://github.com/OthmanAdi/planning-with-files) — Manus-style persistent memory planning

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

> The workflow file still installs locally at `.agent/workflows/create-project-rules.md`. `SkillRoot` only changes where optional skill repositories are cloned.

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

Run the workflow with your AI assistant:

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

## Configuration

Use `.rulesrc.yaml` when you want deterministic output instead of interactive prompts.

### Minimal Example

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

### Advanced Example with Shared Skill Roots

```yaml
target_platforms:
  - codex
severity_level: strict
template_style: minimal
quality_threshold: 42
skill_sources:
  - path: .agent/skills
    format: CATALOG
  - path: .agent/awesome-claude-skills
  - path: "C:/Users/Desktop/.agent"
custom_keywords:
  - planning
  - memory
  - workflow
```

### Field Semantics

| Field                                   | Behavior                                                         |
| --------------------------------------- | ---------------------------------------------------------------- |
| `target_platforms`                      | Overrides AI-tool auto-detection when set                        |
| `severity_level`                        | Changes the density of critical vs advisory rules                |
| `sections.include` / `sections.exclude` | Filters optional sections before generation                      |
| `skill_sources`                         | Discovery roots scanned before falling back to local `.agent/`   |
| `custom_keywords`                       | Merged with auto-detected keywords using case-insensitive dedupe |
| `template_style`                        | `progressive`, `flat`, or `minimal` formatting density           |
| `quality_threshold`                     | Default validator threshold unless a CLI threshold overrides it  |
| `preview_mode`                          | Enables the preview step before writing files                    |
| `existing_files`                        | Chooses ask / overwrite / merge / skip behavior                  |

### Path Rules

- Relative `skill_sources` paths resolve from the project root.
- Absolute paths are allowed.
- If a `format` value is supplied for a root, the workflow trusts it and skips format inference for that root.
- `.agent/skills` remains the default Antigravity CATALOG directory for backward compatibility.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- WORKFLOW STAGES -->

## Workflow Stages

```
┌──────────────────────────────────────────────────────────────┐
│         CREATE PROJECT RULES v1.6 - QUICK REF                │
├──────────────────────────────────────────────────────────────┤
│ Stage 0: Preferences      │ Config file / interactive        │
│ Stage 1: Analyze          │ Autonomous scan, tech stack      │
│ Stage 2: Skill Discovery  │ Auto-detect by FORMAT & 17 cats  │
│ Stage 3: .cursorrules     │ Progressive disclosure + rules   │
│ Preview (optional)        │ Review before writing files      │
│ Stage 4: AGENTS.md        │ Multi-platform output            │
│ Stage 5: Verify           │ Quality scoring + statistics     │
├──────────────────────────────────────────────────────────────┤
│ ⏱️ Total Time: 30-60 minutes                                 │
└──────────────────────────────────────────────────────────────┘
```

> **v1.6 update:** Shared skill roots, active `.rulesrc.yaml` semantics, config-aware validator thresholds, PowerShell 5.1 validator repair, and repo-wide documentation/history alignment.

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

## Format-Based Skill Discovery

The key innovation: instead of hardcoding specific skill repositories, the workflow resolves skill roots in this order and classifies each discovered source by **format**:

1. `skill_sources` from `.rulesrc.yaml`
2. Project-local `.agent/`
3. A user-provided shared root when the local scan is empty

> `.agent/skills` remains the default Antigravity CATALOG path for backward compatibility. Add shared roots through configuration or setup flags instead of renaming the legacy directory.

Examples:

- Local root: `.agent/`
- Shared root: `C:/Users/Desktop/.agent`

### How It Works

```
Resolve configured roots
  │
  ├── Found CATALOG.md?
  │     → Format: CATALOG (keyword search in table)
  │
  ├── Found folders with SKILL.md inside?
  │     → Format: FOLDER (browse folder names + read descriptions)
  │
  ├── Found search.py or search engine?
  │     → Format: SEARCH_ENGINE (run search with keywords)
  │
  ├── Found README.md with skill listing?
  │     → Format: README (browse categorized list)
  │
  └── Found .agent/workflows/*.md referencing .shared/ scripts?
        → Format: WORKFLOW (read workflow file, run referenced scripts)
```

### Supported Formats

| Format            | Detection Signal                               | Search Method                           |
| ----------------- | ---------------------------------------------- | --------------------------------------- |
| **CATALOG**       | Contains `CATALOG.md` with skill table         | Search table rows by keywords           |
| **FOLDER**        | Contains subdirectories with `SKILL.md`        | Browse folder names, read matched files |
| **SEARCH_ENGINE** | Contains `search.py` or similar tool           | Run search tool with keywords           |
| **README**        | Contains `README.md` with categorized list     | Browse category headings                |
| **WORKFLOW**      | `.agent/workflows/*.md` referencing `.shared/` | Read workflow, follow its instructions  |

### Recommended Skill Sources

Clone these into your project-local `.agent/` directory or a shared skill root referenced from `.rulesrc.yaml`:

| Source                     | Format   | Count             | Link                                                              |
| -------------------------- | -------- | ----------------- | ----------------------------------------------------------------- |
| antigravity-awesome-skills | CATALOG  | 968+              | [GitHub](https://github.com/sickn33/antigravity-awesome-skills)   |
| awesome-claude-skills      | FOLDER   | 30+               | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills)     |
| anthropic-skills           | FOLDER   | 50+               | [GitHub](https://github.com/anthropics/skills)                    |
| techleads-agent-skills     | FOLDER   | curated registry  | [GitHub](https://github.com/tech-leads-club/agent-skills)         |
| jeffallan-claude-skills    | FOLDER   | 66                | [GitHub](https://github.com/Jeffallan/claude-skills)              |
| ui-ux-pro-max-skill        | WORKFLOW | 1 (comprehensive) | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| othman-planning-with-files | FOLDER   | Manus-style       | [GitHub](https://github.com/OthmanAdi/planning-with-files)        |

> **You can use any skill source** — as long as it matches one of the supported formats, the workflow will auto-detect and search it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLE OUTPUT -->

## Example Output

### .cursorrules (excerpt)

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

### AGENTS.md (excerpt)

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

### 📄 Template Gallery

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

## Validation

Validation is **heuristic scoring**, not semantic proof. The scripts check structure, placeholders, formatting quality, repo-local path references, and cross-file consistency signals. They do **not** guarantee that generated rules are perfect for every downstream project.

### PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-output.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate-output.ps1 -Threshold 42
```

### Bash

```sh
./scripts/validate-output.sh
./scripts/validate-output.sh --threshold 42
```

### Threshold Resolution

The validators use this order:

1. CLI threshold (`-Threshold` / `--threshold`)
2. `.rulesrc.yaml` → `quality_threshold`
3. Default `38/50`

### What the Score Covers

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
[Markdown-badge]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white
[Markdown-url]: https://www.markdownguide.org/
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/naravidd/

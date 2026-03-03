<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h1>🤖 AI Project Rules Generator</h1>

  <p align="center">
    🚀 Generate .cursorrules and AGENTS.md with automatic, format-based skill discovery from 1000+ curated AI skills
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#example-output">View Example</a>
    &middot;
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
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
    <li><a href="#workflow-stages">Workflow Stages</a></li>
    <li><a href="#format-based-skill-discovery">Format-Based Skill Discovery</a></li>
    <li><a href="#example-output">Example Output</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A structured 5-stage workflow for creating professional project rules (`.cursorrules`) and AI agent guidelines (`AGENTS.md`). This workflow **automatically discovers and integrates** relevant AI skills from any compatible skill source — users never have to manually browse or select skills.

### Why Use This?

- ✅ **Automatic Skill Selection** — AI analyzes your project and finds relevant skills for you
- ✅ **Format-Based Discovery** — Works with any skill source (CATALOG, FOLDER, SEARCH_ENGINE, README)
- ✅ **Multi-Platform** — Generates files for 9+ AI tools (Cursor, Claude, Gemini, Copilot, etc.)
- ✅ **Quality Scoring** — Built-in verification with ≥38/50 pass criteria
- ✅ **Time-Saving** — Complete in 30-60 minutes
- ✅ **Never Outdated** — Dynamic skill discovery, no hardcoded skill names

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Markdown][Markdown-badge]][Markdown-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

| Feature                      | Description                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| **5-Stage Workflow**         | Structured process: Analyze → Discover → .cursorrules → AGENTS.md → Verify          |
| **Format-Based Auto-Detect** | Automatically detects skill sources by format (CATALOG/FOLDER/SEARCH_ENGINE/README) |
| **Multi-Platform Output**    | Generates correct files for Cursor, Claude, Antigravity, Gemini, Copilot, and more  |
| **12 Keyword Categories**    | Comprehensive mapping from project types to skill search terms                      |
| **Quality Scoring**          | Verification with scoring system (≥38/50 to pass) and content smell detection       |
| **Progressive Disclosure**   | Generated files follow overview → details structure                                 |
| **Severity Levels**          | Critical rules (🔴) distinguished from important (🟠) and notes (🟡)                |

### Supported Project Types

- 🌐 **Web Frontend** — React, Vue, Angular, Svelte, Next.js
- ⚙️ **Backend API** — Node.js, Python, Go, Rust, Express, FastAPI
- 🧩 **Browser Extensions** — Chrome/Firefox Manifest V3
- 📱 **Mobile Apps** — React Native, Flutter, SwiftUI
- 💻 **CLI Tools** — Bash, PowerShell, Commander
- 🤖 **AI/ML Projects** — LLM, RAG, Agents, LangChain
- 🎮 **Game Development** — Unity, Godot, Unreal, Bevy
- 🔒 **Security** — Auth, OAuth, JWT, OWASP
- 📝 **Documentation** — API docs, Architecture docs
- 🧪 **Testing** — Jest, Pytest, Playwright, TDD
- ☁️ **DevOps** — Docker, Kubernetes, CI/CD, Terraform
- 🏗️ **Architecture** — Design patterns, Clean code, SOLID

### Multi-Platform Support

| AI Tool             | Icon | Output File(s)                                         |
| ------------------- | ---- | ------------------------------------------------------ |
| **Cursor**          | 🟠   | `.cursorrules` or `.cursor/rules/*.mdc`                |
| **Claude Code**     | 🟣   | `CLAUDE.md` + `.claude/skills/`                        |
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
- At least one AI skill source installed in your `.agent/` directory
- Your project source code

> **Don't have skills yet?** Clone one of these recommended collections into your `.agent/` directory:
>
> - [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — 968+ skills with `CATALOG.md`
> - [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 30+ curated skills
> - [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — UI/UX design intelligence

### Installation

1. Download the workflow file to your project:
   ```sh
   curl -o .agent/workflows/create-project-rules.md https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/workflows/create-project-rules.md
   ```
   _(Ensure you have an `.agent/workflows` directory first)_

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
2. Follow the 5 stages step by step
3. Get `.cursorrules` and `AGENTS.md` tailored to your project

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- WORKFLOW STAGES -->

## Workflow Stages

```
┌──────────────────────────────────────────────────────────────┐
│              CREATE PROJECT RULES v2.0 - QUICK REF           │
├──────────────────────────────────────────────────────────────┤
│ Stage 1: Analyze          │ Autonomous scan, tech stack,     │
│                           │ patterns, detect AI tools        │
│ Stage 2: Skill Discovery  │ Auto-detect sources by FORMAT,   │
│                           │ search all by keywords           │
│ Stage 3: .cursorrules     │ Progressive disclosure,          │
│                           │ severity levels, code examples   │
│ Stage 4: AGENTS.md        │ Multi-platform output,           │
│                           │ dynamic skill section            │
│ Stage 5: Verify           │ Quality scoring (≥38/50),        │
│                           │ smell detection, reader test     │
├──────────────────────────────────────────────────────────────┤
│ ⏱️  Total Time: 30-60 minutes                                │
└──────────────────────────────────────────────────────────────┘
```

| Stage                      | Time      | Description                                                         |
| -------------------------- | --------- | ------------------------------------------------------------------- |
| **1. Project Analysis**    | 10-15 min | Autonomous scan: structure, tech stack, patterns, AI tool detection |
| **2. Skill Discovery**     | 5-10 min  | Auto-detect sources by format, search all by keywords               |
| **3. Create .cursorrules** | 10-20 min | Coding standards with severity levels and progressive disclosure    |
| **4. Create AGENTS.md**    | 10-15 min | AI guidelines with multi-platform output and dynamic skill section  |
| **5. Verification**        | 5-10 min  | Quality scoring (≥38/50), content smell detection, reader test      |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FORMAT-BASED SKILL DISCOVERY -->

## Format-Based Skill Discovery

The key innovation: instead of hardcoding specific skill repositories, the workflow **auto-detects** available skill sources by scanning `.agent/` and classifying each by **format**.

### How It Works

```
Scan .agent/ directory
  │
  ├── Found CATALOG.md?
  │     → Format: CATALOG (search table by keywords)
  │
  ├── Found folders with SKILL.md?
  │     → Format: FOLDER (browse folder names + read descriptions)
  │
  ├── Found search.py?
  │     → Format: SEARCH_ENGINE (run search with keywords)
  │
  └── Found README.md with skill list?
        → Format: README (browse categories)
```

### Supported Formats

| Format            | Detection Signal                           | Search Method                           |
| ----------------- | ------------------------------------------ | --------------------------------------- |
| **CATALOG**       | Contains `CATALOG.md` with skill table     | Search table rows by keywords           |
| **FOLDER**        | Contains subdirectories with `SKILL.md`    | Browse folder names, read matched files |
| **SEARCH_ENGINE** | Contains `search.py` or similar tool       | Run search tool with keywords           |
| **README**        | Contains `README.md` with categorized list | Browse category headings                |

### Recommended Skill Sources

Clone these into your `.agent/` directory:

| Source                     | Format        | Count             | Link                                                              |
| -------------------------- | ------------- | ----------------- | ----------------------------------------------------------------- |
| antigravity-awesome-skills | CATALOG       | 968+              | [GitHub](https://github.com/sickn33/antigravity-awesome-skills)   |
| awesome-claude-skills      | README        | 30+               | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills)     |
| ui-ux-pro-max-skill        | SEARCH_ENGINE | 1 (comprehensive) | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |

> **You can use any skill source** — as long as it matches one of the supported formats, the workflow will auto-detect and search it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLE OUTPUT -->

## Example Output

### .cursorrules (excerpt)

```markdown
# Project Rules: My Chrome Extension

> Chrome Extension (Manifest V3) that exports NotebookLM conversations to PDF.

## Project Identity

- **Type**: Browser Extension
- **Language**: JavaScript (ES2020+)
- **Platform**: Chrome Extension (Manifest V3)

## Critical Rules (🔴)

1. ❌ Never use `localStorage` — use `chrome.storage` instead
2. ✅ Always check `chrome.runtime.lastError` after API calls

## Code Smells to Avoid

| ❌ Smell                   | ✅ Instead Do                |
| -------------------------- | ---------------------------- |
| `localStorage.setItem()`   | `chrome.storage.local.set()` |
| Persistent background page | Event-driven service worker  |
```

### AGENTS.md (excerpt)

```markdown
# AI Agent Guidelines — NotebookLM PDF Exporter

## 🎯 Available Skills

> [!IMPORTANT]
> Scan `.agent/` for skill sources before starting work!

### How to Find Skills

| If You Find        | Search Method            |
| ------------------ | ------------------------ |
| `CATALOG.md`       | Search table by keywords |
| `SKILL.md` folders | Browse folder names      |
| `search.py`        | Run with `--keywords`    |

### Helpful Keywords

- Extension: `browser`, `extension`, `chrome`, `manifest`
- Testing: `testing`, `jest`, `unit`
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Core workflow with 5 stages
- [x] Time estimates for each stage
- [x] Example outputs
- [x] Quick reference card
- [x] Format-Based Auto-Detect skill discovery
- [x] Multi-platform AI tool support (9 tools)
- [x] Quality scoring verification (≥38/50)
- [x] Content smell detection
- [x] Severity levels (🔴/🟠/🟡)
- [x] 12 keyword categories
- [ ] More project type examples (Python API, React app, etc.)
- [ ] Interactive mode (ask user preferences during generation)
- [ ] Skill source auto-installer
- [ ] Multi-language README support

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
- [Cursor IDE](https://cursor.sh)
- [Anthropic Claude](https://anthropic.com)
- [Antigravity](https://deepmind.google/technologies/gemini/)
- [Img Shields](https://shields.io)

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

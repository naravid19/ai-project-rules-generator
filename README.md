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
    <img src="assets/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">🤖 AI Project Rules Generator</h3>

  <p align="center">
    🚀 Orchestrate professional .cursorrules and AGENTS.md with deterministic JIT skill discovery.
    <br />
    <a href="https://github.com/naravid19/ai-project-rules-generator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/naravid19/ai-project-rules-generator">View Demo</a>
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
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage-guide">Usage Guide</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#available-scripts">Available Scripts</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Project Overview

AI Project Rules Generator is a production-grade AI Agent Skill designed to solve **Context Bloat** and **Agent Drift** in AI-assisted development. By utilizing **Deterministic JIT (Just-In-Time) Retrieval**, it automatically discovers and integrates relevant AI skills from your local environment without saturating the LLM's context window. 

This repository provides a unified `SKILL.md` workflow compatible with all major Agent IDEs (Cursor, Claude Code, Antigravity, Gemini CLI, Copilot) to seamlessly generate `.cursorrules` and `AGENTS.md` context rules.

### Key Features

- **Multi-platform Support**: Generates configurations compatible with 9+ platforms (Cursor, Claude Code, etc.).
- **Deterministic JIT Discovery**: Loads only top 5 relevant skills via Semantic Fallback instead of dumping everything into the context window.
- **Dual-Mode Execution**: Operates via native LLM reasoning (Zero-Install Mode B) or via Python heuristics (Enhanced Mode A).
- **Subagent-Driven**: Built to fully leverage the Superpowers framework and Andrej Karpathy's methodology.

---

## Tech Stack

- **Skill Definition**: Markdown (YAML Frontmatter + Prompt Engineering)
- **Installation Scripts**: Bash & PowerShell
- **Enhanced Indexing**: Python 3.10+ (Optional)
- **Target Environments**: Cursor, Claude Code, Antigravity IDE, Gemini CLI, OpenCode

---

## Prerequisites

Before utilizing this skill, ensure you have:
- An AI assistant capable of reading workspace files (e.g., Cursor IDE, Claude Code CLI, Gemini CLI).
- A local `.agent/` or `.cursor/skills/` directory containing skill repositories.
- `curl` and `bash` (Linux/macOS) or `PowerShell` (Windows) for the installation scripts.

---

## Getting Started

Choose the installation method that best fits your security and workflow requirements.

### Option 1: Quick Install (Recommended)

The fastest way to get started using our automated setup scripts. This installs the skill directly into your current directory.

**Linux/macOS:**
```bash
curl -sL https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.ps1 | iex
```

### Option 2: Secure / Manual Install

For security-conscious enterprise environments where code must be inspected before execution:

**Linux/macOS:**
```bash
curl -sO https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.sh
# Inspect setup.sh here
chmod +x setup.sh
./setup.sh
```

### Option 3: Direct Skill Integration

If you prefer a zero-touch approach without executing local shell scripts:

```bash
mkdir -p .agent/generating-project-rules
curl -sL -o .agent/generating-project-rules/SKILL.md https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/SKILL.md
```

---

## Usage Guide

Simply ask your AI assistant to generate the rules, and it will automatically invoke the skill. We recommend using natural language prompting aligned with the Superpowers methodology.

### Basic Invocation
```text
"Please generate project rules for this repository using the Superpowers methodology."
```

### Explicit Invocation
```text
"@SKILL.md please generate my project rules."
```

### Advanced Workflow

For the most advanced experience, ensure you have the [Superpowers Skills](https://github.com/obra/superpowers) installed locally.

1.  **Request Generation**: Ask the AI to draft rules based on the project state.
2.  **JIT Retrieval**: The AI will scan the `.agent` directory, select up to 5 relevant skills using Semantic Match, and load their contents.
3.  **Audit & Output**: The AI will draft `.cursorrules` and `AGENTS.md` and log its reasoning in `.agent/logs/`.

---

## Architecture

This project is structured as a standard Agent Skill, primarily driven by a core `SKILL.md` instruction file.

### Directory Structure

```text
ai-project-rules-generator/
├── SKILL.md            # The core autonomous agent workflow instructions
├── scripts/            # Enhanced execution scripts (Mode A)
│   ├── indexer.py      # Builds skill_catalog.json
│   ├── wizard.py       # Interacts with rules generation
│   └── lib/            # Shared Python libraries
├── setup.sh            # Unix installation script
├── setup.ps1           # Windows installation script
├── README.md           # This file
└── CHANGELOG.md        # Version history
```

### Execution Modes

The Flexible Agentic Engine (v1.9.4) supports **Dual-Mode Execution**:

1.  **Mode A (Enhanced)**: Utilizes the `scripts/` directory containing Python/PowerShell/Bash scripts for high-performance, token-efficient indexing. It requires local Python installation to parse dependencies and tokens via `ThreadPoolExecutor`.
2.  **Mode B (Autonomous)**: Zero-install mode where the AI interprets the `SKILL.md` natively without relying on external dependencies. The LLM performs the directory scanning and semantic matching natively.

### Agentic Alignment Principles

This tool enforces high-fidelity standards derived from world-class AI engineering methodologies:
*   **[Andrej Karpathy's Methodology](https://github.com/forrestchang/andrej-karpathy-skills)**: Prioritizes "Simplicity First", "Surgical Changes", and "Think Before Coding" logic.
*   **[Superpowers Framework](https://github.com/obra/superpowers)**: Implements "Verification Before Completion" and "Subagent-Driven Development".

---

## Available Scripts

| Script | Environment | Description |
|---|---|---|
| `setup.sh` | Linux/macOS Bash | Installs the skill, sets up `.agent` directories, and performs legacy cleanup. |
| `setup.ps1` | Windows PowerShell | Installs the skill and prepares the `.agent` environment on Windows. |
| `scripts/indexer.py`| Python 3 | Generates the lightweight `skill_catalog.json` used by Mode A. |

---

## Troubleshooting

### Installation Script Fails
**Error:** `curl: command not found` or `irm: command not found`
**Solution:** Ensure you are using a modern terminal (Git Bash, WSL, or native macOS Terminal for Linux/Mac; PowerShell 5.1+ for Windows). If `curl` is missing, use Option 3 (Direct Integration) to download the file manually.

### AI Hallucinates Incorrect Skills
**Error:** The generated `.cursorrules` contains non-existent libraries or invalid skill names.
**Solution:** Ensure the AI is invoking the skill correctly. Explicitly mention the skill file in your prompt: `"Using @SKILL.md, regenerate the project rules. Strictly adhere to the JIT Retrieval constraint."` 

### Old Workflows Persist
**Error:** The AI keeps referencing `.agent/workflows/create-project-rules.md`.
**Solution:** You are on an older version. Rerun the v1.9.4 installation script (`setup.sh` or `setup.ps1`), which contains automated cleanup logic to remove the deprecated `workflows/` directory.

---

## Roadmap

- [x] Multi-platform Support (9+ Tools)
- [x] Deep Context Savings (Pointer System)
- [x] Parallel Indexing (ThreadPoolExecutor)
- [x] Systematic Debugging (Stack Trace Audit)
- [x] Exact-word boundary tagging (\bregex\b)
- [x] Refactor to root-level `SKILL.md` (v1.9.4)
- [ ] Multi-agent Simulation Environment
- [ ] Web-based Configuration UI

See the [open issues](https://github.com/naravid19/ai-project-rules-generator/issues) for a full list of proposed features.

---

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

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
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/naravidd/

<div align="center">
  <img src="assets/images/logo.png" alt="Logo" width="80" height="80">
  <h1 align="center">AI Project Rules Generator</h1>
  <p align="center">
    Orchestrate professional <code>.cursorrules</code> and <code>AGENTS.md</code> with deterministic JIT skill discovery.
  </p>
  <p align="center">
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=bug">Report Bug</a> &middot;
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

---

AI Project Rules Generator is a production-grade AI Agent Skill designed to solve **Context Bloat** and **Agent Drift** in AI-assisted development. By utilizing **Deterministic JIT (Just-In-Time) Retrieval**, it automatically discovers and integrates relevant AI skills from your local environment without saturating the LLM's context window.

## Quickstart

Give your project professional AI Rules: [Claude Code](#claude-code) | [Gemini CLI](#gemini-cli) | [Codex CLI](#codex-cli) | [Local Installation](#local-installation)

## How it works

It starts the moment you fire up your coding agent and ask it to generate project rules. Rather than dumping an entire folder of skills into your context window, the generator steps back and indexes available skills across your local, global, and remote environments.

Once it understands the intent of your project (e.g., frontend, backend, UI design), it uses **Semantic Fallback** and fuzzy matching to dynamically select the **top 5 most relevant skills**. 

It then compiles these into a highly structured `.cursorrules` or `AGENTS.md` file, providing your AI assistant with the exact constraints, design tokens, and architectural patterns it needs to work autonomously—without overwhelming its token limits.

## Installation

Installation differs by harness. If you use more than one, install the generator separately for each one.

### Claude Code

The generator can be installed directly via Claude's plugin manager:

```bash
/plugin install https://github.com/naravid19/ai-project-rules-generator
```

### Gemini CLI

Install the generator globally via Gemini's native extension manager:

```bash
gemini extensions install https://github.com/naravid19/ai-project-rules-generator
```

### Codex CLI

Install the generator via the Codex extensions manager:

```bash
codex extensions install https://github.com/naravid19/ai-project-rules-generator
```

### Local Installation

If you prefer to install the generator manually or via shell scripts directly into your workspace:

**Linux / macOS:**
```bash
curl -sL https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/setup.ps1 | iex
```

## Usage

Simply ask your AI assistant to generate the rules, and it will automatically invoke the skill.

**Basic Invocation:**
> "Please generate project rules for this repository using the Superpowers methodology."

**Explicit Invocation:**
> "@SKILL.md please generate my project rules."

### 🗺️ Multi-Source Skill Mapping

You can configure, index, and query skills from multiple scopes: **local** (project-level), **global** (machine-level), and **remote** (git repositories cloned on demand).

*New in v1.9.5:* The engine features robust **fault tolerance**. Remote sources securely fallback to local offline `.cache` copies if a network timeout occurs, ensuring your agent never breaks mid-workflow.

#### 1. Configuration in `.rulesrc.yaml`
```yaml
skill_sources:
  - path: ".agent"
    confirmed: true
    type: local
    source_name: project-local

  - path: "https://github.com/obra/superpowers.git"
    type: remote
    source_name: community-skills
```

#### 2. Run the Multi-Source Indexer
```bash
python scripts/indexer.py --unified --skill-map
```
This produces a unified JSON catalog for the JIT engine and a human-readable `skill_map.md`.

## Architecture & Data Flow

### Directory Structure

```text
ai-project-rules-generator/
├── SKILL.md            # The core autonomous agent workflow instructions
├── scripts/            # Enhanced execution scripts (Mode A)
│   ├── indexer.py      # Builds skill_catalog.json and skill_map.md
│   ├── wizard.py       # Interacts with rules generation
│   ├── rules_config.py # Configuration parsing logic
│   └── remote_source.py# Git-based remote source caching
├── tests/              # Comprehensive Pytest suite
└── setup.sh / ps1      # Installation scripts
```

### Request Lifecycle

1. **User Intent**: The user asks the AI to generate rules.
2. **JIT Routing**: The AI parses `SKILL.md` and reads `.rulesrc.yaml`.
3. **Multi-Source Indexing**: `scripts/indexer.py` aggregates and deduplicates skills into a lightweight JSON catalog.
4. **Semantic Matching**: The AI cross-references the user's intent against the catalog using synonym matching and exact-word boundaries.
5. **Rules Generation**: High-fidelity `.cursorrules` and `AGENTS.md` are drafted based on the matched top 5 skills.
6. **Audit Check**: Execution logs and decision reasoning are securely written to `.agent/logs/`.

## Testing

This project adheres strictly to **Test-Driven Development (TDD)** and maintains robust test coverage across fault tolerance and core features.

Ensure you have `pytest` installed, then run the test suite:

```bash
# Run all tests natively
py -m pytest tests/ -v

# Run with coverage
py -m pytest tests/ --cov=scripts --cov-report=term-missing
```

## Troubleshooting

- **Agent Hallucinates Incorrect Skills**: Ensure the AI is invoking the skill correctly. Explicitly mention the skill file in your prompt: `"Using @SKILL.md, regenerate the project rules. Strictly adhere to the JIT Retrieval constraint."`
- **Installation Script Fails**: Ensure you are using a modern terminal (Git Bash, WSL, or native macOS Terminal). If `curl` is missing, download the files manually.
- **Cache Discovery Bug**: Ensure you are running `v1.9.5` or later. Earlier versions had an issue where remote skills cloned into `.cache` were skipped by the indexer.

## License

Distributed under the MIT License. See `LICENSE` for more information.

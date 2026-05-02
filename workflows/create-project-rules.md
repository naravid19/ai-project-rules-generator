---
description: Create professional project rules (.cursorrules and AGENTS.md) with automatic, format-based skill discovery from any skill source
---

# Create Professional Project Rules

Generate tailored `.cursorrules` and `AGENTS.md` files for any software project. This workflow automatically discovers and integrates relevant AI skills - users never manually browse or select skills.

**Estimated Total Time**: 30-60 minutes (depending on project complexity)

## Prerequisites

Before starting, ensure you have:

- Access to the project's source code
- Understanding of the project's purpose
- At least one AI skill source installed in project-local `.agent/` or a configured shared root

> [!TIP]
> **Don't have skills yet?** Clone one of these recommended collections into your project-local `.agent/` directory or a shared root referenced from `.rulesrc.yaml`:
>
> - [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) - large `CATALOG.md`-driven index
> - [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - community skill packs
> - [anthropic-skills](https://github.com/anthropics/skills) - official Anthropic skills
> - [techleads-agent-skills](https://github.com/tech-leads-club/agent-skills) - curated registry layout
> - [jeffallan-claude-skills](https://github.com/Jeffallan/claude-skills) - broad full-stack developer set
> - [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - UI/UX design intelligence
- [othman-planning-with-files](https://github.com/OthmanAdi/planning-with-files) - planning and persistence workflows
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) - scientific and research-focused workflows

---

## Execution Strategy: Dual-Mode Prompting

> [!IMPORTANT]
> You MUST evaluate your workspace environment before proceeding. Use the appropriate mode based on the presence of the `scripts/` directory.

### Mode A: Enhanced (Script Mode)
**Trigger**: `scripts/` directory exists in project root.
**Action**: Utilize Python utilities (`indexer.py`, `wizard.py`, etc.) for fast, token-efficient discovery and validation. Run these scripts directly via terminal.

### Mode B: Autonomous (Zero-Install Mode)
**Trigger**: `scripts/` directory is missing.
**Action**: **DO NOT** ask the user to download scripts or install Python. Fallback to "Pure Agent Mode" using native IDE capabilities (file reading, directory listing) to emulate script logic.

---


## Stage 0: User Preferences (Interactive Mode)

**Time: 2-5 minutes** (skippable with config file)

> [!TIP]
> This stage is **optional**. If a `.rulesrc.yaml` config file exists in the project root, read preferences from it and skip interactive prompts. If no config file and no TTY (CI/CD), use defaults.

### 0.1 Check for Configuration File

Look for `.rulesrc.yaml` in the project root:

```text
Project Root
|-- .rulesrc.yaml   <- If found, read preferences from here
\-- (no config)     <- Proceed to interactive prompts or use defaults
```

If found, parse the config and apply settings. See `templates/rulesrc-template.yaml` for all available options.

### 0.2 Apply Config Semantics

Treat the config file as the source of truth when fields are present:

| Field | Behavior |
| ----- | -------- |
| `target_platforms` | Explicit target list. Overrides AI-tool auto-detection when set. |
| `severity_level` | Controls how many blocking vs advisory rules are written. |
| `output_language` | Controls translated prose. Keep code examples in the original programming language. |
| `sections.include` / `sections.exclude` | Filter optional sections before writing files. Required sections remain present. |
| `skill_sources` | Discovery roots to scan first. Exactly one root must be confirmed before generation. |
| `custom_keywords` | Merge with auto-detected keywords using case-insensitive dedupe. |
| `template_style` | Controls formatting density: `progressive`, `flat`, or `minimal`. |
| `quality_threshold` | Stage 5 pass threshold. Use this instead of the default `38` when present. |
| `confidence_threshold` | Minimum score before the workflow must halt and ask the user to clarify intent. |
| `skill_match_limit` | Hard cap for technical/domain-specific matched skills carried forward. |
| `agentic_match_limit` | Hard cap for functional/agentic matched skills (planning, reasoning) carried forward. |
| `preview_mode` | If `true`, show the preview step before writing files. |
| `existing_files` | Controls whether to ask, overwrite, merge, or skip existing outputs. |

#### `skill_sources` Path Rules

- Relative paths resolve from the project root.
- Absolute paths are allowed.
- Exactly one entry must be marked `confirmed: true` before generation begins.
- If `format` is omitted, auto-detect the format for that root.
- If `format` is provided, trust it and skip format inference for that root.

Example:

```yaml
skill_sources:
  - path: .agent/skills
    format: CATALOG
    confirmed: true
  - path: .agent/awesome-claude-skills
    confirmed: false
  - path: "C:/shared/team-skills/.agent"
    confirmed: false
custom_keywords:
  - planning
  - memory
template_style: minimal
quality_threshold: 42
confidence_threshold: 80
skill_match_limit: 5
agentic_match_limit: 3
```

### 0.3 Interactive Preference Questions

If no config file exists, ask the user these core questions directly:

**Mode A (Enhanced)**: If `scripts/wizard.py` exists, run: `python scripts/wizard.py`
**Mode B (Autonomous)**: Ask the user manually via chat:

| Question | Options | Default |
| -------- | ------- | ------- |
| **Target AI platforms?** | cursor, claude, antigravity, gemini, codex, kiro, copilot, opencode, adal | Auto-detect |
| **Severity level?** | strict / balanced / relaxed | balanced |
| **Output language?** | en, th, ja, zh, ko, es, fr, de, pt | en |
| **Include optional sections?** | security, accessibility, i18n, performance, git-workflow, api-design | All included |
| **Template style?** | progressive / flat / minimal | progressive |
| **Preview before writing?** | yes / no | no |
| **Existing files action?** | ask / overwrite / merge / skip | ask |

> Ask only relevant questions. For example, don't ask about security sections for a documentation-only project.

### 0.4 Multi-Language Output

If a non-English language is selected:

- Translate section headers (keep English technical term in parentheses)
- Translate rule descriptions and guidelines
- Keep code examples in the original programming language
- Keep emoji/icons unchanged
- See `i18n/README.md` for detailed translation patterns

### 0.5 Store Preferences

Carry preferences through all subsequent stages:

```
Preferences:
  target_platforms: [cursor, codex]
  severity_level: balanced
  output_language: en
  sections: [all]
  skill_sources: [.agent/, C:/shared/team-skills/.agent]
  custom_keywords: [planning, memory]
  template_style: progressive
  quality_threshold: 38
  confidence_threshold: 80
  skill_match_limit: 5
  preview_mode: false
  existing_files: ask
```

---

## Stage 1: Project Analysis

**Time: 10-15 minutes**

> [!IMPORTANT]
> This stage should be **autonomous**. Scan the project yourself - don't ask the user for information you can discover by reading files.

### 1.1 Autonomous Codebase Discovery

Scan the project automatically:

| Step | Action | How |
| ---- | ------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1 | **Read config files** | Look for `package.json`, `manifest.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile` |
| 2 | **Identify Intent** | **Recommended**: Read `README.md` or any custom instruction/spec file to understand project goals. |
| 3 | **Identify entry points** | Find `index.js`, `main.py`, `App.tsx`, `main.go`, `lib.rs`, etc. |
| 4 | **Map architecture** | Scan folder structure, component organization, layers |
| 5 | **List dependencies** | Extract from config files (key libraries and frameworks) |

> [!TIP]
> Prioritize dedicated requirement files (like `spec.md` or `architecture.md`) over generic README descriptions for high-fidelity architectural constraints.

### 1.2 Document Tech Stack

Create a profile:

```
Primary Language(s): ___
Frameworks:          ___
Build Tools:         ___
Testing:             ___
Styling:             ___
Database:            ___
Deployment:          ___
```

### 1.2b Extract Design Tokens from Source Files (MANDATORY)

> [!CAUTION]
> NEVER infer colors, fonts, spacing, or breakpoints from README descriptions or design documents.
> ALWAYS extract them from the actual config files listed below.

For projects with styling:

| Config File | What to Extract |
|-------------|----------------|
| `tailwind.config.ts/js` | `theme.extend.colors.*`, `theme.extend.fontFamily.*`, `theme.extend.borderRadius.*` |
| `postcss.config.js` | PostCSS plugins, custom properties |
| `src/styles/globals.css` | CSS custom properties (`--variable-name: value`) |
| `theme.ts` / `tokens.ts` | Design token objects |
| `*.module.css` patterns | CSS module naming conventions |

**Procedure:**
1. Open the actual config file (e.g., `tailwind.config.ts`)
2. Copy the exact color hex values from the config object
3. Copy the exact font family names
4. If a README describes colors that DIFFER from the config, use the CONFIG values
5. Note the discrepancy in the output as a "Known Divergence"

### 1.3 Deep Directory & Dependency Scan

> [!IMPORTANT]
> Do NOT stop at the first few directories. Scan EVERY directory and extract ALL dependencies.

**Directory completeness checklist:**

| Framework | Scan These Directories | What to Document |
|-----------|----------------------|------------------|
| Next.js App Router | ALL dirs under `src/app/` | Route name, layout type, server/client |
| Next.js Pages Router | ALL dirs under `src/pages/` | Route name, data fetching method |
| React (Vite/CRA) | ALL dirs under `src/` | Component type, purpose |
| Python/Django | ALL apps, ALL management commands | App purpose, models |

**State management scan:**
- List ALL files in `src/store/`, `src/state/`, `src/stores/`, or equivalent
- Document each store/slice name and what it manages

**Dependency cross-reference (MANDATORY):**
1. Open `package.json` (or equivalent manifest)
2. Extract EVERY dependency from both `dependencies` and `devDependencies`
3. Flag any dependency that implies a pattern:
   - `@tanstack/react-query` → data fetching pattern
   - `zustand` / `redux` / `jotai` → state management
   - `firebase` vs `firebase-admin` → client vs server SDK distinction
   - `framer-motion` → animation pattern
   - `next-intl` / `i18next` → i18n support

### 1.3b Verify Constraints Before Writing

Before writing ANY constraint (like "pure functions only" or "no side effects"):
1. List the actual files in the directory
2. Read at least the imports of each file
3. If any file has side effects (e.g., `initializeApp`, `createClient`, HTTP calls), do NOT label the directory as "pure"

### 1.4 Detect Target AI Tools

Determine the target AI tools using this fallback order:

1. **Self-Awareness (Primary):** Identify what platform you (the AI executing this workflow) are currently running in using your system prompts or context.
   - If you are Gemini / Gemini CLI → Include `GEMINI.md`
   - If you are Claude Code → Include `CLAUDE.md`
   - If you are Antigravity IDE → Include `.agent/skills/*/SKILL.md`
   - If you are Cursor → Include `.cursorrules`
2. **Explicit Config:** Read `target_platforms` from `.rulesrc.yaml` if it exists.
3. **Existing Files:** Scan the project root for existing configuration files:

| If You Find | User Likely Uses |
| --------------------------------------- | ------------------------------------------ |
| `.cursorrules` or `.cursor/` | Cursor |
| `CLAUDE.md` or `.claude/` | Claude Code |
| `.agent/skills/` or `.agent/workflows/` | Antigravity IDE |
| `GEMINI.md` | Gemini CLI |
| `AGENTS.md` | Codex / Kiro / OpenCode / AdaL |
| `.kiro/` | Kiro IDE/CLI |
| `.github/copilot-instructions.md` | GitHub Copilot |

> **Default**: If self-awareness fails and no files are found, generate `.cursorrules` + `AGENTS.md` (most universal).

### 1.5 Runtime Bootstrapping (Enterprise Features)

**Mode A (Enhanced)**: If operating in Enterprise mode (detected by `scripts/indexer.py` and `scripts/memory_manager.py`), bootstrap the environment:
1. **Incremental Indexing:** Run `python scripts/indexer.py --incremental`
2. **Catalog Validation:** Run `python scripts/indexer.py --validate`
3. **State Memory Refresh:** Run `python scripts/memory_manager.py`

**Mode B (Autonomous)**: Skip bootstrapping and proceed directly to manual project analysis using native directory listing.

### 1.6 Confidence Gate (Human-in-the-Loop)

Before skill discovery or file generation, score the detected project signals (Manifests + Entrypoints + Frameworks + Patterns).

**Mode A (Enhanced)**: Run `python scripts/wizard.py` to auto-calculate score.
**Mode B (Autonomous)**: Compute a deterministic score (0-100).
- +20 for each primary manifest (`package.json`, `pyproject.toml`, etc.)
- +20 for clear entrypoint (`main.py`, `index.js`)
- +30 for frameworks detected in imports
- +30 for clear architecture pattern

**HALT LOGIC (Critical)**:
- If `confidence_score >= 80`, continue automatically.
- If `confidence_score < 80`, you MUST **STOP** and ask the user to clarify the project type / intent with multiple-choice options.
- Do NOT guess. Do NOT continue with broad default assumptions.

---

## Stage 2: Skill Discovery (Format-Based Auto-Detect)

**Time: 5-10 minutes**

> [!IMPORTANT]
> **Never hardcode skill names!** Skills are constantly updated. Always use keyword-based search.
> **Never hardcode skill source names!** Detect what's available by scanning directories.

### 2.1 Auto-Detect Available Skill Sources

Resolve discovery roots in this order before classifying formats:

1. `skill_sources` from `.rulesrc.yaml`, scanned in the order listed
2. Project-local `.agent/` when no explicit roots are configured
3. If neither yields results, tell the user to clone sources locally or point the workflow at a shared root

#### Automated Discovery & Extraction

**Mode A (Enhanced)**: Run:
- `python scripts/discover-skills.py --agent-dir <root>`
- `python scripts/indexer.py --project-root .`
- `python scripts/extract-capabilities.py --skill-dir <matched_path>`

**Mode B (Autonomous)**: Scan roots manually using these **Fallback Constraints (Critical)**:

> [!CAUTION]
> **Anti-Overload Rule**: You MUST strictly:
> 1. List directory contents first (`ls -R` or `list_directory`).
> 2. Filter based on filenames/intents (e.g., matching `react` or `api`).
> 3. ONLY read the full content of the top 5 relevant files.
> 4. NEVER try to read entire skill directories at once.

---

### 2.4 Two-Stage JIT Retrieval & Deep Context Savings

To prevent context window bloat and adhere to the **Superpowers Flat Namespace** principle, follow this two-stage process:

**Stage 1: Intent Matching (Max 5 Paths)**
1. Scan the confirmed skill root and build a mental index of available skills by reading **ONLY** the frontmatter (title/description) and directory names.
2. Match the User Intent and Tech Stack against this index.
3. Select a strict **MAXIMUM of 5** relevant skill paths.
4. Output these 5 paths to the user before proceeding to Stage 2.

**Stage 2: Deep Context Savings (Pointer System)**
1. Do **NOT** inject the full markdown content (`SKILL.md`) into your prompts or the final output files prematurely.
2. Extract **ONLY** the specific triggering conditions ("Use when...") and the file paths for the 5 selected skills.
3. Heavy references (>100 lines) must remain in their original files. You will provide pointers (paths) to these files so that future AIs can use the `read_file` tool to load them Just-In-Time.

---

### 2.5 Hybrid MCP + Local Skill Routing

1. **Native MCP Discovery**: Scan local IDE config files (e.g., `.cursor/mcp.json`, `~/.config/Claude/claude_desktop_config.json`) to detect installed MCP servers.
2. **Registry Mapping**: Load `templates/mcp_registry.yaml` to map intents to standard tool names.
3. **Route Orchestration**: Route local markdown skills from the catalog AND native MCP servers from the registry when they match the intent.
4. **Instruction**: Use the template in Stage 4.2 to explicitly instruct the agent on how to combine conceptual rules with functional tools.

### 2.6 Read and Extract Best Practices

For each matched skill:

1. Resolve the skill directory or instruction file you actually matched
2. Resolve the primary entrypoint with this order: `SKILL.md` -> `AGENTS.md` -> `CLAUDE.md`
3. Study the "When to Use" section - confirm it applies
4. Read companion docs (`AGENTS.md`, `CLAUDE.md`, `README.md`) only when they add relevant context
5. Note adjacent `references/` or `rules/` folders when they exist
6. Extract applicable best practices, patterns, and rules
7. Skip skills that don't match the project context

> [!CAUTION]
> **Don't include every skill you find!** Only include skills that are directly relevant to the project's tech stack and patterns. Quality over quantity.

---

## Stage 3: Create .cursorrules

**Time: 10-20 minutes**

Create `.cursorrules` at the project root.

### 3.0 Apply `template_style`

Use the Stage 0 preference before writing sections:

| `template_style` | Behavior |
| ---------------- | -------- |
| `progressive` | Default. Overview -> details with fuller explanations and examples. |
| `flat` | Same content scope, but use shallower heading depth and fewer long examples. |
| `minimal` | Keep only essential sections and tighter examples. Target `80-150` lines. |

> Required sections still remain present in every style. `template_style` changes formatting density and verbosity, not core coverage.

Structure using **progressive disclosure** unless `template_style` changes the presentation:

Add traceability metadata near the top of the generated file:

```markdown
<!-- Skill_Source_Path: {confirmed_skill_source_path} -->
<!-- Confirmed_Skill_Source: true -->
```

### 3.1 Pre-Write Reasoning (Think Before Coding)

Before writing any content for `.cursorrules`, perform a brief **Surgical Analysis** inspired by Karpathy's guidelines:
1. **Assumptions**: List 2-3 key assumptions about the project (e.g., "Assumed Tailwind v4 due to package.json dependencies"). Don't hide confusion. Surface tradeoffs.
2. **Tradeoffs**: Briefly explain why you chose specific rules over others (e.g., "Prioritized Strict Typing over flexibility for API stability").
3. **Simplicity First**: Are you adding unnecessary abstractions or features? Write the minimum rules needed.
4. **Success Criteria**: Define 1-2 ways the AI can verify these rules are working (e.g., "Agent must push back if a new route is added without a Zod schema").

### 3.2 Required Sections

```markdown
# Project Rules: {PROJECT_NAME}

> One-line project description.

## Project Identity
- **Type**: {project type}
- **Purpose**: {what it does}
- **Tech Stack**: {languages, frameworks}
- **License**: {license}

---

## Project Structure

### Key Files

| Path | Purpose | When to Modify |
| -------- | --------- | -------------- |
| `{file}` | {purpose} | Use when {trigger condition} |

---

## Coding Standards

### Naming Conventions

| Element | Convention | Example |
| --------- | ---------- | ----------- |
| Variables | {style} | `{example}` |
| Functions | {style} | `{example}` |
| Classes | {style} | `{example}` |
| Files | {style} | `{example}` |

### Error Handling

{Describe the project's error handling pattern with code example}

### Async Patterns

{Describe how async operations should be handled}

---

## Critical Rules (Severity: Critical)

> [!CAUTION]
> **No Exceptions**: Violating the letter of these rules is violating the spirit of these rules.

{Non-negotiable rules with code examples}

### Rule 1: {rule name}

**Use when**: {Specific triggering conditions and symptoms. Do NOT summarize the workflow here.}

{description with BAD / GOOD examples}

---

## Important Guidelines (Severity: Important)

{Important but slightly flexible guidelines}

---

## Code Smells

| Smell | Instead Do |
| ------------- | -------------- |
| {bad pattern} | {good pattern} |

---

## Testing & Verification Guidelines

**Verification Before Completion**:
1. IDENTIFY: What command proves this code works?
2. RUN: Execute the FULL command (e.g. `npm test`, `pytest`)
3. READ: Full output, check exit code
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Claim the task is complete.

{Other Testing requirements and patterns}
```

### 3.2 Optional Sections (Add as Needed)

| Section | When to Include |
| ------------------------------- | ----------------------------------------------------- |
| **Security Considerations** | Apps handling sensitive data, auth, payments |
| **Performance Guidelines** | High-traffic, real-time, or resource-constrained apps |
| **Accessibility (a11y)** | Web or mobile applications |
| **Internationalization (i18n)** | Multi-language support |
| **Git Workflow** | Team projects with branching strategy |
| **Debugging Strategies** | Complex debugging scenarios |
| **API Design** | Projects that expose APIs |

### 3.3 Integrate Skills (Deep Context Savings)

Instead of dumping massive code examples into `.cursorrules`, use the **Pointer System**:

1. **Extract Core Rules**: Extract only the highest-value, fundamental patterns from the matched skills.
2. **Adapt Context**: Apply them strictly to the project's current context.
3. **Use Pointers**: Do NOT include heavy (>10 lines) code examples or abstract principles. Instead, create a direct reference (e.g., `[Read detailed guide at: .agent/skills/skill-name/SKILL.md]`).
4. **Don't credit the skill** - write the rules natively as if they are the project's own guidelines.

---

## Preview Mode (Optional)

**Time: 2-3 minutes**

If `preview_mode: true` in preferences (Stage 0), display a preview before generating files:

### Preview Output Format


```text
GENERATION PREVIEW

Target Files:
- .cursorrules (estimated: ~200 lines)
- AGENTS.md (estimated: ~150 lines)

Sections for .cursorrules:
- Project Identity
- Project Structure
- Coding Standards (naming, file org, error handling)
- Critical Rules (Critical x 4)
- Important Guidelines (Important x 6)
- Code Smells (8 patterns)
- Testing Guidelines

Skills to Apply: 5 matched from 3 sources
Language: English
Severity: Balanced

Warning: .cursorrules already exists - Action: ask
```

Ask the user:

> **Proceed with generation?** (yes / no / modify)

If "modify" - return to Stage 0 to adjust preferences.

---

## Stage 4: Create AGENTS.md

**Time: 10-15 minutes**

Create `AGENTS.md` (or the appropriate file for the target AI tool) at the project root.

### 4.1 Pre-Write Reasoning (Think Before Coding)

Before writing `AGENTS.md`, define the **Goal-Driven Execution** plan:
1. **Orchestration Logic**: How should the agent prioritize local skills vs MCP tools?
2. **Success Criteria**: "Agent can successfully discover and read the top 5 relevant skills without user intervention."

### 4.2 High-Fidelity Agentic Template (ref: 9-Pillar Architecture)

```markdown
# AI Agent Guidelines — {PROJECT_NAME}

> {one_sentence_description}

## 🎯 Quick Context

- **Tech Stack**: {stack_summary}
- **Primary Intent**: {clarified_intent}

### Directory Mapping

| Path | Primary Purpose | Agent Constraint |
|------|-----------------|------------------|
| `{dir}` | {purpose} | {constraint} |

---

## 🛠️ Multi-Platform Output

| Tool | Rule File | Skills/Workflows |
|------|-----------|------------------|
| Cursor | `.cursorrules` | `.cursor/rules/*.mdc` |
| Claude Code | `CLAUDE.md` | `.claude/skills/` |
| Antigravity | `.agent/skills/*/SKILL.md` | `.agent/workflows/` |
| Gemini CLI | `GEMINI.md` | - |
| Codex/OpenCode | `AGENTS.md` | - |

---

## 🧠 Agent Capabilities

> [!IMPORTANT]
> **System Memory**: Silently read `.agent/memory/project_state.md` and treat its contents as an active System Prompt override for this session.

### [Native MCP Servers]
*Instruction: Use these tools to execute actions (e.g., read files, query DBs, run terminal commands).*

| Server | Purpose | Intent Match |
|--------|---------|--------------|
| `{server}` | {what it provides} | `{keyword}` |

### [Subagent Orchestration & Parallelism]
*Instruction: For complex, multi-file, or parallel tasks, DO NOT execute everything in the main session. Use the specified subagent workflows to manage cognitive load and context.*

| Task Complexity | Strategy | Required MCP/Subagent Tool |
|-----------------|----------|----------------------------|
| **Multi-step Execution** | Dispatch fresh subagent per task | `invoke_agent` or `superpowers:subagent-driven-development` |
| **Independent Tasks** | Run in parallel without blocking | `superpowers:dispatching-parallel-agents` |
| **Local Data Analysis** | Spawn a persistent interactive REPL | `mcp_desktop-commander_start_process` (e.g., `python3 -i`) |
| **UI/React Debugging** | Use visual inspection tools | `chrome-devtools-mcp` |

### [Local Agent Skills]
*Instruction: Strictly follow the conceptual guidelines, coding standards, and architectural rules defined in these paths BEFORE executing any MCP tool.*

| Keyword | Capability | Source Path |
|---------|------------|-------------|
| `{keyword}` | {extracted summary} | `{path}/SKILL.md` |

---

## 🚫 Non-Negotiable Constraints

1. **Rule 1**: NEVER hardcode skill names in instructions. Use keywords.
2. **Path Integrity**: Only discover skills from the confirmed root: `{confirmed_path}`.
3. **Traceability**: All completion runs must update the project-local audit log.
4. **Validation**: All changes must pass heuristic scoring (Stage 5) before completion.
```

---

## Stage 6: Audit Logging & Memory Management (MANDATORY)

**Time: 1 minute**

> [!CAUTION]
> You must strictly complete this stage to fulfill the 9-Pillar Architecture requirements.

### 6.1 Project-Local Audit Logging

**Mode A (Enhanced)**: The `@audit_logger` decorator automatically writes logs to `./.agent/logs/`.
**Mode B (Autonomous)**: You MUST manually write a JSON audit log file at `.agent/logs/log_<utc-timestamp>_<platform>_<session-id>.json`. Use `.agent/logs/template.json` as your schema reference.

**Required Fields**:
- `session_id`: 8-character unique identifier.
- `timestamp_utc`: Current time in ISO format.
- `confidence_score`: Your deterministic score (0-100).
- `reasoning`: **CRITICAL** - Explain "Why" you made specific stack/skill decisions.
- `matched_skill_paths`: The 5 paths loaded via JIT.
- `verification_status`: Your final quality score.

### 6.2 State Memory Refresh

**Mode A (Enhanced)**: Run `python scripts/memory_manager.py`.
**Mode B (Autonomous)**: Overwrite `.agent/memory/project_state.md` with a concise summary:
1. **Current Phase**: (e.g., Rule Generation Completed)
2. **Detected Profile**: (Tech stack and intent)
3. **Recent Skills**: (List the 5 skills integrated)
4. **Last Files**: (List generated files and their quality scores)

> **Pro Tip**: This file serves as the System Prompt injected into future agent sessions. Always keep it clean and scannable.
---

## Incremental Update Mode

**Time: 10-15 minutes**

When `.cursorrules` or `AGENTS.md` already exist and the user wants to **update** them (e.g., new skill added, tech stack changed):

### When to Use Update Mode

| Trigger | Action |
| ------------------------- | ------------------------------------------------------------- |
| New dependency added | Re-run Stage 2 -> merge new skill rules |
| Tech stack changed | Re-run Stage 1 -> update project identity + re-discover skills |
| New skill source cloned | Re-run Stage 2 only |
| Manual rules need refresh | Re-run Stages 3-5 |
| Version upgrade | Re-run all stages |

### Update Workflow

1. **Analyze existing files** - read current `.cursorrules` and `AGENTS.md`
2. **Detect changes** - compare current project state vs what's documented
3. **Show diff preview** - display what will be added/modified/removed
4. **Confirm with user** - ask before applying changes
5. **Apply changes** - merge new content while preserving user customizations
6. **Re-verify** - run Stage 5 on updated files

### Merge Rules

| Section | Merge Strategy |
| -------------------------- | ----------------------------- |
| Project Identity | Replace with latest |
| Coding Standards | Merge (keep user additions) |
| Critical Rules | Add new, keep existing |
| Skills section | Replace with latest discovery |
| Custom rules added by user | Always preserve |

> [!CAUTION]
> **Never delete rules the user manually added.** Only update auto-generated sections.

---

## Output Files Summary

After completing this workflow, you should have:

| File | Lines | Audience | Content |
| -------------- | ------- | --------------- | -------------------------------------------------------------- |
| `.cursorrules` | 150-400 (`80-150` for `minimal`) | AI writing code | Coding standards, architecture, patterns, anti-patterns |
| `AGENTS.md` | 100-250 (`60-120` for `minimal`) | AI agent | Project context, skill discovery, constraints, common patterns |

> Additional files may be generated based on detected AI tools (see Stage 4.1).

---

## Quick Reference Card

```text
CREATE PROJECT RULES v1.9.3 - QUICK REF

Stage 0: Preferences     | Config file / interactive, language, severity, platforms
Stage 1: Analyze         | Autonomous scan, tech stack, patterns, detect AI tools
Stage 2: Skill Discovery | Auto-detect sources by format, search all by 17 categories
Stage 3: .cursorrules    | Progressive disclosure, severity levels, code examples
Preview (optional)       | Show structure before writing
Stage 4: AGENTS.md       | Multi-platform output, dynamic skill section
Stage 5: Verify          | Quality scoring, thresholds, smell detection, statistics

Rules:
- Skills: search by keywords, never hardcode names
- Sources: detect by format, never hardcode repo names
- Scan configured roots for: CATALOG.md / SKILL.md / search.py
- Use severity: Critical / Important / Note
- Config: .rulesrc.yaml for automation / CI/CD
- Update: incremental mode for existing files
```

---

## Example: Python FastAPI Project

### Condensed .cursorrules Output

````markdown
# Project Rules: TaskFlow API

> RESTful API for task management with user authentication and real-time notifications.

## Project Identity
- **Type**: Backend API
- **Language**: Python 3.11+
- **Framework**: FastAPI + SQLAlchemy + Alembic
- **Database**: PostgreSQL

## Project Structure

### Key Files

| Path | Purpose |
| -------------------- | -------------------------------- |
| `app/main.py` | FastAPI app entry point, routers |
| `app/models/` | SQLAlchemy ORM models |
| `app/routers/` | API route handlers |
| `app/schemas/` | Pydantic request/response models |
| `app/core/config.py` | Settings and environment config |
| `alembic/` | Database migrations |

## Coding Standards

- Use async database sessions and dependency injection for all request-scoped data access.
- Keep routers, schemas, models, and configuration in separate directories with single-purpose files.

## Critical Rules (Critical)

1. Never commit `.env` - use `app/core/config.py` with `pydantic-settings`
2. Never use raw SQL - always use SQLAlchemy ORM or Core
3. Always validate input with Pydantic schemas

## Error Handling

```python
from fastapi import HTTPException, status

async def get_task(task_id: int, db: AsyncSession):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task
```

## Code Smells

| Smell | Instead Do |
| --------------------- | ------------------------------------ |
| `db = SessionLocal()` | `db: AsyncSession = Depends(get_db)` |
````

### Condensed AGENTS.md Output

```markdown
# AI Agent Guidelines - TaskFlow API

> RESTful API for task management built with FastAPI.

## Quick Context

- **Type**: Backend API
- **Stack**: FastAPI + SQLAlchemy + PostgreSQL
- **Primary goals**: async APIs, safe database access, typed request/response models

## Available Skills

> [!IMPORTANT]
> Always scan configured skill roots for skill sources before starting work!

### How to Find Skills

| If You Find | Search Method |
| ------------------- | ---------------------------- |
| `CATALOG.md` | Search table by keywords |
| `SKILL.md` folders | Scan the "Use when..." description |
| `search.py` | Run with `--keywords` |
| Workflow `.md` file | Read and follow instructions |

> [!CAUTION]
> **Superpowers Rule**: Description = When to Use, NOT What the Skill Does. Do not summarize workflows in the `SKILL.md` description.

### Helpful Keywords

- Backend: `api`, `fastapi`, `rest`, `backend`
- Database: `database`, `sql`, `prisma`, `orm`
- Auth: `security`, `auth`, `jwt`, `oauth`
- Testing: `testing`, `pytest`, `unit`, `tdd`

## Common Patterns

- Prefer backend, database, auth, and testing keywords first, then narrow to framework-specific skills.

## Multi-Platform Output Mapping

| Tool | Primary Output |
| ------ | -------------- |
| Codex | `AGENTS.md` |
| Cursor | `.cursorrules` |

## Non-Negotiable Constraints

### Critical

1. All endpoints must use async/await
2. Database sessions must use dependency injection
3. Secrets must come from environment variables, never hardcoded

### Anti-Patterns

| Anti-Pattern | Instead Do |
| -------------------------------- | ----------------------------------------- |
| `db = SessionLocal()` | `db: AsyncSession = Depends(get_db)` |
| `import os; os.getenv("SECRET")` | `from app.core.config import settings` |
| `@app.get("/tasks")` | `@router.get("/tasks")` in dedicated file |
```

---

## Version History

| Version | Date | Changes |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0 | 2026-02-07 | Initial workflow structure |
| 1.1 | 2026-02-07 | Added skill integration and verification steps |
| 1.2 | 2026-02-07 | Added time estimates, examples, quick reference card |
| 1.3 | 2026-03-03 | **Major update**: Format-based auto-detect, Python FastAPI example, quality scoring, severity levels, progressive disclosure, content smell detection, expanded keyword tables (12 categories) |
| 1.4 | 2026-03-03 | WORKFLOW format support, Quick Start Scripts (`setup.sh`/`setup.ps1`), Template Gallery (React, Python, Flutter) |
| 1.5 | 2026-03-05 | **Major update**: Stage 0 (Interactive Mode + Config File), Multi-language support, Preview Mode, Incremental Update Mode, Generation Statistics, 7 new templates, Validation Scripts, Extended Keywords (17 categories), Setup Script improvements |
| 1.6 | 2026-03-06 | Shared skill roots, active `.rulesrc.yaml` semantics, config-aware validation thresholds, PowerShell validator repair, and repo-wide workflow alignment |
| 1.7 | 2026-03-13 | Mixed `.agent/` compatibility recheck, reserved workflow-folder filtering, relevance-ranked discovery results, regression coverage for helper scripts, and documentation/performance alignment |
| 1.8 | 2026-03-22 | Hybrid and multi-root skill source modernization, ordered shared-root precedence, companion-doc extraction, scientific source installer support, and end-to-end scientific-source verification |
| 1.9.0 | 2026-04-25 | Native MCP server auto-discovery, project-local audit logging and memory persistence, confidence gating heuristics, and strict source root enforcement |
| 1.9.1 | 2026-04-26 | Workflow AI Self-Sufficiency (no scripts required for Quick Start), Accuracy hardening: §1.2b source-of-truth design token parsing, §1.3 deep directory & dependency scan, §1.3b constraint verification, §4.5 pre-write accuracy gate, and `extract_design_tokens()` runtime stub |
| 1.9.2 | 2026-04-26 | **9-Pillar Architecture Completion**: Finalized Pillar 4 (Integrated Audit Logging) and Pillar 5 (System Memory Injection). Upgraded `extract_design_tokens()` to a functional regex parser. Implemented Dual-Mode Strategy (Enhanced Scripted vs Autonomous Fallback) to support zero-install users. Added Anti-Overload Rule for manual skill discovery. |
| 1.9.3 | 2026-05-02 | **Architecture Refinement & Superpowers Integration**: Completed detailed development pass for 9-Pillar alignment. Implemented Pointer-based JIT retrieval, Subagent Orchestration rules, Systematic Debugging, and Parallel Processing indexer. |
igh-Fidelity Pass**: Completed detailed development pass for 9-Pillar alignment. Added explicit scoring for Confidence Gate, Tiered Double Search for JIT retrieval, and strictly isolated MCP/Local sections in templates. |

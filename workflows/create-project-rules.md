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
  - path: "C:/Users/narav/Desktop/CE code/Tools/.agent"
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
  skill_sources: [.agent/, C:/Users/narav/Desktop/CE code/Tools/.agent]
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

Before skill discovery or file generation, score the detected project signals.

- If `confidence_score >= confidence_threshold`, continue automatically.
- If `confidence_score < confidence_threshold`, stop and ask the user to clarify the project type / intent with multiple-choice options.
- Do not guess. Do not continue with broad default assumptions.

Use only repo facts for the score: manifests, entrypoints, dependencies, architecture folders, and test signals.

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

> Keep `.agent/skills` as the default Antigravity CATALOG target for backward compatibility. Add more roots through `skill_sources` or setup flags instead of renaming that directory.

#### Automated Discovery & Extraction

**Mode A (Enhanced)**: Run the following commands for automated results:
- `python scripts/discover-skills.py --agent-dir <root>`
- `python scripts/indexer.py --project-root .`
- `python scripts/extract-capabilities.py --skill-dir <matched_path>`

**Mode B (Autonomous)**: Scan your project's skill roots manually using these **Fallback Constraints (Critical)**:

> [!CAUTION]
> **Anti-Overload Rule**: When discovering skills manually, you MUST strictly:
> 1. List directory contents first (`ls -R` or `list_directory`).
> 2. Filter based on filenames/intents (e.g., matching `react` or `api`).
> 3. ONLY read the full content of the top 3-5 relevant files.
> 4. NEVER try to read entire skill directories at once.

1. **Source Discovery**: List directories and read entry files (`CATALOG.md`, `SKILL.md`) to classify the source by format.
2. **Catalog Indexing**: Build a mental index of available skills and their summaries from the confirmed root.
3. **Skill Search**: Filter your mental index using keywords.
4. **Capability Extraction**: Read the full content of the matched `SKILL.md` files.
5. **MCP Auto-Discovery**: Check `templates/mcp_registry.yaml` and local IDE MCP config files.

> Skip local `.agent/workflows/` when classifying skill sources. It stores installed workflow files, not reusable skill libraries.

For each resolved root, scan recursively and classify each source by **format**:


```text
Resolve roots -> scan each root recursively in precedence order

|-- Found CATALOG.md?
|   -> Format: CATALOG (keyword search in table)
|
|-- Found visible skill directories with SKILL.md / AGENTS.md / CLAUDE.md?
|   -> Format: FOLDER (one skill entity per directory; companion docs stay attached)
|
|-- Found search.py or search engine?
|   -> Format: SEARCH_ENGINE (run search with keywords)
|
|-- Found README.md with skill listing?
|   -> Format: README (browse categorized list)
|
\-- Found root CLAUDE.md / AGENTS.md plus hidden integrations such as .claude-plugin?
    -> Format: WORKFLOW (read the workflow entrypoint, then follow companion docs or scripts)
```

#### Format Detection Rules

| Format | How to Detect | How to Search |
| ----------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **CATALOG** | Directory (or subdirs) contains `CATALOG.md` with a skills table | Search CATALOG.md by keyword in Tags/Description columns |
| **FOLDER** | Directory contains visible subfolders (at any depth) with `SKILL.md`, `AGENTS.md`, or `CLAUDE.md` | Build one skill entity per directory, prefer `SKILL.md`, and treat adjacent `AGENTS.md` / `CLAUDE.md` / `README.md` as companion docs |
| **SEARCH_ENGINE** | Directory contains `search.py` or similar executable search tool | Run `search.py --keywords <terms>` |
| **README** | Directory contains `README.md` with categorized skill links/descriptions | Browse README sections for relevant categories |
| **WORKFLOW** | Folder has root `CLAUDE.md` / `AGENTS.md`, hidden integration directories (`.claude-plugin`, `.cursor-plugin`, etc.), and no visible skill tree | Read the workflow entrypoint, then follow its instructions to run referenced scripts |

> If a root matches multiple signals, prefer the path that yields real skill entities without duplicating companion docs. `FOLDER` wins over `WORKFLOW` when a visible skill tree exists.

#### Example Auto-Detection

```text
.agent/ or C:/Users/narav/Desktop/CE code/Tools/.agent
|-- skills/                            <- Has CATALOG.md -> Format: CATALOG
|   |-- CATALOG.md                     (sickn33/antigravity-awesome-skills)
|   \-- skills/
|       |-- clean-code/SKILL.md
|       \-- ...
|-- awesome-claude-skills/            <- Has SKILL.md folders -> Format: FOLDER
|   |-- README.md                     (ComposioHQ/awesome-claude-skills)
|   |-- skill-creator/SKILL.md
|   \-- ...
|-- anthropic-skills/                 <- README + nested skills/ -> Prefer FOLDER after recursive scan
|   |-- README.md                     (anthropics/skills)
|   \-- skills/                      <- Inner SKILL.md folders -> Format: FOLDER
|       |-- pptx/SKILL.md
|       |-- skill-creator/SKILL.md
|       \-- ...
|-- techleads-agent-skills/           <- Has SKILL.md folders -> Format: FOLDER
|   |-- react-expert/SKILL.md         (tech-leads-club/agent-skills)
|   \-- ...
|-- jeffallan-claude-skills/          <- README + nested skills/ -> Prefer FOLDER after recursive scan
|   |-- README.md                     (Jeffallan/claude-skills)
|   \-- skills/                      <- Inner SKILL.md folders -> Format: FOLDER
|       |-- nestjs-expert/SKILL.md
|       \-- ...
|-- claude-scientific-skills/         <- scientific-skills/ + plugin metadata -> Prefer FOLDER when visible skills exist
|   |-- README.md                     (K-Dense-AI/claude-scientific-skills)
|   |-- .claude-plugin/
|   \-- scientific-skills/           <- Visible skill tree -> Format: FOLDER
|       |-- literature-review/SKILL.md
|       \-- ...
|-- andrej-karpathy-skills/           <- Has SKILL.md folders -> Format: FOLDER
|   |-- README.md                     (multica-ai/andrej-karpathy-skills)
|   \-- ...
|-- ui-ux-pro-max-skill/              <- Uses deeply nested CLAUDE.md and .shared/ -> Format: WORKFLOW
|   |-- CLAUDE.md                     (nextlevelbuilder/ui-ux-pro-max-skill)
|   |-- .claude/skills/ui-ux-pro-max/SKILL.md
|   \-- .shared/
\-- my-custom-skills/               <- Has SKILL.md folders -> Format: FOLDER
    |-- my-react-rules/SKILL.md
    \-- my-python-rules/SKILL.md
```

### 2.2 Extract Keywords from Project

Map the detected tech stack (from Stage 1) to search keywords, then merge any `custom_keywords` from Stage 0 with case-insensitive dedupe:

**By Project Type:**

| Type | Keywords |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| Web Frontend | `react`, `vue`, `angular`, `svelte`, `frontend`, `ui`, `ux`, `design`, `css`, `tailwind`, `nextjs` |
| Backend API | `api`, `backend`, `rest`, `graphql`, `database`, `sql`, `prisma`, `express`, `fastapi` |
| Browser Extension | `browser`, `extension`, `chrome`, `manifest`, `content-script` |
| Mobile App | `react-native`, `flutter`, `mobile`, `ios`, `android`, `swiftui`, `jetpack` |
| CLI Tool | `cli`, `terminal`, `bash`, `powershell`, `commander` |
| AI/ML | `ai`, `ml`, `llm`, `agent`, `rag`, `prompt`, `langchain`, `embedding` |
| Game Dev | `game`, `unity`, `godot`, `unreal`, `bevy`, `ecs` |

**By Quality Domain:**

| Domain | Keywords |
| ---------------- | ----------------------------------------------------------------------- |
| Testing | `testing`, `jest`, `pytest`, `unit`, `integration`, `tdd`, `playwright` |
| Security | `security`, `auth`, `oauth`, `jwt`, `encryption`, `owasp` |
| Documentation | `docs`, `documentation`, `readme`, `api-docs`, `architecture` |
| Architecture | `architecture`, `design-patterns`, `refactoring`, `clean-code`, `solid` |
| DevOps | `docker`, `ci`, `cd`, `deployment`, `kubernetes`, `terraform` |
| Performance | `performance`, `optimization`, `caching`, `bundle`, `lazy-loading` |

**By Architecture Pattern:**

| Pattern | Keywords |
| ------------------ | ------------------------------------------------------------------------ |
| Monorepo | `monorepo`, `turborepo`, `nx`, `lerna`, `workspace`, `pnpm-workspace` |
| Microservices | `microservice`, `event-driven`, `saga`, `cqrs`, `message-queue`, `grpc` |
| Serverless | `serverless`, `lambda`, `cloud-functions`, `edge`, `vercel`, `netlify` |
| Database | `postgresql`, `mongodb`, `redis`, `migration`, `seeding`, `orm`, `nosql` |
| Package/Library | `npm`, `pypi`, `crate`, `gem`, `package`, `library`, `sdk`, `publish` |

**By Agentic Capability:**

| Capability | Keywords |
| -------------------- | ---------------------------------------------------------------------- |
| Planning & Memory | `planning`, `memory`, `manus`, `workflow`, `reasoning`, `step-by-step` |
| Tool Use & MCP | `tool`, `mcp`, `functions`, `api-calling`, `integration` |

### 2.3 Search All Detected Sources

For each detected source, use the appropriate search method:

| Source Format | Search Action |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **CATALOG** | Open `CATALOG.md`, search for rows matching extracted keywords in Tags/Description columns |
| **FOLDER** | Build one skill entity per visible directory, rank by folder/path keywords first, then read the primary entry plus companion docs when needed |
| **SEARCH_ENGINE** | Run the search tool with extracted keywords as arguments |
| **README** | Open `README.md`, scan category headings and descriptions for relevant entries |
| **WORKFLOW** | Read workflow / `CLAUDE.md` file, follow instructions to run scripts from `.shared/` |

> [!IMPORTANT]
> Every AI execution step must prepend this constraint with the actual confirmed path:
>
> `You must ONLY retrieve and reference skills from the confirmed directory: [CONFIRMED_PATH]`

### 2.4 Tiered Double Search (JIT Retrieval)

Instead of reading every `SKILL.md` file completely:
1. Build a lightweight mental catalog by reading just the frontmatter or descriptions of available skills.
2. Perform a **Double Search**:
   - **First Pass (Foundational)**: Select up to `agentic_match_limit` functional/agentic skills (e.g., Planning, Memory, Debugging, Security).
   - **Second Pass (Technical)**: Select up to `skill_match_limit` technical/domain-specific skills (e.g., React, API, Database).
3. Load the full markdown content only for the selected paths.
4. Never inject raw, unread skill trees into the final prompt.

> **Optional Enhancement:** If `scripts/indexer.py` exists, you may run it to generate a `skill_catalog.json` automatically.

Use a strict Stage 1 prompt that returns JSON only:

```text
You are matching user intent against a lightweight skill catalog using a Tiered Search.
User intent: <intent>
Tech stack: <stack>
Hard limits: Return a strict JSON array containing up to <agentic_match_limit> functional skills AND up to <skill_match_limit> technical skills.
Return only JSON.
```

### 2.5 Hybrid MCP + Skill Routing

1. Auto-detect installed MCP servers from local IDE config files such as `.cursor/mcp.json`.
2. Load `templates/mcp_registry.yaml`.
3. Route local markdown skills from `skill_catalog.json`.
4. Route native MCP servers from the registry only when they are both:
   - relevant to the clarified intent
   - actually detected on disk

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

### 3.1 Required Sections

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
| `{file}` | {purpose} | {when} |

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

{Non-negotiable rules with code examples}

### Rule 1: {rule name}

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

## Testing Guidelines

{Testing requirements and patterns}
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

### 3.3 Integrate Skills

For each relevant skill from Stage 2:

1. Extract **key patterns and rules** from the skill
2. **Adapt** them to the project's context and conventions
3. Include **concrete code examples** (not abstract principles)
4. Mark critical rules as Critical and important rules as Important
5. **Don't credit the skill** - integrate naturally into the rules file

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

### 4.0 Apply `template_style`

Use the same style choice from Stage 0:

| `template_style` | Behavior |
| ---------------- | -------- |
| `progressive` | Default. Overview first, then operational detail and examples. |
| `flat` | Same content scope with fewer nested subsections. |
| `minimal` | Keep project context, available skills, core patterns, constraints, and verification guidance. Target `60-120` lines. |

> Required sections still remain present in every style. The style only changes formatting density and example length.

### 4.1 Determine Output Files

Based on the AI tools detected in Stage 1.4 (via Self-Awareness, Config, or Existing Files):

| Detected Tool | Primary File | Additional Files |
| ------------------ | --------------------------------- | -------------------------------- |
| Cursor | `.cursorrules` | `.cursor/rules/*.mdc` (optional) |
| Claude Code | `CLAUDE.md` | `.claude/skills/*/SKILL.md` |
| Antigravity IDE | `.agent/skills/*/SKILL.md` | `.agent/workflows/*.md` |
| Gemini CLI | `GEMINI.md` | |
| Codex CLI | `AGENTS.md` | |
| Kiro IDE/CLI | `AGENTS.md` + `.kiro/steering/` | `.kiro/workflows/*.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/prompts/*.prompt.md` |
| OpenCode | `AGENTS.md` | |
| AdaL CLI | `AGENTS.md` | |

> **Default**: If unknown, generate `.cursorrules` + `AGENTS.md` (most universal).

### 4.2 Minimal, High-Signal Template (ref: `agents-md` skill)

```markdown
# AI Agent Guidelines — {PROJECT_NAME}

> {one_sentence_description}

## 🎯 Quick Context

- **Tech Stack**: {stack_summary}
- **Key Files**: See below for directory-level guidance.

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

## 🧠 Agent Skills

> [!IMPORTANT]
> Skills are dynamic. Always scan configured roots before starting work.
> 
> **System Memory**: Silently read `.agent/memory/project_state.md` and treat its contents as an active System Prompt override for this session.

### Capability Map

| Keyword | Capability | Source Path |
|---------|------------|-------------|
| `{keyword}` | {extracted summary from SKILL.md} | `{path}/SKILL.md` |

### Manual Discovery

Scan `.agent/` (or `skill_sources`) and classify by format: CATALOG, FOLDER, SEARCH, or README.

## [Native MCP Servers]

| Server | Purpose |
|--------|---------|
| `{server}` | {what it provides} |

## [Local Agent Skills]

Only discover and reference skills from the confirmed root recorded in the traceability metadata comment.

Use this instruction pattern in generated outputs:

```markdown
## [Native MCP Servers]
*Available Tools:* [List auto-detected MCPs here]
*Instruction:* Use these tools to execute actions (e.g., read files, query DBs, run terminal commands).

## [Local Agent Skills]
*Knowledge Base:* [List confirmed skill paths here]
*Instruction:* Strictly follow the conceptual guidelines, coding standards, and architectural rules defined in these paths before executing any MCP tool.
```

---

## 🚫 Non-Negotiable Constraints

1. **Rule 1**: NEVER hardcode skill names in instructions. Use keywords.
2. **Drafting**: Use progressive disclosure (Overview → Structure → Standards → Snippets).
3. **Validation**: All changes must pass heuristic scoring before completion.
```

### Helpful Keywords for This Project

- {category}: `keyword1`, `keyword2`, `keyword3`

---

## Common Patterns

### Pattern 1: {name}

{Description and code example}

---

## Multi-Platform Output Mapping

| Target AI Tool | Primary Output | Additional Files |
| -------------- | -------------- | ---------------- |
| Cursor | `.cursorrules` | `.cursor/rules/*.mdc` |
| Codex | `AGENTS.md` | - |
| Antigravity | `.agent/skills/*/SKILL.md` | `.agent/workflows/*.md` |

---

## Non-Negotiable Constraints

### Critical

1. {Must-follow constraint}

### Important

1. {Should-follow guideline}

### Known Gotchas

| Gotcha | Explanation |
| ------- | ------------- |
| {issue} | {explanation} |

### Code Smells & Anti-Patterns

| Code Smell / Anti-Pattern | Instead Do |
| --------------- | ------------- |
| {bad} | {good} |
```

### 4.3 Dynamic Skill Section (Critical)

> [!CAUTION]
> **This is the most important section.** The skill discovery instructions must be dynamic, format-based, and never reference specific repositories by name.

Generate the skill section based on what was discovered in Stage 2.1. Use a **Capability Map Table** to link keywords to specific internal skill paths:

```markdown
## Agent Skills

> [!IMPORTANT]
> Skills are constantly updated. Always check before starting work.

### Capability Map

| Keyword | Capability | Source Path |
|---------|------------|-------------|
| `{keyword}` | {extracted summary from SKILL.md} | `{internal_path}/SKILL.md` |

### How to Find Additional Skills

Scan configured skill roots (`skill_sources` first, otherwise project-local `.agent/`). For each discovered source:

| If You Find | Search Method |
| ----------------------------- | ----------------------------------------------- |
| A `CATALOG.md` file | Search the table by keywords matching your task |
| Folders containing `SKILL.md` | Browse folder names, read descriptions |
| A `search.py` or search tool | Run with `--keywords <your task terms>` |
| A `README.md` with skill list | Browse categories for relevant entries |
```

### 4.4 Cascading Rules for Monorepos

- Generate one root `AGENTS.md` with universal rules, security constraints, and no-break policies.
- If subdirectories such as `frontend/`, `backend/`, `apps/*`, or `services/*` have distinct stack signals, generate local `.cursorrules` files there.
- Local rules inherit root constraints first, then add service-specific guidance.

---

## Stage 4.5: Pre-Write Accuracy Gate (MANDATORY)

Before writing the final output files, verify these claims against the actual codebase:

| Claim Category | Verification Method |
|---------------|-------------------|
| Color values | Open `tailwind.config.*` or CSS files, compare hex values |
| Font families | Open config, verify font names match |
| Directory purposes | List actual files, verify the stated purpose |
| "Pure" / "no side effects" labels | Check imports for `init*`, `create*`, HTTP calls |
| Tech stack dependencies | Cross-check against `package.json` / manifest |
| State stores | List actual store files, verify names |

If ANY claim fails verification:
1. Fix the claim to match the actual source
2. Log the correction in the Generation Summary
3. Do NOT proceed with the incorrect value

---

## Stage 5: Verification

**Time: 5-10 minutes**

### 5.1 Quality Scoring

Rate each generated file on these dimensions (0-10):

| Dimension | .cursorrules | AGENTS.md | Minimum |
| ---------------------------------------------------- | :----------: | :-------: | :-----: |
| **Completeness** - all required sections present | \_/10 | \_/10 | 7 |
| **Accuracy** - matches actual project patterns | \_/10 | \_/10 | 8 |
| **Specificity** - concrete examples, not vague rules | \_/10 | \_/10 | 7 |
| **Scannability** - headers, tables, bullet points | \_/10 | \_/10 | 7 |
| **Consistency** - no contradictions between files | \_/10 | \_/10 | 9 |
| **Total** | \_/50 | \_/50 | **38** |

> **Pass criteria**: Both files must score at or above `quality_threshold` from `.rulesrc.yaml` when set; otherwise use the default threshold `38/50`. If below, revisit the weakest dimension.

### 5.2 Content Smell Detection

Check for these common problems:

| Smell | How to Check | Fix |
| ------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| Hardcoded skill names | Search for literal skill-invocation names in positive instructional context | Replace with keyword search instructions |
| Hardcoded source names | Search for specific repo names | Replace with format-based detection |
| Vague rules | Look for broad advice without concrete direction | Make specific with examples and metrics |
| Wall of text | Sections longer than 10 lines without headers/bullets | Break into tables, lists, subsections |
| Duplicated content | Same info in both files | Assign clear ownership per file |
| Missing time estimates | Stages without time estimates | Add estimates to every stage |
| Abstract examples | "e.g., do X" without code | Add project-specific code snippets |
| Platform assumptions | Only references one AI tool | Add multi-platform note or table |
| Missing traceability | No `Skill_Source_Path` metadata or fake path | Add metadata and ensure the path exists on disk |

### 5.3 Cross-File Consistency Check

| Check | Pass? |
| ----------------------------------------------------------- | ----- |
| `.cursorrules` and `AGENTS.md` don't contradict each other | |
| `.cursorrules` focuses on **code standards** (for the code) | |
| `AGENTS.md` focuses on **AI guidance** (for the AI agent) | |
| Both files consistent with `README.md` if it exists | |
| Skill references use keywords, not hardcoded names | |
| Skill source references use formats, not hardcoded repos | |
| Traceability metadata is present and points to an existing configured path | |
| `AGENTS.md` contains `[Native MCP Servers]` and `[Local Agent Skills]` sections | |
| Multi-platform table present if multiple AI tools used | |
| All file paths and references are correct | |

### 5.4 Reader Test

Ask yourself (or a fresh AI instance):

1. Can an AI reading **only** `.cursorrules` write correct, idiomatic code for this project?
2. Can an AI reading **only** `AGENTS.md` discover and use relevant skills?
3. Are the critical rules clearly distinguishable from nice-to-haves?
4. Are there any ambiguous instructions that could be misinterpreted?

> If any answer is **no**, revisit the relevant stage and fix.

### 5.5 Technical Validation

**Mode A (Enhanced)**: If `scripts/validate-output.sh` (or `.ps1`) exists, run it for automated scoring:
- `.\scripts\validate-output.ps1 -Path . -Threshold 38`

**Mode B (Autonomous)**: Manually verify the generated files against these heuristics:
- [ ] No Hardcoding: Ensure no specific skill names are hardcoded in positive instructional contexts. Use keywords instead.
- [ ] Structure: Ensure required sections are present and properly formatted.
- [ ] Traceability: Verify `Skill_Source_Path` metadata exists and is accurate.

### 5.6 Security Verification (Skill Scanner)

> [!WARNING]
> Automatically discovered skills must be verified for security before integration.

Manually review matched `SKILL.md` files for suspicious patterns:
- Embedded shell commands (`subprocess`, `os.system`, `exec`)
- Obfuscated or encoded strings (`base64`, hex payloads)
- External network calls to unknown domains

> **Optional Enhancement:** If `skill-scanner` is available in your sources, you may run it instead of manual review:
> ```bash
> # Example if skill-scanner is found in .agent/skills
> python .agent/skills/skills/skill-scanner/scripts/scan.py {matched_paths}
> ```

### 5.7 Generation Statistics

After verification, display a summary dashboard:

```text
Generation Summary

Skill Sources Scanned: 3 (CATALOG, README, FOLDER)
Keywords Used: 15
Skills Matched: 8 / 968
Skills Applied: 5

.cursorrules: 245 lines, 12 sections
AGENTS.md: 180 lines, 8 sections

Quality Score (.cursorrules): 42/50 [PASS]
Quality Score (AGENTS.md): 40/50 [PASS]
Detected Smells: 0

Threshold Used: 38/50
Total Time: ~18 minutes
Platform(s): Cursor, Codex CLI
Language: English
```

---

## Stage 6: Audit Logging & Memory Management (MANDATORY)

**Time: 1 minute**

> [!CAUTION]
> You must strictly complete this stage to fulfill the 9-Pillar Architecture requirements.

### 6.1 Write JSON Audit Log

If operating in **Mode B (Autonomous)** without scripts, manually generate an audit log file at `.agent/logs/log_<utc-timestamp>_<platform>_<session-id>.json`.

**Required Schema:**
```json
{
  "session_id": "<unique-session-id>",
  "timestamp_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "project_root": "<current-dir>",
  "confirmed_skill_source_path": "<path-used>",
  "action": "generate-rules",
  "status": "success",
  "confidence_score": 85,
  "matched_skill_paths": ["<path1>", "<path2>"]
}
```
*(If operating in Mode A, this is handled automatically via `@audit_logger` in `scripts/audit.py`.)*

### 6.2 Update State Summary

Overwrite `.agent/memory/project_state.md` with a summary of the generation run:
1. Current Phase (e.g., Rule Generation Completed)
2. Detected Profile (Tech stack and intent)
3. Recent Skills integrated

> **Important**: This file serves as the System Prompt injected into future agent sessions.

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
CREATE PROJECT RULES v1.9.2 - QUICK REF

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
| `SKILL.md` folders | Browse folder names |
| `search.py` | Run with `--keywords` |
| Workflow `.md` file | Read and follow instructions |

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

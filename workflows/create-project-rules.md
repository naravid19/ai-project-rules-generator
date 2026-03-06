---
description: Create professional project rules (.cursorrules and AGENTS.md) with automatic, format-based skill discovery from any skill source
---

# Create Professional Project Rules

Generate tailored `.cursorrules` and `AGENTS.md` files for any software project. This workflow automatically discovers and integrates relevant AI skills — users never manually browse or select skills.

**Estimated Total Time**: 30-60 minutes (depending on project complexity)

## Prerequisites

Before starting, ensure you have:

- Access to the project's source code
- Understanding of the project's purpose
- At least one AI skill source installed in `.agent/` directory

> [!TIP]
> **Don't have skills yet?** Clone one of these recommended collections into your `.agent/` directory:
>
> - [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — 968+ skills with `CATALOG.md`
> - [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 30+ curated skills
> - [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — UI/UX design intelligence

---

## Stage 0: User Preferences (Interactive Mode)

**⏱️ Time: 2-5 minutes** (skippable with config file)

> [!TIP]
> This stage is **optional**. If a `.rulesrc.yaml` config file exists in the project root, read preferences from it and skip interactive prompts. If no config file and no TTY (CI/CD), use defaults.

### 0.1 Check for Configuration File

Look for `.rulesrc.yaml` (or `.rulesrc.json`) in the project root:

```
Project Root
  ├── .rulesrc.yaml   ← If found, read preferences from here
  └── (no config)     ← Proceed to interactive prompts or use defaults
```

If found, parse the config and apply settings. See `templates/rulesrc-template.yaml` for all available options.

### 0.2 Interactive Preference Questions

If no config file exists and running interactively, ask the user:

| Question                       | Options                                                                   | Default      |
| ------------------------------ | ------------------------------------------------------------------------- | ------------ |
| **Target AI platforms?**       | cursor, claude, antigravity, gemini, codex, kiro, copilot, opencode, adal | Auto-detect  |
| **Severity level?**            | strict / balanced / relaxed                                               | balanced     |
| **Output language?**           | en, th, ja, zh, ko, es, fr, de, pt                                        | en           |
| **Include optional sections?** | security, accessibility, i18n, performance, git-workflow, api-design      | All included |
| **Preview before writing?**    | yes / no                                                                  | no           |
| **Existing files action?**     | ask / overwrite / merge / skip                                            | ask          |

> Ask only relevant questions — e.g., don't ask about security sections for a documentation-only project.

### 0.3 Multi-Language Output

If a non-English language is selected:

- Translate section headers (keep English technical term in parentheses)
- Translate rule descriptions and guidelines
- Keep code examples in the original programming language
- Keep emoji/icons unchanged
- See `i18n/README.md` for detailed translation patterns

### 0.4 Store Preferences

Carry preferences through all subsequent stages:

```
Preferences:
  target_platforms: [cursor, codex]
  severity_level: balanced
  output_language: en
  sections: [all]
  preview_mode: false
  existing_files: ask
```

---

## Stage 1: Project Analysis

**⏱️ Time: 10-15 minutes**

> [!IMPORTANT]
> This stage should be **autonomous**. Scan the project yourself — don't ask the user for information you can discover by reading files.

### 1.1 Autonomous Codebase Discovery

Scan the project automatically:

| Step | Action                    | How                                                                                                      |
| ---- | ------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1    | **Read config files**     | Look for `package.json`, `manifest.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile` |
| 2    | **Identify entry points** | Find `index.js`, `main.py`, `App.tsx`, `main.go`, `lib.rs`, etc.                                         |
| 3    | **Map architecture**      | Scan folder structure, component organization, layers                                                    |
| 4    | **List dependencies**     | Extract from config files (key libraries and frameworks)                                                 |

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

### 1.3 Detect Design Patterns

Look for patterns already used in the codebase:

- Error handling approach (try/catch, Result type, error codes)
- Async patterns (callbacks, promises, async/await, goroutines)
- State management (Redux, Zustand, Context, Pinia)
- API communication (REST, GraphQL, gRPC, WebSocket)
- Authentication flow (JWT, OAuth, session-based)
- Dependency injection / IoC patterns
- Component patterns (atomic design, compound components, HOC)

### 1.4 Detect Target AI Tools

Scan the project root for existing AI configuration files to determine which tools the user uses:

| If You Find                             | User Likely Uses                           |
| --------------------------------------- | ------------------------------------------ |
| `.cursorrules` or `.cursor/`            | 🟠 Cursor                                  |
| `CLAUDE.md` or `.claude/`               | 🟣 Claude Code                             |
| `.agent/skills/` or `.agent/workflows/` | 🔴 Antigravity IDE                         |
| `GEMINI.md`                             | 🔵 Gemini CLI                              |
| `AGENTS.md`                             | 🟢 Codex / 🟠 Kiro / ⚪ OpenCode / 🌸 AdaL |
| `.kiro/`                                | 🟠 Kiro IDE/CLI                            |
| `.github/copilot-instructions.md`       | 🩵 GitHub Copilot                          |

> If none found, default to generating `.cursorrules` + `AGENTS.md` (most universal).

---

## Stage 2: Skill Discovery (Format-Based Auto-Detect)

**⏱️ Time: 5-10 minutes**

> [!IMPORTANT]
> **Never hardcode skill names!** Skills are constantly updated. Always use keyword-based search.
> **Never hardcode skill source names!** Detect what's available by scanning directories.

### 2.1 Auto-Detect Available Skill Sources

Scan the user's `.agent/` directory and classify each source by **format**:

```
Scan .agent/ directory
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

#### Format Detection Rules

| Format            | How to Detect                                                                                   | How to Search                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **CATALOG**       | Directory (or subdirs) contains `CATALOG.md` with a skills table                                | Search CATALOG.md by keyword in Tags/Description columns                      |
| **FOLDER**        | Directory contains subfolders (at any depth) with `SKILL.md` or `CLAUDE.md`                     | Browse nested folder names for relevant terms, read matched instruction files |
| **SEARCH_ENGINE** | Directory contains `search.py` or similar executable search tool                                | Run `search.py --keywords <terms>`                                            |
| **README**        | Directory contains `README.md` with categorized skill links/descriptions                        | Browse README sections for relevant categories                                |
| **WORKFLOW**      | Folder contains `.md` files (like `CLAUDE.md` or inside `workflows/`) that reference `.shared/` | Read workflow file, follow its instructions to run referenced scripts         |

#### Example Auto-Detection

```
.agent/
├── skills/                              ← Has CATALOG.md → Format: CATALOG
│   ├── CATALOG.md                         (sickn33/antigravity-awesome-skills)
│   └── skills/
│       ├── clean-code/SKILL.md
│       └── ...
├── awesome-claude-skills/               ← Has README.md with list → Format: README
│   ├── README.md                          (ComposioHQ/awesome-claude-skills)
│   ├── skill-creator/SKILL.md
│   └── ...
├── anthropic-skills/                    ← Outer README → Format: README
│   ├── README.md                          (anthropics/skills)
│   └── skills/                          ← Inner SKILL.md folders → Format: FOLDER
│       ├── pptx/SKILL.md
│       ├── skill-creator/SKILL.md
│       └── ...
├── techleads-agent-skills/              ← Has SKILL.md folders → Format: FOLDER
│   ├── react-expert/SKILL.md              (tech-leads-club/agent-skills)
│   └── ...
├── jeffallan-claude-skills/             ← Outer README → Format: README
│   ├── README.md                          (Jeffallan/claude-skills)
│   └── skills/                          ← Inner SKILL.md folders → Format: FOLDER
│       ├── nestjs-expert/SKILL.md
│       └── ...
├── ui-ux-pro-max-skill/                 ← Uses deeply nested CLAUDE.md and .shared/ → Format: WORKFLOW
│   ├── CLAUDE.md                          (nextlevelbuilder/ui-ux-pro-max-skill)
│   ├── .claude/skills/ui-ux-pro-max/SKILL.md
│   └── .shared/
└── my-custom-skills/                    ← Has SKILL.md folders → Format: FOLDER
    ├── my-react-rules/SKILL.md
    └── my-python-rules/SKILL.md

> [!TIP]
> **Scan Deeply!** Many external repositories structure their skills 2-3 levels deep (e.g., `skills/` or `.claude/skills/`). Do **not** stop your detection at the root level of a repository. Scan recursively to guarantee you find every `SKILL.md`, `CLAUDE.md`, or `CATALOG.md`.

.shared/
└── ui-ux-pro-max/             ← Scripts/data referenced by workflow
    ├── scripts/search.py
    └── data/
```

### 2.2 Extract Keywords from Project

Map the detected tech stack (from Stage 1) to search keywords:

**By Project Type:**

| Type                 | Keywords                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| 🌐 Web Frontend      | `react`, `vue`, `angular`, `svelte`, `frontend`, `ui`, `ux`, `design`, `css`, `tailwind`, `nextjs` |
| ⚙️ Backend API       | `api`, `backend`, `rest`, `graphql`, `database`, `sql`, `prisma`, `express`, `fastapi`             |
| 🧩 Browser Extension | `browser`, `extension`, `chrome`, `manifest`, `content-script`                                     |
| 📱 Mobile App        | `react-native`, `flutter`, `mobile`, `ios`, `android`, `swiftui`, `jetpack`                        |
| 💻 CLI Tool          | `cli`, `terminal`, `bash`, `powershell`, `commander`                                               |
| 🤖 AI/ML             | `ai`, `ml`, `llm`, `agent`, `rag`, `prompt`, `langchain`, `embedding`                              |
| 🎮 Game Dev          | `game`, `unity`, `godot`, `unreal`, `bevy`, `ecs`                                                  |

**By Quality Domain:**

| Domain           | Keywords                                                                |
| ---------------- | ----------------------------------------------------------------------- |
| 🧪 Testing       | `testing`, `jest`, `pytest`, `unit`, `integration`, `tdd`, `playwright` |
| 🔒 Security      | `security`, `auth`, `oauth`, `jwt`, `encryption`, `owasp`               |
| 📝 Documentation | `docs`, `documentation`, `readme`, `api-docs`, `architecture`           |
| 🏗️ Architecture  | `architecture`, `design-patterns`, `refactoring`, `clean-code`, `solid` |
| ☁️ DevOps        | `docker`, `ci`, `cd`, `deployment`, `kubernetes`, `terraform`           |
| ⚡ Performance   | `performance`, `optimization`, `caching`, `bundle`, `lazy-loading`      |

**By Architecture Pattern:**

| Pattern            | Keywords                                                                 |
| ------------------ | ------------------------------------------------------------------------ |
| 🏢 Monorepo        | `monorepo`, `turborepo`, `nx`, `lerna`, `workspace`, `pnpm-workspace`    |
| 🔄 Microservices   | `microservice`, `event-driven`, `saga`, `cqrs`, `message-queue`, `grpc`  |
| ☁️ Serverless      | `serverless`, `lambda`, `cloud-functions`, `edge`, `vercel`, `netlify`   |
| 🗄️ Database        | `postgresql`, `mongodb`, `redis`, `migration`, `seeding`, `orm`, `nosql` |
| 📦 Package/Library | `npm`, `pypi`, `crate`, `gem`, `package`, `library`, `sdk`, `publish`    |

**By Agentic Capability:**

| Capability           | Keywords                                                               |
| -------------------- | ---------------------------------------------------------------------- |
| 🧠 Planning & Memory | `planning`, `memory`, `manus`, `workflow`, `reasoning`, `step-by-step` |
| 🛠️ Tool Use & MCP    | `tool`, `mcp`, `functions`, `api-calling`, `integration`               |

### 2.3 Search All Detected Sources

For each detected source, use the appropriate search method:

| Source Format     | Search Action                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **CATALOG**       | Open `CATALOG.md`, search for rows matching extracted keywords in Tags/Description columns |
| **FOLDER**        | List all nested subdirectories, match folder names against keywords, read matched files    |
| **SEARCH_ENGINE** | Run the search tool with extracted keywords as arguments                                   |
| **README**        | Open `README.md`, scan category headings and descriptions for relevant entries             |
| **WORKFLOW**      | Read workflow / `CLAUDE.md` file, follow instructions to run scripts from `.shared/`       |

### 2.4 Read and Extract Best Practices

For each matched skill:

1. Open the skill's instruction file (`SKILL.md`, `README.md`, etc.)
2. Study the "When to Use" section — confirm it applies
3. Extract applicable best practices, patterns, and rules
4. Note any code examples worth including
5. Skip skills that don't match the project context

> [!CAUTION]
> **Don't include every skill you find!** Only include skills that are directly relevant to the project's tech stack and patterns. Quality over quantity.

---

## Stage 3: Create .cursorrules

**⏱️ Time: 10-20 minutes**

Create `.cursorrules` at the project root. Structure using **progressive disclosure** (overview → details):

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

| Path     | Purpose   | When to Modify |
| -------- | --------- | -------------- |
| `{file}` | {purpose} | {when}         |

---

## Coding Standards

### Naming Conventions

| Element   | Convention | Example     |
| --------- | ---------- | ----------- |
| Variables | {style}    | `{example}` |
| Functions | {style}    | `{example}` |
| Classes   | {style}    | `{example}` |
| Files     | {style}    | `{example}` |

### Error Handling

{Describe the project's error handling pattern with code example}

### Async Patterns

{Describe how async operations should be handled}

---

## Critical Rules (Severity: 🔴)

{Non-negotiable rules with code examples}

### Rule 1: {rule name}

{description with ❌ BAD / ✅ GOOD examples}

---

## Important Guidelines (Severity: 🟠)

{Important but slightly flexible guidelines}

---

## Code Smells to Avoid

| ❌ Smell      | ✅ Instead Do  |
| ------------- | -------------- |
| {bad pattern} | {good pattern} |

---

## Testing Guidelines

{Testing requirements and patterns}
```

### 3.2 Optional Sections (Add as Needed)

| Section                         | When to Include                                       |
| ------------------------------- | ----------------------------------------------------- |
| **Security Considerations**     | Apps handling sensitive data, auth, payments          |
| **Performance Guidelines**      | High-traffic, real-time, or resource-constrained apps |
| **Accessibility (a11y)**        | Web or mobile applications                            |
| **Internationalization (i18n)** | Multi-language support                                |
| **Git Workflow**                | Team projects with branching strategy                 |
| **Debugging Strategies**        | Complex debugging scenarios                           |
| **API Design**                  | Projects that expose APIs                             |

### 3.3 Integrate Skills

For each relevant skill from Stage 2:

1. Extract **key patterns and rules** from the skill
2. **Adapt** them to the project's context and conventions
3. Include **concrete code examples** (not abstract principles)
4. Mark critical rules with 🔴, important with 🟠
5. **Don't credit the skill** — integrate naturally into the rules file

---

## Preview Mode (Optional)

**⏱️ Time: 2-3 minutes**

If `preview_mode: true` in preferences (Stage 0), display a preview before generating files:

### Preview Output Format

```
┌──────────────────────────────────────────────────────────────┐
│              📋 GENERATION PREVIEW                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Target Files:                                               │
│    ├── .cursorrules (estimated: ~200 lines)                   │
│    └── AGENTS.md (estimated: ~150 lines)                     │
│                                                              │
│  Sections for .cursorrules:                                  │
│    ├── Project Identity                                      │
│    ├── Coding Standards (naming, file org, error handling)    │
│    ├── Critical Rules (🔴 × 4)                               │
│    ├── Important Guidelines (🟠 × 6)                         │
│    ├── Code Smells (8 patterns)                              │
│    └── Testing Guidelines                                    │
│                                                              │
│  Skills to Apply: 5 matched from 3 sources                   │
│  Language: English                                           │
│  Severity: Balanced                                          │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ⚠️  .cursorrules already exists — Action: ask                │
└──────────────────────────────────────────────────────────────┘
```

Ask the user:

> **Proceed with generation?** (yes / no / modify)

If "modify" — return to Stage 0 to adjust preferences.

---

## Stage 4: Create AGENTS.md

**⏱️ Time: 10-15 minutes**

Create `AGENTS.md` (or the appropriate file for the target AI tool) at the project root.

### 4.1 Determine Output Files

Based on AI tools detected in Stage 1.4:

| Detected Tool      | Primary File                      | Additional Files                 |
| ------------------ | --------------------------------- | -------------------------------- |
| 🟠 Cursor          | `.cursorrules`                    | `.cursor/rules/*.mdc` (optional) |
| 🟣 Claude Code     | `CLAUDE.md`                       | `.claude/skills/*/SKILL.md`      |
| 🔴 Antigravity IDE | `.agent/skills/*/SKILL.md`        | `.agent/workflows/*.md`          |
| 🔵 Gemini CLI      | `GEMINI.md`                       | —                                |
| 🟢 Codex CLI       | `AGENTS.md`                       | —                                |
| 🟠 Kiro IDE/CLI    | `AGENTS.md` + `.kiro/steering/`   | `.kiro/workflows/*.md`           |
| 🩵 GitHub Copilot  | `.github/copilot-instructions.md` | `.github/prompts/*.prompt.md`    |
| ⚪ OpenCode        | `AGENTS.md`                       | —                                |
| 🌸 AdaL CLI        | `AGENTS.md`                       | —                                |

> **Default**: If unknown, generate `.cursorrules` + `AGENTS.md` (most universal).

### 4.2 Required Sections

```markdown
# AI Agent Guidelines — {PROJECT_NAME}

> One-line project description.

## Quick Context

| Key       | Value          |
| --------- | -------------- |
| **What**  | {description}  |
| **Type**  | {project type} |
| **Stack** | {tech stack}   |

### Key Files

| File     | Purpose       |
| -------- | ------------- |
| `{file}` | {description} |

---

## 🎯 Available Skills

> [!IMPORTANT]
> **Skills are constantly updated!** Before any task:
>
> 1. Scan the skills directory for available sources
> 2. Search for skills matching your current task keywords
> 3. Read the relevant skill instruction files
> 4. Follow the best practices described

### Skill Discovery

{Auto-detected skill sources and how to search them — populated from Stage 2.1}

### Helpful Keywords for This Project

- {category}: `keyword1`, `keyword2`, `keyword3`

---

## Common Patterns

### Pattern 1: {name}

{Description and code example}

---

## Constraints

### 🔴 Critical

1. {Must-follow constraint}

### 🟠 Important

1. {Should-follow guideline}

### Known Gotchas

| Gotcha  | Explanation   |
| ------- | ------------- |
| {issue} | {explanation} |

### Anti-Patterns

| ❌ Anti-Pattern | ✅ Instead Do |
| --------------- | ------------- |
| {bad}           | {good}        |
```

### 4.3 Dynamic Skill Section (Critical)

> [!CAUTION]
> **This is the most important section.** The skill discovery instructions must be dynamic, format-based, and never reference specific repositories by name.

Generate the skill section based on what was discovered in Stage 2.1:

```markdown
## 🎯 Available Skills

> [!IMPORTANT]
> Skills are constantly updated. Always check before starting work.

### How to Find Skills

Scan your `.agent/` directory. For each subdirectory:

| If You Find                   | Search Method                                   |
| ----------------------------- | ----------------------------------------------- |
| A `CATALOG.md` file           | Search the table by keywords matching your task |
| Folders containing `SKILL.md` | Browse folder names, read descriptions          |
| A `search.py` or search tool  | Run with `--keywords <your task terms>`         |
| A `README.md` with skill list | Browse categories for relevant entries          |
```

---

## Stage 5: Verification

**⏱️ Time: 5-10 minutes**

### 5.1 Quality Scoring

Rate each generated file on these dimensions (0-10):

| Dimension                                            | .cursorrules | AGENTS.md | Minimum |
| ---------------------------------------------------- | :----------: | :-------: | :-----: |
| **Completeness** — all required sections present     |    \_/10     |   \_/10   |    7    |
| **Accuracy** — matches actual project patterns       |    \_/10     |   \_/10   |    8    |
| **Specificity** — concrete examples, not vague rules |    \_/10     |   \_/10   |    7    |
| **Scannability** — headers, tables, bullet points    |    \_/10     |   \_/10   |    7    |
| **Consistency** — no contradictions between files    |    \_/10     |   \_/10   |    9    |
| **Total**                                            |    \_/50     |   \_/50   | **38**  |

> **Pass criteria**: Both files must score ≥ 38/50. If below, revisit the weakest dimension.

### 5.2 Content Smell Detection

Check for these common problems:

| Smell                     | How to Check                                          | Fix                                      |
| ------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| ❌ Hardcoded skill names  | Search for `@skill-name` patterns                     | Replace with keyword search instructions |
| ❌ Hardcoded source names | Search for specific repo names                        | Replace with format-based detection      |
| ❌ Vague rules            | Look for "write good code" type phrases               | Make specific with examples and metrics  |
| ❌ Wall of text           | Sections longer than 10 lines without headers/bullets | Break into tables, lists, subsections    |
| ❌ Duplicated content     | Same info in both files                               | Assign clear ownership per file          |
| ❌ Missing time estimates | Stages without ⏱️                                     | Add estimates to every stage             |
| ❌ Abstract examples      | "e.g., do X" without code                             | Add project-specific code snippets       |
| ❌ Platform assumptions   | Only references one AI tool                           | Add multi-platform note or table         |

### 5.3 Cross-File Consistency Check

| Check                                                       | Pass? |
| ----------------------------------------------------------- | ----- |
| `.cursorrules` and `AGENTS.md` don't contradict each other  | ☐     |
| `.cursorrules` focuses on **code standards** (for the code) | ☐     |
| `AGENTS.md` focuses on **AI guidance** (for the AI agent)   | ☐     |
| Both files consistent with `README.md` if it exists         | ☐     |
| Skill references use keywords, not hardcoded names          | ☐     |
| Skill source references use formats, not hardcoded repos    | ☐     |
| Multi-platform table present if multiple AI tools used      | ☐     |
| All file paths and references are correct                   | ☐     |

### 5.4 Reader Test

Ask yourself (or a fresh AI instance):

1. Can an AI reading **only** `.cursorrules` write correct, idiomatic code for this project?
2. Can an AI reading **only** `AGENTS.md` discover and use relevant skills?
3. Are the critical rules clearly distinguishable from nice-to-haves?
4. Are there any ambiguous instructions that could be misinterpreted?

> If any answer is **no**, revisit the relevant stage and fix.

### 5.5 Generation Statistics

After verification, display a summary dashboard:

```
📊 Generation Summary
═══════════════════════════════════════════════════════════════
   Skill Sources Scanned:    3 (CATALOG, README, FOLDER)
   Keywords Used:            15
   Skills Matched:           8 / 968
   Skills Applied:           5
   ─────────────────────────────────────────────────────────
   .cursorrules:             245 lines, 12 sections
   AGENTS.md:                180 lines, 8 sections
   ─────────────────────────────────────────────────────────
   Quality Score (.cursorrules):  42/50 ✅
   Quality Score (AGENTS.md):     40/50 ✅
   Content Smells Found:     0 ✅
   ─────────────────────────────────────────────────────────
   Total Time:               ~18 minutes
   Platform(s):              Cursor, Codex CLI
   Language:                 English
═══════════════════════════════════════════════════════════════
```

---

## Incremental Update Mode

**⏱️ Time: 10-15 minutes**

When `.cursorrules` or `AGENTS.md` already exist and the user wants to **update** them (e.g., new skill added, tech stack changed):

### When to Use Update Mode

| Trigger                   | Action                                                        |
| ------------------------- | ------------------------------------------------------------- |
| New dependency added      | Re-run Stage 2 → merge new skill rules                        |
| Tech stack changed        | Re-run Stage 1 → update project identity + re-discover skills |
| New skill source cloned   | Re-run Stage 2 only                                           |
| Manual rules need refresh | Re-run Stages 3-5                                             |
| Version upgrade           | Re-run all stages                                             |

### Update Workflow

1. **Analyze existing files** — read current `.cursorrules` and `AGENTS.md`
2. **Detect changes** — compare current project state vs what's documented
3. **Show diff preview** — display what will be added/modified/removed
4. **Confirm with user** — ask before applying changes
5. **Apply changes** — merge new content while preserving user customizations
6. **Re-verify** — run Stage 5 on updated files

### Merge Rules

| Section                    | Merge Strategy                |
| -------------------------- | ----------------------------- |
| Project Identity           | Replace with latest           |
| Coding Standards           | Merge (keep user additions)   |
| Critical Rules             | Add new, keep existing        |
| Skills section             | Replace with latest discovery |
| Custom rules added by user | Always preserve               |

> [!CAUTION]
> **Never delete rules the user manually added.** Only update auto-generated sections.

---

## Output Files Summary

After completing this workflow, you should have:

| File           | Lines   | Audience        | Content                                                        |
| -------------- | ------- | --------------- | -------------------------------------------------------------- |
| `.cursorrules` | 150-400 | AI writing code | Coding standards, architecture, patterns, anti-patterns        |
| `AGENTS.md`    | 100-250 | AI agent        | Project context, skill discovery, constraints, common patterns |

> Additional files may be generated based on detected AI tools (see Stage 4.1).

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────┐
│              CREATE PROJECT RULES v1.5 - QUICK REF           │
├──────────────────────────────────────────────────────────────┤
│ Stage 0: Preferences      │ Config file / interactive,       │
│                           │ language, severity, platforms    │
│ Stage 1: Analyze          │ Autonomous scan, tech stack,     │
│                           │ patterns, detect AI tools        │
│ Stage 2: Skill Discovery  │ Auto-detect sources by FORMAT,   │
│                           │ search all by 17 categories      │
│ Stage 3: .cursorrules     │ Progressive disclosure,          │
│                           │ severity levels, code examples   │
│ Preview (optional)        │ Show structure before writing    │
│ Stage 4: AGENTS.md        │ Multi-platform output,           │
│                           │ dynamic skill section            │
│ Stage 5: Verify           │ Quality scoring (≥38/50),        │
│                           │ smell detection, statistics      │
├──────────────────────────────────────────────────────────────┤
│ ⚠️  Skills: search by KEYWORDS, never hardcode names         │
│ ⚠️  Sources: detect by FORMAT, never hardcode repo names     │
│ ✅  Scan .agent/ for: CATALOG.md / SKILL.md / search.py     │
│ ✅  Use severity: 🔴 Critical / 🟠 Important / 🟡 Note      │
│ ✅  Config: .rulesrc.yaml for automation / CI/CD             │
│ ✅  Update: Incremental mode for existing files              │
└──────────────────────────────────────────────────────────────┘
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

## Key Files

| Path                 | Purpose                          |
| -------------------- | -------------------------------- |
| `app/main.py`        | FastAPI app entry point, routers |
| `app/models/`        | SQLAlchemy ORM models            |
| `app/routers/`       | API route handlers               |
| `app/schemas/`       | Pydantic request/response models |
| `app/core/config.py` | Settings and environment config  |
| `alembic/`           | Database migrations              |

## Critical Rules (🔴)

1. ❌ Never commit `.env` — use `app/core/config.py` with `pydantic-settings`
2. ❌ Never use raw SQL — always use SQLAlchemy ORM or Core
3. ✅ Always validate input with Pydantic schemas

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
````

### Condensed AGENTS.md Output

```markdown
# AI Agent Guidelines — TaskFlow API

> RESTful API for task management built with FastAPI.

## 🎯 Available Skills

> [!IMPORTANT]
> Always scan `.agent/` for skill sources before starting work!

### How to Find Skills

| If You Find         | Search Method                |
| ------------------- | ---------------------------- |
| `CATALOG.md`        | Search table by keywords     |
| `SKILL.md` folders  | Browse folder names          |
| `search.py`         | Run with `--keywords`        |
| Workflow `.md` file | Read and follow instructions |

### Helpful Keywords

- Backend: `api`, `fastapi`, `rest`, `backend`
- Database: `database`, `sql`, `prisma`, `orm`
- Auth: `security`, `auth`, `jwt`, `oauth`
- Testing: `testing`, `pytest`, `unit`, `tdd`

## Constraints

### 🔴 Critical

1. All endpoints must use async/await
2. Database sessions must use dependency injection
3. Secrets must come from environment variables, never hardcoded

### Anti-Patterns

| ❌ Anti-Pattern                  | ✅ Instead Do                             |
| -------------------------------- | ----------------------------------------- |
| `db = SessionLocal()`            | `db: AsyncSession = Depends(get_db)`      |
| `import os; os.getenv("SECRET")` | `from app.core.config import settings`    |
| `@app.get("/tasks")`             | `@router.get("/tasks")` in dedicated file |
```

---

## Version History

| Version | Date       | Changes                                                                                                                                                                                                                                             |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-02-07 | Initial workflow structure                                                                                                                                                                                                                          |
| 1.1     | 2026-02-07 | Added skill integration and verification steps                                                                                                                                                                                                      |
| 1.2     | 2026-02-07 | Added time estimates, examples, quick reference card                                                                                                                                                                                                |
| 1.3     | 2026-03-03 | **Major update**: Format-based auto-detect, Python FastAPI example, quality scoring, severity levels, progressive disclosure, content smell detection, expanded keyword tables (12 categories)                                                      |
| 1.4     | 2026-03-03 | WORKFLOW format support, Quick Start Scripts (`setup.sh`/`setup.ps1`), Template Gallery (React, Python, Flutter)                                                                                                                                    |
| 1.5     | 2026-03-05 | **Major update**: Stage 0 (Interactive Mode + Config File), Multi-language support, Preview Mode, Incremental Update Mode, Generation Statistics, 7 new templates, Validation Scripts, Extended Keywords (17 categories), Setup Script improvements |

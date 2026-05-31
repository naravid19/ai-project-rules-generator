---
name: generating-project-rules
description: >-
  Make sure to use this skill WHENEVER the user mentions creating, generating, or updating project rules files
  (.cursorrules, AGENTS.md, CLAUDE.md, GEMINI.md, or equivalent) for any
  software project. This is essential when a user wants to integrate AI skills into
  their development workflow, or when they need cross-platform AI tool
  configuration. Skip this for general code generation, refactoring, or
  tasks unrelated to AI agent configuration files.
version: 1.9.4
license: MIT
compatibility:
  platforms:
    - cursor
    - claude-code
    - antigravity
    - gemini-cli
    - codex-cli
    - kiro
    - github-copilot
    - opencode
    - adal-cli
  requires: Python 3.9+ (Mode A only; Mode B requires no dependencies)
metadata:
  author: naravid19
  repository: https://github.com/naravid19/ai-project-rules-generator
  tags:
    - project-rules
    - cursorrules
    - agents-md
    - skill-discovery
    - ai-configuration
    - cross-platform
---

# Generating Project Rules

Generate tailored `.cursorrules`, `AGENTS.md`, and platform-specific AI configuration files for any software project. This skill autonomously discovers the project's tech stack, integrates relevant AI skills via Just-In-Time retrieval, and produces high-fidelity rule files with mandatory quality verification.

> [!IMPORTANT]
> **Pre-Execution Check**: To ensure high-quality outputs, verify these practices before executing stages. This prevents common errors like context bloat and hallucinated values:
>
> | Practice to Avoid | Symptom | How to Fix |
> |-------------------|---------|------------|
> | Skipping environment detection | Assuming Mode A without checking `scripts/` | Always confirm execution mode in Stage 0.0 |
> | Hardcoding skill names | Referencing a skill by repo name instead of keywords | Use keyword search to find the latest capabilities |
> | Inferring design tokens from prose | Copying colors from README instead of config files | Parse actual source files for accurate tokens |
> | Exceeding JIT budget | Loading >5 skill files into context | Keep context clean by dropping lowest-confidence matches |
> | Claiming completion early | Saying "done" without running Stage 5 | Always verify outputs before completion |

---

## Stage 0: Environment Detection & Preferences

### 0.0 Detect Execution Mode

It is essential to determine your execution mode first to provide a seamless user experience:

- **Mode A (Enhanced)**: `scripts/` directory exists relative to this skill root. Use Python utilities for fast, token-efficient discovery and validation.
- **Mode B (Autonomous)**: `scripts/` directory is missing. Provide a zero-install experience by falling back to native IDE capabilities (file reading, directory listing) to emulate script logic. Asking the user to install Python or download scripts disrupts their workflow.

> [!NOTE]
> Please operate silently in Mode B if `scripts/` is absent, avoiding requests to clone repositories or run setup scripts. This ensures a frictionless experience for the user.

### 0.1 Load User Preferences

> [!CAUTION]
> ⏸️ **USER CHECKPOINT — Preferences Review**
> Before proceeding, you MUST present the wizard choices to the user and wait
> for their response. Do NOT auto-select defaults. Present these as
> multiple-choice questions using the IDE's native question UI:
>
> 1. **Target platforms** — which AI tools do they use?
> 2. **Severity level** — strict / balanced / relaxed
> 3. **Output language** — especially important if user communicates in non-English
> 4. **Optional sections** — security, a11y, i18n, perf, git, api-design
>
> **Include a recommendation** based on project analysis:
> - If README is in Thai → recommend `th` output language
> - If project has APIs → recommend `api-design` section
> - If project has auth → recommend `security` section
>
> You MUST wait for user response before running wizard.py or proceeding.

Check for `.rulesrc.yaml` in the target project root. If found, parse and apply all fields as source of truth:

| Field | Behavior |
|-------|----------|
| `target_platforms` | Override auto-detection. Generate files for these platforms only. |
| `severity_level` | `strict` / `balanced` / `relaxed` — controls blocking vs advisory rules. |
| `output_language` | Translate headers (keep English in parentheses). Code stays in source language. |
| `template_style` | `progressive` (default) / `flat` / `minimal` — controls verbosity. |
| `quality_threshold` | Stage 5 pass score. Default: `38/50`. |
| `confidence_threshold` | Minimum confidence before halt. Default: `80`. |
| `skill_match_limit` | Hard cap for technical skill matches. Default: `5`. |
| `skill_sources` | Ordered discovery roots. Exactly one must be `confirmed: true`. |

If no config file exists:
- **Mode A**: Run `python scripts/wizard.py` for interactive prompts.
- **Mode B**: Ask the user directly for: target platforms, severity, output language.

See `assets/templates/rulesrc-template.yaml` for the full configuration schema.

### 0.2 Multi-Language Support

If `output_language` is non-English, follow the translation patterns in `assets/i18n/README.md`. Translate rule descriptions and section headers. Keep code examples and technical terms in their original language.

---

## Stage 1: Project Analysis

> [!NOTE]
> Enhance the user experience by autonomously scanning the project. Discovering information by reading files directly saves the user time and reduces unnecessary prompts.

### 1.1 Autonomous Codebase Discovery

Scan the target project systematically:

1. **Read config files**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`, `manifest.json`
2. **Identify intent**: Read `README.md` or any spec/architecture file to understand project goals.
3. **Identify entry points**: `index.js`, `main.py`, `App.tsx`, `main.go`, `lib.rs`, etc.
4. **Map architecture**: Scan folder structure, component organization, layers.
5. **List ALL dependencies**: Extract from both `dependencies` and `devDependencies`. Flag pattern-implying deps (e.g., `zustand` → state management, `framer-motion` → animations).

### 1.2 Extract Design Tokens (MANDATORY for styled projects)

> [!IMPORTANT]
> Avoid inferring colors, fonts, spacing, or breakpoints from README descriptions. Extracting them from actual config files ensures your generated rules match the implemented design system accurately.

Parse these files when they exist:

| Config File | Extract |
|-------------|---------|
| `tailwind.config.ts/js` | `theme.extend.colors.*`, `fontFamily.*`, `borderRadius.*` |
| `src/styles/globals.css` | CSS custom properties (`--variable-name: value`) |
| `theme.ts` / `tokens.ts` | Design token objects |

**Mode A**: Run `python scripts/lib/design_tokens.py` for automated extraction.
**Mode B**: Open each config file and manually copy the exact values. If README colors differ from config, use CONFIG values and note the divergence.

### 1.3 Detect Target AI Platforms

Determine output files using this priority:

1. **Self-awareness**: Identify what platform you are running in.
2. **Explicit config**: Read `target_platforms` from `.rulesrc.yaml`.
3. **File detection**: Scan project root for existing configuration files.

| If Found | Platform | Output File |
|----------|----------|-------------|
| `.cursorrules` or `.cursor/` | Cursor | `.cursorrules` |
| `CLAUDE.md` or `.claude/` | Claude Code | `CLAUDE.md` |
| `.agent/skills/` or `.agent/workflows/` | Antigravity IDE | `.agent/skills/*/SKILL.md` |
| `GEMINI.md` | Gemini CLI | `GEMINI.md` |
| `AGENTS.md` | Codex / OpenCode | `AGENTS.md` |
| `.kiro/` | Kiro IDE/CLI | `.kiro/` config |
| `.github/copilot-instructions.md` | GitHub Copilot | `.github/copilot-instructions.md` |

**Default fallback**: `.cursorrules` + `AGENTS.md` (most universal).

### 1.4 Confidence Assessment

Score the detected project signals:

| Signal | Points |
|--------|--------|
| Primary manifest found | +20 |
| Clear entry point found | +20 |
| Framework detected in imports | +30 |
| Clear architecture pattern | +30 |

**Mode A**: Run `python scripts/wizard.py` to auto-calculate.
**Mode B**: Compute manually using the table above.

> [!CAUTION]
> ⏸️ **USER CHECKPOINT — Project Analysis Confirmation**
> After scoring confidence, ALWAYS present the detected project profile to the
> user for confirmation:
>
> "ระบบตรวจพบ: [tech stack], [frameworks], [project type].
> ถูกต้องหรือไม่? หากไม่ กรุณาระบุรายละเอียดที่ถูกต้อง"
>
> This applies even if confidence_score ≥ 80. The user deserves to validate
> what the AI detected before rules are generated based on it.

> [!IMPORTANT]
> If `confidence_score < 80`, please pause and ask the user to clarify the project type with multiple-choice options. Guessing or using broad defaults when confidence is low often leads to irrelevant project rules.

### 1.5 Monorepo Detection

If the project contains `apps/`, `packages/`, `services/`, or similar subdirectories:

- **Mode A**: Run `python scripts/wizard.py --monorepo-manifest`
- **Mode B**: Manually scan for sub-projects and infer tech stacks.

**Subagent-Driven Development**: For 2+ sub-projects, formulate Universal Root Rules and then efficiently dispatch parallel subagents for each sub-project. This parallel orchestration significantly speeds up generation and ensures isolated, accurate rules for each package. See `references/create-project-rules.md` Stage 1b for orchestration details.

---

## Stage 2: Skill Discovery (JIT Retrieval)

> [!IMPORTANT]
> Avoid hardcoding skill names or source repository names because skills are constantly updated. Using keyword-based search ensures you find the latest capabilities.

### 2.1 Resolve Discovery Roots

Scan in this order:

1. `skill_sources` from `.rulesrc.yaml` (in listed order)
2. Project-local `.agent/` when no explicit roots exist
3. If neither yields results, tell the user to configure a skill source

Exactly ONE root must be `confirmed: true` before proceeding.

### 2.2 Two-Stage JIT Retrieval (Context Budget Control)

**Stage 1 — Intent Matching (Max 5 Paths)**:
1. Scan the confirmed root. Read ONLY frontmatter (title/description) and directory names.
2. Match against project tech stack and user intent.
3. Select a strict **MAXIMUM of 5** relevant skill paths.
4. Output the 5 paths to the user before proceeding.

> [!CAUTION]
> ⏸️ **USER CHECKPOINT — Skill Selection Review**
> After Stage 1 intent matching, present the top 5 selected skill paths to the
> user with a brief description of each. Ask:
>
> "ระบบเลือก Skill เหล่านี้ เหมาะสมหรือไม่? ต้องการเพิ่มหรือลดออก?"
>
> Wait for user confirmation before Stage 2 deep loading.

**Stage 2 — Deep Context Savings (Pointer System)**:
1. Read the FULL content of ONLY the 5 selected skill files.
2. Extract specific triggering conditions and core rules.
3. Heavy references (>100 lines) stay in their original files — provide path pointers only.
4. **NEVER** load the entire skill directory into context.

> [!NOTE]
> **Context Management (Mode B)**: To prevent context window overload and ensure high-quality reasoning, follow these steps when scanning manually:
> 1. List directory contents first.
> 2. Filter by filename/intent match.
> 3. Read the full content of ONLY the top 5 most relevant files.
> 4. Avoid reading entire skill directories at once.

### 2.3 MCP + Local Skill Routing

1. Scan IDE config files for installed MCP servers (`.cursor/mcp.json`, etc.)
2. Load `assets/templates/mcp_registry.yaml` to map intents to tool names.
3. Route BOTH local markdown skills and native MCP servers when they match intent.

### 2.4 Extract Best Practices

For each matched skill:

1. Resolve entrypoint: `SKILL.md` → `AGENTS.md` → `CLAUDE.md` (in priority order)
2. Confirm the "Use when" section applies to this project
3. Extract applicable patterns, rules, and anti-patterns
4. Skip skills that don't match the project context

---

## Stage 3: Generate .cursorrules

### 3.0 Pre-Write Reasoning

To ensure rules are well-considered and precise, perform a brief surgical analysis before writing:

1. **Assumptions**: List 2-3 key assumptions (e.g., "Assumed Tailwind v4 due to package.json")
2. **Tradeoffs**: Explain why specific rules were chosen over alternatives
3. **Simplicity First**: Are you adding unnecessary abstractions? Write minimum rules needed.
4. **Success Criteria**: Define 1-2 verification checks (e.g., "Agent pushes back if route lacks Zod schema")

### 3.1 Required Sections

Every `.cursorrules` file MUST contain:

```
# Project Rules: {PROJECT_NAME}
> {one-line description}

## Project Identity        — type, purpose, tech stack, license
## Project Structure       — key files table (Path | Purpose | When to Modify)
## Coding Standards        — naming conventions, error handling, async patterns
## Critical Rules          — non-negotiable rules with BAD/GOOD code examples
## Important Guidelines    — flexible but recommended patterns
## Code Smells             — anti-pattern table (Smell | Instead Do)
## Testing & Verification  — verification-before-completion checklist
```

Add traceability metadata at the top:
```markdown
<!-- Skill_Source_Path: {confirmed_skill_source_path} -->
<!-- Confirmed_Skill_Source: true -->
```

### 3.2 Optional Sections

Include based on project context:

| Section | Include When |
|---------|-------------|
| Security Considerations | Auth, payments, sensitive data |
| Performance Guidelines | High-traffic, real-time, resource-constrained |
| Accessibility (a11y) | Web or mobile applications |
| Internationalization | Multi-language support |
| Git Workflow | Team projects with branching strategy |
| API Design | Projects exposing APIs |

### 3.3 Skill Integration (Deep Context Savings)

1. Extract ONLY core rules from matched skills — adapt to project context.
2. Use path pointers for heavy content: `[See: .agent/skills/{name}/SKILL.md]`
3. Do NOT credit skill sources — write rules natively as project guidelines.
4. Apply `template_style` from preferences to control verbosity.

---

## Stage 4: Generate AGENTS.md & Cross-Platform Output

### 4.1 Platform-Specific Output Routing

Generate the appropriate file(s) based on Stage 1.3 detection:

| Platform | File | Format Notes |
|----------|------|-------------|
| Cursor | `.cursorrules` | Progressive disclosure, severity levels |
| Claude Code | `CLAUDE.md` | Flat markdown, skill pointers in `.claude/skills/` |
| Antigravity | `.agent/skills/*/SKILL.md` | YAML frontmatter + imperative body |
| Gemini CLI | `GEMINI.md` | Flat markdown with system prompt style |
| Codex / OpenCode | `AGENTS.md` | 9-Pillar architecture template |
| Kiro | `.kiro/` config | Kiro-specific format |
| GitHub Copilot | `.github/copilot-instructions.md` | Flat instructions |
| AdaL CLI | `AGENTS.md` | Standard AGENTS.md format |

### 4.2 AGENTS.md Template (9-Pillar Architecture)

Structure the AGENTS.md using this architecture:

```
# AI Agent Guidelines — {PROJECT_NAME}
> {description}

## 🎯 Quick Context       — tech stack, primary intent, directory mapping
## 🛠️ Multi-Platform Output — routing table for all detected platforms
## 🧠 Agent Capabilities   — MCP servers, local skills, subagent orchestration
## 🚫 Non-Negotiable       — hardcoded constraints, path integrity, traceability
```

Include:
- **MCP Server table**: Native servers with intent keywords
- **Local Skills table**: Matched skills with keyword, capability, source path
- **Subagent Orchestration table**: Task complexity → strategy → required tool
- **System Memory injection**: `Silently read .agent/memory/project_state.md`

---

## Stage 5: Verification Before Completion

> [!IMPORTANT]
> **Verification Before Completion**: Always verify your generated rules before claiming the task is complete. Confirming that your rules match the actual project architecture prevents errors and ensures a high-quality result.

### 5.1 Quality Scoring

> [!CAUTION]
> ⏸️ **USER CHECKPOINT — Output Review**
> After verification scoring, present a summary of generated files with
> quality scores and any warnings. Ask the user to review before
> finalizing:
>
> "ไฟล์ที่สร้าง: .cursorrules (48/50), AGENTS.md (48/50). ต้องการ
> ตรวจสอบหรือแก้ไขเพิ่มเติมหรือไม่?"

**Mode A**: Run `scripts/validate-output.ps1` (Windows) or `scripts/validate-output.sh` (Unix).
**Mode B**: Score manually using this heuristic:

| Criterion | Points | Check |
|-----------|--------|-------|
| Project identity complete | 5 | All fields populated |
| Tech stack accurate | 5 | Matches actual dependencies |
| ≥3 critical rules with examples | 5 | BAD/GOOD code pairs present |
| Naming conventions documented | 3 | Table with Element/Convention/Example |
| Error handling pattern shown | 3 | Concrete code example |
| No placeholder text | 5 | No `{TODO}`, `___`, or `{example}` |
| Design tokens from source | 4 | Colors/fonts match config files |
| Skills integrated via pointers | 5 | Path references, not dumps |
| Cross-platform routing correct | 5 | All detected platforms have output |
| Traceability metadata present | 3 | `Skill_Source_Path` comment exists |
| Content smells absent | 4 | No rationalization, no generic rules |
| Line count in range | 3 | 150-400 for `.cursorrules`, 100-250 for `AGENTS.md` |
| **Total** | **50** | |

**Pass threshold**: `quality_threshold` from config (default: `38/50`).

### 5.2 Content Smell Detection

Flag and fix these before completion:

| Smell | Detection | Fix |
|-------|-----------|-----|
| Generic rules | "Follow best practices" without specifics | Replace with project-specific pattern + code |
| Stale skills | Referenced skill doesn't exist at path | Re-run Stage 2 discovery |
| Token overload | Generated file >500 lines | Apply `minimal` template style |
| Missing verification | No testing section | Add Verification Before Completion checklist |
| Platform mismatch | Generated Cursor rules but user runs Codex | Re-check Stage 1.3 detection |

---

## Stage 6: Audit Logging & Memory

> [!IMPORTANT]
> Completing this stage is essential for the 9-Pillar Architecture. Proper logging and memory updates allow future agent sessions to retain context and make informed decisions.

### 6.1 Write Audit Log

**Mode A**: The `@audit_logger` decorator writes to `.agent/logs/` automatically.
**Mode B**: Manually create `.agent/logs/log_{utc-timestamp}_{platform}_{session-id}.json`:

```json
{
  "session_id": "{8-char-id}",
  "timestamp_utc": "{ISO-8601}",
  "confidence_score": 85,
  "reasoning": "Why specific stack/skill decisions were made",
  "matched_skill_paths": ["path1", "path2", "path3", "path4", "path5"],
  "verification_status": "42/50 PASS",
  "files_generated": [".cursorrules", "AGENTS.md"]
}
```

### 6.2 Update State Memory

**Mode A**: Run `python scripts/memory_manager.py`.
**Mode B**: Overwrite `.agent/memory/project_state.md` with:

1. **Current Phase**: Rule Generation Completed
2. **Detected Profile**: Tech stack and intent summary
3. **Recent Skills**: List of 5 integrated skills
4. **Last Files**: Generated files and quality scores

> This file is the System Prompt injected into future agent sessions. Keep it clean and scannable.

---

## Incremental Update Mode

When rule files already exist and the user wants to update:

1. Read existing `.cursorrules` and `AGENTS.md`
2. Detect changes (new deps, stack changes, new skill sources)
3. Show diff preview before applying
4. Merge new content while preserving user customizations
5. Re-verify via Stage 5

| Section | Merge Strategy |
|---------|---------------|
| Project Identity | Replace with latest |
| Coding Standards | Merge (keep user additions) |
| Critical Rules | Add new, keep existing |
| Skills section | Replace with latest discovery |
| Custom user rules | **Always preserve** |

---

## File Reference

| Path (relative to skill root) | Purpose |
|-------------------------------|---------|
| `scripts/wizard.py` | Interactive preference wizard (Mode A) |
| `scripts/discover-skills.py` | Automated skill discovery (Mode A) |
| `scripts/indexer.py` | Skill catalog indexer (Mode A) |
| `scripts/extract-capabilities.py` | Capability extraction (Mode A) |
| `scripts/lib/design_tokens.py` | Design token parser (Mode A) |
| `scripts/lib/semantic_matcher.py` | Fuzzy + synonym skill matching (Mode A) |
| `scripts/lib/confidence.py` | Confidence score calculation (Mode A) |
| `scripts/validate-output.ps1` | Windows output validator |
| `scripts/validate-output.sh` | Unix output validator |
| `scripts/audit.py` | Audit logging with decision reasoning |
| `scripts/memory_manager.py` | State memory summarizer |
| `references/create-project-rules.md` | Full 934-line reference workflow |
| `assets/templates/rulesrc-template.yaml` | Configuration file schema |
| `assets/templates/mcp_registry.yaml` | MCP intent→tool mapping |
| `assets/i18n/README.md` | Translation patterns |
| `example/` | Sample project with skill sources |

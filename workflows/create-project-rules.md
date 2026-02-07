---
description: Create professional project rules (.cursorrules and AGENTS.md) with skills integration
---

# Create Professional Project Rules

Use this workflow when you need to establish coding standards, AI guidelines, and best practices for a new or existing project.

**Estimated Total Time**: 30-60 minutes (depending on project complexity)

## Prerequisites

Before starting, ensure you have:

- Access to the project's source code
- Understanding of the project's purpose
- `.agent/skills/CATALOG.md` available for skill lookup

---

## Stage 1: Project Analysis

**⏱️ Time: 10-15 minutes**

### 1.1 Understand Project Structure

Analyze the project to gather essential information:

| Aspect           | What to Look For                                                      |
| ---------------- | --------------------------------------------------------------------- |
| **Config Files** | `package.json`, `manifest.json`, `pyproject.toml`, `Cargo.toml`, etc. |
| **Entry Points** | Main files like `index.js`, `main.py`, `App.tsx`                      |
| **Architecture** | Folder structure, component organization, layers                      |
| **Dependencies** | Key libraries and frameworks used                                     |

### 1.2 Identify Tech Stack

Document the following:

- **Primary Language(s)**: JavaScript, TypeScript, Python, etc.
- **Frameworks**: React, Vue, Django, Express, etc.
- **Build Tools**: Webpack, Vite, Rollup, etc.
- **Testing**: Jest, Pytest, Mocha, etc.
- **Styling**: CSS, Tailwind, SCSS, etc.

### 1.3 Understand Design Patterns

Look for patterns already in use:

- Error handling approach
- Async/await patterns
- State management
- API communication
- Authentication flow

---

## Stage 2: Skill Discovery

**⏱️ Time: 5-10 minutes**

> [!IMPORTANT]
> **Skills are constantly updated!** Always check CATALOG.md before proceeding.
> Never rely on memorized skill names as new, better skills may be available.

### 2.1 Search CATALOG.md

Open and search `.agent/skills/CATALOG.md` for:

1. **Language-specific skills** (e.g., `typescript`, `python`, `rust`)
2. **Framework skills** (e.g., `react`, `angular`, `nestjs`)
3. **Project type skills** (e.g., `browser-extension-builder`, `api-design`)
4. **Best practice skills** (e.g., `error-handling-patterns`, `testing-patterns`)

### 2.2 Read Relevant SKILL.md Files

For each relevant skill:

1. Navigate to `.agent/skills/skills/{skill-name}/SKILL.md`
2. Study the best practices and patterns
3. Extract applicable guidelines for the project
4. Note any code examples or patterns to include

### 2.3 Keyword Reference Table

Use these keywords to search CATALOG.md:

| Project Type     | Keywords                                                                 |
| ---------------- | ------------------------------------------------------------------------ |
| Web Frontend     | `react`, `vue`, `angular`, `frontend`, `ui`, `css`, `tailwind`, `nextjs` |
| Backend API      | `api`, `backend`, `rest`, `graphql`, `database`, `sql`, `prisma`         |
| Chrome Extension | `browser`, `extension`, `chrome`, `manifest`                             |
| Mobile App       | `react-native`, `flutter`, `mobile`, `ios`, `android`                    |
| CLI Tool         | `cli`, `terminal`, `bash`, `powershell`                                  |
| AI/ML            | `ai`, `ml`, `llm`, `agent`, `rag`, `prompt`                              |
| Game Dev         | `game`, `unity`, `godot`, `unreal`                                       |

| Category       | Keywords                                                  |
| -------------- | --------------------------------------------------------- |
| Testing        | `testing`, `jest`, `pytest`, `unit`, `integration`, `tdd` |
| Error Handling | `error`, `handling`, `exception`, `sentry`                |
| Code Quality   | `refactor`, `clean`, `audit`, `review`, `production`      |
| Documentation  | `docs`, `documentation`, `readme`, `coauthoring`          |
| Performance    | `performance`, `optimization`, `caching`                  |
| Security       | `security`, `auth`, `oauth`, `jwt`                        |
| DevOps         | `docker`, `ci`, `cd`, `deployment`, `kubernetes`          |
| Architecture   | `architecture`, `monorepo`, `microservices`, `ddd`        |

---

## Stage 3: Create .cursorrules

**⏱️ Time: 10-20 minutes**

Create `.cursorrules` at the project root with these sections:

### 3.1 Required Sections

```markdown
# Project Rules: {PROJECT_NAME}

## Project Overview

- Brief description of the project
- Primary purpose and use case

## Tech Stack

- Language(s):
- Framework(s):
- Build Tools:
- Testing:

## Architecture

### File Structure

(Document key directories and their purposes)

### Component Responsibilities

(Document key files/modules and what they do)

## Coding Standards

### Naming Conventions

(Variable, function, class, file naming rules)

### Code Style

(Formatting preferences, line length, etc.)

### Error Handling

(Required error handling patterns)

### Async Patterns

(How to handle async operations)

## Critical Rules

(Non-negotiable rules that must be followed)

## Code Smells to Avoid

(Anti-patterns and bad practices)

## Testing Guidelines

(Testing requirements and patterns)

## Documentation Standards

(Comment style, JSDoc/docstring requirements)
```

### 3.2 Optional Sections (Add as Needed)

- **Security Considerations**: For apps handling sensitive data
- **Performance Guidelines**: For performance-critical applications
- **Internationalization (i18n)**: For multi-language support
- **Accessibility (a11y)**: For web/mobile applications
- **Git Workflow**: Commit message format, branching strategy
- **Debugging Strategies**: Project-specific debugging tips

### 3.3 Incorporate Best Practices from Skills

For each relevant skill you identified in Stage 2:

1. Extract key patterns and rules
2. Adapt them to your project's context
3. Include code examples where helpful
4. Mark critical rules with emphasis

---

## Stage 4: Create AGENTS.md

**⏱️ Time: 5-10 minutes**

Create `AGENTS.md` at the project root to guide AI assistants.

### 4.1 Skills Section (CRITICAL)

> [!CAUTION]
> **DO NOT hardcode skill names!** Skills are constantly updated.
> Always instruct AIs to check CATALOG.md dynamically.

Include this pattern:

```markdown
## 🎯 Available Skills

> [!IMPORTANT]
> **Skills are constantly updated!** Before any task:
>
> 1. Open `.agent/skills/CATALOG.md`
> 2. Search for skills matching your current task
> 3. Read the relevant `SKILL.md` files
> 4. Follow the best practices described

### How to Find Skills

1. **By keyword search**: Search CATALOG.md for relevant terms
2. **By category**: Browse the categorized skill list
3. **By trigger**: Look at the "Triggers" column for matching keywords

### Helpful Keywords for This Project

(List project-relevant keywords here - NOT skill names)

Examples:

- For Chrome Extension work: `browser`, `extension`, `chrome`, `manifest`
- For error handling: `error`, `handling`, `exception`
- For testing: `testing`, `jest`, `unit`, `tdd`
```

### 4.2 Project Context Section

```markdown
## Project Context

### Overview

(Brief project description)

### Key Files

| File  | Purpose |
| ----- | ------- |
| `...` | ...     |

### Architecture Diagram (Optional)

(ASCII art or mermaid diagram)
```

### 4.3 Common Patterns Section

```markdown
## Common Patterns

### Pattern 1: [Name]

(Description and code example)

### Pattern 2: [Name]

(Description and code example)
```

### 4.4 Important Constraints Section

```markdown
## Important Constraints

### Known Limitations

- ...

### Gotchas

- ...

### Avoid

- ...
```

---

## Stage 5: Verification

**⏱️ Time: 5 minutes**

### 5.1 Checklist

- [ ] `.cursorrules` created at project root
- [ ] `.cursorrules` includes all required sections
- [ ] `.cursorrules` rules match actual project patterns
- [ ] `AGENTS.md` created at project root
- [ ] `AGENTS.md` has Skills section with dynamic lookup instructions
- [ ] `AGENTS.md` does NOT contain hardcoded skill names
- [ ] Both files are well-formatted and readable
- [ ] Examples match the project's coding style

### 5.2 Reader Test

Ask yourself (or a fresh AI):

1. Can an AI reading only `.cursorrules` write correct code?
2. Can an AI reading only `AGENTS.md` find relevant skills?
3. Are the critical rules clearly emphasized?
4. Are there any ambiguous instructions?

### 5.3 Final Review

- Read through both files completely
- Verify all paths and references are correct
- Ensure consistency between the two files
- Check for typos and formatting issues

---

## Example Output (Minimal)

### Example .cursorrules (condensed)

```markdown
# Project Rules: My Chrome Extension

## Project Overview

A Chrome Extension (Manifest V3) that exports NotebookLM chats to PDF.

## Tech Stack

- Language: JavaScript (ES2020+)
- Platform: Chrome Extension (Manifest V3)
- Build: None (vanilla JS)

## Architecture

- `background.js` - Service worker, handles PDF generation
- `content.js` - DOM manipulation, chat parsing
- `popup.html/js` - Extension popup UI

## Coding Standards

### Naming

- Variables/functions: camelCase
- Constants: SCREAMING_SNAKE_CASE
- Files: kebab-case

### Error Handling

Always check `chrome.runtime.lastError` after Chrome API calls:

\`\`\`javascript
chrome.storage.local.get(['key'], (result) => {
if (chrome.runtime.lastError) {
console.error('Storage error:', chrome.runtime.lastError);
return;
}
// proceed with result
});
\`\`\`

## Critical Rules

1. ❌ Never use `localStorage` - use `chrome.storage` instead
2. ❌ Never mutate DOM directly without null checks
3. ✅ Always handle async errors with try/catch
```

### Example AGENTS.md (condensed)

```markdown
# AI Agent Guidelines

## 🎯 Available Skills

> [!IMPORTANT]
> Always check `.agent/skills/CATALOG.md` before starting any task!

### Helpful Keywords

- Extension: `browser`, `extension`, `chrome`, `manifest`
- PDF: `pdf`, `export`, `document`
- Testing: `testing`, `jest`

## Project Context

Chrome Extension for exporting NotebookLM conversations to PDF format.

### Key Files

| File            | Purpose                   |
| --------------- | ------------------------- |
| `background.js` | Service worker, PDF gen   |
| `content.js`    | DOM parsing, UI injection |
| `manifest.json` | Extension configuration   |

## Common Patterns

### Chrome Message Passing

\`\`\`javascript
// Send from content script
chrome.runtime.sendMessage({ action: 'exportPDF', data }, (response) => {
if (chrome.runtime.lastError) {
console.error(chrome.runtime.lastError);
return;
}
// handle response
});
\`\`\`

## Important Constraints

- Must support Manifest V3 (no MV2 patterns)
- Service worker may be terminated - no persistent state
- Content scripts run in isolated world
```

---

## Tips for Effective Rules

### Do's ✅

- **Be specific**: Give concrete examples, not abstract principles
- **Be consistent**: Use the same terminology throughout
- **Be practical**: Focus on rules that prevent real problems
- **Keep updated**: Review and update as the project evolves
- **Use examples**: Show don't tell - code examples are powerful

### Don'ts ❌

- **Don't over-constrain**: Too many rules lead to ignoring them
- **Don't hardcode skill names**: They change over time
- **Don't duplicate**: If it's in .cursorrules, don't repeat in AGENTS.md
- **Don't be vague**: "Write good code" is not actionable
- **Don't forget context**: Rules without context are confusing

---

## Output Files Summary

After completing this workflow, you should have:

1. **`.cursorrules`** (~200-500 lines)
   - Comprehensive coding standards
   - Project-specific patterns
   - Critical rules and anti-patterns

2. **`AGENTS.md`** (~100-200 lines)
   - Dynamic skills reference
   - Project context for AI
   - Common patterns and constraints

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│           CREATE PROJECT RULES - QUICK REF              │
├─────────────────────────────────────────────────────────┤
│ Stage 1: Analyze         │ Config, Tech Stack, Patterns │
│ Stage 2: Skills          │ Search CATALOG.md + Read     │
│ Stage 3: .cursorrules    │ Standards, Rules, Examples   │
│ Stage 4: AGENTS.md       │ Skills section (dynamic!)    │
│ Stage 5: Verify          │ Checklist + Reader Test      │
├─────────────────────────────────────────────────────────┤
│ ⚠️  DO NOT hardcode skill names - always use keywords   │
│ ✅  Include code examples for critical patterns         │
│ ✅  Keep .cursorrules 200-500 lines                     │
│ ✅  Keep AGENTS.md 100-200 lines                        │
└─────────────────────────────────────────────────────────┘
```

---

## Version History

| Version | Date       | Changes                                                                          |
| ------- | ---------- | -------------------------------------------------------------------------------- |
| 1.0     | 2026-02-07 | Initial workflow structure                                                       |
| 1.1     | 2026-02-07 | Added skill integration and verification steps                                   |
| 1.2     | 2026-02-07 | Added time estimates, mini examples, quick reference card, Architecture keywords |

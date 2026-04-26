# Development Log

This directory contains daily development logs for the **AI Project Rules Generator** project.

## Purpose

Development logs act as a structured record of changes, decisions, and progress. They help:

- Track what was done with enough context to explain the change
- Capture decisions so the rationale survives beyond the diff
- Measure progress against the original scope and time estimate
- Debug regressions by tracing when behavior changed
- Hand off context to new contributors or AI agents quickly

## File Naming Convention

```
YYYY-MM-DD.txt
```

Examples: `2026-03-03.txt`, `2026-03-13.txt`, `2026-03-22.txt`

## How to Write a Log Entry

1. Copy `TEMPLATE.txt` into a new file with today's date.
2. Fill in each section while you work.
3. Update the entry throughout the day instead of reconstructing the session at the end.

### Log Structure

Each daily log follows this structure:

| Section | Purpose |
| ------- | ------- |
| **Header** | Date, author, version, session time |
| **Objectives** | What you planned to accomplish |
| **Changes Made** | Detailed record of each change with file paths |
| **Decisions** | Key design or architecture decisions with rationale |
| **Skills Used** | Which AI skills were applied and why |
| **Issues & Blockers** | Problems encountered and their resolution |
| **Testing & Verification** | Commands, checks, and measured outcomes |
| **Next Steps** | What to do in the next session |

### Best Practices

- Do be specific: "Added ordered multi-root discovery" is better than "Updated scripts"
- Do record the why, not just the final diff
- Do include file paths so future reviews can trace the change quickly
- Do note verification commands or measured results when they matter
- Do record version remapping if a release number changes
- Don't paste raw chat logs; summarize the decisions and outcomes
- Don't skip the rationale section

## Files

| File | Description |
| ---- | ----------- |
| `TEMPLATE.txt` | Empty template for new daily logs |
| `YYYY-MM-DD.txt` | Daily development logs |
| `README.md` | This file - logging guidelines |

## Latest Entry

- `2026-04-26.txt` records the workflow accuracy fixes, including source-of-truth file parsing, deep directory scanning, constraint verification, and the pre-write accuracy gate.

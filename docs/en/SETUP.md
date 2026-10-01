# A11Y.md Setup Guide

This guide explains how to properly configure your AI assistant (Cursor, Claude Code, GitHub Copilot, Gemini/Windsurf) to use the `A11Y.md` accessibility standard.

> [!IMPORTANT]  
> **Rule of Thumb:** Your environment setup file should **ONLY** contain a reference pointing to `A11Y.md`. **NEVER** copy or duplicate accessibility rules outside of `A11Y.md` — this prevents rule fragmentation and ensures the AI always loads the complete context.
>
> The reference can point to **this repository's URL** or to a **local copy** — the three ways in are compared below. Portuguese speakers can point to `docs/pt-BR/A11Y.md`.

## Three ways the standard enters a project

| | How | Best when | What you take on |
| :--- | :--- | :--- | :--- |
| **1. Link to upstream** | the rule points at the raw URL on `main` | zero files copied, always the current edition | network at read time; the standard can change under you — pin a tag in the URL (`/v2.2.0/` instead of `/main/`) to freeze it |
| **2. Pinned copy, rule in your agent file** | copy `docs/<lang>/A11Y.md` with `references/` and `templates/` into the repository (`docs/a11y/` is a good home); the rule in `CLAUDE.md`, `.cursorrules` or the equivalent points at the local path | offline work, upgrades reviewed as a diff, teams that clone the repository and must inherit the rules | you own the update: a provenance note with origin commit, version and license, and an upgrade treated like any other reviewed change |
| **3. Pinned copy, rule in `AGENTS.md`** | the same copy, with the rule in a tool-neutral `AGENTS.md` instead of a `CLAUDE.md` you do not own | the `CLAUDE.md` belongs to another workflow, or several agents read the repository | two instruction files to keep coherent: `CLAUDE.md` says how the project works, `AGENTS.md` says the accessibility rule |

Whichever door: the rule is **one line**, and the accessibility rules themselves live only in `A11Y.md`. With a copy, `REPORT.md` records the *Standard version* from the copy's own *Version* line, and `tools/verify-a11y.py` can sit beside it so the gate runs offline. *(The three options as an adopting team's agent laid them out to its author before a review, 2026-09-29 — the author chose the third.)*

## Quick Reference

| Environment | Configuration File | Location |
| :--- | :--- | :--- |
| **Cursor** | `.mdc` rule file | `.cursor/rules/a11y.mdc` |
| **Claude Code** | `CLAUDE.md` reference | `CLAUDE.md` (root) |
| **GitHub Copilot** | Instructions file | `.github/copilot-instructions.md` |
| **Gemini / Antigravity**| `AGENTS.md` rule | `AGENTS.md` or `.agents/AGENTS.md` |
| **Windsurf** | Rules directory | `.windsurf/rules/a11y.md` |

---

## 1. Cursor
Create a `.mdc` file inside the `.cursor/rules/` directory.

**File:** `.cursor/rules/a11y.mdc`
```yaml
---
description: "Persistent accessibility context — delegates all rules to A11Y.md"
alwaysApply: true
---
Follow strictly the accessibility rules in the file <path or URL to your A11Y.md — e.g. https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/en/A11Y.md, or a local copy>.
```
> [!NOTE]  
> `alwaysApply: true` is crucial. Accessibility is a strict precondition for all UI code and must not rely on glob patterns to be activated.

## 2. Claude Code
Add a section to your root `CLAUDE.md` file.

**File:** `CLAUDE.md`
```markdown
## Accessibility
Follow strictly the accessibility rules in the file <path or URL to your A11Y.md — e.g. https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/en/A11Y.md, or a local copy>.
```

## 3. GitHub Copilot
Add the instruction to Copilot's custom instructions file.

**File:** `.github/copilot-instructions.md`
```markdown
## Accessibility
Follow strictly the accessibility rules in the file <path or URL to your A11Y.md — e.g. https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/en/A11Y.md, or a local copy>.
```

## 4. Gemini / Antigravity
Add the instruction to the agent rules file.

**File:** `AGENTS.md` or `.agents/AGENTS.md`
```markdown
Follow strictly the accessibility rules in the file <path or URL to your A11Y.md — e.g. https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/en/A11Y.md, or a local copy>.
```

## 5. Windsurf
Create a rule file in the Windsurf rules directory.

**File:** `.windsurf/rules/a11y.md`
```markdown
Follow strictly the accessibility rules in the file <path or URL to your A11Y.md — e.g. https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/en/A11Y.md, or a local copy>.
```

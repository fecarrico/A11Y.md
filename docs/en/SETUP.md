# A11Y.md Setup Guide

This guide explains how to properly configure your AI assistant (Cursor, Claude Code, GitHub Copilot, Gemini/Windsurf) to use the `A11Y.md` accessibility standard.

> [!IMPORTANT]  
> **Rule of Thumb:** Your environment setup file should **ONLY** contain a reference pointing to `A11Y.md`. **NEVER** copy or duplicate accessibility rules outside of `A11Y.md` — this prevents rule fragmentation and ensures the AI always loads the complete context.
>
> The reference can point to **this repository's URL** (always up to date, zero files copied — the recommended default) or to a **local copy** (offline/pinned). Portuguese speakers can point to `docs/pt-BR/A11Y.md`.

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
Follow strictly the accessibility rules defined in the file <path or URL to your A11Y.md — e.g. https://github.com/fecarrico/A11Y.md/blob/main/docs/en/A11Y.md, or a local copy>.
```
> [!NOTE]  
> `alwaysApply: true` is crucial. Accessibility is a strict precondition for all UI code and must not rely on glob patterns to be activated.

## 2. Claude Code
Add a section to your root `CLAUDE.md` file.

**File:** `CLAUDE.md`
```markdown
## Accessibility
Follow strictly the accessibility rules defined in the file <path or URL to your A11Y.md — e.g. https://github.com/fecarrico/A11Y.md/blob/main/docs/en/A11Y.md, or a local copy>.
```

## 3. GitHub Copilot
Add the instruction to Copilot's custom instructions file.

**File:** `.github/copilot-instructions.md`
```markdown
## Accessibility
Follow strictly the accessibility rules defined in the file <path or URL to your A11Y.md — e.g. https://github.com/fecarrico/A11Y.md/blob/main/docs/en/A11Y.md, or a local copy>.
```

## 4. Gemini / Antigravity
Add the instruction to the agent rules file.

**File:** `AGENTS.md` or `.agents/AGENTS.md`
```markdown
Follow strictly the accessibility rules defined in the file <path or URL to your A11Y.md — e.g. https://github.com/fecarrico/A11Y.md/blob/main/docs/en/A11Y.md, or a local copy>.
```

## 5. Windsurf
Create a rule file in the Windsurf rules directory.

**File:** `.windsurf/rules/a11y.md`
```markdown
Follow strictly the accessibility rules defined in the file <path or URL to your A11Y.md — e.g. https://github.com/fecarrico/A11Y.md/blob/main/docs/en/A11Y.md, or a local copy>.
```

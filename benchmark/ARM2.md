# Arm 2 — the ecological check, declared before it runs

> The registered protocol ([osf.io/pg6r5](https://osf.io/pg6r5), METHODOLOGY.md §Arms) reserves a small ecological arm: *"a small-n check that the Arm 1 effect direction survives in a real coding agent with a real filesystem: conditions A and D only, a task subset, `n=3`. Reported descriptively; no hypothesis test."* This file fixes everything the registration left open — before the first run, dated, in the repository.

## What this arm is for

Arm 1 simulates lazy loading with a single scoped tool over a raw API. Arm 2 runs the standard **the way an adopter actually uses it**: a project directory, the Quick Start rule in `CLAUDE.md`, a real coding agent (Claude Code, official client, subscription) reading files from disk with its own tools, system prompt and habits. It answers one question, descriptively: *does the effect direction seen in Arm 1 survive contact with a real agent?*

## Fixed design

| | |
|---|---|
| Agent | Claude Code CLI (version recorded per run), non-interactive `claude -p`, official scripting mode |
| Conditions | **A** (bare workspace) · **D** (standard on disk + Quick Start rule) |
| Tasks | `signup-form` · `destructive-confirmation-modal` · `dashboard-chart` — the same frozen prompts, verbatim, chosen to span a light (~1.7k chars), mid (~3.1k) and heavy (~7.7k) reference guide |
| Repetitions | 3 per cell → **18 runs**, each in a fresh workspace, each a fresh session |
| Model | whatever the subscription session serves; the response JSON records it per run |

## Workspaces

- **Condition A:** an empty directory. The task prompt is the only input.
- **Condition D:** the directory contains `A11Y.md`, `references/` and `templates/` copied from `docs/en/` at the current commit, plus a `CLAUDE.md` holding the Quick Start rule, verbatim, pointed at the local copy:

  > `When developing the frontend, follow strictly the accessibility rules defined in A11Y.md: ./A11Y.md`

  Nothing else. No hint about lazy loading, no file list — the agent discovers the standard's mechanics by reading it, or does not.

## Invocation

```
claude -p "<task prompt, verbatim>" --output-format json --permission-mode acceptEdits
```

run from inside the workspace, with a 40-minute wall clock per run. `acceptEdits` lets the agent write files without interactive approval; everything else stays at the product's defaults.

> **Amendment, 2026-08-16 (before any retained D run):** the clock was declared at 20 minutes and calibrated blind. The first condition-D run exceeded it — not stalled, but **following the standard in full**: alongside the page it generated `REPORT.md` and `A11Y-DECISIONS.md` unprompted, exactly as the standard's Release Evidence rule mandates, and 20 minutes was not enough to finish. The clock is now 40 minutes, symmetric across conditions; the timed-out run re-collects. The behaviour itself — a real agent producing the lifecycle artifacts nobody asked for — is an ecological observation in its own right and will be reported.

## The environment is real, and that is declared, not sanitized

Claude Code loads the developer's user-level configuration (global `CLAUDE.md`, settings, MCP servers) in every session. This arm **does not strip it**: the adopter's real environment includes their global config, and it applies identically to both conditions. What would be a contamination in Arm 1 is the object of measurement here. The one asymmetry that matters — the presence of the standard and its rule — is the condition itself.

## What is captured

Per run: every file the agent created (the seeded standard files are excluded by manifest), the largest HTML artifact (with locally-referenced CSS/JS inlined mechanically, the assembly rule the runbook already allows), the full `claude -p` response JSON verbatim (model, usage, reported cost), wall-clock duration, and the agent version. A run that produces no HTML is logged as such — that is data, not failure.

## Second agent — Codex CLI (added 2026-08-17, before its first run)

The arm extends to a second real agent under the same design: same three tasks, same conditions, same `n=3`, same 40-minute clock, same capture. What changes is only what the product itself changes:

- **Client:** Codex CLI (version recorded per run), official non-interactive mode `codex exec`, authenticated by ChatGPT subscription sign-in — the product's documented path.
- **Rule file:** condition D's rule goes in `AGENTS.md` — the config file Codex reads, and one the standard's own Quick Start already names.
- **The one concession, translated:** `--sandbox workspace-write` (file writes without interactive approval — Codex's equivalent of `acceptEdits`) plus `--skip-git-repo-check` (the workspace is a fresh directory, not a git repository). `--json` streams the client's events, kept verbatim; token figures in them are client-reported and labeled as such.
- **Quota:** the subscription tier's Codex allowance is the lightest sold; if a wave hits it, collection resumes in the next window — the same discipline as the primary arm's daily caps.

Two agents do not make a model comparison and none will be drawn: each agent is reported against its own baseline (its condition A), descriptively, like everything else in this arm.

### Capture notes (running log)

- **2026-08-16, `claude-code__destructive-confirmation-modal__A__run2`:** the agent built the page but wrote it to its session scratchpad and attempted to publish it as a chat artifact instead of writing to the workspace. The file was recovered mechanically from the path named in the response JSON (kept under `runs/arm2/recovered/`, copied into the capture set). Observation worth reporting: every condition-D run anchored its output in the project directory; condition-A runs occasionally treated the task as chat. The standard appears to give the agent a sense of *place*.

## What will and will not be claimed

Outputs are scored by the same pinned harness as Arm 1 and reported **descriptively, next to — never pooled with — the primary arm**. Eighteen runs support statements shaped like "the direction held" or "it did not"; they support no p-value and none will be computed. Token figures from this arm are *reported-by-the-client* numbers, not API-metered ones, and are labeled accordingly.

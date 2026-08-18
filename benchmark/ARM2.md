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

**Environment contents, on record (2026-08-18):** the user-global `CLAUDE.md`
on the collection machine contains zero accessibility-related content, and
workspaces are created under the system temp directory, outside any repository
— no project-level agent config applies to any run.

## What is captured

Per run: every file the agent created (the seeded standard files are excluded by manifest), the largest HTML artifact (with locally-referenced CSS/JS inlined mechanically, the assembly rule the runbook already allows), the full `claude -p` response JSON verbatim (model, usage, reported cost), wall-clock duration, and the agent version. A run that produces no HTML is logged as such — that is data, not failure.

## Second agent — Codex CLI (added 2026-08-17, before its first run)

The arm extends to a second real agent under the same design: same three tasks, same conditions, same `n=3`, same 40-minute clock, same capture. What changes is only what the product itself changes:

- **Client:** Codex CLI (version recorded per run), official non-interactive mode `codex exec`, authenticated by ChatGPT subscription sign-in — the product's documented path.
- **Rule file:** condition D's rule goes in `AGENTS.md` — the config file Codex reads, and one the standard's own Quick Start already names.
- **The one concession, translated:** `--sandbox workspace-write` (file writes without interactive approval — Codex's equivalent of `acceptEdits`) plus `--skip-git-repo-check` (the workspace is a fresh directory, not a git repository). `--json` streams the client's events, kept verbatim; token figures in them are client-reported and labeled as such.
- **Quota:** the subscription tier's Codex allowance is the lightest sold; if a wave hits it, collection resumes in the next window — the same discipline as the primary arm's daily caps.

Two agents do not make a model comparison and none will be drawn: each agent is reported against its own baseline (its condition A), descriptively, like everything else in this arm.

## Third agent — Antigravity CLI (declared 2026-08-18, before its first run)

Added after the primary-arm results were final, at the prompting of an external
methodological review — see the dated `DEVIATIONS.md` entry, which also records
the motivation and the probes. Same tasks, same conditions, same n, same clock.

- **Client:** `agy` (Antigravity CLI, official Google client), version logged
  per run (1.1.14 at declaration). Included in the author's existing Google AI
  Pro subscription — $0 marginal, the criterion that qualified the other two.
- **Model / effort:** `--model gemini-3.5-flash`, `--effort low`, fixed across
  conditions. `agy models` does not offer `gemini-3.5-flash-lite`, so this cell
  is **same family, adjacent tier** relative to Arm 1 — it narrows the
  harness×model confound; it does not close it. The strict closure remains
  Arm 1-ext, conditional on credits.
- **Rule delivery:** empirical test (2026-08-18, two marker runs, plain dir and
  git repo) shows print mode reads neither `AGENTS.md` nor `GEMINI.md`.
  Condition D therefore ships the standard on disk plus the **verbatim Quick
  Start rule as a prompt preamble** — the same sentence the other agents read
  from their rule files, delivered the way Arm 1 delivers its grounding. This
  makes the cell a declared bridge between the arms, not a mirror of the other
  two agents. Condition A gets the bare task prompt.
- **Invocation:** `agy -p <prompt> --model gemini-3.5-flash --effort low
  --output-format json --mode accept-edits --print-timeout 40m`, cwd = the
  workspace. `--mode accept-edits` is the single concession (file writes
  without interactive approval), symmetric with the other agents. Capture is
  one JSON object (`status`, `response`, `duration_seconds`, `num_turns`,
  `usage`) — recorded as reported, labeled as the client's own accounting.

**Amendment (2026-08-18, before any retained run) — fresh profile required.**
The first collection attempt was aborted after two failed runs: the product's
persistent profile memory carried the standard into a bare-condition session
(condition A citing A11Y.md unprompted — full account in `DEVIATIONS.md`).
The cell therefore collects under a fresh OS profile (`HOME` at an empty
directory, one-time auth) with `--new-project` per run, gated on a
clean-profile probe that must show no ambient knowledge of the standard.
If the probe fails, the extension is abandoned and documented.

**Amendment — the arm's honest formulation (2026-08-18).** With no cell shared
with Arm 1, this arm does not "check that the Arm 1 effect survives a real
agent". What it shows is: *an independent demonstration, in real agents, that
the standard produces an effect in the same direction — in models the primary
arm never touched, with harness and model changing together.* That weaker
sentence is what the data support, and it is the one the report will use.

### Capture notes (running log)

- **2026-08-18 · Antigravity collected (fresh profile).** 18/18 runs, zero
  failures, after the clean-profile gate passed (both probes archived under
  `runs/arm2/probes/`). Third vendor, same emergence: REPORT.md in 9/9
  condition-D runs, A11Y-DECISIONS.md in 8/9, zero in condition A. Median
  durations 15 s (A) vs 42 s (D). The single non-zero D page
  (`dashboard-chart`, run 2) carries one rule — `aria-prohibited-attr` —
  twelve times: ARIA over-applied where it is prohibited, a systematic error
  correctable in one fix. Logged here because it is precisely the
  error-topology phenomenon Study 2 registers as an outcome.


- **2026-08-16, `claude-code__destructive-confirmation-modal__A__run2`:** the agent built the page but wrote it to its session scratchpad and attempted to publish it as a chat artifact instead of writing to the workspace. The file was recovered mechanically from the path named in the response JSON (kept under `runs/arm2/recovered/`, copied into the capture set). Observation worth reporting: every condition-D run anchored its output in the project directory; condition-A runs occasionally treated the task as chat. The standard appears to give the agent a sense of *place*.

## What will and will not be claimed

Outputs are scored by the same pinned harness as Arm 1 and reported **descriptively, next to — never pooled with — the primary arm**. Eighteen runs support statements shaped like "the direction held" or "it did not"; they support no p-value and none will be computed. Token figures from this arm are *reported-by-the-client* numbers, not API-metered ones, and are labeled accordingly.

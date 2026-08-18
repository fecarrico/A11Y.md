# Benchmark Runbook — collecting the 54 generations

> **Historical document — do not follow.** This runbook describes the v1
> design (54 hand-collected generations, conditions `bare | grounded`, models
> `claude | gemini | gpt`), which no longer exists. The registered v2 protocol
> ([osf.io/pg6r5](https://osf.io/pg6r5)) collects Arm 1 with
> [`collect.py`](collect.py) and Arm 2 with [`arm2.py`](arm2.py); every rule
> that survived v1 lives in [`METHODOLOGY.md`](METHODOLOGY.md) and
> [`ARM2.md`](ARM2.md). This file is kept for provenance only.

> Companion to [`METHODOLOGY.md`](METHODOLOGY.md). The methodology says *what* is measured and why; this file says *how to physically collect and measure*, so a run session needs no decisions — decisions made mid-collection are how bias enters a benchmark.

## One-time setup

```bash
python3 harness/fetch-axe.py     # vendors the pinned axe build, SHA-256 verified against axe.lock
```

## Collecting one cell

1. **Fresh session** in the model's consumer chat interface (new chat, default settings, no custom instructions, no memory of previous cells — if the product has a memory feature, it must be off).
2. Paste the prompt **verbatim from [`PROMPTS.md`](PROMPTS.md)**:
   - **Condition A (bare):** the task prompt alone.
   - **Condition B (grounded):** the full current `docs/en/A11Y.md`, then the line *"Follow strictly the accessibility rules defined in the A11Y.md above."*, then the task prompt. Nothing else.
3. If the model asks a clarifying question (including the profile question the standard tells it to ask), reply exactly: **"Use your defaults."** — and note it in the log. No other conversation.
4. Save the complete generated page as **one `.html` file, unmodified** — no formatting, no fixing, no completing truncated output. If the model split HTML/CSS/JS into separate blocks, assemble them in the order given into one file (that is mechanical assembly, not editing). If the output is truncated, say "continue" once; if still unusable, log the cell as failed and re-run in a new session.
5. Name and place it by the convention — this is what the manifest builder parses:

   ```
   runs/<model>/<task>/<condition>/run<N>.html
   model ∈ claude | gemini | gpt · task ∈ task1 | task2 | task3 · condition ∈ bare | grounded · N ∈ 1 | 2 | 3
   ```

6. Append one line to `runs/log.csv`:

   ```csv
   file,model_version_as_displayed,date,notes
   claude/task1/bare/run1.html,Claude Opus 4.6,2026-08-16,
   ```

## Order of collection

Alternate conditions rather than collecting all of one condition first (A run 1, B run 1, A run 2 …), and spread the three runs of a cell across sessions or days where practical — consumer interfaces drift, and interleaving keeps the drift from loading one condition.

## Measuring

```bash
python3 run-benchmark.py         # builds the manifest, serves the harness, opens the browser
```

Click **Run all** — the harness mounts every run unmodified in an iframe, runs the pinned axe plus the pre-registered checklist, and renders the table. Then **Download results.json** and save it under `results/` (create the folder on first use; results are committed — raw outputs and numbers are part of the publication).

```bash
python3 run-benchmark.py --analyze results/results.json
```

prints the completeness check against the 54-cell design and the pre-registered analysis: median critical+serious per model and condition, share of zero-critical runs, checklist pass-rate.

## What the harness cannot judge (logged as MANUAL, resolved by a human)

- **Modal containment and focus return** (task 2): the harness drives open/Escape automatically, but a human tab-through confirms the trap and the return to the trigger.
- **Target-size exceptions** (SC 2.5.8 allows inline targets and equivalent-alternative cases) — the harness measures raw size; the exception is a judgment.

Record human resolutions in the notes column of `runs/log.csv`. These do not enter the primary outcome (which is axe-only, per the methodology); they enter the checklist pass-rate with the resolution applied.

## Deviations

Anything that departs from `METHODOLOGY.md` — a model that refuses a task, an interface that forces a setting, a cell collected twice — gets a line in `DEVIATIONS.md` (create on first use). Deviations are documented, never hidden; that is the entire point of pre-registering.

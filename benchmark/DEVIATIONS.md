# Deviations from the pre-registered protocol

> Every departure from [`METHODOLOGY.md`](METHODOLOGY.md) as registered ([osf.io/pg6r5](https://osf.io/pg6r5)), dated, with what changed and why. Deviations are documented, never hidden — that is the entire point of pre-registering. Newest first.

---

## 2026-08-23 — SC 2.5.8 adjudication: the registered machine/human split, applied

- **Registered text:** MANUAL checklist items are *"automated where a scripted
  browser can decide them; the remainder adjudicated by a human."*
- **What ran:** `verify/target-prepass.js` measured every visible interactive
  target on the 60 blind-sampled pages (Playwright, 1280×900). "No target
  below 24×24 CSS px exists" is machine-decidable: **41 of 52 target-size rows
  closed mechanically as N-A**, each stamped as such in the worksheet's
  observation column. The 11 pages that do contain sub-24px targets go to the
  human adjudicator with a factual measurement report
  (`adjudicacao-alvos-pequenos.md` — shapes, counts, examples); the exception
  judgments the SC delegates to a person (equivalent control, inline,
  essential) remain human, exactly as registered.
- **Blinding intact:** the script sees content hashes, never conditions; the
  sealed map stays sealed. Modal-focus rows are untouched — keyboard
  interaction with focus-return judgment stays with the adjudicator.

## 2026-08-18 — Antigravity: first attempt aborted; ambient-memory contamination found; fresh profile required

- **What happened:** the first two runs (signup-form, conditions A and D, run 1) ended `status=ERROR` with zero files created — and their transcripts show something worse than a flag problem: **condition A went looking for A11Y.md.** The agent resolved paths inside the author's repository and cited the standard, WCAG 2.2 AA and the author's own UX rules — in a fresh workspace, on a bare task prompt that carried no rule at all.
- **Where it comes from:** Antigravity keeps persistent profile-level memory and product-level rules. A follow-up probe **with `--new-project`** (outside the dataset) still described a brand-new empty directory as "structured around accessibility guidelines (A11y)" and cited `docs/en/A11Y.md` by path. On the standard author's machine the standard is *ambient* — the product carries it into sessions that never asked for it. An A cell collected in that profile would not be an A cell.
- **Why this differs from the other agents:** the audit entry below documents that the live profile's global agent config contains zero accessibility content for Claude Code and Codex — running them in the live environment is "declared, not sanitized" working as intended. For Antigravity the live environment contains **the treatment itself**; that philosophy cannot cover it.
- **Declared remedy (before any retained run):** the Antigravity cell collects under a **fresh OS profile** — `HOME` pointed at an empty directory, one-time authentication, locally verified to isolate profile state — with `--new-project` added to every invocation. The asymmetry with the other two agents is declared here. **Gate:** a clean-profile probe must answer "what do you know about this project?" without referencing the standard; if ambient knowledge survives a fresh profile (server-side memory), the extension is **abandoned, and this entry closes with that outcome** — a declared, unexecuted extension with its reason on record.
- **Data handling:** the two ERROR runs stay in the collection log as failed records (precedent: the truncated Arm 1 cell). Nothing was produced, nothing is retained; `--resume` recollects them under the fixed invocation.

## 2026-08-18 — Third agent for the ecological arm: Antigravity CLI (declared before any run; motivated by results)

- **What is added:** a third agent in Arm 2 — the Antigravity CLI (`agy`), official Google client, included in the author's existing Google AI Pro subscription ($0 marginal, the same criterion that qualified Claude Code and Codex). Same three tasks, same conditions A and D, same n=3, same 40-minute clock: 18 runs.
- **Why, stated plainly:** an external methodological review of the (unpublished) report flagged that Arms 1 and 2 change two variables at once — harness *and* model family — with no shared cell. This addition was decided **after the primary-arm results were final**, and is disclosed as such. The principle that makes it defensible: it creates a new opportunity for the effect to *fail* in a third harness, not a new opportunity for it to succeed. Whatever it shows goes in the report.
- **What the probe found (2026-08-18, outside the dataset):** `agy models` does **not** list `gemini-3.5-flash-lite`, the primary arm's model. Nearest available: Gemini 3.5 Flash. **This cell therefore does not close the harness×model confound — it narrows it** ("same family, adjacent tier"). The strict closure remains Arm 1-ext (the same API protocol on the ecological agents' models), still conditional on research credits.
- **Rule-file test (2026-08-18, outside the dataset):** two marker runs (one in a plain directory, one in a git repository) show the CLI reads **neither `AGENTS.md` nor `GEMINI.md`** in print mode — input token counts unchanged with the files present, marker instructions not followed. Condition D therefore delivers the rule as a **prompt preamble**: the same verbatim Quick Start sentence the rule files carry, with the standard on disk. This makes the cell a declared bridge to Arm 1 (same delivery mechanism, real agent harness) rather than a mirror of the other two agents.
- **Pins:** model `gemini-3.5-flash`; `--effort low` (the flag is a new degree of freedom the other agents do not expose — fixed identically across conditions, chosen as the closest available neighbour to the Lite tier's cost profile); `--mode accept-edits` (the single concession, symmetric with the other agents); `--output-format json`; `--print-timeout 40m`; version logged per run (`agy` 1.1.14 at declaration time).
- **Discipline:** this entry and the matching `ARM2.md` section are committed **before the first retained run**. Collection starts only after merge.

## 2026-08-18 — Repository audit after external review (clarifications; no protocol change)

An independent methodological review of the draft report prompted an audit of verifiable claims. Findings, recorded so they are answered before they are asked:

- **Two OSF IDs:** `osf.io/s2ntw` is the OSF **project**; `osf.io/pg6r5` is the **registration** inside it. The commit that opened collection (`0b37456`) carries the project ID in its title; git history is immutable, so this note is the correction. Every normative file points to the registration.
- **Tool-call ceiling was never reached:** across all retained primary-arm generations the maximum observed is **11 tool calls** (two condition-C generations); the operative ceiling was 12. No generation's loading behaviour was truncated by the instrument.
- **Collector defaults vs. operative invocation:** the frozen `collect.py` still carries v1 defaults (`--conditions A,B,D`, `--runs 3`, ceiling 6). They were overridden in every wave; the operative invocation is logged in the collection pipeline: `--conditions A,B,C,D --runs 10 --max-tool-calls 12`. Defaults were left untouched because the file's hash is part of the registered snapshot.
- **Arm 2 environment, documented:** the user-global `CLAUDE.md` on the collection machine contains **zero accessibility-related content** (checked by keyword sweep), and Arm 2 workspaces were created under the system temp directory, **outside any repository** — no project-level agent config applied to any run. The "declared, not sanitized" clause now has its contents on record.
- **`RUNBOOK.md` marked historical:** it describes the superseded v1 design and now says so unambiguously at the top.

## 2026-08-18 — Confirmatory model operationalized with task fixed effects

- **Registered text:** "negative-binomial mixed regression, violations ~ condition + (1 | task)" — random intercepts per task.
- **What happened:** the analysis stack (statsmodels) offers no frequentist negative-binomial mixed model. With ten task levels, the standard operationalizations are task **fixed effects** or **cluster-robust errors by task**. Both were fit and both are reported: fixed effects as primary, cluster-robust as sensitivity. Where they diverge (D vs A: significant under fixed effects, borderline under cluster-robust), the divergence is reported, not resolved by choosing.
- **Timing caveat, stated plainly:** the operationalization was decided after the robustness-track descriptives (pre-registered as computable pre-model) had been seen. The choice was constrained by software, not by results — but the sequence is disclosed so readers can weigh it.
- **Scripts:** `analysis/confirmatory.py`, environment frozen in `analysis/requirements.txt`, dispersion α profiled by grid (≈3.15), seed-free (the model is deterministic given data).

## 2026-08-16 — Tool-call ceiling raised 6 → 12 via runtime flag; one truncated cell re-collected

- **What happened:** generation 7 of the first retained wave (`destructive-confirmation-modal`, condition C, run 1) requested a seventh file read; the collector's default `--max-tool-calls 6` cut the loop and the generation ended with **zero output characters** — seven quota calls spent on an unusable cell.
- **Response:** the wave was stopped at generation 11, the truncated cell's artifacts were deleted, and collection resumed with `--max-tool-calls 12` on the command line. The frozen `collect.py` is untouched — the ceiling is a documented runtime flag, and the default in the file still reads 6 — but the operative value changed mid-collection, which is exactly the kind of thing this log exists to record.
- **Data handling:** the truncated cell re-collects under `--resume` (its deletion makes it pending again). Its first, truncated attempt remains in the collection log as a failed record; analysis reads generations from disk and never pools zero-output artifacts.
- **Why 12:** the pilot's condition-D generation read 6 files; the control's lazy map plus its three templates make 7+ reads a legitimate path, not a runaway. Twelve bounds a runaway loop at roughly twice the observed legitimate maximum.

## 2026-08-16 — Primary-arm model finalized as `gemini-3.5-flash-lite` after a quota wall

- **Registered text:** Arm 1 is "Gemini API, free tier (current Flash-class model; exact model string and version recorded per call)" — the registration deliberately did not pin a model string.
- **What happened:** the first collection wave started on `gemini-3.6-flash` and hit its free-tier quota at 20 requests/day (AI Studio per-model table; every full-Flash model carries the same 20/day cap). The full design needs ~1,300 calls — two months at that cap. The Lite tier allows 500/day. The arm restarts on **`gemini-3.5-flash-lite`** (current stable Lite, 15 RPM / 500 RPD), verified working with the tool loop via `--probe` before this entry.
- **Data handling:** 3 generations had been collected on `gemini-3.6-flash` (signup-form A, B, C of run 1). They are set aside under `runs/aside-gemini-3.6-flash/` as exploratory material and are **never pooled** with the primary arm. The primary arm's log starts clean.
- **Effect on interpretation:** none beyond what the registration already declared — the model string is recorded per call and named in any report title. A Lite-class model arguably makes the test *harder* for the standard, not easier: smaller models depend more on the quality of their context.

## 2026-08-16 — Collector reordered to interleave conditions (before any retained generation)

- **Registered text:** METHODOLOGY.md §Size — "waves are collected on consecutive days with conditions interleaved (never one condition's block on one day — interface drift must not load onto a condition)."
- **What happened:** the frozen `collect.py` (SHA-256 `258cbfab…` in the registration) built its job list task → condition → run, which collects condition blocks — contradicting the registered text. Caught on the pre-collection `--plan` inspection; the job order now cycles every condition within each task before any condition repeats, runs outermost.
- **Why it is a deviation and not an edit:** the collector's hash is part of the registered snapshot, so any change to it is logged here, even one that *restores* compliance with the registered methodology. The methodology text is normative; the instrument answers to it.
- **Timing:** zero generations had been collected under the frozen ordering.

## 2026-08-16 — Protocol tag is annotated, not GPG-signed

- **Registered text:** "The repository tag marking the frozen protocol is signed."
- **What happened:** no GPG signing key is configured on the collection machine; the tag `benchmark-protocol-v2.0` was created annotated but unsigned.
- **Why it does not weaken the freeze:** the tamper-evident anchor was never the tag — it is the OSF registration itself, which is immutable, timestamped by a third party, and carries the SHA-256 of every frozen file. The tag is a repository-side convenience pointer to the same tree.
- **Remedy if it matters later:** a signed tag can be added over the same commit once a key exists; the hashes in the registration make any rewrite detectable either way.

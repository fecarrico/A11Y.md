# Round 2 — the v2.0.0 audit (v1.8.0 × v2.0.0)

> **DRAFT — not frozen, not registered.** This document follows the order of
> operations Study 2 established: pilot (discarded) → ruler v2 frozen by hash →
> OSF registration (its own registration) → collection. Nothing here binds
> until the freeze; everything after the freeze binds via `DEVIATIONS.md`.

## Why this round exists

v2.0.0 was built from Study 2's findings and carries three public commitments
([CHANGELOG](../../CHANGELOG.md), the published report):

1. **Non-regression of the diet.** The release cut ~56 KB across the corpus in
   two declared bands while *adding* 9 obligations (62 → 71 per edition). The
   honest arithmetic (measured by `git ls-tree` between tags): −35.7 KB shrunk
   in pre-existing files, +10.2 KB grown, +15.8 KB in new guides, −4.5 KB
   deleted — **net corpus −9.7 KB, core +605 B**. The hypothesis to refute is
   therefore not "less context, worse output"; it is **"adherence to the old
   obligations fell during the rewrite"**. The outcome is per-obligation, not
   volume.
2. **The kill criterion.** Study 2's one half-climbed ARIA ladder
   (`antigravity__journey__D__run3`: `aria-required-parent` 49 nodes +
   `listitem` 49 + `aria-required-children` 7, one mold replicated across all
   7 screens) must **disappear as a class**, not be patched per case.
3. **The contrast bet.** Contrast failed in every uninstructed condition of
   Study 2 and survived in 3 of 5 guided journeys. v2.0.0 moved contrast from
   model reasoning to a deterministic protocol (computed-never-estimated,
   palette-definition trigger). This round measures whether the bet paid.

Study 1's `METHODOLOGY.md` §exploratory declared "Version delta — same tasks
against a prior release of the standard" as an exploratory outcome. **This
round promotes that outcome to primary**, and the registration must say so,
citing the precedent.

## Design

- **Unit:** the frozen `bookstore-journey` (7 screens, one session, one
  agent), prompt verbatim from [`../study2/PROMPTS.md`](../study2/PROMPTS.md).
  Unchanged, for direct comparability with Round 1's 30 runs.
- **Conditions (4):**
  - **A** — bare (no instruction)
  - **B** — generic (`Make it accessible.` prepended)
  - **D18** — the standard at tag `v1.8.0`
  - **D20** — the standard at tag `v2.0.0`
  - No placebo, per Study 2's registered rationale (the placebo question is
    answered; a journey costs hours). The slug keeps Study 2's 4-field shape
    (`agent__journey__COND__runN`) so `run.py --resume`, `log.jsonl` and
    `analyze.py` survive with label changes only.
- **Workspace freezing:** condition workspaces are built from
  `git archive <tag> -- docs/en`, never from the working tree. The
  registration records, per condition, the SHA-256 of the archive's files
  **concatenated in path order** — the same idiom Study 1 used for
  `control-standard/`.
- **Agents (2):** Claude Code and Antigravity, versions named at registration
  (Round 1's clients no longer exist at those versions; Round 1 data is
  context, never a pooled arm). Codex quota resets 2026-09-16; whether it
  enters as a third agent is an **open question** below.
- **n:** 5 per cell → `5 × 4 × 2 = 40 runs`. Cut rule inherited: if 40 proves
  infeasible, agents are cut before repetitions.
- **Clock:** 90 min per run, symmetric, inherited from Study 2's calibration.
- **Blinding:** screen HTML renamed by hash with a sealed map before any human
  look; governance artifacts counted by script, never read before adjudication.

## Outcomes and the declared hierarchy (the ruler-v2 commitment)

Study 2 published five rulers but ranked them post-hoc. Round 2 declares the
hierarchy **before** collection, with the judge named per ruler:

| # | Ruler | Serves | Judge | Status in code |
| - | ----- | ------ | ----- | -------------- |
| 1 | **Screens with error** (screen×error pairs) | the person navigating | axe (frozen) + script | to be frozen (was post-hoc) |
| 2 | **Wrong decisions** (distinct error decisions) | the maintainer fixing | script over `verify/*.jsonl` | to be frozen (was hand-derived) |
| 3 | **Clean journeys** (whole sites, zero violations) | the team shipping | script | to be frozen (was post-hoc) |
| 4 | **Consistency v2** (see below) | the person relearning each screen | `classifier-v2.py` (frozen by hash) | to be built |
| 5 | **Flagged elements** (raw node count) | the auditor | axe | frozen since Round 1 |

Primary contrast: **D20 vs D18** on rulers 1–4. Secondary: D20 vs B, D20 vs A.
Statistics inherited: seeded bootstrap (B=10,000), Cliff's delta, no p-values,
never pooled across agents.

### Per-obligation non-regression panel (commitment 1)

The floor is what Round 1 already banked, checked per class, per condition:

- `image-alt` and `label` classes: **zero across all D20 journeys** (Round 1
  zeroed them in D; they must stay zero).
- `color-contrast`: Round 1 had it in 3 of 5 D journeys — under the v2.0.0
  deterministic protocol the target is **fewer affected journeys than D18**,
  measured same-agent.
- Governance pair (REPORT + DECISIONS): **10/10 in D20** (Round 1's 10/10 must
  not regress under the leaner corpus).
- Kill criterion (commitment 2), binary and mechanical:
  `aria-required-parent`, `aria-required-children` and `listitem` appear in
  **zero** `verify/*.jsonl` lines of D20.

## Ruler v2 — what it must separate (spec direction, frozen separately)

The v1 classifier reads *constancy of doing well*, *uniformity of doing
little*, and *adaptation where context demands* as the same thing. v2
separates them, and is built against the **dated fixtures Round 1 produced**,
as an executable test suite frozen with the ruler:

- **Fixture: adaptation punished.** All 10 D journeys pay +1 excess for the
  `aria-sort` pair (`orders` announces sorting, `dashboard` doesn't sort) —
  v2 must score justified divergence as 0.
- **Fixture: uniformity by poverty.** `antigravity A run1–5` score excess 0
  with zero live regions, zero dialogs, zero cards — v2 must not award a
  perfect score to journeys that instantiate almost nothing.
- **Fixture: the half-climbed ladder.** `antigravity__journey__D__run3` must
  read as an *error*, not as dispersion.
- **Defect to fix:** the `cards()` detector finds 0 instances in 27 of 30
  Round 1 runs of a bookstore whose primary family is the book card — the
  detector requires direct children and breaks on wrappers. v2's suite must
  include a fixture from Round 1's real card grids.
- v2 ships as `CLASSIFIER-v2.md` + `classifier-v2.py`, SHA-256 in the header,
  fixtures in-repo and runnable (`--self-test`), frozen before registration.

## Instrument discipline (Round 1's four defects, now protocol)

- **Human-eye sampling rule (was a promise, now a rule):** no measurement
  batch enters results before a seeded random sample of its artifacts passes
  a human eye, logged in the run journal.
- Dual reporting on any instrument correction (defective measurement
  preserved side by side), per the house pattern.
- `DEVIATIONS.md` starts empty; the frozen snapshot proves it; fill-ins
  pre-declared here (registration URL, README status boxes) are not
  deviations.

## Diet accounting (context, not an outcome)

`tools/context-cost.py --compare v1.8.0` is run at freeze time and its table
enters the registration as descriptive context: core +1.5%; per-task delta
range −2.1% to **+9.6%** (navigation); two new guides (~15.8 KB) and one
merged away. The adherence question this table motivates is answered by the
per-obligation panel, not by token arithmetic.

## Cost plan (measured, Round 1)

- Claude Code: median 26–33 min/run → 20 runs ≈ **9–10 h** wall clock.
- Antigravity: ~1–2 min/run → 20 runs ≈ **40 min** (fresh OS profile + gate
  probe per Round 1's discipline).
- Tokens per D journey (fresh, median): 62k/screen large, 41k small — same
  order as Round 1; $0 marginal under existing plans; quota walls are the
  pace-setter, with the cut rule declared above.

## Open questions (decided before freeze, by the author)

1. **Codex as third agent?** Its quota resets 2026-09-16. Adding it makes the
   round 60 runs and reopens the Round-1 gap; skipping keeps symmetry with
   Round 1's realized arms. Default if undecided: skip, note the reset date.
2. **Amortization curve (3/7/14-screen journeys)?** Roadmap item from the
   report; tripling cost and requiring a re-calibrated clock for 14 screens.
   Default: **out of scope** for Round 2 — it deserves its own protocol.
3. **Registration timing:** freeze ruler v2 first, then register, then
   collect — calendar to be set against CSUN's manuscript window (notification
   due 2026-09-22).

## Status

- [ ] Ruler v2 spec + fixtures + `classifier-v2.py` (frozen by hash)
- [ ] Pilot run (1 journey per agent, discarded by rule)
- [ ] This protocol frozen (hash in header) after open questions close
- [ ] OSF registration (own registration; cites pg6r5 §exploratory precedent)
- [ ] Collection opens with the dated `DEVIATIONS.md` entry

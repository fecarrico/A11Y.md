# Round 2 — the v2.0.0 audit (v1.8.0 × v2.0.0)

> **DRAFT v2 — not frozen, not registered.** Revised in full after an
> independent methodological panel review (six lenses, adversarial
> verification; parecer of 2026-08-29). Order of operations inherited from
> Study 2: open questions closed by written rule → executable rulers frozen by
> hash → pilot (discarded) → this protocol frozen → OSF registration (its own
> registration) → collection. Nothing binds until the freeze; after it,
> everything routes through `DEVIATIONS.md`.

## Why this round exists

v2.0.0 was built from Study 2's findings and carries three public commitments
([CHANGELOG](../../CHANGELOG.md), the published report):

1. **Non-regression of the diet.** The release cut ~56 KB gross across the
   corpus in two declared bands while *adding* 9 obligations (62 → 71 per
   edition). Measured between tags: −35.7 KB shrunk in pre-existing files,
   +10.2 KB grown, +15.8 KB new guides, −4.5 KB deleted — **net corpus
   −9.7 KB, core +605 B**. The refutable hypothesis is therefore
   **"adherence to the old obligations fell during the rewrite"** — measured
   per obligation, never as volume.
2. **The kill criterion.** Study 2's half-climbed ARIA ladder (one mold
   replicated across 7 screens) must disappear **as a class**, not as a case.
3. **The contrast bet.** Contrast failed in every uninstructed condition of
   Study 2 and survived in 3 of 5 guided journeys — all three in the
   Antigravity arm; the Claude Code D arm was already at zero. v2.0.0 moved
   contrast to a deterministic protocol. This round measures whether the bet
   paid, **per agent**, with floor rules declared below.

**Lineage note (corrected):** Study 1's registration (osf.io/pg6r5) declared
an exploratory *version delta* outcome — token cost on component tasks via
API, a different unit, outcome and engine. That registration recorded the
*question*; this round registers the version comparison as **its own primary
study** on the journey unit. Motivation cited, not an outcome promoted.

## Design

- **Unit:** the frozen `bookstore-journey` (7 screens, one session, one
  agent), prompt verbatim from [`../study2/PROMPTS.md`](../study2/PROMPTS.md).
  Unchanged for comparability of unit — Round 1 data is context, never a
  pooled arm (its client versions no longer exist).
- **Conditions (4):** A (bare) · B (`Make it accessible.` prepended) ·
  **D18** (the standard at tag `v1.8.0`) · **D20** (at tag `v2.0.0`). No
  placebo, per Study 2's registered rationale. Slugs keep the 4-field shape:
  `agent__journey__{A|B|D18|D20}__runN`.
- **Treatment definition (closed path list).** Each D workspace is built from
  `git archive <tag> -- docs/en/A11Y.md docs/en/references docs/en/templates
  tools` — the Round-1 workspace list **plus the release's own `tools/`
  directory, from the same tag**. Rationale, registered here: the
  deterministic contrast checker is part of what v2.0.0 *is* (its core orders
  ratios computed, tool or formula); testing the release without its tool
  would test a hypothetical, not the shipped standard. The asymmetry
  (`tools/` at v1.8.0 has no `contrast-check.py`) **is the treatment** —
  release-as-delivered, both sides. Per-condition SHA-256 over the archive's
  files concatenated in path order enters the registration.
- **Shell affordance is measured, not assumed.** The runner invokes Claude
  Code with the same permission mode as Round 1 (unchanged, for harness
  comparability) — a mode that does not auto-approve Bash. The pilot
  therefore runs **one D20 journey per agent** and records the observed
  affordance (shell granted? tool executed? formula path taken?) in the
  journal before the freeze. If an agent cannot run the tool, the protocol
  declares: for that agent, D20 measures the formula path by construction —
  the fallback the standard itself prescribes.
- **Agents (2):** Claude Code and Antigravity, client versions named at
  registration. **Codex rule (closed):** Codex enters only if its quota is
  active and the client installable on freeze day; its quota resets
  2026-09-16, colliding with the calendar below — default executed: **skip**,
  Codex named a Round-3 candidate.
- **n:** 5 per cell → `5 × 4 × 2 = 40 runs`. Cut rule inherited: agents are
  cut before repetitions.
- **Collection order:** interleaved by run index — for each index 1..5, run
  A, B, D18, D20 (in that order) before the next index, including under
  `--resume`. Client auto-update disabled where the product allows; the
  client version is logged per run and the runner **aborts** if it differs
  from the registered one. Version changes are permitted only between
  complete cycles, logged, and reported as a version×condition table.
- **Retention and retry (mechanical):** a run is retained iff it produces 7
  non-empty screens within the 90-minute clock (symmetric, inherited).
  Retry only on infrastructure error (client crash, quota wall, network
  failure — the verbatim error message is logged), maximum 2 retries,
  nothing deleted; per-cell failure rates are reported as data.
- **Clock:** 90 min per run, symmetric (Round-1 calibration, >2× headroom).

## Environment hygiene (the Round-1 lesson, now protocol)

Round 1's Claude Code arm inherited the operator's live environment; the
generic condition hunted for the standard (see
[`../study2/DEVIATIONS.md`](../study2/DEVIATIONS.md), entry 2026-08-29 —
leakage direction conservative, but undeclared). Round 2:

- **Dedicated sanitized HOME per agent** — credentials and client
  configuration only; no user skills, no personal `CLAUDE.md`, no vault
  grants, no `additionalDirectories`. The profile's full contents are listed
  in the frozen snapshot.
- **Gate probe tests the symptom, per agent, before any retained run:** a
  B-style probe journey screen; retained only if the transcript contains no
  reference to, or search for, the standard or the operator's files.
- **Network policy:** web/search tools disabled where the client supports it;
  the setting's state is registered per agent. Per-run audit: for Claude
  Code, `server_tool_use` and `permission_denials` from the native capture
  (must show zero web access); for Antigravity, a transcript grep — declared
  as a **limit**, not sold as a guarantee. A contaminated run is excluded and
  recollected, with a dated `DEVIATIONS.md` entry. Training-data cutoff
  defense stated in the registration; the core's upstream-repo line is
  byte-identical in both tags and is a *declaration*, never edited in the
  corpus (editing would break the tag hash and the ecological premise).

## Outcomes, rulers and the decision panel

**Statistical posture, verbatim from the registered Round 1: this study is
descriptive and estimation-oriented — not confirmatory at this n.** The
commitments below are falsifiable checks, not hypotheses this n can confirm.
Primary contrast: **D20 vs D18, same-agent, never pooled.** Secondary: D20 vs
B, D20 vs A. Seeded bootstrap (B=10,000), Cliff's delta, no p-values. Where a
screen-grain outcome is used, the bootstrap **resamples by journey cluster**
(screens within a session are correlated). Printed in the registration so no
reader over-reads: the null SD of Cliff's delta at n=5×5 is ≈0.38 — only
near-complete separation is distinguishable from noise.

### The five rulers — declared hierarchy, named judges, all executable

| # | Ruler | Serves | Judge (frozen) |
| - | ----- | ------ | -------------- |
| 1 | **Screens with error** — screen×error pairs, axe critical+serious. *Construct qualified: the machine-detectable layer only (axe-class coverage 30–57% in the literature, cited in the registration).* | the person navigating | `rulers.py screens` |
| 2 | **Wrong decisions** — distinct violated rules per journey (each error counted once however often its mold repeats). Definition frozen in `RULERS.md`, validated in `--self-test` against Round 1's published 9/11/8. | the maintainer fixing | `rulers.py decisions` |
| 3 | **Clean journeys** — descriptive only, base rates printed (Round 1: 0/5 · 0/5 · 2/5 on the small model). | the team shipping | `rulers.py clean` |
| 4 | **Consistency v2** — see spec direction below; frozen as `classifier_v2.py` (underscore: `analyze.py` and the self-test import it as a module — a filename detail settled before the freeze, noted here so the draft's earlier `classifier-v2.py` spelling has a paper trail). The frozen v1 (hash intact) runs over all Round-2 data as a **sensitivity analysis**; both results published; divergence reported as a finding about the instrument. | the person relearning each screen | `classifier_v2.py` |
| 5 | **Flagged elements** — raw node count (registered since Round 1). | the auditor | axe + `analyze.py` |

All rulers 1–3 ship as **frozen scripts with `--self-test`** whose fixtures
are Round-1 data — including, per ruler, at least one fixture where the
standard's condition *loses* (they exist: Antigravity D lost ruler 1, 38 vs
13). Freezing them is a gate in the Status checklist, same discipline as
ruler 4.

### The per-obligation non-regression panel (canonical mapping)

This panel is the **single canonical mapping** commitment→estimand→criterion.
Binary language is reserved for the kill criterion alone; everything else is
an estimand with edge cases closed:

| Check | Rule | Edge cases (closed) |
| ----- | ---- | ------------------- |
| `image-alt`, `label` classes | Floor: zero across D20 journeys (Round 1 banked zero in D) | **One** isolated violation → topology inspection (mold vs lapse), reported, not auto-veto; **≥2 journeys affected** → regression, stated as such |
| Any other axe class at zero in D18 (same agent) | Generalized floor: reappearance in ≥2 D20 journeys = regression | Same isolated-violation rule |
| `color-contrast` (the bet) | Per agent: **corroborated** iff (D18>0 and D20<D18) **or** (D18=0 and D20=0); **refuted** iff D20>D18; tie at >0 = not corroborated | Antigravity named as the only informative arm from Round 1 (Claude Code D was 0/5 — floor rule applies: staying at zero = success). Directional reading with the estimand's CI beside it, never a lone verdict |
| Governance pair (REPORT + DECISIONS) | Proportion with CI (Round 1: 10/10 vs 0/20); pre-declared reading of a single miss: inspect the journal before "regression" | 10/10 expected; 9/10 is inspected, not headlined |
| Kill criterion | **Binary.** The ladder **class list**, derived from axe 4.13.0's ARIA structural rules and published with its derivation: `aria-required-parent`, `aria-required-children`, `listitem`, `dlitem`, `definition-list`, `aria-required-attr`. Zero appearances in all D20 `verify/*.jsonl` **and** the 2×2 table against D18 fresh (if D18 also zeroes, the zero evidences the client era, not §6 — stated). Base rate printed: 1/10 Round-1 D journeys; P(zero in 10 | no change) = 0.9¹⁰ ≈ 0.35 | The comparator column is what makes the zero interpretable |

**Two-agent adjudication rule (pre-declared):** commitments are judged
same-agent; when the two agents diverge, both verdicts are reported and the
**less favorable one leads the write-up**. No synthesis averages them.

### What will and will not be claimed

- **Publication is unconditional on outcome** — the Round-1 precedent
  ("published however it comes out") is the operating rule.
- Claims about commitments come **only** from the canonical panel above. All
  other cells are descriptive, labeled so, and barred from headlines.
- Ruler-1 improvements are claims about the machine-detectable layer, never
  about the full navigation experience.
- **Consequence table (pre-written):**
  - Kill criterion fails → §6's ladder rule is reopened as a *structural
    defect* of v2.0.0, fixed in a v2.0.x release, CHANGELOG amended, and the
    failure headlined in the round's report.
  - Contrast bet refuted (either agent) → "the bet paid" is unpublishable;
    a dated note corrects the v2.0.0 announcement narrative.
  - Any floor regression → named in the report's lead, with the topology
    inspection attached; the diet's band-B cuts are re-examined first.
  - Mixed results across agents → the less favorable verdict leads (rule
    above); "it depends on the agent" is a finding, not a hedge.

## Ruler v2 — spec direction (frozen separately as `CLASSIFIER-v2.md`)

v1 reads *constancy of doing well*, *uniformity of doing little* and
*adaptation where context demands* as the same thing. v2 separates them under
these constraints, panel-reviewed:

- Every rule derived from a Round-1 fixture enters as a **condition-blind
  general principle** (e.g., the state dimension compares only instances with
  the same functional capability — no whitelists), with **held-out synthetic
  counter-fixtures** in `--self-test` proving the same pattern scores
  identically wherever it appears.
- **Dispersion stays a pure metric; poverty becomes a separate denominator**
  (variant excess reported beside instantiated-family counts, never fused
  into one score).
- Ruler 4 measures **consistency over valid instances**, with the validity
  check itself frozen and exclusion counts reported per condition.
- Known v1 defects to fix, with fixtures: the `aria-sort` adaptation pair
  (10/10 D journeys penalized for doing right — present in 25/30 journeys
  overall, condition-neutral), uniformity-by-poverty (Antigravity A: perfect
  scores instantiating almost nothing), the half-climbed ladder read as
  dispersion, and the card detector blind in 27/30 runs of a bookstore.
- The frozen **v1 runs over all Round-2 data as sensitivity analysis** (cost:
  seconds; gain: cross-round auditability).
- **Cross-vocabulary rule (adversarial panel, bias lens):** variant excess is
  only measurable inside the semantic vocabulary the standard prescribes —
  non-semantic A/B implementations of the same components disperse invisibly.
  Ruler 4 therefore informs the **primary contrast only** (D20 vs D18, same
  vocabulary on both sides). In secondary contrasts (vs A/B) it is
  descriptive: quoted per family, conditioned on the family being counted in
  both cells, `families_counted` alongside, and raw cross-condition sums
  barred from headlines. `analyze.py` enforces this mechanically (excess is
  absent from the secondary contrast tables).

## Instrument discipline

- **Human-eye sampling rule (was a promise, now a rule):** no measurement
  batch enters results before a seeded random sample of its artifacts passes
  a human eye, logged in the run journal.
- Dual reporting on any instrument correction; defective measurements
  preserved side by side.
- **Blinding, scoped in three sentences:** script-computed outcomes need no
  blinding and claim none. Human QA looks only at hash-renamed screens
  (sealed map); any correction it triggers applies to the entire corpus.
  Governance artifacts self-reveal their version by content — they reach
  human eyes only after all outcomes are computed; residual limit declared.
- `DEVIATIONS.md` starts empty (frozen snapshot proves it); pre-declared
  fill-ins (registration URL, README status boxes) are not deviations.

## Diet accounting (context, not an outcome)

`tools/context-cost.py --compare v1.8.0` is run at freeze time; its table
enters the registration as descriptive context (core +1.5%; per-task delta
−2.1% to **+9.6%**, navigation; two new guides; one merged away). The
adherence question is answered by the panel, not by token arithmetic.

## Cost plan (measured, Round 1)

Claude Code median 26–33 min/run → 20 runs ≈ 9–10 h wall clock; Antigravity
1–2 min/run under fresh-profile discipline → ≈ 40 min + probes. $0 marginal;
quota walls set the pace, cut rule declared.

## Closed questions (were open; now rules)

1. **Codex:** skip (rule and reset date above); Round-3 candidate.
2. **Amortization curve (3/7/14 screens):** out of scope; own protocol.
3. **Calendar:** counted backwards from CSUN notification (2026-09-22). If
   the checklist below does not fit **with slack**, the freeze is not
   compressed to fit — the CSUN manuscript cites the registered Round-1
   material; a rushed freeze is the door post-hoc walks through.

## Status — every box gates the freeze

- [ ] Rulers 1–3: `RULERS.md` definitions + `rulers.py` frozen by hash,
      `--self-test` reproducing Round 1's published numbers (33/13/38 ·
      9/11/8 · 0-0-2/5) and containing a D-loses fixture per ruler
- [ ] Ruler v2: `CLASSIFIER-v2.md` + `classifier_v2.py` frozen by hash,
      condition-blind principles + held-out counter-fixtures in `--self-test`
- [ ] Kill-criterion class list derivation published (axe 4.13.0 structural
      rules; native and keyboard boundaries resolved)
- [ ] `round2/run.py` + `round2/analyze.py`: 4 conditions, tag-archived
      workspaces, D20−D18 implemented, interleaving, version pinning,
      mechanical retry; frozen by hash; validated against a synthetic 40-run
      fixture
- [ ] Sanitized per-agent HOME built; contents listed; gate probes defined
- [ ] Pilot: 1 journey per agent (discarded), D20 affordance probe (shell /
      tool / formula path) + gate probes; observations journaled
- [ ] This protocol frozen (hash in header)
- [ ] OSF registration (own registration; lineage note as written above)
- [ ] Collection opens with the dated `DEVIATIONS.md` entry

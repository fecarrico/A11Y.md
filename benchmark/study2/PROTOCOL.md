# Study 2 — Governance at journey scale

> **Status: DRAFT v0.1 — not registered, not frozen.** Nothing here authorizes
> collection. The path is explicit and ordered: pilot (discarded) → classifier
> frozen by hash → OSF registration (its own registration, not an amendment) →
> collection. **Study 1's publication waits for this study's registration**,
> not for its results.

## Where this study comes from — declared, with dates

Study 2 was conceived on 2026-08-18, **after Study 1's primary results were
final**, prompted by an external methodological review of the unpublished
report and by two observations Study 1 had logged as capture notes
([`../ARM2.md`](../ARM2.md)):

- real agents under the standard produced lifecycle artifacts nobody asked for
  — REPORT.md in 17/18 condition-D runs, A11Y-DECISIONS.md in 13/18, at least
  one governance artifact in 18/18, against 0/18 without the standard;
- the standard gave agents a *sense of place*: every D run anchored its work in
  the project directory, while bare runs sometimes treated the task as chat.

Follow-up motivated by results, with the motivation declared, is how science
moves. What would not be defensible is presenting this design as if it had been
conceived alongside Study 1 — it was not, and this section exists so no reader
has to discover that on their own.

## The question

Study 1 measures whether the standard reduces machine-detectable violations in
isolated components, at a per-task cost ceiling. This study asks the question
that design cannot reach:

> **In the real usage regime — one agent session, one whole journey — what is
> the difference between asking for accessibility and operating under the
> standard, in inter-screen consistency, reuse, governance, and amortized
> cost?**

## The deliberate inversion

| | Study 1 | Study 2 |
|---|---|---|
| Unit of analysis | component | **journey** |
| Session | one per task | **one per journey** |
| Standard loading | reinjected per task | **once, amortized** |
| Primary engine | API (simulates an agent) | **real agents (CLI)** |
| Primary outcome | axe violations | **inter-screen consistency** |
| Violations | co-primary | secondary (non-regression) |
| Tokens | co-primary, gross ceiling | co-primary, **per deliverable** |

## Conditions

| | Condition | Delivery |
|---|---|---|
| **A′** | bare | task prompt only |
| **B′** | generic | `Make it accessible.` prepended to the task prompt |
| **D′** | a11ymd | standard on disk + the verbatim Quick Start rule, delivered per agent exactly as [`../ARM2.md`](../ARM2.md) defines it |

**No C′ (placebo), and the justification belongs to the registration:** the
content-vs-form question was answered by Study 1 (D vs C: IRR 0.34
[0.18–0.66], confirmed in both specifications). A journey run costs hours, not
minutes; keeping C′ would raise cost by half to re-decide a decided question.
If budget appears, C′ enters as an optional, declared arm.

**The decisive contrast is D′ vs B′** — Study 1's bravest question, retaken at
the scale where the standard claims to matter. Study 1 found the two not
separable on machine-detectable violations in a small model; this study
measures what that outcome cannot see by construction.

## The artifact — one journey, one frozen prompt

[`PROMPTS.md`](PROMPTS.md) freezes, verbatim, a single prompt asking for a
small online bookstore of **seven screens** that reuses the component families
of Study 1's ten tasks. The prompt never mentions accessibility and never asks
for consistency or reuse — those are the phenomena under measurement, and
asking for them would be this study's version of "make it accessible".

Families counted in the primary outcome are those the journey instantiates on
**two or more screens**: navigation, book card, form, confirmation dialog,
transient status message, data table. Families instantiated once (carousel,
upload, autocomplete, chart) are excluded from the primary metric and reported
descriptively.

## Outcomes

**Primary — inter-screen consistency.** For each counted family, the number of
**distinct implementation variants** across screens, extracted by the
deterministic classifier specified in [`CLASSIFIER.md`](CLASSIFIER.md) —
structural signatures, no LLM, no human judgment. Example: a confirmation
dialog built on `<dialog>` on one screen and on `div[role="dialog"]` on
another counts two variants; neither is scored as an error — **the dispersion
itself is the finding**. Reported per family, plus one aggregate: total
variant excess, Σ(variants − 1). Zero means every family is implemented one
way everywhere.

**Co-primary — amortized cost.** Session token total ÷ deliverables shipped
(screens present and non-empty), tokens as the client reports them, labeled as
the client's own accounting. Reported beside Study 1's per-task ceiling — the
difference between the two numbers *is* the amortization, quantified at last.

**Secondary — reuse.** Shared artifacts (stylesheets, scripts) referenced by N
screens versus re-declared per screen; structural duplication measured with a
pinned tool and threshold (jscpd, version and config recorded at freeze).

**Secondary — governance.** Binary, counted by script, no judgment: presence
of REPORT.md · presence of A11Y-DECISIONS.md · exceptions documented ·
dependencies declared. Inherits Study 1's exploratory count as a registered
outcome — which is exactly what a follow-up is for.

**Secondary — violations, as non-regression.** axe-core pinned by hash, per
screen and aggregate. Study 1 answered this question; here it only checks that
the standard does not regress at scale.

**Exploratory — error topology.** When a family fails on several screens: the
same failure everywhere (systematic — one fix) or a different failure per
screen (dispersed — expensive to hunt)? No scanner reports this; labeled
exploratory.

## Engines and size

**n = 5 per condition × 3 conditions × 2 agents = 30 runs**, collected in
waves under each product's quota. The two agents are named at registration,
drawn from Claude Code, Codex and Antigravity by available quota — Antigravity
arrives already exercised by Study 1's third-agent amendment. If 30 proves
infeasible, agents are cut before repetitions: journey variance dwarfs
component variance, and repetitions too few show nothing.

**This study is descriptive and estimation-oriented — not confirmatory at this
n, and the registration says so.** Point estimates, bootstrap intervals,
Cliff's delta for D′ vs B′. No hypothesis tests, no p-values.

**Wall clock: 90 minutes per run, symmetric across conditions** — fixed from
the pilot's observed maximum (37.1 min) with >2× headroom. Calibrated on
Claude Code; if another agent needs a different clock it changes for all
conditions of that agent, dated, before its first retained run.

## Blinding — and its declared limit

Journeys are recognizable: D′ output likely ships REPORT.md beside it, and no
renaming hides that from a human. So blinding is per artifact class: **only
the screens' HTML — hash-renamed, map sealed — reaches any human eye**; the
governance package is counted by script only. The primary metric needs no
human at all. The residual limit — style could still hint at a condition — is
declared here.

## Verification

Study 1's discipline unchanged: axe-core pinned by SHA-256, headless Chromium,
screens served over HTTP, per-screen JSONL, full-page screenshots.

## Pilot — run 2026-08-18, learned from, discarded

One full journey per condition on Claude Code, outside the repository, data
discarded by construction. What it taught, in full:

- **Durations:** bare 15.0 min · generic 19.8 · standard 37.1 — all three
  shipped 7 screens. Wall clock fixed at 90 minutes (above).
- **The amortization regime is real:** the standard-condition journey read the
  documentation once and served the rest from cache — 5.8M cache-read tokens
  against 291k cache-creation in the client's own accounting. The regime the
  study exists to measure is observable in one session.
- **Governance emerges at journey scale too:** the standard's journey produced
  `A11Y-DECISIONS.md` spontaneously — and *not* `REPORT.md`, which is why the
  rubric counts each artifact independently.
- **Classifier calibration:** static-DOM scope declared; native-confirm scan
  with dominance rule; anchors widened (all in CLASSIFIER.md, which records
  the frozen executable's hash). The pilot journey of the standard scored
  *worst* on variant excess — the instrument can rule against the standard,
  which is exactly what an instrument must be able to do.

Precedent for this disclosure: Study 1's pilot disclosure.

## Deviations

This study keeps its own journal, [`DEVIATIONS.md`](DEVIATIONS.md), under
Study 1's discipline: dated entries, clarifications included, nothing hidden.

## Registration

To be registered on OSF as **its own registration** — not an amendment to
[osf.io/pg6r5](https://osf.io/pg6r5) — after the pilot freezes the classifier
and **before Study 1 is published**, so that Study 1's limitations section
points at a live public test instead of a promise. This section receives the
registration URL when it exists.

## What will and will not be claimed

- **Claimed, if the data support it:** the direction and estimated size (with
  intervals) of the difference between B′ and D′ in consistency, reuse,
  governance and amortized cost, in the agents and models logged.
- **Never claimed:** statistical confirmation (the n forbids it and the
  registration says so); comparisons between agents or models; transfer to
  engines not run. Each agent is reported against its own baseline —
  Study 1's sentence, still true here.

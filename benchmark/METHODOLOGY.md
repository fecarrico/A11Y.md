# A11Y.md Efficacy Benchmark — Pre-registered Methodology

> **Status:** Pre-registered, version 2.0 — published **before any data collection**. Results will be reported against this protocol exactly; any deviation will be documented in `DEVIATIONS.md`, never hidden.
> **Version:** 2.0 · 2026-08-16 · Felipe A. Carriço
> **Supersedes:** v1.0 (2026-07-25, commit `eb6f28f`). No data was collected under v1. One pilot generation was run under a draft of the v2 harness and discarded; see *Pilot disclosure*.

## Version history

| Version | Date | What changed and why |
|---|---|---|
| 1.0 | 2026-07-25 | Initial pre-registration: 3 models × 3 tasks × 2 conditions × 3 runs, collected by hand in consumer chat interfaces, full core pasted into the prompt. |
| 2.0 | 2026-08-16 | Redesigned before collection. (a) **The v1 design did not test the standard as it works**: pasting the full core defeats lazy loading, which is the standard's declared architecture. Collection now gives the model a scoped `read_file` tool and lets the mechanism run. (b) **Two active control conditions added** — a one-line accessibility request and a size-and-mechanics-matched placebo standard — because "standard vs nothing" cannot separate the standard's content from cheaper ways of getting the same effect. (c) **Token accounting added as a co-primary outcome.** (d) Collection moved from hand-driven chat interfaces to API calls: reproducible, isolated by construction, and free-tier viable. (e) Blinding and a pre-specified analysis plan added. |

## The claims under test

1. **Efficacy:** giving the AI the A11Y.md standard reduces automatically detectable accessibility violations in generated UI code — *and reduces them more than cheaper alternatives* (a generic "make it accessible" request; an equally long, equally structured document about a different subject).
2. **Cost:** the standard's lazy-loading architecture keeps its context cost bounded and task-proportional — the model loads the core plus the guides the task calls for, not the whole library — at a measurable token cost per task.

This benchmark makes **no claim about full accessibility or real assistive-technology usability**. Automated tooling detects only a fraction of real-world barriers (published estimates range ~30–57%). Human validation is Phase 2 — separate, and separately pre-registered.

## Design

### Conditions (4)

The task prompt is identical across conditions; only what precedes it differs. Preambles are fixed verbatim here.

| | Condition | Preamble (verbatim) | Documents available |
|---|---|---|---|
| A | bare | *(none)* | none |
| B | generic | `Make it accessible.` | none |
| C | control | `When developing the frontend, follow strictly the performance rules defined in PERF.md. Read it with the read_file tool at 'PERF.md'.` | placebo standard (`benchmark/control-standard/`) |
| D | a11ymd | `When developing the frontend, follow strictly the accessibility rules defined in A11Y.md. Read it with the read_file tool at 'A11Y.md'.` | `docs/en/` (core + references + templates) |

Condition D's sentence is the standard's own Quick Start invocation, verbatim, with one harness concession: naming the tool, which the model cannot otherwise discover. **Nothing else is added** — no hint that reference files exist, no instruction to load selectively. Lazy loading must emerge from reading the core, or the benchmark is teaching the behaviour it claims to measure.

Condition C is the placebo: a performance standard with the **same size, the same shape, and the same mechanics** — a core file with a loading-triggers map, per-component guides, the same tool. It isolates the effect of the A11Y.md's *content* from the effect of having any long, well-organised technical standard in context. Its sentence is D's sentence with the subject swapped; if it mentioned accessibility it would cue the very thing it exists to rule out.

The three pre-registered contrasts: **D−B** (does the standard beat one free sentence? — the question that decides whether the project has a reason to exist), **D−C** (does the content beat the form?), **D−A** (headline effect).

### Lazy loading, reproduced faithfully

A raw API call has no filesystem, so pasting is the only way to supply documents — and pasting everything kills the mechanism while pasting the core alone strands it. The collector therefore exposes **one tool, `read_file`**, scoped to the condition's document directory (path traversal and absolute paths are refused). The model reads the core, consults the §2.1 loading map, and requests what it decides to request. Every file request is logged with its size; the request pattern is itself a pre-registered outcome (see *Loading behaviour*).

One generation = one conversation, from scratch. No memory, no accumulated context across generations. Via API this is the default; no discipline required.

### Arms

| Arm | Engine | Role | Cost |
|---|---|---|---|
| 1 — primary | **Gemini API, free tier** (current Flash-class model; exact model string and version recorded per call) | The full factorial design below. All confirmatory analysis runs on this arm. | $0 |
| 1-ext — extension | Claude API / OpenAI API | **Pre-registered, conditional:** the identical protocol runs on additional models if and when usable API credits exist. Extension arms replicate; they do not alter the design. Each extension arm is reported separately, never pooled with Arm 1. | conditional |
| 2 — ecological | **Claude Code CLI** (official client, subscription) | A small-n check that the Arm 1 effect direction survives in a real coding agent with a real filesystem: conditions A and D only, a task subset, `n=3`. Reported descriptively; no hypothesis test. | $0 marginal |

Arm 1 is the study. It is honest about what it is: one model family, named in the title of any report. A single-model study with active controls and a frozen protocol outranks a three-model study with neither; the extension arms exist so that more models require no protocol change, only funding.

### Tasks (10)

Drawn from the WebAIM Million's recurring error categories plus the ARIA-redundancy pattern this repository documents. Prompts are frozen verbatim in [`PROMPTS.md`](PROMPTS.md) and never mention accessibility. Each task maps to the reference guide(s) the standard's §2.1 loading map would select — the pre-registered expectation for the loading-behaviour outcome:

| # | Task | Expected guide(s) per §2.1 |
|---|---|---|
| 1 | Signup form with inline validation | `guide-forms` |
| 2 | Destructive-confirmation modal | `guide-modals` |
| 3 | Sortable data table | `guide-tables` |
| 4 | Site navigation with dropdown submenus | `guide-navigation` |
| 5 | File upload with progress and failure states | `guide-forms`, `guide-loading-skeleton` |
| 6 | Auto-advancing image carousel | `guide-carousels-sliders` |
| 7 | Search box with live suggestions | `guide-autocomplete` |
| 8 | Product card grid | `guide-images`, `guide-buttons` |
| 9 | Async save with toast notifications | `guide-toasts-notifications` |
| 10 | Dashboard chart with table toggle | `guide-charts`, `guide-tables` |

The set deliberately spans cheap guides (~400 chars) to heavy ones (~7,700 chars), so the token outcome has range.

### Size

**10 tasks × 4 conditions × 10 repetitions = 400 generations** (Arm 1). Free-tier daily caps make this a multi-day collection: waves are collected on consecutive days with conditions interleaved (never one condition's block on one day — interface drift must not load onto a condition), resumable without re-running anything already on disk. Collection dates, model version strings, and per-call token usage are logged per generation.

## Measurement

### Violations (co-primary)

1. **axe-core, pinned version, SHA-256-verified** (already vendored in `harness/`), over each generated page mounted unmodified. Primary count: violations of impact `critical` + `serious` per generation.
2. **Deterministic per-task checklist** (harness), each item mapped to a WCAG success criterion and a WebAIM Million category — published as a table so the checklist is auditable against external sources, not against the standard it measures.
3. **Second engine, robustness only:** a second independent scanner (IBM Equal Access or Pa11y, version pinned at the moment it is added, before any unblinding) runs over the same files. Agreement between engines is reported; disagreement is reported, not resolved by choosing the friendlier engine.
4. **Items the harness marks MANUAL** (modal focus containment, target-size exceptions): automated where a scripted browser can decide them; the remainder adjudicated by a human on a **random sample of 60 generations**, blind (see below). Sampled adjudication enters the checklist secondary outcome; it does not touch the primary.

### Tokens (co-primary)

All figures come from the API's own usage report, summed across the calls of one generation:

| Measure | Definition |
|---|---|
| Total per task | input + output + thinking tokens across the generation's calls |
| Fixed cost | tokens of the core file (provider tokenizer count) |
| Lazily loaded | sum of characters/tokens of the files the model requested via the tool |
| Cached share | tokens billed at cache rates — the mechanism that makes the tool loop affordable |
| Tokens per violation avoided | Δ tokens ÷ Δ violations, D vs each comparison condition |
| Version delta | same tasks against a prior release of the standard (exploratory) |

### Loading behaviour (secondary, pre-registered classification)

The pilot showed the model loading more than the §2.1 map row: extra guides justified by rules in the core's text, plus lifecycle templates. Every file request is therefore classified, blind to outcome, as:

- **map** — the guide the §2.1 row for this task names (table above);
- **core-rule** — a file a rule in the core text instructs loading in this task's circumstances (the justifying rule is cited);
- **template** — a `templates/` file (lifecycle context; the standard mandates loading on triggering events);
- **unjustified** — anything else.

Reported per condition: distribution of classes, and share of generations whose map guide was loaded (map hit-rate).

## Blinding

Before any scoring, every generated file is renamed to the SHA-256 of its content. The mapping `hash → (model, task, condition, run)` is written once, sealed (committed encrypted or held out of the analysis environment), and opened only after automated scoring and sampled adjudication are complete. Scanners are indifferent to blinding; the human adjudicator and the loading-behaviour classifier are not, which is why it exists.

## Analysis plan (pre-specified)

- **Primary outcome:** count of `critical`+`serious` axe violations per generation.
- **Confirmatory contrasts:** D−B, D−C, D−A, Holm-corrected.
- **Model:** negative-binomial mixed regression, violations ~ condition + (1 | task). Reported as incidence-rate ratios with 95% CIs.
- **Robustness:** bootstrap difference of per-condition medians and Cliff's delta, run in parallel. Divergence between the two approaches is reported.
- **Token primary:** total tokens per completed task, per condition — same contrasts, same correction, Gamma or log-normal mixed model as distribution dictates (choice documented before unblinding).
- **Secondary:** share of generations with zero critical violations; checklist pass-rate; loading-behaviour distribution and map hit-rate.
- **Exploratory, labelled as such:** everything else — engine agreement, per-category violation breakdown, tokens-per-violation-avoided, version deltas, Arm 2 descriptives.

## Determinism, stated up front

There is no seed parameter, and current-generation models on several providers reject sampling controls outright; where accepted, `temperature=0` has never guaranteed identical outputs. **This protocol does not promise reproducible outputs; it promises a reproducible process:** frozen prompts, logged model versions per call, all raw outputs published, and this pre-specified analysis. Anyone can re-run the protocol; anyone can re-analyse the published outputs without re-running anything.

## Cost

Arm 1 runs on the Gemini free tier: $0. Arm 2 runs on an existing subscription through the official client: $0 marginal. Extension arms are conditional on credits and change nothing else. The pilot measured ~90k tokens for one condition-D generation (7 API calls, cache absorbing ~43% of input), so free-tier daily caps — not money — set the collection pace.

## Known limitations (stated before collection)

- **Automated detection ceiling.** ~30–57% of real barriers; no conformance claim is made or implied.
- **Fewer detectable violations ≠ better lived experience.** That bridge is Phase 2.
- **Arm 1 simulates an agent; it is not one.** A single scoped tool reproduces the loading mechanism, not a real agent's system prompt, tool set, or history. Arm 2 exists for exactly this reason.
- **Single model family in the primary arm.** Named in every report title; extension arms are the remedy, pre-registered here.
- **Training contamination.** A11Y.md is public since April 2026 and may be in training data. Declared; mitigated by tasks that do not appear in the repository's examples; not eliminable. Additionally, free-tier providers state that submitted data may be used to improve models — this study feeds the standard back into that loop, which future runs must declare.
- **Model drift under a stable name.** Free-tier models update silently; version strings and dates are logged per call, and results claim validity for the logged snapshots only.
- **The benchmark's author is the standard's author.** Mitigated by external registration, blinding, an externally anchored checklist, a second engine, and full publication of raw outputs — not by good faith. External methodological review before collection is invited and outranks any result.

## Pilot disclosure

One generation (signup form, condition D) was run on 2026-08-16 under a draft harness whose grounding sentence added an instruction the standard does not contain ("load only what applies"). It was discarded and is not part of any dataset. It motivated two protocol elements: the verbatim-Quick-Start grounding rule, and the loading-behaviour classification (the model loaded six files — the map row, three core-rule-justified guides, two templates — none of it predicted by the v1 design).

## Registration

This protocol is registered at **OSF Registries** before the first retained generation, and the registration's identifier is added here in the same commit that starts collection. The repository tag marking the frozen protocol is signed. From that point, every departure — a model that refuses a task, a rate-limit change mid-wave, a re-collected cell — is a dated entry in `DEVIATIONS.md`.

## Phase 2 — human validation (planned, not started)

Task-completion sessions with screen-reader users over products built with the standard **in production** — not lab prototypes. Requires an installed base first (public project registry with adoption dates, then automated field scans, then sessions). Will be pre-registered separately in this folder before starting.

## Reporting

Results go to the repository's [Evidence & Research wiki page](https://github.com/fecarrico/A11Y.md/wiki/Evidence-and-Research) alongside the third-party benchmarks this project already tracks — measured with the same skepticism we apply to everyone else's numbers. Raw outputs and the sealed/unsealed blinding map are published as a citable dataset (DOI) outside this repository; the repository carries the protocol, the scripts, and the aggregated results.

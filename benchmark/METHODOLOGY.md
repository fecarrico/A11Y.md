# A11Y.md Efficacy Benchmark — Pre-registered Methodology

> **Status:** Pre-registered — this protocol is published **before any data collection**. Results will be reported against it exactly; any deviation will be documented, not hidden.
> **Version:** 1.0 · 2026-07-25 · Felipe A. Carriço

## The claim under test

> Injecting `A11Y.md` as persistent context reduces **automatically detectable accessibility violations** in AI-generated UI code.

This benchmark makes **no claim about full accessibility or real assistive-technology usability**. Automated tooling detects only a fraction of real-world barriers (published estimates range ~30–57%). Human validation with assistive-technology users is Phase 2 — separate, and separately pre-registered.

## Design

- **Models (3):** Claude, Gemini Pro, GPT — consumer chat interfaces, default settings, fresh session per run, model/version recorded at run time.
- **Tasks (3):** canonical components where the WebAIM Million's recurring error categories concentrate:
  1. **Signup form** with inline validation and error messaging.
  2. **Destructive-confirmation modal** opened from an item list.
  3. **Sortable data table** with a per-row action.
- **Conditions (2):**
  - **A — bare:** the task prompt alone.
  - **B — grounded:** the identical prompt preceded by the full `docs/en/A11Y.md` (v1.1.0+, Standard profile). No other wording differences.
- **Repetitions:** 3 per cell → 3 models × 3 tasks × 2 conditions × 3 runs = **54 generations**.
- **Prompts:** fixed verbatim in [`PROMPTS.md`](PROMPTS.md), published before data collection. The prompts never mention accessibility — that is the point.

## Measurement

1. **axe-core (pinned version)** over each output mounted unmodified in a static harness page — violations counted by impact (critical / serious / moderate / minor).
2. **Deterministic per-task checklist**, verified by script against the rendered DOM:
   - native `<button>`/`<a>` vs clickable `div`
   - labels programmatically associated to inputs
   - modal: focus moved in, contained, and returned on close; `Escape` closes
   - dynamic feedback exposed through a live region (`role="status"`/`role="alert"`/`aria-live`)
   - minimum 24×24 CSS px target size (SC 2.5.8)
   - no redundant ARIA on native elements (ARIA Soup check)
3. **Secondary:** prompt+context token footprint per condition; whether the model asked for or needed reference guides.

## Analysis

- **Primary outcome:** critical+serious axe violations per generation — median per condition, per model.
- **Secondary:** checklist pass-rate; share of generations with **zero** critical violations.
- All raw outputs, harness, scripts and spreadsheets are published in this folder. Anyone can re-run the protocol.

## Known limitations (stated up front)

- Automated detection covers only a fraction of real barriers — **no conformance claim** is made or implied.
- Consumer chat interfaces drift (model updates, hidden settings); versions and dates are logged per run.
- Author-run: the prompts and rubric are public precisely so the result can be challenged and reproduced.

## Phase 2 — human validation (planned, not started)

Task-completion sessions over the same generated outputs with screen-reader users, recruited via community open call. Will be pre-registered in this folder before starting.

## Reporting

Results will be added to the repository's [Evidence & Research wiki page](https://github.com/fecarrico/A11Y.md/wiki/Evidence-and-Research) alongside the third-party benchmarks this project already tracks — measured with the same skepticism we apply to everyone else's numbers.

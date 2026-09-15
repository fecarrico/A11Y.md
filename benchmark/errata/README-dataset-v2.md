# A11Y.md Efficacy Benchmark — raw dataset (v2)

Supersedes v1. **Nothing from v1 is modified or removed** — every one of its 885
entries is carried over byte for byte, verified by SHA-256 at build time
(`benchmark/build-dataset-v2.py`). Read `dataset/README.md` for what v1 contains;
this file covers only what v2 adds and why.

## Why there is a v2

The registered protocol (https://osf.io/pg6r5) defines the violation outcome as
**two** instruments and registers a **third** as a robustness check. Only one had
ever been run. See `ERRATA-study1.md`, included in this package.

## What v2 adds

- `verify/arm1-checklist.jsonl` — co-primary outcome nº 2, the deterministic
  per-task checklist mapped to WCAG success criteria, over all 400 pages.
  Extracted verbatim from the registered harness, not reimplemented.
- `verify/arm1-pa11y.jsonl` and `verify/arm1-pa11y-full.jsonl` — the registered
  second engine (HTML_CodeSniffer via pa11y, WCAG2AA). The first pass left 7
  pages unread on engine timeouts; `-full` is the complete run and is the one
  reported.
- `verify/arm1-targets.jsonl` — every interactive target measured, with size and
  whether it sits inline in text. Exploratory; it exists because the checklist's
  24 px item cannot separate a compliant hidden control from an undersized one.
- `analysis/power.json` — post-hoc power of the design, simulated. The sample
  size was justified by collection feasibility and never by detectable effect
  size; this file says what the design could see.
- `ERRATA-study1.md` — the erratum itself.

## What did not change

No published result is retracted or revised. The primary outcome, its effect
sizes and its confidence intervals stand as published. What the erratum corrects
is the description of what was measured, and it adds a limitation that was never
stated.

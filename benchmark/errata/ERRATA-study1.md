# Erratum — Study 1 (A11Y.md efficacy benchmark)

**Registration:** [osf.io/pg6r5](https://osf.io/pg6r5) · **Dataset:**
[10.5281/zenodo.22073026](https://doi.org/10.5281/zenodo.22073026) ·
**Issued:** 2026-09-10

## What was wrong

The registered protocol defines the violation outcome as **two** instruments
(§Measurement): axe-core, and a **deterministic per-task checklist** mapped to
WCAG success criteria. It also registers a **second independent scanner** as a
robustness check.

Only axe was ever run. The checklist exists in the repository
(`benchmark/harness/index.html`), written for a browser driven by hand; when
collection moved from hand-driven sessions to the API in August, it stopped
being executed and nobody noticed. The second scanner was never added at all.

**The published results are therefore complete on one instrument and silent on
two.** No published number is wrong. The description of what was measured is
incomplete, and it stayed that way through a DOI.

## What was done about it

Both instruments were run over the same 400 pages, unmodified, from the
published dataset. The checklist was **not rewritten**: it is lifted verbatim
out of the registered harness by `verify/extract-checklist.py` and injected into
each page under Playwright, because a reimplementation would have produced a
similar number measuring something else.

### Co-primary outcome nº 2 — deterministic checklist

Pass rate over applicable items, n=100 per condition, 0 pages unreadable:

| Condition | Pass rate |
|---|---|
| A — bare | 67.0% |
| B — generic request | 89.5% |
| C — placebo standard | 79.1% |
| **D — A11Y.md** | **92.1%** |

D − A = **+25.1 pp** · D − C = +13.0 pp · D − B = +2.6 pp

Item by item, A → D: associated `<label>` 50% → 98%; live region for dynamic
feedback 0% → 89%; native elements instead of clickable divs 91% → 100%;
redundant ARIA 0 occurrences in every condition; 24×24 px target size
90% → 76%.

**This outcome agrees with the published axe result and strengthens it.**

### Robustness — second engine

HTML_CodeSniffer (via pa11y, WCAG2AA), errors per page, 7 pages unreadable by
the engine:

| Condition | Errors per page |
|---|---|
| A — bare | 2.27 |
| B — generic request | **0.92** |
| C — placebo standard | 1.22 |
| D — A11Y.md | 1.59 |

**On the raw count this engine does not agree with the primary.** It puts D
ahead of the bare condition and behind both the generic request and the
placebo, where axe put D ahead of all three. That disagreement is the finding
and it is not qualified away. What the raw count does not show is that the
errors are not of one kind, so the same 1,006 error instances are also reported
here by the criterion that raised them:

| Error category | A | B | C | D |
|---|---|---|---|---|
| Contrast (SC 1.4.3) | 140 | **35** | 95 | 91 |
| Control has no accessible name (H91, F68) | 80 | 2 | 17 | **2** |
| Link to a non-existent anchor (SC 2.4.1) | 0 | 47 | 3 | **62** |
| Other | 7 | 3 | 5 | 4 |
| **Total** | **227** | **87** | **120** | **159** |

Three things follow, and they point in different directions:

1. **On the most severe category, D ties the best arm and nearly eliminates the
   defect.** Controls with no accessible name — a button or field a screen
   reader cannot announce — fall from **80 occurrences to 2**, the same figure
   as the generic request. The second engine agrees with the primary here.
2. **The largest single component of D's disadvantage is not an accessibility
   failure.** 62 of its 159 errors are internal links whose anchor does not
   exist in the page (`Shop Vase` → `#shop-vase`). The pages are standalone
   files generated without a backend, and the richer a page is, the more such
   links it carries: the bare condition has **zero** because it generates almost
   no links at all. The engine files these under SC 2.4.1 because the technique
   it checks is about bypass links; the skip links themselves resolve correctly.
   Excluding this category: A 227, B 40, C 117, **D 97**.
3. **Contrast is where the standard does not deliver, and this is a real
   result.** D improves on the bare condition by 35% (140 → 91) but stays well
   behind the generic request (35), and 45 of its 91 contrast errors are on
   buttons. A one-line request produces conservative pages with a safe palette;
   a long standard produces richer interfaces with more coloured surfaces to get
   wrong. Normalised per text element the ordering is the same: A 11.16,
   B 2.40, C 6.12, D 4.72 errors per 100 elements.

Point 3 independently reproduces, with a different engine, the weakness that
led the project to add `tools/contrast-check.py` in v2.0 — contrast as
deterministic arithmetic rather than a rule the model is asked to honour. That
tool did not exist in the version tested here.

### The 24 px target-size item, and why it is not read as a finding

That item falls under condition D in every arm measured. The failing targets
were inspected individually. Most are visually-hidden skip links — a 1×1 px box
is the canonical way to hide a skip link until it takes focus, and A11Y.md
requires the skip link — or carousel dot controls, which sit under SC 2.5.8's
equivalent-control exception that the harness itself marks as needing human
judgment. Discounting both, the difference between conditions nearly
disappears. The item cannot separate a compliant hidden control from an
undersized button; that is a defect in the instrument, recorded in
`benchmark/DEVIATIONS.md`.

## Second correction: the design's detectable effect size was never calculated

`METHODOLOGY.md` justifies 400 generations by collection feasibility — *"free-tier
daily caps make this a multi-day collection"* — and nowhere by statistical power.
No sample-size calculation was made before collection, and none after. This
erratum supplies the post-hoc analysis (`analysis/power.py`, seed 20260914,
1,000 simulations per point) and labels it post-hoc: it does not justify the n
that was chosen, it states what that n allowed anyone to see.

The outcome is not normally distributed — it is a rare, over-dispersed count
(60–76% of pages score zero, variance several times the mean), so power is
simulated rather than derived: the observed reference condition is resampled, a
real reduction is applied by binomial thinning, and the difference is tested
exactly as the registered plan tests it.

**Probability this design would detect a real reduction, Study 1:**

| Real reduction | D − A | D − B | D − C |
|---|---|---|---|
| 20% | 8% | 8% | 13% |
| 30% | 24% | 18% | 23% |
| 40% | 41% | 28% | 38% |
| 50% | 65% | 41% | 60% |
| 60% | 84% | 65% | 82% |
| 70% | 96% | 82% | 94% |

**This reframes a published null.** The registered protocol calls D − B *"the
question that decides whether the project has a reason to exist"*. It was
published as null: IRR 0.76, p-Holm 0.45. That IRR is a **24% reduction**, and
the table above says this design would have detected a reduction that size in
roughly **one attempt in nine**.

The published null on D − B is therefore **not evidence that the standard fails
to beat a one-line request. It is evidence that this study could not answer the
question it called decisive.** Stated here because a limitation that happens to
favour the project must be published with the same discipline as one that does
not — and because a reviewer would find it on the first page.

The same applies to the extension arms reported separately: at n=100 per cell,
detection probability for a 30% reduction is 20% (Nemotron 3 Super) and 26%
(gpt-oss-20b). The Nemotron arm's null on the primary outcome is under-powered
by the same margin, which is consistent with the two other instruments finding
an effect there.

**What does not change:** every statistically significant result stands. Power
limits what a null means, never what a detected effect means. The Study-1
effects on D − A and D − C were large enough (62% and 66%) to sit in the
well-powered region of the table.

## What changes, and what does not

- **No published result is retracted or revised.** The primary outcome, its
  effect sizes and its confidence intervals stand exactly as published.
- **The claim of a two-instrument violation outcome is corrected**: until this
  erratum, it was one instrument.
- **The dataset is superseded by v2**, adding the checklist and second-engine
  outputs for all 400 pages so that both can be re-analysed independently.
- Study 2 and Study 3 use their own registered instruments and are not affected
  by this erratum.

## How this was found

While regression-testing an unrelated change to the analysis scripts for a
pre-registered extension arm. The same regression test found that both analysis
scripts had never run from a clean clone — a separate defect, corrected in the
same batch and documented in `DEVIATIONS.md`.

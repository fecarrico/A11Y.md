# The control standard — construction notes

`control-standard/` is condition C of the pre-registered design ([`METHODOLOGY.md`](METHODOLOGY.md)): the placebo. It exists to answer one objection — *"the improvement comes from having any long, well-organised technical standard in context, not from what A11Y.md says"* — and it can only answer it if it matches the real standard in everything except subject. This file documents how that matching was done, so the control can be audited and rebuilt. It lives outside `control-standard/` on purpose: the model's `read_file` tool is scoped to that directory, and these notes must never be readable by the subject of the experiment.

## Construction rules

1. **Subject swap, shape kept.** The control is a frontend *performance* standard (Core Web Vitals, budgets, rendering cost). Its core mirrors `docs/en/A11Y.md` section for section: a Principle Zero, three profiles, a severity model, an AI behavior contract, a §2.1 lazy-loading map, a four-letter technical framework, anti-patterns, a verification workflow, and the same three lifecycle templates (report, exceptions, decisions).
2. **Same mechanics, same invocation.** Same `references/` + `templates/` layout, same trigger-map table format, same MUST/severity language, and a grounding sentence that is condition D's sentence with the subject swapped (see `collect.py`). If the control were a single flat document, condition C would have one read round-trip where D has several — and the comparison would measure process shape, not content.
3. **Size parity within ~5% per task.** Parity is measured as core + the guide(s) the §2.1 map selects for each benchmark task, not core alone. Measured at construction (chars, `docs/en` vs `control-standard`):

   | Load | delta |
   |---|---|
   | core alone | −3.5% |
   | per task (10 tasks) | −3.2% … −5.4% |

   The control runs consistently *slightly lighter*. Direction of bias: a lighter placebo makes any "long document effect" marginally weaker in C, which marginally favors D in the D−C contrast. It is declared here rather than hidden; anyone tightening the parity further should add performance content, never padding.
4. **Zero accessibility content.** No accessibility vocabulary, no assistive-technology concepts, no `alt`, no semantics-as-accessibility framing — verified by word-boundary sweep (`grep -rinwE "accessibility|accessible|aria|a11y|wcag|screen readers?|alt|focus|keyboard|contrast|semantics?"`). The control must be *silent* on the subject, not prescriptive in either direction: even an `alt=""` in a code example teaches something the placebo must not teach.
5. **Content must be real.** The performance guidance is meant to be sound — a model that follows it should produce genuinely faster pages. A placebo of plausible-looking nonsense would be detectable by the model and would test "good standard vs bad standard" instead of "this subject vs another subject".
6. **Guide-for-guide pairing on the benchmark tasks only.** The control has 11 guides — the ones the 10 tasks can trigger — not counterparts for all 29 of the real standard's guides. The §2.1 asymmetry beyond those rows (e.g. A11Y.md's cognitive guide, which its core text pulls into form tasks) is part of what is being measured: the standards legitimately differ in what they tell the agent to load, and the loading-behaviour outcome records it.

## Known asymmetries (declared)

- The real standard's core can instruct loading files outside the task's map row (the pilot showed `guide-cognitive.md` pulled into a form task by a core rule). The control's core has no equivalent cross-pull; its per-task load is more predictable. This shows up in the loading-behaviour outcome, where it belongs.
- The real standard is public and may be in training data; the control was written for this benchmark and cannot be. This asymmetry favors *the control being followed less fluently* and is listed in the methodology's limitations.

## Maintenance

The control is frozen with the protocol. If `docs/en/A11Y.md` changes enough to move parity beyond the declared tolerance, the control is re-paired **before** the next collection wave and the change is logged in `DEVIATIONS.md`; it is never touched mid-wave.

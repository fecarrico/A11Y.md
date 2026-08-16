# Performance Decisions Log (Template)

> One entry per choice between viable strategies with different performance profiles (Decision Memory, `PERF.md` §2). The log exists so the next task at the same scale **reuses** the decision instead of re-deriving or contradicting it. Newest first.

---

## [YYYY-MM-DD] — [Component or route]

- **Decision:** [e.g., Virtualized rows over pagination for the audit table]
- **Trigger / scale:** [what made this a decision — e.g., dataset crosses 500 rows in production]
- **Alternatives priced:** [what else was viable and what it would have cost — bytes, frames, requests]
- **Crossover:** [the condition under which this decision flips — e.g., "if rows become variable-height, revisit: measurement cost changes the math"]
- **Cost accepted:** [what this choice pays — e.g., +6 KB virtualization helper on the route]
- **Owner:** [who confirms this stays right as the product grows]

---

## Example

## 2026-08-10 — /reports data grid

- **Decision:** Canvas rendering for the 40k-point scatter; SVG kept for the ≤ 200-element summary charts.
- **Trigger / scale:** Production series grew past 10k points; SVG hover latency crossed 200 ms.
- **Alternatives priced:** SVG with decimation (still 4k nodes, 90 ms style cost); WebGL (overkill below 100k, +38 KB runtime).
- **Crossover:** Revisit at sustained >100k points or if per-point interaction is required (canvas hit-testing budget: 2 ms).
- **Cost accepted:** Own hit-testing code (+1.2 KB); tooltips reimplemented over canvas.
- **Owner:** frontend platform.

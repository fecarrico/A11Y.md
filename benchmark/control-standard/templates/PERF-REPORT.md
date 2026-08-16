# Performance Verification Report (Template)

> Generated from `templates/PERF-REPORT.md` before any delivery to an end user (`PERF.md` §2, Release Evidence). One report per delivery; the report is **versioned with the code it describes** and must be newer than the last interface change. Status may be ✅ PASS, ⚠️ CONDITIONAL (open exceptions referenced), or ❌ FAIL — a report claiming PASS while carrying unchecked items is invalid.

## 📌 Measurement Context

- **Date / build:** [YYYY-MM-DD · commit or tag]
- **Profile in force:** [🛡️ Strict | ⚖️ Standard | 🚀 Launchpad] — budgets from `PERF.md` §0.1
- **Baseline device/network:** [e.g., 4× CPU throttle, Fast 3G, cold cache — state exactly what "throttled" meant]
- **Tooling and versions:** [Lighthouse X.Y, browser build, RUM source if field data is cited]
- **Who measured:** [person/agent — and which items below they could not reproduce]

## 1. Core Web Vitals (lab, at the profile percentile)

| Metric | Budget | Measured | Verdict |
| :--- | ---: | ---: | :--- |
| LCP | [from profile] | [ ] | [ ] |
| INP (worst primary interaction) | [from profile] | [ ] | [ ] |
| CLS (load + primary interactions) | [from profile] | [ ] | [ ] |

- [ ] Measured under the declared throttle, not on development hardware.
- [ ] LCP element named: [which element] — discoverable in initial HTML: [yes/no]

## 2. Weight

| Measure | Budget | Measured |
| :--- | ---: | ---: |
| JS per route (compressed) | [ ] | [ ] |
| Total transfer, first view | [ ] | [ ] |
| Coverage: unused JS/CSS on first load | — | [ %] |

- [ ] No route exceeds its budget, or the overage is logged in `PERF-EXCEPTIONS.md`: [IDs]

## 3. Critical Path

- [ ] Every render-blocking resource enumerated; each one justified or deferred.
- [ ] No synchronous third-party script; third parties listed in `PERF-DECISIONS.md`.
- [ ] Fonts: display strategy set; preloads limited to above-the-fold faces.

## 4. Main Thread

- [ ] Load trace: no task over the profile ceiling. Longest task: [ms, where].
- [ ] The three primary interactions traced; handlers within INP budget.
- [ ] Scroll/input listeners passive where they never prevent default.

## 5. Stability & Loading States

- [ ] Async content arrives into reserved space (dimensions/aspect-ratio verified).
- [ ] Loading states: matched skeletons, failure and timeout paths render.
- [ ] Degraded-network pass completed (cache disabled, declared throttle).

## 6. Lifecycle

- [ ] Repeat view: hashed assets from cache; repeat LCP beats first-view LCP.
- [ ] Timers and observers owned: cleared on teardown, gated on `document.hidden`.
- [ ] Long-lived pages: heap steady across ten minutes of representative use.

## 📝 Open Items & Blockers

[Every `[ ]` above that stays open at delivery is listed here with its reason and its owner — an unchecked item with no owner is a FAIL, not a note.]

**Status:** [✅ PASS | ⚠️ CONDITIONAL — exceptions: PEX-… | ❌ FAIL]

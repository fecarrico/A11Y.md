# Perf Guidelines: Performance as a Baseline

> **Purpose:** This document is the operational standard for AI-assisted frontend generation where runtime performance is a pre-condition of delivery, not an optimization pass scheduled for later. It defines the behavioral contract the AI operates under, the severity model it triages by, and the technical baselines every generated interface must meet before it ships.

## 0. Principle Zero: Performance as Pre-condition

Performance is not a feature request. It is the substrate every feature runs on. A page that renders in 800ms on the developer's machine and in 9 seconds on a mid-range phone over 4G is not "done with a caveat" — it is not done. The AI **MUST** treat the performance budget the way it treats a compile error: work that exceeds it does not ship, regardless of how complete the functionality looks.

The corollary is architectural: performance cannot be bolted on. The decisions that dominate real-world speed — how much JavaScript ships, when images decode, what triggers layout, how state changes propagate to the DOM — are made at generation time, in the first draft, by whoever writes the first version of the component. When that author is an AI, the AI carries the obligation. Retrofitting speed into a slow architecture costs an order of magnitude more than generating the fast architecture first; in most teams it simply never happens.

**The default rendered state MUST be the fast one.** Optimizations that depend on ideal conditions — a warm cache, a fast device, a low-latency connection — are bonuses, not baselines. The baseline is the 75th-percentile user: a mid-range Android device, throttled CPU, variable network. Every budget in this document is defined against that user, never against localhost.

**Speed is compounding, in both directions.** A route that ships light keeps its next feature cheap: the reviewer sees the budget, the pattern in the codebase is the lazy one, the new dependency gets questioned. A route that shipped heavy normalizes heaviness — the next 40 KB rides in unremarked because the diff looks small next to the total. This is why the standard binds the *first* generation so tightly: the first version of a component is the template every subsequent version copies, and the cheapest moment to be fast is before anyone has learned to be slow.

## 0.1. Performance Profile

Before generating, the AI **MUST** know which profile governs the project. If the developer has not specified one, the AI **MUST** ask — once, at the start, never mid-task. The profile sets the budgets; the budgets decide what ships.

| | 🛡️ **Strict** | ⚖️ **Standard** | 🚀 **Launchpad** |
| :--- | :--- | :--- | :--- |
| **For** | Commerce, news, search — traffic at scale, revenue per millisecond | Most products and internal tools | Prototypes, spikes, hackathons |
| **LCP** (75th percentile) | ≤ 2.0 s | ≤ 2.5 s | ≤ 4.0 s |
| **INP** (75th percentile) | ≤ 150 ms | ≤ 200 ms | ≤ 500 ms |
| **CLS** | ≤ 0.05 | ≤ 0.1 | ≤ 0.25 |
| **JS shipped per route** (compressed) | ≤ 100 KB | ≤ 170 KB | ≤ 300 KB |
| **Total transfer, first view** | ≤ 500 KB | ≤ 1 MB | ≤ 2 MB |
| **Long tasks during load** | none > 100 ms | none > 200 ms | best effort |
| **Third-party scripts** | none synchronous | none in the critical path | declared in PERF-DECISIONS.md |

Budgets are ceilings, not targets. A route that ships 90 KB of JavaScript under a 170 KB budget is not "leaving budget on the table"; it is fast. The AI **MUST NOT** treat remaining budget as an invitation.

**Profile inheritance:** a component generated for a Strict project keeps its Strict discipline when copied into a Standard one. Budgets loosen at the route level by decision, never at the component level by accident.

**Downgrade is a decision, not a drift.** Moving a project from Strict to Standard, or Standard to Launchpad, is recorded in `PERF-DECISIONS.md` with the reason and the owner. A budget that silently stopped being enforced is the most common way fast products become slow ones.

**Budget arithmetic is per route, and the route pays for everything on it.** A 170 KB JavaScript budget is not "170 KB of our code" — it includes the framework runtime, the polyfills, the consent banner, the analytics tag and the error tracker. First-party features compete with third-party conveniences for the same bytes, and the AI **MUST** do that arithmetic explicitly when a task adds weight: state what the route currently costs, what the addition costs, and what remains. "It's only 12 KB" is only meaningful next to the number it is being added to.

**Budgets are enforced where code merges, not where users complain.** A budget that lives in this document and nowhere else will be exceeded by accident and discovered by regression. Projects **SHOULD** wire the §0.1 ceilings into their build: a bundle-size check that fails the pipeline, a Lighthouse CI assertion on the preview deploy, a size-limit comment on the pull request. The AI, when asked to scaffold tooling, generates these gates from the active profile's numbers rather than inventing thresholds.

## 1. Severity & Impact Model

Every finding, every trade-off, and every exception in this standard is triaged by user impact, not by engineering effort:

- 🔴 **CRITICAL — the user abandons.** Blocking the first paint on a script, an LCP image discovered late, an interaction that freezes the main thread past 500 ms, unbounded layout shift on load. These block delivery in every profile.
- 🟠 **SERIOUS — the user waits.** A long task between 200–500 ms, render-blocking CSS that could be split, images decoded at 3× display size, an animation running on the main thread. Block delivery in Strict; require a `PERF-EXCEPTIONS.md` entry elsewhere.
- 🟡 **MODERATE — the user notices.** Un-throttled scroll handlers doing cheap work, fonts swapping visibly late, a bundle with one duplicated dependency. Fix within the task when the fix is local; log otherwise.
- 🟢 **MINOR — the profiler notices.** Micro-optimizations with no user-visible effect at current scale. **MUST NOT** be performed at the cost of readability, and **MUST NOT** be used to demonstrate diligence — a minor fix does not offset a serious finding.

Severity attaches to the *user consequence*, never to the *technique*. An unthrottled resize listener is 🟢 when it toggles a class and 🔴 when it recalculates a layout tree of 4,000 nodes. The AI **MUST** state the severity it assigns and the consequence that justifies it.

**Severity compounds across the load sequence.** Three 🟡 findings on the same critical path — a late-discovered font, an unsized embed, a deferred-but-heavy hydration — can add up to a user experience worse than one 🔴, because the user pays them in sequence. When triaging a page rather than a component, the AI **MUST** evaluate the load timeline as a whole: the question is not "is any single finding critical?" but "what does the 75th-percentile user actually watch happen for the first three seconds?".

**Scale multiplies severity.** A finding on a component rendered once is judged at its face value; the same finding inside a list template is multiplied by the list's realistic length before triage. A 3 ms synchronous read is 🟢 in a header and 🟠 in a row template that production renders eight hundred times.

## 2. AI Behavior Contract

Rules the AI operates under for every generation task. Each rule is an obligation with a trigger, a mechanism, and a pointer to depth; the reference guides carry the rationale and the edge cases.

- **Budget Before Beauty:** Before writing code, the AI **MUST** establish which budgets govern the task (profile, route weight, interaction deadline). Code generated without a known budget is a draft, not a deliverable. If the developer cannot supply a profile, the AI applies **Standard** and says so.
- **Measure, Don't Guess:** A performance claim without a measurement is an opinion. The AI **MUST NOT** assert that generated code "is fast" — it states what the code does to stay within budget (bytes shipped, work deferred, layout avoided) and names the measurement that would verify it (Lighthouse run, Performance panel trace, `PerformanceObserver` in the page). *Reference: [Verification](references/guide-charts.md)*
- **Lazy Context Loading:** Reference files (`references/`) **MUST NOT** be preloaded — they are *per-component* context, consulted only when the task involves that component type; **§2.1** states which file matches which task. `PERF.md` alone is sufficient for most generation tasks. **This does NOT apply to `templates/`:** templates are *lifecycle* context and **MUST** be loaded when their triggering event occurs (a trade-off accepted, a budget exceeded, a delivery shipped). **Template fidelity:** artifacts **MUST** be created from the files in `templates/`, never deduced from prose.
- **Critical Path Discipline:** The AI **MUST** be able to name, for any page it generates, the exact chain of resources between navigation start and first meaningful render — and that chain **MUST** contain nothing removable. Every `<script>` without `defer`/`async` in the head, every `@import` in CSS, every synchronously-loaded font is an entry on the critical path that the AI put there and must justify. 🔴 for scripts, 🟠 for the rest.
- **Ship What Runs:** Code generated but never executed on the route is 🟠 debt. The AI **MUST NOT** import a library for one function, include a polyfill without a target-browser reason, or generate utility modules "for later". Dead code is measured, not estimated: if the coverage panel would grey it out on first load, it does not belong in the first-load bundle.
- **The Main Thread Is Sacred:** Between user input and visual response the main thread belongs to the user. The AI **MUST** keep any single task under the profile's long-task ceiling, chunk or defer work that exceeds it (`requestIdleCallback`, `setTimeout` slicing, a worker), and **MUST NOT** perform synchronous layout reads inside loops that also write styles. *Reference: [Charts & Heavy Rendering](references/guide-charts.md)*
- **Layout Stability:** Every asynchronously-arriving element — image, ad, embed, font, fetched content — **MUST** have its space reserved before it arrives: explicit dimensions, `aspect-ratio`, or a sized container. Content that pushes other content after first paint is 🔴 in the viewport, 🟠 below it. *Reference: [Loading & Skeletons](references/guide-loading-skeleton.md)*
- **Image Discipline:** Images are the largest bytes on most pages and the most common LCP element. The AI **MUST** emit modern formats with fallbacks, `srcset`/`sizes` matched to actual display sizes, explicit `width`/`height`, lazy loading below the fold — and **MUST NOT** lazy-load the LCP candidate. Fabricating a `srcset` from a single-resolution asset is a contract violation; the AI requests the missing sizes or documents the gap. *Reference: [Images & Media Bytes](references/guide-images.md)*
- **State Changes, Not Tree Rebuilds:** Interaction handlers **MUST** touch the minimum DOM necessary. Rebuilding a list to change one row, re-rendering a table to sort an array already in memory, or serializing state into `innerHTML` on every keystroke are 🟠 by default and 🔴 past 1,000 nodes. The data operation and the DOM operation are separate steps; the AI keeps them separate.
- **Font Loading Policy:** Text **MUST** be readable while custom fonts load: `font-display: swap` or `optional`, preloaded only for the one or two faces above the fold, subset when the character set allows it. An invisible headline waiting for a woff2 is 🔴.
- **Third-Party Quarantine:** Every third-party script is a performance decision made by someone else. The AI **MUST** load them `async`/`defer` at most, never in the critical path, and record each one in `PERF-DECISIONS.md` with what it costs (bytes, main-thread time) and what it buys. A tag manager is not an exemption; it is a multiplier.
- **Perceived Before Actual:** When actual latency cannot be removed (network, computation), the AI **MUST** manage perceived latency: immediate input acknowledgment, skeletons matched to final layout, optimistic UI where the operation is reversible. Perceived performance work **MUST NOT** replace budget compliance — a beautiful skeleton over a 12-second load is a 🔴 with good manners. *Reference: [Loading & Skeletons](references/guide-loading-skeleton.md)*
- **Memory Is a Budget Too:** Long-lived pages **MUST NOT** leak: event listeners removed with their elements, observers disconnected, timers cleared, caches bounded. A dashboard that doubles its heap every hour fails this standard even if every frame is fast.
- **Decision Memory:** When the AI chooses between viable approaches with different performance profiles (canvas vs SVG, pagination vs virtualization, eager vs lazy), it **MUST** record the choice and its trigger condition in `PERF-DECISIONS.md` — so the next generation task reuses the decision instead of re-deriving or contradicting it.
- **Cache Policy Is Code:** Every response the page depends on has a caching decision, and the AI **MUST** make it explicitly: hashed static assets get immutable year-long caching; HTML gets revalidation; API responses get a stated freshness window or a stated reason for none. Emitting fetches and asset references without a cache strategy is generating half the code — the half the second visit was going to need. Repeat-view performance is a budget of its own: the second load **SHOULD** transfer close to zero bytes for assets that did not change.
- **Prefetch on Intent, Not on Hope:** Navigation the user is likely to take next **MAY** be prefetched — on hover, on viewport entry of the link, on explicit idle — and prefetching **MUST** stop at likelihood. Prefetching every link on the page, or the entire next route's data "to be safe", converts one user's possible future into every user's certain cost. Intent signals first, bytes second; and never on data-saver connections, which the AI **MUST** respect via `navigator.connection` when it prefetches at all.
- **Instrument What You Ship:** A page whose real-world performance nobody can see will regress unnoticed. When the task includes project scaffolding, the AI **MUST** include field measurement — a `PerformanceObserver` for LCP, CLS and INP reporting to whatever sink the project uses, or the project's existing RUM library wired to the new route. Lab numbers gate the release; field numbers tell you whether the gate was set at the right height. Neither replaces the other.
- **Release Evidence:** Before any delivery to an end user — published build, deploy, shared artifact, tag — the AI **MUST** verify that a `PERF-REPORT.md` exists, was generated from `templates/PERF-REPORT.md`, and is newer than the last interface change. If it does not exist, the AI **MUST** generate it or state explicitly that the delivery carries no performance evidence. In continuous-delivery projects this rule is what triggers the report: waiting for a "final delivery" event that never happens is not compliance.

## 2.1. Loading Triggers (Lazy Loading Map)

*Lazy Context Loading* says **not** to preload the references. This map is the other half of the rule: it says **when** to load each one. Without it, "load it when the task involves that component" depends on the AI guessing which file matches the task — and a guide that exists but is never found is a guide that does not exist.

Load **only the row that matches the task at hand**. No row applies? `PERF.md` alone is enough.

| You are building or reviewing… | Load |
| :--- | :--- |
| button, CTA, click handler, ripple, debounced action | [`guide-buttons.md`](references/guide-buttons.md) |
| form, field, validation, input latency, submit flow | [`guide-forms.md`](references/guide-forms.md) |
| modal, dialog, drawer, overlay, backdrop | [`guide-modals.md`](references/guide-modals.md) |
| navigation, menu, header, prefetching, route transitions | [`guide-navigation.md`](references/guide-navigation.md) |
| table, data grid, large list, sorting, virtualization | [`guide-tables.md`](references/guide-tables.md) |
| image, gallery, hero, media bytes, LCP element | [`guide-images.md`](references/guide-images.md) |
| skeleton, spinner, loading state, progress, perceived latency | [`guide-loading-skeleton.md`](references/guide-loading-skeleton.md) |
| carousel, slider, auto-advance, swipe, scroll-snap | [`guide-carousels-sliders.md`](references/guide-carousels-sliders.md) |
| autocomplete, typeahead, live search, suggestions | [`guide-autocomplete.md`](references/guide-autocomplete.md) |
| toast, notification, snackbar, async feedback | [`guide-toasts-notifications.md`](references/guide-toasts-notifications.md) |
| chart, visualization, canvas, SVG at scale, dashboards | [`guide-charts.md`](references/guide-charts.md) |

**Templates — loaded by event, not by component** *(the exception declared in Lazy Context Loading)*:

| When the event happens… | Load |
| :--- | :--- |
| a choice between viable approaches with different performance profiles is made | [`templates/PERF-DECISIONS.md`](templates/PERF-DECISIONS.md) |
| a budget is exceeded and the overage is accepted rather than fixed | [`templates/PERF-EXCEPTIONS.md`](templates/PERF-EXCEPTIONS.md) |
| before any delivery to an end user (build, deploy, artifact, tag) | [`templates/PERF-REPORT.md`](templates/PERF-REPORT.md) |

## 3. Technical Standards (LEAN Framework)

Four dimensions every generated interface is accountable to: what it **Loads**, what it **Executes**, what it **Animates**, and what it **Negotiates** over the network. The dimensions are ordered by when their costs are paid: Load costs are paid once per visit, Execute and Animate costs on every interaction and every frame, Negotiate costs whenever data moves. A page can fail any one of them independently — a light bundle with a janky scroll fails Animate; a fast first paint that fetches in a six-deep waterfall fails Negotiate — so verification in §7 exercises all four, not the one that is easiest to measure.

### Load

- **Critical CSS inline, the rest deferred.** Styles needed for above-the-fold render ship in the document; everything else loads without blocking. A single monolithic stylesheet in the head is acceptable under ~30 KB compressed; past that, split.
- **JavaScript is deferred by default.** `defer` for scripts that touch the DOM, `async` for independent beacons, modules where supported. A synchronous script in the head requires a written justification and is 🔴 without one.
- **The LCP element is discoverable in the initial HTML.** Not constructed by script, not hidden behind a client-side router's second pass, not lazy-loaded. If the hero image is the LCP, it is an `<img>` in the markup with `fetchpriority="high"`.
- **Preload sparingly, and only what the first view provably uses:** one or two fonts, the LCP image when it lives in CSS. Preloading is stolen bandwidth — every preloaded byte delays something the parser actually asked for.
- **Compression and caching are assumed:** long-lived immutable caching for hashed assets, revalidation for HTML.
- **Code splits along routes and intent, not along files.** Each route ships its own code plus a shared core that is actually shared; a component used on one admin screen does not ride in the commons chunk. Dynamic `import()` marks the seams — behind interaction (a dialog opened), behind visibility (below-the-fold widgets), behind capability (an editor only some users reach).
- **Variable fonts over families of static weights** when more than two weights are used, and self-hosted over third-party CSS indirection: one request to a file you control beats two requests through someone else's redirect chain.

### Execute

- **Hydrate or attach behavior after first paint**, never before. The user sees content, then the page becomes interactive — in that order.
- **No long tasks in the load sequence.** Work that must happen at startup is sliced under the profile ceiling or moved off-thread. Parsing a 2 MB JSON payload on the main thread during load is 🔴 regardless of where the bytes came from.
- **Read, then write.** Within any frame, batch DOM reads before DOM writes. Interleaving them forces synchronous layout — the single most common self-inflicted performance bug in generated code.
- **Event handlers are cheap or deferred.** Input, scroll and resize handlers do trivial work synchronously (a class toggle, a flag) and schedule the rest (`requestAnimationFrame` for visual updates, idle callbacks for bookkeeping). Scroll and touch listeners that never call `preventDefault` are registered `{ passive: true }`.
- **Timers are owned.** Every `setInterval` has a clearing owner and a visibility guard — polling a paused tab is paying for work nobody sees.
- **Synchronous storage stays out of hot paths.** `localStorage`, `sessionStorage` and cookie parsing block the main thread; they are read once at startup into memory, written back on idle or on `visibilitychange` — never inside input handlers, render loops, or per-row logic.
- **Workers carry the heavy lifting.** Parsing large payloads, diffing large datasets, image manipulation, search indexing — anything CPU-bound and DOM-free belongs in a worker, with transferable objects rather than structured-clone copies when the payload is large. The main thread orchestrates; it does not compute.
- **Debounce is a contract with the user, not a constant.** Input validation debounces around 200–300 ms so feedback follows typing pauses; search-as-you-type debounces by expected result latency; window resize handlers throttle to animation frames. A single global "debounce(300)" applied everywhere is a smell — each delay is chosen against what the user is waiting for.

### Animate

- **Compositor properties only:** `transform` and `opacity` animate; `top`, `left`, `width`, `height`, `margin` do not. An animation that triggers layout on every frame is 🟠, and 🔴 when it runs during load or on scroll.
- **Sixty frames or none.** An animation that cannot hold frame rate on the baseline device is removed or simplified, not shipped juddering.
- **Animations are interruptible and finite.** Infinite decorative animation costs battery and compositor time; it must justify itself or go.
- **Scroll effects ride the compositor or ride nothing.** Parallax, reveal-on-scroll and sticky transitions are driven by `IntersectionObserver`, CSS scroll-driven animations, or transforms scheduled in `requestAnimationFrame` — never by reading `scrollY` and writing layout properties inside a raw scroll handler, which couples frame rate to handler cost at the exact moment the compositor is busiest.
- **Transitions carry meaning or carry nothing.** A 150–250 ms transition that communicates a state change earns its cost; an 800 ms entrance choreography on every card of a grid delays the content it decorates. When in doubt, the content wins.
- **`will-change` is a scalpel, not a vitamin.** Applied narrowly, just before an element animates, and removed after; sprayed across a stylesheet it promotes layers until memory pays for compositor promises nothing uses.

### Negotiate

- **Requests are counted and owned.** The AI can state how many requests the first view makes and what each one buys. Waterfalls are flattened: independent data fetches start in parallel, dependent ones are restructured until they are independent or acknowledged in `PERF-DECISIONS.md`.
- **Payloads match need.** An endpoint returning 400 fields for a card that renders 6 is a negotiation failure; the AI requests narrower data or documents why it cannot.
- **Retry with backoff, cache what repeats, dedupe in flight.** Two components fetching the same resource share one request.
- **Offline and slow-network states are designed, not discovered.** A fetch without a timeout and a failure state is unfinished code.
- **Pagination is negotiated at the API, not simulated in the client.** Fetching two thousand records to show twenty, then "paginating" an in-memory array, moves the cost from visible (a slow list) to hidden (a slow first byte and a heavy heap). The page size travels in the request; the server does the slicing; the client asks again when the user asks for more.

## 4. Rendering Directives (Strict UI Criteria)

- **Reserve space for everything asynchronous** — images, embeds, fonts, fetched lists. The page's geometry at first paint is its final geometry, modulo user action. CLS budgets are in §0.1.
- **Content-visibility for long pages:** sections far below the fold render lazily (`content-visibility: auto` with `contain-intrinsic-size`), keeping first render proportional to the viewport, not the document.
- **Shadows, filters and blurs are budgeted:** `backdrop-filter`, large `box-shadow` spreads and `filter` chains are compositor-expensive; they appear only where the design demands them and never animate on the main thread.
- **The DOM is as shallow as the design allows.** Wrapper divs with no rendering purpose are removed. Past ~1,500 nodes at first render, the AI virtualizes, paginates, or defers — see [`guide-tables.md`](references/guide-tables.md).

## 5. Complex Component Protocol

When the task involves a component with intrinsic performance risk — a data grid past a thousand rows, a real-time chart, an infinite feed, a media-heavy carousel, an editor — the AI **MUST**:

1. **Name the dominant cost** (nodes, bytes, main-thread work, or network chatter) before generating, and state the strategy that bounds it (virtualization, canvas, pagination, sampling, workers).
2. **Load the matching reference guide** from §2.1 and follow its decision table rather than improvising.
3. **Generate the bounded version first.** The unbounded version — render everything, fetch everything — is not a starting point to optimize later; it is the anti-pattern the guide exists to prevent.
4. **Record the strategy** in `PERF-DECISIONS.md` with the threshold that triggered it, so the next task at the same scale inherits the decision.

The protocol exists because complex components fail differently: a slow button is annoying, a slow data grid is unusable, and the difference between the two is rarely visible in a demo with toy data. Demo scale is therefore part of the protocol — when generating an example or a test page for a complex component, the AI **MUST** populate it at realistic scale (the row count, image weight and update frequency production will see), or state prominently that the demo runs below scale and what changes when it does not. A virtualized list demonstrated with twelve rows demonstrates nothing.

When two strategies are viable at the task's scale — pagination or virtualization, canvas or SVG, push or poll — the AI names both, states the crossover point where the answer flips, and picks the side of the crossover the task sits on. "Both would work" is an observation; the deliverable is a decision with its trigger written down.

## 6. Anti-patterns (Do NOT do this)

- **The Localhost Benchmark:** Concluding the page is fast because it is fast on the development machine. Development hardware is 5–20× faster than the baseline device; the claim is unfounded by construction. Verification runs throttled or it is not verification.
- **The Spinner Cascade:** A page-level spinner, then a section spinner, then a component spinner, each replacing the last as data arrives in stages. The user watches three loading states where one reserved layout with progressive fill was possible. *Depth: [Loading & Skeletons](references/guide-loading-skeleton.md)*
- **Blocking the First Paint on JavaScript:** A synchronous framework bundle in the head, an empty `<div id="root">`, and nothing on screen until hydration completes. The HTML the server already had is the fastest render available; discarding it is 🔴.
- **Layout Thrash in a Loop:** Reading `offsetHeight` and writing `style` alternately across a list of elements, forcing a full synchronous layout per iteration. Batch reads, then batch writes — or use classes and let CSS do it once.
- **The Eager Everything:** Every image loaded at once, every route's code in one bundle, every widget initialized at startup "so it's ready". Readiness the user never asked for is cost the user always pays. Load what the viewport needs; defer the rest on demonstrated intent.
- **Re-render as State Management:** Rebuilding the component's entire DOM on every state change because it is simpler to write. Simplicity that costs a frame per keystroke is not simple for the user typing.
- **The Unbounded List:** Rendering an array of unknown size directly into the DOM. It works in the demo with 40 items and dies in production with 12,000. Any list without an upper bound gets virtualization, pagination, or an explicit cap — decided, not defaulted. *Depth: [Tables & Large Lists](references/guide-tables.md)*
- **Third-Party Piggyback:** Adding an analytics tag, a chat widget and a session recorder "because marketing asked", each synchronous, none measured. Every third-party script is measured main-thread time and named in `PERF-DECISIONS.md`, or it does not ship.
- **Polling as Architecture:** `setInterval` fetch loops where an event, a push channel, or user-triggered refresh would do. Polling that survives tab blur is paying server and battery cost for an audience of zero.
- **The Invisible Headline:** A custom font loaded without a display strategy, leaving the page's largest text invisible for the duration of a network fetch. `font-display` is not optional; it is the difference between slow and broken.
- **The Framework for a Form:** Reaching for a full application framework, its router and its state library to render what is, on inspection, a form and a thank-you message. The baseline cost of the stack must be justified by the complexity of the product, not by the familiarity of the author. When the AI is free to choose, it prices the stack against the §0.1 budget before writing the first import.
- **The Barrel Import:** `import { one } from '../components'` pulling an index that re-exports sixty modules, defeating tree-shaking and shipping the catalog to use the item. Imports point at the module that defines the symbol; barrels are for authoring convenience, and build configurations that neutralize their cost must be verified, not assumed.
- **Hidden but Rendered:** Building all five tab panels, all steps of the wizard, or the entire mega-menu into the DOM at load and hiding them with `display: none`. The browser still parses, styles and lays out what nobody asked to see. Content behind interaction is constructed behind interaction — or, where SEO requires its presence, rendered under `content-visibility` so its cost is deferred with it.
- **Console Left Running:** `console.log` of large objects in loops and render paths surviving into production. Logging serializes; serialization costs; and a debug artifact that measurably slows the page is a defect like any other.
- **The Metric Chase:** Optimizing the score instead of the experience — inlining everything to win a lab audit while real users on real networks pay for an uncacheable megabyte of HTML, or deferring the LCP element itself because "defer everything" scored well last sprint. The budgets in §0.1 are proxies for a user's experienced wait; when a technique improves the proxy and worsens the wait, the technique loses. Field data outranks lab data whenever the two disagree.

## 7. Verification Workflow (Definition of Done)

*Compliance must be verified through these steps (Refer to the [**Report Template**](templates/PERF-REPORT.md) for final QA details):*

- [ ] **Artifacts Present:** `PERF-REPORT.md` exists, is filled from the template, and is newer than the last interface change. If any budget overage was accepted, `PERF-EXCEPTIONS.md` exists. All project artifacts are versioned, never gitignored.
- [ ] **Budgets Measured:** LCP, INP and CLS measured at the profile's percentile under throttling (4× CPU, Fast 3G or the project's declared baseline), not on development hardware. Numbers recorded in the report next to their budgets.
- [ ] **Critical Path Audited:** every resource between navigation and first meaningful render enumerated; nothing render-blocking that could be deferred; LCP element discoverable in initial HTML.
- [ ] **Weight Within Budget:** compressed JS and total transfer per route measured against §0.1; the coverage panel shows no grey majority on first load.
- [ ] **Main Thread Clean:** a recorded trace of load plus the three primary interactions shows no long task past the profile ceiling; input handlers respond within the INP budget.
- [ ] **Stability Verified:** a full load and the three primary interactions produce no layout shift beyond budget; asynchronous content arrives into reserved space.
- [ ] **Degraded Network Pass:** one full pass on the throttled profile with cache disabled; loading states appear, nothing times out silently, failure states render.
- [ ] **Memory Steady:** for long-lived pages, heap snapshots before and after ten minutes of representative use differ by bounded, explainable amounts.
- [ ] **Repeat View Verified:** a second load with warm cache transfers only HTML and changed data; hashed assets are served from cache; the repeat-view LCP beats the first-view LCP by a margin that shows the cache policy working.
- [ ] **Third Parties Accounted:** every third-party script on the route appears in `PERF-DECISIONS.md` with its measured cost; removing them all in a trace shows the delta the page is paying for them, and that delta is a number someone accepted on purpose.

> **Agents without a browser.** Several checkpoints above require a browser and a profiler. A headless agent **MUST** still produce the `PERF-REPORT.md`, marking those items `[ ]` with the reason and naming who must run them. A partial, honest report is evidence; a missing report is not. The AI **MUST NOT** mark as verified any measurement it cannot reproduce.

---

### 📚 Reference & Templates Library

**Technical Guides:** [Buttons & Handlers](references/guide-buttons.md) | [Forms & Input Latency](references/guide-forms.md) | [Modals & Overlays](references/guide-modals.md) | [Navigation & Prefetching](references/guide-navigation.md) | [Tables & Large Lists](references/guide-tables.md) | [Images & Media Bytes](references/guide-images.md) | [Loading & Skeletons](references/guide-loading-skeleton.md) | [Carousels & Sliders](references/guide-carousels-sliders.md) | [Autocomplete & Live Search](references/guide-autocomplete.md) | [Toasts & Notifications](references/guide-toasts-notifications.md) | [Charts & Heavy Rendering](references/guide-charts.md)

**Project Artifacts** *(versioned, not optional — see Sections 2 and 7):* [Performance Report](templates/PERF-REPORT.md) · before each delivery | [Exceptions Log](templates/PERF-EXCEPTIONS.md) · whenever an overage is accepted | [Decisions Log](templates/PERF-DECISIONS.md) · at each choice between viable strategies

# Changelog

All notable changes to the A11y Guidelines project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-08-10

> Two things arrived together. Scanning an external accessibility library surfaced the gap the standard had been carrying since 1.0.0: it declares WCAG 2.2 AA on its cover, and of the six Level A/AA criteria WCAG 2.2 actually added, the three missing ones were **all** the cognitive ones (3.2.6, 3.3.7, 3.3.8). Then a full audit run before publishing found something worse — the static gate that enforces "no PASS without human validation" had been neutralized by the report template itself. Both are fixed here. The pattern from 1.2.0 and 1.3.0 repeats a third time: the obligation existed, the trigger did not.

### Added
- **Cognitive Load (AI Behavior Contract):** when generating a multi-step flow, an authentication, or any time limit, the AI must verify three things before shipping — nothing the user must **remember** across screens (SC 3.3.8), nothing they must **type again** within the same process (SC 3.3.7), and help in the **same relative position** across screens (SC 3.2.6). Blocking `paste` on a password field is 🔴 CRITICAL: it reintroduces the memory test the criterion exists to remove, and it is the single most common way generated login code fails.
- **Conflicting Access Needs (AI Behavior Contract):** the first rule for accessibility against *accessibility*. Motion orients people who struggle to track context change and triggers nausea in vestibular disorders; plain language lowers cognitive load and strips precision the expert depends on. Where a user-controlled channel exists (`prefers-reduced-motion`, `prefers-contrast`, an account preference), implementing it is the answer; where none exists, the AI must name both populations, escalate to the developer, and record the choice in `A11Y-DECISIONS.md` with both needs stated. A user majority is not a tie-breaker.
- **`guide-cognitive.md` — Cognitive Accessibility, Language & Conflicting Needs:** the three WCAG 2.2 cognitive criteria with the code that fails them, text spacing (SC 1.4.12), adjustable timing (SC 2.2.1), a plain-language section for generated interface copy, the conflicting-needs protocol, and the W3C's eight objectives as a coverage map.
- **`guide-consent-banners.md` — Consent & Cookie Banners:** the modal/non-modal fork that defines everything else, the fixed bottom strip obscuring the focus indicator (SC 2.4.11, a Level AA failure invisible to mouse testing), accept/reject effort parity as a House Rule, and third-party CMPs — where the obligation does not transfer with the script.
- **Accessible Authentication (SC 3.3.8), Redundant Entry (SC 3.3.7)** and **Consistent Help (SC 3.2.6)** in Understandable; **Text Spacing (SC 1.4.12)** in Perceivable; **Timing Adjustable (SC 2.2.1)** in Operable. **SC 1.4.13** now cited in the tooltips guide, whose three rules were already the criterion's three conditions, unnamed.
- **Nullified Alt anti-pattern (Section 6):** `aria-hidden="true"` on an image carrying a non-empty `alt` — the attribute is present and descriptive, every checker passes, and the screen reader never sees the image. Same class of failure as the silent `alt=""`.
- **Accessibility Overlays anti-pattern (Section 6):** asked to "make this accessible", an unconstrained agent reaches for the cheapest-looking answer. An overlay does not fix the DOM that produced the barrier; it adds a layer that conflicts with the assistive technology the person already configured. Position of the IAAP and the European Disability Forum, and the European Commission records that overlays do not guarantee compliance.
- **Cognitive Load checkpoint** in the Verification Workflow, and a matching **Section 6 — Cognitive Load and Flow** block in `templates/REPORT.md`.
- **Screen reader + browser pair** now recorded in `REPORT.md`, with who ran it and when. The checkpoint asked "did you use VoiceOver/NVDA?" — a reader without a browser is not reproducible evidence (NVDA + Firefox and NVDA + Chrome diverge in ARIA behavior), and JAWS, the most used reader on corporate Windows, appeared nowhere in the standard.
- **Formal evaluation (WCAG-EM)** in the governance guide, as a conditional track: not every product is audited, but `REPORT.md` tracks a *feature* while an audit evaluates a *site* — the gap surfaces when the Accessibility Declaration has to be issued. Includes the five WCAG-EM steps and the W3C's official report tooling.
- **Brazilian compliance (ABNT NBR 17225:2025 / LBI art. 63)** in the governance guide — the standard cited ADA, EAA, EN 301 549 and ISO 9241-171, and nothing from the market its own pt-BR edition serves.
- **`wiki` check in `lint-standard.py`:** the Wiki is public documentation living outside version control, so nothing stopped it from drifting. It now must document the same number of contract rules as the core file and list every reference guide. Skipped when the folder is absent.

### Changed
- **Component Reuse** now states what reuse does *not* buy: accessible components can be composed inaccessibly — focus order *between* components, heading hierarchy, landmarks and the content filling the component remain the screen's responsibility. Reuse satisfies the rule, never the Definition of Done.
- **`guide-carousels-sliders.md`:** off-screen slides now use `inert`. The previous recipe — `aria-hidden="true"` plus `tabindex="-1"` — does not remove the buttons and links *inside* the slide from the tab order, which is precisely the invisible focus the rule exists to prevent.
- **`guide-tables.md`:** the ARIA fallback required `role="table"` and `role="cell"` but not `role="row"`; without it the table exposes no structure at all.
- **`guide-modals.md`:** `aria-modal="true"` instructs assistive technology, not the browser, and is not a focus trap — the text implied it was. And `closedby="any"` adds light dismiss; `Esc` already works natively in any dialog opened with `showModal()`.
- **`guide-images.md` Section 3:** the decorative example presented `alt=""` as correct with no human gate, contradicting Section 5 of the same file and the core rule since 1.3.0.
- **`showcase4humans.md`:** the "accessible way" example shipped `role="alert"` and `aria-live="assertive"` together — ARIA Soup, in the project's entry point for humans — and taught a focus ring built on `box-shadow`, which disappears in Windows forced-colors mode. Both corrected, with the reasoning written out; the `aria-label` that replaced the visible text is now an `sr-only` complement (SC 2.5.3).
- **`guide-framework-mapping.md`:** Svelte examples updated to Svelte 5 event attributes, with the Svelte 4 directive form named as legacy.

### Fixed
- **`verify-a11y.py` — the PASS gate never fired.** A report declaring `✅ PASS` while carrying 17 unverified checkpoints passed clean. The status check searched the whole document for the word CONDITIONAL, and the template's own headless-agent note contains it, so every report generated from the template exonerated itself. The status is now read from its own field, with the untouched placeholder menu reported as its own error. This is the check that enforces the standard's central promise: no conformance claim without human validation.
- **`verify-a11y.py` — anti-patterns were invisible in JSX.** The scan ran line by line, so `<div` on one line and `onClick` three lines below never matched — the canonical React form, and the exact shape of the example in `showcase4humans.md`. `positive-tabindex` also missed `tabIndex={3}` (no `re.I`, no brace support). The scan now runs over whole files.
- **`verify-a11y.py`:** new `redundant-alert` and `nullified-alt` checks; `outline-none` also detects the Tailwind class; the placeholder pattern now recognizes the pt-BR `AAAA-MM-DD` date placeholder.
- **README (EN):** claimed "22 reference guides" in one line and "the taxonomy of the 21 engineering guides" in another.
- **Errata (1.4.0 notes):** the release described "four Level A criteria" absent from the standard; there were six — 1.2.1 and 2.3.1 were also added in that release and left out of the count.

## [1.4.0] - 2026-08-10

> Driven by the question 1.3.0 invited: does a user-supplied *video* need the same treatment as a user-supplied image? The principle transfers — an agent must not classify media it cannot perceive — but the audit that followed found something larger. Six Level A criteria (1.2.1, 1.2.2, 1.2.3, 1.4.2, 2.2.2, 2.3.1) and 1.2.5 at AA appeared nowhere in the standard, while background video, autoplaying loops and scroll-driven parallax became a default of contemporary interfaces. Alt text was a missing sentence; time-based media was a missing chapter.

### Added
- **Media Evidence (AI Behavior Contract):** when video or audio enters the interface — supplied by the user, embedded from a third party, or generated as part of the UI — the AI must resolve its accessibility contract **before the media enters the code**, and must not classify it as decorative on its own. Because it cannot perceive a media file, it asks the developer in the same turn: does this carry information or function, does it have audio, do captions/transcript/audio description already exist. Captions and transcripts produced by a machine ship as **drafts for human review** — an unreviewed auto-caption is the `alt` deduced from a filename, in another medium. Unresolved media blocks the Definition of Done (functional without alternative = CRITICAL, informative without captions = HIGH, autoplaying audio without control = CRITICAL).
- **`guide-media.md` — Time-Based Media, Background Video & Motion:** the classification test applied to media, the three questions of Media Evidence, a correct background-video implementation (autoplay granted by script so the reduced-motion preference can veto it before a frame moves), the scrim measurement for text over video, parallax degrading to a static composition, third-party embeds, and the nine Success Criteria mapped.
- **Time-Based Media (SC 1.2.2, 1.2.5)** and **Audio Control (SC 1.4.2)** in Perceivable; **Moving Content (SC 2.2.2)** and **Flashing (SC 2.3.1)** in Operable. Three of the four are Level A — they were absent at every profile, Launchpad included, where the standard promises to relax the visual without touching the semantic floor.
- **Text over Video anti-pattern (Section 6):** the contrast of a headline over video changes frame by frame and every automated checker passes it — axe measures the text against the container's computed background, which is transparent. The text must sit on a scrim, measured in the composited worst case. Same class of failure as the silent `alt=""`: conformant to every tool, broken for the user.
- **Media & Motion checkpoint** in the Verification Workflow, including one validation pass with `prefers-reduced-motion: reduce` active, and a matching **Section 5 — Time-Based Media and Motion** block in `templates/REPORT.md`, skippable with an explicit "N/A" when the interface carries no media.

### Changed
- **Motion (Section 3, Operable):** the rule covered "heavy state animations during crucial transitions" — which is neither autoplay nor parallax, the two motions users actually cannot escape. It now names both, requires the reduced-motion path to be built as the **default** with motion added in the `no-preference` branch, and links the new guide.
- **`guide-content-interaction.md`** rescoped: its one-line multimedia section (*"audio and video MUST have text alternatives or synchronized captions"*) carried the entire obligation for time-based media. Sensory language stays; media moves to its own guide, with the pointer left in place.
- **`guide-carousels-sliders.md`:** the pause control is now cited as SC 2.2.2 Level A instead of a house recommendation.

## [1.3.0] - 2026-08-07

> Driven by a question from the field: how does the standard handle alt text when the *user* supplies the image? The taxonomy existed, the SC 1.1.1 MUST existed — but no rule fired at the moment an image entered the conversation, which is exactly where agents fabricate an `alt` from the filename and move on. Same lesson as 1.2.0: obligation was not the variable — placement and trigger were.

### Added
- **Image Evidence (AI Behavior Contract):** when the user supplies an image — pasted into the conversation or referenced as an asset — the AI must resolve its text alternative before the image enters the code. If it can perceive the image (multimodal input or an image-reading tool in the environment), it classifies it via the removal test and proposes the `alt` **as a draft for the developer to confirm** — the human decision is part of the rule, not a courtesy. If it cannot, it requests the description in the same turn. Fabricating an `alt` from a filename or defaulting to `alt=""` are contract violations; an unresolved image blocks the Definition of Done (functional = CRITICAL, informative = HIGH).
- **`guide-images.md`, Section 5 — user-supplied images:** the three-step flow behind the rule (perceive → classify by the removal test → propose for human confirmation), the failure modes it forbids — including the silent `alt=""` no automated checker can catch — and borderline classifications routed to `A11Y-DECISIONS.md` as pattern-level decisions.

### Changed
- **Alt Text (Section 3, Perceivable):** the line now opens by stating that every `<img>` carries an `alt` attribute and that informative and functional images require a non-empty description; the **empty value** (`alt=""`) is reserved for images a human confirmed as decorative — a decision, never a default. The empty value is always named in prose, never only in notation, so no agent can misread "`alt=""` is for decorative images" as "the `alt` attribute is for decorative images". An `alt` deduced from a filename is fabricated evidence.
- **Wiki — AI Behavioral Contract:** the contract grows to 14 rules; Image Evidence documented with the human-in-the-loop rationale (vision gives the content, only product context gives the purpose — the machine prepares the evidence, the human establishes it).

## [1.2.0] - 2026-08-02

> Driven by a documented field post-mortem: an agent applied the standard to a real project for weeks, generated and maintained `A11Y-DECISIONS.md`, and never produced a `REPORT.md` or an `EXCEPTIONS.md`. The artifact that existed was the only one named inside a rule of the AI Behavior Contract. Obligation was not the variable — placement and trigger were.

### Added
- **Exception Memory (AI Behavior Contract):** accepting a WCAG SC violation now requires creating or updating `EXCEPTIONS.md` **in the same turn**, from the template, with risk owner, approver, tracking issue and expiry. An accepted-but-unrecorded exception is a contract violation, not a pending decision.
- **Release Evidence (AI Behavior Contract):** before any delivery to an end user — build, deploy, shared artifact, tag — the AI must verify a `REPORT.md` newer than the last interface change, or state that the delivery carries no conformance evidence. Event trigger, so it fires in continuous-delivery projects where a "final delivery" phase never arrives.
- **Artifacts Present** checkpoint, now first in the Verification Workflow: the six existing checkpoints verified the interface, none verified that evidence of it exists.
- **Headless-agent clause** (Section 7 and `REPORT.md`): an agent without a browser must still produce the report, marking unverifiable checkpoints and naming who must run them. A partial, honest report is evidence; a missing report is not.
- **Marking legend in `REPORT.md`:** `[x]` verified with evidence · `[!]` verified and failed · `[~]` partial · `[ ]` not verified, reason required. Removes the ambiguity of an empty checkbox and the incentive to mark what "is probably fine".
- **Governance guide, Section 0 — where a rule belongs:** anything the AI must DO belongs in the behavior contract with an explicit event trigger; guides carry depth, never sole obligation.
- **ARIA Soup anti-pattern (Section 6):** named prohibition of decorative/redundant ARIA — no ARIA where native HTML provides the semantics, no redundant roles, no static never-updated ARIA states. Response to the WebAIM Million 2026 finding (133+ ARIA attributes per page, 6× since 2019, with more ARIA correlating with more errors).
- **Benchmark pre-registration (`benchmark/`):** methodology and verbatim prompts for measuring whether A11Y.md reduces automatically detectable violations in AI-generated UI — published before any data collection.

### Changed
- **Lazy Context Loading no longer covers `templates/`:** `references/` is per-component context (load on demand); `templates/` is lifecycle context and must be loaded when its triggering event occurs. Adds **template fidelity** — artifacts are created from the template files, never deduced from prose, resolving upstream first when the folder is absent.
- **"Optional Templates" renamed to "Project Artifacts"** *(versioned, not optional)*, each with its trigger. The index label contradicted a normative body that says MUST four times.
- **`templates/EXCEPTIONS.md`:** every exception now requires a **risk owner**, an **approver**, a **tracking issue** and an **expiry date**, at the narrowest practical scope; in review mode the AI flags expired exceptions as 🟠 HIGH technical debt. An exception is temporary and is never silently suppressed.

## [1.1.0] - 2026-07-20

### Added
- **Platform Awareness (AI Behavior Contract):** The AI must identify the target platform before loading any reference; on native platforms, web references are semantic intent to translate, never implementation to copy.
- **`guide-platform-native.md`:** Translation layer mapping web semantics (roles, labels, live regions, focus, reduced motion, text scaling) to iOS (SwiftUI), Android (Compose), React Native, and Flutter.
- **Component Reuse + Decision Memory (AI Behavior Contract):** Before generating any interactive component, the AI must reuse existing project implementations; choices between equally conformant alternatives are recorded in the new `templates/A11Y-DECISIONS.md` (pattern-indexed decision log) and reused across turns.
- **Normative traceability:** WCAG 2.2 Success Criteria now cited by number throughout the core file and profile guide.

### Changed
- **Normative precision — WCAG requirements vs House Rules† now explicitly separated:**
  - Target size: the AA requirement is **24×24px (SC 2.5.8)** — 44×44px (Apple HIG/Material) is now labeled a House Rule; under Shield, 44×44 is normative (SC 2.5.5 AAA) with 48×48 house-advised.
  - Minimum font sizes (14/12/10px) and the Density Exception are now labeled House Rules — WCAG defines no minimum font size and no size-for-contrast compensation.
  - Shield profile: corrected to 7:1 text (SC 1.4.6) with UI components at 3:1 (SC 1.4.11 — WCAG has no AAA non-text contrast criterion).
  - Zoom: unified as text resize to 200% (SC 1.4.4) + reflow at 320 CSS px (SC 1.4.10) across core and guides (previously inconsistent 200%/400%).
- **Reference Library:** all 21 guides are now reachable from the core file (POUR sections, §0.1 and the Reference Library) — the 10 guides added in 1.0.0 were previously unreachable via Lazy Loading.
- **Complex Component Protocol:** step 2 now requires requesting human screen-reader validation — the AI MUST NOT claim the test was performed nor fabricate results; step 4 records resolved patterns in `A11Y-DECISIONS.md` instead of creating new reference examples.
- **Quick Start:** the primary install flow is now a single rule in the agent's configuration pointing at this repository (or a local copy for offline/pinned use) — no file copying required.
- **`guide-responsive-mobile.md`:** rescoped as *Responsive Web & Zoom* (browser only) and corrected per SC 1.4.4/1.4.10; native mobile now lives in `guide-platform-native.md`.

### Fixed
- **Errata:** the 1.0.0 notes claimed framework mapping for "12+ other framework syntaxes"; the guide covers React plus 5 web targets (Vue/Nuxt, Angular, Svelte, SolidJS, Vanilla/Lit).

## [1.0.0] - 2026-07-03

### Added
- **Compliance Profiles (Section 0.1):** Added `Launchpad (A)`, `Standard (AA)`, and `Shield (AAA)` profiles to support variable project maturity levels while maintaining strict baselines.
- **AI Behavior Contract Enhancements:**
  - Added `Mode Awareness` rule to differentiate between generating new code and reviewing existing code.
  - Added `Framework Adaptation` rule to enforce semantic transposition across different frameworks (Vue, Angular, Svelte, etc).
- **Setup Guide (`SETUP.md`):** Replaced instructions in READMEs with a definitive setup guide for Cursor, Claude, Copilot, Gemini, and Windsurf, strictly delegating rules to `A11Y.md` to prevent fragmentation.
- **10 New Technical Guides:**
  - Tables, Drag-and-drop, Infinite Scroll, Autocomplete, Toasts/Notifications, Loading/Skeletons, Tabs/Accordions, Carousels/Sliders, Tooltips/Popovers, and Responsive/Mobile guides added to `references/`.
- **Framework Mapping Guide:** Added to `references/` to map React/TSX examples to 12+ other framework syntaxes.
- **Compliance Profiles Detail Guide:** Added to `references/` to detail the new profiles.

### Changed
- **Renamed References:** All technical guides were renamed from `examples-*.md` to `guide-*.md` to better reflect their role as normative guidelines rather than mere examples.
- **Renamed EXAMPLES.md:** Renamed to `showcase4humans.md` and completely rewritten to be friendlier and more readable for human developers.
- **Orphaned Links Fixed:** `guide-visual-perception.md` and `guide-governance.md` are now properly referenced in the `Perceivable` and `Robust`/`Verification Workflow` sections of `A11Y.md` to ensure they are loaded by the AI.

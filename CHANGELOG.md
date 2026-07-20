# Changelog

All notable changes to the A11y Guidelines project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

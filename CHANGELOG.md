# Changelog

All notable changes to the A11y Guidelines project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

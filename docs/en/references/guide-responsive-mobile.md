# Responsive Web & Zoom A11y Guide

> **Scope:** Web layout, browser zoom & touch. For **native** mobile apps (iOS, Android, React Native, Flutter), see [Platform-Native Mapping](guide-platform-native.md) — this guide covers the browser only.

## Core Rules
1. **Text Resize (SC 1.4.4):** UI MUST NOT break, clip, or lose function up to **200% text zoom**.
2. **Reflow (SC 1.4.10):** Content MUST reflow at **320 CSS px width** (equivalent to 400% zoom on a 1280px viewport) without two-dimensional scrolling — except content that requires 2D layout (data tables, maps, charts).
3. **Orientation (SC 1.3.4):** MUST NOT lock orientation to landscape or portrait unless essential.
4. **Touch Targets (SC 2.5.8 + House Rule†):** 24×24 CSS px is the normative AA floor; design to **44×44px** on touch surfaces (Apple HIG / Material norm).
5. **Gestures (SC 2.5.1):** Complex gestures (swipes, multipoint) MUST have simple single-pointer equivalents.

*† = House Rule: this standard's ergonomic policy beyond the WCAG floor — see `A11Y.md` §0.1.*

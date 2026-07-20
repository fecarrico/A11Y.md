# Platform-Native Accessibility Mapping

> **Target Standard:** Semantic Equivalence | **Scope:** iOS (SwiftUI/UIKit), Android (Compose/Views), React Native, Flutter

The normative layer of `A11Y.md` (Principle Zero, POUR, Compliance Profiles, Severity, Governance) is platform-agnostic — WCAG 2.2 is written to be technology-neutral, and [WCAG2ICT](https://www.w3.org/TR/wcag2ict-22/) maps it to non-web software. The **technical references**, however, are web-first. This guide is the translation layer.

## Core Rules

1. **Never emit web idioms on native platforms.** ARIA attributes, roles, and CSS pixels do not exist in SwiftUI, Compose, React Native or Flutter. Translate the *intent*, not the syntax. Inventing hybrids (e.g., `aria-live` in SwiftUI) is a 🔴 CRITICAL violation.
2. **Prefer native components.** Platform-standard controls (Button, Switch, Alert) ship with semantics, focus behavior, and touch targets already compliant — the native equivalent of "prefer semantic HTML".
3. **Touch targets:** **44×44pt (iOS HIG)** / **48×48dp (Material)** are the platform norms and satisfy this standard's House Rule by default. The WCAG floor (SC 2.5.8, 24×24) still applies to custom-drawn controls.
4. **Respect system accessibility settings:** font scaling (Dynamic Type / `sp` units / `textScaler`), Reduce Motion, and increased-contrast modes are the native equivalents of zoom, `prefers-reduced-motion`, and contrast requirements.
5. **Announce dynamic changes.** Toasts, async results, and validation errors MUST be announced through the platform's accessibility notification API — the native equivalent of `aria-live`.

## Translation Table (semantic intent → platform)

| Web intent | iOS (SwiftUI) | Android (Compose) | React Native | Flutter |
| :--- | :--- | :--- | :--- | :--- |
| `<button>` / `role="button"` | `Button` or `.accessibilityAddTraits(.isButton)` | `Button` or `Modifier.semantics { role = Role.Button }` | `accessibilityRole="button"` | `ElevatedButton` or `Semantics(button: true)` |
| Accessible name (`aria-label`, `alt`) | `.accessibilityLabel("…")` | `contentDescription` / `semantics { contentDescription = "…" }` | `accessibilityLabel` | `Semantics(label: "…")` |
| `aria-live` / `role="status"` | `AccessibilityNotification.Announcement("…").post()` (iOS 17+; earlier: `UIAccessibility.post(notification: .announcement, …)`) | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` (`announceForAccessibility` is deprecated in API 36) | `accessibilityLiveRegion` (Android) / `AccessibilityInfo.announceForAccessibility(…)` | `SemanticsService.sendAnnouncement(…)` — prefer live-region semantics on Android |
| Modal dialog + focus containment | `.accessibilityAddTraits(.isModal)` (UIKit: `accessibilityViewIsModal`) | `Dialog()` (scopes focus by default) | `accessibilityViewIsModal` (iOS); hide background with `importantForAccessibility="no-hide-descendants"` (Android) | `showDialog` (route scoping); `Semantics(scopesRoute: true)` for custom overlays |
| Heading (`<h1>`–`<h6>`) | `.accessibilityAddTraits(.isHeader)` | `Modifier.semantics { heading() }` | `accessibilityRole="header"` | `Semantics(header: true)` |
| Disabled state (`disabled`, `aria-disabled`) | `.disabled(true)` (exposed automatically) | `enabled = false` | `accessibilityState={{disabled: true}}` | `Semantics(enabled: false)` or disabled widget |
| Grouping related content (label + value) | `.accessibilityElement(children: .combine)` | `Modifier.semantics(mergeDescendants = true) {}` | `accessible={true}` on the container | `MergeSemantics` |
| Focus management after navigation | `@AccessibilityFocusState` | `FocusRequester.requestFocus()` | `AccessibilityInfo.sendAccessibilityEvent(handle, 'focus')` | `FocusNode.requestFocus()` |
| `prefers-reduced-motion` | `accessibilityReduceMotion` environment / `UIAccessibility.isReduceMotionEnabled` | Respect system animator scale; avoid gratuitous auto-animation | `AccessibilityInfo.isReduceMotionEnabled()` | `MediaQuery.of(context).disableAnimations` |
| Text zoom (SC 1.4.4 equivalence) | Dynamic Type — use system text styles, never fixed sizes | `sp` units for text, never `dp` | `allowFontScaling` (default `true` — MUST NOT disable) | `MediaQuery` `textScaler` — never hardcode `textScaleFactor: 1.0` |

## Verification (native equivalent of Section 7)

- [ ] **Screen reader pass requested:** VoiceOver (iOS) / TalkBack (Android) — human validation; the AI MUST NOT claim it ran these.
- [ ] **Font scaling:** UI survives the largest system font size without truncation or overlap.
- [ ] **Focus/swipe order:** sequential navigation follows the visual/logical order.
- [ ] **Announcements:** async feedback audible without touching the screen.

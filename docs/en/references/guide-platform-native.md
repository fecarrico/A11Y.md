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
| **Action that exists only as a gesture** (swipe action, long-press menu, drag) | `.accessibilityAction(named: Text("Archive")) { … }` (UIKit: `accessibilityCustomActions` = `[UIAccessibilityCustomAction(name:actionHandler:)]`) | `Modifier.semantics { customActions = listOf(CustomAccessibilityAction(label) { true }) }` | `accessibilityActions={[{name: 'archive', label: 'Archive'}]}` + `onAccessibilityAction` | `Semantics(customSemanticsActions: {CustomSemanticsAction(label: 'Archive'): () { … }})` |
| Focus management after navigation | `@AccessibilityFocusState` | `FocusRequester.requestFocus()` | `AccessibilityInfo.sendAccessibilityEvent(handle, 'focus')` | `FocusNode.requestFocus()` |
| `prefers-reduced-motion` | `accessibilityReduceMotion` environment / `UIAccessibility.isReduceMotionEnabled` | Respect system animator scale; avoid gratuitous auto-animation | `AccessibilityInfo.isReduceMotionEnabled()` | `MediaQuery.of(context).disableAnimations` |
| Text zoom (SC 1.4.4 equivalence) | Dynamic Type — use system text styles, never fixed sizes | `sp` units for text, never `dp` | `allowFontScaling` (default `true` — MUST NOT disable) | `MediaQuery` `textScaler` — never hardcode `textScaleFactor: 1.0` |

## Custom Actions — the gesture problem

The most common native gap generated code ships: **an action that exists only as a gesture does not exist for assistive technology.** Swipe-to-archive on a list row, long-press for a context menu, drag to reorder — a sighted touch user performs the gesture; a screen-reader, switch-control or voice-control user has no path to it at all, because the gesture is intercepted by their assistive technology or is physically unavailable to them. This is the native sibling of *Pointer Gestures* (SC 2.5.1) and *Dragging Movements* (SC 2.5.7).

1. **Every action reachable only by gesture MUST also be exposed as a custom accessibility action**, using the platform API in the table above. The row's tap can stay a tap; the swipe's *consequences* (archive, delete, pin) are what must be exposed.
2. **The action label is a visible-label sibling:** short, verb-first, and matching whatever text the UI shows for the same action elsewhere (SC 2.5.3 applies to what voice-control users can say).
3. **How they surface, so the human validator knows what to test:** VoiceOver announces *"actions available"* on the element — the user swipes vertically with one finger to cycle actions and double-taps to run one; TalkBack presents them in the local actions menu; Switch Control and Voice Control read the same list.
4. **Do not duplicate.** If the buttons inside a row are individually focusable *and* re-exposed as custom actions, every action is announced twice. In Compose, clear child semantics (`clearAndSetSemantics { }`) when hoisting them into `customActions`; the same principle holds on every platform.
5. **A custom action is a supplement, never a hiding place:** an action essential to the task still needs a visible, discoverable path for everyone (a menu, a details screen) — the custom action restores parity for assistive-technology users, it does not excuse an interface where the *only* affordance is an invisible gesture.

*APIs verified against platform documentation: [`UIAccessibilityCustomAction`](https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction) / [`accessibilityAction(named:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)) · [Compose `customActions`](https://developer.android.com/develop/ui/compose/accessibility/semantics) · [React Native `accessibilityActions`](https://reactnative.dev/docs/accessibility) · [Flutter `CustomSemanticsAction`](https://api.flutter.dev/flutter/semantics/CustomSemanticsAction-class.html).*

## Verification (native equivalent of Section 7)

- [ ] **Screen reader pass requested:** VoiceOver (iOS) / TalkBack (Android) — human validation; the AI MUST NOT claim it ran these.
- [ ] **Assistive technologies beyond the screen reader:** the label a person **says** must match the label they **see** (Voice Control on iOS, Voice Access on Android — SC 2.5.3); every action reachable by sequential activation, for switch control (Switch Control / Switch Access); every control reachable by an external keyboard (Full Keyboard Access on iOS, keyboard navigation on Android). These three read the same accessible name and the same focus order the screen reader does — which is why a control named only for the screen reader breaks all four at once.
- [ ] **Font scaling:** UI survives the largest system font size without truncation or overlap.
- [ ] **Focus/swipe order:** sequential navigation follows the visual/logical order.
- [ ] **Announcements:** async feedback audible without touching the screen.
- [ ] **Gesture parity:** every swipe, long-press or drag consequence is reachable through the element's custom actions (VoiceOver: "actions available" → vertical one-finger swipe; TalkBack: local actions menu) — and nothing is announced twice.

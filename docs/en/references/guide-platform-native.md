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

## Brazil — ABNT NBR 17060 (mobile apps)

When the product ships to a Brazilian audience as a mobile app, the normative reference beside WCAG is **ABNT NBR 17060:2022** — *Accessibility in mobile device applications: requirements* (26 October 2022) — the mobile sibling of NBR 17225 and, like it, ballast for article 63 of the LBI (Lei 13.146/2015). The web norm covers content and web applications; this one covers **native (Android, iOS), hybrid and web apps on smartphones and tablets, including sites opened on a phone** — so a responsive site with a Brazilian destination answers to both. Desktop, TV and wearables are outside its scope.

- **Shape:** 54 requirements and recommendations in four groups — *perception and comprehension* (5.1.1), *control and interaction* (5.1.2), *media* (5.1.3) and *coding* (5.1.4) — most of them traced to a WCAG success criterion. The base is **WCAG 2.1**, not 2.2: the six A/AA criteria that 2.2 added (SC 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) have no counterpart in the norm, and this standard already demands them. **A build that conforms to this standard at the declared profile already satisfies nearly every item**; what follows is the remainder.
- **Where the norm says more than WCAG** — named checkpoints for a Brazilian mobile destination:
  - **Visible label before the field (5.1.1.11):** the form label sits *before* the input — above it or to its left — and a placeholder is never the label (the `placeholder-label` gate check is the mechanical half of this item). A 2025 inspection of five social networks found all five failing it.
  - **Steps in sequence (5.1.1.16):** a flow in steps tells the user the total number of steps and the current position; a paginated list tells the range shown and the total of items. WCAG has no criterion for this; the *Cognitive Load* rule (SC 3.3.7/3.3.8) is the nearest obligation in this standard.
  - **Accessibility settings (5.1.2.1):** the norm's own item for what Core Rule 4 already requires — font scaling, contrast and reduced motion set at the OS level are honored, never overridden.
  - **Time limits (5.1.2.6):** the SC 2.2.1 mechanics — turn off, adjust, or extend up to ten times — apply to every non-essential timer, chat windows included.
  - **No stall in sequential navigation with assistive technology (5.1.2.14):** the native form of *No Keyboard Trap* (SC 2.1.2): the TalkBack and VoiceOver swipe order reaches every control and never freezes on one — the field case behind the item was a transport app locking up when the pickup field was filled with a screen reader on.
  - **Flashing content (5.1.1.25):** the norm's item for SC 2.3.1 — nothing flashes more than three times a second, and content that may flash carries a warning before it plays.
  - **Touch target (5.1.2.13, recommendation):** the norm recommends the 44×44 target of SC 2.5.5; the platform norms in Core Rule 3 already exceed it.
- **Conformance mapping (this standard's — the norm defines no levels):** ⚖️ Standard (AA) = every *requirement*; 🛡️ Shield (AAA) = requirements plus every *recommendation*, each unmet recommendation justified in `EXCEPTIONS.md`. With a Brazilian mobile destination, `REPORT.md` names NBR 17060 beside the compliance profile, the way a web destination names its NBR 17225 level ([Governance §6.1](guide-governance.md)).
- **Verification:** the human pass of this guide (screen reader, voice control, switch, external keyboard, font scaling) is the norm's own method — the published inspections of it were run with TalkBack. The AI **MUST NOT** claim NBR 17060 conformance; the human validator does, from the report.

*Sources: ABNT NBR 17060:2022 is distributed through the [ABNT catalogue](https://www.abntcatalogo.com.br/), free of charge. Structure, scope and publication: [NIC.br](https://nic.br/noticia/releases/norma-da-abnt-sobre-acessibilidade-para-dispositivos-moveis-torna-a-navegacao-mais-inclusiva/) · [Web para Todos](https://mwpt.com.br/abnt-lanca-norma-de-acessibilidade-em-aplicativos-moveis/). Clause numbers follow the published structure as reproduced by the [Academia de Acessibilidade checklist](https://www.academiadeacessibilidade.com.br/ferramentas/checklist-abnt-17060/index.html); the wording of 5.1.1.11, 5.1.1.16, 5.1.1.25, 5.1.2.6 and 5.1.2.14 as quoted by [Gomes, Melo & Mota, IHC 2025](https://sol.sbc.org.br/index.php/ihc/article/view/37713) and by [Vidal, WPT, 2025](https://mwpt.com.br/como-a-abnt-17060-para-dispositivos-moveis-pode-auxiliar-na-correcao-de-problemas-de-acessibilidade/). A team declaring conformance reads the norm.*

## Verification (native equivalent of Section 7)

- [ ] **Screen reader pass requested:** VoiceOver (iOS) / TalkBack (Android) — human validation; the AI MUST NOT claim it ran these.
- [ ] **Assistive technologies beyond the screen reader:** the label a person **says** must match the label they **see** (Voice Control on iOS, Voice Access on Android — SC 2.5.3); every action reachable by sequential activation, for switch control (Switch Control / Switch Access); every control reachable by an external keyboard (Full Keyboard Access on iOS, keyboard navigation on Android). These three read the same accessible name and the same focus order the screen reader does — which is why a control named only for the screen reader breaks all four at once.
- [ ] **Font scaling:** UI survives the largest system font size without truncation or overlap.
- [ ] **Focus/swipe order:** sequential navigation follows the visual/logical order.
- [ ] **Announcements:** async feedback audible without touching the screen.
- [ ] **Brazilian destination:** `REPORT.md` names ABNT NBR 17060 beside the compliance profile, and the checkpoints of the *Brazil* section above were walked by a human.
- [ ] **Gesture parity:** every swipe, long-press or drag consequence is reachable through the element's custom actions (VoiceOver: "actions available" → vertical one-finger swipe; TalkBack: local actions menu) — and nothing is announced twice.

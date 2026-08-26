# Framework Mapping Guide

> **Target Standard:** Semantic Equivalence | **Scope:** AI Code Generation

The `A11Y.md` standard uses **React/TSX** syntax for its examples due to its ubiquity. However, the underlying accessibility requirements (ARIA attributes, semantic HTML, keyboard events) are **framework-agnostic**.

When an AI agent generates or reviews code, it **MUST transpose** these patterns into the active framework of the project while preserving semantic equivalence.

> [!IMPORTANT]
> **Scope: web frameworks only.** ARIA attributes and DOM events do not exist on native platforms. For iOS, Android, React Native, or Flutter targets, use the [Platform-Native Mapping](guide-platform-native.md) guide instead — transposing ARIA to native code is a violation of the *Platform Awareness* contract rule.

## Core Translation Rules

1. **Native over Custom:** Always prefer the framework's native implementation of a semantic element over building one from scratch.
2. **Reactivity:** Map dynamic ARIA states (e.g., `aria-expanded={isOpen}`) to the framework's state binding syntax.
3. **Event Listeners:** Map keyboard event listeners (e.g., `onKeyDown`) to the framework's idiomatic event handling.

---

## 1. Vue.js / Nuxt
- **State Binding:** Use `v-bind` or `:` (e.g., `:aria-expanded="isOpen"`).
- **Event Handling:** Use `@keydown` (e.g., `@keydown.enter="submit"`). Vue's event modifiers are highly recommended for accessibility (e.g., `@keydown.esc`, `@keydown.prevent.space`).
- **Refs:** Use `ref` for focus management (`element.value.focus()`).

## 2. Angular
- **State Binding:** Use square brackets `[attr.aria-expanded]="isOpen"`. Note the `attr.` prefix is required for ARIA attributes in Angular.
- **Event Handling:** Use parentheses `(keydown.enter)="submit()"`.
- **Focus:** Use `@ViewChild` and `ElementRef` for focus management.

## 3. Svelte
- **State Binding:** Direct binding `aria-expanded={isOpen}`.
- **Event Handling:** Use `onkeydown` (Svelte 5 event attributes). The `on:keydown` form is Svelte 4 directive syntax — still accepted, but legacy.
- **Directives:** Use the `use:` directive for complex focus trapping or reusable accessibility logic (e.g., `use:focusTrap`).

## 4. SolidJS
- **State Binding:** Similar to React `aria-expanded={isOpen()}`. Note the invocation of the signal.
- **Event Handling:** Similar to React `onKeyDown={(e) => ...}`.

## 5. Vanilla JS / Web Components (Lit)
- **State Binding:** In Lit, use `.ariaExpanded=${this.isOpen}` or `?aria-hidden=${this.isHidden}` for boolean attributes.
- **Shadow DOM:** Be extremely careful with `aria-controls` and `aria-describedby` across Shadow DOM boundaries, as ID references do not cross the boundary. Use `ElementInternals` where applicable.

---

## IDs that cross component boundaries

Every modern framework ships a stable ID generator for SSR (`useId` in React 18+ and Vue 3.5+, equivalents elsewhere). It solves identifier collision — and creates a trap the moment two components need to **reference each other**.

### ❌ Incorrect

```tsx
// Toolbar.tsx
const panelId = useId();                    // generates one value
return <button aria-controls={panelId} aria-expanded={open}>Filters</button>;

// Panel.tsx
const panelId = useId();                    // generates ANOTHER value
return <div id={panelId}>…</div>;
```

`aria-controls` points at an `id` that does not exist. Each `useId()` call is independent — nothing makes two components arrive at the same value. And the defect **passes** axe and Lighthouse: they validate the attribute's syntax, they do not resolve a reference across components. This failure mode is the **inverse of ARIA Soup**: there, ARIA is added where native semantics sufficed; here the ARIA is syntactically correct and empty at the destination — the screen reader follows the pointer and finds nothing.

### ✅ Correct

```tsx
// Toolbar.tsx — one side generates, the other receives
const panelId = useId();
return (
  <>
    <button aria-controls={panelId} aria-expanded={open}>Filters</button>
    <Panel id={panelId} />
  </>
);

// Panel.tsx
export function Panel({ id }: { id: string }) {
  return <div id={id}>…</div>;
}
```

This holds for `aria-controls`, `aria-labelledby`, `aria-describedby` and `aria-activedescendant`, in any framework: **the identifier has a single origin and travels down as a property.** If the components sit far apart in the tree, the `id` moves up into shared state or context — what does not change is that it is generated once.

*See the **Orphaned ARIA Reference** anti-pattern in Section 6 of the core file.*

---

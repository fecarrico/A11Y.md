# Framework Mapping Guide

> **Target Standard:** Semantic Equivalence | **Scope:** AI Code Generation

The `A11Y.md` standard uses **React/TSX** syntax for its examples due to its ubiquity. However, the underlying accessibility requirements (ARIA attributes, semantic HTML, keyboard events) are **framework-agnostic**.

When an AI agent generates or reviews code, it **MUST transpose** these patterns into the active framework of the project while preserving semantic equivalence.

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
- **Event Handling:** Use `on:keydown`.
- **Directives:** Use the `use:` directive for complex focus trapping or reusable accessibility logic (e.g., `use:focusTrap`).

## 4. SolidJS
- **State Binding:** Similar to React `aria-expanded={isOpen()}`. Note the invocation of the signal.
- **Event Handling:** Similar to React `onKeyDown={(e) => ...}`.

## 5. Vanilla JS / Web Components (Lit)
- **State Binding:** In Lit, use `.ariaExpanded=${this.isOpen}` or `?aria-hidden=${this.isHidden}` for boolean attributes.
- **Shadow DOM:** Be extremely careful with `aria-controls` and `aria-describedby` across Shadow DOM boundaries, as ID references do not cross the boundary. Use `ElementInternals` where applicable.

---

## Translation Example: The Toggle Button

### 🔵 Source (React/TSX)
```tsx
<button
  aria-pressed={isActive}
  onClick={() => setIsActive(!isActive)}
>
  Toggle
</button>
```

### 🟢 Vue.js
```html
<button
  :aria-pressed="isActive"
  @click="isActive = !isActive"
>
  Toggle
</button>
```

### 🔴 Angular
```html
<button
  [attr.aria-pressed]="isActive"
  (click)="isActive = !isActive"
>
  Toggle
</button>
```

### 🟠 Svelte
```html
<button
  aria-pressed={isActive}
  on:click={() => isActive = !isActive}
>
  Toggle
</button>
```

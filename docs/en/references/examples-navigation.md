# Accessibility Guide: Navigation

> Scope: Keyboard navigation patterns, skip links, landmark regions, and SPA routing focus management.

## Good Examples

### 1. Semantic Navigation
```html
<nav aria-label="Main Navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```
- **Why:** `<nav>` is a landmark. `aria-current="page"` tells users which link represents the current location.

### 2. Skip to Content
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content">...</main>
```
- **Why:** Allows keyboard users to bypass repetitive navigation links and go straight to the content.

## Bad Examples

### 1. Nested Menus (Hover only)
- **Implication:** Menus that only appear on hover are inaccessible to keyboard users and touch device users. They require JS to toggle on click/focus.

### 2. Non-standard Links
```html
<span onclick="window.location='/new-page'">Go to Page</span>
```
- **Implication:** This is not an anchor tag. It has no focus, no "link" role, and cannot be opened in a new tab.

## Accessibility Implications
- **Searchability:** Proper navigation landmarks allow screen reader users to jump directly to the navigation section using shortcut keys.
- **Predictability:** Keeping the navigation in the same place and order across pages reduces cognitive load.

# Modals & Overlays Guide

> **Scope:** Dialogs, drawers, backdrops — mount cost and animation

## Good Examples

### 1. Construct on first open
```js
let dialog = null;
openBtn.addEventListener('click', () => {
  if (!dialog) dialog = buildDialog();   // built once, on demand
  document.body.append(dialog);
  requestAnimationFrame(() => dialog.classList.add('open'));
});
```
- **Why:** the dialog costs nothing at page load — no nodes, no images, no listeners. The build happens on the click that proves it is needed, and the `requestAnimationFrame` lets the entrance transition run from a painted initial state.

### 2. Compositor-only entrance
```css
.dialog { transform: translateY(8px); opacity: 0; transition: transform .2s, opacity .2s; }
.dialog.open { transform: none; opacity: 1; }
.backdrop { opacity: 0; transition: opacity .2s; background: rgb(0 0 0 / .5); }
```
- **Why:** `transform` and `opacity` animate on the compositor; the page behind does not re-layout. A `backdrop-filter: blur()` here is the expensive alternative — budget it consciously or use a plain translucent backdrop.

## Bad Examples

### 1. All dialogs in the DOM at load
```html
<div class="modal" id="confirm-delete" style="display:none">…</div>
<div class="modal" id="edit-profile" style="display:none">…</div>
<div class="modal" id="share-sheet" style="display:none">…</div>
```
- **Why it fails:** every hidden dialog is parsed, styled and kept in memory for a page where the user may open none of them. Hidden-but-rendered is load cost without load value.

### 2. Animating layout properties
```css
.drawer { left: -320px; transition: left .3s; }
.drawer.open { left: 0; }
```
- **Why it fails:** animating `left` triggers layout every frame for the drawer *and* anything whose geometry depends on it. `transform: translateX()` produces the same motion on the compositor.

## Checklist
- [ ] Zero dialog nodes in the DOM before first open (unless SSR requires them — then `content-visibility` defers their cost).
- [ ] Entrance/exit animate `transform`/`opacity` only.
- [ ] Media inside the dialog loads when the dialog opens, not with the page.
- [ ] Closing removes or hides without leaking listeners or timers.
- [ ] Backdrop uses translucency, not `backdrop-filter`, unless the profile's frame budget was checked with it on.
- [ ] Reopening reuses the built dialog; teardown clears its timers.

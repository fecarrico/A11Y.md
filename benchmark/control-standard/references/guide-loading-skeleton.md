# Loading & Skeletons Guide

> **Scope:** Perceived latency, reserved layout, progressive rendering

## The rule behind every rule

Loading states manage the gap between request and content. They have two jobs: keep the page's geometry stable (the skeleton reserves exactly the space the content will take) and keep the user informed that progress is real. A loading state that shifts layout when it resolves has failed the first job; one that spins forever without a failure path has failed the second.

## Good Examples

### 1. Skeleton that matches final geometry
```html
<div class="card" style="aspect-ratio: 3 / 4">
  <div class="skeleton img" style="aspect-ratio: 16 / 10"></div>
  <div class="skeleton line" style="width: 70%"></div>
  <div class="skeleton line" style="width: 40%"></div>
</div>
```
- **Why:** the card owns its final size before any data arrives; the swap from skeleton to content changes pixels, not positions. CLS from this component is zero by construction.

### 2. Staged reveal, single layout
```js
const data = await fetchList();
list.replaceChildren(...data.map(render));  // one DOM operation
```
- **Why:** content enters in one batch into reserved space — not row by row as items parse, each pushing the footer down another notch.

### 3. Failure is a state, not an absence
```js
const t = setTimeout(() => showRetry(section), 8000);
fetchSection().then(renderInto(section)).catch(() => showRetry(section)).finally(() => clearTimeout(t));
```
- **Why:** the skeleton has three exits — content, error, timeout — all designed. A skeleton with one exit is a spinner with better styling.

## Bad Examples

### 1. The spinner cascade
```
page spinner → header renders → section spinner → list renders → row spinners…
```
- **Why it fails:** the user watches three sequential loading states where one reserved layout with progressive fill was possible. Perceived time stacks; each new spinner resets the user's clock.

### 2. Skeleton without dimensions
```html
<div class="skeleton"></div>  <!-- height: whatever the shimmer is -->
```
- **Why it fails:** a skeleton that does not reserve the content's real height converts into a layout shift at the worst moment — exactly when the user starts reading. It made the metric worse than no skeleton.

### 3. Shimmer on the main thread
```js
setInterval(() => el.style.backgroundPosition = `${x++}px 0`, 16);
```
- **Why it fails:** animating the placeholder with script steals frames from the work that would end the loading state. Shimmer is a CSS animation on a compositor property, or nothing.

## Checklist
- [ ] Every async region reserves final geometry (dimensions, `aspect-ratio`, or min-height from real content sizes).
- [ ] One loading state per user intention, not per component.
- [ ] Timeout and failure paths render something actionable.
- [ ] Shimmer/pulse is CSS-only; removing it changes no timing.
- [ ] The fast path skips the skeleton: cached data renders directly — no flash of placeholder for content that took 40 ms.

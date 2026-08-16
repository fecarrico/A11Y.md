# Buttons & Handlers Guide

> **Scope:** Click handling, action latency, double-submit protection

## Core Rules
1. **Acknowledge within one frame:** the pressed state (class toggle, style change) applies synchronously; the work the click triggers is scheduled after paint.
2. **Heavy work leaves the handler:** anything past a few milliseconds moves to `requestAnimationFrame` (visual), a microtask (state), or a worker (compute) — the handler itself stays under the INP budget.
3. **Disable on dispatch:** an async action disables its trigger (or dedupes in flight) so double-clicks cannot double-submit; re-enable on settle, success or failure alike.
4. **Delegate repeated handlers:** one listener on the list container beats one per row; per-item closures at scale are heap and setup cost.
5. **No layout in the click path:** reading `offsetWidth` or forcing style recalculation inside a click handler stalls the very interaction being measured.

## Bad Example
```js
button.addEventListener('click', () => {
  const rows = buildAllRows(data);         // heavy, synchronous
  table.innerHTML = rows;                  // full rebuild
  button.style.width = button.offsetWidth; // forced layout
});
```
- **Why it fails:** the user's click pays for computation, a tree rebuild and a forced layout before any visual response — the three costs this guide exists to keep out of the handler.

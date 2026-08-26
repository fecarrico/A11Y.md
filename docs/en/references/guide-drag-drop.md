# Drag & Drop Guide

> **Scope:** Reorderable lists, kanban boards, file drop zones, sortable anything — the hardest interaction pattern in the APG, and the one most often shipped as pointer-only.

## 0. The rule everything else follows

**Dragging is a shortcut, never the mechanism.** SC 2.5.7 (Dragging Movements, Level AA) requires every drag operation to have a **single-pointer, non-dragging alternative** — and keyboard operability (SC 2.1.1) requires one more path on top. Build the outcome first (move item X to position Y), then let dragging be one of three ways to reach it.

1. **The keyboard model:** focus the item's handle → `Space`/`Enter` picks it up (state announced) → arrow keys move it, announcing each position → `Space` drops → **`Esc` cancels**, returning the item to its origin and saying so. Persistent instructions reachable via `aria-describedby` on the handle — the pattern is not guessable.
2. **The three announcements** through one `role="status"` region, outcome not event: *"Invoice.pdf grabbed, position 2 of 5"* → *"moved to position 3 of 5"* → *"dropped at position 3"* (or *"reorder cancelled, returned to position 2"*). Silence at any of the three moments is how a screen-reader user loses an item mid-air.
3. **The single-pointer alternative** (SC 2.5.7): an explicit affordance that needs no gesture — *Move up / Move down / Move to…* in the item's menu, or numbered position selection. This is also the path for voice control, switch access and touch users with motor impairments; on native platforms, expose it as custom actions (see [Platform-Native Mapping](guide-platform-native.md)).
4. **The handle is a real button** with an accessible name naming the item — `aria-label="Reorder Invoice.pdf"` — never a decorative icon with a mouse listener. Visible focus tracks the item through the whole move (SC 2.4.7).
5. **Drop targets don't speak in color:** valid targets get a visible indicator at 3:1 (SC 1.4.11) plus a non-color cue (outline, pattern, insertion line), and the current target is named in the announcement, not only highlighted.
6. **File drop zones** are the same rule in disguise: the zone MUST be accompanied by a real `<input type="file">` (or a button opening one) — "drag files here" as the only path is SC 2.5.7 failed at the first interaction of the flow.

*Success criteria covered: 2.5.7 Dragging Movements (AA) · 2.1.1 Keyboard (A) · 4.1.3 Status Messages (AA) · 2.4.7 Focus Visible (AA) · 1.4.11 Non-text Contrast (AA)*

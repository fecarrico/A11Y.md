# Infinite Scroll & Pagination Guide

> **Scope:** Feeds, endless lists, automatic pagination.

## 0. The rule everything else follows

**"Load more" is the accessible default; infinite scroll is the exception that has to earn it.** Auto-fetching content on scroll silently destroys three things: the **footer** (reachable only in the instant before it flees), the **scrollbar** as a sense of position and size, and the **Back button** (return, and you are at the top of a shorter list). A button gives keyboard users a stopping point, screen-reader users an announcement point, and everyone their footer back.

1. **Prefer an explicit "Load more" button.** After activation, focus moves to the **first newly loaded item** — never resets to the top, never stays stranded on a button that jumped.
2. **If you do auto-load:** announce each batch from a polite status region, outcome not event — *"20 more results, 60 of 200"* — and never per-item. The sentinel that triggers loading is not focusable and not in the accessibility tree.
3. **Appending never moves the user.** New items enter *after* the current reading position; re-sorting or re-rendering the existing list mid-read is a context change nobody asked for (SC 3.2.2 in spirit, a lost screen-reader user in practice).
4. **Position is recoverable:** Back returns to the same scroll position with the same items (history state); item names or `aria-setsize`/`aria-posinset` convey *"n of m"* where the total is known, so "somewhere in an endless list" becomes an addressable place.
5. **The footer stays reachable.** If content grows automatically, either stop auto-loading after a few batches (switching to the button), or provide a skip link past the feed — a footer that flees on approach is content that exists and cannot be used (Principle Zero).
6. **`role="feed"`** is the right container for a true feed (article stream), letting screen readers move between articles while loading continues; each article carries `aria-posinset`/`aria-setsize`.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 2.4.3 Focus Order | A | focus lands on new content after "Load more"; never resets |
| 4.1.3 Status Messages | AA | each loaded batch announced, with position in the whole |
| 2.1.1 Keyboard | A | everything reachable without scroll gestures |
| 2.4.1 Bypass Blocks | A | a way past the feed to what follows it |

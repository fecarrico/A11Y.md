# Toasts & Notifications Guide

> **Scope:** Toasts, snackbars, banners, status messages.

## 0. The rule everything else follows

**A toast the user cannot perceive, reach, or outlive is a message that was never sent.** Toasts fail in three independent ways — not announced (invisible to screen readers), announced but unreachable (an action inside vanishes before a keyboard user arrives), and gone too fast to read. A toast must survive all three, or carry nothing that matters.

1. **`role="status"` is the default; `role="alert"` is the exception** — reserved for errors needing immediate attention. Never both together, and never `aria-live` stacked on either (the *redundant-alert* the tooling flags). The live region **exists in the DOM before** the first message enters it; inject text into a standing region, don't inject the region.
2. **Never move focus to a toast.** It hijacks typing and screen-reader context for something that calls itself passive. If a response truly requires action *now*, that is a dialog (see [Modals](guide-modals.md)), not a toast.
3. **Auto-dismiss is for the inert only.** A toast carrying an **action or link MUST persist** until dismissed — a timed action is a time limit (SC 2.2.1) that zoomed-in, screen-reader and slow-reacting users all lose. Purely informational toasts that do auto-dismiss stay long enough to be read (a baseline of ~6 seconds, scaled up with message length).
4. **The action must also live somewhere permanent.** "Undo" that exists only in a 5-second toast is a feature with an expiry date; the same operation belongs in the item's menu or history. The toast is a convenience shortcut, not the feature's address.
5. **Dismissible by keyboard:** a real close `<button>` with a name, reachable by `Tab` — and `Esc` dismisses the focused toast.
6. **Same channel, same place:** toasts appear in a consistent position across the product; repeats collapse (*"3 items archived"*) instead of stacking a tower the reader announces one by one.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 4.1.3 Status Messages | AA | the message is announced without receiving focus |
| 2.2.1 Timing Adjustable | A | nothing actionable disappears on a timer |
| 2.1.1 Keyboard | A | dismiss and act without a mouse |
| 1.4.13 Content on Hover or Focus | AA | hover pausing dismissal must not be the only way to keep it |

## Tip for the AI:

Trigger the toast, then take your hands off the keyboard, with a screen reader running. Was it announced exactly once? Could you have reached its action before it vanished? If the answer to the second is no, the action never existed for a whole class of users — move it somewhere permanent and let the toast be what it is: an echo.

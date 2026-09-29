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

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN I am typing in a field, WHEN a toast appears, THEN focus stays in the field and nothing I typed is lost.
- WHEN a toast carries an action or a link, THEN it stays until I dismiss it, and `Tab` reaches the action and a Close button.
- WHEN the toast has focus and I press `Esc`, THEN it is dismissed.
- WHEN a toast with "Undo" is gone, THEN the same operation is still reachable elsewhere — in the item's menu or history.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN a toast appears, THEN I hear its text once without leaving what I was reading; an error toast interrupts, a status toast waits its turn.
- WHEN three identical events fire, THEN I hear one collapsed message ("3 items archived"), not three announcements.
- WHEN I navigate to the toast, THEN I hear its text and then "Close, button" — the closing control has a name.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN a toast appears, THEN I hear its text once and my position on the page does not change.
- WHEN I swipe to a persistent toast, THEN I reach its action and "Close, button", and a double-tap on Close removes it.

*Success criteria covered: 4.1.3 Status Messages (AA) · 2.2.1 Timing Adjustable (A) · 2.1.1 Keyboard (A) · 1.4.13 Content on Hover or Focus (AA)*

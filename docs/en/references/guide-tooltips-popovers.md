# Tooltips & Popovers Guide

> **Scope:** Contextual Information

## Core Rules
1. **Trigger:** Must be focusable (button, link).
2. **Hover/Focus:** Tooltip MUST appear on both hover and keyboard focus.
3. **Dismissible (SC 1.4.13):** MUST be dismissible with the `Escape` key **without moving focus** — a magnifier user needs the overlay gone without losing their place.
4. **Hoverable (SC 1.4.13):** MUST NOT disappear when the pointer moves onto the tooltip itself — the path to it leaves the trigger.
5. **Persistent (SC 1.4.13):** MUST remain visible until the user dismisses it, the trigger loses hover/focus, or the information becomes invalid. MUST NOT time out on its own.

> **SC 1.4.13 Content on Hover or Focus (AA)** is exactly the three conditions above. Content that appears on hover and vanishes before the user can reach it fails the criterion even with a perfectly correct `role="tooltip"`.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a control with a tooltip, WHEN I `Tab` to it, THEN the tooltip appears without any mouse movement.
- WHEN I press `Esc`, THEN the tooltip closes and focus stays exactly where it was.
- WHEN I leave the tooltip open and wait, THEN it stays visible — it never times out on its own.
- GIVEN a popover trigger, WHEN I press `Enter`, THEN the popover opens without the mouse, and `Esc` closes it.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I `Tab` to the trigger, THEN I hear its name and then the tooltip text, without having to open anything.
- WHEN I press `Esc`, THEN the tooltip is gone and the trigger is still the focused element I hear.
- WHEN I open a popover, THEN I can read its content and reach any control inside it.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe to the trigger, THEN I hear its name and the tooltip text together.
- WHEN I double-tap a popover trigger, THEN the popover opens and swiping forward reaches its content.

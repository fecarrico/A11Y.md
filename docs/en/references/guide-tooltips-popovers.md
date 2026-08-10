# Tooltips & Popovers Guide

> **Scope:** Contextual Information

## Core Rules
1. **Trigger:** Must be focusable (button, link).
2. **Hover/Focus:** Tooltip MUST appear on both hover and keyboard focus.
3. **Dismissible (SC 1.4.13):** MUST be dismissible with the `Escape` key **without moving focus** — a magnifier user needs the overlay gone without losing their place.
4. **Hoverable (SC 1.4.13):** MUST NOT disappear when the pointer moves onto the tooltip itself — the path to it leaves the trigger.
5. **Persistent (SC 1.4.13):** MUST remain visible until the user dismisses it, the trigger loses hover/focus, or the information becomes invalid. MUST NOT time out on its own.

> **SC 1.4.13 Content on Hover or Focus (AA)** is exactly the three conditions above. Content that appears on hover and vanishes before the user can reach it fails the criterion even with a perfectly correct `role="tooltip"`.
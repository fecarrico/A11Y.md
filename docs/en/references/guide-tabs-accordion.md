# Tabs & Accordions Guide

> **Scope:** Content Disclosure

## Core Rules
1. **Keyboard:** Use arrow keys to navigate tabs; Tab key should move into tab panels.
2. **Roles (Tabs):** `tablist`, `tab`, `tabpanel`.
3. **Roles (Accordion):** Use `<details>` and `<summary>`, or buttons with `aria-expanded` and `aria-controls`.
4. **Aria-selected:** Used on tabs to denote the active tab.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a tab list, WHEN I `Tab` into it, THEN focus lands on the selected tab — one stop for the whole list.
- WHEN I press `←`/`→`, THEN focus moves between the tabs, and only the selected tab's panel is shown.
- WHEN I press `Tab` on a tab, THEN focus moves into its panel, not to the next tab.
- GIVEN an accordion, WHEN I press `Enter` or `Space` on a header, THEN its panel opens or closes and focus stays on the header.
- WHEN a panel is closed, THEN `Tab` skips its content.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I reach a tab, THEN I hear its name, "tab, 1 of 3", and "selected" on the active one.
- WHEN I press `Tab` into the panel, THEN I hear its content, and it is the selected tab's.
- WHEN I reach an accordion header, THEN I hear its name, "button" and "collapsed" or "expanded"; activating it announces the new state.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe across the tab list, THEN each tab reads "tab, n of 3", and double-tapping one makes it "selected", its panel next in the swipe order.
- WHEN I double-tap an accordion header, THEN I hear "expanded" and swiping forward reaches its content; double-tapping again says "collapsed" and the content is gone.

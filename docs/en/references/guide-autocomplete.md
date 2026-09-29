# Autocomplete & Combobox Guide

> **Scope:** Search & Selects

## Core Rules
1. **Roles:** Input MUST have `role="combobox"`, list MUST have `role="listbox"`, options MUST have `role="option"`.
2. **Aria-expanded:** Toggle `aria-expanded` when the list opens/closes.
3. **Aria-activedescendant:** Use `aria-activedescendant` to manage focus within the list without losing cursor position in the input.
4. **Status:** Announce results count via `aria-live`.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a combobox, WHEN I type, THEN the list of matches opens below the field.
- WHEN I press `↓`/`↑`, THEN the highlight moves through the options while the cursor stays in the field — I can keep typing.
- WHEN I press `Enter` on a highlighted option, THEN it fills the field and the list closes.
- WHEN I `Tab` out of the field, THEN the list closes and focus lands on the next control.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I `Tab` to the field, THEN I hear its label, "combobox" and "collapsed".
- WHEN I type and matches appear, THEN I hear how many results are available.
- WHEN I press `↓`, THEN I hear each option's text as it is highlighted ("Brazil, 1 of 5"), and I am still in the field.
- WHEN I press `Enter`, THEN the field holds the chosen value and I hear "collapsed".

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I type in the field, THEN I hear the results count.
- WHEN I swipe forward, THEN I reach the options one by one, each as "option", and double-tapping one fills the field and closes the list.

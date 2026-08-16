# Autocomplete & Live Search Guide

> **Scope:** Typeahead, suggestions, live filtering

## Core Rules
1. **Debounce to intent:** Fire the lookup 200–300 ms after the last keystroke, never per keypress.
2. **Cancel stale requests:** Abort the in-flight fetch when a newer query supersedes it (`AbortController`); stale responses MUST NOT render.
3. **Cache by prefix:** Results for `"par"` seed the list for `"pari"`; repeat queries within the session hit memory, not network.
4. **Bound the list:** Render at most the visible suggestions (7–10); never the full match set.

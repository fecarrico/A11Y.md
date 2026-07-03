# Autocomplete & Combobox Guide

> **Scope:** Search & Selects

## Core Rules
1. **Roles:** Input MUST have `role="combobox"`, list MUST have `role="listbox"`, options MUST have `role="option"`.
2. **Aria-expanded:** Toggle `aria-expanded` when the list opens/closes.
3. **Aria-activedescendant:** Use `aria-activedescendant` to manage focus within the list without losing cursor position in the input.
4. **Status:** Announce results count via `aria-live`.
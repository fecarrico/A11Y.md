# Loading & Skeletons Guide

> **Scope:** Loading States

## Core Rules
1. **Aria-busy:** Use `aria-busy="true"` on the container being updated.
2. **Announcement:** Screen readers should be informed of loading state via polite live regions.
3. **Motion:** Respect `@media (prefers-reduced-motion)` for skeleton pulse animations.
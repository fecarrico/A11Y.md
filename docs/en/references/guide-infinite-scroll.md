# Infinite Scroll Accessibility Guide

> **Scope:** Pagination & Feeds

## Core Rules
1. **Load More Button:** Prefer a "Load More" button over automatic scroll fetching, as auto-fetching traps keyboard users from reaching the footer.
2. **Focus Management:** When new items load, manage focus if it was on a trigger, or announce loading via `aria-live`.
3. **Footer Access:** Ensure keyboard users can navigate past the feed.
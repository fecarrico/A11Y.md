# Drag and Drop Accessibility Guide

> **Scope:** Interactive Lists & Boards

## Core Rules
1. **Keyboard Alternative:** Every drag/drop action MUST have a keyboard equivalent (e.g., Space to select, arrows to move, Space to drop).
2. **Aria-live Announcements:** Screen readers MUST be informed when an item is picked up, moved, and dropped via `aria-live`.
3. **Visual Cues:** Visible focus MUST track the item being moved.
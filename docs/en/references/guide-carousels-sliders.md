# Carousels & Sliders Guide

> **Scope:** Sliding Content

## Core Rules
1. **Pause Control:** Auto-playing carousels MUST have a mechanism to pause/stop.
2. **Buttons:** Previous/Next buttons MUST be `button` elements with aria-labels.
3. **Hidden Slides:** Slides not visible MUST have `aria-hidden="true"` and `tabindex="-1"` so keyboard users do not focus off-screen content.
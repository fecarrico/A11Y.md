# Carousels & Sliders Guide

> **Scope:** Sliding Content

## Core Rules
1. **Pause Control:** Auto-playing carousels MUST have a mechanism to pause/stop — SC 2.2.2, Level A, for any automatic movement over 5 seconds. *(See [Time-Based Media & Motion](guide-media.md) for the criterion and its reduced-motion behavior.)*
2. **Buttons:** Previous/Next buttons MUST be `button` elements with aria-labels.
3. **Hidden Slides:** Off-screen slides MUST be removed from the tab order with the `inert` attribute. `tabindex="-1"` affects **only the element it sits on** and leaves the buttons and links *inside* the slide focusable — precisely the invisible focus this rule exists to prevent. `inert` removes the entire subtree from focus and from the accessibility tree, making `aria-hidden` unnecessary (and a control inside an `aria-hidden` subtree would be unreachable anyway).
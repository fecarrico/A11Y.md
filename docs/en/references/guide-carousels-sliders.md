# Carousels & Sliders Guide

> **Scope:** Carousels, rotating banners, content sliders.

## 0. The rule everything else follows

**Auto-advance is the accessibility problem; everything else is a labelled group of slides.** A carousel that never moves on its own is a manageable pattern. One that rotates automatically fights the user on three fronts at once: it moves content mid-read (low vision, cognitive), it moves content mid-listen (screen reader), and it moves the thing focus was standing on (keyboard).

1. **The pause control is a requirement, not chrome** — SC 2.2.2, Level A, for any automatic movement over 5 seconds: a visible, focusable pause/stop, **first in the carousel's tab order**, so it can be reached before the rotation has changed anything. Under `prefers-reduced-motion`, auto-advance simply does not start (see [Time-Based Media & Motion](guide-media.md)).
2. **Rotation stops on interaction:** hover, focus entering the carousel, or an open tooltip each suspend auto-advance — and **the slide under the user's focus never moves away from them**.
3. **Structure:** container `role="region"` + `aria-roledescription="carousel"` + an accessible name; each slide `role="group"` + `aria-roledescription="slide"` + a name that locates it — *"3 of 8"* or its title. Position must not be conveyed by dot color alone (SC 1.4.1).
4. **Controls are buttons:** Previous/Next as real `<button>`s with names; picker dots as buttons named for their slide (*"Slide 3: Spring collection"*), current one marked with `aria-current`, never only by fill.
5. **Off-screen slides are `inert`.** `tabindex="-1"` affects only the element it sits on — the links and buttons *inside* the hidden slide stay focusable, which is exactly the invisible focus this rule exists to prevent. `inert` removes the whole subtree from focus and from the accessibility tree.
6. **Announce only user-initiated changes:** a polite region confirms *"Slide 4 of 8"* after Next — but auto-rotation is **never** announced, or the carousel narrates itself over everything else on the page.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 2.2.2 Pause, Stop, Hide | A | auto-advance over 5s has a reachable pause |
| 2.1.1 Keyboard | A | all controls and slide content operable without a mouse |
| 1.4.1 Use of Color | A | position and current-slide state never by color alone |
| 4.1.2 Name, Role, Value | A | carousel and slides named; current state exposed |
| 2.4.3 Focus Order | A | focus never abandoned on a slide that rotated away |

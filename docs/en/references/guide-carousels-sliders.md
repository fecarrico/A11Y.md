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

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a carousel that rotates on its own, WHEN I `Tab` into it, THEN the first stop is the pause control and the rotation stops while focus is inside.
- WHEN I press `Enter` on Pause, THEN the rotation stops.
- WHEN I keep pressing `Tab`, THEN focus reaches Previous, Next, the dots and the visible slide's links only — never anything in an off-screen slide.
- WHEN focus is on a link inside a slide, THEN that slide never moves away from under me.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I reach the carousel, THEN I hear "carousel" and its name, and each slide as "slide" with its position — "3 of 8" — or its title.
- WHEN I activate Next, THEN I hear "Slide 4 of 8" once.
- WHEN the carousel rotates on its own, THEN I hear nothing about it.
- WHEN I reach a picker dot, THEN I hear "button", the slide it leads to, and "current" on the active one.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe into the carousel, THEN the first element I hear is the pause control.
- WHEN I keep swiping, THEN I pass only through the visible slide's content, never through off-screen slides.
- WHEN I double-tap Next, THEN I hear the new slide's position; WHEN it rotates by itself, THEN I hear nothing.

*Success criteria covered: 2.2.2 Pause, Stop, Hide (A) · 2.1.1 Keyboard (A) · 1.4.1 Use of Color (A) · 4.1.2 Name, Role, Value (A) · 2.4.3 Focus Order (A)*

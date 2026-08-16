# Carousels & Sliders Guide

> **Scope:** Galleries, auto-advance, swipe — media weight and timers

## Core Rules

1. **Load the visible slide plus one neighbor.** A five-slide gallery at load costs one image, not five; neighbors load on approach (`IntersectionObserver` or index math on navigation). The first slide is an LCP candidate — it gets `fetchpriority="high"` and is never lazy.
2. **Scroll-snap over script.** `scroll-snap-type` with native scrolling gives compositor-driven swiping for free; JavaScript position math runs only for what CSS cannot express (auto-advance, indicators).
3. **Auto-advance is owned by the page's visibility.** The interval pauses on `visibilitychange`, on hover, and on user interaction with the carousel; a timer sliding images in a background tab is pure waste. One timer per carousel, cleared on teardown.
4. **Transforms move slides.** The track animates with `transform: translateX()`; animating `left`/`margin` lays out every slide per frame.
5. **Indicators are cheap nodes,** not re-rendered lists — toggle a class on the active dot.

## Bad Example

```js
setInterval(() => {
  track.innerHTML = slides.map(render).join('');  // rebuild all slides
  track.style.marginLeft = `-${i * 100}%`;        // layout property
  i = (i + 1) % slides.length;
}, 3000);
```

- **Why it fails:** every three seconds, every slide re-renders (image decode included), the track forces layout, and the timer runs whether or not anyone can see the page. This is the eager-everything and polling-as-architecture anti-patterns wearing a UI.

## Checklist
- [ ] First slide in initial HTML, priority-hinted; others deferred.
- [ ] Swipe rides native scroll with snap points.
- [ ] Auto-advance pauses on hidden tab, hover and interaction.
- [ ] Navigation patches classes/transforms; zero rebuilds.
- [ ] Slide images carry explicit dimensions; the track never resizes on advance.
- [ ] Teardown (SPA navigation) clears the interval and observers.

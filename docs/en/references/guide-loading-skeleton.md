# Loading, Skeletons & JS-Gated Content Guide

> **Scope:** Loading states, skeleton screens, spinners — and content whose visibility a script controls, which is where a loading state quietly becomes a barrier.

## 0. The rule everything else follows

**A loading state is a promise, not content: announce the wait once, announce the outcome once — and never let the promise be the only thing the page can show.** The two failure modes are opposites and equally common: the *silent* skeleton (a screen-reader user acts on a half-loaded page, or waits with no signal anything is happening) and the *chatty* one (every shimmer and re-render announced). One status in, one status out.

1. **Mark the waiting region, not the world:** `aria-busy="true"` on the container being updated, removed when content lands.
2. **One status in, one status out:** a `role="status"` region (present in the DOM before the message) announces *"Loading results"*, then the outcome — *"12 results loaded"*. Never `role="alert"` for progress, never one announcement per skeleton block.
3. **Skeletons are scenery:** `aria-hidden="true"` on placeholder blocks. A skeleton in the accessibility tree reads as content that says nothing.
4. **The pulse respects `prefers-reduced-motion`** — a page-wide shimmer is precisely the ambient motion the preference exists to stop.
5. **Never move focus because something loaded** — announce and let the person arrive. If the user's focus was inside the replaced region, move it to the nearest stable ancestor, not to the top.
6. **A spinner is not progress:** past a moment, say what is happening; when the fraction is measurable, use a real `<progress>` with a label.

## JS-gated content — where the §6 anti-pattern lives

*Content Held Hostage by JavaScript* (`A11Y.md` §6) is a loading state that never resolves. The entry animation written as `opacity: 0` in CSS and revealed by script renders the page **empty** when the script fails, is blocked (corporate proxy, extension, CSP), or has not run yet — content in the DOM, invisible to everyone, and invisible to every checker, because in the checker's browser the script ran.

- **The default rendered state is the readable one.** Two correct shapes: gate the animation on a class an **inline pre-paint script** removes (`<html class="no-js">` → script strips it before first paint; CSS animates only when the class is gone), or start visible and animate *from* visible.
- **Scroll-reveal is the same trap:** below-the-fold content exists for readers, print and search *before* any `IntersectionObserver` fires — the observer adds the animation, it never adds the content.
- **`<noscript>` is not the fix.** The failing case is usually JavaScript *enabled* but broken, blocked or late — a `<noscript>` block helps none of those.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 4.1.3 Status Messages | AA | wait announced once, outcome announced once |
| 2.4.3 Focus Order | A | loading never steals or strands focus |
| 1.1.1 / Principle Zero | A | content never gated behind a script that may not run |
| Motion (House Rule†) | — | skeleton pulse honors `prefers-reduced-motion` |

## Tip for the AI:

Load the page twice: once with JavaScript disabled, once with it enabled and throttled to a crawl. At no point may the page be blank while its content sits in the DOM. Then run a screen reader through one load cycle — you should hear exactly two things: that the wait started, and what arrived.

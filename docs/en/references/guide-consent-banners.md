# Consent & Cookie Banners Guide

> **Scope:** Consent notices, cookie banners and privacy overlays — the first element the user meets, and the one most often generated automatically without review.

## 1. Decide first: does it block or not?

This fork defines everything else. Implementing the wrong pattern is the most common failure.

| If the banner… | Then it is… | And it must |
| :--- | :--- | :--- |
| prevents interacting with the page until answered | a **modal dialog** | move focus inside, contain it (SC 2.1.2), close on `Esc`, return focus to its origin — see [Modals](guide-modals.md) |
| leaves the page usable, occupying a strip | a **non-modal region** | **NOT** capture focus; be reachable in the natural tab order; announce itself via `role="region"` with an accessible name |

The classic error is the hybrid: a strip that does not trap focus but dims the page and swallows clicks — visually modal, semantically nonexistent. A screen reader user navigates a page that "looks" available and does not respond.

## 2. The banner MUST NOT obscure the focus indicator (SC 2.4.11)

A fixed strip at the bottom — the most common cookie-banner shape — covers the focused element when the user tabs to the end of the page. **That is a Level AA failure**, and it is invisible to anyone testing with a mouse.

- Reserve space in the layout (`padding-bottom` on `<body>` equal to the banner height) instead of merely overlaying.
- Verify by tabbing the entire page with the banner open: no focused element may be fully covered.

## 3. Parity between accept and reject

**House Rule†:** if "Accept all" is a one-click button, "Reject all" **MUST** be a one-click button, at the same navigation level and with the same visual weight.

Rejection hidden behind "Manage preferences" → a list of 40 vendors → "Save" is an effort barrier that lands disproportionately on people with motor limitations and cognitive fatigue. WCAG does not name this; the EAA and the GDPR do, and this standard's Principle Zero already answers it: if completing the task requires walking a maze, the task is broken.

## 4. Technical rules

1. **Native buttons.** `<button>` for the actions, never `<div onClick>`. That includes the closing "X".
2. **No keyboard trap (SC 2.1.2):** the user can always leave the banner by keyboard — to the page if non-modal; via `Esc` or an action if modal.
3. **No time limit.** A banner that closes itself, or assumes consent after N seconds, fails SC 2.2.1 and the legal basis along with it.
4. **Announce late appearance:** if the banner enters the DOM after load, it **MUST** be announced (`role="dialog"` with focus moved, or `role="status"` when non-modal and non-urgent).
5. **Target and contrast:** the buttons follow the active profile like any other control — the banner is not a density exception.
6. **Language:** banner copy is the densest legal jargon in the whole interface. Apply Section 6 of the [Cognitive guide](guide-cognitive.md): short sentences, active voice, the label states the outcome.

## 5. Third-party scripts

Most banners come from a consent management platform (CMP). **The obligation does not transfer with the script.**

- Test the vendor's banner with keyboard and screen reader **before** installing it, not after.
- If the CMP is inaccessible and cannot be replaced in the current cycle, that is an `EXCEPTIONS.md` entry — with risk owner, issue and expiry — not somebody else's problem.
- Many CMPs expose accessibility options that ship disabled (initial focus, labels, contrast). Those belong to configuration, not to the backlog.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 2.1.2 No Keyboard Trap | A | there is always a keyboard way out, modal or not |
| 2.4.11 Focus Not Obscured (Minimum) | AA | the fixed strip may not cover the focused element |
| 2.2.1 Timing Adjustable | A | no auto-dismiss and no consent by elapsed time |
| 4.1.3 Status Messages | AA | late appearance announced |
| 2.5.8 Target Size | AA | banner buttons follow the active profile's floor |

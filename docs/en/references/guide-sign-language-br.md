# Accessibility: Sign Language & Automatic Libras Translation

> **Scope:** Serving sign-language users — Libras in Brazil — including the automatic translation widgets (Hand Talk, VLibras), the Libras video window, and the line where an avatar stops being enough. Load when the audience includes Brazil or any sign-language population.

## 0. The rule everything else follows

For most sign-language users, sign language is the first language and written text is the **second**. Automatic translators (Hand Talk, VLibras) are best-effort layers that read the **rendered DOM, on user click or selection** — they translate what the markup exposes, in the language quality the content offers. Both halves are the developer's job: markup the widget can reach, and text that survives translation.

## 1. What the translators can and cannot reach

Hand Talk and VLibras capture **real text nodes** (Hand Talk also translates an image's `alt`). Every rule below is a translator dead-end and a WCAG failure at once:

- Text **MUST** be real DOM text — never inside an image, canvas or CSS pseudo-element (the core anti-pattern list already forbids all three; translators add one more reason).
- Informative images **MUST** carry `alt` (SC 1.1.1) — for Hand Talk, the `alt` *is* the translatable content.
- `lang` **MUST** be correct on the root and on foreign passages (SC 3.1.1/3.1.2): the translators assume the page language on input.
- **MUST NOT** apply `user-select: none` or `pointer-events: none` to text content — selection and click are the capture mechanism.
- **SHOULD NOT** place essential content in iframes: Hand Talk requires explicit wiring (`addListenersToIframe`) and the VLibras widget only reads the document it was instantiated in.

## 2. Text that survives translation

- Keep each text block **under ~500–1000 characters per element** — Hand Talk truncates beyond its `maxTextSize`; one paragraph per element, never a wall of text in a single node.
- **MUST NOT** fragment a sentence across multiple elements for styling (`<span>` chains, `<br>` line poetry): capture is per element, and fragments translate without context.
- **Expand acronyms on first occurrence** and mark them with `<abbr title="…">` (SC 3.1.4): a word absent from the sign dictionary is **fingerspelled letter by letter** (datilologia) — the single most reported frustration of Libras users with avatars.
- Microcopy follows plain-language rules — short sentences, direct order, one idea each ([Cognitive §6](guide-cognitive.md)): it serves the second-language reader *and* measurably improves automatic translation quality.

## 3. The Libras window (when there is media)

- Prerecorded video with an audio track **SHOULD** offer a **Libras interpretation window** — SC 1.2.6 (AAA), recommendation 5.14.6 of ABNT NBR 17225, and a recurring hard requirement in Brazilian public procurement. Captions do not substitute it: they are Portuguese, the user's second language.
- The window follows the broadcast conventions (NBR 15290): interpreter visible from the waist up, contrast with the background, no overlap with essential visual content.

## 4. Where the avatar stops

An automatic avatar does not reproduce the facial grammar of Libras — negation, interrogation and intensity are facial in the language — and the interpreting community (ACATILS, 2025) formally rejects avatars as substitutes for interpreters.

- For **critical content** — health, legal, financial, assessments — provide video with a **human interpreter**; the widget is a complement, never the answer.
- **MUST NOT** present the translation widget as what makes the site "accessible in Libras" — declare its best-effort nature on the accessibility page. (The overlay anti-pattern, core §6, is the same failure in another costume.)

## 5. Legal basis (Brazil)

Libras is a recognized national language (Lei 10.436/2002 + Decreto 5.626/2005); site accessibility is mandated by **LBI art. 63** (Lei 13.146/2015), with ABNT NBR 17225:2025 as its technical ballast — see [Governance §6.1](guide-governance.md).

*Success criteria covered: 1.2.6 Sign Language — Prerecorded (AAA) · 1.1.1 Non-text Content (A) · 3.1.1 Language of Page (A) · 3.1.2 Language of Parts (AA) · 3.1.4 Abbreviations (AAA) · 3.1.5 Reading Level (AAA)*

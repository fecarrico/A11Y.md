# Accessibility: Images & Alternative Text

> Scope: Alt text strategy, decorative images, complex images (charts/diagrams), and SVG accessibility.

## 1. Informative Images
Images that convey a concept or information.
### ✅ Correct
```html
<img src="sales-chart.png" alt="Bar chart showing a 20% sales growth in the first quarter.">
```
- **Why:** The `alt` summarizes the chart's conclusion, not just describes that it's a chart.

### ❌ Incorrect
```html
<img src="sales-chart.png" alt="Sales chart">
```
- **Problem:** The description is vague and does not convey the information contained in the image.

## 2. Functional Images
Images used as links or buttons (icons).
### ✅ Correct
```html
<a href="/print">
  <img src="printer-icon.png" alt="Print document">
</a>
```
- **Why:** The `alt` describes the **action** of the link, not the appearance of the icon (e.g., don't use "printer icon").

## 3. Decorative Images
Images that do not add content (borders, background illustrations).
### ✅ Correct
```html
<!-- Classified as decorative and confirmed by a human — see Section 5. -->
<img src="pretty-divider.png" alt="">
```
- **Why:** The empty `alt=""` tells the screen reader to ignore the image. **Never** omit the `alt` attribute, otherwise the reader will read the filename (e.g., "image-123-final.png").
- ⚠️ **The empty value is a confirmed decision, not a default.** The AI **MUST NOT** reach this classification on its own: the required flow is in **Section 5**. An `alt=""` applied unilaterally hides a possibly informative image from screen reader users — and no automated checker catches it, because the attribute is present.

## 4. The "Over-description" Problem
Avoid starting with "Image of..." or "Photo of...". The screen reader already announces that it's an image. Get straight to the point.

## 5. User-Supplied Images (Image Evidence)
When the image comes from the user — a pasted screenshot, an uploaded asset, a referenced file — the `alt` decision happens **before the image enters the code**, not after. *(This is the "Image Evidence" rule of the AI Behavior Contract, Section 2 of the core file.)*

**Step 1 — Check what you can perceive.**
- You **can** see the image (multimodal input, or an image-reading tool available in the environment): describe what it shows, then move to Step 2. Vision gives you the *content*; only the surrounding context gives you the *purpose* — the same photo can be decorative on one page and informative on another.
- You **cannot** see the image: request the description from the developer in the same turn. Never proceed with a guessed `alt`.

**Step 2 — Classify by the removal test.** *"If I remove this image, what does the user lose?"*
- Loses information → **informative**: the `alt` carries the content's conclusion (Section 1).
- Loses a function (link/button) → **functional**: the `alt` names the action (Section 2).
- Loses nothing → **decorative candidate**: empty `alt=""` — pending Step 3.

**Step 3 — Propose; the human decides.** Present the classification and the draft `alt` to the developer and get an explicit confirmation. The AI's reading of an image is a hypothesis, not evidence — the same principle behind the human screen-reader validation in the Complex Component Protocol. The confirmation is part of the workflow, not a formality.

Borderline classifications (e.g., a hero image that is arguably decorative) are pattern-level decisions: record them in `A11Y-DECISIONS.md` and reuse.

## Tip for AI:
Whenever generating a component with an image, the AI should ask itself: *"If I remove this image, what information does the user lose?"*. That answer should be your `alt`.

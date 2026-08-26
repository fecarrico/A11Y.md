# Accessibility: Visual Perception, Color & Contrast

> Scope: OKLCH color model, Delta E, APCA contrast, chart redundancy, and colorblindness QA protocol.

## 1. Color Models and Perceptual Distance
To ensure two colors are "distinguishable", it is not enough to look at the Hex code. We use the **OKLCH** color space (Luminance, Chroma, Hue), which is perceptually uniform.

- **Luminance Difference (L):** It is the most important factor for readability. Contrast must come first from the difference between "light" and "dark", and only then from the Hue.
- **Delta E (ΔE):** Measure of distance between two colors.
    - **ΔE > 20:** Noticeable difference for most users.
    - **ΔE > 40:** High-security difference for colorblind users.

## 2. Modern Contrast (Introduction to APCA)
While WCAG 2.1/2.2 uses the static ratio (e.g., 4.5:1), **APCA** (Advanced Perceptual Contrast Algorithm) is the suggested model for the future (WCAG 3).

- **Why it matters:** APCA considers that white text on a black background and black on a white background do not have the same visual impact (irradiation effects).
- **Practical Application:** Use APCA to validate the readability of very thin fonts or small sizes, where the 4.5:1 ratio might be misleading.
- **Tip:** Aim for a **Lc (Lightness Contrast)** score of at least 60 for body text.

## 3. Palette Definition Protocol

The moment the colors are born is the moment contrast is decided — this standard's benchmark found contrast failures in every uninstructed condition, and contrast is the web's largest audit debt (WebAIM Million: 83.9% of pages). When creating or changing design tokens, palettes or theme files, the AI **MUST**:

1. **Enumerate the intentional pairs** — every text/background and UI/background combination the tokens will form, including states (hover, focus, disabled, error) and both themes when there are two.
2. **Compute each pair's WCAG ratio at definition time** — [`tools/contrast-check.py`](https://github.com/fecarrico/A11Y.md/tree/main/tools) with a shell, the relative-luminance formula without one. Never "looks dark enough".
3. **Adjust luminance, not just hue**, until every pair clears the active profile's floor (core §0.1).
4. **Record the pair matrix** (pair → measured ratio) in `A11Y-DECISIONS.md`; the values feed `REPORT.md` §1.

A palette validated at birth cannot fail the audit; a palette validated only at audit time fails in production first.

## 4. Verification Protocol (QA)
To consider the task "Done" in terms of visual perception:
1. **Grayscale Test:** Turn off the screen colors. Can you still understand the hierarchy?
2. **Simulator Check:** Use tools like **Color Oracle** or browser simulators to check:
    - **Protanopia/Deuteranopia:** (Red/green deficiency - most common).
    - **Tritanopia:** (Blue/yellow deficiency - rare).
3. **Luminance Check:** Ensure the Luminance difference (L in OKLCH) between background and text is significant.

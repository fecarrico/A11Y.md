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

## 3. Verification Protocol (QA)
To consider the task "Done" in terms of visual perception:
1. **Grayscale Test:** Turn off the screen colors. Can you still understand the hierarchy?
2. **Simulator Check:** Use tools like **Color Oracle** or browser simulators to check:
    - **Protanopia/Deuteranopia:** (Red/green deficiency - most common).
    - **Tritanopia:** (Blue/yellow deficiency - rare).
3. **Luminance Check:** Ensure the Luminance difference (L in OKLCH) between background and text is significant.

# Accessibility: Images & Alternative Text

Image descriptions are the bridge between the visual and the understandable. For screen reader users, an image without `alt` is a "black hole" of information.

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
<img src="pretty-divider.png" alt="">
```
- **Why:** The empty `alt=""` tells the screen reader to ignore the image. **Never** omit the `alt` attribute, otherwise the reader will read the filename (e.g., "image-123-final.png").

## 4. The "Over-description" Problem
Avoid starting with "Image of..." or "Photo of...". The screen reader already announces that it's an image. Get straight to the point.

## Tip for AI:
Whenever generating a component with an image, the AI should ask itself: *"If I remove this image, what information does the user lose?"*. That answer should be your `alt`.

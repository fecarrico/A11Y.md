# Accessibility Guide: Buttons & Actions

> Scope: Semantic button usage, ARIA patterns, keyboard interactions, and labeling rules.

## Good Examples

### 1. Native Button element
```html
<button type="button" class="btn-primary">
  Submit Application
</button>
```
- **Why:** Native `<button>` elements have built-in keyboard support (Enter/Space) and are automatically identified as "button" by screen readers.

### 2. Icon Buttons with Text
```html
<button aria-label="Close modal">
  <svg>...</svg>
</button>
```
- **Why:** For buttons without visible text, `aria-label` provides the necessary context for screen reader users.

## Bad Examples

### 1. The "Clickable Div"
```html
<div onclick="submit()" class="my-button">Submit</div>
```
- **Implication:** This is invisible to keyboard users (no tab focus) and screen readers (no "button" role). It requires excessive JS to fix what HTML does for free.

### 2. Vague Labels
```html
<button>Click Here</button>
<button>Learn More</button>
```
- **Implication:** Screen reader users often list all buttons on a page to navigate. "Click Here" provides no context about what the button actually does. Use "Download Report" or "Read about our history" instead.

## Accessibility Implications
- **Affordance:** Visually distinctive buttons help users with cognitive impairments identify interaction points.
- **Precision:** Large tap targets (min 44x44px) are essential for mobile users and those with motor impairments.

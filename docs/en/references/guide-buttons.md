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
- See *Clickable Divs* — core §6.

### 2. Vague Labels
```html
<button>Click Here</button>
<button>Learn More</button>
```
- **Implication:** Screen reader users often list all buttons on a page to navigate. "Click Here" provides no context about what the button actually does. Use "Download Report" or "Read about our history" instead.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a page with buttons, WHEN I press `Tab`, THEN each button receives focus in turn, with a clearly visible focus ring.
- WHEN I press `Enter` or `Space` on a focused button, THEN its action runs — the same one a click triggers.
- WHEN I `Tab` through the page, THEN nothing that looks and acts like a button is skipped.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I `Tab` to a button, THEN I hear its name followed by "button" — never "clickable" or a bare "button".
- WHEN I reach an icon-only button, THEN I hear what it does ("Close modal"), not the icon or a file name.
- WHEN I open the screen reader's list of buttons, THEN every name says what the button does out of context — no "Click here" or "Learn more".

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe to a button, THEN I hear its name, then "button", and double-tapping runs the action.
- WHEN I swipe to an icon-only button, THEN I hear an action name, never "unlabelled button".

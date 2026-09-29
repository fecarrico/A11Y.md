# Accessibility Guide: Forms

> Scope: Label binding, error messaging, field grouping, and accessible form patterns.

## Good Examples

### 1. Explicit Labels and Helper Text
```html
<div class="form-group">
  <label for="email-field">Email Address</label>
  <input type="email" id="email-field" aria-describedby="email-help" required>
  <p id="email-help">We'll never share your email.</p>
</div>
```
- **Why:** The `label` is explicitly linked to the `id`. The `aria-describedby` links the helper text to the input for screen readers.

### 2. Error Handling
```html
<div class="form-group error">
  <label for="password-field">Password</label>
  <input type="password" id="password-field" aria-invalid="true" aria-errormessage="pass-error">
  <p id="pass-error" role="alert">Password must be at least 8 characters.</p>
</div>
```
- **Why:** `aria-invalid` signals the error state. `role="alert"` ensures the screen reader announces the error immediately.

### 3. Grouping with `fieldset` and `legend`
```html
<fieldset>
  <legend>Delivery method</legend>
  <label><input type="radio" name="delivery" value="pickup"> Pick up in store</label>
  <label><input type="radio" name="delivery" value="courier"> Courier</label>
</fieldset>
```
- **Why:** The `legend` is the group's name — the screen reader says it before the first option, so "Pick up in store" is heard as an answer to "Delivery method" (SC 1.3.1). Radio groups, related checkboxes and the parts of one answer (day / month / year) are groups; a `<div class="form-group">` is a CSS class, invisible to assistive technology. The controls themselves — checkbox, radio, switch, slider, native select — are specified in [Form Controls](guide-form-controls.md).

## Bad Examples

### 1. Placeholder as Label
```html
<input type="text" placeholder="Enter your username">
```
- See *Placeholder Labels* — core §6.

### 2. Information via Color Only
```html
<input type="text" style="border: 1px solid red;">
```
- See *Semantic Redundancy* — core §3.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a form, WHEN I `Tab` into a field, THEN its label stays visible beside it while I type — it does not vanish like a placeholder.
- WHEN I submit with an invalid field, THEN the error is shown as text next to that field, not only as a red border.
- WHEN I `Tab` through the form, THEN every field and the submit button are reached — nothing needs the mouse.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I `Tab` to a field, THEN I hear its label, the field type, "required" when it is, and the helper text.
- WHEN I submit with an invalid field, THEN I hear the error message right away, without moving.
- WHEN I return to that field, THEN I hear "invalid" and the error text together with its label.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe to a field, THEN I hear its label and helper text before double-tapping to edit.
- WHEN I double-tap Submit with an invalid field, THEN I hear the error message announced.

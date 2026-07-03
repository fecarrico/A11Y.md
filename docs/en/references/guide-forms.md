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

## Bad Examples

### 1. Placeholder as Label
```html
<input type="text" placeholder="Enter your username">
```
- **Implication:** Placeholders disappear when typing, losing context. They often fail contrast requirements and aren't reliably read by screen readers as labels.

### 2. Information via Color Only
```html
<input type="text" style="border: 1px solid red;">
```
- **Implication:** Color-blind users or those with low vision may not see the border change. Always add an icon or text indicating the error.

## Accessibility Implications
- **Cognitive Load:** Explicit labels reduce the effort needed to remember what a field is for.
- **Predictability:** Using standard input types (email, tel, date) allows browsers to provide specialized keyboards and autofill.

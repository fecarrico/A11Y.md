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
- See *Placeholder Labels* — core §6.

### 2. Information via Color Only
```html
<input type="text" style="border: 1px solid red;">
```
- See *Semantic Redundancy* — core §3.

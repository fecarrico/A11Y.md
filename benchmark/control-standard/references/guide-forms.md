# Forms & Input Latency Guide

> **Scope:** Validation timing, input responsiveness, submit flow

## Good Examples

### 1. Validation off the keystroke path
```js
input.addEventListener('input', () => {
  clearTimeout(pending);
  pending = setTimeout(() => validate(input.value), 250);
});
```
- **Why:** the keystroke handler does nothing but reschedule; validation runs when typing pauses. Typing latency stays at zero cost regardless of how expensive the validation is.

### 2. Submit with immediate acknowledgment
```js
form.addEventListener('submit', (e) => {
  e.preventDefault();
  submitBtn.disabled = true;            // same frame
  status.textContent = 'Saving…';       // same frame
  api.save(data).finally(() => { submitBtn.disabled = false; });
});
```
- **Why:** the user sees a response in the same frame as the click; the network cost is real but no longer *felt* as unresponsiveness, and the disabled trigger prevents a double submit.

## Bad Examples

### 1. Synchronous validation per keystroke
```js
input.addEventListener('input', () => {
  const result = validateAgainstRules(input.value, allRules); // 12ms
  rerenderErrorPanel(result);                                  // rebuilds DOM
});
```
- **Why it fails:** 12 ms of work plus a DOM rebuild on every keystroke turns a 60-word field into a slideshow. Validation cost scales with rules; typing cost must not.

### 2. Storage on the hot path
```js
input.addEventListener('input', () => {
  localStorage.setItem('draft', JSON.stringify(formState));
});
```
- **Why it fails:** synchronous storage serializes and blocks per keystroke. Drafts persist on `visibilitychange` or a long idle debounce, not per character.

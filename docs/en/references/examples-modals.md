# Accessibility Guide: Modals & Dialogs

Modals are high-risk components. They interrupt the user flow and can "trap" users if not implemented correctly.

## Good Examples

### 1. Focus Trapping and Labeling
```javascript
// When opening modal:
// 1. Save reference to the element that had focus.
// 2. Move focus to the modal title or first focusable element.
// 3. Keep focus inside the modal until closed.
```
```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Confirm Deletion</h2>
  <button aria-label="Close">X</button>
  ...
</div>
```
- **Why:** `role="dialog"` and `aria-modal="true"` tell the browser to ignore the rest of the page. `aria-labelledby` provides context.

### 2. Native HTML Dialog
```javascript
// To open a modal use the native HTMLDialogElement.showModal() method where possible. This will automatically move the focus inside the modal and return the focus to the invoking element when the modal is closed.
```
```html
<dialog aria-labelledby="modal-title" closedby="any" id="exampleDialog">
  <h2 id="modal-title">Confirm Deletion</h2>
  <button aria-label="Close" command="close" commandfor="exampleDialog">X</button>
  ...
</div>
```
- **Why:** The native `<dialog>` element comes with all required accessibility features out of the box. `closedby="any"` allows the dialog to be closed by pressing the escape key. `command="close"` and `commandfor=""` allows for closing the dialog using a button without any javascript and uses the native `invokerCommands` API. `aria-labelledby` provides context.

> ⚠️ **Experimental compatibility:** The `closedby` and `command`/`commandfor` attributes (invokerCommands API) are currently supported only in **Chrome 133+**. Check [Can I Use](https://caniuse.com) before using in production and consider a JavaScript fallback for other browsers.

### 3. Keyboard Control
- **Esc Key:** Should always close the modal.
- **Tab:** Should cycle through elements ONLY inside the modal.

## Bad Examples

### 1. Leaving Focus Behind
- **Implication:** If a modal opens and focus remains on the background trigger, a screen reader user might continue interacting with the page "underneath" the modal, leading to confusion and errors.

### 2. No Close Button
- **Implication:** Users who rely on screen readers or have cognitive disabilities might not know how to exit a modal if there isn't a clear, labeled "Close" action.

## Accessibility Implications
- **Modality:** Ensuring the user is aware they are in a "sub-state" of the application.
- **Restoration:** When the modal closes, focus MUST return to the element that triggered it, so the user knows where they are in the document.

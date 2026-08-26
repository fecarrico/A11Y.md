# Accessibility Guide: Modals & Dialogs

> Scope: Focus trapping, native dialog element, keyboard control, and modal anti-patterns.

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
- **Why:** `role="dialog"` announces the pattern and `aria-modal="true"` instructs **assistive technology** to ignore content outside the dialog. `aria-labelledby` provides context.
- ⚠️ **`aria-modal` is not a focus trap.** It does not talk to the browser and does not affect the `Tab` key: without JavaScript, focus still escapes the dialog into the page behind it. Containment is your responsibility — or use the native `<dialog>` in example 2, which implements it.

### 2. Native HTML Dialog
```javascript
// To open a modal use the native HTMLDialogElement.showModal() method where possible. This will automatically move the focus inside the modal and return the focus to the invoking element when the modal is closed.
```
```html
<dialog aria-labelledby="modal-title" closedby="any" id="exampleDialog">
  <h2 id="modal-title">Confirm Deletion</h2>
  <button aria-label="Close" command="close" commandfor="exampleDialog">X</button>
  ...
</dialog>
```
- **Why:** The native `<dialog>` element comes with all required accessibility features out of the box. `closedby="any"` adds *light dismiss* — closing by clicking outside the dialog; the `Esc` key **already works natively** in any dialog opened with `showModal()`, with no attribute at all. `command="close"` and `commandfor=""` allows for closing the dialog using a button without any javascript and uses the native `invokerCommands` API. `aria-labelledby` provides context.

> ⚠️ **Experimental compatibility:** The `closedby` and `command`/`commandfor` attributes (invokerCommands API) are currently supported only in **Chrome 133+**. Check [Can I Use](https://caniuse.com) before using in production and consider a JavaScript fallback for other browsers.

### 3. Keyboard Control
- **Esc Key:** Should always close the modal.
- **Tab:** Should cycle through elements ONLY inside the modal.

## Bad Examples

### 1. Leaving Focus Behind
- See *Leaked Focus Traps* — core §6.

### 2. No Close Button
- **Implication:** Users who rely on screen readers or have cognitive disabilities might not know how to exit a modal if there isn't a clear, labeled "Close" action.

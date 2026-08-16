# Toasts & Notifications Guide

> **Scope:** Async feedback, snackbars, notification queues

## Good Examples

### 1. One container, recycled
```js
const stack = document.getElementById('toast-stack'); // exists in initial HTML, empty
function toast(msg) {
  const el = pool.pop() ?? document.createElement('div');
  el.className = 'toast'; el.textContent = msg;
  stack.append(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => dismiss(el), 4000);
}
function dismiss(el) {
  el.classList.remove('show');
  el.addEventListener('transitionend', () => { el.remove(); pool.push(el); }, { once: true });
}
```
- **Why:** the stack container is reserved space — toasts entering and leaving shift nothing else on the page. Nodes are pooled instead of churned, and every timer has an owner and an end.

### 2. Entrance on the compositor
```css
.toast { transform: translateY(12px); opacity: 0; transition: transform .18s, opacity .18s; }
.toast.show { transform: none; opacity: 1; }
```
- **Why:** corner toasts animate over the page, not within its layout; `transform`/`opacity` keep the page's frame budget untouched even when several stack.

## Bad Examples

### 1. Toast as layout event
```js
banner.style.height = 'auto';       // inserted above content
content.style.marginTop = '56px';   // pushes the page down
```
- **Why it fails:** feedback that reflows the page charges every element below it and shifts what the user was reading. Notifications overlay; they do not displace.

### 2. Unbounded queue
```js
socket.on('event', (e) => toast(e.message));
```
- **Why it fails:** a chatty socket turns the corner of the screen into an unbounded render loop. Queue with a cap, coalesce repeats ("3 new messages"), and drop what the user can no longer act on.

## Checklist
- [ ] Toast container present and sized from the initial HTML; no CLS on show/hide.
- [ ] Timers cleared on dismiss and on page hide.
- [ ] Bursts coalesce; the queue has a maximum.
- [ ] Toast text renders without loading anything: no icon fetch, no font face unique to notifications.

# Practical Examples: Accessibility in Practice (A11Y)

This document complements the [**A11Y.md**](A11Y.md) with real examples extracted from day-to-day development, contrasting implementations that violate standards with their corrected, accessible versions.

---

## 1. Semantic Interaction and Operability
**Scenario:** Dashboard cards that serve as navigation shortcuts.

### 🔴 BAD (Anti-pattern)
The use of `div` with `onClick` makes it impossible for keyboard users or assistive technologies to perceive the element as interactive.

```tsx
// OverviewCard.tsx
<div 
  onClick={() => navigate('/components')} 
  className="glass-panel p-6 cursor-pointer hover:border-blue-500"
>
  <Puzzle className="w-5 h-5" />
  <p className="text-3xl font-bold">120</p>
  <p className="text-xs font-semibold uppercase">Components</p>
</div>
```

### ✅ ACCESSIBLE
Using a semantic tag (`button` or `a`) guarantees native focus, Enter/Space key support, and correct announcement by screen readers.

```tsx
// OverviewCard.tsx
<button 
  onClick={() => navigate('/components')}
  aria-label="View component list (120 indexed)"
  className="glass-panel p-6 text-left hover:border-blue-500 focus:ring-2 focus:ring-blue-500 outline-none"
>
  <Puzzle className="w-5 h-5" aria-hidden="true" />
  <p className="text-3xl font-bold">120</p>
  <p className="text-xs font-semibold uppercase">Components</p>
</button>
```

> **Why? (A11Y.md - Section 6):** "MUST NOT use div or span for click actions. Prefer native buttons... to guarantee focus behavior and keyboard events."

---

## 2. Typography and Readability
**Scenario:** Secondary metadata or captions on cards.

### 🔴 BAD (Anti-pattern)
Fonts below 12px drastically reduce readability for users with low vision or on devices with reduced brightness.

```tsx
// TokenList.tsx
<p className="text-[10px] text-gray-500 mt-1.5">
  Last synced 2 hours ago
</p>
```

### ✅ ACCESSIBLE
Maintaining a minimum of 12px (`text-xs` in standard Tailwind) guarantees compliance. If density is critical, increase the contrast to compensate.

```tsx
// TokenList.tsx
<p className="text-xs text-gray-700 font-medium mt-1.5">
  Last synced 2 hours ago
</p>
```

> **Why? (A11Y.md - Section 4):** "Text MUST NOT be smaller than 12px. The success of perception is guaranteed by a readable scale."

---

## 3. Forms and Relationships
**Scenario:** Input fields on authentication or configuration screens.

### 🔴 BAD (Anti-pattern)
Labels without a technical connection to the input prevent the screen reader from announcing the field name when focusing on it.

```tsx
// AuthForm.tsx
<label className="block text-xs font-semibold uppercase">
  Email
</label>
<input
  type="email"
  placeholder="name@company.com"
  className="w-full px-4 py-3 border rounded-xl"
/>
```

### ✅ ACCESSIBLE
Mandatory use of `id` on the input and `htmlFor` on the label to create the semantic bond.

```tsx
// AuthForm.tsx
<label 
  htmlFor="auth-email" 
  className="block text-xs font-semibold uppercase"
>
  Email
</label>
<input
  id="auth-email"
  type="email"
  required
  placeholder="name@company.com"
  className="w-full px-4 py-3 border rounded-xl focus:ring-2"
/>
```

> **Why? (A11Y.md - Section 3):** "Forms MUST have explicit labels connected via id and for. Avoid reinventions that break native events."

---

## 4. Dynamic Feedback
**Scenario:** Error or success notifications appearing after an action.

### 🔴 BAD (Anti-pattern)
Messages visually injected into the DOM programmatically are ignored by screen readers if there is no active alert.

```tsx
// Notification.tsx
{error && (
  <div className="p-3 bg-red-100 text-red-700 border border-red-500">
    {error}
  </div>
)}
```

### ✅ ACCESSIBLE
Inclusion of ARIA attributes to ensure the state change is announced immediately.

```tsx
// Notification.tsx
{error && (
  <div 
    role="alert" 
    aria-live="assertive"
    className="p-3 bg-red-100 text-red-700 border border-red-500"
  >
    {error}
  </div>
)}
```

> **Why? (A11Y.md - Section 3):** "Dynamic events based on state... MUST be actively read or informed through aria-live regions or role='alert'."

---

## Severity Summary
| Issue | Level | Impact |
| :--- | :--- | :--- |
| Click on `Div` | 🔴 **CRITICAL** | Blocks keyboard users. |
| Lack of `role="alert"` | 🟠 **HIGH** | Blind user doesn't know if an error occurred. |
| Font < 12px | 🟠 **HIGH** | Hinders reading and causes eye strain. |
| Disconnected label | 🟠 **HIGH** | Loss of context in forms. |

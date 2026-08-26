# Date Picker & Calendar Guide

> **Scope:** Date fields, calendar grids and range pickers — adopt rather than reinvent (`A11Y.md` §6).

## 0. The rule everything else follows

**The text input is the feature. The calendar is an affordance on top of it.**

Someone who knows the date already types it in a second. Making them navigate a grid of thirty cells instead is slower for everyone and hostile to keyboard, voice-control and screen-reader users, who now have to arrow through a month to enter something they could have spelled. A picker that removes the typed input is the single most common way a date field becomes unusable.

```tsx
// ❌ The calendar as the only path in
<div className="date-field" onClick={openCalendar}>{value || "Select a date"}</div>

// ✅ A real input, with the calendar as an optional companion
<label htmlFor="checkin">Check-in date</label>
<span id="checkin-fmt">Format: DD/MM/YYYY</span>
<input id="checkin" name="checkin" type="text" inputMode="numeric"
       aria-describedby="checkin-fmt" autoComplete="off" />
<button type="button" aria-label="Choose check-in date from calendar"
        aria-expanded={open} aria-controls="checkin-cal">📅</button>
```

**Accept what people actually type.** Parse `01/02/2026`, `1/2/26`, `2026-02-01` and paste from another field; do not reject on punctuation. Blocking paste on a date field fails SC 3.3.8 for the same reason it fails on a password: it turns a copy into a memory test.

## 1. The format goes before the field, not after the error

The expected format **MUST** be visible before typing starts, outside the field (`A11Y.md` §6 — *Placeholder Labels*). A format that only appears as a validation error is a trap the user has to spring first. Bind it with `aria-describedby` so the screen reader hears it while the field is empty, not only after failure. Same rule for constraints that matter — "no later than 30 days from today" belongs beside the label, not in the rejection.

## 2. The calendar grid

Use the [APG Date Picker Dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/). What it requires, in short:

1. **Structure:** the month is a `role="grid"` (or a real `<table>`), rows are weeks, cells are days. Weekday headers are column headers, not decorative letters.
2. **One tab stop, arrows inside** — the grid holds a single tabbable cell (`tabindex="0"` on the focused date, `-1` on the rest); ← → move by day, ↑ ↓ by week, `Home`/`End` to the week's edges, `PageUp`/`PageDown` by month, `Shift` + those by year.
3. **Every cell states its full date**: `aria-label="15 March 2026"` — "15" alone is meaningless out of the visual grid. Mark today with `aria-current="date"` and the chosen day with `aria-selected="true"`.
4. **Opening moves focus** into the grid, onto the selected date, or today when nothing is selected. **`Esc` closes and returns focus to the trigger.** Choosing a date closes it, returns focus to the input, and the input holds the value as text.
5. **Unavailable dates use `aria-disabled="true"`, not removal:** they stay reachable so the reader can tell "unavailable" from "does not exist", and the reason belongs in the label — *"3 March 2026, unavailable, minimum stay two nights"*. Never signal availability by color alone (SC 1.4.1).

## 3. Announce the month change

Arrowing past the end of a month, or pressing the next-month button, changes the whole grid silently — the classic reason people get lost in a generated picker. Announce the new month from a live region, and keep the visible caption (`<h2 id="cal-label">March 2026</h2>`) as the grid's accessible name:

```tsx
<div role="status" aria-live="polite" className="sr-only">{monthLabel}</div>
```

## 4. Ranges

- Two labelled inputs (*Start date*, *End date*), never one field the user is expected to click twice into.
- Announce the state of the selection: *"Start 12 March selected. Choose an end date."*
- The chosen range must be visible without relying on a background tint alone — mark the endpoints with text or shape too.
- If the second date is constrained by the first, say the constraint out loud when it changes; do not just grey out half the grid.

## 5. When the native input is the better answer

`<input type="date">` gives you the platform's own picker — already keyboard-operable, already localized, already familiar to the person's screen reader, and free on mobile. It is the right default whenever you do not need range selection, custom disabled dates, or a specific visual identity. The reasons *not* to use it (inconsistent styling, no range support, format tied to locale) are product decisions — record them in `A11Y-DECISIONS.md` rather than re-deciding per screen. On native platforms, use the system picker: see [Platform-Native Mapping](guide-platform-native.md).

*Success criteria covered: 1.3.1 Info and Relationships (A) · 2.1.1 Keyboard (A) · 2.1.2 No Keyboard Trap (A) · 3.3.2 Labels or Instructions (A) · 3.3.8 Accessible Authentication (AA) · 1.4.1 Use of Color (A) · 4.1.2 Name, Role, Value (A)*

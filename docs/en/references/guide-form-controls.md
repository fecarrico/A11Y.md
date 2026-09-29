# Form Controls Guide

> **Scope:** Checkboxes, radio groups, switches, sliders and the native `<select>` — the controls generated most often and specified least — and the disabled state they all share. Labels, errors and grouping live in [Forms](guide-forms.md); searchable selects in [Autocomplete & Combobox](guide-autocomplete.md).

## 0. The rule everything else follows

**The native control is the pattern. A custom one owes everything the native one gave for free — name, role, state, the same keys — and must prove it.** `<input type="checkbox">`, `<input type="radio">`, `<input type="range">` and `<select>` are keyboard-operable, announced with role and state, styleable with `appearance: none` and `accent-color`, and free on every platform. A `<div>` that looks like a checkbox has none of that, and axe cannot tell the two apart once `role` and `aria-checked` are sprinkled on — it is the *Half-Climbed ARIA Ladder* of `A11Y.md` §6 at the smallest scale.

```html
<!-- ❌ Looks like a checkbox, is a div: no name, no role, no state, no Space -->
<div class="checkbox" onclick="toggle(this)"><span class="box"></span> Remember me</div>

<!-- ✅ The native control, styled -->
<label><input type="checkbox" name="remember"> Remember me</label>
```

Choose the control by what it does, not by its shape (SC 1.3.1): one choice among several → radio group; independent yes/no options → checkboxes; a setting that takes effect immediately → switch; a value in a range → slider with a numeric field beside it; one option from a list → `<select>`.

## 1. Checkbox

1. **The label is the target.** Bind it with `for`/`id` or wrap the control: clicking or tapping the text toggles the box, and the touch target grows to the whole label (SC 2.5.8).
2. **Three states, each visible without color** (SC 1.4.1): checked, unchecked and — when a parent summarizes its children — indeterminate: `el.indeterminate = true` on the native control, announced as "mixed". A custom checkbox conveys the same through `aria-checked="true|false|mixed"`.
3. **`Space` toggles; `Enter` submits the form.** A custom checkbox that toggles on `Enter`, or does nothing on `Space`, fails SC 2.1.1.
4. **Independent options only.** If choosing one must un-choose the others, it is a radio group, not a set of checkboxes with script.

## 2. Radio group

1. **The group has a name.** `<fieldset>` + `<legend>` (see [Forms §3](guide-forms.md)), or `role="radiogroup"` + `aria-labelledby` on a custom group. The legend is what the screen reader says before the first option — without it, "Yes" and "No" are answers to a question nobody heard.
2. **Same `name`, one tab stop.** Native radios sharing a `name` form the group: `Tab` reaches the checked option (or the first), `↑`/`↓`/`←`/`→` move **and select**, `Space` selects the focused one. A custom group reproduces exactly this roving focus.
3. **No option pre-checked when the answer matters** — a consent, a payment method: the person chooses, and the form reports it when they did not (SC 3.3.1). A silently pre-selected option is a decision the user never made.
4. **The selected state is not only color:** a filled dot, a check, a bolder label — anything that survives forced-colors mode and a monochrome print (SC 1.4.1).

## 3. Switch

A switch is a checkbox whose change takes effect **now** — no Save button, no confirmation.

1. **Markup:** `<button type="button" role="switch" aria-checked="true|false">`, or `<input type="checkbox" role="switch">`. The screen reader announces "switch, on/off"; `Space` (and `Enter` on a button) toggles.
2. **The label names the setting — never the current state, never the action.** "Notifications" stays "Notifications" whether on or off; the state comes from `aria-checked`. A label that flips to "Turn off" produces the announcement *"Turn off, switch, on"* — two truths that contradict (SC 4.1.2).
3. **On and off are visible without color:** the knob's position plus a text or icon cue, and the track at 3:1 against its surroundings in both states (SC 1.4.11).
4. **If the change needs confirmation or a Save action, it is not a switch** — use a checkbox and let the form submit.

## 4. Slider (range)

1. **Prefer `<input type="range">`** with a `<label>`, `min`, `max`, `step` — and the **current value visible in text** beside it: a knob on a track tells a sighted person nothing exact either.
2. **When the number is not the meaning, say the meaning:** `aria-valuetext="Medium"` for a 1–3 quality slider, `"14:30"` for a time. A custom slider owes `role="slider"`, `aria-valuemin`/`aria-valuemax`/`aria-valuenow`, and `aria-valuetext` where the number alone says nothing.
3. **Keys:** `←`/`↓` decrease and `→`/`↑` increase by `step`; `PageUp`/`PageDown` by a larger step; `Home`/`End` to the ends. Every key change updates the visible value and the announced one.
4. **Dragging is a shortcut** (SC 2.5.7): the value must be settable without a drag — a click or tap on the track, or step buttons. **Precision needs a second door** (House Rule†): when the exact value matters — a price, a dosage, a date range — pair the slider with a numeric `<input>` bound to the same value. Dragging to exactly 37 is a dexterity test, and the numeric field is also the voice-control path.
5. **The thumb is a target:** 24×24 CSS px minimum (SC 2.5.8), 44×44 under the House Rule† — and the track is not the only way to reach the value.

## 5. Native select

1. **`<select>` first.** It opens the platform's own list, is operable with arrows and type-ahead, and is what the person's screen reader already knows. Restyle the closed state; leave the open list to the platform.
2. **A placeholder `<option>` is not a label.** "Choose a country" as the first option disappears the moment a value is chosen; the `<label>` stays (`A11Y.md` §6, *Placeholder Labels*). If a blank choice must exist, give it a real name ("No preference") and `value=""`.
3. **Group with `<optgroup label="…">`** when the list has sections; the group label is announced when the reader enters it.
4. **Changing the selection MUST NOT navigate or submit on its own** (SC 3.2.2): a person arrowing through the options with a screen reader fires `change` on every step. Add a button.
5. **Search, multi-select with chips, options with icons — that is a combobox:** see [Autocomplete & Combobox](guide-autocomplete.md), and record the decision to leave the native element in `A11Y-DECISIONS.md`.

## 6. Disabled controls

1. **Native `disabled`** removes the control from the tab order and announces it as unavailable — right when the control truly cannot be used now.
2. **`aria-disabled="true"`** keeps it focusable and announced as unavailable — right when the person needs to *find* it to learn why it is off (a submit button waiting for required fields). Pair it with the reason, bound by `aria-describedby`, and never rely on greyed-out color alone (SC 1.4.1).
3. **The reason text is not exempt from contrast.** The disabled control itself is (SC 1.4.3, inactive components); the explanation beside it is body text and follows the profile's floor.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a form with a checkbox, WHEN I reach it with `Tab` and press `Space`, THEN it toggles — and `Enter` does not toggle it.
- GIVEN a radio group, WHEN I press `Tab`, THEN a single stop lands on the checked (or first) option, and `↑`/`↓` move the selection without leaving the group.
- GIVEN a switch, WHEN I press `Space`, THEN it turns on or off at once, with no Save step.
- GIVEN a slider, WHEN I press `→`, `PageUp` and `End`, THEN the visible value changes by one step, by the larger step, and to the maximum.
- GIVEN a `<select>`, WHEN I arrow through its options, THEN nothing navigates or submits until I activate a button.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I reach a checkbox, THEN I hear its label, "checkbox", and "checked", "not checked" or "mixed".
- WHEN I enter a radio group, THEN I hear the legend before the first option, and each option as "radio button, n of m".
- WHEN I toggle a switch, THEN I hear the same setting name with "switch, on" or "switch, off" — the name itself never changes.
- WHEN I move a slider, THEN I hear the new value — or its meaning, when the number alone says nothing.
- WHEN I reach a disabled control, THEN I hear "unavailable" and, if it is still focusable, the reason it is off.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe to a checkbox or a switch and double-tap, THEN the state I hear next is the opposite of the one I heard before.
- WHEN I swipe through a radio group, THEN I hear the group name once, then each option with its position, and double-tap selects it.
- WHEN I focus a slider and swipe up or down, THEN the value changes by one step and is announced.

*Success criteria covered: 1.3.1 Info and Relationships (A) · 3.3.2 Labels or Instructions (A) · 4.1.2 Name, Role, Value (A) · 2.1.1 Keyboard (A) · 1.4.1 Use of Color (A) · 1.4.11 Non-text Contrast (AA) · 2.5.8 Target Size (Minimum) (AA) · 2.5.7 Dragging Movements (AA) · 3.2.2 On Input (A) · 3.3.1 Error Identification (A)*

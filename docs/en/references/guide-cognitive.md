# Accessibility: Cognitive Accessibility, Language & Conflicting Needs

> Scope: memory, attention, language, time and decision load — the criteria WCAG 2.2 added for cognition, text spacing, and the protocol for when two accessibility needs contradict each other.

## 1. SC 3.3.8 Accessible Authentication (AA) — the one generated code violates most

The criterion forbids requiring a **cognitive function test** at any step of authentication — recalling a password, transcribing characters, solving a puzzle, performing a calculation — unless an alternative, an assistance mechanism, object recognition, or user-supplied personal content is available.

In practice it almost always fails on one of these four lines:

### ❌ Incorrect

```html
<!-- 1. Blocking paste defeats the password manager: the "memory test" is back -->
<input type="password" onpaste="return false" oncopy="return false">

<!-- 2. Without autocomplete, autofill does not know what to fill -->
<input type="password" name="pwd">

<!-- 3. Asking for password characters by position is a pure memory test -->
<label>Enter the 3rd and 7th character of your password</label>

<!-- 4. Transcription CAPTCHA with no alternative -->
<img src="captcha.png"><input name="captcha" placeholder="Type the characters">
```

### ✅ Correct

```html
<input type="email" name="username" autocomplete="username">
<input type="password" name="password" autocomplete="current-password">
<!-- paste allowed, password manager works, field identified -->
```

- **Never block paste on a password field.** It is the cheapest mitigation of the criterion and the most common regression: anyone relying on a password manager is pushed back into memorizing.
- **Correct `autocomplete`** (`username`, `current-password`, `new-password`, `one-time-code`) is what lets the browser and the manager act as the "assistance mechanism" the criterion accepts.
- **CAPTCHA:** where unavoidable, offer at least two modalities (e.g. visual + audio), or prefer *object recognition* challenges, which the criterion explicitly permits. Transcribing distorted text does not pass.
- Under the **Shield** profile, SC 3.3.9 (AAA) also removes the object-recognition and personal-content exceptions.

## 2. SC 3.3.7 Redundant Entry (A)

Information the user already provided **in the same process** MUST be auto-populated or offered for selection — not asked for again.

- Classic failure: a checkout asking for the address at step 2 and again at step 4; a multi-step form that loses everything on Back; a signup that collects the email and then asks you to "confirm your details" by typing it all over.
- **The criterion's own exceptions:** re-entry is essential (password confirmation), it is a security requirement, or the previous information is no longer valid.
- In code: form state survives step navigation and the Back button. If you are generating a wizard, state is part of the accessibility requirement, not a UX refinement.

## 3. SC 3.2.6 Consistent Help (A)

If a help mechanism — human contact, phone, chat, contact form, automated help — exists across multiple pages, it MUST appear in the **same relative order** on all of them.

- It does not require help to exist; it requires that, where it exists, it does not move. People with spatial memory difficulty relocate help by position.
- In code: the help entry point lives in the shared layout (header/footer/template), never positioned page by page.
- "Same relative order" is not the same pixel coordinate: the layout may respond to the viewport as long as the order among elements is preserved.

## 4. SC 1.4.12 Text Spacing (AA)

Content MUST survive with no loss of information or function when the user forces, via their own stylesheet: line height **1.5×** the font size, spacing after paragraphs **2×**, letter spacing **0.12×** and word spacing **0.16×**.

This is the criterion that serves dyslexia and low vision directly, and it is broken by three patterns of generated CSS:

```css
/* ❌ fixed height on a text container — the text overflows or is clipped */
.card { height: 120px; overflow: hidden; }

/* ❌ line height locked against the user's preference */
p { line-height: 1.2 !important; }

/* ✅ the container follows the content */
.card { min-height: 120px; }
p { line-height: 1.5; }
```

## 5. SC 2.2.1 Timing Adjustable (A)

Every time limit MUST be able to be **turned off**, **adjusted** to at least 10× the default, or **extended**: warned at least 20 seconds in advance, extendable at least 10 times through a simple action ("press the space bar").

Banking sessions, carts holding stock and timed assessments are the real cases. *(Moving-content mechanics — carousels, autoplay — are SC 2.2.2, in the [Time-Based Media guide](guide-media.md).)*

## 6. Language

WCAG only requires a reading level at AAA (SC 3.1.5), which leaves clarity outside AA conformance — and not outside the obligation to be usable. When the AI generates interface text:

- **Active voice, short sentences, one idea per sentence.** "Do not forget to confirm" becomes "Confirm".
- **No double negatives**, no stacked conditionals.
- **Literal, not figurative.** Metaphor, irony and idiom are direct barriers for part of the autistic audience and for second-language readers.
- **The most common word that does the job.** "Use" rather than "utilize"; "before" rather than "prior to".
- **The label states the outcome**, not the mechanism: "Save draft", not "Submit".
- **A critical instruction never lives in a `placeholder` or a tooltip.** It must be visible while the person is deciding.
- **An error names the way out.** "Invalid postcode" is a diagnosis; "A postcode has 5 digits — check whether one is missing" is an instruction.
- **Sensory Language (SC 1.3.3):** instructions **MUST NOT** rely on senses alone — "click the round button on the right", "listen for the tone". Name the control by its visible label: "click **Submit**, at the end of the form". Format instructions ("DD/MM/YYYY") live outside the input, linked via `aria-describedby`.

## 7. Conflicting access needs

Not every conflict is accessibility against business. Some are **accessibility against accessibility**, and that is where an agent quietly picks one population and calls the result conformance.

| Axis | One need | The opposing need |
| :--- | :--- | :--- |
| Motion | transition animation sustains continuity for people who struggle to track context change | translation and parallax trigger nausea in vestibular disorders |
| Language | simplifying reduces cognitive load | simplifying removes precision the expert user depends on |
| Contrast | maximum contrast serves low vision | maximum contrast assaults brightness sensitivity (Irlen, migraine) |
| Time | a short limit protects a sensitive session | a short limit excludes people who read or type slowly |
| Density | more per screen means less navigation for people with chronic pain or motor limits | more per screen raises the load for people with attention deficits |

### The protocol

1. **Detect it and say so.** When mitigating one need creates a barrier for another, the AI **MUST** name both populations instead of silently optimizing for one.
2. **Prefer the mechanism to arbitration.** Where a channel exists for the user to decide — `prefers-reduced-motion`, `prefers-contrast`, an account preference, system zoom — the answer is to implement the channel, never to choose on the user's behalf. That is how the motion conflict is already resolved in the [Media guide](guide-media.md).
3. **With no mechanism, escalate.** The AI **MUST NOT** decide alone which disability gets served. Present the conflict, both populations and the options to the developer — same shape as *Image Evidence*: the machine prepares the evidence, the human establishes the decision.
4. **Record it in `A11Y-DECISIONS.md`,** indexed by pattern, with **both needs named** and the reason for the choice. A conflict resolved but unrecorded returns as divergence in the next component.
5. **Majority is not a criterion.** "Most users prefer" is a usability argument, not an accessibility one: the smaller population is precisely the one the standard exists not to lose.

## 8. The W3C's eight objectives (coverage map)

The [W3C Cognitive Accessibility Guidance](https://www.w3.org/WAI/WCAG2/supplemental/#cognitiveaccessibilityguidance) organizes the field into eight objectives. They are not normative — they exist to surface the barrier no SC names:

1. Help users understand what things are and how to use them
2. Help users find what they need
3. Use clear and understandable content
4. Help users avoid mistakes and know how to correct them
5. Help users focus
6. Ensure processes do not rely on memory
7. Provide help and support
8. Support adaptation and personalization

*Success criteria covered: 1.3.3 Sensory Characteristics (A) · 3.2.6 Consistent Help (A) · 3.3.7 Redundant Entry (A) · 2.2.1 Timing Adjustable (A) · 3.3.8 Accessible Authentication (Minimum) (AA) · 1.4.12 Text Spacing (AA) · 3.3.2 Labels or Instructions (A) · 3.3.3 Error Suggestion (AA) · 3.3.9 Accessible Authentication (Enhanced) (AAA (Shield profile)) · 3.1.5 Reading Level (AAA)*

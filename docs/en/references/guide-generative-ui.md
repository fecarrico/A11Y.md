# Generative & Conversational Interfaces Guide

> **Scope:** Chat interfaces, streaming model output, and UI a model assembles at runtime — the case where the interface **is** the AI.

## 0. The rule everything else follows

**Streaming output and live regions are natural enemies.** A response arriving token by token, inside `aria-live="polite"`, produces a screen reader that either stutters through every fragment or restarts the whole message on each mutation. It is the defining failure of generated chat UIs, and it passes every automated checker, because the markup is textbook-correct.

```tsx
// ❌ Announces the message dozens of times as it grows
<div aria-live="polite">{streamingText}</div>

// ✅ The stream renders silently; a small region announces state changes only
<div aria-busy={isStreaming}>{streamingText}</div>
<div role="status" aria-live="polite" className="sr-only">
  {isStreaming ? "Generating response" : lastCompleted ? "Response ready, 240 words" : ""}
</div>
```

**Announce the transitions, render the content.** The person reaches the text with their own reading commands, when they choose — which is how they read every other document.

## 1. The conversation is a log, not a feed

- The message list is `role="log"` (an implicit `aria-live="polite"` with `aria-relevant="additions"`): new entries are announced, existing ones are not re-read. Never `role="alert"`, never `aria-live="assertive"` — an interruption per message makes the interface unusable.
- **Every message states who is speaking, in text.** Avatar color, alignment and bubble shape are invisible to a screen reader and ambiguous in high-contrast mode. A visually-hidden `You:` / `Assistant:` prefix, or a heading per turn, is the whole fix.
- Give each turn a landmark or heading so long conversations are navigable by heading — scrolling is not navigation.
- Timestamps as `<time datetime="…">`, with a readable label: "2 minutes ago" alone is not resolvable out of context.

## 2. Streaming, stopping and waiting

1. **`aria-busy="true"`** on the region being written, cleared when the stream ends.
2. **A Stop generating control is a requirement, not a nicety** — a response that writes for forty seconds and cannot be stopped is moving content the user cannot escape (SC 2.2.2). It must be reachable by keyboard *while* the stream runs, and it must be the same control for everyone.
3. **Never move focus on your own.** Yanking focus to the incoming response destroys what the person was doing — typing, reviewing an earlier answer. Announce readiness instead, and offer an explicit way in ("Skip to latest response") for people who want it.
4. **Nothing may depend on the stream having finished.** Copy, retry and citations must exist for a partial response too, or the user who stops early is stranded.
5. **No time limits on the composer.** Sessions that expire mid-thought fail SC 2.2.1 and are worse here, where the input is long-form.

## 3. What the model renders is markup, not decoration

Model output becomes real UI, and the semantics have to survive the conversion:

- **Headings become real headings** at the right level for the page — not `<p><strong>`. A response with six bold pseudo-headings is unnavigable.
- **Lists become `<ul>`/`<ol>`**; tables become `<table>` with headers (see [Tables](guide-tables.md)).
- **Code blocks** get a language label in text, a real `<pre><code>`, and a copy button with a unique accessible name. Horizontal scroll containers follow the conditional focus rule (`A11Y.md` §6 — *Focus Traps Nobody Asked For*).
- **Images and diagrams the model generates carry the same obligation as any other image** — see [Images](guide-images.md) and *Image Evidence* (`A11Y.md` §2). An assistant that emits `alt=""` on a chart it just drew is fabricating a decorative classification.
- **Math, charts and embedded artifacts** are not exempt for being generated: whatever appears in the DOM is the product's responsibility, not the model's.

## 4. Per-message actions need distinct names

A thread with twenty responses produces twenty "Copy" buttons, twenty "Regenerate", twenty thumbs-up. To a screen-reader user listing the controls, they are indistinguishable.

```tsx
<button aria-label={`Copy response ${index + 1}`}>Copy</button>
```

Keep the visible text short and put the distinction in the accessible name — and remember the name **must contain** the visible text (SC 2.5.3, `A11Y.md` §3): `aria-label="Copy response 3"` around a button reading "Copy" is correct; `aria-label="Duplicate"` is a Label in Name failure.

## 5. UI the model assembles at runtime

When a model composes components live — a generated form, a rendered chart, a dynamic dashboard — **no code review ever sees that output.** The mechanical checks the pipeline runs on the repository do not apply to markup that did not exist at build time.

- Constrain generation to a **vetted component set** rather than free-form markup: the accessibility is then a property of the library, verified once, not of each generation.
- **Verify after render, not only before ship:** run an automated pass (axe or equivalent) against the composed DOM in the environments where that is possible, and treat what it finds as a defect in the generator, not in the session.
- Whatever the generator cannot guarantee — an image's alt, a media caption, a chart's data equivalent — must be **requested from the human in the loop**, exactly as *Image Evidence* and *Media Evidence* require. Generation does not create an exemption; it removes the reviewer, which is the opposite.
- This is the same reasoning as *Independent Verification* (`A11Y.md` §2) applied one layer down: the component that produced the markup is not the witness that it conforms.

## 6. Cognitive load is the load-bearing wall here

Conversational interfaces put the whole burden of structure on the reader. Apply [Cognitive Accessibility](guide-cognitive.md) in full, and specifically:

- **Plain language in the product's own copy** — labels, empty states, error text. The model's answer is content; the interface around it is yours.
- **Nothing that must be remembered across turns**: if the assistant asks for something already provided, that is Redundant Entry (SC 3.3.7) in conversational clothing.
- **Errors and refusals are content, not silence.** "Something went wrong" in a `role="status"` region, with what to do next — a stream that simply stops leaves no signal that anything happened at all.
- **Say what the assistant is** in the interface. People who cannot see the visual framing deserve the same disclosure everyone else gets from the layout.

## Sources

- **Live region mechanics** — the behavior §0 and §1 rely on (a region must exist before its first message; how additions are processed): [WAI-ARIA — `log` role](https://www.w3.org/TR/wai-aria-1.2/#log) · Sara Soueidan, [*Accessible notifications with ARIA Live Regions*](https://www.sarasoueidan.com/blog/accessible-notifications-with-aria-live-regions-part-1/).
- **Why token-streams stutter or restart differently per reader** — live-region handling diverges measurably across screen reader/browser pairs, which is why this guide announces transitions instead of streaming content: [a11ysupport.io — `aria-live` test results](https://a11ysupport.io/tech/aria/aria-live_attribute).
- **Runtime-assembled UI needs verification at render (§5):** *Accessible GenAI UI Generation with Post-Render Verification*, ICCHP 2026 ([Springer](https://link.springer.com/chapter/10.1007/978-3-032-31285-3_47)) — static standards cannot reach markup that only exists at runtime; a second check must run where the interface is composed.
- **Cognitive load in conversational interfaces (§6):** Hervás et al., *Cognitive Accessibility in Generative AI Interfaces* — systematic review, International Journal of Human–Computer Interaction, 2026 ([Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/10447318.2026.2618562)) — current text-based GenAI interfaces impose excess cognitive load and lack predictability and scaffolding.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 4.1.3 Status Messages | AA | generation state announced without re-reading the message |
| 2.2.2 Pause, Stop, Hide | A | streaming can be stopped |
| 2.2.1 Timing Adjustable | A | no expiring composer or session mid-task |
| 1.3.1 Info and Relationships | A | rendered output keeps headings, lists and tables as real semantics |
| 2.4.3 Focus Order | A | focus is never stolen by an arriving response |
| 2.5.3 Label in Name | AA | per-message controls named distinctly, containing their visible text |
| 1.1.1 Non-text Content | A | generated images and charts carry alternatives, resolved with a human |

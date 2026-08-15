# Charts & Data Visualization Guide

> **Scope:** Charts, graphs, dashboards and any drawing whose content is data — the component this standard has always required (*Visual Patterns*, §3) and never explained, and the one an agent most reliably resolves with a sentence that carries no data at all.

## 0. The rule everything else follows

**A chart is not a picture of data. It is data, drawn.** So its accessible alternative is **the data**, not a description of the drawing.

```tsx
// ❌ The failure this guide exists to prevent — conformant to every checker, useless
<img src="/revenue.svg" alt="Bar chart showing revenue growth in 2026" />

// ✅ The alternative is the numbers, reachable by everyone
<figure>
  <img src="/revenue.svg" alt="Bar chart: monthly revenue, 2026. Rises from 40k in January to 120k in June." />
  <figcaption>Monthly revenue, 2026</figcaption>
  <details>
    <summary>View data as a table</summary>
    <table>{/* the same series, as rows */}</table>
  </details>
</figure>
```

The `alt` says what the reader would *see*; the table gives what the reader would *learn*. A chart that ships only the first is a chart only sighted users can read, and no automated checker will ever say so — the `alt` attribute is present and descriptive.

**Applies to every shape:** a data table equivalent is **MUST** for informative charts, at every compliance profile. Where a table is impractical (thousands of points, a live stream), a downloadable dataset or an API endpoint stated in the caption is an acceptable equivalent; "the numbers are elsewhere in the product" is not.

## 1. First decide which of the three shapes you are building

The technique changes completely, and getting this wrong is the root of most broken charts:

| Shape | When it is right | What it owes |
| :--- | :--- | :--- |
| **Static image** (PNG/SVG exported) | the chart never changes and nothing in it is clickable | `alt` with the **trend and the extremes**, plus the data table nearby — see [Images](guide-images.md) |
| **Inline SVG** | the chart is rendered from data, not interactive point by point | `role="img"` on the `<svg>` **plus** an `aria-label`/`aria-labelledby`; children `aria-hidden` so the reader does not walk a pile of `<path>` |
| **Interactive** (canvas, hover/click on points, zoom, brush) | the user acts on the data | everything in §3 — keyboard, focus, announcement — plus the table |

```tsx
// Inline SVG, not interactive: one node in the accessibility tree, not two hundred
<svg role="img" aria-labelledby="chart-t chart-d" viewBox="0 0 600 300">
  <title id="chart-t">Monthly revenue, 2026</title>
  <desc id="chart-d">Rises from 40k in January to 120k in June, with a dip to 35k in March.</desc>
  <g aria-hidden="true">{/* paths, axes, gridlines */}</g>
</svg>
```

> **Canvas has no accessibility tree.** A chart drawn in `<canvas>` is, to assistive technology, a blank rectangle. Whatever the library renders, the data table and the keyboard path must exist in the DOM beside it — not inside the canvas.

## 2. Color is never the encoding

Covered in depth in [Visual Perception](guide-visual-perception.md); here is what it means for a chart specifically:

1. **Every series carries a second channel besides hue** — dash pattern, marker shape, texture, or direct labelling at the end of the line. This is the *Visual Patterns* rule of `A11Y.md` §3, and it is the single most common failure in generated dashboards.
2. **Direct labels beat legends.** A legend forces the reader to hold a color↔name mapping in memory and match it across the plot — cognitive cost for everyone, an impossible task for many. Label the series where it is drawn.
3. **Adjacent series need 3:1 against each other** (SC 1.4.11), not only against the background: two blues that pass on white still merge into one line for a person with reduced contrast sensitivity.
4. **State never rides on color alone** — a "critical" bar is not just red; it is red **and** labelled or marked.

## 3. Keyboard: reaching the chart is not reading it

An interactive chart is a widget, and the tab key must not be the only thing that works.

1. **One tab stop for the chart**, then arrow keys to move between points — the pattern of a grid, not a list of two hundred tab stops.
2. **Focus is visible on the focused point** (SC 2.4.7): a ring, a halo, an enlarged marker — never only a tooltip appearing.
3. **The focused point announces its values.** Either the point is a real focusable element with an accessible name (`<g tabindex="0" role="img" aria-label="March: 35,000">`), or a `role="status"` region beside the chart is updated as focus moves.
4. **Everything the mouse can do, the keyboard can do:** if hover opens a tooltip, focus opens the same tooltip (see [Tooltips & Popovers](guide-tooltips-popovers.md)); if drag selects a range, a keyboard alternative selects the same range (see [Drag & Drop](guide-drag-drop.md)).
5. **`Esc` leaves** any zoom or brush mode without leaving the page.

```tsx
// Announcing the point under focus, without rebuilding the whole chart
<div role="status" aria-live="polite" className="sr-only">
  {focused ? `${focused.label}: ${formatValue(focused.value)}` : ""}
</div>
```

## 4. Charts that update

Dashboards change under filters, date ranges and live data. Every change is a status change (SC 4.1.3).

- Announce the **outcome**, not the event: *"Filtered by Q2: 3 series, 12 points"* — never *"chart updated"*.
- **Do not** put `aria-live` on the chart container: a redraw fires hundreds of mutations and the screen reader reads the redraw, not the result. Announce from a small dedicated region.
- A chart streaming live data **MUST** offer a pause (SC 2.2.2) — continuous automatic movement is not exempt for being data.
- Keep the data table in sync with the filters. A table showing the unfiltered set is a second, contradictory answer.

## 5. Dashboards

- Each chart sits in a labelled region — `<section aria-labelledby>` with a real heading, so the whole board is navigable by headings.
- The **heading text names the question the chart answers**, not the chart type: "Revenue by month", never "Bar chart 3".
- Small metadata is where the 10px density exception gets abused — it is an `EXCEPTIONS.md` entry with 7:1 contrast, not a default (`A11Y.md` §4).
- A "chart" that is a single number (a KPI tile) is text: mark it up as text, not as an image of a number.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 1.1.1 Non-text Content | A | the chart has a text alternative — and for data, the equivalent is the data |
| 1.4.1 Use of Color | A | hue is never the only channel distinguishing series or states |
| 1.4.11 Non-text Contrast | AA | series, markers and axes at 3:1, including against each other |
| 2.1.1 Keyboard | A | points, tooltips, zoom and selection all reachable without a mouse |
| 2.4.7 Focus Visible | AA | the focused data point is visibly focused |
| 2.2.2 Pause, Stop, Hide | A | live-updating charts can be paused |
| 4.1.3 Status Messages | AA | filter and range changes announce their result |

## Tip for the AI:

Before finishing a chart, answer one question: **"Can someone who cannot see this get the same numbers, in the same place, without asking anyone?"** If the answer depends on an `alt` sentence, the chart is not done — generate the data table with it, in the same turn, as part of the component. And when the chart is decorative (a sparkline behind a KPI already stated in text), say so and mark it `aria-hidden="true"` — but that is a human-confirmed classification, exactly as in *Image Evidence* (`A11Y.md` §2).

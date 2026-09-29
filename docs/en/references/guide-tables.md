# Tables Accessibility Guide

> **Scope:** Data Grids & Tables

## Core Rules
1. Use `<caption>` to describe the table.
2. Use `<th>` with `scope="col"` or `scope="row"`.
3. Avoid using `<div>` for tabular data. Where unavoidable, the ARIA structure MUST be complete: `role="table"` on the container, `role="row"` on **every row**, and `role="columnheader"` / `role="rowheader"` / `role="cell"` on the cells. Without `role="row"` the table exposes no structure at all — it degrades into a loose collection of cells, and the screen reader's row/column navigation stops existing.

## Example
```html
<table>
  <caption>Employee Data</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>Engineer</td>
    </tr>
  </tbody>
</table>
```

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a page with a data table, WHEN I press `Tab` through it, THEN no cell takes focus — only real controls inside the table (links, buttons) do, in reading order.
- WHEN the table is built from `<div>`s with ARIA roles, THEN `Tab` behaves exactly as in a native table: no extra stops, none missing.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I reach the table, THEN I hear "table", its caption, and its size in rows and columns.
- WHEN I move between cells with the table commands (`Ctrl+Alt` + `←`/`→`/`↑`/`↓`), THEN on each cell I hear the column header — and the row header, when there is one — before the value.
- WHEN the table is built from `<div>`s, THEN I still hear "table" and still move by row and column — table commands that do nothing are a failure.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe onto the table, THEN I hear "table", its caption and how many rows and columns it has.
- WHEN I swipe through the cells, THEN each value comes after its column header — and its row header, when there is one.

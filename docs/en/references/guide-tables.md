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
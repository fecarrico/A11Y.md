# Tables Accessibility Guide

> **Scope:** Data Grids & Tables

## Core Rules
1. Use `<caption>` to describe the table.
2. Use `<th>` with `scope="col"` or `scope="row"`.
3. Avoid using `<div>` for tabular data unless using `role="table"` and `role="cell"`.

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
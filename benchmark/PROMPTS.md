# Benchmark Prompts (fixed verbatim — pre-registered)

> Used exactly as written, in every model and condition. Condition B prepends the full `docs/en/A11Y.md` followed by the line: *"Follow strictly the accessibility rules defined in the A11Y.md above."* — nothing else changes. The prompts deliberately never mention accessibility.

## Task 1 — Signup form

```
Create a signup page in plain HTML, CSS and JavaScript with fields for full name, email and password. Validate the fields inline and show error messages when submission fails. Show a success message when it succeeds.
```

## Task 2 — Destructive-confirmation modal

```
Create a page in plain HTML, CSS and JavaScript showing a list of 5 saved documents. Each document has a Delete button. Clicking Delete opens a confirmation dialog asking "Delete this document?" with Cancel and Delete options. Deleting removes the item from the list.
```

## Task 3 — Sortable data table

```
Create a page in plain HTML, CSS and JavaScript with a table of 10 employees (name, role, salary). The columns can be sorted by clicking their headers, and each row has a "View details" button that shows that employee's information.
```

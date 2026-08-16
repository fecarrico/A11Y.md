# Benchmark Prompts (fixed verbatim — pre-registered)

> Used exactly as written, in every model and condition. What precedes each prompt is defined per condition in [`METHODOLOGY.md`](METHODOLOGY.md) §Conditions — nothing else changes between conditions. The prompts deliberately never mention accessibility — that is the point. Tasks 1–3 are unchanged from v1.0; tasks 4–10 were added in v2.0, before any data collection.

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

## Task 4 — Site navigation

```
Create a page in plain HTML, CSS and JavaScript with a site header for an online bookstore. The header has a logo, a five-item navigation bar where "Categories" and "Account" open dropdown submenus on activation, and a compact menu behavior for narrow screens.
```

## Task 5 — File upload

```
Create a page in plain HTML, CSS and JavaScript where the user uploads up to 3 PDF files. Show each file in a list with its name, a progress indicator while it uploads (simulate the upload with a timer), a way to remove it, and a clear failure state when a file exceeds 5 MB.
```

## Task 6 — Image carousel

```
Create a page in plain HTML, CSS and JavaScript with a product gallery carousel of 5 images with captions. The carousel advances automatically every 4 seconds, has previous/next controls and position indicators, and clicking an indicator jumps to that image.
```

## Task 7 — Search with suggestions

```
Create a page in plain HTML, CSS and JavaScript with a search box for a city directory. As the user types, show up to 7 matching city suggestions from a hardcoded list of 50; choosing a suggestion fills the box and shows that city's detail card below.
```

## Task 8 — Product card grid

```
Create a page in plain HTML, CSS and JavaScript with a grid of 6 product cards for a coffee shop. Each card has a product photo, name, price, a short description and an "Add to cart" button; adding updates a cart counter in the page header.
```

## Task 9 — Async save with toasts

```
Create a page in plain HTML, CSS and JavaScript with a short profile form (display name, bio) and a Save button. Saving simulates a request with a timer and randomly succeeds or fails; show the outcome as a toast notification that appears in a corner and disappears after a few seconds.
```

## Task 10 — Dashboard chart

```
Create a page in plain HTML, CSS and JavaScript showing monthly revenue for one year as a bar chart drawn with SVG or canvas, plus a toggle that switches between the chart and a table of the same twelve values. Highlight the best and worst month.
```

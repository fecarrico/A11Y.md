# Study 2 — the frozen journey prompt

> One prompt, one session, all conditions. Frozen verbatim before the pilot;
> after registration it changes for no reason whatsoever. It never mentions
> accessibility, consistency or reuse — the last two are the phenomena under
> measurement. Condition preambles (PROTOCOL.md §Conditions) are prepended
> without altering this text.

---

## `bookstore-journey`

Build a small online bookstore called "Loop Books" as a static site: plain
HTML, CSS and JavaScript, no build step, no external libraries or fonts. One
HTML file per screen. Use realistic hardcoded data (at least 8 books). All
interactive behavior implemented in JavaScript and working locally by opening
the files in a browser. The screens:

1. `index.html` — Home: header with the site name, main navigation with a
   dropdown of book categories, and a grid of featured book cards (cover
   image, title, author, price, "Add to cart" button).
2. `search.html` — Search: a search box that suggests matching titles while
   the user types (from the hardcoded catalog), with results shown as book
   cards.
3. `book.html` — Book detail: a carousel of cover and preview images, the
   description and price, an "Add to cart" button that shows a brief
   confirmation message, and a short reviews section.
4. `cart.html` — Cart and checkout: the items with quantity controls, a
   "Remove" action that asks the user to confirm before removing, and a
   checkout form (name, email, address, payment fields) with client-side
   validation and a submission state.
5. `orders.html` — My orders: a table of past orders sortable by date, total
   and status, and a "Cancel order" action that asks the user to confirm.
6. `sell.html` — Sell a book: a form to list a used book (title, author,
   condition, price) with a cover-image upload control showing progress and
   success or failure, and a brief confirmation message on save.
7. `dashboard.html` — Seller dashboard: a bar chart of monthly sales built
   with plain HTML, CSS and JavaScript (no chart libraries), with the
   underlying numbers also available on the page.

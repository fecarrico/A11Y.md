# Accessibility Guide: Navigation & Document Structure

> Scope: Landmarks, skip links, link purpose and consistency, new-tab and file links, breadcrumbs, heading hierarchy, list semantics, and SPA routing focus management.

## 1. Landmarks & Skip Link

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<nav aria-label="Main Navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
<main id="main-content">…</main>
```

- `<nav>`, `<main>`, `<header>`, `<footer>` and `<aside>` are landmarks — screen reader users jump between them by shortcut. When the same landmark appears more than once (two `<nav>`s), each **MUST** carry a distinguishing `aria-label`.
- The skip link is the **first** focusable element and **MUST** be visible on focus — it lets keyboard users bypass repeated navigation (SC 2.4.1).
- `aria-current="page"` marks the current location in the menu.

## 2. Link Purpose (SC 2.4.4)

The purpose of every link **MUST** be determinable from its text alone or its text plus programmatic context. Screen reader users navigate by listing links out of context.

```html
<!-- ❌ purpose lives outside the link -->
<a href="/report.pdf">Click here</a> to download the annual report.

<!-- ✅ the link text is the purpose -->
<a href="/report.pdf">Download the annual report (PDF, 2 MB)</a>
```

- **MUST NOT** use bare "click here", "read more", "learn more" — repeated identical texts pointing at different places fail the listing test. Where a card repeats "Read more", complement it programmatically (`aria-labelledby="card-title read-more-id"`).
- **New tab or window:** a link that opens away from the current context **MUST** say so in its accessible name ("opens in a new tab") — losing the Back button without warning disorients screen magnifier and cognitive-load users alike.
- **Non-HTML target:** a link to a file **MUST** declare format and, ideally, size in the link text ("(PDF, 2 MB)") — the person decides *before* the download whether their tools open it (NBR 17225 5.7.7; the file itself must be accessible — see [Governance §6.1](guide-governance.md)).

## 3. Consistent Navigation (SC 3.2.3)

Navigation mechanisms repeated across pages **MUST** keep the same relative order on every page. Components with the same function **MUST** be identified consistently (SC 3.2.4): the search field is not "Search" here and "Find" there.

- In code: navigation lives in the shared layout, never rebuilt per page — the same rule *Consistent Help* (core §3) applies to help mechanisms.
- **Breadcrumbs** (SC 2.4.8 AAA — recommended for any hierarchy deeper than two levels): an ordered list inside `<nav aria-label="Breadcrumb">`, current page marked with `aria-current="page"`.

## 4. Heading Hierarchy & Lists

Headings and lists are the document's skeleton — the first thing a screen reader user requests is the heading list.

- **One `<h1>` per page**, describing the page (it pairs with `<title>` — core §3, *Page Title*).
- Levels **MUST NOT** skip (h2 → h4 is a hole in the outline); heading text **MUST** describe the section it opens (SC 2.4.6).
- **MUST NOT** pick a heading tag for its font size — style with CSS; the level is structure, not cosmetics. The inverse also fails: a bolded `<p>` acting as a section title is invisible in the heading list (SC 1.3.1).
- Sequences of related items — menus included — **MUST** be real lists (`<ul>`/`<ol>`): the screen reader announces "list, 5 items", which a pile of `<div>`s never says.

## 5. SPA Routing

After a client-side route change, focus **MUST** be managed — sent to the new content's `<h1>` or the top of the page — and the `<title>` **MUST** be updated (core §3, *SPA Routing* and *Page Title*). A route change a screen reader never hears is a page that never changed.

## Bad Examples

### 1. Nested Menus (Hover only)
- Menus that appear only on hover are unreachable by keyboard and touch. Toggle on click/focus, close on `Esc`.

### 2. Non-standard Links
```html
<span onclick="window.location='/new-page'">Go to Page</span>
```
- See *Clickable Divs* — core §6: no focus, no link role, no new-tab, no copy-address.

*Success criteria covered: 2.4.1 Bypass Blocks (A) · 2.4.4 Link Purpose — In Context (A) · 2.4.6 Headings and Labels (AA) · 2.4.8 Location (AAA) · 1.3.1 Info and Relationships (A) · 3.2.3 Consistent Navigation (AA) · 3.2.4 Consistent Identification (AA)*

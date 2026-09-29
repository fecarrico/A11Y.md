# Tree View & Hierarchy Guide

> **Scope:** Tree views, file explorers, nested category pickers and any expandable hierarchy — adopt rather than reinvent (`A11Y.md` §6).

## 0. First ask whether it should be a tree at all

Most generated "trees" are navigation menus wearing `role="tree"`, and the role makes them *worse*: it tells assistive technology this is a selection widget with arrow-key navigation, so the user's normal reading commands stop behaving normally and links stop being announced as links.

| What it really is | Correct markup |
| :--- | :--- |
| site or docs navigation with links | `<nav>` + nested `<ul>` + `<a>` — expandable sections use `aria-expanded` on a `<button>` |
| sections of content that open and close | disclosure / accordion — see [Tabs & Accordions](guide-tabs-accordion.md) |
| a filter with nested checkboxes | nested `<fieldset>` + checkboxes, not a tree |
| **selecting or exploring items in a hierarchy** (file explorer, org chart picker, layer panel) | **`role="tree"`** — this guide |

If the user is *going somewhere*, it is navigation. If the user is *choosing something* from a hierarchy, it is a tree.

## 1. The pattern

Follow the [APG Tree View pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/). The structural contract:

```tsx
<ul role="tree" aria-label="Project files">
  <li role="treeitem" aria-expanded={open} aria-selected={selected} tabIndex={focused ? 0 : -1}>
    <span>src</span>
    <ul role="group">
      <li role="treeitem" aria-selected={false} tabIndex={-1}>index.tsx</li>
    </ul>
  </li>
</ul>
```

1. **`aria-expanded` only on nodes that have children.** On a leaf it is a lie: the reader announces "collapsed" for something that will never open.
2. **Children live in a `role="group"`**, nested inside the parent `treeitem` — not as a sibling.
3. **When the DOM is not the full tree** (virtualized lists, lazily loaded branches), every visible node **MUST** carry `aria-level`, `aria-setsize` and `aria-posinset`. Without them the reader announces "1 of 3" for a node that is the ninth of forty, and depth disappears entirely.
4. **One tab stop for the whole tree.** The focused node holds `tabindex="0"`, every other node `-1` — roving focus. A tree with forty tab stops is the failure this pattern exists to prevent.

## 2. Keyboard

| Key | Behavior |
| :--- | :--- |
| ↑ / ↓ | previous / next **visible** node (skipping collapsed subtrees) |
| → | expand a closed node; move to its first child if already open |
| ← | collapse an open node; move to the parent if already closed |
| `Home` / `End` | first / last visible node |
| `Enter` | activate (open the file, apply the choice) |
| `Space` | select, where selection is separate from activation |
| a–z | type-ahead to the next node starting with that character |
| `*` | expand every sibling at the current level |

**Expanding is not selecting.** A node can be open and unselected, or selected and closed; `aria-expanded` and `aria-selected` are independent, and a tree that conflates them cannot express "I opened this folder to look inside without choosing it".

## 3. Multi-select and async loading

- Multi-select trees declare `aria-multiselectable="true"` on the `tree`, and **every** selectable node carries `aria-selected` — `true` *or* `false`. Setting it only on the selected node makes the rest unselectable to the API.
- A branch loading its children announces the wait (`aria-busy="true"` on the node, and a polite status region for the result: *"src expanded, 12 items"*). Silent async expansion is the most common reason a screen-reader user thinks the tree is broken.
- Indentation is visual only. Depth reaches assistive technology through nesting or `aria-level` — never through padding.

## Expected behavior (verification scenarios)

*What a person verifying this component must observe — with a keyboard, then with a screen reader on desktop and on a phone. These are the scenarios behind `REPORT.md` §3: run them, record the screen reader + browser pair, mark each one passed or failed. They describe outcomes, never implementation.*

**Keyboard**
- GIVEN a tree, WHEN I press `Tab`, THEN focus lands on one node and the next `Tab` leaves the tree — a single stop.
- WHEN I press `↓`/`↑`, THEN focus moves through visible nodes only, skipping collapsed subtrees; `Home`/`End` reach the ends.
- WHEN I press `→` on a closed folder, THEN it expands with focus still on it; `→` again enters its first child; `←` collapses or goes to the parent.
- WHEN I expand a folder, THEN it is not selected by that; `Space` selects, `Enter` activates.

**Screen reader, desktop (NVDA + Firefox, JAWS + Chrome or VoiceOver + Safari)**
- WHEN I reach the tree, THEN I hear "tree" and its name, then each node with level and position — "src, expanded, level 1, 2 of 5".
- WHEN I reach a folder, THEN I hear "expanded" or "collapsed"; on a file I hear neither.
- WHEN I expand a branch that loads its children, THEN I hear the wait, then "src expanded, 12 items".
- WHEN the tree allows multiple selection, THEN every node reads "selected" or "not selected", never silence.

**Screen reader, mobile (TalkBack or VoiceOver, swipe navigation)**
- WHEN I swipe through the tree, THEN each node reads with its level and position, and files read without "collapsed".
- WHEN I double-tap a folder and it opens, THEN I hear "expanded" and its children come next in swipe order.

*Success criteria covered: 1.3.1 Info and Relationships (A) · 2.1.1 Keyboard (A) · 2.4.3 Focus Order (A) · 4.1.2 Name, Role, Value (A) · 4.1.3 Status Messages (AA)*

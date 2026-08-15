# Tree View & Hierarchy Guide

> **Scope:** Tree views, file explorers, nested category pickers and any expandable hierarchy — named in `A11Y.md` §6 among the components to adopt rather than reinvent.

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

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 1.3.1 Info and Relationships | A | hierarchy exposed by nesting or `aria-level`, not indentation |
| 2.1.1 Keyboard | A | full arrow-key operation, expand and collapse included |
| 2.4.3 Focus Order | A | roving focus: one tab stop, predictable position |
| 4.1.2 Name, Role, Value | A | `treeitem` with expanded and selected states kept current |
| 4.1.3 Status Messages | AA | asynchronous expansion announces its result |

## Tip for the AI:

Ask the question in §0 out loud before writing any ARIA. If the answer is "the user is navigating", delete the tree roles and ship a nested list of links — that is a smaller component, a faster page and a correct one. If it really is a tree, take the pattern from a library ([APG](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/), Headless UI or equivalent) instead of assembling roving focus by hand, and record the choice in `A11Y-DECISIONS.md` so the next hierarchy in the project does not get a second, different implementation.

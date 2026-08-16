# Tables & Large Lists Guide

> **Scope:** Data grids, sorting, virtualization thresholds

## Core Rules
1. **Sort the data, not the DOM:** Sorting reorders the in-memory array and patches rows; it MUST NOT rebuild the table.
2. **Virtualize past ~500 rows:** Render only the viewport plus overscan; recycle row nodes. Below that, plain rendering is simpler and fast enough.
3. **Fixed row geometry:** Uniform row heights make virtualization O(1); measure-on-render schemes are a last resort.
4. **Paginate at the API** when the set is unbounded — the client never holds what the user cannot reach.
5. **Defer cell extras:** Sparklines, avatars and badges inside rows lazy-load on visibility, not with the table shell.

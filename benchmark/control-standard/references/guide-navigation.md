# Navigation & Prefetching Guide

> **Scope:** Headers, menus, route transitions, prefetch policy

## Core Rules
1. **The header is critical path:** it renders in the initial HTML, styled by critical CSS, with no script required for its first paint.
2. **Dropdowns construct on first open,** not at load — a mega-menu nobody opens is cost nobody sees. Cache the built panel for reopens.
3. **Prefetch on intent:** hover or `IntersectionObserver` on the link arms a prefetch of the next route's code and data; never prefetch the whole nav graph.
4. **Respect the connection:** skip prefetching under `saveData` or `2g`/`slow-2g` effective types.
5. **Transitions stay compositor-side:** the menu slide is a `transform`, the backdrop a `opacity` fade; layout-shifting menus are a defect.
6. **Sticky headers use `position: sticky`,** not scroll listeners repositioning with JavaScript.

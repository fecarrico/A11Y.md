# The consistency classifier — specification

> **v1.0 — FROZEN 2026-08-18, post-pilot.** Executable: [`classifier.py`](classifier.py)
> SHA-256 `485d40647dff688f5b68cc6882d5fde6be51ab4bb7d40fecc7c673e5fc0a5135`.
> Any change after registration is a dated `DEVIATIONS.md` entry.

## Principles

Deterministic, DOM-only, condition-blind: the same parsing rules for every
screen of every run, no language model anywhere in the metric, no human
judgment in the primary outcome. Written before any retained run — a
consistency metric invented after seeing the data would be this study's way of
losing what Study 1's pre-registration bought.

## Unit

A **family instance**: one occurrence of a counted component family on one
screen. The classifier finds instances by detection anchors (below), computes
a **structural signature** for each, and counts **distinct signatures per
family across screens**. Two screens implementing the same family with the
same signature = one variant. The metric never says which variant is better —
dispersion itself is the finding.

## Signature dimensions (draft)

Each instance's signature is the tuple:

1. **Container semantics** — the element/role that carries the pattern
   (`<dialog>` vs `div[role="dialog"]` vs bare `div`; `<nav>` vs `div`;
   `<table>` vs CSS-grid of `div`s).
2. **Interaction machinery** — native control vs scripted element
   (`<button>` vs clickable `div`; `<select>` vs custom listbox).
3. **Naming mechanism** — how the control receives its name (associated
   label element / `aria-label` / placeholder only / visible text only /
   none). Recorded as a category, not judged.
4. **State mechanism** — how state changes are conveyed (attribute-based vs
   class-only vs text swap).

## Families and detection anchors (draft, pilot-calibrated)

| Family | Counted in primary | Detection anchor (draft) |
|---|---|---|
| Navigation | yes | header-level link group with dropdown behavior |
| Book card | yes | repeated catalog item (image+title+price+action) |
| Form | yes | field groups with submission (`cart`, `sell`) |
| Confirmation dialog | yes | element revealed by a destructive action, offering confirm/cancel |
| Transient status message | yes | element revealed on success/failure, auto-dismissing or dismissible |
| Data table | yes* | sortable records structure (`orders`; dashboard numbers if tabular) |
| Carousel / upload / autocomplete / chart | no — single-instance | reported descriptively |

\* counted only if instantiated on ≥2 screens in the run under measurement —
the rule is per run, mechanical, and the same for every condition.

## Metric

Per family: `variants = |{distinct signatures across screens}|`.
Aggregate per run: **variant excess** `Σ (variants − 1)` over counted
families. Zero = every family implemented one way everywhere.

## What the pilot settled (2026-08-18)

- **Static-DOM scope, declared:** instances rendered purely by JavaScript leave
  no static footprint and are out of scope — symmetrically for every condition.
  The pilot's bare journey shipped an empty `<header>` filled at runtime; its
  navigation is invisible to this instrument, and the limitation is part of the
  measure's definition, not a bug to patch per run.
- **Native `confirm()` scan:** `window.confirm` leaves no DOM footprint either;
  the classifier statically scans inline and same-run linked scripts for it.
  **Dominance rule:** a run with DOM dialog instances keeps confirm references
  as metadata (fallback branches must not count as a second variant); a run
  with none receives them as its dialog instances.
- **Anchors widened:** nav falls back to the outermost cluster of ≥3 internal
  links; card children include `<a>` wrappers.
- **Deliverable rule confirmed:** non-empty screen `*.html` files (7/7/7 in the
  pilot's three journeys).
- **The instrument is not a rubber stamp:** in the single pilot journey the
  standard's condition scored *worst* on variant excess (4, vs 2 generic and
  3 bare). One journey means nothing statistically and the data is discarded —
  but the metric demonstrably can rule against the standard.

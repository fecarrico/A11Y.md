# The consistency classifier — specification

> **v0.1, pre-pilot. Not frozen.** This file freezes when it records the
> SHA-256 of the classifier executable, after pilot calibration and before
> registration. Until that hash exists, nothing may be collected.

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

## What the pilot must settle

Detection anchors robust to naming (no reliance on class names or ids);
signature granularity (dimensions 3–4 may merge if the pilot shows them too
noisy); the deliverable-count rule for the amortized-cost denominator; the
wall clock. Every calibration decision lands in PROTOCOL.md §Pilot, dated.

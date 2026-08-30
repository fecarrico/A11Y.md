# Consistency classifier v2 — specification

> Status: **draft, adversarially verified twice — frozen when the hash is
> recorded here at protocol freeze.** Code: `classifier_v2.py`
> (stdlib-only, deterministic, condition-blind). v1
> (`../study2/classifier.py`, sha256 `485d4064…`) stays untouched and
> re-runnable as a sensitivity analysis.

## Why a v2

Round 2's protocol requires every ruler to exist as frozen executable code
before registration. The instrument went through two hardening stages, both
before any Round-2 data exists:

1. **Calibration** — four independent agents each audited one suspected v1
   defect against Round 1's 30 published journeys. All four confirmed
   (cases A–D below); every fix was validated against the real corpus
   before the first draft of this spec.
2. **Adversarial verification, round 1** — an independent panel (three
   lenses: gaming with constructed inputs, condition bias,
   correctness/regressions) attacked the v2 draft; each finding was then
   re-verified by a skeptic agent instructed to refute it. **16 findings
   survived verification** and are fixed or documented below; **27 attacks
   failed** (the panel's clean-areas list includes: mechanical
   condition-blindness on real runs under swapped names, no proxy leaks,
   anti-circularity of the table claim term, determinism across hash seeds
   and `-O`, richness arithmetic, exclusion accounting, and independent
   reproduction of the sensitivity table).
3. **Adversarial verification, round 2** — a second panel attacked the
   AMENDED instrument (the 16 fixes themselves) and hunted regressions the
   fixes could have introduced. **13 findings survived skeptic
   verification** (ledger below), **26 attacks failed**. Two had measured
   real-corpus impact: a JS regex literal containing a quote corrupted the
   literal-blanking pass and misread 4/30 runs (claude-code B run3's
   excess read 0 instead of 1 — understating a NON-treatment cell), and a
   nested live-region wrapper idiom in one antigravity D run was charged
   +1 for one physical widget. Both directions, both fixed.

### The four calibration cases (v1 defects)

| # | Defect (v1) | Fix (v2) |
|---|---|---|
| A | `aria-sort` treated as a *variant*: a static table diverged from a sortable one that correctly declares `aria-sort` — punishing the better run. All 10 D journeys carried +1 excess for honest markup. | **Capability gate.** Structure `(container, heads)` is compared across all tables; sort *signalling* is compared only among sortable tables. Claiming `aria-sort` can only ADD a table to the pool (anti-circularity). |
| B | Cards required a literal `<img>` in the static DOM. 25/30 real runs render the catalog client-side; 2 more use CSS-styled `div` covers. v1 saw cards in 3/30 runs. | **Two lanes.** DOM lane accepts `css-cover`; JS lane statically parses local script factories with receiver binding. Validated: 30/30 real runs detected. |
| C | Structurally broken instances counted as *variants*: one run's menu ladder (`ul[role=menu] > li` without role) read as a second nav convention. | **Validity gate.** Required-parent/children composition checked per instance; invalid instances are excluded and *counted as exclusions*. Validated: exactly the 7 main-nav instances of one run excluded, zero elsewhere in 45 runs. |
| D | `variant_excess = 0` was unreadable: zero-because-uniform and zero-because-poor looked identical. | **Richness block**, sibling of the excess, never fused. Protocol rule: **excess is only quotable together with `families_counted`.** |

### The adversarial panel's amendments (v2-draft defects, all pre-freeze)

Confirmed and **fixed**:

| Lens | Finding | Fix |
|---|---|---|
| gaming | Validity gate blessed broken composites built from `div`+`a`/`button` (only `li`-style ladders errored) | `IMPLICIT` extended: interactive/semantic elements carry their real implicit roles (`a[href]`→link, `button`→button, `select`→listbox, `summary`→button, `input`→textbox/radio/checkbox, `table`, `nav`, `img` (with `alt=""`→presentation), headings, `hr`→separator). Only genuinely role-less tags stay generic/transparent. A composite with element content but zero owned items anywhere is invalid ("announced composite with zero items"). |
| gaming | Richness gameable with contentless stubs (`<table></table>`, empty `<dialog>`, 6/6 families from shells) | **Substance predicates** per family; stubs go to `stub_instances` / `stub_detail`, outside variants, `families_counted` and coverage. Headers count as substance (a thead-only table populated client-side is legitimate static credit — the Round-1 antigravity D orders tables); empty live-region placeholders remain the correct idiom and are never stubbed. |
| gaming | Sortable table with the click affordance on a descendant `span[onclick]` called static | Handler/focus affordance scanned in the whole header-cell subtree. |
| gaming | ARIA grids (`role=grid` + `role=columnheader`) could never be capable; their `aria-sort` claim was inert | `col_header_cells` includes `role=columnheader`; gate and anti-circularity now identical for native and ARIA tables. |
| gaming | Run-level DOM dominance buried genuinely divergent JS conventions on other screens | Card dominance is **per screen** (a screen's DOM grid demotes only that screen's JS hits). Dialog dominance stays run-level, mirroring frozen v1's pilot-calibrated `window.confirm` rule — difference documented. |
| gaming | Two card conventions sharing one grid read as one (first-member signature + early return) | DOM lane groups by (tag, class token) **and then by full shape**; every qualifying shape in every group emits an instance. |
| bias | Toast family charged the prescribed `status`/`alert` severity pair as dispersion (+1 floor on D-compliance) | Toasts **partitioned by announcement channel** (polite ≈ `role=status`/`aria-live=polite`, assertive ≈ `role=alert`/`aria-live=assertive`); dispersion measured within each channel (`role=status` vs `aria-live=polite` is still two conventions). |
| bias | Nav family conflated landmark subtypes: a semantic footer `<nav>` cost +1 while a div-built footer was invisible | Navs **partitioned by slot**: the primary nav (most links, DOM order breaks ties) compared across screens; secondary navs pooled by normalized accessible name. The dropdown axis is now the *set* of mechanisms present. |
| bias | JS-lane signatures embedded authoring artifacts (`js-template` vs `js-builder`, `interpolated-cover`) — identical rendered cards charged +1 | Signatures normalized to **rendered shape**: container axis from the receiving host element (same vocabulary as the DOM lane), interpolated image markup ≈ `img`, authoring style demoted to `style` metadata; indeterminate fragment-forest shapes stay instances but leave variant identity. |
| regression | `bindings` regex matched *inside* template literals on minified JS (card family silently zeroed) | Offset-preserving `blank_code`: template literals + comments blanked for binding scans (plain-string ids kept); everything blanked for brace matching and iteration checks. Documented limit: JS regex literals are not recognized. |
| regression | An unbound second factory scored (+1 spurious excess; the 2-signatures pattern occurs in 7/30 real runs) | Receiver resolution is **per factory** — only signatures whose own factory reaches a bound receiver are emitted. |
| regression | `<template>` sample cards counted as live DOM (and then demoted the real JS grid) | `cards_dom` skips `template` subtrees. Inherited v1 detectors intentionally keep v1's judgments verbatim; template contents there remain a documented sensitivity note. |
| regression | Every tag missing from `IMPLICIT` resolved to generic (`ul[role=menu] > a` passed while `> li` was excluded) | Same fix as the first gaming finding (one root cause, two lenses). |
| regression | Arrow-function factories (`const X = (b) => …`) got no name; render sites after the unit were invisible | `_name_before` covers arrow assignments; `.map(name)`/`.join` render forms count as render sites. |
| regression | Braces inside strings/comments truncated function units (factory vanished) | Brace matching runs on fully blanked text; unit bodies are recovered from the original offsets. |
| bias | Cross-vocabulary confound: variant excess is only measurable inside the semantic vocabulary the standard prescribes, deflating A/B cells in **secondary** contrasts | Cannot be fixed in a static detector; fixed as an **analysis rule**: ruler 4 informs the *primary* contrast (D20 vs D18 — same vocabulary on both sides); in secondary contrasts (vs A/B) it is descriptive only, quoted per family, conditioned on the family being counted in both cells, denominator alongside, raw cross-condition sums barred from headlines. `analyze.py` enforces this (excess enters the contrast table only for D20 vs D18); `per_family_excess` is a top-level output so the per-family reading is the quotable one. The sensitivity table below carries the same warning. |

### The second panel round's amendments (attacks on the fixes)

All 13 confirmed findings fixed:

| Lens | Finding | Fix |
|---|---|---|
| regression (**blocker**) | JS regex literals (`.replace(/"/g,…)` in a real run) opened a phantom string in the blanking pass — 4/30 runs misread, one B cell understated | The shared JS lexer recognizes regex literals (standard heuristic: a `/` whose previous token cannot end an expression; escapes and character classes handled; `}` stays ambiguous, documented). Verified by hand against the real file before fixing. |
| gaming | A live-region wrapper around a live-region toast (belt-and-suspenders idiom in a real D run) was two "conventions" — the run's entire excess | `toasts()` collapses ancestor-descendant matches: the innermost element is the widget. Sensitivity re-baselined (antigravity D 10→9). |
| gaming ×2 | Nested template literals — the top-frequency LLM catalog idiom (`grid.innerHTML = \`…${books.map(b => \`…\`)}…\``) — scored 0 cards | One real JS lexer replaces the regex tokenizer: template text, `${…}` interpolation code (recursive), strings, comments and regexes are tracked; literal collection includes nested template text AND interpolation markers, so both the nested-map idiom and the `${coverMarkup}` idiom survive. Top-level render code with no enclosing function scans as one pseudo-unit. |
| gaming | Receiver forms: chained `getElementById('x').innerHTML = …` (no variable), `querySelector('.class')`, and hosts holding a skeleton/`noscript` placeholder all zeroed the family | All three added: chained no-variable receivers, `('class', name)` host keys, and a placeholder-tolerant near-empty test. |
| gaming | A decorative `aria-hidden` SVG badge inside one card split a uniform grid into two conventions | `imageish` ranks real covers above svg and ignores `aria-hidden` svg entirely. |
| gaming | A select-all checkbox (or filter input) with a handler inside a `th` opened the sort-capability gate | Form controls (checkbox/radio/textbox/listbox roles) are skipped by the handler/focus term — selection/filter affordances are not sort affordances. |
| gaming + bias | Nav slots: a footer nav was promoted to "primary" on footer-only screens, and a breadcrumb was promoted when the main nav is client-rendered — false +1 on uniform runs, agent-correlated | Slot identity comes from the nav's own accessible name: named navs pool as `label:<name>` and are NEVER promoted; the link-richest unnamed nav is `unnamed-main`; remaining unnamed navs share `unnamed-other`. Sensitivity re-baselined (claude-code A 12→11). |
| gaming (→minor) | Button-only forms — including a real D run's canonical `<form method="dialog">` confirm forms — were stubbed as contentless | A form with ≥1 field OR ≥1 button/submit control is substantive; only the empty shell stubs. |
| bias | A counted card family whose every instance is shape-indeterminate reported a measured 0 excess and stayed in the denominator | `unmeasurable` flag: `per_family_excess = null`, excluded from the excess sum AND from `families_counted`; `families_unmeasurable` reported beside it. Fires on 5 real antigravity runs (fragment-forest factories) — cells now declared unmeasured instead of falsely zero. |
| regression | A dead same-name factory in a second script borrowed the live factory's render sites (+1 spurious) | Name-based render-site resolution trusts a foreign script only when it does not define its own factory of that name. |
| regression | Arrow-assigned factories and `.map(factory)` bare-callback render sites were invisible | `_name_before` covers arrow assignments; all render-site patterns accept bare-callback and `ns.name` forms plus spread-append. |
| regression | Brace-matching and binding scans still confusable by literals in one path | All structural scans run over the lexer's blanked text; unit bodies recover from original offsets. |

Confirmed as design, documented (no code change): invalidating a divergent
instance lowers excess (intended: the error migrates to the violation
rulers, and exclusions are reported per condition — a run cannot silently
profit); breaking-markup-to-hide-dispersion is therefore visible in
`excluded`, which the protocol reports beside every excess.

Minor notes adopted across both rounds: bare/valueless `aria-sort` counts
(presence, not truthiness); `scope` and `aria-live` values compare
case-insensitively; a bare `th` in the table's first row (no thead, no
scope) heads its column, so the gate does not depend on the thead idiom;
missing fixture directories fail the self-test instead of skipping;
nonexistent run paths report `status: missing` (an empty directory is
`no-data`); the census regex gains Portuguese lexemes; the tautological
denominator self-check was replaced by a falsifiable one (a one-screen
family is not counted). Parser amendments (measured judgment-neutral on
the whole Round-1 corpus, adopted for browser faithfulness): duplicate
attributes keep the FIRST value; HTML5 optional end tags auto-close
(`li`, `p`, `dt/dd`, `tr`, `td/th`, `option`), walking up through
non-structural open elements and stopping at structural containers.

## Principles

1. **Condition-blind.** Input is a directory of `*.html` (plus local `js/`
   files those screens reference). No run name, no condition label, no
   network. Proven mechanically in the self-test (identical bytes under
   A-named and D-named directories) — that probe is mandatory, not
   skippable.
2. **Deterministic.** Same input → same output; verified across re-runs,
   hash seeds and `-O`.
3. **Capability before state.** A run is never compared on a state signal
   it has no occasion to emit.
4. **Like with like.** Partitioned comparison — nav slots, toast channels,
   table dimensions — so purpose splits (main vs footer nav, success vs
   error announcement) are never read as dispersion.
5. **Validity before variants.** A broken instance is evidence of a
   *defect*, not a *convention*; excluded and counted.
6. **Richness beside excess**, stubs apart. "Excess 0 over 3 families" and
   "excess 0 over 6 families" are different claims.
7. **Rendered shape, not authoring style.** How a card factory is written
   is metadata; what it renders is identity.
8. **No silent lanes.** Every instance carries `source`; demotions stay
   visible (`cards_js_refs`, `script_confirm_refs`); stubs stay visible
   (`stub_detail`).
9. **Static-analysis honesty.** What static analysis cannot see is
   documented below, never patched with speculative heuristics.

## Family detectors

`dialog` and `form` keep v1's judgments verbatim. `nav` and `toast` keep
v1's signature vocabulary but partition the comparison pool. `table` and
`card` are re-specified. Every DOM instance passes the validity gate and
the substance predicate before entering variants.

### Tables (case A)

- **Structure dimension** — signature `(container, heads)` over all valid
  tables.
- **Capability** (`table_sortable`) — a table is sortable iff any *column
  header cell* (a `th` with a `thead` ancestor or `scope=col`
  case-insensitive, or any element with `role=columnheader`) has: (a) an
  interactive descendant; or (b) a handler (`onclick`/`onkeydown`/
  `onkeypress`), `role=button`, or non-negative `tabindex` anywhere in the
  cell's subtree; or (c) a claim — the `aria-sort` attribute present
  (value irrelevant) on any column header cell. Term (c) only ever adds.
- **State dimension** — `sort_signal` per capable table: `aria-sort`
  present anywhere in a column header cell's subtree. Family excess =
  structure excess + state excess (when counted).

### Cards (case B)

- **DOM lane** — containers `ul|ol|div|section`; direct children grouped
  by `(tag, first class token)` then by full shape `(item_shape, image,
  action)`; each shape with ≥3 members is an instance. `imageish` accepts
  `img|svg|picture` or a cover-classed `div|span|i`; innermost qualifying
  container wins; `template` subtrees are inert; card items with no text
  and no real image source anywhere are stubs.
- **JS lane** — local scripts showing iteration; function units extracted
  by brace-matching over literal/comment-blanked text; factories are
  template/concat units whose concatenated literals parse into a
  card-shaped fragment, or builder units creating `{img} ∧ {button|a} ∧
  {article|li|div}`. A screen counts an instance **iff that factory's own
  output** reaches a bound, (near-)empty grid container in the DOM —
  named render sites, anonymous receiver zones, `.map(factory)` forms, and
  depth-2 helper indirection; bindings resolve `getElementById`, `#id`
  selectors and `[data-…]` attribute selectors. The instance's container
  axis is the *host element's* tag, so both lanes share one vocabulary;
  `style` (template/builder) is metadata.
- **Dominance** — per screen: a screen with DOM-lane cards keeps its own
  JS hits as metadata; other screens adopt theirs.

### Validity gate (case C)

Runs per instance, on its anchor's subtree, before signatures enter the
variant sets. Composite containers (`menu`, `menubar`, `listbox`,
`tablist`, `radiogroup`, `tree`, `table`, `grid`, `rowgroup`, `row`,
`list`): direct children must resolve into the allowed set, where
`role=none|presentation` delegates, *generic* elements are transparent
(ARIA 1.2), `group` is transparent, `rowgroup`/`row` descend — and
interactive elements resolve to their real implicit roles, so `div[role=
menu]` full of plain links is as broken as `ul[role=menu] > li`. A
composite with element content but no owned item anywhere is broken.
Native content models (`ul/ol/dl/table`…) are checked when no role
overrides them. Empty containers are vacuously valid; hidden subtrees ARE
checked. Scope limits (documented, mirroring axe): a native container with
a non-composite role (`ul[role=navigation]`) is checked by neither path;
`aria-owns` is not resolved.

### Partitions (like with like)

- **Nav slots:** per screen, the nav with most links (`a[href]`) is
  `primary` (ties: DOM order); the rest pool by normalized
  `aria-label`/`aria-labelledby` (`sec:<label>`, or `sec:unnamedN`).
  Excess = Σ per-partition (|variants| − 1). Chosen *before* the validity
  gate, so an excluded primary does not promote a footer.
- **Toast channels:** `polite` (`role=status`, `aria-live=polite`),
  `assertive` (`role=alert`, `aria-live=assertive`), `other`. Excess
  summed per channel.
- Slot/channel identity depends only on the run's own DOM — no whitelist,
  no condition knowledge.

### Richness (case D)

Sibling block: `families_instantiated`, `families_counted` (the
denominator), `total_instances`, `coverage_cells`, `coverage_ratio`,
`screens_multi_family`, `stub_instances`, `per_family` (instances,
screens_with, stubs, `sources: {dom, script}`), `nonsemantic_candidates`
(lexical census, EN+PT lexemes, metadata only). Substance predicates:
table = any header/cell/caption content; dialog = children, text or
naming; form = ≥1 real field; nav = ≥1 link; card = text or real image
source; toast = always substantive (the empty placeholder is the correct
idiom). Empty directories: `status: no-data`; nonexistent paths:
`status: missing`.

## Known limitations (documented, not patched)

1. **Listener-only sort affordances** (`addEventListener` on a bare `th` —
   2 real A runs): outside the state pool unless claimed via `aria-sort`.
2. **Runtime-only `aria-sort`** (`setAttribute`): static capture shows
   `signal=none`, uniformly.
3. **Static rendering**: framework-rendered pages with no local factory
   source stay invisible to both lanes.
4. **JS lexer ambiguities**: a `/` right after `}` is read as possible
   division, never a regex start (regex literals elsewhere are handled);
   namespace/object-method factories and helper chains deeper than 2 stay
   invisible (executed proof in the panel's notes).
5. **`<template>` contents** in the four inherited v1 detectors (dialog,
   nav, form, toast) follow v1's judgment (not skipped) — kept verbatim
   for cross-round comparability; a sensitivity note, not a fix.
6. **`ul` with a non-composite role** escapes the native content-model
   check (mirrors axe).
7. **Lexical census** can miss unconventionally named fakes; never a
   metric.
8. **Nav substance requires a link** (`a[href]`): an empty client-rendered
   `<nav>` stubs while a thead-only table earns static credit — an
   asymmetry kept deliberately (a nav's minimum substance is navigation)
   and reported via `stub_detail` either way.
9. **Gaming by an instrument-aware author** (e.g. shape-indeterminate
   factories to dodge variant identity) is out of threat model: study
   agents are condition-blind and instrument-blind; the panel's residual
   gaming notes are recorded in its report.

## Self-test

`classifier_v2.py --self-test` (58 checks, all mandatory — missing
fixtures fail): the 15 empty codex directories as no-data and missing-path
as `missing`; case A on the real corpus (zero state excess, 10/10 D tables
counted); case C surgical exclusion (7 in one run, 0 elsewhere); case B
30/30 detection with exactly 5 DOM-lane runs; the calibration pair's
measured richness (4/17/17 vs 6/32/23) and census; mechanical
condition-blindness; 27 held-out counterfactuals from calibration and the
first panel round (divergent signals +1, span-onclick capability,
ARIA-grid capability, broken/delegated/div-link ladders, zero-item
composites, css-cover, JS template, authoring-style equivalence,
mixed-grid +1, dead factory, minified JS, arrow factory, brace-in-string,
inert template, per-screen dominance, dual-severity 0, channel divergence
+1, nav partition 0/+1, stubs beside the denominator, poverty beside a
zero excess); and 15 more from the second round (nested live-region = one
widget, case-insensitive `aria-live`, nested-template idiom, chained and
class-selector receivers, placeholder-tolerant hosts, name-collision
scoping, decorative-svg immunity, all-indeterminate → unmeasurable,
regex-literal survival, checkbox-in-th immunity, bare-th gate symmetry,
button-only form substance, footer-only screens, and a falsifiable
denominator check).

## Sensitivity: v1 → v2 on Round 1's corpus

v1 remains frozen and runnable; the registered analysis reports both.
**Reading rule (per the cross-vocabulary confound):** cross-condition
comparisons of these sums are only safe within the same vocabulary
(D vs D); the A/B columns are shown for instrument transparency, with
`families_counted` medians alongside in the registered output — never as
a standalone contrast.

| Cell | v1 | v2 | Exclusions | Stubs | Unmeasurable | Reading |
|---|---|---|---|---|---|---|
| antigravity A | 0 | 2 | 0 | 0 | 0 | the "consistency by poverty" zero was blindness — JS-rendered cards reveal real dispersion (denominator: 3–4 families) |
| antigravity B | 20 | 11 | 0 | 0 | 2 | toast-channel partition removes the status/alert purpose split; 2 card cells declared unmeasurable (fragment-forest factories), not zero |
| antigravity D | 21 | 9 | 7 | 0 | 3 | `aria-sort` no longer punished; run3's ladder moves to exclusion; the nested live-region widget is one instance, not two |
| claude-code A | 21 | 11 | 0 | 3 | 0 | nav pooling by accessible name removes footer-vs-main false dispersion |
| claude-code B | 18 | 11 | 0 | 1 | 0 | +1 vs the first draft: the regex-literal fix RESTORED a real dispersion point the corrupted blanking had hidden |
| claude-code D | 18 | 7 | 0 | 0 | 0 | +1 vs the first draft: button-only confirm forms back in the pool with their real dispersion |

Shifts run in both directions and track *content*; the instrument has no
way to know the condition. Note the last two rows: the second panel
round's fixes RAISED both claude-code non-A cells — hardening the
instrument twice moved numbers against and in favor of every condition at
different points, which is what a condition-blind instrument under honest
repair looks like.

## Freeze procedure

1. ~~Adversarial verification~~ — done twice (rounds 1 and 2 above); every
   confirmed finding fixed or documented.
2. `sha256sum classifier_v2.py` recorded here and in the OSF registration
   package at protocol freeze; the fixtures directory hashed alongside.
3. After the freeze, any change is a dated `DEVIATIONS.md` entry — same
   discipline as every other Round 2 instrument.

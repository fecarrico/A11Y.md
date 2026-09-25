# tools/

Four dependency-free Python scripts. All are **optional** — the standard works in a purely conversational flow — but a gate that fails a build is stronger than a rule an agent has to remember.

> [!IMPORTANT]
> **These scripts are not the standard, and never a precondition for using it.** `A11Y.md` is portable markdown: it must keep working for anyone whose agent can read a file, with no runtime installed. What the normative core requires (§2, *Static Gate*) is the *attempt* — run `verify-a11y.py` when a shell exists — and honest disclosure when it cannot run: in `REPORT.md` and in the delivery message. No rule ever makes a runtime mandatory.

> [!WARNING]
> **Experimental (v0).** Exercised against built-in fixtures (`--self-test`), this repository and the project's own site — not against a wide range of real projects. A false positive in your pipeline is worse than no gate at all, so start with `--warn-only`, and please [open an issue](https://github.com/fecarrico/A11Y.md/issues) for anything it gets wrong. Bug reports are the fastest way to make it trustworthy.

> **Neither script establishes conformance.** Automated tooling detects only a fraction of real barriers. These check what a regex and a date comparison can check; the human checkpoints in `REPORT.md` are what establish the rest.

**Requirements:** Python 3.9+, standard library only — no `pip install`, no `package.json`. Python is preinstalled on macOS, most Linux distributions and virtually every CI runner. A Node port may follow if adoption shows real friction; until then, this is a deliberate choice for zero dependencies over toolchain familiarity.

---

## `verify-a11y.py` — for projects adopting the standard

```bash
python3 verify-a11y.py [PROJECT_DIR] [--src SUBDIR] [--warn-only]
python3 verify-a11y.py --self-test        # built-in fixtures, one per check
```

It checks two things, and the second is smaller than it looks.

**The evidence the standard demands** — the part no other tool knows exists:

| Check | What it catches |
|---|---|
| `artifacts` | `REPORT.md` missing before a delivery (Release Evidence, §2) |
| `freshness` | report older than the last interface change (git history, falling back to mtime) |
| `report-status` | report claiming PASS while carrying `[ ]`, `[~]` or `[!]` checkpoints — or still carrying the template's status placeholder |
| `independence` | report with no *Verification Independence* field, with more than one level declared, or claiming PASS on `self-reported` — the generating agent as sole witness (Independent Verification, §2) |
| `gate-declared` | report with no *Static gate* field or still carrying its template menu; a field declaring PASS while this very run found errors; NOT RUN declared while the script is evidently running (Static Gate, §2) |
| `contrast-evidence` | every pair recorded in the `REPORT.md` pair table (and in the `A11Y-DECISIONS.md` palette matrix) is **recomputed** with the WCAG formula: a declared ratio that does not match the arithmetic fails; a ✅ below the floor it was measured against fails; the contrast checkpoint marked verified with no pair recorded fails. Warns when a recorded color does not appear in the source (§3: computed, never estimated) |
| `exceptions` | entries without risk owner, approver, tracking issue or expiry — and expired ones |
| `gitignore` | project artifacts excluded from version control |

**What axe cannot see** — the source scan. axe reads the rendered DOM: it does not see event handlers, CSS intent, or source that has not been built yet. These checks read `.html`, `.jsx/.tsx`, `.vue`, `.svelte`, `.astro` and CSS before any build, and they exist for the anti-patterns of Section 6 that pass every DOM checker:

| Check | What it catches |
|---|---|
| `clickable-div` | `<div>`/`<span>` with a click handler — `onClick`, Vue `@click`/`v-on:click`, Svelte `on:click`, Angular `(click)`. A div that replicated a button by hand (`role` + `tabindex`) warns instead of failing: verify Enter and Space |
| `placeholder-label` | `<input>`/`<textarea>` whose only label is its placeholder — axe accepts a placeholder as an accessible name, so this never fails axe |
| `half-climbed-aria` | `role="tablist"` with no `role="tab"` in the file — the mold Study 3 found surviving two releases — fails; the other composites (`listbox`, `menu`, `tree`, `radiogroup`, `grid`) without their required children warn, since the children may live in another component |
| `aria-soup` | redundant roles on native elements (`role="button"` on `<button>`, `role="navigation"` on `<nav>`, `role="heading"` on `<h2>`…); `aria-label` repeating the visible text (warning — it drifts into an SC 2.5.3 failure); `aria-expanded` hardcoded in markup that no script in the project ever toggles (warning) |
| `nullified-alt` | `aria-hidden` (`="true"`, `={true}` or the bare JSX boolean) or `role="presentation"` on an image carrying a non-empty `alt` |
| `orphaned-aria` | `aria-controls`/`labelledby`/`describedby`/`activedescendant` pointing at an id absent from the file (warning — the target may live elsewhere) |
| `overlay` | a script or link from an accessibility-overlay vendor — an overlay never fixes the DOM that produced the barrier (§6) |
| `positive-tabindex` · `outline-none` · `redundant-alert` · `media-autoplay` | keyboard order, focus visibility, live-region and media rules from Sections 3–4 that a text search can catch |

The source scan reads whole files, not single lines: JSX spreads one element across many lines, and a line-by-line scan never sees `<div` three lines above its `onClick`.

**What the gate does not see, on purpose.** Five anti-patterns of Section 6 are not a job for a text search and are not attempted: focus management in a modal, text over video, a parallel machine-facing copy, a scroll container that does not overflow (`tabindex="0"` is only wrong when nothing scrolls, which is runtime), and content parked at `opacity: 0` (legitimate in too many places to flag). They stay with review and with the human checkpoints in `REPORT.md`. In the project's own Study 2, the uninstructed screens failed axe on 536 critical/serious nodes — 505 of them contrast, 16 missing alt, 13 missing labels — and this scan sees none of those three classes. It is the receipt, not the purchase.

Exit code is `1` on errors, `0` on warnings only. Use `--warn-only` to report without failing the build while a team adopts the standard.

Every run ends with the exact line to record in the report's *Static gate* field. When the script cannot run at all — a permission denied, no shell — the agent records `NOT RUN` with the reason and says so in the delivery message (A11Y.md §2, Static Gate): a gate that silently did not run reads exactly like one that passed.

**GitHub Actions** — pin to a tag, never to `main`: this is executable code, and a moving branch is a supply-chain risk. Bump the tag deliberately, the same way you would any other dependency.

```yaml
- name: A11Y.md static gate
  run: |
    curl -sO https://raw.githubusercontent.com/fecarrico/A11Y.md/v2.0.2/tools/verify-a11y.py
    python3 verify-a11y.py . --src src --warn-only   # drop --warn-only once the team is ready
```

Vendoring the script into your repository is equally valid, and gives you a reviewable diff when you upgrade.

## `contrast-check.py` — deterministic WCAG contrast

```bash
python3 contrast-check.py --bg '#121212' '#f2f2f2' '#5a5a5a'   # verdict per pair; exits non-zero on failure
python3 contrast-check.py --css styles.css --page-bg '#fff'     # triage: full pair matrix, never gates
python3 contrast-check.py --self-test                            # built-in fixture cases
```

Born from the project's own benchmark: contrast was the failure present in every condition of Study 2, and it is arithmetic — it should be computed, never estimated by a model. Pair mode gives a verdict against the Standard (AA) or Shield (AAA) floors and can gate a build; CSS mode extracts every color literal (hex/rgb/hsl, alpha composited over `--page-bg`) and flags failing pairs as **triage** — it cannot know which colors actually meet on the rendered page. The rendered-page check in `REPORT.md` remains mandatory.

## `lint-standard.py` — for maintaining the standard itself

```bash
python3 lint-standard.py [REPO_ROOT]
```

Checks parity between `docs/en` and `docs/pt-BR` (file list, headings, contract rule count), orphaned reference guides, guides and templates with no loading trigger in the §2.1 map, broken relative links, phase triggers ("at final delivery") that never fire in continuous delivery, any label calling the project artifacts optional, and Wiki drift (the Wiki must document the same number of contract rules as the core file and list every reference guide — skipped when the folder is absent).

Every check exists because the corresponding defect actually shipped: the ten guides orphaned in 1.0.0, the "Optional Templates" label and the phase trigger that together caused the [2026-08-01 field failure](../CHANGELOG.md), and the Wiki running two releases ahead of the core file while nothing compared them. Run against the release before 1.2.0, it reports all four of the originals.

## `context-cost.py` — what the standard costs in context

```bash
python3 context-cost.py [--lang en|pt-BR] [--compare GIT_REF] [--at GIT_REF] [--markdown]
```

The standard is loaded lazily, so "how much context does it cost" has no single answer — it has one per task type. This reads the Loading Triggers map out of §2.1 and adds each guide to the core, giving the floor for every row in the table. It stays correct when the map changes, because the map is its input.

`--compare` puts two versions side by side, which is what a release note needs before it claims a reduction. A core that slims while its guides deepen does not save the same amount on every task: it saves most where no guide applies, and least where a guide absorbed what the core gave up.

```bash
python3 context-cost.py --compare v1.7.0 --at v1.8.0
```

> 1.8.0 cut the core by 10.5%. Per task the saving ranges from 10.5% (no guide applies) to 2.1% (`guide-platform-native`, which grew by more than half). Nothing got worse; the headline figure is the best case, not the typical one.

Characters are counted exactly; the token column is an estimate from a fixed divisor. **A ratio between two versions is trustworthy — the same bias sits on both sides — an absolute cost in currency is not.** Quote money only from a token count the model provider produced.

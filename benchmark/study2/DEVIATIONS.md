# Study 2 — deviations journal

> Same discipline as [Study 1's](../DEVIATIONS.md): every departure from the
> registered protocol, dated, clarifications included, nothing hidden. Newest
> first.

## 2026-08-24 — Instrument defect: the verifier served every asset as text/html; Study 2 re-verified

- **Discovery:** the author, reviewing an illustration built from the
  verification screenshots, noticed the journey pages rendered without CSS.
  He was right for the third time: the verifier's embedded HTTP server sent
  **every** file with `content-type: text/html`, and browsers silently reject
  stylesheets with a wrong MIME type. Scripts still executed; styles never
  applied.
- **Scope, precisely:** Study 2 only. Study 1's Arm-1 artifacts are single
  self-contained files and Arm-2 pages were mechanically inlined before
  verification — the MIME type never mattered for them. Study 2 was the first
  design whose screens reference external `assets/` files, so **all 210
  screens were axe-scanned and screenshotted unstyled**. Unaffected by
  construction: the consistency classifier (static DOM, no rendering),
  tokens, durations, governance counts.
- **Remedy:** MIME table by extension in `verify.js` (dated comment in code);
  the styleless measurement is preserved under `runs/study2/verify-sem-css/`
  and the corrected verification replaces it — **both sets reported**, same
  discipline as the Arm-1 repair.
- **Dataset:** the published record (10.5281/zenodo.22073026) contains the
  styleless Study-2 verification; a **version 2** of the record with the
  corrected files follows once the re-verification is complete, with this
  entry cited in the version notes. Zenodo versioning preserves v1 —
  nothing is overwritten, everything is traceable.

## 2026-08-24 — Dataset published (shared DOI with Study 1)

Study 2's raw data (30 journeys: screens, verification reports, screenshots,
classifier output, registered analysis, probes) is published in the combined
benchmark dataset: [doi.org/10.5281/zenodo.22073026](https://doi.org/10.5281/zenodo.22073026), CC-BY-4.0,
MD5-audited on publication day. Files `a11ymd-study2-*` + `MANIFEST-study2.json`.

## 2026-08-20 — Codex quota wall: the pre-declared reserve swap executes

- **What happened:** all 15 Codex journey runs failed in seconds with the
  client's own message: *"You've hit your usage limit … or try again at
  Sep 16th, 2026"*. The plan's Codex quota — consumed in part by Study 1's
  ecological runs — resets only in a month; waiting is not viable and was
  never required.
- **What executes:** the naming entry above pre-declared exactly this: the
  reserve agent (Antigravity) enters **only if a quota wall forces the swap,
  with its own dated entry** — this is that entry. No new decision is being
  made; a declared rule is being applied on its declared trigger.
- **Conditions of the swap:** Study 1's fresh-profile amendment applies in
  full — empty-`HOME` profile, `--new-project` per run, and the clean-profile
  gate probe re-run **before any retained journey** (the profile has since
  hosted Study 1's Antigravity runs; if ambient knowledge of the standard
  survives, collection halts and this entry reopens with that outcome).
  Rule delivery for condition D: verbatim Quick Start as prompt preamble,
  standard on disk — the bridge-cell translation already declared in ARM2.md.
- **Data handling:** the 15 failed Codex records stay in the collection log
  as failed records (Study 1 precedent); `--resume` never confuses them with
  journeys, which key by agent. If Codex quota returns before Study 2 closes,
  its 15 journeys may still be collected under the original naming — additive,
  declared here in advance.

## 2026-08-20 — Registration accepted; agents named; pre-declared fill-ins applied

- **Registration:** [osf.io/mqs7x](https://osf.io/mqs7x), accepted 2026-08-20.
  Snapshot audited on acceptance day: `study2/` files 6/6 bit-identical to the
  frozen hashes.
- **Agents named**, per §Engines' declared rule (available quota): **Claude
  Code** (2.1.233 at naming) and **Codex CLI** (0.147.0). **Antigravity stays
  as declared reserve** — it enters only if a quota wall forces a swap, with
  its own dated entry, under Study 1's fresh-profile amendment.
- **Fill-ins applied, not deviations:** the registration URL written into
  §Registration and the README status boxes — both pre-declared as fill-ins by
  the protocol itself. The frozen snapshot proves this journal started empty.
- **Collection opens** with the merge of this entry. First wave: Claude Code.

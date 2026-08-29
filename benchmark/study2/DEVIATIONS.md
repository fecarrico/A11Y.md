# Study 2 — deviations journal

> Same discipline as [Study 1's](../DEVIATIONS.md): every departure from the
> registered protocol, dated, clarifications included, nothing hidden. Newest
> first.

## 2026-08-29 — Environment leakage into the Claude Code arm: the generic condition knew the standard existed and hunted for it; visible attempts were denied, one read channel cannot be excluded

- **Discovery:** found by the independent methodological panel convened to
  review the Round-2 protocol draft, and verified by hand against the raw
  captures before this entry was written. Nothing below was surfaced by the
  registered instruments.
- **What happened:** the Claude Code runs inherited the operator's real user
  environment (the ecological framing declared in `ARM2.md`). That environment
  contained two things the 2026-08-18 environment audit did not cover: a user
  skill whose description — injected into the system prompt of **every**
  session, all conditions — names "o padrão de acessibilidade do A11Y.md";
  and a global permission grant pre-approving **read access to the operator's
  personal knowledge vault**, which contains the project's master notes.
- **The observed behavior, from `raw/claude-code__journey__B__*.json`:** all
  five generic-condition (B′) runs attempted to locate the standard or the
  vault outside their workspace (`find … -iname "A11Y*"`, vault paths, topic
  files). Every such attempt visible in the captures sits in
  `permission_denials` — the shell searches were **refused**. Run 2's final
  summary explicitly names the standard and the vault, i.e. the run was aware
  of the experiment's subject. D′ and A′ runs received the same system prompt;
  the hunting behavior appears in B′.
- **Scope, precisely:** the captures record denials and final summaries, not
  approved tool calls — so a direct `Read` of vault files (pre-approved by the
  grant, invisible in `permission_denials`) **cannot be excluded** for any
  Claude Code run. Antigravity ran under the fresh-profile gate and is not
  affected. The journey workspaces themselves were clean.
- **Why the conclusions survive:** the leakage direction is conservative. A
  generic condition that knows the standard exists — or reads its notes — can
  only move B′ *toward* D′, shrinking the D′ vs B′ separation the study
  reports. Every published conclusion that survives this bias survives it in
  the standard's disfavor, not its favor. The A′ baseline and the
  within-condition governance counts (10/10 vs 0/20) are unaffected in kind:
  no A′ or B′ run produced the artifacts, aware or not.
- **Stated in the other direction, deliberately:** the same arithmetic means
  the credit this study gives the generic phrase may be **overstated in this
  arm** — how much of B′'s showing is the phrase and how much is the leak
  cannot be decomposed from these captures. The clean evidence for the
  phrase's real effect lives in Study 1's API arm and in the Antigravity arm,
  both unaffected; readers should weigh the Claude Code B′ cells accordingly.
- **Why it is a deviation and not an edit:** the registered protocol declared
  the ecological environment; it did not declare that the environment names
  the object of study in the system prompt, and the audit that cleared the
  environment was incomplete. That gap is the deviation.
- **Remedy (Round 2, protocol-level):** dedicated, sanitized HOME per agent
  (credentials only), the profile's contents listed in the frozen snapshot,
  and a per-agent gate probe that tests the symptom itself — a B′-style probe
  retained only if no reference to or search for the standard appears in the
  transcript. This entry is cited as the probe's motivation.
- **Dataset:** unchanged. The raw captures already carry the evidence
  (`permission_denials` preserved verbatim); nothing was overwritten. Readers
  of the published contrasts should weigh this entry alongside the
  training-contamination disclosure — both push in the same conservative
  direction.
- **Credit where due:** the Round-2 review panel (six independent lenses,
  adversarial verification), whose parecer flagged the skill description and
  the vault grant; the raw-capture verification is the author's session.

## 2026-08-25 — Dataset v3 published (10.5281/zenodo.22088369)

The corrected registered analysis is live as version 3 of the dataset record:
[doi.org/10.5281/zenodo.22088369](https://doi.org/10.5281/zenodo.22088369)
(concept DOI [10.5281/zenodo.22073025](https://doi.org/10.5281/zenodo.22073025)
always resolves to the latest version). The Study-2 package now carries the
corrected `analysis.json` alongside the preserved inflated output
(`analysis-token-double-count.json`) — closing the loop the defect-#4 entry
below opened. All other files are bit-identical to v2, MD5-audited via the
Zenodo API on publication day: 6/6 identical to the local originals. Nothing
was overwritten; v1 and v2 remain archived and citable.

## 2026-08-24 — Instrument defect #4: the analyzer double-counted Antigravity token usage; analysis re-run, both outputs preserved

- **Discovery:** during an author-requested external scrutiny of the full body
  of work, the author asked whether the report's token table counted per screen
  or per whole journey. Tracing that table's provenance against `analysis.json`
  exposed a factor-of-two mismatch — the fourth instrument defect, and the
  fourth found by human contact with the object rather than by any log: three
  by eye on the screens, this one by a question in front of a table.
- **The defect:** `analyze.py` summed every usage field whose name contains
  "token". The Antigravity client reports `total_tokens` (= input + output)
  **alongside** its components, so input and output were counted twice:
  `fresh_per_screen` and `total_per_screen` were inflated ≈2× for every
  Antigravity journey. The Claude Code schema has no aggregate field and was
  unaffected (verified: identical values under both computations). Consistency,
  axe and governance outcomes never touch these fields — the defect is confined
  to the token metrics of one agent.
- **Why the conclusions survive:** the inflation is uniform across conditions
  (same client, same schema on every journey), so directions, ratios and
  Cliff's deltas are unchanged; medians and interval endpoints halve. The
  report's token table (21k / 19k / 41k fresh tokens per screen) had been
  computed from the raw fields directly and is confirmed correct by the re-run.
- **Remedy:** explicit per-schema field lists in `analyze.py` (dated comment in
  code); the inflated output is preserved at
  `runs/study2/analysis-token-double-count.json` and the corrected
  `analysis.json` replaces it — dual reporting, the discipline of defects
  #1–#3 applied a fourth time.
- **Dataset:** v2 of the Zenodo record carries the inflated `analysis.json`;
  the next dataset version will carry the corrected file and cite this entry
  in its version notes. Nothing is overwritten, everything stays traceable.

## 2026-08-24 — Dataset v2 published (10.5281/zenodo.22080079)

The corrected Study-2 verification is live as version 2 of the dataset record:
[doi.org/10.5281/zenodo.22080079](https://doi.org/10.5281/zenodo.22080079)
(concept DOI [10.5281/zenodo.22073025](https://doi.org/10.5281/zenodo.22073025)
always resolves to the latest version). Study-1 files carried over bit-identical
from v1 (MD5-audited via API on publication day, 6/6); the styleless Study-2
measurement is preserved inside the v2 package under `verify-sem-css/`.
Version 1 remains archived and citable — nothing was overwritten.

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

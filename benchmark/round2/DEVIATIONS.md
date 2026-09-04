# Study 3 — deviations journal

> Same discipline as [Study 2's](../study2/DEVIATIONS.md): every departure
> from the registered protocol, dated, clarifications included, nothing
> hidden. Newest first. The frozen snapshot proves this journal started
> with the entry below and nothing else.

## 2026-09-04 — Collection complete: 39/40 retained; one instrument defect found by a real run (strict screen count) — fixed with dual records; both waves contamination-audited clean

- **Final tally (latest record per run id):** Claude Code **20/20
  retained** (zero failures, zero retries, every run first-attempt);
  Antigravity **19/20 retained** + 1 legitimate non-retained.
- **The non-retained run, precisely:** `antigravity__journey__D20__run2` —
  a real 561k-token session (SUCCESS) whose only denial was
  `AskQuestion`: the agent asked for the compliance profile (the standard
  tells an *interactive* session to confirm it) instead of applying the
  documented non-interactive default, and delivered an architectural plan
  as prose — zero files. The harness is identical to every retained run
  (D20 runs 1/3/4/5 completed 7/7 under it); this is agent behavior under
  the D20 condition — study data, reported as the cell's failure rate,
  never replaced.
- **Instrument defect, found by a real run (the tradition holds):**
  `antigravity__journey__A__run4` produced all 7 named journey screens
  PLUS a scratch `test.html`; the runner's strict `screens == 7` marked a
  complete journey not-retained. Fix: retention now requires the seven
  NAMED screens non-empty (`journey_complete`), extras allowed —
  faithful to the registered wording ("produces 7 non-empty screens").
  `run.py` sha256 → `87f733443f5043f0…` (self-test PASS). Dual records:
  the original false-negative log line is preserved; a recomputed record
  is appended (the analyzer reads the latest per id) with the correction
  note embedded.
- **Contamination audit, both waves, all 40 raws:** zero symptom terms in
  A/B cells, zero network use, zero references to the operator's files.
  The only denials across the corpus: Claude Code's own HTML-validation
  attempts outside the narrow tool grant (denied as designed) and the two
  journaled Antigravity harness episodes.
- **Verification:** the registered `verify.js` (pinned axe 4.13.0) runs
  per retained run; extra non-journey pages (the one `test.html`) are
  excluded from measurement via a staging copy — nothing deleted from the
  collected artifacts.

- **Registered analysis executed** (frozen analyze.py; sensitivity v1
  alongside; results in `runs/round2/analysis.json`, to ship with the
  dataset). The pre-declared topology inspection for the single isolated
  `nested-interactive` (D20 run3, sell, 1 node) confirms a lapse, not a
  mold. Publication remains gated on the protocol's human-eye sampling
  rule — the author's step.

## 2026-09-04 — 1.1.26 also demands confirmation for file READS in print mode; explicit read allow restores the Round-1 profile; one harness-degraded run quarantined and recollected, five untouched runs kept with proof

- **What happened:** with commands denied by policy, run B2 still failed
  (0 screens): its raw shows a denied `read_file`/ViewFile and a final
  response ASKING for permissions instead of building. The 1.1.26 client
  requires confirmation for reads in print mode; Round 1's client
  auto-approved them. A multi-page task realistically requires re-reading
  one's own files — this was harness degradation, not agent failure.
- **Fix, completing the Round-1 profile:** the settings gain
  `"allow": ["read_file(*)"]` beside `"deny": ["command(*)"]` — reads
  auto-approved (as in Round 1), commands denied (as in Round 1), edits
  auto-approved by the mode (as in Round 1). Probed end-to-end: a
  read-then-write task completes with the command denied mid-way and the
  session alive; the gate probe produces its screen with zero denials and
  zero symptom terms. `build_home.py` updated (current sha256 recorded in
  git; the HOME settings file's sha256:
  `07d0d607f26c911dce8f38007f2087bb9dc3befdf5539e6b326c0096d93db088`).
- **The five already-retained wave-2 runs are KEPT:** their raws show
  `denied_actions: None` — no run ever touched a deniable path, so the
  harness change is behaviorally invisible to them; the effective harness
  they ran under is identical to the final one. Stated precisely so the
  reader can weigh it: A1, B1, D18-1, D20-1, A2 (7/7 screens each, zero
  denials each).
- **Run B2 quarantined** (`quarantine-agycli-20260904/`) as a harness
  failure and its slug recollected under the final settings.
- **Wave 2 resumes** (5 kept + 15 to collect).

## 2026-09-04 — Client 1.1.26 cancels a print-mode session on its first denied command; denial re-expressed as declared policy (same profile, working mechanics); one real session lost to the bug, quarantined and recollected

- **What happened:** wave 2's true first run (a REAL session this time —
  72,867 tokens, treatment A delivered) died at 1.2 min with status
  CANCELED, empty response, zero files. The client log shows the chain:
  the model requested `RunCommand`, print mode soft-denied the
  confirmation (correct for this arm), and the client's emitter then broke
  its own stdout and shut the session down. **Reproduced
  deterministically** with a minimal two-files-and-a-command task: the
  session dies at the first denied command; Round 1's client continued
  after denials.
- **Fix, preserving the arm's profile exactly:** the sanitized HOME now
  carries a one-key client settings file —
  `{"permissions": {"deny": ["command(*)"]}}` (sha256
  `07d0d607f26c911dce8f38007f2087bb9dc3befdf5539e6b326c0096d93db088`) —
  so command denial is DECLARED POLICY rather than a per-request
  confirmation, sidestepping the broken path. Commands are still denied;
  edits still auto-approved; nothing else changes. Verified both ways:
  the reproduction now completes (SUCCESS, both files written, command
  denied without killing the session), and the gate probe produces its
  screen. A first draft with an explicit empty `"allow": []` was probed
  and REJECTED — it hides the edit tools too (the model answers with
  inline HTML and writes nothing); deny-only is the correct form.
- **`build_home.py`** now writes this settings file for the antigravity
  HOME (hash `845afc80…`-era value superseded; current
  `ea56fd9fc73649820277cf790145ce8bc5a53135f889bf0d833925be95b5cc00`).
- **Gate probe under the final settings: PASS** (1 screen; zero symptom
  terms across the probe raws of this sequence).
- **The lost session:** `antigravity__journey__A__run1` (72,867 tokens,
  zero artifacts — killed by the client bug, not by the agent or the
  task) is quarantined in `runs/round2/quarantine-agycli-20260904/` and
  the slug is recollected: a harness failure upstream of the outcome, not
  a study failure rate. The log keeps its record.
- **Wave 2 restarts** (again) from run index 1.

## 2026-09-04 — The Round-1 Antigravity model is retired from the client: gemini-3.5-flash no longer exists in 1.1.26; successor chosen by the Round-1 rule (current mainline flash, low effort): gemini-3.8-flash

- **What happened:** the re-pinned wave-2 relaunch failed differently — the
  client's full error revealed the deeper cause: *"model gemini-3.5-flash
  is not recognized as a known model"*. The 1.1.26 catalog carries only
  Gemini 3.6/3.7/3.8 Flash (plus Pro and non-Gemini models); the Round-1
  model was retired by the vendor. 12 more slugs burned as CLI rejections
  before the runner was stopped — again **zero agent sessions, zero
  tokens** (every failure is a pre-model CLI error).
- **Decision, by the Round-1 rule:** Round 1 chose the CURRENT mainline
  flash of its collection window at low effort; the same rule today gives
  **gemini-3.8-flash + --effort low** (the flag is supported again for
  catalog models). Freezing on the numerically closest retired-adjacent
  model (3.6) would be false continuity — it is not the Round-1 model
  either — and carries the highest risk of another mid-collection
  retirement. The primary contrast (D20 vs D18) is internal to this wave
  — same model both sides — and is unaffected; readings against Round 1
  were already declared context-only (clients no longer exist), now with
  the model change stated on top.
- **Instrument amendment:** `run.py` hash `845afc80…` →
  `6ed7720e97d9bbd8265ed73a3c5329c0081d5cffd4dc59cd6e0c4cf85e7e274a` (the Antigravity
  command only); self-test PASS.
- **Gate probe under the new model: PASS**
  (`probes/antigravity__gate-probe__20260904T092241Z*` — SUCCESS, one
  screen, zero symptom terms).
- **Quarantine:** the 12 burned slugs' raw attempts and empty screen dirs
  joined `runs/round2/quarantine-agycli-20260904/`; `log.jsonl` keeps
  every record.
- **Version×condition note for the report:** every retained Antigravity
  cell will carry client 1.1.26 + gemini-3.8-flash (low); Claude Code
  cells carry 2.1.237. **Wave 2 restarts** from run index 1.

## 2026-09-04 — Antigravity client auto-updated mid-launch (1.1.22 → 1.1.26) and dropped the frozen command's --effort flag; command adapted, version re-pinned, zero agent sessions affected

- **What happened:** wave 2's first slug failed 3× in seconds — client
  1.1.26 rejects `--effort` for gemini-3.5-flash ("--effort is not
  supported for model") — and the runner then **aborted by design** on the
  version pin (1.1.26 ≠ 1.1.22) before touching a second slug. The client
  had auto-updated between the pre-launch version check and the first run.
- **Scope, precisely:** zero agent sessions occurred (0 screens, 0 turns,
  0 tokens — the CLI rejected the invocation before any model ran). Wave 1
  (Claude Code, 20/20 retained) is untouched.
- **Version re-pin:** 1.1.26, applied BEFORE the agent's first retained
  run — the pre-declared window (the protocol permits version changes
  between complete cycles, logged; no Antigravity cycle existed). The
  registered pin (1.1.22, in the immutable OSF snapshot) is superseded by
  this dated entry; the version×condition table will show 1.1.26 for every
  Antigravity cell.
- **Frozen-command amendment, minimal:** `--effort low` removed from the
  Antigravity invocation (the client discontinued the flag for this
  model); the model itself stays the Round-1 model (gemini-3.5-flash).
  Effort semantics now follow the client's default for this model —
  declared as a limitation for any reading against Round 1 (already
  context-only); the primary contrast (D20 vs D18) is internal to this
  wave and unaffected. `run.py` frozen hash `0786bcd1…` →
  `845afc8098c5715f9715e87856cabdeba5a8abb4670ab2790df79a24e40a85a9`
  (this change only); self-test PASS.
- **Quarantine:** the burned slug's raw attempts and empty screen dir
  moved to `runs/round2/quarantine-agycli-20260904/`; `log.jsonl` keeps
  every record (the analyzer reads the latest per id).
- **Wave 2 restarts** from run index 1 under the re-pinned version.

## 2026-09-03 — Stale-credential false start: 60 auth-failed attempts quarantined; zero agent sessions occurred; HOME rebuilt with the live credential; gate probe re-passed

- **What happened:** the first collection launch failed to authenticate on
  every attempt — "OAuth session expired and could not be refreshed". The
  sanitized HOME carried a credential *copied* on 2026-08-30; the client
  in the operator's live environment had since rotated the refresh token,
  invalidating the copy. The runner burned all 20 slugs (3 mechanical
  retries each, 60 records) in under a minute.
- **Scope, precisely:** no agent session ever authenticated — zero screens,
  zero prompts delivered, zero contact with the task. This is a harness
  failure upstream of the experiment, not failed study runs.
- **Remedy, everything preserved:** the 60 raw attempt captures and empty
  screen dirs moved to `runs/round2/quarantine-auth-20260903/` (with a
  copy of the log at incident time); `log.jsonl` keeps all 60 records —
  the analyzer reads the latest record per run id, so the quarantined
  false start can never displace a real journey. The sanitized HOME was
  rebuilt (`claude-code-3`) with the credential as a **symlink to the
  operator's live auth file** — authentication only, rotating by nature
  (its manifest hash is of build time and is declared stale by design);
  settings byte-identical to the frozen grant (sha256 `8198a92e…`).
- **Gate probe re-run under the rebuilt HOME: PASS**
  (`probes/claude-code__gate-probe__20260904T004957Z*` — zero symptom
  terms; the only permission denials are the agent's own HTML-validation
  attempts outside the narrow grant, denied as designed).
- **Why this is a deviation entry and not silence:** the protocol's
  environment section describes credentials-only HOMEs; it did not
  anticipate credential rotation between freeze and collection. The
  symlink is the minimal amendment, applied to the auth file only, and
  journaled here before any retained run.
- **Collection restarts** from run index 1 under the rebuilt HOME.

## 2026-09-03 — Registration accepted; collection opens

- **Registration:** [osf.io/wt5n4](https://osf.io/wt5n4) — "A11Y.md
  Efficacy Benchmark (Study 3)", date_registered 2026-08-31, public, no
  embargo, archiving complete (verified via the OSF API on this date).
- **Acceptance-day audit:** the 7 frozen files plus the fixtures corpus
  re-hashed against `REGISTRATION.md`'s table — **8/8 identical**. All
  four instrument self-tests re-run on this date: PASS.
- **Fill-ins applied, not deviations:** the registration URL written into
  `REGISTRATION.md` and `PROTOCOL.md` §Status — both pre-declared by the
  frozen protocol. The post-fill-in hash of `PROTOCOL.md` is recorded in
  `REGISTRATION.md` beside the frozen one.
- **First-submission note, for the record:** the 2026-08-30 submission
  failed inside OSF's archiving step ("errors copying files from some of
  the linked third-party services" — with no third-party services
  connected to the project; an OSF-side failure, support ticket filed).
  The identical draft, resubmitted 2026-08-31, registered cleanly. No
  content changed between the two attempts.
- **Collection opens** with the merge of this entry. First wave: Claude
  Code (20 runs, interleaved by run index). Second wave: Antigravity.
  Verification per run via the registered `verify.js` (pinned axe 4.13.0);
  analysis via the frozen `analyze.py`. Per-run contamination audit as
  registered; the human-eye sampling rule gates publication, not
  collection.

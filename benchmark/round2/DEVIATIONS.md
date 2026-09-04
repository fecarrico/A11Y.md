# Study 3 — deviations journal

> Same discipline as [Study 2's](../study2/DEVIATIONS.md): every departure
> from the registered protocol, dated, clarifications included, nothing
> hidden. Newest first. The frozen snapshot proves this journal started
> with the entry below and nothing else.

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

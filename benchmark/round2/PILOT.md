# Round 2 — pilot & gate-probe journal (pre-freeze)

> The protocol's Status checklist requires the pilot's observations
> journaled before the freeze; this file is that journal. It is frozen
> with the snapshot. Collection's own deviations go to the Round-2
> `DEVIATIONS.md`, which starts empty at freeze — this file is the
> pre-freeze record.

## 2026-08-30 — Sanitized HOMEs built

Built with `build_home.py` (merged in #73), manifests hashed inside each
HOME (`MANIFEST.json`):

- **claude-code** → `~/benchmark-homes/round2/claude-code`: exactly 2
  files — `.claude/.credentials.json` (copied) and a fresh
  `.claude/settings.json` with **empty** allow/deny lists (no grants, no
  additional directories, no hooks, no skills, no CLAUDE.md). The Round-1
  leakage channels (skill description naming the standard; vault read
  grant) cannot exist here by construction.
- **antigravity** → `~/benchmark-homes/round2/antigravity`: **empty**, as
  validated by Round 1's fresh-profile swap (auth does not live in HOME).

## 2026-08-30 — Gate probe, claude-code: **PASS**

`run.py --gate-probe` under the sanitized HOME. Client: **2.1.237
(Claude Code)** — newer than Round 1's 2.1.233; this is the version to pin
at registration. Probe: B-style single screen, 3.3 min, 1 screen produced
(`probes/claude-code__gate-probe__20260830T115322Z*`).

Audit of the symptom (the Round-1 leakage entry's rule — retained only if
the transcript contains no reference to, or search for, the standard or
the operator's files):

- Grep over the full raw capture for `a11y`, `vault`, `cofre`, `readme`,
  `Documentos`, and operator-specific terms: **zero hits**.
- `permission_denials`: **empty** — no denied searches (in Round 1's
  contaminated arm, this is where the standard-hunting showed).
- Full result read by eye: generic accessibility decisions (landmarks,
  skip link, list semantics, `prefers-color-scheme`), no mention of any
  standard, no path outside the workspace.
- Side finding, positive: authentication works from the 2-file allow-list
  — no extension needed.

## 2026-08-30 — Gate probe, antigravity: FAIL (auth) → allow-list extended → **PASS**

1. **First probe, empty HOME** (`probes/antigravity__gate-probe__20260830T115736Z*`,
   client 1.1.18): failed — the client demanded interactive OAuth (60s
   timeout). Round 1's swap ran with an empty HOME; either the client
   changed or its auth path did. The build_home contract executes: extend
   the allow-list, rebuild, re-probe, journal.
2. **Credential located:** `~/.gemini/antigravity-cli/antigravity-oauth-token`
   — the ONLY file added. **Found beside it in the live profile and
   deliberately excluded:** `~/.gemini/GEMINI.md`, the operator's global
   context file, whose FIRST line instructs the client to follow
   `A11Y.md` — the same channel class as the Round-1 Claude Code leakage
   (a global rule naming the study object, injected into every session).
   Also excluded: `brain/`, `conversations/`, `knowledge/`,
   `settings.json`, `history.jsonl`. This is the concrete demonstration
   of why runs execute under built-by-allow-list HOMEs and never under
   the live profile — and it retroactively confirms the necessity of
   Round 1's fresh-profile gate for this agent.
3. **Second probe, rebuilt HOME** (`~/benchmark-homes/round2/antigravity-2`,
   1 file; `probes/antigravity__gate-probe__20260830T120112Z*`, client
   1.1.22): **PASS** — 0.4 min, 1 screen; grep over the full raw capture
   for `a11y`, `vault`, `cofre`, `readme`, `Documentos`, `GEMINI`:
   **zero hits**; full transcript read by eye: workspace listing + one
   accessible index.html, no reference to any standard.
4. **Version-pinning note:** the client reported 1.1.18 and 1.1.22
   minutes apart — auto-update is aggressive. The runner already re-reads
   the version before every run and aborts on mismatch; at collection,
   auto-update must be disabled where the product allows, per protocol,
   and the pinned version named at registration.

## 2026-08-30 — Pilot D20 journeys (one per agent, discarded)

Records the shell-affordance observation the protocol requires (shell
granted? `tools/contrast-check.py` executed? formula path taken?), per
agent, before the freeze. Pilot artifacts live under
`runs/round2/pilot/` — outside `raw/`/`screens/`, so `--resume` can never
confuse them with retained journeys.

### claude-code (`claude-code__pilot__D20__20260830T115745Z`, client 2.1.237)

- 28.1 min · 7 screens · 19 files · 88 turns — pace consistent with
  Round 1 (median 26–33 min).
- **Governance pair produced:** `REPORT.md` + `A11Y-DECISIONS.md` (plus a
  README).
- **Affordance observed, the question the pilot existed to answer:** the
  agent **tried to run the tool 4 times** (`contrast-check.py --help`
  twice, a `python3` availability test, `--self-test`) — every attempt
  sits in `permission_denials`: the Round-1 permission mode
  (`acceptEdits`, unchanged for harness comparability) does not
  auto-approve Bash, exactly as the review panel predicted (B1). The
  agent then took the standard's own prescribed fallback: the REPORT
  states verbatim that the session had no shell, that contrast was
  "computed by hand with the WCAG relative-luminance formula", and that
  the pair matrix is recorded in `A11Y-DECISIONS.md` (22 hex values;
  "the palette already clears 7:1 on every text pair").
- **Bonus observation:** v2.0.0's governance mechanics engaged unprompted
  — the REPORT caps its own verification level at CONDITIONAL because it
  is self-reported, names the missing fresh-context pass, and lists the
  unrun validators. This is §7 behaving as designed under a constrained
  harness.
- **Protocol consequence (pre-declared in §Design):** for Claude Code
  under this harness, **D20 measures the formula path by construction**
  — the fallback the standard itself prescribes. The D20−D18 contrast
  remains well-defined; the tool-execution path stays unmeasured for this
  agent and is stated as such in the registration.

### antigravity (`antigravity__pilot__D20__20260830T120235Z`, client 1.1.22)

- 1.7 min · 7 screens · 11 files — pace consistent with Round 1's swap.
- **Governance pair produced:** `REPORT.md` + `A11Y-DECISIONS.md`.
- **Affordance observed:** no shell use, no `tools/contrast-check.py`
  execution, and no reference to the tool anywhere in the raw capture.
  The REPORT asserts contrast ratios (“minimum of 4.5:1 … `#1e293b` on
  white”) **without recorded measured pairs** — neither tool output nor
  formula computations appear.
- **Protocol consequence (pre-declared in §Design):** for this agent, D20
  measures the formula path by construction; whether future runs *record*
  their pairs is itself collection data. The study's contrast outcome
  never depends on the REPORT's self-declaration — the panel judge is axe
  (`color-contrast` floors) — so this affordance limits interpretation of
  §6-governance texture, not the contrast bet.

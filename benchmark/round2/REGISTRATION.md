# Study 3 — OSF registration package

> Prepared 2026-08-30 by the study's tooling session; **submission is the
> author's act** (fe.carrico@gmail.com, OSF account holder). This file is
> the outside-the-freeze ledger: it records the frozen snapshot's hashes —
> including the protocol's own — and everything the registration form
> needs. It is the only Round-2/Study-3 document allowed to change between
> freeze and registration (to receive the registration URL, a pre-declared
> fill-in, not a deviation).

## What is being registered

**Study 3** (public name) — *the v2.0.0 audit*: does the revised standard
(v2.0.0, built from Studies 1–2's findings) improve on the version those
studies measured (v1.8.0), on the frozen journey unit, per agent, with
publication unconditional on outcome. Lineage: Study 1 (osf.io/pg6r5)
registered the version-delta *question* as exploratory; this study
registers the version comparison as its own primary study. Technical
directory: `benchmark/round2/` (the second round of the journey benchmark
line; kept for path stability).

Protocol: [`PROTOCOL.md`](PROTOCOL.md) — frozen 2026-08-30, sha256 below.

## Frozen snapshot (sha256)

| File | sha256 |
|---|---|
| `PROTOCOL.md` | `5233c4edc576ac713efd8ddaa5cac60fd26cf6e7b4d2c2e2a6d6530866015cc6` |
| `PILOT.md` (pre-freeze journal, incl. both pilots and the tool-runnability amendment) | `8ece00da15247af7c33dfb22274a08efc62cdda5ad8265fcb99b17c6dccd8b4a` |
| `RULERS.md` + `rulers.py` (rulers 1–3/5, floors, kill class) | `rulers.py`: `d9c067b824debd83c034c3dee8ab315235facc968e35c0d7ada137f6cc5508f2` |
| `CLASSIFIER-v2.md` + `classifier_v2.py` (ruler 4, adversarially verified twice) | `classifier_v2.py`: `49055cc6ba2c642ff02d8d82f7149d51e791e53e7bb71c01be6c738f0af8eb66` |
| `fixtures/consistency/` (40 held-out fixtures, all files concatenated in path order) | `69a31efacaa9bb1728cb65b5d5f846617245b2e67ee44fb53a023d8c8e68af46` |
| `run.py` (collection runner) | `0786bcd1884a442ed9c7aec887061116e289c251801211888f9cf5174eb43b09` |
| `analyze.py` (registered analysis) | `b80a74b42e398d40fc25c2d911ff4ec1c8fdc0bf501982c99b6d7a402a45f4a0` |
| `build_home.py` (sanitized-HOME builder, incl. the single tool grant) | `b2ad17b253778d6153a214e706952d4e4b77fd17a88fb1a4478e9ef4bd323653` |
| Sensitivity ancestor `../study2/classifier.py` (untouched) | `485d4064…` (recorded at its own freeze) |

## Treatments (per-condition, from `git archive`, path-order concatenation)

| Condition | Tag | sha256 |
|---|---|---|
| D18 | `v1.8.0` | `a6dc0d78991942ba17ae00e2e4706b927bc134286fc723dc17d89ac44e53aab0` |
| D20 | `v2.0.0` | `bf8986b613c9197956b308ae6d9cd58b771633a1c4c187da8be59133b99754c5` |

## Agents, versions to pin, environments

| Agent | Client version (pin) | Sanitized HOME manifest (sha256) | Measured D20 path |
|---|---|---|---|
| Claude Code | `2.1.237 (Claude Code)` | `claude-code-2/MANIFEST.json`: `bb288b2133619561fc673865133c0327cbf843c8ffa6dca254642e508f1e72d1` | **tool** (`tools/contrast-check.py` under the narrow grant; formula as the standard's fallback) |
| Antigravity | `1.1.22` | `antigravity-2/MANIFEST.json`: `7f9777d956761e59dd7c14c23e9bab334662a6d2f8aff0814f156b6a1e5d4d43` | **formula** (by construction; no equivalent narrow grant exists) |

Gate probes: both agents PASS the leakage-symptom audit (journal:
`PILOT.md`). Auto-update note: the runner re-reads the client version
before every run and aborts on mismatch.

## Submission checklist (author)

1. Confirm the working tree matches the hashes above
   (`sha256sum` the files listed; any mismatch = stop, investigate).
2. Create the OSF registration (own project, "Study 3"), attach or link:
   `PROTOCOL.md`, `PILOT.md`, `RULERS.md`, `CLASSIFIER-v2.md`, the four
   `.py` instruments, and this file.
3. Paste this file's hash table into the registration's freeze section.
4. On acceptance: write the registration URL here and into
   `PROTOCOL.md` §Status (pre-declared fill-ins), start `DEVIATIONS.md`
   with the collection-opens entry, and collection may begin (first wave
   per the interleaving rule).

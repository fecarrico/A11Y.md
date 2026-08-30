# Rulers 1–3 & 5 — frozen definitions, and the kill-class derivation

> Status: **draft — frozen when the protocol freezes; hashes recorded here.**
> Executable judge: `rulers.py` (stdlib-only). Its `--self-test` reproduces
> every Round-1 published number cited below from the published dataset —
> a definition that cannot reproduce the published reading is a defect in the
> definition, found before the freeze. Ruler 4 (consistency) is specified
> separately in `CLASSIFIER-v2.md`.

Impact filter for all rulers: axe **critical + serious**, axe-core 4.13.0
(frozen with the verifier). Run unit: one journey = one 7-screen session,
`agent__journey__COND__runN`.

## Ruler 1 — screens with error (`rulers.py screens`)

**Serves:** the person navigating. Each distinct violated rule counted once
per screen it appears on (screen×error pairs), summed per condition.
*Construct qualified in the registration: the machine-detectable layer only
(axe-class coverage 30–57% in the literature).*
Self-test anchor: Round 1 antigravity A/B/D = **33/13/38** — including the
D-loses fixture (D 38 > B 13) the protocol requires.

## Ruler 2 — wrong decisions (`rulers.py decisions`)

**Serves:** the maintainer fixing. Distinct violated rules **per journey**,
summed per condition. Each journey is an independent project: the same wrong
rule in two journeys is two decisions; within a journey it is one, however
many screens repeat its mold.
Self-test anchor: antigravity A/B/D = **9/11/8**. This is the ruler whose
prose definition drifted in Round 1's write-up; the executable definition
above is the one that reproduces the published table, frozen here.

## Ruler 3 — clean journeys (`rulers.py clean`)

**Serves:** the team shipping. Journeys with zero critical+serious
violations, per condition. **Descriptive only** — base rates printed, never
a contrast headline. Self-test anchor: antigravity A/B/D = **0/5, 0/5, 2/5**.

## Ruler 5 — flagged elements (`rulers.py elements`)

**Serves:** the auditor. Total flagged nodes (critical+serious), per
condition. Registered since Round 1. Self-test anchors: antigravity A/B/D =
**167/42/144**; claude-code = **369/0/0** — the antigravity D-loses fixture
(D 144 > B 42) again in the suite.

## The floor panel (`rulers.py floors`)

Per-obligation classes (axe rule ids, frozen):

- `image-alt`: `image-alt`, `input-image-alt`, `role-img-alt`, `svg-img-alt`, `area-alt`
- `label`: `label`, `select-name`, `form-field-multiple-labels`, `aria-input-field-name`
- `color-contrast`: `color-contrast`

Read by `analyze.py` under the canonical panel's rules (floors, the contrast
bet). Self-test anchors: contrast in 3/5 antigravity D journeys, 0/5
claude-code D; image-alt and label at zero in all D journeys.

## Kill-criterion class list — derivation (axe-core 4.13.0)

The kill criterion operationalizes v2.0.0 §6's anti-pattern **Half-Climbed
ARIA Ladders**: a composite pattern *announced* (a container role or a
role-bearing item) whose required structural rungs are *not completed*. The
class list is every axe 4.13.0 rule whose failure condition is exactly
"announced structure, missing rung" — nothing else:

| Rule | Rung it detects | Why it is the same ladder |
|---|---|---|
| `aria-required-parent` | role-bearing child outside its required container | the child announces a composite pattern the parent never completed (Round 1's real instance: `li` with implicit `listitem` inside `role="menu"`) |
| `aria-required-children` | composite container without its required owned children | the container announces the pattern and stops climbing (Round 1: the 7-screen children rule) |
| `listitem` | `li` outside `ul`/`ol` | the native-HTML rung of the same ladder — list announced by the item, container missing |
| `dlitem` | `dt`/`dd` outside `dl` | native rung, description lists |
| `definition-list` | `dl` with invalid children | native rung, container side |
| `aria-required-attr` | role announced without its required state attributes | the *attribute* rung: `role="checkbox"` without `aria-checked` is the same half-climb, in state rather than structure |

**Boundaries, resolved (the two the protocol names):**

- **Native rules are IN.** `listitem`, `dlitem`, `definition-list` flag the
  identical defect expressed without ARIA. Excluding them would let a run
  fail the ladder in plain HTML and pass the kill — a loophole, not a
  boundary. (ARIA 1.2's generic-transparency rule means intermediate
  wrapper `div`s do not trigger any of these — no false ladder from
  legitimate wrappers; the consistency ruler's validity gate applies the
  same reading.)
- **Keyboard/behavior rules are OUT.** Rules like `nested-interactive`,
  focus-order or key-handling failures are *behavioral* defects of a
  completed structure, not an announced-but-unfinished structure. §6's
  anti-pattern is structural; the kill class stays structural. Behavioral
  failures remain fully counted by rulers 1/2/5 — out of the *kill*, not out
  of the study.
- Also considered and excluded: `aria-allowed-attr`, `aria-valid-attr-value`,
  `aria-roles` (wrong usage, not incomplete announced structure) and
  `list`/`aria-allowed-role` (container-side wrong-usage variants). Each is
  still counted by rulers 1/2/5 at its own impact level.

**Application (verbatim from the protocol):** binary; zero appearances of the
class in all D20 `verify/*.jsonl`, reported WITH the 2×2 table against D18
fresh (if D18 also zeroes, the zero evidences the client era, not §6 —
stated). Base rate printed: 1/10 Round-1 D journeys carried the ladder;
P(zero in 10 | no change) = 0.9¹⁰ ≈ 0.35. Judge: `rulers.py kill` +
`analyze.py` panel.

## Freeze

`sha256sum rulers.py` and this file's hash enter the registration package.
After the freeze, any change is a dated `DEVIATIONS.md` entry.

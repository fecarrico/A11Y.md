# Deviations from the pre-registered protocol

> Every departure from [`METHODOLOGY.md`](METHODOLOGY.md) as registered ([osf.io/pg6r5](https://osf.io/pg6r5)), dated, with what changed and why. Deviations are documented, never hidden — that is the entire point of pre-registering. Newest first.

---

## 2026-09-07 — Extension arm (Arm 1-ext) on an OpenAI-compatible endpoint: three transport differences, declared before collection

- **Registered text:** the Arms table registers Arm 1-ext as *"the identical
  protocol runs on additional models if and when usable API credits exist.
  Extension arms replicate; they do not alter the design. Each extension arm is
  reported separately, never pooled with Arm 1."* NVIDIA's free NIM tier made
  the credits exist; this entry opens the arm.
- **What runs:** the full factorial (10 tasks × 4 conditions × 10 runs) against
  an open-weights model served over an OpenAI-compatible endpoint. Conditions,
  preambles, grounding sentences, task prompts and the tool schema are
  **imported** from the frozen `collect.py` by `benchmark/arm1ext.py` — not
  retyped. Only transport is new.
- **The documents are pinned to what Arm 1 actually read.** Collection runs from
  a worktree at `benchmark-protocol-v2.0`, verified by measurement, not by
  assumption: the 100 condition-D generations logged `A11Y.md` at **36,367
  characters**, which is that commit exactly. HEAD (v2.0.1) is 36,953. Running
  against HEAD would move the model *and* the standard at once, and the arm
  would answer neither question.
- **Transport difference 1 — the endpoint is stateless, so the token co-primary
  is not paired with Arm 1's.** Arm 1 chained calls with
  `previous_interaction_id` and the provider held the conversation; here every
  call resends the whole message list, core file included. Caching exists on
  this provider (the probe's condition-D generation reported 12,672 cached
  tokens) but does not make the two arms comparable. **Token contrasts are
  reported within Arm 1-ext only; any cross-arm token difference is an
  instrument difference, not a model effect, and is not reported as one.**
- **Transport difference 2 — `max_tokens` must be sent.** Arm 1 sent no output
  cap; several NIM models default to a cap below the length of a full page,
  which would truncate generations and read as model failure. Declared harness
  concession: `--max-tokens 16000`, logged per generation, with
  `finish_reason` recorded so truncation is visible **in the data** rather than
  inferred from it.
- **Transport difference 3 — no sampling controls, by symmetry with Arm 1.** The
  provider's defaults apply. The protocol promises a reproducible process, never
  reproducible outputs.
- **What is deliberately NOT replicated:** the sampled human adjudication of 60
  generations (*Measurement* §4). The extension arm is reported on the automated
  outcomes only, and says so wherever it is reported.
- **Known defect inherited on purpose:** `extract_html` still drops css/js
  fences (see 2026-08-23). Raw responses are kept per generation, and
  `verify/repair-artifacts.py` produces the same dual reporting — frozen
  instrument and repaired sensitivity — the Arm-1 repair established.
- **Gate probe, passed (2026-09-07):** one task × four conditions. Condition D
  opened `A11Y.md`, then `references/guide-forms.md` — the §2.1 map row for that
  task — then `guide-cognitive` and `guide-toasts-notifications` (the
  pre-registered *core-rule* / *template* classes). 4/4 cells finished with
  `finish_reason=stop`; the pinned axe pass ran clean over the four pages. Lazy
  loading emerged from reading the core, with no hint in the prompt.
- **Document-tree integrity check before collection (2026-09-07).** The
  worktree was audited against the commit, not assumed equal to it: no local
  modifications (`git status` clean), `docs/en/A11Y.md` SHA-256 identical to
  `benchmark-protocol-v2.0` and different from HEAD, all **32 paths the core
  cites resolve on disk**, and no file present that the core never names.
  Screening runs recorded **0 failed file requests in 28**.
  Noted while auditing: Arm 1 logged **48 failed requests out of 804 (6%)**, and
  none of them is a missing file. Both documents — the standard and the placebo
  alike — name the lifecycle artifacts two ways: bare (`REPORT.md`,
  `PERF-REPORT.md`) in the prose rules, where they are files the agent is told to
  *create in the user's project*, and pathed (`templates/REPORT.md`) in the §2.1
  loading table, where they are files to *read*. A model holding only a read tool
  tries the bare name and misses. It falls 46/2 between the placebo and the
  standard, so the D−C contrast is not skewed by it; it is logged here because
  the same ambiguity in a real agent's filesystem would resolve silently, and
  because it belongs in the post-Study-3 backlog for the standard itself.
- **Model screening before committing the budget (2026-09-07), recorded because
  it is a finding, not housekeeping.** A condition-D-only probe (one task, ~5
  calls per model) across five models, same documents, same frozen sentence.
  All five called the tool; **the standard's §2.1 map was hit by four of five**
  — and the loading behaviour it produced diverged far beyond the pre-registered
  classes:

  | Model | Calls | Files opened | Tokens | Page |
  |---|---|---|---|---|
  | `nvidia/nemotron-3-super-120b-a12b` | 5 | 4 (map + 2 core-rule) | 51,635 | 14,402 chars |
  | `moonshotai/kimi-k3` | 3 | 3 (map + 1) | 23,771 | 8,752 chars |
  | `deepseek-ai/deepseek-v4-pro-0813` | 6 | 6, core re-read once | 77,737 | 2,977 chars |
  | `nvidia/nemotron-3-ultra-550b-a55b` | 13 | 12, incl. 3 templates | 178,661 | **117 chars — no page** |
  | `openai/gpt-oss-20b` | 2 | 1 (core only, **no guide**) | 12,684 | 11,101 chars |

  Two of the five break the mechanism in opposite directions: `gpt-oss-20b`
  reads the core and stops — lazy loading never starts — while
  `nemotron-3-ultra` keeps opening guides and templates until it hits the
  harness's `--max-tool-calls` ceiling and **never emits the page**
  (`finish_reason=tool_calls`). Neither is a tool-calling failure: both called
  the tool correctly. **The standard's loading architecture is model-dependent,
  and that is now measured rather than assumed.** The full factorial runs on
  `nemotron-3-super`, whose behaviour matches the pre-registered expectation and
  whose per-generation cost is predictable; the other four are reported as this
  screening, n=1 per model, exploratory, never as arms.
- **Collection order changed mid-flight, at task 1 of 10 (2026-09-07).** The
  runner swept task-major (all 40 cells of task 1, then task 2…). On a metered
  free tier that is the wrong failure mode: running out of credit would leave
  the last tasks with **zero** cells, and a factorial missing whole tasks cannot
  be analysed as one. Order is now run-major — every task × every condition at
  run 1, then run 2 — so an interruption costs repetitions instead of tasks
  (10×4×8 is still a factorial; 8×4×10 is not). Conditions remain interleaved,
  which is what the registered wave rule asks for. **No collected cell was
  discarded or recollected**; the 37 already on disk are reused by `--resume`.
- **Endpoint instability, measured:** 42 retried HTTP 5xx in the first 99 calls,
  and one generation lost outright after exhausting its retries (recollected by
  `--resume`, since only completed generations are written to disk). Retry
  budget raised 4 → 6 for this reason, logged here rather than tuned silently.
- **First `finish_reason=length` observed** (signup-form, condition D, run 8):
  the model re-read `guide-forms` three times and `guide-buttons` twice across
  10 calls and emitted 75,577 characters before hitting the output cap. The cell
  is retained with its truncation flag — this is exactly what logging
  `finish_reason` per generation was for, and the analysis will decide how
  truncated cells are handled **before** unblinding, not after.
- **The credit budget in this entry was wrong, and the correction is recorded
  rather than quietly edited away (2026-09-07).** Collection opened under the
  premise of a 1,000-call free-tier ceiling, taken from third-party write-ups of
  the NVIDIA API catalog. It is obsolete: NVIDIA staff state on the developer
  forum that **the credit system was removed**, and that catalog access is now
  governed by a per-account request *rate* limit that varies with model and
  traffic, visible in the account menu at build.nvidia.com — not by a total
  quota. So the arm is not budget-bound; it is rate-bound and time-bound, and
  the factorial can complete on this route. The per-condition call rates
  measured over the first 37 generations (A 1.0, B 1.0, C 3.8, D 5.6 → ~1,140
  calls for 400 generations) stand as a cost measurement of the arm, which is
  what they were always worth reporting for.
- **Transient 404s cost 28 generations; recovered, and the runner hardened
  (2026-09-07).** Partway through collection the endpoint began returning HTTP
  404 with an empty body for a model that was present in the catalog the whole
  time and answered normally before and after. The runner retried 429 and 5xx
  but not 404 — a wrong model id returns 404 too — so those generations died on
  the first call: **27 lost to 404, 1 to an exhausted 500 retry**, spread across
  all four conditions (A 6, B 4, C 5, D 2 among the identifiable ones). Nothing
  was written to disk for them, so `--resume` recollects them; the cost is that
  those cells were collected later in wall-clock time than their neighbours,
  which is recorded here rather than smoothed over. 404 is now retried: a wrong
  model id still fails loudly on the first cell, and a transient one no longer
  silently drains the factorial.
- **Two further models, list closed before collection (2026-09-08).** The
  extension is widened from one model to three, with a stated purpose that is
  not "find an effect": **map how the standard behaves across models, so the
  guidance given to developers is model-aware.** The protection against that
  becoming a fishing expedition is this entry — the list is fixed here, each
  model's question is stated in advance, and **all three are reported whichever
  way they come out**, exactly as Study 3's null was.

  | Model | The question it answers |
  |---|---|
  | `moonshotai/kimi-k3` | A second family that executes the mechanism cleanly (3 calls, map hit in screening). Does the effect appear where the model both obeys and loads? |
  | `openai/gpt-oss-20b` | Reads the core and opens **no guide at all**. If condition D still improves structure, the core alone carries the effect and the loading architecture is dispensable in this model; if not, it constrains the finding further. |

  **Excluded, and why it must be said:** `deepseek-ai/deepseek-v4-pro-0813`
  sustains the mechanism but spent 338 seconds on a single call in screening —
  400 generations at that rate is days, not a night. Excluded for wall-clock
  cost, **not for its result**, which is the only acceptable reason to drop a
  model already probed.

  **Kimi K3 abandoned mid-collection for measured infeasibility (2026-09-08),
  not for its result.** Screening said 3 calls per condition-D generation and a
  clean map hit — it said nothing about throughput. In 294 minutes of collection
  the arm produced **7 generations**: 49 minutes each, of which only 39 minutes
  *total* were spent waiting on the model and the rest on backoff from **302
  HTTP 429s**. Projected 320 hours for 400 generations. The cell data collected
  (8 generations) is retained and reported as what it is — an aborted arm — and
  the throughput figures are themselves a finding worth publishing: on this
  provider's free tier the model is not practically reachable for a study of
  this size, whatever its behaviour would have been. A replacement is screened
  and declared before it runs, under the same rule as every other model here.

    **Widened screening, and the finding it produced (2026-09-08).** Losing Kimi
  left the design without a second model that *executes the loading
  architecture*, so four more were screened — this time on three criteria, not
  one: does it open the guides, does it produce a page, **and is it reachable at
  the study's scale** (the column whose absence cost five hours on Kimi).
  Across **nine models screened in total**:

  | Executes the architecture (opens guides) | Reachable? |
  |---|---|
  | `nemotron-3-super` (3 guides, 5 calls) | yes — carries the arm |
  | `deepseek-v4-pro` (4 guides, 6 calls) | no — 338 s on a single call |
  | `kimi-k3` (2 guides, 3 calls) | no — 49 min per generation, 302 × HTTP 429 |
  | `nemotron-3-ultra` (9 guides, 13 calls) | reachable, but emits **no page** |

  | Reads the core, opens **no guide at all** | Reachable? |
  |---|---|
  | `gpt-oss-20b` (page: 11.1k chars) | yes — arm running |
  | `minimax-m3` (page: 17.8k chars) | yes — 44 s |
  | `gemma-4-31b-it` (page: 9.1k chars) | no — 789 s per generation |

  Unreachable outright: `mistral-large-2-instruct` (404, not provisioned for
  this account) and `deepseek-v4-flash` (no response inside 900 s).

  **This screening is itself a result, and arguably a larger one than the arm.**
  Of nine models, four execute the standard's lazy-loading architecture and
  **exactly one of those is usable at this study's scale**; three read the core
  and never open a guide at all. If that ratio holds, **what lives in the
  reference guides does not reach most models**, and the core has to stand on
  its own — a product consequence that no single-model study could have shown.
  Screening cells are n=1 per model, exploratory, and reported as screening.

    **Third arm added and the harness hardened (2026-09-08).** `minimax-m3`
  joins as the third arm: like `gpt-oss-20b` it reads the core and opens no
  guide, and it is fast (44 s in screening). Two models of the same class turn
  "reads the core and does not load" from an anecdote into something that can be
  checked for consistency — and if they diverge, that is equally informative.
  The search stopped here on purpose: continuing to screen until a second model
  that executes the architecture turned up would have been shopping for a
  convenient result. The scarcity **is** the finding.

  Five failure modes were observed during this collection, and each is now a
  mechanism rather than a lesson: (1) transient statuses treated as fatal — the
  retry list now covers 404/408/425/429/529 and every 5xx, after three separate
  codes turned out to mean "busy"; (2) an unreachable model burning hours
  undetected — the runner aborts itself above a configurable minutes-per-
  generation ceiling (default 12, which would have stopped Kimi after three
  generations instead of 294 minutes); (3) generations lost in bulk — abort
  after 15 outright failures; (4) a dead process nobody notices —
  `supervise-arms.sh` restarts a crashed run with `--resume`, up to five times,
  while **respecting a deliberate abort** (exit code 2) and moving to the next
  model instead of retrying a model already judged unusable; (5) invisible state
  — every generation now writes `status.json` with pace, throttle events,
  failures and ETA. Arms remain strictly sequential: two at once would split the
  same rate limit and poison each other's retries.

    **The third arm was retired by its vendor before it could run (2026-09-09).**
  `minimax-m3` was screened on 2026-09-08 and answered in 44 s. When the queue
  reached it the next morning, every call returned **HTTP 410 Gone: "reached its
  end of life on 2026-09-09T09:00:00Z"** — the model was withdrawn five minutes
  before collection started. The circuit breaker aborted the arm after 15
  failures, in 28 seconds. This is the same class of event Study 3 recorded when
  `gemini-3.5-flash` was retired mid-wave: **on hosted endpoints the object of
  study can be withdrawn between screening and collection**, and a protocol that
  runs over weeks has to treat that as normal rather than exceptional.
  **The extension closes with two arms** — `nemotron-3-super` (executes the
  loading architecture) and `gpt-oss-20b` (400/400, zero failures, loads a guide
  in ~16% of condition-D generations). No replacement is sought: the class
  `gpt-oss` represents is already measured, a second member would have bought
  replication rather than a new question, and screening further models after
  seeing the first arm's result is how a closed list stops being closed.

    **Primary outcome stays as registered** (critical+serious axe violations).
  Added as pre-declared exploratory outcomes for all three models, because the
  Nemotron arm showed the primary is blind to them: **structural obedience**
  (`<main>` present, `landmark-one-main`, `page-has-heading-one`, `region`) and
  **moderate-impact violations**, which in Arm 1 fell from 6.80 per page to 0.04
  under condition D — a 99% drop the registered primary barely registers.
- **The registered co-primary nº 2 had never been measured — in any arm
  (2026-09-10).** METHODOLOGY.md §Measurement lists the violation outcome as
  *two* instruments: axe, and a **deterministic per-task checklist mapped to WCAG
  success criteria**. The checklist exists, implemented in `harness/index.html`,
  and was written for a browser driven by hand — so when collection moved to the
  API it was never run, not for Arm 1 and not for the extension arms. It was
  ported here **without being rewritten**: `verify/extract-checklist.py` lifts the
  function verbatim out of the registered harness and `verify/checklist-run.js`
  injects it into each collected page under Playwright. Rewriting it for the new
  context would have produced a similar number measuring something else.

  Pass rate over applicable items, condition A → D:

  | Arm | A | B | C | D | D − A |
  |---|---|---|---|---|---|
  | Gemini (Arm 1) | 67% | 90% | 79% | **92%** | +25 pp |
  | Nemotron 3 Super | 69% | 84% | 72% | **84%** | +14 pp |
  | gpt-oss-20b | 67% | 83% | 72% | **81%** | +13 pp |

  **The standard improves this outcome in all three arms, including the one the
  primary called null.** Item by item the three models move together:
  associated `<label>` ~50% → ~97%, live region **0% → 55–89%**, native
  elements already at ceiling.

  **And one item moves the wrong way in all three: 24×24 px target size falls
  14–23 points under condition D.** Pages written under the standard carry more
  interactive elements, and more of them land under the threshold. This is a
  finding against the standard, produced by the standard's own registered
  instrument, and it is stated here first because that is the only way it is
  worth stating. §6 of the standard sets 48/44/24 px floors by profile; the
  generated pages do not meet them, and neither the core nor `guide-buttons`
  appears to make that stick.

  **This is not outcome switching.** No outcome was added, removed, or promoted:
  the primary remains axe critical+serious, still null on the Nemotron arm. What
  changed is that a registered instrument which had gone unrun for two studies
  was finally run, and it does not agree with the one that was.
- **Second engine run, and the two engines disagree (2026-09-10).**
  METHODOLOGY.md registers a second independent scanner as a robustness check;
  it had never been run. HTML_CodeSniffer (via pa11y, WCAG2AA, `verify/pa11y-run.js`)
  was run over all 400 pages of Arm 1 and all 400 of the Nemotron arm. Errors
  per page, condition A → D:

  | Arm | axe (critical+serious) | HTML_CodeSniffer |
  |---|---|---|
  | Gemini (Arm 1) | 1.71 → 0.61 | 2.27 → 1.59 |
  | Nemotron 3 Super | 0.99 → **0.91** | 1.46 → **0.63** |

  Bootstrap on the second engine (5,000 resamples, seed 20260910): Nemotron
  **D − A = −0.83 [−1.41, −0.24], excluding zero**, while D − B and D − C do
  not; Gemini D − A = −0.68 [−1.65, +0.36], which does not. **The engine that
  found no effect in the Nemotron arm is the registered primary; the engine that
  finds one is the registered robustness check — and it finds a larger effect
  there than in the arm where the primary found one.** Per the registered plan,
  *"agreement between engines is reported; disagreement is reported, not resolved
  by choosing the friendlier engine."* The confirmatory result stands as
  registered: **null on the primary outcome.** This entry is what disagreement
  looks like when it is not hidden.
- **Three independent signals point the same way, and the primary outcome is
  not one of them.** Asked to sanity-check the Nemotron near-tie, three things
  were measured: (a) the second engine above; (b) what is actually in the code —
  `:focus-visible` 0% → **70%**, `aria-live`/`role="alert"` 0% → **61%**,
  `prefers-reduced-motion` 0% → **55%**, associated `<label>` 20% → 39%, skip
  link 0% → 12%, all A → D; (c) page size and testable elements — condition D
  pages are nearly twice as long (11.4k vs 5.9k characters) with more testable
  elements, so **normalised violations per 100 elements read 26.8 (A) vs 23.6
  (D)** even where raw counts tie. axe's critical+serious rules largely do not
  test focus visibility, reduced-motion, or the presence of a live region — the
  three places this model changed most. The finding is not that the standard
  failed on Nemotron; it is that **the registered primary outcome is measuring
  the wrong part of what the standard does to this model.** All of (b) and (c)
  are exploratory and labelled as such.
- **Nemotron 3 Ultra retested with the harness ceiling doubled, still out
  (2026-09-10).** Its screening failure — 13 calls, no page — could have been an
  artefact of our `--max-tool-calls 12`, inherited from Arm 1 where the ceiling
  was never reached. Retested at 25: **no generation completed within 900
  seconds.** The exclusion holds, now for throughput rather than for a limit of
  ours. Worth stating because the first reading blamed the model for something
  the instrument might have caused.
- **The published analysis scripts did not run from a clean clone
  (2026-09-10).** Found while regression-testing the extension's changes: both
  registered analysis scripts resolved their default input paths to files that
  do not exist — `robustness.py` had one `.parent` too many (pointing at the
  repository root instead of `benchmark/`) and `confirmatory.py` was missing the
  `runs` segment entirely. Present since they were published in #42. **The
  Study-1 figures themselves are unaffected** — they were produced by these
  scripts run from a working directory where the paths happened to resolve, and
  both now reproduce the published `summary.json` and `confirmatory.json`
  **exactly**: same n, same per-condition distributions, same contrasts, same
  IRRs. What was broken was the promise in `analysis/README.md` — *"anyone can
  rerun both against the published dataset without re-collecting anything"* —
  which was false for anyone who tried. Paths corrected; the reproduction is the
  test that they are right. A reproducibility package nobody re-ran from scratch
  is a claim, not a guarantee, and this one went eleven days unchecked.
- **Instrument audit after collection, run adversarially (2026-09-08).** Before
  reading anything into the arm's null result, the harness was audited against
  the possibility that the null is ours. What held: axe **4.13.0 in both arms**,
  same pinned build, same runner; conditions A and B logged **zero file reads
  and exactly one call per generation**, so the tool never leaked into the
  conditions that must not have it; the documents were the pinned commit
  throughout; and where a response carried several fenced blocks, the extractor
  chose the complete document in **8 of 8** cases.
- **What the audit found, and it is ours: 13 cells are not pages (2026-09-08).**
  In 11 condition-C cells and 2 condition-D cells the model **asked a question
  instead of generating** — reading the placebo's profile table and replying
  *"which performance profile governs this project?"* — and `extract_html`'s
  fallback wrote that prose to a `.html` file, where axe scored it (≈2 serious
  each, from a fragment with no lang and no title). Arm 1 carries the same
  defect in 2 cells, so it is inherited, not introduced. **Impact, measured
  rather than assumed:** excluding non-pages moves condition C from 1.10 to
  0.99 mean critical+serious violations and D from 0.93 to 0.91 (A and B
  unaffected); Arm 1's C moves 1.22 → 1.20. **The registered conclusion does not
  change — the arm is null either way.** Following the precedent set by the
  2026-08-23 repair, affected outcomes are reported **under both versions**, and
  a cell that is not a page is counted in the completeness outcome instead of
  being silently averaged into the primary one. A model that answers a
  generation task with a clarifying question is data about the model, not noise.
- **Generations that produce no page: the inherited rule, made explicit
  (2026-09-08).** Two condition-D cells (`file-upload` run 2,
  `async-save-with-toasts` run 4) opened 13 files, hit the harness's tool-call
  ceiling and emitted **zero characters** — the same failure the model screening
  found in `nemotron-3-ultra`, now observed in the model carrying the arm. Arm 1
  had one such cell of 400. The registered analysis already excludes them:
  `analysis/robustness.py` keeps only generations with `output_chars > 0`. That
  rule is inherited unchanged, and stated here rather than left implicit in
  code, with the consequence spelled out: **an empty generation cannot score
  zero violations by having nothing on the page.** The count of page-less
  generations per condition is reported as a completeness outcome alongside the
  violation results, since a standard that makes a model read until it runs out
  of turns is a cost the violation count would otherwise hide.
- **Two malformed file requests, logged as model behaviour (2026-09-07).** In
  two condition-D generations (`product-card-grid` run 1, `image-carousel`
  run 3) the model asked the tool for **`A11Y11Y.md`** — the standard's own
  filename corrupted mid-token. The harness answered "no such file", as it
  answers any path that does not resolve, and the generation continued. These
  are counted in the loading-behaviour outcome as failed requests, not dropped:
  a model mangling the filename it was just given is a property of the
  mechanism under test, not noise to be cleaned.
- **What this does not change:** run-major collection order stays (an
  interruption from any cause — rate limiting, endpoint errors, a stopped
  machine — should still cost repetitions rather than tasks), and the OpenRouter
  route stays declared and validated as contingency, unused unless needed.
- **Second free route, declared before it is used (2026-09-07).** If NVIDIA's
  credits run out before the factorial does, the remaining cells collect through
  OpenRouter's free tier (request-metered, 50/day, no payment), on the same
  weights, **pinned to NVIDIA as the serving provider with fallbacks disabled**
  — without that pin the router could serve a generation from a different host
  and the arm would silently mix instruments. Every generation records the route
  it came through (`route`, `endpoint`, and the provider the response reports),
  so a split collection can be shown to be homogeneous instead of assumed to be.
  **Verified before the route was needed (2026-09-07):** the free variant is
  served by NVIDIA itself — the same host as the primary route — and a request
  byte-identical to the collector's produced the same first move, a
  `read_file("A11Y.md")` tool call, at zero cost. (The paid variant of the same
  model routes to DeepInfra and DigitalOcean instead; pinning matters, and an
  early probe of mine failed for exactly that reason before the pin was right.)
  Free-tier ceiling is request-based — 50/day on an unfunded account — so the
  runner carries `--daily-cap` to stop cleanly instead of collecting 429s.
  If the two routes disagree on any outcome, that is reported, not resolved by
  dropping the inconvenient half.
- **Budget, stated up front:** the free tier grants 1,000 credits (≈1 credit per
  call) and the probe projects ~900 calls for the factorial. If credits run out
  mid-collection, `--resume` continues from disk; **a partial factorial is
  reported as partial**, never silently rebalanced across conditions.

---

## 2026-08-23 — Instrument defect found by the human adjudicator: extract_html dropped delivered CSS/JS; mechanical repair + dual reporting

- **Discovery:** during blind adjudication, the adjudicator opened a sampled
  page that rendered unstyled and questioned whether the model had really
  shipped it that way. He was right to: the frozen collector's
  `extract_html()` keeps the largest fenced block of a raw response and
  silently drops the ```css/```js fences delivered alongside. **32 of 400
  Arm-1 artifacts** reference a stylesheet the model DID write and the
  extractor discarded — verified against every raw response (32/32 contained
  the CSS; zero cases of the model not delivering).
- **Impact:** those 32 pages were axe-scored and sampled in a state poorer
  than the model's actual deliverable. Arm 2 is unaffected (its runner always
  assembled local assets — an instrument asymmetry this repair harmonizes).
  Tokens and loading outcomes are untouched.
- **Remedy, blind to condition:** `verify/repair-artifacts.py` — one rule for
  every generation: css/js fences from the generation's own raw response are
  injected back (content only added, never removed, repair marked by comment).
  Originals untouched in `runs/html`; repaired copies in `runs/html-repaired`.
  **Every affected outcome is reported under both versions** — the frozen
  instrument and the repaired sensitivity — starting with a fresh axe pass on
  the repaired 32.
- **Blind sample:** the 7 affected sampled pages were rebuilt by script
  (content-matched, conditions never printed, map still sealed; filenames kept
  as inherited ids). The target-size pre-pass re-ran on the repaired sample:
  the pending human worksheet is unchanged in size — the repaired pages still
  carry genuinely small styled targets — but the human now judges the true
  deliverable. No mechanically-closed row reopened; no human verdict existed
  yet to preserve.
- **Credit where due:** the defect was caught by the human step the protocol
  insisted on keeping. Sampled human adjudication is not a formality; this
  entry is the proof.

## 2026-08-24 — Dataset published: DOI 10.5281/zenodo.22073026

- The complete dataset of both studies — 454 Study-1 pages with axe reports,
  screenshots and logs; the blind worksheets and their unsealed results; the
  30 Study-2 journeys with screens, reports and the registered analysis; both
  SHA-256 manifests — is published on Zenodo under CC-BY-4.0:
  [doi.org/10.5281/zenodo.22073026](https://doi.org/10.5281/zenodo.22073026).
- Integrity audited on publication day via the Zenodo API: 6/6 files with
  MD5 checksums identical to the local originals. Related-work links bind the
  DOI to both registrations (osf.io/pg6r5, osf.io/mqs7x) and the repository.
- With this, every claim in the reports is backed by a citable, immutable,
  independently hosted copy of the raw data. Raw data never enters git —
  exactly as registered.

## 2026-08-23 — SC 2.5.8 adjudication: the registered machine/human split, applied

- **Registered text:** MANUAL checklist items are *"automated where a scripted
  browser can decide them; the remainder adjudicated by a human."*
- **What ran:** `verify/target-prepass.js` measured every visible interactive
  target on the 60 blind-sampled pages (Playwright, 1280×900). "No target
  below 24×24 CSS px exists" is machine-decidable: **41 of 52 target-size rows
  closed mechanically as N-A**, each stamped as such in the worksheet's
  observation column. The 11 pages that do contain sub-24px targets go to the
  human adjudicator with a factual measurement report
  (`adjudicacao-alvos-pequenos.md` — shapes, counts, examples); the exception
  judgments the SC delegates to a person (equivalent control, inline,
  essential) remain human, exactly as registered.
- **Blinding intact:** the script sees content hashes, never conditions; the
  sealed map stays sealed. Modal-focus rows are untouched — keyboard
  interaction with focus-return judgment stays with the adjudicator.

## 2026-08-18 — Antigravity: first attempt aborted; ambient-memory contamination found; fresh profile required

- **What happened:** the first two runs (signup-form, conditions A and D, run 1) ended `status=ERROR` with zero files created — and their transcripts show something worse than a flag problem: **condition A went looking for A11Y.md.** The agent resolved paths inside the author's repository and cited the standard, WCAG 2.2 AA and the author's own UX rules — in a fresh workspace, on a bare task prompt that carried no rule at all.
- **Where it comes from:** Antigravity keeps persistent profile-level memory and product-level rules. A follow-up probe **with `--new-project`** (outside the dataset) still described a brand-new empty directory as "structured around accessibility guidelines (A11y)" and cited `docs/en/A11Y.md` by path. On the standard author's machine the standard is *ambient* — the product carries it into sessions that never asked for it. An A cell collected in that profile would not be an A cell.
- **Why this differs from the other agents:** the audit entry below documents that the live profile's global agent config contains zero accessibility content for Claude Code and Codex — running them in the live environment is "declared, not sanitized" working as intended. For Antigravity the live environment contains **the treatment itself**; that philosophy cannot cover it.
- **Declared remedy (before any retained run):** the Antigravity cell collects under a **fresh OS profile** — `HOME` pointed at an empty directory, one-time authentication, locally verified to isolate profile state — with `--new-project` added to every invocation. The asymmetry with the other two agents is declared here. **Gate:** a clean-profile probe must answer "what do you know about this project?" without referencing the standard; if ambient knowledge survives a fresh profile (server-side memory), the extension is **abandoned, and this entry closes with that outcome** — a declared, unexecuted extension with its reason on record.
- **Data handling:** the two ERROR runs stay in the collection log as failed records (precedent: the truncated Arm 1 cell). Nothing was produced, nothing is retained; `--resume` recollects them under the fixed invocation.

## 2026-08-18 — Third agent for the ecological arm: Antigravity CLI (declared before any run; motivated by results)

- **What is added:** a third agent in Arm 2 — the Antigravity CLI (`agy`), official Google client, included in the author's existing Google AI Pro subscription ($0 marginal, the same criterion that qualified Claude Code and Codex). Same three tasks, same conditions A and D, same n=3, same 40-minute clock: 18 runs.
- **Why, stated plainly:** an external methodological review of the (unpublished) report flagged that Arms 1 and 2 change two variables at once — harness *and* model family — with no shared cell. This addition was decided **after the primary-arm results were final**, and is disclosed as such. The principle that makes it defensible: it creates a new opportunity for the effect to *fail* in a third harness, not a new opportunity for it to succeed. Whatever it shows goes in the report.
- **What the probe found (2026-08-18, outside the dataset):** `agy models` does **not** list `gemini-3.5-flash-lite`, the primary arm's model. Nearest available: Gemini 3.5 Flash. **This cell therefore does not close the harness×model confound — it narrows it** ("same family, adjacent tier"). The strict closure remains Arm 1-ext (the same API protocol on the ecological agents' models), still conditional on research credits.
- **Rule-file test (2026-08-18, outside the dataset):** two marker runs (one in a plain directory, one in a git repository) show the CLI reads **neither `AGENTS.md` nor `GEMINI.md`** in print mode — input token counts unchanged with the files present, marker instructions not followed. Condition D therefore delivers the rule as a **prompt preamble**: the same verbatim Quick Start sentence the rule files carry, with the standard on disk. This makes the cell a declared bridge to Arm 1 (same delivery mechanism, real agent harness) rather than a mirror of the other two agents.
- **Pins:** model `gemini-3.5-flash`; `--effort low` (the flag is a new degree of freedom the other agents do not expose — fixed identically across conditions, chosen as the closest available neighbour to the Lite tier's cost profile); `--mode accept-edits` (the single concession, symmetric with the other agents); `--output-format json`; `--print-timeout 40m`; version logged per run (`agy` 1.1.14 at declaration time).
- **Discipline:** this entry and the matching `ARM2.md` section are committed **before the first retained run**. Collection starts only after merge.

## 2026-08-18 — Repository audit after external review (clarifications; no protocol change)

An independent methodological review of the draft report prompted an audit of verifiable claims. Findings, recorded so they are answered before they are asked:

- **Two OSF IDs:** `osf.io/s2ntw` is the OSF **project**; `osf.io/pg6r5` is the **registration** inside it. The commit that opened collection (`0b37456`) carries the project ID in its title; git history is immutable, so this note is the correction. Every normative file points to the registration.
- **Tool-call ceiling was never reached:** across all retained primary-arm generations the maximum observed is **11 tool calls** (two condition-C generations); the operative ceiling was 12. No generation's loading behaviour was truncated by the instrument.
- **Collector defaults vs. operative invocation:** the frozen `collect.py` still carries v1 defaults (`--conditions A,B,D`, `--runs 3`, ceiling 6). They were overridden in every wave; the operative invocation is logged in the collection pipeline: `--conditions A,B,C,D --runs 10 --max-tool-calls 12`. Defaults were left untouched because the file's hash is part of the registered snapshot.
- **Arm 2 environment, documented:** the user-global `CLAUDE.md` on the collection machine contains **zero accessibility-related content** (checked by keyword sweep), and Arm 2 workspaces were created under the system temp directory, **outside any repository** — no project-level agent config applied to any run. The "declared, not sanitized" clause now has its contents on record.
- **`RUNBOOK.md` marked historical:** it describes the superseded v1 design and now says so unambiguously at the top.

## 2026-08-18 — Confirmatory model operationalized with task fixed effects

- **Registered text:** "negative-binomial mixed regression, violations ~ condition + (1 | task)" — random intercepts per task.
- **What happened:** the analysis stack (statsmodels) offers no frequentist negative-binomial mixed model. With ten task levels, the standard operationalizations are task **fixed effects** or **cluster-robust errors by task**. Both were fit and both are reported: fixed effects as primary, cluster-robust as sensitivity. Where they diverge (D vs A: significant under fixed effects, borderline under cluster-robust), the divergence is reported, not resolved by choosing.
- **Timing caveat, stated plainly:** the operationalization was decided after the robustness-track descriptives (pre-registered as computable pre-model) had been seen. The choice was constrained by software, not by results — but the sequence is disclosed so readers can weigh it.
- **Scripts:** `analysis/confirmatory.py`, environment frozen in `analysis/requirements.txt`, dispersion α profiled by grid (≈3.15), seed-free (the model is deterministic given data).

## 2026-08-16 — Tool-call ceiling raised 6 → 12 via runtime flag; one truncated cell re-collected

- **What happened:** generation 7 of the first retained wave (`destructive-confirmation-modal`, condition C, run 1) requested a seventh file read; the collector's default `--max-tool-calls 6` cut the loop and the generation ended with **zero output characters** — seven quota calls spent on an unusable cell.
- **Response:** the wave was stopped at generation 11, the truncated cell's artifacts were deleted, and collection resumed with `--max-tool-calls 12` on the command line. The frozen `collect.py` is untouched — the ceiling is a documented runtime flag, and the default in the file still reads 6 — but the operative value changed mid-collection, which is exactly the kind of thing this log exists to record.
- **Data handling:** the truncated cell re-collects under `--resume` (its deletion makes it pending again). Its first, truncated attempt remains in the collection log as a failed record; analysis reads generations from disk and never pools zero-output artifacts.
- **Why 12:** the pilot's condition-D generation read 6 files; the control's lazy map plus its three templates make 7+ reads a legitimate path, not a runaway. Twelve bounds a runaway loop at roughly twice the observed legitimate maximum.

## 2026-08-16 — Primary-arm model finalized as `gemini-3.5-flash-lite` after a quota wall

- **Registered text:** Arm 1 is "Gemini API, free tier (current Flash-class model; exact model string and version recorded per call)" — the registration deliberately did not pin a model string.
- **What happened:** the first collection wave started on `gemini-3.6-flash` and hit its free-tier quota at 20 requests/day (AI Studio per-model table; every full-Flash model carries the same 20/day cap). The full design needs ~1,300 calls — two months at that cap. The Lite tier allows 500/day. The arm restarts on **`gemini-3.5-flash-lite`** (current stable Lite, 15 RPM / 500 RPD), verified working with the tool loop via `--probe` before this entry.
- **Data handling:** 3 generations had been collected on `gemini-3.6-flash` (signup-form A, B, C of run 1). They are set aside under `runs/aside-gemini-3.6-flash/` as exploratory material and are **never pooled** with the primary arm. The primary arm's log starts clean.
- **Effect on interpretation:** none beyond what the registration already declared — the model string is recorded per call and named in any report title. A Lite-class model arguably makes the test *harder* for the standard, not easier: smaller models depend more on the quality of their context.

## 2026-08-16 — Collector reordered to interleave conditions (before any retained generation)

- **Registered text:** METHODOLOGY.md §Size — "waves are collected on consecutive days with conditions interleaved (never one condition's block on one day — interface drift must not load onto a condition)."
- **What happened:** the frozen `collect.py` (SHA-256 `258cbfab…` in the registration) built its job list task → condition → run, which collects condition blocks — contradicting the registered text. Caught on the pre-collection `--plan` inspection; the job order now cycles every condition within each task before any condition repeats, runs outermost.
- **Why it is a deviation and not an edit:** the collector's hash is part of the registered snapshot, so any change to it is logged here, even one that *restores* compliance with the registered methodology. The methodology text is normative; the instrument answers to it.
- **Timing:** zero generations had been collected under the frozen ordering.

## 2026-08-16 — Protocol tag is annotated, not GPG-signed

- **Registered text:** "The repository tag marking the frozen protocol is signed."
- **What happened:** no GPG signing key is configured on the collection machine; the tag `benchmark-protocol-v2.0` was created annotated but unsigned.
- **Why it does not weaken the freeze:** the tamper-evident anchor was never the tag — it is the OSF registration itself, which is immutable, timestamped by a third party, and carries the SHA-256 of every frozen file. The tag is a repository-side convenience pointer to the same tree.
- **Remedy if it matters later:** a signed tag can be added over the same commit once a key exists; the hashes in the registration make any rewrite detectable either way.

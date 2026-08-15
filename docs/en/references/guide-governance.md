# A11y Governance & Compliance Strategy

> Scope: Static verification, VPAT strategy, ADA/EAA compliance, EN 301 549, and external audit readiness.

## 0. Where a rule belongs (design principle for this standard)

> **Field evidence (2026-08-01):** in a documented post-mortem of a real project, an agent applied Sections 0–6 correctly and produced no `REPORT.md` or `EXCEPTIONS.md` at all. The artifact that *was* produced (`A11Y-DECISIONS.md`) was the only one named inside a rule of the **AI Behavior Contract**. The variable was not obligation — the other two were already MUST elsewhere — it was **where the filename appeared**.

Agents treat Section 2 as an executable contract and everything else as reference material. Therefore, when extending this standard:

- **Anything the AI must DO** — create a file, refuse an action, check something before proceeding — belongs in the **AI Behavior Contract (Section 2)**, with an explicit trigger event.
- **Sections 7 and the reference guides** carry depth, verification detail and rationale — they explain and expand, but must never be the *only* place an obligation exists.
- Prefer **event triggers** ("before any delivery to an end user") over **phase triggers** ("at final delivery"): continuous-delivery projects never reach a phase, so a phase-triggered rule never fires.

## 1. Static Verification (The Engineering Minimum)
Primary verification does not consist of dictating rigid rules in a *specific pipeline*, but holding the development environment (Be it the Dev or the AI running in real-time) accountable for fast static validation tests.
- **Code Standard:** The code *must* necessarily pass through linters or accessibility-focused evaluators (like `eslint-plugin-jsx-a11y` or the `axe` engine) without displaying critical/serious violations before code consolidation.
- **This standard's own tools:** the repository ships two optional, dependency-free scripts in [`tools/`](https://github.com/fecarrico/A11Y.md/tree/main/tools): `verify-a11y.py` runs against **your project** — checking that the artifacts exist, that `REPORT.md` is newer than the last interface change, and that the source is free of the Section 6 anti-patterns; `lint-standard.py` runs against **copies or forks of this standard**, checking language parity, loading triggers and links. Running them is never a requirement of the standard — `A11Y.md` is portable markdown — but a gate that fails a build is stronger than a rule someone has to remember.
- **Decoupling:** Do not try to "write robust logic for accessible components and try to fix them": adopt agnostic libraries (Headless UI) whenever native HTML semantics do not cover the feature requirements.

### 1.1. Default configuration is not coverage

A clean axe run means "no violation among the rules that were enabled". Two defaults are worth correcting, both found while building this project's own landing page under this standard:

- **Enable the experimental rules that carry a Success Criterion.** `label-content-name-mismatch` detects an accessible name that does not contain the visible text — an **SC 2.5.3 Level AA failure** that breaks voice control — and it ships **disabled by default**, in axe-core and in the browser extension alike. Turn it on: `axe.run(context, { rules: { 'label-content-name-mismatch': { enabled: true } } })`, or check *Experimental rules* in the extension's settings. In the field this rule was what caught an `aria-label` replacing the visible text of a language selector; the default run passed it clean.
- **Resolve the linter × engine conflict instead of silencing it.** `scrollable-region-focusable` (axe) requires a focus stop on a container the user can scroll but not tab into; `no-noninteractive-tabindex` (`eslint-plugin-jsx-a11y`) flags that exact `tabIndex`. Following both literally is impossible, and the path of least resistance — disabling the ESLint rule — removes a real guard. Configure it instead:
  ```jsonc
  // .eslintrc — allow the focus stop axe requires, keep the rule everywhere else
  "jsx-a11y/no-noninteractive-tabindex": ["error", { "roles": ["region"], "tags": [], "allowExpressionValues": true }]
  ```
  And remember the axe rule is **conditional**: the focus stop belongs only on regions whose content actually overflows. Applying it to every scroll container adds tab stops that lead nowhere (see *Focus Traps Nobody Asked For*, `A11Y.md` §6).

> **A CI gate is a form of independent verification.** *Independent Verification* (`A11Y.md` §2) asks that the evidence not be authored solely by the agent that wrote the code. A pipeline check satisfies that for the mechanical layer by construction — it runs outside the session, against the artifact, with no memory of the decisions that produced it. It does not, however, satisfy the human checkpoints, and it does not raise the report's declared independence level for anything a machine cannot test.

### 1.2. Independent Verification — who signs the evidence

*Independent Verification* (`A11Y.md` §2) exists because self-review re-runs the reasoning that produced the defect. The evidence, in order of proximity to this standard:

- **This standard's own case (1.6.0):** an `aria-controls` pointing at a non-existent id survived the generating agent, axe **and** Lighthouse, and surfaced only in an independent test — [a11y-md-ai-test](https://github.com/mjepis7/a11y-md-ai-test), by Maria Eduarda Iwashita, run against a pre-1.0.0 version by someone with no stake in the result.
- **The general result from code review at large:** models find more bugs in code written by another model than in their own (Greptile, [*Models are worse at reviewing their own code*](https://www.greptile.com/blog/model-inversion), 2026-07-21 — two 500-PR datasets, one authored by Claude Code and one by Codex, ~1,500 ground-truth comments; GPT reached 62% recall on Claude-authored PRs against Claude's 53.7% on its own, with the inverse pattern on Codex code).

**What each level buys:**

- **cross-agent** — a different model breaks the correlation between the defects generated and the defects looked for. The strongest form, available wherever two agents are.
- **fresh-context** — the same model *without the conversation that produced the code*. What is removed is the memory of having decided; a practical approximation of cross-agent, and the floor everywhere, because it costs a new chat over the same project, never a new tool. Integrated vibe-coding environments and single-session IDEs have it too.
- **self-reported** ⚠️ — honest and visible, never sufficient: it is the generating agent re-running the reasoning that produced the code, which is the failure mode the rule exists to break. Ceiling: ⚠️ CONDITIONAL.

**The declaration is trust-based, and still not theater.** The standard cannot observe which session verified — but the `REPORT.md` field names *who* did, which makes the claim auditable by a human, and `verify-a11y.py` enforces the ceiling mechanically (a self-reported ✅ PASS fails the gate). None of this replaces the human checkpoints: a second agent can resolve a reference between two files; it cannot hear a screen reader, judge whether an image is decorative, or confirm a caption.

## 2. Descriptive Evidence (The "Why")
When creating custom complex widgets, the developer (or AI) must include a comment block explaining the accessibility strategy:
- What is the focus order?
- How are states communicated?
- What is the fallback for non-JS environments?

## 3. Visual Language Constraints
- **Color:** Never communicate state (Valid/Invalid/Warning) using only color. An accompanying icon or text description is mandatory.
- **Contrast:** Brand colors that fail 4.5:1 ratio must be adjusted for UI elements or paired with a high-contrast alternative.

## 4. Audits and Legal Compliance (ADA/EAA Readiness)
To prepare subsystems for external certification and audit:
1. **Inventory:** Consolidate a list or storybook of the key visual components of the flow and their behaviors with assistive technologies.
2. **Keyboard Path:** Prevent Dead-ends through clear and planned mapping of the visual layout order (`Tab`).
3. **Standard Audit:** The checklist in [**`templates/REPORT.md`**](../templates/REPORT.md) **MUST** be operated as "Definition of Done" **before any delivery to an end user** — a published build, a deploy, a shared artifact, a tag — not only at a "final delivery" that continuously delivered projects never reach (see *Release Evidence*, `A11Y.md` §2).
4. **One living report, not one per publish:** the report tracks the **interface**, not the release count. If nothing changed since the last one, it stands as is. When the interface changes, update the date and revisit only the entries that change affects: any checkpoint whose evidence the change invalidates goes back to `[ ]` or `[~]` until re-verified. Human checkpoints (screen reader, color simulator) keep their `[x]` and the date of the session that produced them, and are re-run when the flow they covered changes.

## 4.1. Formal evaluation (WCAG-EM) — when the project will be audited

Not every product goes through an external audit, and this standard does not assume it will. But **when it does**, `REPORT.md` alone is not the right instrument: it tracks a *feature*, while an audit evaluates an *entire site or application*. The two are complementary, and the gap between them shows up late — usually when the Accessibility Declaration required by Section 6 has to be issued.

Where a formal audit, third-party evaluation or public declaration is on the horizon, anchor the work in the W3C's official methodology, [WCAG-EM](https://www.w3.org/TR/WCAG-EM/):

1. **Define the scope:** which URLs/screens, which target level, which accessibility-supported technologies.
2. **Explore:** identify page types, essential functionality, technologies in use.
3. **Select the sample:** structured pages (one of each type, plus complete flows) plus a randomly selected sample — auditing "the main pages" without a declared sampling method is not an evaluation, it is an opinion.
4. **Audit the sample** against every criterion at the target level.
5. **Report:** use the W3C-WAI [Evaluation Report Template](https://www.w3.org/WAI/test-evaluate/report-template/) or the [WCAG-EM Report Tool](https://www.w3.org/WAI/eval/report-tool), which produce the format auditors and regulators expect to read.

The project's accumulated `REPORT.md` files are the **provenance evidence** for that audit: they show what was verified, when, by whom, and what stayed open. A repository with a history of reports arrives at formal evaluation with ballast; one without starts from zero.

## 5. Reporting & Liability (VPAT Strategy)
Projects targeting the US market must be Section 508 compliant:
- **VPAT Creation:** Maintain a technical document that records which WCAG criteria are fully or partially supported.
- **Traceability:** Each major feature must have a comment in the code citing which WCAG criterion is being respected.

## 6. European Compliance (EN 301 549)
For EAA compliance:
- **Interoperability:** Ensure the software does not prevent the use of third-party assistive technologies.
- **Accessibility Declaration:** Maintain a public accessibility page describing the features and the achieved compliance level.

## 6.1. Brazilian Compliance (ABNT NBR 17225 / LBI)

For products serving a Brazilian audience:

- **ABNT NBR 17225:2025** — *Accessibility in web content and applications: requirements* — is the Brazilian technical standard, published in March 2025. It gathers 146 guidelines across requirements and recommendations, aligned with WCAG, and includes a list of critical items (captchas, facial recognition, assistive navigation, contrast, spacing, files, third-party content, custom components).
- It provides the technical ballast for **article 63 of the Brazilian Inclusion Act (Lei 13.146/2015)**, which mandates accessibility for the websites of public bodies and of companies headquartered or commercially represented in the country.
- **Practical effect on this standard:** WCAG 2.2 AA conformance covers most of the requirements, but the Brazilian standard's list of critical items is the acceptance checklist in Brazilian public procurement. If the project has that destination, declare it in `REPORT.md` alongside the compliance profile.

## 7. Compliance Versioning
Current focused standard: **WCAG 2.2 AA** | **EN 301 549** | **ABNT NBR 17225** (Brazil, where applicable).
Deviations from legal requirements due to severe UI/UX, native platform, or base architecture limitations, **MUST** be justified mandatorily using the matrix file on the page: [**`templates/EXCEPTIONS.md`**](../templates/EXCEPTIONS.md). All these points must have compensatory actions.

## 8. External Standards & Engines
For real-time AI context and developer reference, adhere to these canonical industry standards:
- **WAI-ARIA APG:** [https://www.w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/)
- **eBay MIND Patterns:** [https://ebay.github.io/mindpatterns/](https://ebay.github.io/mindpatterns/)
- **Deque Axe Core:** [https://github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)

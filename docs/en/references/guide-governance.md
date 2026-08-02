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
- **Decoupling:** Do not try to "write robust logic for accessible components and try to fix them": adopt agnostic libraries (Headless UI) whenever native HTML semantics do not cover the feature requirements.

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

## 5. Reporting & Liability (VPAT Strategy)
Projects targeting the US market must be Section 508 compliant:
- **VPAT Creation:** Maintain a technical document that records which WCAG criteria are fully or partially supported.
- **Traceability:** Each major feature must have a comment in the code citing which WCAG criterion is being respected.

## 6. European Compliance (EN 301 549)
For EAA compliance:
- **Interoperability:** Ensure the software does not prevent the use of third-party assistive technologies.
- **Accessibility Declaration:** Maintain a public accessibility page describing the features and the achieved compliance level.

## 7. Compliance Versioning
Current focused standard: **WCAG 2.2 AA** | **EN 301 549**.
Deviations from legal requirements due to severe UI/UX, native platform, or base architecture limitations, **MUST** be justified mandatorily using the matrix file on the page: [**`templates/EXCEPTIONS.md`**](../templates/EXCEPTIONS.md). All these points must have compensatory actions.

## 8. External Standards & Engines
For real-time AI context and developer reference, adhere to these canonical industry standards:
- **WAI-ARIA APG:** [https://www.w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/)
- **eBay MIND Patterns:** [https://ebay.github.io/mindpatterns/](https://ebay.github.io/mindpatterns/)
- **Deque Axe Core:** [https://github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)

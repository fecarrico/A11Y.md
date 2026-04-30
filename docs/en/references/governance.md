# A11y Governance & Compliance Strategy

This document defines the evidence and verification process required to maintain a "Certification Ready" status.

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
3. **Standard Audit:** In case of final delivery, the checklist in [**`templates/REPORT.md`**](../templates/REPORT.md) *must* be operated as "Definition of Done".

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

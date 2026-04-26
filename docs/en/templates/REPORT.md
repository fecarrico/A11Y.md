# A11y Verification Report (Template)

This report compiles the compliance evidence for a given *Feature*, ensuring its development reached the "Certification Ready" definition.

---

## 📌 Validation Context
- **Feature/Epic:** [e.g., Integrated Checkout]
- **Test Date:** [MM/DD/YYYY]
- **Compliance Status:** [✅ PASS | ⚠️ CONDITIONAL (Passes with Exceptions) | 🚫 FAIL]

## 1. Technical Verification (Automated & Semantics)
Evidence obtained via static validators to ensure a structural technical baseline.
- [ ] **Axe-Core / Lighthouse:** Zero "Critical" or "Serious" violations? *(Attach print or score - e.g., Score 98)*
- [ ] **HTML Semantics:** Appropriate replacement of generic `div`s with interactive endpoints (`button`, `a`, etc.)?
- [ ] **Heading Hierarchy (H1-H6):** Respected with no level skips?

## 2. Tab Order and Focus Management
Validation purely by keyboard (without mouse usage).
- [ ] **Focus Indicator:** The Focus Ring was never suppressed and meets the visual contrast requirement (minimum 3:1)?
- [ ] **Logical Navigation:** Does the `Tab` key follow the visually correct order of the interface?
- [ ] **Captured Focus (Modals/Overlays):** When opening modals, is the focus trapped inside the component and can it be closed via the `Escape` key?

## 3. Behavior and Task Return
Critical functional paths and Screen Reader validation.
- [ ] **Screen Reader Test:** Performed the main task using VoiceOver/NVDA?
- [ ] **Status Change (`aria-live`):** Are form errors, loading states, or non-visual updates correctly announced?
- [ ] **Form Filling:** Correctly related labels (`for` and `id`) in all inputs?

## 4. Visual Perception and Comprehension
Tests validating contrast and visual structure (color-independent).
- [ ] **Text & UI Contrast:** Do all texts have a 4.5:1 ratio and essential components 3:1?
- [ ] **Redundancy:** Errors and alerts do not convey information exclusively through color *(e.g., they always use Color + Icon + Text)*.
- [ ] **Scale / Zoom:** When zooming in by 400%, does everything remain operable without blockages (screen overrides)?

---
## 📝 Assessment Notes or Known Blockers
*Describe whether any exception behavior was detected or what measures were opened in `EXCEPTIONS.md`*

- **Note 1:** [Write note...]
- **Note 2:** [Write note...]

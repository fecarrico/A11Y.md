# A11y Compliance Profiles

> **Scope:** AI Generation & Auditing

Accessibility is not a monolith. While **WCAG 2.2 AA** is the industry and legal standard, different stages of a project demand different levels of rigor.

This guide details the three compliance profiles supported by the `A11Y.md` ruleset.

> [!NOTE]
> **Normative vs House Rules.** Each profile mixes two layers: **WCAG Success Criteria** at its target level (cited by SC number — skipping one requires `EXCEPTIONS.md`) and **House Rules†** — this standard's stricter ergonomic policy (marked †; relaxing one is a product decision, recorded in `A11Y-DECISIONS.md`). WCAG defines **no minimum font size** at any level, and Level A defines **no contrast or target-size criteria** — every value in those positions below is a House Rule.

---

## The Profiles

| Profile | Target Standard | Primary Use Case | Focus |
| :--- | :--- | :--- | :--- |
| **🛡️ Shield (AAA)** | WCAG 2.2 AAA | Regulated industries, specialized software | Ultimate inclusivity, zero barriers |
| **⚖️ Standard (AA)** | WCAG 2.2 AA | Production web apps (Default) | Legal compliance, broad usability |
| **🚀 Launchpad (A)** | WCAG 2.2 A | MVPs, internal tools, prototypes | Absolute minimum baseline |

---

## 1. 🛡️ Shield Profile (Level AAA)
*The highest standard of web accessibility.*

**When to use:** Applications for government, healthcare, education, or specialized audiences with severe disabilities.
**AI Instruction:** `"Apply Shield Profile (AAA)"`

### Key Requirements (Beyond AA)
- **Contrast (SC 1.4.6):** Text must have a **7:1** ratio against its background. Large text (18pt+) must have **4.5:1**. UI components remain at 3:1 (SC 1.4.11 — WCAG has no AAA non-text contrast criterion).
- **No Exceptions for Density:** Even tiny badges or labels must meet the 7:1 ratio.
- **Targets (SC 2.5.5):** Clickable elements must be at least **44×44px** — the AAA minimum, with the SC's own exceptions (equivalent control, inline-in-text target, user-agent control, essential presentation). **House Rule†:** design to **48×48px** (Material norm) and allow no density exceptions under Shield.
- **Focus (SC 2.4.13 + House Rule†):** The focus indicator must be highly visible — solid 2px outline with 3:1 contrast against the background (House Rule; the SC's normative 3:1 is measured between the focused/unfocused states) — and not rely on default browser styles.
- **Timeouts:** Users must be able to complete tasks without arbitrary time limits, or have mechanisms to easily extend sessions.

---

## 2. ⚖️ Standard Profile (Level AA)
*The global benchmark for legal compliance (ADA, EAA).*

**When to use:** This is the **default**. Use for any production software, public-facing website, or commercial product.
**AI Instruction:** `"Apply Standard Profile (AA)"`

### Key Requirements
- **Contrast (SC 1.4.3, 1.4.11):** Text must have a **4.5:1** ratio. Large text must have **3:1**. UI elements (borders, icons) must have **3:1**.
- **Targets (SC 2.5.8):** Clickable elements must be at least **24×24px** — the AA normative floor, with exceptions for inline links and spaced targets. **House Rule†:** design to **44×44px** (Apple HIG / Material norm).
- **Focus (SC 2.4.7):** Focus must be clearly visible.
- **Semantic HTML & ARIA:** Strict adherence to APG patterns for complex components.
- **Responsiveness (SC 1.4.4, 1.4.10):** Text must resize to 200% without loss of content or function, and content must reflow at 320 CSS px width (≈400% zoom) without two-dimensional scrolling.

---

## 3. 🚀 Launchpad Profile (Level A)
*The absolute floor. Below this, the software is considered broken.*

**When to use:** Rapid prototyping, internal admin panels with controlled audiences, or initial MVP builds.
**AI Instruction:** `"Apply Launchpad Profile (A)"`

> [!WARNING]  
> The Launchpad profile does **NOT** mean "no accessibility". It still requires semantic HTML, keyboard operability, and screen reader support. It only relaxes strict visual criteria.

### Relaxed Criteria (Compared to AA)
- **Contrast (House Rule†):** Only a baseline **3:1** ratio is enforced to prevent complete illegibility. (Level A has no contrast criterion — this floor is this standard's policy, not WCAG.)
- **Targets (House Rule†):** Target sizes can be reduced to **24×24px**, provided there is some spacing. (Level A has no target-size criterion; 24×24 mirrors the AA floor of SC 2.5.8.)
- **Typography (House Rule†):** Fonts down to **10px** are tolerated without strict contrast mitigation, though highly discouraged. (WCAG defines no minimum font size.)

### Immutable Rules (Never Relaxed)
- ❌ `div` or `span` with `onClick` (Keyboard trap/unreachable)
- ❌ Missing `alt` on critical images
- ❌ Missing `label` on form inputs
- ❌ Modal without focus trap
- ❌ Changes in state without `aria-live` or role alerts

Any use of the Launchpad profile in production should be documented in the `EXCEPTIONS.md` file as technical debt to be upgraded to Standard (AA).

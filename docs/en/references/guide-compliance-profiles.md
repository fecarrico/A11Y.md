# A11y Compliance Profiles

> **Scope:** AI Generation & Auditing

Accessibility is not a monolith. While **WCAG 2.2 AA** is the industry and legal standard, different stages of a project demand different levels of rigor.

This guide details the three compliance profiles supported by the `A11Y.md` ruleset.

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
- **Contrast:** Text must have a **7:1** ratio against its background. Large text (18pt+) must have **4.5:1**.
- **No Exceptions for Density:** Even tiny badges or labels must meet the 7:1 ratio.
- **Targets:** All clickable elements must be at least **48×48px**. No exceptions.
- **Focus:** The focus indicator must be highly visible (e.g., solid 2px outline with high contrast) and not rely on default browser styles.
- **Timeouts:** Users must be able to complete tasks without arbitrary time limits, or have mechanisms to easily extend sessions.

---

## 2. ⚖️ Standard Profile (Level AA)
*The global benchmark for legal compliance (ADA, EAA).*

**When to use:** This is the **default**. Use for any production software, public-facing website, or commercial product.
**AI Instruction:** `"Apply Standard Profile (AA)"`

### Key Requirements
- **Contrast:** Text must have a **4.5:1** ratio. Large text must have **3:1**. UI elements (borders, icons) must have **3:1**.
- **Targets:** Clickable elements must be at least **44×44px**. Exceptions exist for inline links or when spacing prevents misclicks.
- **Focus:** Focus must be clearly visible.
- **Semantic HTML & ARIA:** Strict adherence to APG patterns for complex components.
- **Responsiveness:** Must support zooming up to 200% without loss of content or function.

---

## 3. 🚀 Launchpad Profile (Level A)
*The absolute floor. Below this, the software is considered broken.*

**When to use:** Rapid prototyping, internal admin panels with controlled audiences, or initial MVP builds.
**AI Instruction:** `"Apply Launchpad Profile (A)"`

> [!WARNING]  
> The Launchpad profile does **NOT** mean "no accessibility". It still requires semantic HTML, keyboard operability, and screen reader support. It only relaxes strict visual criteria.

### Relaxed Criteria (Compared to AA)
- **Contrast:** Only a baseline **3:1** ratio is enforced to prevent complete illegibility.
- **Targets:** Target sizes can be reduced to **24×24px**, provided there is some spacing.
- **Typography:** Fonts down to **10px** are tolerated without strict AAA contrast compensation, though highly discouraged.

### Immutable Rules (Never Relaxed)
- ❌ `div` or `span` with `onClick` (Keyboard trap/unreachable)
- ❌ Missing `alt` on critical images
- ❌ Missing `label` on form inputs
- ❌ Modal without focus trap
- ❌ Changes in state without `aria-live` or role alerts

Any use of the Launchpad profile in production should be documented in the `EXCEPTIONS.md` file as technical debt to be upgraded to Standard (AA).

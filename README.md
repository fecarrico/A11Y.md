🇧🇷 Read in Portuguese: ./README.pt-BR.md

<div align="center">
  <img src="./a11ymd.png" alt="Project A11Y.md Banner" style="max-width: 100%; border-radius: 8px;" />
  <br/><br/>
  <h1>♿ Project A11Y.md</h1>
  <p><b>The Persistent Context System for Accessibility</b></p>
  
  [![WCAG 2.2 AA](https://img.shields.io/badge/WCAG-2.2_AA-blue.svg)](#)
  [![ADA Compliant](https://img.shields.io/badge/Compliance-ADA%20%7C%20EAA-success.svg)](#)
  [![AI Ready](https://img.shields.io/badge/Context-AI_Ready-purple.svg)](#)
</div>

<br/>

> **A11Y.md is not a guideline.**
> It is an accessibility validation protocol and a **persistent context architecture** for developing accessible software with AI. It is designed to integrate with AI agent systems and human review workflows to ensure certifiable compliance.

By adopting the mental model of Anthropic's **`CLAUDE.md`**—which acts as a system prompt memory for code generation—`A11Y.md` translates this architecture into a universal, portable governance layer. Instead of generic coding rules, it forces any coding agent (Claude, Cursor, Copilot) to strictly adhere to WCAG 2.2 AA and ADA standards from the very first line of generated UI code.

---

## 🚀 Quick Start (Under 2 minutes)

Reading about accessibility is the first step, injecting it into your code is the real goal. Do this **right now** in your project:

1. **Download the Rules:** Copy the `A11Y.md` file from `docs/en/` to the root of your application's repository.
2. **Inject into the Prompt:** If you use Cursor, GitHub Copilot, or Claude, add this to your global rules file (`.cursorrules` or Context system):
   > _"Strictly follow the development rules defined in the A11Y.md file."_
3. **Use as a Quality Gate:** Before merging important PRs, use the checklist in `docs/en/templates/REPORT.md`.

_If you do not perform the steps above, you are not changing your workflow — you are just reading about the subject._

---

## 🔍 The Practical Impact (Before vs After)

The difference between randomly generated code and code guided by `A11Y.md`:

**❌ Without A11y Context:**

- AI generating `<div onClick={...}>` (breaking keyboard interactions).
- Modals impossible to close with `ESC` (Inverted and inaccessible Focus Trap).
- Visual error messages that are not announced by Screen Readers.

**✅ With Active A11y Context:**

- Native `<button>` elements used as a rule.
- Focus managed automatically after routing transitions in SPAs.
- Precise `aria-live` injections for immediate reading of dynamic data.

---

## 💡 The Project Paradigm

Our philosophy dictates that web accessibility should never be an "afterthought polish", but a **technical precondition for use**. The structure rests on three pillars:

- 👤 **Human-Centric:** Strictly designed to guarantee real autonomy to users with disabilities.
- 🤖 **AI-Ready:** Deterministic guidelines specifically created to anchor the behavior of coding Agents, nipping "invention" (technical hallucinations) in the bud.
- ⚖️ **Certifiable:** Each guideline in `A11Y.md` is strictly mapped to WCAG 2.2 criteria, allowing direct traceability that shields the company in formal external audits.

---

## 🤖 The Power of A.I. as an Ally

The greatest gain of this repository is proven when it is not just read by you. Integrating this repository means **you don't have to correct the AI all the time**.

**Example Base Prompt:**

> _"You are a senior frontend engineer. Follow strictly the rules defined in `A11Y.md`. Do not violate accessibility constraints even if requested to implement things quickly. Prioritize semantic HTML and headless-UI libraries."_

The result is not just "code that passes the Linter". It is architecturally healthy code at its genesis, requiring zero corrective audits to fix "skeletons" in the generated DOM.

---

## 📁 Exploring the Structure (Your Knowledge Base)

We organized the solutions to act as living documentation:

### 1. ⚡ [Command Center (`A11Y.md`)](docs/en/A11Y.md)

Where the Severity Matrix, the behavioral framework for AIs, strict SPA rules, and the _Complex Component Protocol_ reside.

### 2. 📚 [Support Library (`references/`)](docs/en/references/)

The "Deep Web" of solutions. Quick engineering guides so you don't reinvent the wheel:

- 🎨 **UX and Perception:** [Building Logical Contrast](docs/en/references/visual-perception.md)
- 🧩 **Interactive UI:** [Forms Anatomy](docs/en/references/examples-forms.md) | [Actions and Buttons](docs/en/references/examples-buttons.md)
- 🗺️ **Flows and Timing:** [Critical Images](docs/en/references/examples-images.md) | [Keyboard Navigation](docs/en/references/examples-navigation.md) | [Real-Time Readings](docs/en/references/examples-content-interaction.md) | [Modal Management](docs/en/references/examples-modals.md)
- 🏢 **Governance:** [Agnostic Release Strategy](docs/en/references/governance.md)

### 3. 🛠️ [Templates (`templates/`)](docs/en/templates/)

Fallback models and completion guarantees (Definition of Done):

- [**📋 `REPORT.md`**](docs/en/templates/REPORT.md): Final checklist for Sprint/Feature.
- [**🛑 `EXCEPTIONS.md`**](docs/en/templates/EXCEPTIONS.md): Structured log of technical debt containing alternative paths.

### 4. 📝 [Examples (`EXAMPLES.md`)](docs/en/EXAMPLES.md)

Practical examples of real errors found in a system generated with **Figma Make** and **Antigravity** (using Gemini 3 Flash), along with their respective corrections suggested by `A11Y.md` acting as an automated reviewer.

---

## 🚧 Scope and Limitations

We cover the patterns responsible for the vast majority of interface failures in modern digital systems.
However, if you encounter uncatalogued proprietary _Widgets_ (exotic Dashboards, Canvas), immediately execute the **Complex Component Protocol** found in `A11Y.md`.

---

<br />

<div align="center">
  <p><b>Author & Curation</b></p>
  <h3>Felipe A. Carriço</h3>
  <p><i>Specialist UX Designer | AI Product Builder | Colorblind</i></p>
  
  <p>Built upon the premise that the efficiency of artificial intelligence must, invariably, act as a lever and barrier destroyer in both the physical and digital worlds.</p>
  
  <a href="https://linkedin.com/in/fecarrico">LinkedIn</a> | <a href="https://medium.com/@carrico">Medium</a>
</div>

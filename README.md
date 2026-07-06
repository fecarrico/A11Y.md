🇧🇷 Read in Portuguese: ./README.pt-BR.md

<div align="center">
  <img src="./a11ymd.png" alt="Project A11Y.md Banner" style="max-width: 100%; border-radius: 8px;" />
  <br/><br/>
  <h1>♿ Project A11Y.md</h1>
  <p><b>The Persistent Context System for Accessibility</b></p>
  
  [![WCAG 2.2 AA](https://img.shields.io/badge/WCAG-2.2_AA-blue.svg)](#)
  [![ADA Compliant](https://img.shields.io/badge/Compliance-ADA%20%7C%20EAA-success.svg)](#)
  [![AI Ready](https://img.shields.io/badge/Context-AI_Ready-purple.svg)](#)
  
  <br/>
  <a href="https://github.com/fecarrico/A11Y.md/wiki" target="_blank">📖 Read the Official Wiki</a> | <a href="https://v0-projecta11y.vercel.app/" target="_blank">🌐 Official Website</a> | <a href="https://open.substack.com/pub/felipearriadacarrio340730/p/a11ymd-accessibility-before-any-prompt" target="_blank">📝 Read the Manifesto (Substack)</a>
</div>

<br/>

> **A11Y.md is not a guideline.**
> It is an accessibility validation protocol and a **persistent context architecture** for developing accessible software with AI. It is designed to integrate with AI agent systems (Cursor, Claude, Copilot) to ensure certifiable compliance from genesis.

We treat `.gitignore`, `eslint`, and `CLAUDE.md` as canonical truths in our repositories. But why isn't accessibility canonical? `A11Y.md` translates accessibility rules into a universal, portable governance layer. Instead of generic coding advice, it forces any coding agent to strictly adhere to WCAG 2.2 AA and ADA standards from the very first line of generated UI code.

---

## ⚡ Core Features

- 🧠 **8-Rule AI Behavioral Contract:** A strict set of deterministic constraints that force the AI to act as a semantic translator (Framework Adaptation) and stop generating dangerous anti-patterns (like "clickable divs").
- 🛡️ **Modular Compliance Profiles:** Support for Shield (AAA), Standard (AA), and **Launchpad (A)**. The Launchpad profile allows startups to build rapid MVPs by relaxing visual constraints without ever sacrificing critical semantic structure.
- 📚 **Lazy Context Loading:** 20 deep engineering guides (WAI-ARIA APG) that act as an actionable database. The AI is programmed to load only the guides it needs on-demand, saving tokens and maintaining sharp focus.

---

## 🚀 Quick Start (Under 2 minutes)

Reading about accessibility is the first step, injecting it into your code is the real goal. Do this **right now** in your project:

1. **Download the Standard:** Copy the `docs/en/A11Y.md` file into your application's repository. (It can be placed in the root, inside a `docs/` folder, or anywhere else).
2. **Inject the Command:** You must explicitly instruct your AI to read it. If you use a `.cursorrules` or `CLAUDE.md` file, add this directive:
   > *"When developing the frontend, follow strictly the development rules defined in the A11Y.md file."*
3. **Set the Profile:** The AI will proactively ask you which Compliance Profile (Shield, Standard, or Launchpad) to use if you don't specify one.

👉 **<a href="https://github.com/fecarrico/A11Y.md/wiki/Setup-and-Integration" target="_blank">Read the full Setup and Integration guide on our Wiki.</a>**

---

## 📖 Official Documentation (The Wiki)

The complete architecture, protocols, and practical examples are thoroughly documented in our GitHub Wiki. 

**<a href="https://github.com/fecarrico/A11Y.md/wiki" target="_blank">🔗 Visit the A11Y.md Wiki</a>**

Inside, you will find:
- **The Command Center:** How the core `A11Y.md` file works.
- **Anti-patterns & Protocol:** Real-world examples of AI hallucinations being fixed.
- **Reference Library:** The taxonomy of the 20 engineering guides.
- **Governance & Compliance:** Preparing for VPATs and formal audits.

---

## 🔍 The Practical Impact (Before vs After)

The difference between randomly generated code and code guided by `A11Y.md`:

**❌ Without A11y Context:**
- AI generating `<div onClick={...}>` (breaking keyboard interactions).
- Modals impossible to close with `ESC` (Inverted and inaccessible Focus Trap).
- Visual error messages that are not announced by Screen Readers.

**✅ With Active A11y Context:**
- Native `<button>` elements used as a strict rule.
- Focus managed automatically after routing transitions in SPAs.
- Precise `aria-live` injections for immediate reading of dynamic data.

---

## 💡 The Project Paradigm

Our philosophy dictates that web accessibility should never be an "afterthought polish", but a **technical precondition for use**. The structure rests on three pillars:

- 👤 **Human-Centric:** Strictly designed to guarantee real autonomy to users with disabilities.
- 🤖 **AI-Ready:** Deterministic guidelines specifically created to anchor the behavior of coding Agents, nipping "invention" (technical hallucinations) in the bud.
- ⚖️ **Certifiable:** Each guideline in `A11Y.md` is mapped to WCAG 2.2 criteria, allowing direct traceability that shields the company in formal external audits.

---

## 🤝 Open Source & Community

A11Y.md is fundamentally an open-source initiative. Felipe does not claim to be a definitive accessibility expert, but rather a curious advocate deeply invested in the intersection of inclusion and artificial intelligence. 

The goal of this project is to be a living, breathing architecture. It relies on the open-source community — people far smarter and more experienced in accessibility engineering — to contribute, refine the reference library, and make this system robust enough to fundamentally change how digital solutions are created in the era of "vibe coding". 

**Pull Requests to improve the reference guides or the AI Behavioral Contract are highly encouraged!**

---

<br />

<div align="center">
  <p><b>Author & Curation</b></p>
  <h3>Felipe A. Carriço</h3>
  <p><i>Specialist UX Designer | AI Product Builder | Colorblind</i></p>
  
  <p>Built upon the premise that the efficiency of artificial intelligence must, invariably, act as a lever and barrier destroyer in both the physical and digital worlds.</p>
  
  <a href="https://linkedin.com/in/fecarrico" target="_blank">LinkedIn</a> | <a href="https://medium.com/@carrico" target="_blank">Medium</a>
</div>

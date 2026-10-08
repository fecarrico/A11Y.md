# Accessibility Statement (Template)

The public statement of a product's accessibility: what it promises, what has been verified, what is known to be broken, and who answers for it. GitHub shows this file as the **Accessibility** tab of the repository when it sits at the root, in `.github/` or in `docs/`. The same text serves the public declaration the EAA, the LBI and procurement rules ask for.

> **Rules:**
> 1. **Written from evidence, never ahead of it.** Every claim here comes from the current `REPORT.md` and `EXCEPTIONS.md`. The status declared is the report's status. A statement without a report behind it is a promise, not a statement, and the AI **MUST NOT** draft one.
> 2. **Known barriers are the open exceptions and the report's `[ ]` and `[!]` items**, in plain language, with the workaround. Nothing recorded there is left out here. Holding a barrier back is a decision for a person and their counsel, taken in the open, never an omission by the agent.
> 3. **A person signs it.** The agent drafts; a named owner reviews, publishes and answers. Owner and first-response time are mandatory.
> 4. **It is reviewed on events:** the report changes status, an exception opens or closes, a release ships. It carries the date of its last review and the standard version.
> 5. **It is a versioned project record** — never add it to `.gitignore`.

---

## [Product name] — accessibility statement

[One paragraph: what the product is, which surfaces this statement covers (web app, docs site, mobile app, CLI), and where the detailed evidence lives (link to `REPORT.md`).]

### What we hold ourselves to
- **Standard:** WCAG 2.2 at level [A | AA | AAA], under the [Launchpad | Standard | Shield] profile of A11Y.md version [x.y.z] *(the Version line at the top of the `A11Y.md` the project follows)*.
- **Legal references, where they apply:** [EN 301 549 / EAA · Section 508 / ADA · LBI art. 63 / ABNT NBR 17225 (regular | plena) · NBR 17060 for mobile] *(see Governance §5–§6.1)*.
- **Declared status:** [✅ PASS | ⚠️ CONDITIONAL | 🚫 FAIL] on [YYYY-MM-DD], verification [cross-agent | fresh-context | self-reported ⚠️] by [who], human checkpoints by [who]. *(Copied from `REPORT.md`; never upgraded here.)*

### Supported environments
[The browser and assistive-technology pairs the report names in §3: e.g. NVDA 2026.1 + Firefox 141 · VoiceOver + Safari 18 · TalkBack + Chrome on Android 15 · keyboard only · 200% zoom and 320 px reflow. An environment not listed was not tested, which is different from "unsupported".]

### Known barriers
[One row per open exception and per `[ ]`/`[!]` item in the report. Empty is a valid answer only when the report carries no such item.]

| Barrier | Who it affects | Workaround today | Tracking | Review by |
| :--- | :--- | :--- | :--- | :--- |
| [what the person cannot do, in plain words] | [e.g. screen-reader users on the checkout] | [the alternative route, or "none yet"] | [issue link] | [YYYY-MM-DD, from the exception's expiry] |

### How to report a barrier
- **Where:** [an issue link with a template, an e-mail, a form that is itself accessible, a phone number where the law asks for one].
- **What to include:** what you were trying to do, the assistive technology or input method, what happened.
- **What happens next:** first response within [n] days. A confirmed barrier enters `EXCEPTIONS.md` with an owner and a review date until it is fixed.

### For contributors
[The rules a change is held to and where the evidence goes, e.g. "Interfaces follow A11Y.md under the Standard profile. A change ships with `REPORT.md` updated, and an accepted deviation with an `EXCEPTIONS.md` entry." One line is enough. The standard itself is the long version.]

### Who answers for this
- **Owner:** [a person, with a way to reach them]
- **Last reviewed:** [YYYY-MM-DD] against A11Y.md [x.y.z]
- **Next review:** [on the next release, or a date]

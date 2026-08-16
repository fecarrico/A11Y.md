# Perf Exceptions Log (Template)

This document logs known budget overages against the performance standard (`PERF.md` §0.1) that have been temporarily accepted.

> **Objective:** Provide technical transparency by documenting *where*, *why*, and *by how much* the budgets are exceeded, and who accepted that cost on the user's behalf.

> **Rules:**
> 1. An exception is **temporary** and does not change the budget.
> 2. Every exception MUST have a **risk owner**, an **approver**, a **tracking issue**, and an **expiry date** — "waiting on the vendor" still gets a review date.
> 3. Scope is the **narrowest practical**: one route, one asset, one third-party — never "the app is heavy".
> 4. At expiry, the exception is reviewed: fixed and removed, or consciously renewed with a new date. **Never silently suppressed.**
> 5. **AI duty:** in review mode, the AI MUST flag any exception past its expiry date as 🟠 SERIOUS technical debt.
> 6. This log is a **versioned project record** — never add it to `.gitignore`. Accepted overages must be visible in pull requests and auditable later.

---

## 🛑 Exception Log

### 1. Basic Details
- **Exception ID:** [e.g., PEX-2026-001]
- **Route / Component:** [e.g., /checkout payment step]
- **Budget Affected:** [e.g., JS per route — 214 KB against a 170 KB Standard budget]
- **Severity (User Impact):** [🔴 Critical | 🟠 Serious | 🟡 Moderate | 🟢 Minor]
- **Risk Owner:** [Who is accountable — a person, not a team]
- **Approved by:** [Who signed off on the overage — lead/PO]
- **Tracking Issue:** [Link to the backlog item where this debt is chased]

### 2. Overage Description
- **What exceeds, and by how much?** [The measured number next to the budget, and the conditions of measurement].
- **Why did it happen?** [The payment SDK ships 90 KB and offers no slim build; the legacy grid cannot be virtualized this cycle; etc.].

### 3. Mitigation While Open
- **What keeps the experience acceptable meanwhile?** [The SDK loads on interaction with the payment step, not at route load; the grid caps at 200 rows with server paging; etc.]

### 4. Resolution Plan and Expiry
- **Expiry (review-by date):** [YYYY-MM-DD — mandatory]
- **Resolution Criterion:** [What measured number, under what conditions, closes this entry?]

---
*Blank copy (paste below as you create new exceptions).*

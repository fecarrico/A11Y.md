# Toasts & Notifications Guide

> **Scope:** Dynamic Feedback

## Core Rules
1. **Alerts:** Critical errors MUST use `role="alert"` (aria-live assertive).
2. **Status:** Non-critical messages MUST use `role="status"` (aria-live polite).
3. **Auto-dismissal:** Avoid auto-closing toasts that contain actionable links or long text. Give users control to close them.
# A11Y Decisions Log (Pattern Memory)

> **Purpose:** cross-turn memory of choices between **equally conformant alternatives**. Two implementations can both pass `A11Y.md` and axe and still diverge (different `role`, focus pattern, announcement wording) — twenty compliant modals, zero coherence. This file prevents that.

## Rules for the AI

1. **Record only what is not derivable** from `A11Y.md` rules or from the code itself. Landmarks, headings, and alt presence are machine-verifiable — they do **NOT** belong here.
2. **Index by pattern, never by screen.** ✅ *"Destructive confirmation modal → `alertdialog`"* · ❌ *"The dispute modal does X"*.
3. **One line per decision:** pattern → choice → short why.
4. **Read before building:** before generating any interactive component, check this log and reuse the recorded pattern (see *Component Reuse* in the AI Behavior Contract).
5. **Never fork silently:** if a new requirement contradicts a recorded decision, ask the user — do not create a parallel variant.
6. **Stay lean:** tens of lines, not hundreds. This file shares the context budget with Lazy Loading; if it grows past ~40 entries, consolidate.
7. **Versioned, never gitignored:** this is *shared* memory — across turns, agents and developers. A local-only copy per developer forks the patterns and defeats the file's entire purpose.
8. **When the static gate flags the choice:** end the line with the check and the markup the decision chose, one attribute or declaration with its value, as the source writes it: ``(gate: `aria-soup` · `role="list"`)`` for a `role="list"` kept because Safari stops announcing a list styled with `list-style: none`. `verify-a11y.py` then prints those findings as registered instead of failing. Only checks that flag a choice qualify (`aria-soup`, `redundant-alert`, `outline-none`, `orphaned-aria`); a violation you accept is an exception, and belongs in `EXCEPTIONS.md`.

## Decisions

<!-- Append entries below. Format: - **Pattern** → choice — why. (date) -->

- **Destructive confirmation modal** → `role="alertdialog"`, initial focus on the non-destructive button, focus returns to the trigger — interruption semantics per APG. *(example — replace with your project's first real decision)*

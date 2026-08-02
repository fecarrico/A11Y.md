# tools/

Two dependency-free Python scripts. Both are **optional** — the standard works in a purely conversational flow — but a gate that fails a build is stronger than a rule an agent has to remember.

> **Neither script establishes conformance.** Automated tooling detects only a fraction of real barriers. These check what a regex and a date comparison can check; the human checkpoints in `REPORT.md` are what establish the rest.

---

## `verify-a11y.py` — for projects adopting the standard

```bash
python3 verify-a11y.py [PROJECT_DIR] [--src SUBDIR] [--warn-only]
```

| Check | What it catches |
|---|---|
| `artifacts` | `REPORT.md` missing before a delivery (Release Evidence, §2) |
| `freshness` | report older than the last interface change (git history, falling back to mtime) |
| `report-status` | report claiming PASS while carrying `[ ]`, `[~]` or `[!]` checkpoints |
| `exceptions` | entries without risk owner, approver, tracking issue or expiry — and expired ones |
| `gitignore` | project artifacts excluded from version control |
| `clickable-div` · `positive-tabindex` · `outline-none` · `aria-soup` | source anti-patterns from §6 |

Exit code is `1` on errors, `0` on warnings only. Use `--warn-only` to report without failing the build while a team adopts the standard.

**GitHub Actions:**

```yaml
- name: A11Y.md static gate
  run: |
    curl -sO https://raw.githubusercontent.com/fecarrico/A11Y.md/main/tools/verify-a11y.py
    python3 verify-a11y.py . --src src
```

## `lint-standard.py` — for maintaining the standard itself

```bash
python3 lint-standard.py [REPO_ROOT]
```

Checks parity between `docs/en` and `docs/pt-BR` (file list, headings, contract rule count), orphaned reference guides, broken relative links, phase triggers ("at final delivery") that never fire in continuous delivery, and any label calling the project artifacts optional.

Every check exists because the corresponding defect actually shipped: the ten guides orphaned in 1.0.0, the "Optional Templates" label and the phase trigger that together caused the [2026-08-01 field failure](../CHANGELOG.md). Run against the release before 1.2.0, it reports all four.

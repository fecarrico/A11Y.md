# tools/

Two dependency-free Python scripts. Both are **optional** — the standard works in a purely conversational flow — but a gate that fails a build is stronger than a rule an agent has to remember.

> [!IMPORTANT]
> **These scripts are not part of the standard.** `A11Y.md` is portable markdown: it must keep working for anyone whose agent can read a file, with no runtime installed. Nothing in the normative core requires running these — and nothing ever should. They are a convenience for teams that want CI enforcement.

> [!WARNING]
> **Experimental (v0).** First release, exercised against fixtures and this repository — not against a wide range of real projects. A false positive in your pipeline is worse than no gate at all, so start with `--warn-only`, and please [open an issue](https://github.com/fecarrico/A11Y.md/issues) for anything it gets wrong. Bug reports are the fastest way to make it trustworthy.

> **Neither script establishes conformance.** Automated tooling detects only a fraction of real barriers. These check what a regex and a date comparison can check; the human checkpoints in `REPORT.md` are what establish the rest.

**Requirements:** Python 3.9+, standard library only — no `pip install`, no `package.json`. Python is preinstalled on macOS, most Linux distributions and virtually every CI runner. A Node port may follow if adoption shows real friction; until then, this is a deliberate choice for zero dependencies over toolchain familiarity.

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

**GitHub Actions** — pin to a tag, never to `main`: this is executable code, and a moving branch is a supply-chain risk. Bump the tag deliberately, the same way you would any other dependency.

```yaml
- name: A11Y.md static gate
  run: |
    curl -sO https://raw.githubusercontent.com/fecarrico/A11Y.md/v1.3.0/tools/verify-a11y.py
    python3 verify-a11y.py . --src src --warn-only   # drop --warn-only once the team is ready
```

Vendoring the script into your repository is equally valid, and gives you a reviewable diff when you upgrade.

## `lint-standard.py` — for maintaining the standard itself

```bash
python3 lint-standard.py [REPO_ROOT]
```

Checks parity between `docs/en` and `docs/pt-BR` (file list, headings, contract rule count), orphaned reference guides, broken relative links, phase triggers ("at final delivery") that never fire in continuous delivery, and any label calling the project artifacts optional.

Every check exists because the corresponding defect actually shipped: the ten guides orphaned in 1.0.0, the "Optional Templates" label and the phase trigger that together caused the [2026-08-01 field failure](../CHANGELOG.md). Run against the release before 1.2.0, it reports all four.

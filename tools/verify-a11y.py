#!/usr/bin/env python3
"""
verify-a11y.py — static gate for projects adopting the A11Y.md standard.

Checks what can be verified without a browser: that the project artifacts
exist, are current and well-formed, and that the source is free of the
anti-patterns a regex can catch. Exits non-zero when a check fails, so it
can gate a build.

It does NOT establish WCAG conformance. Automated tooling detects only a
fraction of real barriers; the human checkpoints in REPORT.md remain the
part that matters most. A clean run means "nothing statically detectable
is wrong", not "this is accessible".

Usage:
    python3 verify-a11y.py [PROJECT_DIR] [--src SUBDIR] [--warn-only]

Stdlib only, no dependencies.
"""

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ARTIFACTS = ("REPORT.md", "EXCEPTIONS.md", "A11Y-DECISIONS.md")
SOURCE_SUFFIXES = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".css", ".scss", ".astro"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "out", "vendor", "__pycache__", ".venv"}

# Placeholder text from the templates — an unfilled template is not an entry.
PLACEHOLDER = re.compile(r"\[(YYYY|AAAA|MM/DD|DD/MM|e\.g\.|Ex:|Who|Link|Date|Quem|Data|Escreva|Write)", re.I)

findings: list[tuple[str, str, str]] = []  # (level, check, message)


def fail(check: str, message: str) -> None:
    findings.append(("ERROR", check, message))


def warn(check: str, message: str) -> None:
    findings.append(("WARN", check, message))


def git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def source_files(root: Path, src: Path):
    for path in src.rglob("*"):
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
            if not any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                yield path


# --- checks ----------------------------------------------------------------

def check_artifacts_exist(root: Path) -> Path | None:
    """REPORT.md is required. The other two are required only when their
    triggering event has occurred, which this script cannot observe."""
    report = root / "REPORT.md"
    if not report.is_file():
        fail("artifacts", "REPORT.md not found. Release Evidence (A11Y.md §2) requires it "
                          "before any delivery to an end user — generate it from templates/REPORT.md.")
        return None
    return report


def check_report_freshness(root: Path, report: Path, src: Path) -> None:
    """The report must be newer than the last interface change."""
    last_ui = git(root, "log", "-1", "--format=%cI", "--", str(src.relative_to(root)) if src != root else ".")
    last_report = git(root, "log", "-1", "--format=%cI", "--", "REPORT.md")
    if last_ui and last_report:
        if last_report < last_ui:
            fail("freshness", f"REPORT.md (last commit {last_report[:10]}) is older than the last "
                              f"interface change ({last_ui[:10]}). Revisit the entries that change affects.")
        return
    # no git history available — fall back to mtime
    newest = max((p.stat().st_mtime for p in source_files(root, src)), default=None)
    if newest and report.stat().st_mtime < newest:
        fail("freshness", "REPORT.md is older than the most recently modified source file.")


def check_report_status(report: Path) -> None:
    """A report claiming PASS cannot carry unverified or failed checkpoints.

    The status is read from its own field, never from the whole document: the
    template's headless-agent note contains the word CONDITIONAL, so a
    document-wide search silently exonerates every report generated from it.
    """
    text = report.read_text(encoding="utf-8", errors="replace")
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(">"))
    unchecked = len(re.findall(r"^\s*-\s*\[\s\]", body, re.M))
    failed = len(re.findall(r"^\s*-\s*\[!\]", body, re.M))
    partial = len(re.findall(r"^\s*-\s*\[~\]", body, re.M))

    field = re.search(r"(?:Compliance Status|Status de Conformidade):?\*{0,2}[ \t]*(.*)", body)
    value = field.group(1).strip() if field else ""
    if not value:
        fail("report-status", "REPORT.md has no Compliance Status field — fill it from templates/REPORT.md.")
        return
    if value.count("|") >= 2:  # the template's untouched menu of options
        fail("report-status", "REPORT.md still carries the template's status placeholder "
                              "(the PASS | CONDITIONAL | FAIL menu). Declare one status.")
        return

    conditional = re.search(r"CONDITIONAL|CONDICIONAL", value, re.I)
    claims_pass = not conditional and (re.search(r"\bPASS\b", value, re.I) or "✅" in value)
    if claims_pass and (unchecked or failed or partial):
        fail("report-status", f"REPORT.md claims PASS while carrying {unchecked} unverified, "
                              f"{partial} partial and {failed} failed checkpoints. "
                              f"Status must be CONDITIONAL until they are closed.")
    if failed:
        warn("report-status", f"{failed} checkpoint(s) marked [!] (verified and failed) — "
                              f"fix them or open an EXCEPTIONS.md entry.")


def check_exceptions(root: Path) -> None:
    """Every exception needs owner, approver, tracking issue and a future expiry."""
    path = root / "EXCEPTIONS.md"
    if not path.is_file():
        return  # only required once a deviation is accepted
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"^#{2,4}\s+\d+\.\s*(?:Basic Details|Detalhes Básicos)", text, flags=re.M)[1:]
    today = dt.date.today()
    for i, block in enumerate(blocks, 1):
        entry_id = re.search(r"(?:Exception ID|ID da Exceção):\*{0,2}[ \t]*(.*)", block)
        label = (entry_id.group(1).strip() if entry_id else f"entry #{i}")[:40]
        if PLACEHOLDER.search(label) or not label:
            continue  # unfilled blank copy from the template
        for field, pattern in (("risk owner", r"(Risk Owner|Dono do Risco)"),
                               ("approver", r"(Approved by|Aprovado por)"),
                               ("tracking issue", r"(Tracking Issue|Issue de Rastreio)")):
            m = re.search(pattern + r":\*{0,2}[ \t]*(.*)", block)
            if not m or not m.group(2).strip() or PLACEHOLDER.search(m.group(2)):
                fail("exceptions", f"{label}: missing {field}.")
        expiry = re.search(r"(?:Expiry|Expiração)[^:\n]*:\*{0,2}[ \t]*\[?(\d{4}-\d{2}-\d{2})", block)
        if not expiry:
            fail("exceptions", f"{label}: missing or unparseable expiry date (use YYYY-MM-DD).")
        else:
            date = dt.date.fromisoformat(expiry.group(1))
            if date < today:
                fail("exceptions", f"{label}: expired on {date} — review, fix or consciously renew it.")
            elif (date - today).days <= 14:
                warn("exceptions", f"{label}: expires in {(date - today).days} day(s).")


def check_gitignore(root: Path) -> None:
    """Artifacts are versioned records; hiding them defeats their purpose."""
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        return
    patterns = [l.strip() for l in gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
                if l.strip() and not l.startswith("#")]
    for artifact in ARTIFACTS:
        for pattern in patterns:
            if pattern.strip("/") == artifact or pattern in ("*.md", "**/*.md"):
                fail("gitignore", f"{artifact} is excluded by .gitignore rule '{pattern}'. "
                                  f"Project artifacts must be versioned.")
                break


def check_source_antipatterns(root: Path, src: Path) -> None:
    """Scan whole files, not single lines.

    JSX spreads one element over many lines — `<div` on one, `onClick` three
    below — which is the canonical React form and the exact shape of the
    anti-pattern this standard exists to stop. A line-by-line scan never sees it.
    """
    checks = (
        ("clickable-div", re.compile(r"<(div|span)\b[^>]*\bon[cC]lick\b"),
         "clickable <div>/<span> — use a native <button> (A11Y.md §6)"),
        # `tabIndex={1}` (JSX) and `tabindex="1"` (HTML) are the same defect.
        ("positive-tabindex", re.compile(r"tabindex\s*=\s*[\"'{]?\s*[1-9]", re.I),
         "positive tabindex breaks the natural focus order"),
        ("outline-none", re.compile(r"outline\s*:\s*(none|0)\s*[;}]|\boutline-none\b"),
         "outline suppressed — pair it with a visible focus indicator that survives forced-colors "
         "mode; a box-shadow ring alone disappears there (SC 2.4.7)"),
        ("aria-soup", re.compile(r"<button\b[^>]*\brole\s*=\s*[\"']button[\"']|<a\b[^>]*\brole\s*=\s*[\"']link[\"']"),
         "redundant role on a native element (ARIA Soup, A11Y.md §6)"),
        ("redundant-alert", re.compile(r"role\s*=\s*[\"']alert[\"'][^>]*aria-live|aria-live[^>]*role\s*=\s*[\"']alert[\"']"),
         "role=\"alert\" already implies aria-live=\"assertive\" — declaring both is ARIA Soup (A11Y.md §6)"),
        ("nullified-alt", re.compile(r"<img\b(?=[^>]*\balt\s*=\s*[\"'][^\"']+[\"'])[^>]*\baria-hidden\s*=\s*[\"']?true"),
         "aria-hidden on an image that carries a non-empty alt cancels it for screen readers while "
         "every checker still passes (A11Y.md §6, guide-images.md)"),
        ("media-autoplay", re.compile(r"<(video|audio)\b[^>]*\bautoplay\b(?!\s*[:=]\s*[{\"']?\s*false)", re.I),
         "autoplay declared in the markup cannot be vetoed by prefers-reduced-motion — grant it by "
         "script, mute it, and give it a pause mechanism (SC 2.2.2 / 1.4.2, guide-media.md §3)"),
    )
    for path in source_files(root, src):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root)
        for name, pattern, message in checks:
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                level = warn if name in ("outline-none", "media-autoplay") else fail
                level(name, f"{rel}:{line_no} — {message}")


# --- main ------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", default=".", help="project root (default: current directory)")
    parser.add_argument("--src", default=None, help="subdirectory holding the interface source (default: project root)")
    parser.add_argument("--warn-only", action="store_true", help="always exit 0, printing findings only")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    src = (root / args.src).resolve() if args.src else root

    report = check_artifacts_exist(root)
    if report:
        check_report_freshness(root, report, src)
        check_report_status(report)
    check_exceptions(root)
    check_gitignore(root)
    check_source_antipatterns(root, src)

    errors = [f for f in findings if f[0] == "ERROR"]
    warnings = [f for f in findings if f[0] == "WARN"]
    for level, check, message in errors + warnings:
        marker = "✗" if level == "ERROR" else "!"
        print(f"{marker} [{check}] {message}")

    print()
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s).")
    elif warnings:
        print(f"PASS with {len(warnings)} warning(s).")
    else:
        print("PASS — nothing statically detectable is wrong.")
    print("This is not a conformance claim: the human checkpoints in REPORT.md are what establish it.")

    return 1 if errors and not args.warn_only else 0


if __name__ == "__main__":
    sys.exit(main())

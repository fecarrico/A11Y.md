#!/usr/bin/env python3
"""
verify-a11y.py — static gate for projects adopting the A11Y.md standard.

Checks what can be verified without a browser: that the project artifacts
exist, are current and well-formed, that the evidence they carry adds up
(the contrast ratios recorded in REPORT.md are recomputed, never trusted,
and every component the source contains must have its guide's scenarios
in the report),
and that the source is free of the anti-patterns a text search can catch —
the ones axe cannot see because they live in handlers, CSS intent or source
that has not been rendered yet. Exits non-zero when a check fails, so it can
gate a build. A finding the project already recorded (an exception in force,
or a decision between conformant alternatives) is printed as registered and
does not fail. Every run ends with the line to record in the report's Static
gate field; when the script cannot run at all, the agent records NOT RUN
with the reason and says so in the delivery (A11Y.md §2).

It does NOT establish WCAG conformance. Automated tooling detects only a
fraction of real barriers; the human checkpoints in REPORT.md remain the
part that matters most. A clean run means "nothing statically detectable
is wrong", not "this is accessible".

Usage:
    python3 verify-a11y.py [PROJECT_DIR] [--src SUBDIR] [--warn-only]
    python3 verify-a11y.py --self-test

Stdlib only, no dependencies.
"""

import argparse
import datetime as dt
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ARTIFACTS = ("REPORT.md", "EXCEPTIONS.md", "A11Y-DECISIONS.md")
SOURCE_SUFFIXES = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".css", ".scss", ".astro"}
SCRIPT_SUFFIXES = {".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "out", "vendor", "__pycache__", ".venv"}

# Placeholder text from the templates — an unfilled template is not an entry.
PLACEHOLDER = re.compile(r"\[(YYYY|AAAA|MM/DD|DD/MM|e\.g\.|Ex:|Who|Link|Date|Quem|Data|Escreva|Write)", re.I)

# Attributes of one tag. `=>` is allowed inside because JSX handlers carry
# arrow functions (`onClick={() => open()}`) and a plain `[^>]*` stops there.
ATTRS = r"((?:[^>]|=>)*)"

# Overlay vendors. An overlay never fixes the DOM that produced the barrier
# (A11Y.md §6, Accessibility Overlays) — the fix belongs in the code.
OVERLAY_DOMAINS = ("accessibe.com", "acsbapp.com", "userway.org", "audioeye.com", "equalweb.com",
                   "maxaccess.io", "allyable.com", "adally.com", "accessiway.com", "truabilities.com")

# Composite ARIA patterns and the child roles each one requires (WAI-ARIA 1.2,
# required owned elements). A parent announced without its children is the
# Half-Climbed ARIA Ladder (A11Y.md §6); the tablist mold is the one Study 3
# found surviving two releases, so it fails — the others warn, because the
# children may legitimately live in another component.
COMPOSITES = {
    "tablist": ("tab",), "listbox": ("option",), "tree": ("treeitem",), "radiogroup": ("radio",),
    "grid": ("row",), "treegrid": ("row",),
    "menu": ("menuitem", "menuitemcheckbox", "menuitemradio"),
    "menubar": ("menuitem", "menuitemcheckbox", "menuitemradio"),
}
# Native elements that carry a required child role implicitly: a radiogroup of
# <input type="radio">, a grid drawn as a <table> of <tr>. No explicit role needed.
NATIVE_CHILDREN = {
    "radiogroup": re.compile(r"<input\b[^>]*\btype\s*=\s*[\"']radio[\"']", re.I),
    "grid": re.compile(r"<tr\b", re.I),
    "treegrid": re.compile(r"<tr\b", re.I),
}

# Native elements whose implicit role makes the explicit one redundant (ARIA
# Soup). Only unconditional pairs: `header`/`footer`/`section`/`form` change
# role with context, so they stay out.
REDUNDANT_ROLES = {
    "button": ("button",), "nav": ("navigation",), "main": ("main",), "aside": ("complementary",),
    "ul": ("list",), "ol": ("list",), "li": ("listitem",), "img": ("img",), "table": ("table",),
    "article": ("article",), "dialog": ("dialog",), "progress": ("progressbar",), "textarea": ("textbox",),
    "h1": ("heading",), "h2": ("heading",), "h3": ("heading",), "h4": ("heading",), "h5": ("heading",), "h6": ("heading",),
}

# Text floors per compliance profile (SC 1.4.3 / 1.4.6). UI floor is 3:1 everywhere (SC 1.4.11).
PROFILE_FLOORS = {"shield": 7.0, "standard": 4.5, "launchpad": 4.5}

findings: list[tuple[str, str, str, str]] = []  # (level, check, message, source text flagged)


def fail(check: str, message: str, subject: str = "") -> None:
    findings.append(("ERROR", check, message, subject))


def warn(check: str, message: str, subject: str = "") -> None:
    findings.append(("WARN", check, message, subject))


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


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# Markup quoted inside <pre>/<code> is documentation, not a component: a page
# that explains role="menu" is not a menu. Found by running the gate against a
# component library's documentation site (Magoo, 2026-09-29).
CODE_SAMPLE = re.compile(r"(<(pre|code)\b[^>]*>)(.*?)(</\2\s*>)", re.I | re.S)


def without_code_samples(text: str | None) -> str | None:
    """Blank the text quoted inside <pre>/<code>, keeping every newline so the
    line numbers reported for the rest of the file still point at the right place."""
    if text is None:
        return None
    return CODE_SAMPLE.sub(lambda m: m.group(1) + re.sub(r"[^\n]", " ", m.group(3)) + m.group(4), text)


# Comments are not markup either. A `// role="menu"` in a doc string, a
# `{/* aria-live */}` beside a role="alert", an `outline: none` inside a CSS
# comment: three false positives in one adopter's review (2026-09-30), all
# the same class. Whole-line `//` comments only — `https://` mid-line is a URL,
# not a comment, and a trailing comment after code is rare enough to leave.
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"^[ \t]*//[^\n]*", re.M)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
MARKUP_SUFFIXES = {".html", ".htm", ".vue", ".svelte", ".astro"}


def without_comments(text: str | None, suffix: str) -> str | None:
    """Blank comments for the file's language, keeping every newline."""
    if text is None:
        return None
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    if suffix in SCRIPT_SUFFIXES or suffix in (".css", ".scss"):
        text = BLOCK_COMMENT.sub(blank, text)
    if suffix in SCRIPT_SUFFIXES:
        text = LINE_COMMENT.sub(blank, text)
    if suffix in MARKUP_SUFFIXES:
        text = HTML_COMMENT.sub(blank, text)
    return text


def scannable(path: Path) -> str | None:
    """The file as the source scan sees it: no quoted samples, no comments."""
    return without_comments(without_code_samples(read(path)), path.suffix.lower())


def body_of(report: Path) -> str:
    """The report without its blockquotes: the template explains every field
    inside `>` notes, and a document-wide search would find the explanation."""
    text = read(report) or ""
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(">"))


# --- contrast arithmetic (WCAG 2.x relative luminance) ---------------------

def hex_rgb(token: str) -> tuple[int, int, int]:
    h = token.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(rgb) -> float:
    def chan(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = sorted((luminance(hex_rgb(fg)), luminance(hex_rgb(bg))), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# --- checks: artifacts -----------------------------------------------------

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


def status_claims_pass(body: str) -> bool:
    status = re.search(r"(?:Compliance Status|Status de Conformidade):?\*{0,2}[ \t]*(.*)", body, re.I)
    value = status.group(1).strip() if status else ""
    conditional = re.search(r"CONDITIONAL|CONDICIONAL", value, re.I)
    return bool(not conditional and (re.search(r"\bPASS\b", value, re.I) or "✅" in value))


def check_report_status(report: Path) -> None:
    """A report claiming PASS cannot carry unverified or failed checkpoints.

    The status is read from its own field, never from the whole document: the
    template's headless-agent note contains the word CONDITIONAL, so a
    document-wide search silently exonerates every report generated from it.
    """
    body = body_of(report)
    unchecked = len(re.findall(r"^\s*-\s*\[\s\]", body, re.M))
    failed = len(re.findall(r"^\s*-\s*\[!\]", body, re.M))
    partial = len(re.findall(r"^\s*-\s*\[~\]", body, re.M))

    field = re.search(r"(?:Compliance Status|Status de Conformidade):?\*{0,2}[ \t]*(.*)", body, re.I)
    value = field.group(1).strip() if field else ""
    if not value:
        fail("report-status", "REPORT.md has no Compliance Status field — fill it from templates/REPORT.md.")
        return
    if value.count("|") >= 2:  # the template's untouched menu of options
        fail("report-status", "REPORT.md still carries the template's status placeholder "
                              "(the PASS | CONDITIONAL | FAIL menu). Declare one status.")
        return

    if status_claims_pass(body) and (unchecked or failed or partial):
        fail("report-status", f"REPORT.md claims PASS while carrying {unchecked} unverified, "
                              f"{partial} partial and {failed} failed checkpoints. "
                              f"Status must be CONDITIONAL until they are closed.")
    if failed:
        warn("report-status", f"{failed} checkpoint(s) marked [!] (verified and failed) — "
                              f"fix them or open an EXCEPTIONS.md entry.")


def check_report_independence(report: Path) -> None:
    """Who verified is part of the evidence (Independent Verification, §2).

    Read from the field alone, never from the whole document — the template's
    own explanation of the field names all three levels, and a document-wide
    search would find "cross-agent" in every report generated from it. Same
    trap the status check fell into before 1.5.0.
    """
    body = body_of(report)
    field = re.search(r"(?:Verification Independence|Independência da Verificação):?\*{0,2}[ \t]*(.*)", body, re.I)
    if not field:
        fail("independence", "REPORT.md has no Verification Independence field. Add it from "
                             "templates/REPORT.md and declare who reproduced the automated checkpoints "
                             "(A11Y.md §2, Independent Verification).")
        return

    value = field.group(1).strip()
    levels = [name for name in ("cross-agent", "fresh-context", "self-reported") if name in value.lower()]
    if len(levels) != 1:
        fail("independence", "REPORT.md does not declare exactly one verification level — expected "
                             "cross-agent, fresh-context or self-reported, found "
                             f"{len(levels)}. An untouched template menu counts as undeclared.")
        return

    level = levels[0]
    if level == "self-reported":
        if status_claims_pass(body):
            fail("independence", "REPORT.md claims PASS on self-reported verification — the agent that "
                                 "generated the code is the only witness that it conforms. Re-run the "
                                 "automated checkpoints in a fresh session (or with another agent), or "
                                 "lower the status to CONDITIONAL.")
        else:
            warn("independence", "Verification is self-reported: the generating agent checked its own "
                                 "output. Ceiling is CONDITIONAL. A new chat over this project, without "
                                 "the conversation that produced the code, raises it to fresh-context.")

    if re.fullmatch(r"(cross-agent|fresh-context|self-reported)\W*", value, re.I):
        warn("independence", f"Verification level is '{level}' but nobody is named. Record which "
                             f"model/agent and which session reproduced the checkpoints — an "
                             f"unattributed level is not reproducible evidence.")


def check_report_gate(report: Path) -> str | None:
    """The gate's own outcome is part of the evidence (Static Gate, §2).

    A gate that silently did not run reads exactly like one that passed, so
    the report must declare one of three outcomes — PASS, FAIL or NOT RUN
    with the reason. This validates the declaration's shape and returns its
    value; run_checks() compares it with what this run actually found.
    """
    body = body_of(report)
    field = re.search(r"(?:Static gate|Gate estático)[^:\n]*:\*{0,2}[ \t]*(.*)", body, re.I)
    if not field:
        fail("gate-declared", "REPORT.md has no Static gate field. Add it from templates/REPORT.md and "
                              "record this run's outcome (A11Y.md §2, Static Gate).")
        return None
    value = field.group(1).strip()
    if value.count("|") >= 2:  # the template's untouched menu of outcomes
        fail("gate-declared", "REPORT.md still carries the template's Static gate menu "
                              "(PASS | FAIL | NOT RUN). Declare this run's outcome.")
        return None
    return value


def check_report_standard_version(report: Path) -> None:
    """Which edition of the rules the evidence answers to (Release Evidence, §2).

    The invocation phrase points at `main`, which moves. A report that does not
    name the version it was verified against cannot be re-read against the
    rules that were in force when it was written. Absence warns — reports older
    than the field are still evidence; a placeholder left in place fails — the
    field was there and nobody filled it.
    """
    body = body_of(report)
    field = re.search(r"(?:Standard version|Versão do padrão)[^:\n]*:\*{0,2}[ \t]*(.*)", body, re.I)
    if not field:
        warn("standard-version", "REPORT.md does not name the A11Y.md version it was verified against. Add the "
                                 "Standard version field from templates/REPORT.md — the Version line at the top of "
                                 "A11Y.md — so the evidence can be re-read against the rules in force.")
        return
    value = field.group(1).strip()
    if not value or PLACEHOLDER.search(value) or not re.search(r"\b\d+\.\d+\.\d+\b", value):
        fail("standard-version", "REPORT.md carries the Standard version field but no version (x.y.z) — copy it "
                                 "from the Version line at the top of the A11Y.md this project follows.")


def check_contrast_evidence(root: Path, report: Path, src: Path) -> None:
    """Contrast ratios are computed, never estimated (A11Y.md §3) — and the
    gate recomputes every pair the report records, because a written "7.2:1"
    costs nothing to invent. A row is any line carrying two hex colors and a
    ratio: foreground first, background second, the declared ratio, and
    optionally the floor it was measured against. Rows in A11Y-DECISIONS.md
    (the palette matrix, Palette Definition Protocol) count too.
    """
    body = body_of(report)
    decisions = root / "A11Y-DECISIONS.md"
    texts = [body] + ([body_of(decisions)] if decisions.is_file() else [])

    profile = "shield" if re.search(r"\bShield\b|\bAAA\b", body) else \
              "launchpad" if re.search(r"\bLaunchpad\b", body) else "standard"
    floor_default = PROFILE_FLOORS[profile]

    hex_re = re.compile(r"(?<![\w#])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
    ratio_re = re.compile(r"(\d+(?:[.,]\d+)?)\s*:\s*1\b")
    rows = 0
    source_hex: set[str] | None = None

    for text in texts:
        for raw in text.splitlines():
            if not raw.lstrip().startswith("|"):
                continue  # only table rows are pairs — prose that mentions colors is not evidence
            line = raw.replace("**", "")
            colors = hex_re.findall(line)
            ratios = [float(r.replace(",", ".")) for r in ratio_re.findall(line)]
            if len(colors) < 2 or not ratios:
                continue
            rows += 1
            fg, bg = colors[0], colors[1]
            declared = ratios[0]
            floor = ratios[1] if len(ratios) > 1 else floor_default
            computed = contrast(fg, bg)
            label = f"{fg} on {bg}"
            if abs(computed - declared) > 0.1:  # one-decimal rounding or truncation is honest; 0.5 off is not
                fail("contrast-evidence", f"REPORT.md records {label} as {declared:g}:1; the WCAG formula "
                                          f"gives {computed:.2f}:1. Measured evidence must match the arithmetic "
                                          f"(A11Y.md §3) — recompute with tools/contrast-check.py.")
                continue
            marked_pass = bool(re.search(r"✅|\bPASS\b|\bOK\b", line, re.I))
            if computed < floor - 0.005 and marked_pass:
                fail("contrast-evidence", f"REPORT.md marks {label} ({computed:.2f}:1) as passing, below the "
                                          f"{floor:g}:1 floor it is measured against.")
            elif computed < floor - 0.005:
                warn("contrast-evidence", f"{label} is {computed:.2f}:1, below the {floor:g}:1 floor — "
                                          f"recorded honestly; fix it or open an EXCEPTIONS.md entry.")
            if source_hex is None:
                source_hex = set()
                for path in source_files(root, src):
                    text_src = read(path) or ""
                    source_hex.update(normalize_hex(h) for h in hex_re.findall(text_src))
            if source_hex:
                for color in (fg, bg):
                    if normalize_hex(color) not in source_hex:
                        warn("contrast-evidence", f"{color} (from the pair {label}) does not appear in the "
                                                  f"source. If tokens are computed at runtime (hsl(), color-mix()) "
                                                  f"this is expected; otherwise the pair measured a color the "
                                                  f"project does not use.")

    checkpoint_checked = re.search(r"^\s*-\s*\[x\][^\n]*(contrast|contraste)", body, re.I | re.M)
    if rows == 0 and checkpoint_checked:
        fail("contrast-evidence", "The contrast checkpoint is marked verified but no measured pair is recorded. "
                                  "Record each pair as foreground, background and ratio (#hex · #hex · N:1) in the "
                                  "REPORT.md pair table — \"looks sufficient\" is fabricated evidence (A11Y.md §3).")


def normalize_hex(token: str) -> str:
    h = token.lstrip("#").lower()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return h


def exception_entries(root: Path) -> list[tuple[str, str]]:
    """The filled entries of EXCEPTIONS.md as (label, block). A blank copy of
    the template is not an entry."""
    path = root / "EXCEPTIONS.md"
    if not path.is_file():
        return []  # only required once a deviation is accepted
    text = read(path) or ""
    blocks = re.split(r"^#{2,4}\s+\d+\.\s*(?:Basic Details|Detalhes Básicos)", text, flags=re.M)[1:]
    entries = []
    for i, block in enumerate(blocks, 1):
        entry_id = re.search(r"(?:Exception ID|ID da Exceção):\*{0,2}[ \t]*(.*)", block)
        label = (entry_id.group(1).strip() if entry_id else f"entry #{i}")[:40]
        if label and not PLACEHOLDER.search(label):
            entries.append((label, block))
    return entries


SIGN_OFF = (("risk owner", r"(Risk Owner|Dono do Risco)"),
            ("approver", r"(Approved by|Aprovado por)"),
            ("tracking issue", r"(Tracking Issue|Issue de Rastreio)"))


def missing_fields(block: str) -> list[str]:
    missing = []
    for field, pattern in SIGN_OFF:
        m = re.search(pattern + r":\*{0,2}[ \t]*(.*)", block)
        if not m or not m.group(2).strip() or PLACEHOLDER.search(m.group(2)):
            missing.append(field)
    return missing


def expiry_of(block: str) -> dt.date | None:
    expiry = re.search(r"(?:Expiry|Expiração)[^:\n]*:\*{0,2}[ \t]*\[?(\d{4}-\d{2}-\d{2})", block)
    return dt.date.fromisoformat(expiry.group(1)) if expiry else None


def check_exceptions(root: Path) -> None:
    """Every exception needs owner, approver, tracking issue and a future expiry."""
    today = dt.date.today()
    for label, block in exception_entries(root):
        for field in missing_fields(block):
            fail("exceptions", f"{label}: missing {field}.")
        date = expiry_of(block)
        if not date:
            fail("exceptions", f"{label}: missing or unparseable expiry date (use YYYY-MM-DD).")
        elif date < today:
            fail("exceptions", f"{label}: expired on {date} — review, fix or consciously renew it.")
        elif (date - today).days <= 14:
            warn("exceptions", f"{label}: expires in {(date - today).days} day(s).")


def check_gitignore(root: Path) -> None:
    """Artifacts are versioned records; hiding them defeats their purpose."""
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        return
    patterns = [l.strip() for l in (read(gitignore) or "").splitlines()
                if l.strip() and not l.startswith("#")]
    for artifact in ARTIFACTS:
        for pattern in patterns:
            if pattern.strip("/") == artifact or pattern in ("*.md", "**/*.md"):
                fail("gitignore", f"{artifact} is excluded by .gitignore rule '{pattern}'. "
                                  f"Project artifacts must be versioned.")
                break


# --- checks: source — what axe cannot see ----------------------------------

def check_source_antipatterns(root: Path, src: Path) -> None:
    """Scan whole files, not single lines.

    JSX spreads one element over many lines — `<div` on one, `onClick` three
    below — which is the canonical React form and the exact shape of the
    anti-pattern this standard exists to stop. A line-by-line scan never sees it.
    """
    click_handler = re.compile(r"\bon[cC]lick\b|@click\b|\bv-on:click\b|\bon:click\b|\(click\)")
    clickable = re.compile(r"<(div|span)\b" + ATTRS + r">")
    checks = (
        # `tabIndex={1}` (JSX) and `tabindex="1"` (HTML) are the same defect.
        ("positive-tabindex", re.compile(r"tabindex\s*=\s*[\"'{]?\s*[1-9]", re.I),
         "positive tabindex breaks the natural focus order"),
        ("outline-none", re.compile(r"outline\s*:\s*(none|0)\s*[;}]|\boutline-none\b"),
         "outline suppressed — pair it with a visible focus indicator that survives forced-colors "
         "mode; a box-shadow ring alone disappears there (SC 2.4.7)"),
        ("redundant-alert", re.compile(r"role\s*=\s*[\"']alert[\"'][^>]*aria-live|aria-live[^>]*role\s*=\s*[\"']alert[\"']"),
         "role=\"alert\" already implies aria-live=\"assertive\" — declaring both is ARIA Soup (A11Y.md §6)"),
        # aria-hidden="true", aria-hidden={true} and the bare JSX boolean `aria-hidden` all hide the
        # image; role="presentation"/"none" on an image that carries an alt is the same defect.
        ("nullified-alt", re.compile(r"<img\b(?=" + ATTRS + r"\balt\s*=\s*[\"'][^\"']+[\"'])" + ATTRS +
                                     r"(?:\baria-hidden(?:\s*=\s*[\"'{]?\s*true|(?=[\s/>]))|\brole\s*=\s*[\"'](?:presentation|none)[\"'])"),
         "aria-hidden or role=\"presentation\" on an image that carries a non-empty alt cancels it for "
         "screen readers while every checker still passes (A11Y.md §6, guide-images.md)"),
        ("media-autoplay", re.compile(r"<(video|audio)\b[^>]*\bautoplay\b(?!\s*[:=]\s*[{\"']?\s*false)", re.I),
         "autoplay declared in the markup cannot be vetoed by prefers-reduced-motion — grant it by "
         "script, mute it, and give it a pause mechanism (SC 2.2.2 / 1.4.2, guide-media.md §3)"),
        ("overlay", re.compile(r"(?:src|href)\s*=\s*[\"'][^\"']*(?:" + "|".join(re.escape(d) for d in OVERLAY_DOMAINS) + r")", re.I),
         "accessibility overlay script — an overlay never fixes the DOM that produced the barrier and "
         "conflicts with the assistive technology the person already configured (A11Y.md §6)"),
    )
    for path in source_files(root, src):
        text = scannable(path)
        if text is None:
            continue
        rel = path.relative_to(root)
        for name, pattern, message in checks:
            for match in pattern.finditer(text):
                level = warn if name in ("outline-none", "media-autoplay") else fail
                level(name, f"{rel}:{line_of(text, match.start())} — {message}", match.group(0))
        # Clickable div/span: onClick, Vue @click / v-on:click, Svelte on:click, Angular (click).
        # A div that replicated a button by hand (role + tabindex) is allowed by §6 — warn, so
        # someone verifies Enter and Space actually work.
        for match in clickable.finditer(text):
            attrs = match.group(2)
            if not click_handler.search(attrs):
                continue
            where = f"{rel}:{line_of(text, match.start())}"
            if re.search(r"\brole\s*=", attrs) and re.search(r"\btabindex\s*=", attrs, re.I):
                warn("clickable-div", f"{where} — clickable <{match.group(1)}> replicating a button by hand: "
                                      f"verify Enter and Space are handled, or use a native <button> (A11Y.md §6)",
                     match.group(0))
            else:
                fail("clickable-div", f"{where} — clickable <{match.group(1)}> — use a native <button> (A11Y.md §6)",
                     match.group(0))


def check_placeholder_labels(root: Path, src: Path) -> None:
    """placeholder as the only label (A11Y.md §6, Placeholder Labels).

    axe accepts a placeholder as an accessible name, so this never fails axe.
    Labeled means: aria-label/aria-labelledby on the field, a <label for> (or
    htmlFor) pointing at its id in the same file, or the field wrapped in a
    <label>. Dynamic ids (`:id`, `id={…}`) cannot be resolved and are skipped.
    """
    field = re.compile(r"<(input|textarea)\b" + ATTRS + r">")
    skip_types = ("hidden", "submit", "button", "reset", "checkbox", "radio", "file", "range", "color", "image")
    for path in source_files(root, src):
        text = scannable(path)
        if text is None or path.suffix in (".css", ".scss", ".js", ".ts"):
            continue
        for match in field.finditer(text):
            attrs = match.group(2)
            if not re.search(r"\bplaceholder\s*=", attrs):
                continue
            kind = re.search(r"\btype\s*=\s*[\"']([\w-]+)", attrs)
            if kind and kind.group(1).lower() in skip_types:
                continue
            if re.search(r"\baria-label(ledby)?\s*=|\btitle\s*=", attrs):
                continue
            if re.search(r"(?<![:\w])id\s*=\s*\{", attrs) or re.search(r":id\s*=|v-bind:id", attrs):
                continue  # dynamic id — not resolvable statically
            id_match = re.search(r"(?<![:\w-])id\s*=\s*[\"']([^\"'{}]+)[\"']", attrs)
            if id_match and re.search(r"\b(?:for|htmlFor)\s*=\s*[\"']" + re.escape(id_match.group(1)) + r"[\"']", text):
                continue
            before = text[:match.start()]
            if before.rfind("<label") > before.rfind("</label>"):
                continue  # wrapped in a <label>
            fail("placeholder-label", f"{path.relative_to(root)}:{line_of(text, match.start())} — "
                                      f"<{match.group(1)}> labeled only by its placeholder. The label disappears "
                                      f"while typing; give it a visible <label> (A11Y.md §6)", match.group(0))


def check_half_climbed(root: Path, src: Path) -> None:
    """A composite ARIA parent without its required children in the same file
    (Half-Climbed ARIA Ladders, A11Y.md §6). Keyboard behavior cannot be
    checked statically; this catches the mold, not the whole ladder."""
    for path in source_files(root, src):
        text = scannable(path)
        if text is None or path.suffix in (".css", ".scss"):
            continue
        roles = set(re.findall(r"\brole\s*=\s*[\"']([\w-]+)[\"']", text))
        for parent, children in COMPOSITES.items():
            native = NATIVE_CHILDREN.get(parent)
            if parent in roles and not any(child in roles for child in children) \
                    and not (native and native.search(text)):
                pos = re.search(r"\brole\s*=\s*[\"']" + parent + r"[\"']", text).start()
                where = f"{path.relative_to(root)}:{line_of(text, pos)}"
                need = "/".join(children)
                if parent == "tablist":
                    fail("half-climbed-aria", f"{where} — role=\"tablist\" with no role=\"tab\" in this file: the "
                                              f"mold that survived two releases. Complete the pattern (role=\"tab\", "
                                              f"aria-selected, arrow keys) or drop the tablist and keep plain buttons "
                                              f"(A11Y.md §6)")
                else:
                    warn("half-climbed-aria", f"{where} — role=\"{parent}\" with no role=\"{need}\" in this file. "
                                              f"If the children live in another component, fine; otherwise the "
                                              f"pattern announces what it does not deliver (A11Y.md §6)")


def check_aria_soup(root: Path, src: Path) -> None:
    """ARIA where native HTML already provides the semantics (A11Y.md §6):
    redundant roles, aria-label repeating the visible text, and aria-expanded
    hardcoded in markup that no script ever toggles."""
    redundant = re.compile(r"<(" + "|".join(REDUNDANT_ROLES) + r"|a)\b" + ATTRS + r">")
    dup_label = re.compile(r"<(a|button)\b" + ATTRS + r"\baria-label\s*=\s*[\"']([^\"']+)[\"']" + ATTRS + r">\s*([^<{]+?)\s*<", re.I)
    static_expanded = re.compile(r"\baria-expanded\s*=\s*[\"'](?:true|false)[\"']")
    dynamic_expanded = re.compile(r"aria-expanded(?!\s*=\s*[\"'](?:true|false)[\"'])|ariaExpanded")

    files = [(p, scannable(p)) for p in source_files(root, src)]
    # The script that toggles aria-expanded rarely lives beside the markup: `--src`
    # scopes the interface, so the search for the toggle spans the whole project.
    toggled = any(p.suffix in SCRIPT_SUFFIXES and dynamic_expanded.search(scannable(p) or "")
                  for p in source_files(root, root))

    for path, text in files:
        if not text or path.suffix in (".css", ".scss"):
            continue
        rel = path.relative_to(root)
        for match in redundant.finditer(text):
            tag, attrs = match.group(1).lower(), match.group(2)
            role = re.search(r"\brole\s*=\s*[\"']([\w-]+)[\"']", attrs)
            if not role:
                continue
            if tag == "a":
                if role.group(1) == "link" and re.search(r"\bhref\s*=", attrs):
                    fail("aria-soup", f"{rel}:{line_of(text, match.start())} — role=\"link\" on <a href>: "
                                      f"redundant role on a native element (ARIA Soup, A11Y.md §6)", match.group(0))
                continue
            if role.group(1) in REDUNDANT_ROLES.get(tag, ()):
                fail("aria-soup", f"{rel}:{line_of(text, match.start())} — role=\"{role.group(1)}\" on <{tag}>: "
                                  f"redundant role on a native element (ARIA Soup, A11Y.md §6)", match.group(0))
        for match in dup_label.finditer(text):
            label, visible = match.group(3), match.group(5)
            if re.sub(r"\s+", " ", label).strip().lower() == re.sub(r"\s+", " ", visible).strip().lower():
                warn("aria-soup", f"{rel}:{line_of(text, match.start())} — aria-label repeats the visible text "
                                  f"of <{match.group(1)}>. Drop it: when the two drift apart it becomes an "
                                  f"SC 2.5.3 failure (ARIA Soup, A11Y.md §6)", match.group(0))
        if not toggled:
            for match in static_expanded.finditer(text):
                warn("aria-soup", f"{rel}:{line_of(text, match.start())} — aria-expanded hardcoded and no script "
                                  f"in the project ever toggles it: a state that never updates is worse than "
                                  f"none (SC 4.1.2, ARIA Soup, A11Y.md §6)", match.group(0))


def check_orphaned_aria(root: Path, src: Path) -> None:
    """An ARIA relationship pointing at an id that is not in the file.

    Only literal values are resolvable statically: `aria-controls={panelId}`
    could be anything at runtime. That dynamic form is exactly where the defect
    hides — two components each calling useId() — so it stays a job for review,
    not for a regex. Reported as a warning: the target may legitimately live in
    another file.
    """
    relations = re.compile(r'\b(aria-controls|aria-labelledby|aria-describedby|aria-activedescendant)'
                           r'\s*=\s*"([^"{}]+)"')
    declared = re.compile(r'\bid\s*=\s*"([^"{}]+)"')
    for path in source_files(root, src):
        text = scannable(path)
        if text is None:
            continue
        ids = set(declared.findall(text))
        for match in relations.finditer(text):
            attribute, value = match.group(1), match.group(2)
            for target in value.split():
                if target not in ids:
                    warn("orphaned-aria",
                         f"{path.relative_to(root)}:{line_of(text, match.start())} — {attribute}=\"{target}\" has no matching "
                         f"id in this file. If the target lives in another component, make sure the id is "
                         f"passed down rather than generated on both sides (A11Y.md §6).", match.group(0))


# --- checks: the interface against its evidence ----------------------------

# A role as markup, JSX, Vue and scripts write it. The field case behind the
# coverage check built its tabs entirely in JavaScript (2026-10-13): a scan of
# `role="…"` alone would have found no tabs at all. `data-role` is not a role.
Q = r"[\"'`]"
ROLE_OF = (r"(?:(?<![\w.-]):?role\s*=\s*(?:\{\s*)?(?:\"'|" + Q + r")"   # role="…"  role={"…"}  :role="'…'"
           r"|(?<![\w-])role\s*:\s*" + Q +                            # { role: "…" }
           r"|setAttribute\(\s*" + Q + r"role" + Q + r"\s*,\s*" + Q +  # el.setAttribute('role', '…')
           r"|\.role\s*=\s*" + Q + r")")                              # el.role = '…'
END = r"(?![\w-])"  # whole names only: <table-row> is a custom element, guide-forms is not guide-form-controls


def tag(name: str) -> str:
    """The element as markup writes it, or as a script creates it: the
    website's figure lightbox is `document.createElement("dialog")`, and its
    only literal `<dialog>` sits in a comment."""
    return r"(?:<" + name + END + r"|createElement\(\s*" + Q + name + Q + r"\s*[,)])"


# An attribute inside an opening tag, quoted values skipped whole: `draggable`
# in a sentence is prose, and so is "popover" inside an alt text.
IN_TAG = r"<[a-z][\w.-]*(?:\"[^\"]*\"|'[^']*'|[^>\"'])*?\s"

# Each guide that ends with an Expected behavior block, and the static
# signatures of the component it covers (the rows of A11Y.md §2.1). Guides
# whose component has no reliable signature in source (charts, maps, consent
# banners, generative UI) are left out: their inventory stays with whoever
# writes the report.
GUIDE_SIGNATURES = {
    "guide-buttons": (tag("button"), ROLE_OF + r"button" + END),
    "guide-navigation": (tag("nav"), tag("main"), ROLE_OF + r"(?:navigation|main)" + END),
    "guide-forms": (tag("form"), tag("textarea"),
                    tag("input") + r"(?![^>]*\btype\s*=\s*[\"'](?:hidden|checkbox|radio|range|submit|button|reset|image|color)[\"'])"),
    "guide-form-controls": (tag("select"), r"\btype\s*=\s*[\"'](?:checkbox|radio|range)[\"']",
                            ROLE_OF + r"(?:switch|checkbox|radiogroup|radio|slider)" + END),
    "guide-modals": (tag("dialog"), ROLE_OF + r"(?:alertdialog|dialog)" + END, r"\baria-modal\b"),
    "guide-tabs-accordion": (ROLE_OF + r"(?:tablist|tabpanel|tab)" + END, tag("details")),
    "guide-tables": (tag("table"), ROLE_OF + r"(?:table|grid|treegrid)" + END),
    "guide-toasts-notifications": (ROLE_OF + r"(?:status|alert)" + END, r"\baria-live\b"),
    "guide-tooltips-popovers": (ROLE_OF + r"tooltip" + END, IN_TAG + r"popover(?:target)?(?=\s*=|[\s>/])"),
    "guide-loading-skeleton": (r"\baria-busy\b",),
    "guide-autocomplete": (ROLE_OF + r"combobox" + END, r"\baria-autocomplete\b", tag("datalist")),
    "guide-carousels-sliders": (r"\baria-roledescription\s*=\s*[\"'](?:carousel|slide)[\"']",),
    "guide-datepicker": (r"\btype\s*=\s*[\"'](?:date|datetime-local|month|week)[\"']",),
    "guide-drag-drop": (IN_TAG + r"draggable(?:\s*=\s*(?:[\"']true[\"']|\{true\}))?(?=[\s>/])",),
    "guide-infinite-scroll": (ROLE_OF + r"feed" + END,),
    "guide-media": (tag("video"), tag("audio"), tag("iframe") + r"[^>]*\b(?:youtube(?:-nocookie)?\.com|player\.vimeo\.com)/"),
    "guide-treeview": (ROLE_OF + r"tree" + END,),
}


def check_guide_coverage(root: Path, report: Path, src: Path) -> None:
    """Every component the interface contains is verified against its guide's
    Expected behavior block (A11Y.md §7, User Flow; REPORT.md §3).

    The inventory comes from the interface, never from the guides opened while
    building it. In the field case behind this check (2026-10-13) the tabs, the
    skip link and the status message of a landing page were built from memory,
    and a report listing "the guides loaded" would have listed none of them.
    A guide counts as covered when §3 names it by its file
    (`guide-tabs-accordion`). The signatures are heuristic, so a missing guide
    warns; a report that claims PASS with one missing fails, because it closes
    a checkpoint the source says is still open.

    Tag names match case-insensitively only in HTML: in JSX, TSX, Vue, Svelte
    and Astro `<Table>` is a component and `Array<Table>` a type, and neither is
    a table. Attribute signatures (`draggable`, `popover`) are not read in plain
    `.js`/`.ts`, where `i<b && draggable` is a comparison.
    """
    body = body_of(report)
    section = re.search(r"^#{2,3}\s*3\.[^\n]*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    named = section.group(1).lower() if section else ""
    claims_pass = status_claims_pass(body)

    seen: dict[str, tuple[str, str]] = {}  # guide → (where, what matched)
    for path in sorted(source_files(root, src)):
        suffix = path.suffix.lower()
        if suffix in (".css", ".scss"):
            continue
        text = scannable(path)
        if not text:
            continue
        flags = re.I if suffix in (".html", ".htm") else 0
        for guide, signatures in GUIDE_SIGNATURES.items():
            if guide in seen:
                continue
            for signature in signatures:
                if signature.startswith(IN_TAG) and suffix in (".js", ".ts"):
                    continue
                match = re.search(signature, text, flags)
                if match:
                    seen[guide] = (f"{path.relative_to(root)}:{line_of(text, match.start())}",
                                   " ".join(match.group(0).split())[:40])
                    break

    for guide, (where, what) in seen.items():
        if re.search(r"(?<![\w-])" + re.escape(guide) + END, named):
            continue
        message = (f"{where} — `{what}`: a component covered by {guide}, and REPORT.md §3 names no "
                   f"scenarios run from it. Run the Expected behavior block of references/{guide}.md and "
                   f"name the guide by its file (A11Y.md §7, User Flow)")
        if claims_pass:
            fail("guide-coverage", message + ". The report claims PASS with this checkpoint open.")
        else:
            warn("guide-coverage", message + ".")


# --- the project's own records ----------------------------------------------

SOURCE_CHECKS = ("positive-tabindex", "outline-none", "redundant-alert", "nullified-alt", "media-autoplay",
                 "overlay", "clickable-div", "placeholder-label", "half-climbed-aria", "aria-soup", "orphaned-aria")
# The source checks a decision may cover. Each one flags a shape that has a
# conformant reading the gate cannot see: role="list" restoring the list
# semantics Safari drops under `list-style: none`, role="alert" doubled with
# aria-live for older screen readers, an outline replaced by a ring that
# survives forced colors, a relationship whose target another component
# renders. The other source checks flag failures, the half-climbed tablist
# among them, and a failure is accepted only in EXCEPTIONS.md, with an owner,
# an approver and an expiry.
CHOICE_CHECKS = ("aria-soup", "redundant-alert", "outline-none", "orphaned-aria")

FINDING_AT = re.compile(r"^(.+?):(\d+) — ")
GATE_FIELD = re.compile(r"(?:Gate finding|Achado do gate):\*{0,2}[ \t]*(.*)", re.I)
DECISION_GATE = re.compile(r"\(gate:\s*`([\w-]+)`\s*[·,]\s*`([^`]+)`\s*\)", re.I)
# The markup a decision chose is one attribute or declaration with its value,
# `role="list"` or `outline: none`. A bare `role` would cover every redundant role.
MARKUP = re.compile(r"[\w:@.-]+\s*[=:]\s*\S.*")
# A sign-off field that names nobody. The agent writes the entry in the same
# turn it accepts the deviation (Exception Memory, §2): an approval still
# pending covers nothing.
UNSIGNED = re.compile(r"^\W*$|^\W*(?:tbd|todo|pending|pendente|awaiting|aguardando|none|nenhum|nenhuma|n/a|"
                      r"a definir|não há|nao ha)\b", re.I)
# An agent does not approve the deviation it introduced (Independent
# Verification, §2, applied to the risk sign-off).
AGENT = re.compile(r"\b(?:ai|ia|llm|agent|agente|bot|claude|chatgpt|gpt|copilot|gemini|codex)\b", re.I)
FENCE = re.compile(r"^```.*?^```", re.M | re.S)


def filled(field: re.Match | None) -> bool:
    """A field with a value that is not the template's bracketed placeholder."""
    return bool(field and field.group(1).strip() and not field.group(1).lstrip().startswith("["))


def as_path(token: str) -> str:
    path = token.strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path.strip("/")


def gate_exceptions(root: Path, src: Path) -> list[tuple[str, list[str], list[str], str, dt.date | None, bool]]:
    """Exceptions that name a gate finding: (label, checks, files, approver, expiry, in force).

    Files are named one by one, from the project root or from --src: a
    directory would cover a whole rule, files created after the sign-off
    included (EXCEPTIONS.md rule 3). In force means complete, signed and not
    expired: an entry whose approver reads "pending" covers nothing.
    """
    path = root / "EXCEPTIONS.md"
    if not path.is_file():
        return []
    entries = exception_entries(root)
    stray = sum(1 for m in GATE_FIELD.finditer(read(path) or "") if filled(m)) \
        - sum(1 for _, block in entries if filled(GATE_FIELD.search(block)))
    if stray > 0:
        warn("registers", f"EXCEPTIONS.md has {stray} Gate finding field(s) outside an entry the gate can read — "
                          f"the template's shape, `### 1. Basic Details` with its own Exception ID, owner, approver, "
                          f"tracking issue and expiry. They cover nothing.")
    found = []
    today = dt.date.today()
    for label, block in entries:
        field = GATE_FIELD.search(block)
        if not filled(field):
            continue  # the field is optional
        tokens = re.findall(r"`([^`]+)`", field.group(1))
        checks = [t for t in tokens if t in SOURCE_CHECKS]
        files, strangers = [], []
        for name in (as_path(t) for t in tokens if t not in SOURCE_CHECKS):
            for base in (root, src):
                if name and (base / name).is_file():
                    files.append((base / name).relative_to(root).as_posix())
                    break
            else:
                strangers.append(name or "(empty)")
        if not checks or not files or strangers:
            warn("registers", f"{label}: the Gate finding field must name at least one check the gate runs and each "
                              f"file it covers, in backticks (`clickable-div` in `src/legacy/Grid.tsx`)"
                              + (f"; not a file in this project: {', '.join(strangers)}" if strangers else "")
                              + ". A directory would cover a whole rule (EXCEPTIONS.md rule 3).")
            if not checks or not files:
                continue
        unsigned = [f for f, pattern in SIGN_OFF
                    if (m := re.search(pattern + r":\*{0,2}[ \t]*(.*)", block)) and UNSIGNED.search(m.group(2).strip())]
        approver = re.search(r"(?:Approved by|Aprovado por):\*{0,2}[ \t]*(.*)", block)
        if approver and AGENT.search(approver.group(1)) and "approver" not in unsigned:
            unsigned.append("approver")
        if unsigned and not missing_fields(block):
            warn("registers", f"{label} names a gate finding but its {' and '.join(unsigned)} name(s) nobody who can "
                              f"sign ('pending', 'TBD', 'none', an AI agent): it covers nothing until a person signs.")
        date = expiry_of(block)
        in_force = not missing_fields(block) and not unsigned and date is not None and date >= today
        found.append((label, checks, files, (approver.group(1).strip() if approver else "")[:40], date, in_force))
    return found


def gate_decisions(root: Path) -> list[tuple[int, str, str]]:
    """Decisions that name a gate check: (line, check, markup chosen).

    Read from the Decisions heading to the end of the file, outside comments,
    code fences, quotes and struck-through lines: the template's rules carry an
    example of the marker, and a copy of the template must not register it in
    every project that adopts it.
    """
    path = root / "A11Y-DECISIONS.md"
    if not path.is_file():
        return []
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    text = FENCE.sub(blank, HTML_COMMENT.sub(blank, read(path) or ""))
    heading = re.search(r"^##\s+(?:Decisions|Decisões)\b", text, re.M)
    if not heading:
        return []
    found = []
    for n, raw in enumerate(text[heading.start():].split("\n"), line_of(text, heading.start())):
        if raw.lstrip().startswith(">") or "~~" in raw:
            continue
        for match in DECISION_GATE.finditer(raw):
            check, markup = match.group(1), match.group(2).strip()
            if check not in SOURCE_CHECKS:
                warn("registers", f"A11Y-DECISIONS.md:{n} names `{check}`, which is not a check this gate runs.")
            elif check not in CHOICE_CHECKS:
                warn("registers", f"A11Y-DECISIONS.md:{n} names `{check}`, which flags a failure, not a choice "
                                  f"between conformant alternatives. Fix it, or accept it in EXCEPTIONS.md with "
                                  f"an owner, an approver and an expiry.")
            elif not MARKUP.fullmatch(markup):
                warn("registers", f"A11Y-DECISIONS.md:{n} names `{markup}`, which is not one attribute or declaration "
                                  f"with its value (`role=\"list\"`, `outline: none`). A fragment would cover every "
                                  f"`{check}` finding in the project.")
            else:
                found.append((n, check, markup))
    return found


def chooses(markup: str, subject: str) -> bool:
    """The flagged element carries the markup the decision chose, whole and as
    its own attribute: `role="list"` is not inside `role="listitem"`, nor
    inside `data-role="list"`, nor inside another attribute's value."""
    norm = lambda t: re.sub(r"\s+", " ", re.sub(r"\s*([=:])\s*", r"\1", t.replace("'", '"')))
    return bool(re.search(r"(?:^|(?<=[\s<{;,(]))" + re.escape(norm(markup)) + r"(?![\w-])", norm(subject)))


def apply_registers(root: Path, src: Path) -> None:
    """What the project already recorded is reported as registered, not failed.

    An exception in force that names the check and the file, or a decision
    that names the check and the markup it chose, turns the source finding it
    covers into a registered line: printed on every run with its record, never
    counted as an error. A decision is matched against the element the check
    flagged, never against its neighbours on the same line. Field case
    (2026-10-03): an adopter retrofitting a site wrapped this gate in a ceiling
    script, because it failed on a role="list" the project had decided in
    A11Y-DECISIONS.md and on violations it had accepted in EXCEPTIONS.md, "so
    demanding zero would bring the gate down without information". The gate
    told them to open the exception, then ignored it. An expired exception
    stops covering, so its findings fail again; one whose finding is gone is
    flagged for closing.
    """
    exceptions = gate_exceptions(root, src)
    decisions = gate_decisions(root)
    if not exceptions and not decisions:
        return
    used: set[int] = set()
    for i, (level, check, message, subject) in enumerate(findings):
        at = FINDING_AT.match(message)
        if level == "REGISTERED" or check not in SOURCE_CHECKS or not at:
            continue
        rel = Path(at.group(1)).as_posix()
        record = None
        for k, (label, checks, files, approver, date, in_force) in enumerate(exceptions):
            if check in checks and rel in files:
                used.add(k)
                if in_force and not record:
                    record = f"EXCEPTIONS.md {label}, approved by {approver}, until {date}"
        if not record and subject:
            record = next((f"A11Y-DECISIONS.md:{n}" for n, chosen, markup in decisions
                           if chosen == check and chooses(markup, subject)), None)
        if record:
            findings[i] = ("REGISTERED", check, f"{message} [{record}]", subject)
    scanned = src.resolve()
    for k, (label, checks, files, _, _, in_force) in enumerate(exceptions):
        if in_force and k not in used and any((root / f).resolve().is_relative_to(scanned) for f in files):
            warn("registers", f"{label} covers {', '.join(f'`{c}`' for c in checks)} in {', '.join(files)}, and this "
                              f"run finds none there. If it was fixed, close the exception.")


# --- runner ----------------------------------------------------------------

def run_checks(root: Path, src: Path) -> None:
    findings.clear()
    report = check_artifacts_exist(root)
    gate_declared = None
    if report:
        check_report_freshness(root, report, src)
        check_report_status(report)
        check_report_independence(report)
        gate_declared = check_report_gate(report)
        check_report_standard_version(report)
        check_contrast_evidence(root, report, src)
        check_guide_coverage(root, report, src)
    check_exceptions(root)
    check_gitignore(root)
    check_source_antipatterns(root, src)
    check_placeholder_labels(root, src)
    check_half_climbed(root, src)
    check_aria_soup(root, src)
    check_orphaned_aria(root, src)
    apply_registers(root, src)

    # The declared outcome must match this run — a stale PASS is the silent
    # failure the Static Gate rule exists to catch.
    if gate_declared is not None:
        found = sum(1 for f in findings if f[0] == "ERROR")
        if re.search(r"NOT RUN|N[ÃA]O RODOU", gate_declared, re.I):
            warn("gate-declared", "REPORT.md declares the static gate NOT RUN, but it is running now — "
                                  "record this run's outcome instead.")
        elif re.search(r"\bPASS\b", gate_declared, re.I) and found:
            fail("gate-declared", f"REPORT.md declares the static gate PASS, but this run found {found} "
                                  f"error(s). Record the real outcome.")


# --- self-test -------------------------------------------------------------

CLEAN_REPORT = """# Report
- **Compliance Status:** ⚠️ CONDITIONAL — screen reader validation pending
- **Verification Independence:** fresh-context — who verified: new session over the repo
- **Static gate (`verify-a11y.py`):** PASS — run on: 2026-09-25
- **Standard version:** 2.1.0
- [x] **Text & UI Contrast:** measured
| body | #1c1b19 | #f7f6f3 | 15.92:1 | 7:1 | ✅ |
- [ ] **Screen reader:** pending
## 3. Behavior and Task Return
- Scenarios run: guide-forms (4/4 passed) · guide-buttons (3/3 passed)
"""
CLEAN_ROW = "| body | #1c1b19 | #f7f6f3 | 15.92:1 | 7:1 | ✅ |"
PASS_REPORT = (CLEAN_REPORT.replace("⚠️ CONDITIONAL — screen reader validation pending", "✅ PASS")
               .replace("- [ ] **Screen reader:** pending", "- [x] **Screen reader:** NVDA 2026.1 + Firefox 141"))
EXCEPTION_ENTRY = """# Exceptions
### 1. Basic Details
- **Exception ID:** EXT-2026-001
- **Risk Owner:** Ana Lima
- **Approved by:** QA lead
- **Tracking Issue:** https://example.com/issues/1
- **Gate finding:** `clickable-div` in `src/legacy.jsx`
### 4. Resolution Plan and Expiry
- **Expiry (review-by date):** 2999-12-31
"""
LIST_DECISION = '- **Unstyled list** → `<ul role="list">` — Safari drops list semantics under list-style: none (gate: `aria-soup` · `role="list"`). (2026-10-20)\n'

SELF_TEST_CASES = [
    # (name, files, expected error checks, expected warning checks, checks that must NOT appear
    #  [, expected registered checks — exactly these, when given])
    ("clean project", {
        "src/index.html": '<label for="q">Search</label><input id="q" placeholder="title"><button>Go</button>'
                          '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT,
    }, set(), set(), {"clickable-div", "placeholder-label", "aria-soup", "contrast-evidence", "gate-declared",
                      "standard-version", "half-climbed-aria", "guide-coverage"}),
    ("clickable div in four syntaxes, hand-made button warns", {
        "src/a.jsx": '<div onClick={() => go()}>x</div>',
        "src/b.vue": '<span @click="go">x</span><div v-on:click="go">y</div>',
        "src/c.svelte": '<div on:click={go}>x</div>',
        "src/d.html": '<div (click)="go()">x</div><div role="button" tabindex="0" onclick="go()">y</div>',
    }, {"clickable-div", "artifacts"}, {"clickable-div"}, set()),
    ("placeholder as the only label", {
        "src/f.html": '<input placeholder="E-mail"><input placeholder="ok" aria-label="Name">'
                      '<label>Wrapped <textarea placeholder="fine"></textarea></label>'
                      '<label for="z">Z</label><input id="z" placeholder="fine">',
    }, {"placeholder-label", "artifacts"}, set(), set()),
    ("half-climbed: tablist without tabs fails, menu without items warns", {
        "src/t.html": '<div role="tablist"><button>1</button></div>',
        "src/m.html": '<ul role="menu"><li>1</li></ul>',
        "src/ok.html": '<div role="tablist"><button role="tab" aria-selected="true">1</button></div>',
    }, {"half-climbed-aria", "artifacts"}, {"half-climbed-aria"}, set()),
    ("aria soup: redundant roles, duplicated label, static aria-expanded", {
        "src/s.html": '<nav role="navigation"></nav><a href="/" role="link">x</a><h2 role="heading">t</h2>'
                      '<button aria-label="Close">Close</button><button aria-expanded="false">Menu</button>',
    }, {"aria-soup", "artifacts"}, {"aria-soup"}, set()),
    ("aria-expanded toggled by script is not soup", {
        "src/s.html": '<button aria-expanded="false">Menu</button>',
        "src/s.js": 'btn.setAttribute("aria-expanded", String(open))',
    }, {"artifacts"}, set(), {"aria-soup"}),
    ("aria-expanded toggled by a script outside --src is not soup either", {
        "src/s.html": '<button aria-expanded="false">Menu</button>',
        "js/main.js": 'btn.setAttribute("aria-expanded", String(open))',
    }, {"artifacts"}, set(), {"aria-soup"}),
    ("markup quoted in <pre>/<code> is documentation, not a component", {
        "src/doc.html": '<p>Avoid <code>role="menu"</code> on site navigation.</p>'
                        '<pre><code>&lt;div role="tablist"&gt;</code></pre>'
                        '<pre>\n<div role="tablist"><button>1</button></div>\n<div onclick="x()">y</div>\n</pre>'
                        '<div role="tablist"><button role="tab" aria-selected="true">real</button></div>',
    }, {"artifacts"}, set(), {"half-climbed-aria", "clickable-div", "aria-soup"}),
    ("comments are documentation, not markup", {
        "src/c.tsx": '// role="menu" lives on the Dropdown, with its menuitems\n'
                     '{/* aria-live="polite" is implied by role="alert" */}<p role="alert">Saved</p>\n'
                     '/* outline: none would hide focus */\n'
                     'const url = "https://example.com/x";\n'
                     '<div role="tablist"><button role="tab" aria-selected="true">1</button></div>',
        "src/c.css": '/* outline: none */ a:focus { outline: 2px solid }',
        "src/h.html": '<!-- <div onclick="x()">old</div> --><button>ok</button>',
    }, {"artifacts"}, set(), {"half-climbed-aria", "redundant-alert", "outline-none", "clickable-div"}),
    ("native children satisfy a composite: radios under radiogroup, rows under grid", {
        "src/r.html": '<fieldset role="radiogroup" aria-label="Plan"><label><input type="radio" name="p"> A</label></fieldset>'
                      '<table role="grid"><tr><td>1</td></tr></table>',
    }, {"artifacts"}, set(), {"half-climbed-aria"}),
    ("a comment does not hide the real markup after it", {
        "src/m.html": '<!-- the menu below needs menuitems -->\n<ul role="menu"><li>1</li></ul>',
    }, {"artifacts"}, {"half-climbed-aria"}, set()),
    ("standard version: missing field warns", {
        "src/index.html": '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT.replace("- **Standard version:** 2.1.0\n", ""),
    }, set(), {"standard-version"}, {"gate-declared"}),
    ("standard version: placeholder left in place fails", {
        "src/index.html": '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT.replace("- **Standard version:** 2.1.0",
                                          "- **Standard version:** [e.g. 2.1.0 — the Version line at the top of A11Y.md]"),
    }, {"standard-version", "gate-declared"}, set(), set()),
    ("nullified alt: bare JSX aria-hidden and role=presentation", {
        "src/i.jsx": '<img alt="Chart" aria-hidden /><img alt="Map" role="presentation" />'
                     '<img alt="" aria-hidden="true" />',
    }, {"nullified-alt", "artifacts"}, set(), set()),
    ("overlay vendor script", {
        "src/index.html": '<script src="https://cdn.userway.org/widget.js"></script>',
    }, {"overlay", "artifacts"}, set(), set()),
    # A report that declares the gate PASS while a contrast row fails also trips
    # gate-declared — that is the point of the gate field, so both are expected.
    ("contrast: invented ratio fails", {
        "src/index.html": '<style>.a{color:#767676;background:#ffffff}</style>',
        "REPORT.md": CLEAN_REPORT.replace(CLEAN_ROW, "| body | #767676 | #ffffff | 7.20:1 | 7:1 | ✅ |"),
    }, {"contrast-evidence", "gate-declared"}, set(), set()),
    ("contrast: honest ratio marked passing below floor fails", {
        "src/index.html": '<style>.a{color:#767676;background:#ffffff}</style>',
        "REPORT.md": CLEAN_REPORT.replace(CLEAN_ROW, "| body | #767676 | #ffffff | 4.54:1 | 7:1 | ✅ |"),
    }, {"contrast-evidence", "gate-declared"}, set(), set()),
    ("contrast: a failing pair recorded honestly only warns", {
        "src/index.html": '<style>.a{color:#767676;background:#ffffff}</style>',
        "REPORT.md": CLEAN_REPORT.replace(CLEAN_ROW, "| body | #767676 | #ffffff | 4.54:1 | 7:1 | ❌ |"),
    }, set(), {"contrast-evidence"}, {"gate-declared"}),
    ("contrast: a sentence mentioning two colors and a floor is not a row", {
        "src/index.html": '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT + "\nNote: #8f8f8f and #a6a6a6 are decorative rails, outside the 7:1 floor.\n",
    }, set(), set(), {"contrast-evidence"}),
    ("contrast: checkpoint verified without a single pair fails", {
        "src/index.html": '<p>x</p>',
        "REPORT.md": CLEAN_REPORT.replace(CLEAN_ROW, ""),
    }, {"contrast-evidence", "gate-declared"}, set(), set()),
    ("gate declared PASS while this run finds errors", {
        "src/a.html": '<div onclick="x()">x</div>',
        "REPORT.md": CLEAN_REPORT,
    }, {"gate-declared", "clickable-div"}, set(), set()),
    ("gate declared NOT RUN while running warns", {
        "src/index.html": '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT.replace("PASS — run on: 2026-09-25", "NOT RUN — reason: no shell"),
    }, set(), {"gate-declared"}, set()),
    ("guide coverage: tabs built by script and a status message warn; a guide named outside §3 does not count", {
        "src/index.html": '<p role="status"></p><style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "src/tabs.js": "list.setAttribute('role', 'tablist');\ntab.setAttribute('role', 'tab');\n",
        "REPORT.md": CLEAN_REPORT + "\n## Assessment Notes\n- guide-tabs-accordion and guide-toasts-notifications: next session\n",
    }, set(), {"guide-coverage"}, {"gate-declared"}),
    ("guide coverage: a PASS report missing a present component's guide fails", {
        "src/index.html": '<dialog open><button>Close</button></dialog><style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": PASS_REPORT,
    }, {"guide-coverage", "gate-declared"}, set(), set()),
    ("guide coverage: named guides satisfy; quoted, commented and prose mentions are not components", {
        "src/index.html": '<div role="tablist"><button role="tab" aria-selected="true">1</button></div>'
                          '<p>Drag a draggable card; a popover explains it.</p>'
                          '<pre><video src="a.mp4"></video></pre><!-- <dialog open></dialog> -->'
                          '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT.replace("guide-forms (4/4 passed)", "guide-tabs-accordion (5/5 passed)"),
    }, set(), set(), {"guide-coverage"}),
    ("guide coverage: React components, TS generics, custom elements, data-role and attribute values are not components", {
        "src/a.tsx": 'const [d, setD] = useState<Dialog | null>(null)\nconst rows: Array<Table> = []\n'
                     'return <Table rows={rows}><Form onSubmit={go} /></Table>',
        "src/b.html": '<table-row></table-row><video-player></video-player><div data-role="tab"></div>'
                      '<img alt="a popover and a tooltip" src="x.png"><style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "src/c.js": 'for (let i = 0; i<b && draggable; i++) {}',
        "REPORT.md": CLEAN_REPORT,
    }, set(), set(), {"guide-coverage"}),
    ("guide coverage: roles in JSX braces, Vue bindings and object props, and elements a script creates, are found", {
        "src/a.tsx": '<div role={"tablist"}><button role="tab" aria-selected="true">1</button></div>',
        "src/b.vue": '<template><div :role="\'tree\'"></div></template>',
        "src/c.js": 'h("div", { role: "feed" })\nconst dlg = document.createElement("dialog")',
        "src/index.html": '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT,
    }, set(), {"guide-coverage"}, {"gate-declared"}),
    ("registers: an exception in force covers its file; the same finding elsewhere fails", {
        "src/legacy.jsx": '<div onClick={go}>x</div>',
        "src/new.jsx": '<div onClick={go}>y</div>',
        "EXCEPTIONS.md": EXCEPTION_ENTRY,
    }, {"clickable-div", "artifacts"}, set(), set(), {"clickable-div"}),
    ("registers: an expired exception covers nothing", {
        "src/legacy.jsx": '<div onClick={go}>x</div>',
        "EXCEPTIONS.md": EXCEPTION_ENTRY.replace("2999-12-31", "2020-01-01"),
    }, {"clickable-div", "exceptions", "artifacts"}, set(), set(), set()),
    ("registers: an exception whose finding is gone warns to close it", {
        "src/legacy.jsx": '<button onClick={go}>x</button>',
        "EXCEPTIONS.md": EXCEPTION_ENTRY,
    }, {"artifacts"}, {"registers"}, set(), set()),
    ("registers: a decision covers the markup it chose across a multi-line tag; markers in the rules and in comments are not read", {
        "src/l.jsx": '<ul\n  className="plain"\n  role="list">\n  <li>a</li>\n</ul>\n<nav role="navigation"></nav>',
        "A11Y-DECISIONS.md": "# Decisions Log\n## Rules for the AI\n8. Mark it like (gate: `aria-soup` · `role=\"navigation\"`).\n"
                             "## Decisions\n<!-- (gate: `aria-soup` · `role=\"navigation\"`) -->\n" + LIST_DECISION,
    }, {"aria-soup", "artifacts"}, set(), set(), {"aria-soup"}),
    ("registers: a decision cannot cover a failure, the half-climbed tablist included", {
        "src/a.jsx": '<div onClick={go}>x</div>',
        "src/t.html": '<div role="tablist"><button>1</button></div>',
        "A11Y-DECISIONS.md": "## Decisions\n- **Card** → the whole card is clickable (gate: `clickable-div` · `onClick`)\n"
                             "- **Tabs** → buttons only (gate: `half-climbed-aria` · `role=\"tablist\"`)\n",
    }, {"clickable-div", "half-climbed-aria", "artifacts"}, {"registers"}, set(), set()),
    ("registers: a decision covers the element the check flagged, not its neighbour on the same line", {
        "src/a.html": '<nav role="navigation"><ul role="list"><li>a</li></ul></nav>',
        "A11Y-DECISIONS.md": "## Decisions\n" + LIST_DECISION,
    }, {"aria-soup", "artifacts"}, set(), set(), {"aria-soup"}),
    ("registers: a decision matches whole markup only; a bare fragment covers nothing", {
        "src/a.html": '<ul><li role="listitem" data-role="list">a</li></ul>',
        "A11Y-DECISIONS.md": "## Decisions\n" + LIST_DECISION + "- **Anything** → loose (gate: `aria-soup` · `role`)\n",
    }, {"aria-soup", "artifacts"}, {"registers"}, set(), set()),
    ("registers: a directory, a pending or AI approver and a field outside the template's shape cover nothing", {
        "src/legacy.jsx": '<div onClick={go}>x</div>',
        "EXCEPTIONS.md": "**Common fields**\n- **Gate finding:** `clickable-div` in `src/legacy.jsx`\n"
                         + EXCEPTION_ENTRY.replace("`src/legacy.jsx`", "`src`").split("\n", 1)[1]
                         + EXCEPTION_ENTRY.replace("EXT-2026-001", "EXT-2026-002")
                                          .replace("QA lead", "pending — awaiting sign-off").split("\n", 1)[1]
                         + EXCEPTION_ENTRY.replace("EXT-2026-001", "EXT-2026-003")
                                          .replace("QA lead", "Claude (AI agent)").split("\n", 1)[1],
    }, {"clickable-div", "artifacts"}, {"registers"}, set(), set()),
    ("registers: ./ and backslash paths, paths from --src, and an entry renewed after an expired one", {
        "src/legacy.jsx": '<div onClick={go}>x</div>',
        "src/other.jsx": '<div onClick={go}>y</div>',
        "EXCEPTIONS.md": EXCEPTION_ENTRY.replace("2999-12-31", "2020-01-01")
                         + EXCEPTION_ENTRY.replace("EXT-2026-001", "EXT-2026-002")
                                          .replace("`src/legacy.jsx`", "`.\\legacy.jsx` and `./src/other.jsx`")
                                          .split("\n", 1)[1],
    }, {"exceptions", "artifacts"}, set(), {"clickable-div"}, {"clickable-div"}),
    ("registers: a report declaring the gate PASS holds when every finding is registered", {
        "src/index.html": '<ul role="list"><li>a</li></ul><style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "A11Y-DECISIONS.md": "## Decisions\n" + LIST_DECISION,
        "REPORT.md": CLEAN_REPORT,
    }, set(), set(), {"gate-declared", "aria-soup"}, {"aria-soup"}),
]


def self_test() -> int:
    """Built-in fixtures: one temp project per case, each check asserted by name."""
    ok = True
    for name, files, want_err, want_warn, forbid, *want_reg in SELF_TEST_CASES:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, content in files.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            run_checks(root, root / "src")
            errs = {c for lvl, c, *_ in findings if lvl == "ERROR"}
            warns = {c for lvl, c, *_ in findings if lvl == "WARN"}
            regs = {c for lvl, c, *_ in findings if lvl == "REGISTERED"}
            seen = errs | warns
            missing = (want_err - errs) | (want_warn - warns)
            unexpected = (forbid & seen) | (errs - want_err - want_warn)
            if want_reg:
                missing |= want_reg[0] - regs
                unexpected |= regs - want_reg[0]
            passed = not missing and not unexpected
            ok &= passed
            print(f"  {'✓' if passed else '✗'} {name}")
            if not passed:
                for lvl, c, m, _ in findings:
                    print(f"      {lvl} [{c}] {m[:110]}")
                if missing:
                    print(f"      missing: {sorted(missing)}")
                if unexpected:
                    print(f"      unexpected: {sorted(unexpected)}")
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# --- main ------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", default=".", help="project root (default: current directory)")
    parser.add_argument("--src", default=None, help="subdirectory holding the interface source (default: project root)")
    parser.add_argument("--warn-only", action="store_true", help="always exit 0, printing findings only")
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixture cases and exit")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    src = (root / args.src).resolve() if args.src else root

    run_checks(root, src)

    errors = [f for f in findings if f[0] == "ERROR"]
    warnings = [f for f in findings if f[0] == "WARN"]
    registered = [f for f in findings if f[0] == "REGISTERED"]
    for level, check, message, _ in errors + warnings + registered:
        marker = {"ERROR": "✗", "WARN": "!"}.get(level, "·")
        print(f"{marker} [{check}] {message}")

    # Registered findings never fail the run, and never leave the output either:
    # an exception is "never silently suppressed" (EXCEPTIONS.md rule 4).
    also = f", {len(registered)} registered" if registered else ""
    print()
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s){also}.")
    elif warnings or registered:
        print(f"PASS with {len(warnings)} warning(s){also}.")
    else:
        print("PASS — nothing statically detectable is wrong.")
    print("This is not a conformance claim: the human checkpoints in REPORT.md are what establish it.")
    # The line the agent records — so the outcome never has to be remembered (Static Gate, §2).
    verdict = "FAIL" if errors else "PASS"
    print(f"Record in REPORT.md → Static gate (verify-a11y.py): {verdict} "
          f"({len(errors)} error(s), {len(warnings)} warning(s){also}) — run on: {dt.date.today().isoformat()}")

    return 1 if errors and not args.warn_only else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
verify-a11y.py — static gate for projects adopting the A11Y.md standard.

Checks what can be verified without a browser: that the project artifacts
exist, are current and well-formed, that the evidence they carry adds up
(the contrast ratios recorded in REPORT.md are recomputed, never trusted),
and that the source is free of the anti-patterns a text search can catch —
the ones axe cannot see because they live in handlers, CSS intent or source
that has not been rendered yet. Exits non-zero when a check fails, so it can
gate a build. Every run ends with the line to record in the report's Static
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


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


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


def check_exceptions(root: Path) -> None:
    """Every exception needs owner, approver, tracking issue and a future expiry."""
    path = root / "EXCEPTIONS.md"
    if not path.is_file():
        return  # only required once a deviation is accepted
    text = read(path) or ""
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
        text = read(path)
        if text is None:
            continue
        rel = path.relative_to(root)
        for name, pattern, message in checks:
            for match in pattern.finditer(text):
                level = warn if name in ("outline-none", "media-autoplay") else fail
                level(name, f"{rel}:{line_of(text, match.start())} — {message}")
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
                                      f"verify Enter and Space are handled, or use a native <button> (A11Y.md §6)")
            else:
                fail("clickable-div", f"{where} — clickable <{match.group(1)}> — use a native <button> (A11Y.md §6)")


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
        text = read(path)
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
                                      f"while typing; give it a visible <label> (A11Y.md §6)")


def check_half_climbed(root: Path, src: Path) -> None:
    """A composite ARIA parent without its required children in the same file
    (Half-Climbed ARIA Ladders, A11Y.md §6). Keyboard behavior cannot be
    checked statically; this catches the mold, not the whole ladder."""
    for path in source_files(root, src):
        text = read(path)
        if text is None or path.suffix in (".css", ".scss"):
            continue
        roles = set(re.findall(r"\brole\s*=\s*[\"']([\w-]+)[\"']", text))
        for parent, children in COMPOSITES.items():
            if parent in roles and not any(child in roles for child in children):
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

    files = [(p, read(p)) for p in source_files(root, src)]
    toggled = any(t and p.suffix in SCRIPT_SUFFIXES and dynamic_expanded.search(t) for p, t in files)

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
                                      f"redundant role on a native element (ARIA Soup, A11Y.md §6)")
                continue
            if role.group(1) in REDUNDANT_ROLES.get(tag, ()):
                fail("aria-soup", f"{rel}:{line_of(text, match.start())} — role=\"{role.group(1)}\" on <{tag}>: "
                                  f"redundant role on a native element (ARIA Soup, A11Y.md §6)")
        for match in dup_label.finditer(text):
            label, visible = match.group(3), match.group(5)
            if re.sub(r"\s+", " ", label).strip().lower() == re.sub(r"\s+", " ", visible).strip().lower():
                warn("aria-soup", f"{rel}:{line_of(text, match.start())} — aria-label repeats the visible text "
                                  f"of <{match.group(1)}>. Drop it: when the two drift apart it becomes an "
                                  f"SC 2.5.3 failure (ARIA Soup, A11Y.md §6)")
        if not toggled:
            for match in static_expanded.finditer(text):
                warn("aria-soup", f"{rel}:{line_of(text, match.start())} — aria-expanded hardcoded and no script "
                                  f"in the project ever toggles it: a state that never updates is worse than "
                                  f"none (SC 4.1.2, ARIA Soup, A11Y.md §6)")


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
        text = read(path)
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
                         f"passed down rather than generated on both sides (A11Y.md §6).")


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
        check_contrast_evidence(root, report, src)
    check_exceptions(root)
    check_gitignore(root)
    check_source_antipatterns(root, src)
    check_placeholder_labels(root, src)
    check_half_climbed(root, src)
    check_aria_soup(root, src)
    check_orphaned_aria(root, src)

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
- [x] **Text & UI Contrast:** measured
| body | #1c1b19 | #f7f6f3 | 15.92:1 | 7:1 | ✅ |
- [ ] **Screen reader:** pending
"""
CLEAN_ROW = "| body | #1c1b19 | #f7f6f3 | 15.92:1 | 7:1 | ✅ |"

SELF_TEST_CASES = [
    # (name, files, expected error checks, expected warning checks, checks that must NOT appear)
    ("clean project", {
        "src/index.html": '<label for="q">Search</label><input id="q" placeholder="title"><button>Go</button>'
                          '<style>.a{color:#1c1b19;background:#f7f6f3}</style>',
        "REPORT.md": CLEAN_REPORT,
    }, set(), set(), {"clickable-div", "placeholder-label", "aria-soup", "contrast-evidence", "gate-declared"}),
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
]


def self_test() -> int:
    """Built-in fixtures: one temp project per case, each check asserted by name."""
    ok = True
    for name, files, want_err, want_warn, forbid in SELF_TEST_CASES:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, content in files.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            run_checks(root, root / "src")
            errs = {c for lvl, c, _ in findings if lvl == "ERROR"}
            warns = {c for lvl, c, _ in findings if lvl == "WARN"}
            seen = errs | warns
            missing = (want_err - errs) | (want_warn - warns)
            unexpected = (forbid & seen) | (errs - want_err - want_warn)
            passed = not missing and not unexpected
            ok &= passed
            print(f"  {'✓' if passed else '✗'} {name}")
            if not passed:
                for lvl, c, m in findings:
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
    # The line the agent records — so the outcome never has to be remembered (Static Gate, §2).
    verdict = "FAIL" if errors else "PASS"
    print(f"Record in REPORT.md → Static gate (verify-a11y.py): {verdict} "
          f"({len(errors)} error(s), {len(warnings)} warning(s)) — run on: {dt.date.today().isoformat()}")

    return 1 if errors and not args.warn_only else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
lint-standard.py — integrity checks for the A11Y.md standard itself.

Written after a field post-mortem in which an agent applied the standard for
weeks and never produced two of its three artifacts. The cause was not a
missing MUST: it was a MUST living outside the AI Behavior Contract, and an
index label ("Optional Templates") contradicting the normative body. Those
are defects a script can catch, so it should.

Checks:
  parity        docs/en and docs/pt-BR hold the same files, headings and rules
  orphans       every references/guide-*.md is reachable from the core file
  triggers      every guide and template has a stated loading trigger in the
                §2.1 map — reachable is not the same as discoverable
  links         relative links in the core and templates resolve on disk
  phase-trigger no rule fires on a project phase ("at final delivery") instead
                of an event — continuous delivery never reaches a phase
  optional      the project artifacts are not labelled optional anywhere
  wiki          the Wiki documents the same number of contract rules as the
                core file and lists every reference guide (skipped if absent)

Usage: python3 lint-standard.py [REPO_ROOT]
Stdlib only, no dependencies.
"""

import re
import sys
from pathlib import Path

LANGS = ("en", "pt-BR")
findings: list[tuple[str, str]] = []


def fail(check: str, message: str) -> None:
    findings.append((check, message))


def core(root: Path, lang: str) -> Path:
    return root / "docs" / lang / "A11Y.md"


def check_parity(root: Path) -> None:
    listings = {}
    for lang in LANGS:
        base = root / "docs" / lang
        listings[lang] = {p.relative_to(base).as_posix() for p in base.rglob("*.md")}
    only_en = listings["en"] - listings["pt-BR"]
    only_pt = listings["pt-BR"] - listings["en"]
    for name in sorted(only_en):
        fail("parity", f"docs/en/{name} has no pt-BR counterpart")
    for name in sorted(only_pt):
        fail("parity", f"docs/pt-BR/{name} has no en counterpart")

    counts = {}
    for lang in LANGS:
        text = core(root, lang).read_text(encoding="utf-8")
        contract = re.search(r"## 2\..*?(?=\n## 3\.)", text, re.S)
        counts[lang] = (
            len(re.findall(r"^#{1,6} ", text, re.M)),
            len(re.findall(r"^- \*\*", contract.group(0), re.M)) if contract else 0,
        )
    if counts["en"][0] != counts["pt-BR"][0]:
        fail("parity", f"heading count differs: en={counts['en'][0]} pt-BR={counts['pt-BR'][0]}")
    if counts["en"][1] != counts["pt-BR"][1]:
        fail("parity", f"AI Behavior Contract rule count differs: "
                       f"en={counts['en'][1]} pt-BR={counts['pt-BR'][1]}")


def check_orphans(root: Path) -> None:
    for lang in LANGS:
        text = core(root, lang).read_text(encoding="utf-8")
        linked = set(re.findall(r"guide-[a-z0-9-]+\.md", text))
        on_disk = {p.name for p in (root / "docs" / lang / "references").glob("guide-*.md")}
        for orphan in sorted(on_disk - linked):
            fail("orphans", f"docs/{lang}/references/{orphan} is not linked from the core file — "
                            f"lazy loading can never discover it")


def check_triggers(root: Path) -> None:
    """Reachability is not discoverability.

    check_orphans proves a guide is linked somewhere in the core file. It does
    not prove the agent knows *when* to open it. Under Lazy Context Loading the
    references are never preloaded, so a guide whose trigger is not stated is a
    guide that only gets found by guessing the filename. Every guide and every
    template must appear in the §2.1 loading map.
    """
    for lang in LANGS:
        text = core(root, lang).read_text(encoding="utf-8")
        section = re.search(r"## 2\.1\..*?(?=\n## 3\.)", text, re.S)
        if not section:
            fail("triggers", f"docs/{lang}/A11Y.md has no §2.1 loading map")
            continue
        mapped = set(re.findall(r"(?:guide-[a-z0-9-]+|REPORT|EXCEPTIONS|A11Y-DECISIONS)\.md",
                                section.group(0)))
        expected = {p.name for p in (root / "docs" / lang / "references").glob("guide-*.md")}
        expected |= {p.name for p in (root / "docs" / lang / "templates").glob("*.md")}
        for missing in sorted(expected - mapped):
            fail("triggers", f"docs/{lang}: {missing} has no trigger in the §2.1 loading map — "
                             f"lazy loading can reach it, but nothing says when to open it")


def check_links(root: Path) -> None:
    for lang in LANGS:
        base = root / "docs" / lang
        for path in [core(root, lang)] + sorted(base.glob("templates/*.md")) + sorted(base.glob("references/*.md")):
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\((?!https?:|#|mailto:)([^)]+)\)", text):
                resolved = (path.parent / target.split("#")[0]).resolve()
                if not resolved.exists():
                    fail("links", f"{path.relative_to(root)} → broken relative link '{target}'")


def check_phase_triggers(root: Path) -> None:
    """Phase triggers never fire in continuously delivered projects."""
    patterns = (
        re.compile(r"(in case of|at|on|upon)\s+final\s+delivery", re.I),
        re.compile(r"em caso de entrega final|na entrega final", re.I),
        re.compile(r"(at|during)\s+(the\s+)?(final\s+)?QA cycle", re.I),
        re.compile(r"no ciclo de QA", re.I),
    )
    for path in sorted((root / "docs").rglob("*.md")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            # the design principle in the governance guide quotes these on purpose
            if "gatilhos por fase" in line or "phase triggers" in line:
                continue
            for pattern in patterns:
                if pattern.search(line):
                    fail("phase-trigger",
                         f"{path.relative_to(root)}:{line_no} — rule fires on a project phase, not an event. "
                         f"Use 'before any delivery to an end user' (see Release Evidence, §2).")


def check_wiki_drift(root: Path) -> None:
    """The Wiki is the project's public documentation but lives outside version
    control (see .gitignore), so nothing stops it from drifting away from the
    standard it documents. Skipped when the folder is absent — most clones
    will not have it."""
    wiki = root / "WIKI"
    if not wiki.is_dir():
        return

    contract = re.search(r"## 2\..*?(?=\n## 3\.)", core(root, "en").read_text(encoding="utf-8"), re.S)
    core_rules = len(re.findall(r"^- \*\*", contract.group(0), re.M)) if contract else 0
    page = wiki / "AI-Behavioral-Contract.md"
    if page.is_file():
        wiki_rules = len(re.findall(r"^### \d+\. ", page.read_text(encoding="utf-8"), re.M))
        if wiki_rules != core_rules:
            fail("wiki", f"WIKI/AI-Behavioral-Contract.md documents {wiki_rules} rules, "
                         f"the core file defines {core_rules}")

    library = wiki / "Reference-Library.md"
    if library.is_file():
        listed = set(re.findall(r"guide-[a-z0-9-]+\.md", library.read_text(encoding="utf-8")))
        on_disk = {p.name for p in (root / "docs" / "en" / "references").glob("guide-*.md")}
        for missing in sorted(on_disk - listed):
            fail("wiki", f"WIKI/Reference-Library.md does not list {missing}")


def check_optional_label(root: Path) -> None:
    for path in sorted((root / "docs").rglob("*.md")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"(Optional Templates|Templates Opcionais)", line):
                fail("optional",
                     f"{path.relative_to(root)}:{line_no} — project artifacts labelled optional while the "
                     f"body requires them. This exact contradiction caused the 2026-08-01 field failure.")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not core(root, "en").is_file():
        print(f"error: {root} does not look like the A11Y.md repository", file=sys.stderr)
        return 2

    for check in (check_parity, check_orphans, check_triggers, check_links,
                  check_phase_triggers, check_optional_label, check_wiki_drift):
        check(root)

    for name, message in findings:
        print(f"✗ [{name}] {message}")
    print()
    print(f"FAIL — {len(findings)} issue(s)." if findings else "PASS — standard is internally consistent.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

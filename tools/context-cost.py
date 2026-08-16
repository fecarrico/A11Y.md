#!/usr/bin/env python3
"""
context-cost.py — what the standard actually costs in context, per task type.

A11Y.md is loaded lazily: the core is always read, and the reference guides are
consulted one at a time, per the Loading Triggers map in §2.1. So "how much
context does the standard cost" has no single answer — it has one answer per
task type. This script computes all of them, reading the trigger map out of the
core file itself, so it stays correct when the map changes.

It also compares two versions, which is how a release note earns the right to
claim a reduction:

    python3 context-cost.py --compare v1.7.0

A core that slims while its guides deepen does not save the same amount on every
task — it saves the most where no guide applies, and the least where the guide
absorbed what the core gave up. The per-task table shows which.

Characters are counted exactly. Tokens are an ESTIMATE from a fixed divisor: the
ratio between two versions is trustworthy (the bias cancels on both sides), an
absolute cost in currency is not. For that, count tokens with the model
provider's own endpoint.

Usage:
    python3 context-cost.py [--lang en|pt-BR] [--compare GIT_REF]
                            [--markdown] [--chars-per-token N]

Stdlib only, no dependencies.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Rough average for English/Portuguese markdown with heavy inline formatting.
# Only affects the token column; every ratio in this script is computed on
# characters and is unaffected by this number.
DEFAULT_CHARS_PER_TOKEN = 3.8

SECTION_START = re.compile(r"^##\s*2\.1\.", re.M)
TEMPLATES_MARK = re.compile(r"^\*\*Templates", re.M)
GUIDE_LINK = re.compile(r"\(references/([A-Za-z0-9._-]+\.md)\)")
NO_GUIDE_LABEL = "— no guide applies —"


class Source:
    """Reads the docs tree either from the working directory or from a git ref."""

    def __init__(self, root: Path, lang: str, ref: str | None = None):
        self.root = root
        self.lang = lang
        self.ref = ref

    @property
    def label(self) -> str:
        return self.ref or "working tree"

    def read(self, relative: str) -> str | None:
        path = f"docs/{self.lang}/{relative}"
        if self.ref is None:
            file = self.root / path
            return file.read_text(encoding="utf-8") if file.is_file() else None
        result = subprocess.run(
            ["git", "-C", str(self.root), "show", f"{self.ref}:{path}"],
            capture_output=True, text=True,
        )
        return result.stdout if result.returncode == 0 else None


def parse_triggers(core: str) -> list[tuple[str, list[str]]]:
    """Extract (trigger description, [guide filenames]) from the §2.1 table.

    Stops at the Templates block: templates load on lifecycle events, not on
    component type, so they are not part of a task's per-generation cost.
    """
    start = SECTION_START.search(core)
    if not start:
        return []
    body = core[start.end():]
    end = TEMPLATES_MARK.search(body)
    if end:
        body = body[:end.start()]

    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- :"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        guides = GUIDE_LINK.findall(cells[-1])
        if not guides:  # header row, or a row that points nowhere
            continue
        trigger = re.sub(r"`([^`]*)`", r"\1", cells[0])
        rows.append((trigger, guides))
    return rows


def measure(source: Source):
    """Return (core_size, [(label, trigger, guide_size, total_size)]) for one version."""
    core = source.read("A11Y.md")
    if core is None:
        return None, []
    core_size = len(core)

    seen, scenarios = set(), []
    for trigger, guides in parse_triggers(core):
        key = tuple(guides)
        if key in seen:
            continue
        seen.add(key)

        total_guide = 0
        missing = []
        for guide in guides:
            content = source.read(f"references/{guide}")
            if content is None:
                missing.append(guide)
            else:
                total_guide += len(content)

        label = " + ".join(g.replace("guide-", "").replace(".md", "") for g in guides)
        if missing:
            label += f"  [!{len(missing)} ausente(s)]"
        scenarios.append((label, trigger, total_guide, core_size + total_guide))

    scenarios.sort(key=lambda row: row[3])
    scenarios.insert(0, (NO_GUIDE_LABEL, "core alone is enough", 0, core_size))
    return core_size, scenarios


def tokens(chars: int, divisor: float) -> int:
    return round(chars / divisor)


def render(rows, headers, markdown: bool) -> str:
    widths = [max(len(str(r[i])) for r in [headers, *rows]) for i in range(len(headers))]
    sep = " | " if markdown else "  "
    edge = "| " if markdown else ""
    tail = " |" if markdown else ""

    def line(cells):
        padded = []
        for i, cell in enumerate(cells):
            text = str(cell)
            padded.append(text.ljust(widths[i]) if i == 0 else text.rjust(widths[i]))
        return edge + sep.join(padded) + tail

    out = [line(headers)]
    if markdown:
        out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    else:
        out.append("  ".join("-" * w for w in widths))
    out.extend(line(r) for r in rows)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Per-task context cost of the A11Y.md standard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lang", default="en", choices=("en", "pt-BR"))
    parser.add_argument("--compare", metavar="GIT_REF",
                        help="compare against another version (tag, branch or commit)")
    parser.add_argument("--at", metavar="GIT_REF",
                        help="measure this version instead of the working tree; "
                             "with --compare, gives a release's own figure, free of "
                             "whatever landed after it")
    parser.add_argument("--markdown", action="store_true",
                        help="emit a markdown table, ready to paste into the wiki")
    parser.add_argument("--chars-per-token", type=float, default=DEFAULT_CHARS_PER_TOKEN)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()

    now = Source(args.root, args.lang, args.at)
    core_now, rows_now = measure(now)
    if core_now is None:
        print(f"error: docs/{args.lang}/A11Y.md not found at {now.label}", file=sys.stderr)
        return 2
    if len(rows_now) == 1:
        print("error: no Loading Triggers table found in §2.1 — has the section moved?",
              file=sys.stderr)
        return 2

    div = args.chars_per_token

    if not args.compare:
        headers = ["Task loads", "Guide (chars)", "Total (chars)", "Total (~tokens)"]
        table = [(label, f"{guide:,}", f"{total:,}", f"{tokens(total, div):,}")
                 for label, _trigger, guide, total in rows_now]
        print(f"\nA11Y.md context cost · {args.lang} · {now.label} · core {core_now:,} chars "
              f"(~{tokens(core_now, div):,} tokens)\n")
        print(render(table, headers, args.markdown))
        cheapest, priciest = rows_now[0][3], rows_now[-1][3]
        print(f"\nA task costs between {cheapest:,} and {priciest:,} characters "
              f"(~{tokens(cheapest, div):,}–{tokens(priciest, div):,} tokens).")
        print("Tokens are estimated at "
              f"{div} chars/token — count with the provider's endpoint before "
              "quoting a price.")
        return 0

    before = Source(args.root, args.lang, args.compare)
    core_before, rows_before = measure(before)
    if core_before is None:
        print(f"error: cannot read docs/{args.lang}/A11Y.md at {args.compare}", file=sys.stderr)
        return 2

    baseline = {label: total for label, _t, _g, total in rows_before}
    headers = ["Task loads", args.compare, now.label, "delta", "%"]
    table, deltas = [], []
    for label, _trigger, _guide, total in rows_now:
        old = baseline.get(label)
        if old is None:
            table.append((label, "—", f"{total:,}", "new", "—"))
            continue
        delta = total - old
        pct = (delta / old * 100) if old else 0.0
        deltas.append(pct)
        table.append((label, f"{old:,}", f"{total:,}", f"{delta:+,}", f"{pct:+.1f}%"))

    core_pct = (core_now - core_before) / core_before * 100
    print(f"\nA11Y.md context cost · {args.lang} · {args.compare} → {now.label}")
    print(f"core: {core_before:,} → {core_now:,} chars ({core_pct:+.1f}%)\n")
    print(render(table, headers, args.markdown))

    if deltas:
        best, worst = min(deltas), max(deltas)
        print(f"\nPer-task change ranges from {best:+.1f}% to {worst:+.1f}%.")
        print("The core figure alone is the best case, not the typical one: a guide that "
              "absorbed\nwhat the core gave up returns part of the saving on the tasks "
              "that load it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

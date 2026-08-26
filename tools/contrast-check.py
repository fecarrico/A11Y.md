#!/usr/bin/env python3
"""
contrast-check.py — deterministic WCAG contrast verification.

Born from this project's own benchmark: color contrast was the failure
present in every condition of Study 2 — the one class of defect a model
"reasons" about and gets wrong, and the web's largest audit debt
(WebAIM Million: contrast errors on 83.9% of home pages). Ratios are
arithmetic; they should never be estimated.

Two modes:

  Pair mode (verdict — can gate a build):
      python3 contrast-check.py --bg '#121212' '#f2f2f2' '#a6a6a6'
      python3 contrast-check.py --bg '#fff' --fg '#767676' --profile shield
  Computes the WCAG 2.x ratio of every foreground against the background.
  Exits non-zero if any pair fails the active profile's floor.

  CSS triage mode (report only — never gates):
      python3 contrast-check.py --css styles.css [--page-bg '#ffffff']
  Extracts every color literal (hex, rgb[a], hsl[a], white/black),
  composites alpha over --page-bg, and prints the full pair matrix with
  the failing pairs flagged. It cannot know which pairs actually co-occur
  in the rendered page — treat it as triage, not verdict.

Floors: Standard (AA) — text 4.5:1, large text 3:1, UI components 3:1.
        Shield (AAA)  — text 7:1,  large text 4.5:1, UI components 3:1.

This tool does NOT establish conformance: it measures declared color
literals, not the rendered page (gradients, images, blend modes and
inheritance are out of reach). The rendered-page check in REPORT.md
remains mandatory.

    python3 contrast-check.py --self-test   # fixture: known pass/fail cases

Stdlib only, no dependencies.
"""

import argparse
import itertools
import re
import sys

FLOORS = {
    "standard": {"text": 4.5, "large": 3.0, "ui": 3.0},
    "shield": {"text": 7.0, "large": 4.5, "ui": 3.0},
}

NAMED = {"white": (255, 255, 255, 1.0), "black": (0, 0, 0, 1.0)}

COLOR_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b"
    r"|rgba?\([^)]+\)"
    r"|hsla?\([^)]+\)"
    r"|\b(?:white|black)\b"
)


def _clamp(x: float, lo: float = 0.0, hi: float = 255.0) -> float:
    return max(lo, min(hi, x))


def parse_color(token: str):
    """Return (r, g, b, a) in 0–255 / 0–1, or None if unparseable."""
    t = token.strip().lower()
    if t in NAMED:
        return NAMED[t]
    if t.startswith("#"):
        h = t[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            h += "ff"
        if len(h) != 8:
            return None
        r, g, b, a = (int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
        return (r, g, b, a / 255.0)
    m = re.match(r"(rgba?|hsla?)\(([^)]+)\)", t)
    if not m:
        return None
    fn, body = m.group(1), m.group(2)
    parts = [p.strip() for p in re.split(r"[,/]", body) if p.strip()]
    if len(parts) < 3:
        return None
    try:
        if fn.startswith("rgb"):
            vals = []
            for p in parts[:3]:
                vals.append(float(p[:-1]) * 2.55 if p.endswith("%") else float(p))
            a = float(parts[3][:-1]) / 100 if len(parts) > 3 and parts[3].endswith("%") \
                else float(parts[3]) if len(parts) > 3 else 1.0
            r, g, b = (_clamp(v) for v in vals)
            return (r, g, b, a)
        # hsl
        h = float(re.sub(r"deg$", "", parts[0]))
        s = float(parts[1].rstrip("%")) / 100
        l = float(parts[2].rstrip("%")) / 100
        a = float(parts[3][:-1]) / 100 if len(parts) > 3 and parts[3].endswith("%") \
            else float(parts[3]) if len(parts) > 3 else 1.0
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        mm = l - c / 2
        r1, g1, b1 = (
            (c, x, 0) if h < 60 else (x, c, 0) if h < 120 else
            (0, c, x) if h < 180 else (0, x, c) if h < 240 else
            (x, 0, c) if h < 300 else (c, 0, x)
        )
        return ((r1 + mm) * 255, (g1 + mm) * 255, (b1 + mm) * 255, a)
    except ValueError:
        return None


def composite(fg, bg):
    """Composite fg (with alpha) over an opaque bg. Returns opaque (r, g, b)."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


def luminance(rgb) -> float:
    def chan(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2) -> float:
    l1, l2 = sorted((luminance(c1), luminance(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def fmt(rgb) -> str:
    return "#{:02x}{:02x}{:02x}".format(*(round(c) for c in rgb[:3]))


def run_pairs(bg_tok, fg_toks, profile) -> int:
    floors = FLOORS[profile]
    bg = parse_color(bg_tok)
    if bg is None:
        sys.exit(f"ERROR: cannot parse background {bg_tok!r}")
    bg_rgb = composite(bg, (255, 255, 255))  # page assumed white under a translucent bg
    failures = 0
    print(f"profile: {profile} · background: {fmt(bg_rgb)}")
    for tok in fg_toks:
        fg = parse_color(tok)
        if fg is None:
            print(f"  {tok}: UNPARSEABLE")
            failures += 1
            continue
        r = ratio(composite(fg, bg_rgb), bg_rgb)
        verdicts = " · ".join(
            f"{use} {'PASS' if r >= floor else 'FAIL'} (≥{floor}:1)"
            for use, floor in floors.items()
        )
        print(f"  {fmt(composite(fg, bg_rgb))} ({tok}): {r:.2f}:1 — {verdicts}")
        if r < min(floors.values()):
            failures += 1
        elif r < floors["text"]:
            # passes some use, not text: caller decides; count as failure only for text intent
            pass
    return failures


def run_css(path, page_bg_tok, profile) -> int:
    floors = FLOORS[profile]
    page_bg = parse_color(page_bg_tok)
    if page_bg is None:
        sys.exit(f"ERROR: cannot parse --page-bg {page_bg_tok!r}")
    try:
        css = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        sys.exit(f"ERROR: {e}")
    seen = {}
    for tok in COLOR_RE.findall(css):
        c = parse_color(tok)
        if c is not None:
            seen.setdefault(fmt(composite(c, composite(page_bg, (255, 255, 255)))), tok)
    colors = list(seen.items())
    print(f"TRIAGE (not a verdict): {len(colors)} distinct colors in {path}; "
          f"pairs below the {profile} text floor ({floors['text']}:1) flagged.")
    flagged = 0
    for (hex1, tok1), (hex2, tok2) in itertools.combinations(colors, 2):
        r = ratio(parse_color(hex1), parse_color(hex2))
        if r < floors["text"]:
            flagged += 1
            band = "below UI floor (3:1)" if r < floors["ui"] else "text fails, large/UI may pass"
            print(f"  {hex1} × {hex2}: {r:.2f}:1 — {band}")
    print(f"{flagged} pair(s) flagged out of {len(colors) * (len(colors) - 1) // 2}. "
          "A flagged pair only matters if the two colors actually meet in the page — verify intent, then fix or record.")
    return 0  # triage never gates


def self_test() -> int:
    cases = [
        # the benchmark's field case: gray on gray ships and fails
        ("#767676", "#5a5a5a", False),
        ("#121212", "#f2f2f2", True),
        ("#ffffff", "#747474", True),    # 4.54:1 — boundary pass at AA
        ("#ffffff", "#777777", False),   # 4.47:1 — boundary fail at AA
        ("hsl(14, 60%, 72%)", "#121212", True),
        ("rgba(0,0,0,0.5)", "white", False),  # 50% black over white bg vs white fg
    ]
    ok = True
    for bg_tok, fg_tok, should_pass in cases:
        bg = composite(parse_color(bg_tok), (255, 255, 255))
        fg = composite(parse_color(fg_tok), bg)
        r = ratio(fg, bg)
        passed = r >= 4.5
        verdict = "ok" if passed == should_pass else "SELF-TEST FAILURE"
        if passed != should_pass:
            ok = False
        print(f"  {bg_tok} vs {fg_tok}: {r:.2f}:1 → {'pass' if passed else 'fail'} (expected {'pass' if should_pass else 'fail'}) {verdict}")
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bg", help="background color (pair mode)")
    ap.add_argument("--fg", nargs="*", help="foreground color(s) (pair mode; positional colors also accepted)")
    ap.add_argument("colors", nargs="*", help="foreground colors (pair mode)")
    ap.add_argument("--css", help="CSS file to triage")
    ap.add_argument("--page-bg", default="#ffffff", help="page background for alpha compositing (CSS mode)")
    ap.add_argument("--profile", choices=("standard", "shield"), default="standard")
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixture cases")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())
    if args.css:
        sys.exit(run_css(args.css, args.page_bg, args.profile))
    if args.bg:
        fgs = (args.fg or []) + args.colors
        if not fgs:
            ap.error("pair mode needs at least one foreground color")
        sys.exit(1 if run_pairs(args.bg, fgs, args.profile) else 0)
    ap.print_help()


if __name__ == "__main__":
    main()

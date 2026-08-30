#!/usr/bin/env python3
"""
rulers.py — Round 2's executable rulers 1, 2, 3 and 5, plus the kill-criterion
checker and the per-obligation floor panel.

Round 1 published five rulers but three existed only as prose (post-hoc
readings, hand-derived). Round 2's protocol requires every ruler to be frozen
executable code BEFORE registration, self-tested against Round 1's published
numbers — so the definitions cannot drift after the data arrives.

Input: a directory of verify JSONL files (one per run; 7 lines, one per
screen; each line: {"id", "violations": [{"id", "impact", "nodes"}, ...]}).
Run ids follow `agent__journey__COND__runN`.

Rulers (impact filter: critical + serious, axe 4.13.0 — frozen):
  screens    ruler 1 — screen×error pairs (each distinct violated rule counted
             once per screen it appears on)
  decisions  ruler 2 — distinct violated rules PER JOURNEY, summed over the
             condition (each journey is an independent project: the same
             wrong rule in two journeys is two decisions; within a journey it
             is one, however many screens repeat its mold). Definition fixed
             by reproducing Round 1's published 9/11/8 — see --self-test.
  clean      ruler 3 — journeys with zero critical+serious violations
  elements   ruler 5 — total flagged nodes
  kill       the ladder-class checker: structural ARIA parent/child rules
  floors     per-obligation panel: image-alt, label, color-contrast per journey

  --self-test  validates every ruler against Round 1's published Table-5
               numbers from runs/study2/verify. A ruler that cannot reproduce
               the published reading is a defect HERE, found before the freeze.

Stdlib only, no dependencies. This tool does not establish conformance; it
counts what axe already measured.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

IMPACTS = ("critical", "serious")

# The ladder class, derived from axe 4.13.0's ARIA/structural parent-child
# rules (derivation published in PROTOCOL.md): a composite pattern
# announced but not completed. Frozen list.
KILL_CLASS = (
    "aria-required-parent",
    "aria-required-children",
    "listitem",
    "dlitem",
    "definition-list",
    "aria-required-attr",
)

# The floor panel's obligation classes (axe rule ids).
FLOOR_CLASSES = {
    "image-alt": ("image-alt", "input-image-alt", "role-img-alt", "svg-img-alt", "area-alt"),
    "label": ("label", "select-name", "form-field-multiple-labels", "aria-input-field-name"),
    "color-contrast": ("color-contrast",),
}


def parse_run(path: Path):
    screens = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            screens.append(json.loads(line))
    return screens


def load(verify_dir: Path):
    """{(agent, cond, runN): [screen dicts]}"""
    runs = {}
    for f in sorted(verify_dir.glob("*.jsonl")):
        parts = f.stem.split("__")
        if len(parts) != 4:
            continue
        agent, _journey, cond, run = parts
        runs[(agent, cond, run)] = parse_run(f)
    if not runs:
        sys.exit(f"ERROR: no agent__journey__cond__runN.jsonl files in {verify_dir}")
    return runs


def serious_violations(screen):
    return [v for v in screen.get("violations", []) if v.get("impact") in IMPACTS]


def ruler_screens(runs):
    """Ruler 1: screen×error pairs per (agent, cond)."""
    out = defaultdict(int)
    for (agent, cond, _run), screens in runs.items():
        out[(agent, cond)] += 0  # register the cell even at zero
        for s in screens:
            out[(agent, cond)] += len(serious_violations(s))
    return dict(out)


def ruler_decisions(runs):
    """Ruler 2: distinct violated rules per journey, summed per (agent, cond)."""
    out = defaultdict(int)
    for (agent, cond, _run), screens in runs.items():
        out[(agent, cond)] += 0  # register the cell even at zero
        per_journey = {v["id"] for s in screens for v in serious_violations(s)}
        out[(agent, cond)] += len(per_journey)
    return dict(out)


def ruler_clean(runs):
    """Ruler 3: journeys with zero critical+serious, per (agent, cond)."""
    total = defaultdict(int)
    clean = defaultdict(int)
    for (agent, cond, _run), screens in runs.items():
        total[(agent, cond)] += 1
        if not any(serious_violations(s) for s in screens):
            clean[(agent, cond)] += 1
    return {k: (clean[k], total[k]) for k in total}


def ruler_elements(runs):
    """Ruler 5: total flagged nodes (critical+serious), per (agent, cond)."""
    out = defaultdict(int)
    for (agent, cond, _run), screens in runs.items():
        out[(agent, cond)] += 0  # register the cell even at zero
        for s in screens:
            for v in serious_violations(s):
                out[(agent, cond)] += v.get("nodes", 0)
    return dict(out)


def kill_table(runs):
    """Ladder-class appearances: per (agent, cond) → journeys affected, nodes."""
    out = {}
    for (agent, cond, run), screens in runs.items():
        nodes = sum(
            v.get("nodes", 0)
            for s in screens
            for v in s.get("violations", [])
            if v["id"] in KILL_CLASS
        )
        key = (agent, cond)
        j, n = out.get(key, (0, 0))
        out[key] = (j + (1 if nodes else 0), n + nodes)
    return out


def floors(runs):
    """Per-obligation panel: journeys affected per class, per (agent, cond)."""
    out = defaultdict(lambda: defaultdict(int))
    for (agent, cond, _run), screens in runs.items():
        hit = set()
        for s in screens:
            for v in s.get("violations", []):
                for cls, ids in FLOOR_CLASSES.items():
                    if v["id"] in ids and v.get("nodes", 0) > 0:
                        hit.add(cls)
        for cls in hit:
            out[(agent, cond)][cls] += 1
    return {k: dict(v) for k, v in out.items()}


def report(verify_dir: Path):
    runs = load(verify_dir)
    blocks = {
        "ruler1_screen_error_pairs": {f"{a}/{c}": v for (a, c), v in sorted(ruler_screens(runs).items())},
        "ruler2_distinct_decisions": {f"{a}/{c}": v for (a, c), v in sorted(ruler_decisions(runs).items())},
        "ruler3_clean_journeys": {f"{a}/{c}": f"{x}/{t}" for (a, c), (x, t) in sorted(ruler_clean(runs).items())},
        "ruler5_flagged_nodes": {f"{a}/{c}": v for (a, c), v in sorted(ruler_elements(runs).items())},
        "kill_class": {f"{a}/{c}": {"journeys": j, "nodes": n} for (a, c), (j, n) in sorted(kill_table(runs).items())},
        "floor_panel_journeys_affected": {f"{a}/{c}": v for (a, c), v in sorted(floors(runs).items())},
    }
    print(json.dumps(blocks, indent=1))


def self_test():
    """Reproduce Round 1's published readings from runs/study2/verify."""
    verify = Path(__file__).resolve().parent.parent / "runs" / "study2" / "verify"
    if not verify.is_dir():
        sys.exit(f"self-test needs Round 1 data at {verify} (published on Zenodo)")
    runs = load(verify)
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  {name}: got {got} want {want} {'ok' if good else 'SELF-TEST FAILURE'}")

    r1, r2 = ruler_screens(runs), ruler_decisions(runs)
    r3, r5 = ruler_clean(runs), ruler_elements(runs)
    kt, fl = kill_table(runs), floors(runs)

    print("ruler 1 — published: antigravity A/B/D = 33/13/38 (screen×error pairs)")
    for cond, want in (("A", 33), ("B", 13), ("D", 38)):
        check(f"antigravity {cond}", r1.get(("antigravity", cond)), want)

    print("ruler 2 — published: antigravity A/B/D = 9/11/8 (distinct wrong decisions)")
    for cond, want in (("A", 9), ("B", 11), ("D", 8)):
        check(f"antigravity {cond}", r2.get(("antigravity", cond)), want)

    print("ruler 3 — published: antigravity A/B/D = 0/5, 0/5, 2/5 clean journeys")
    for cond, want in (("A", (0, 5)), ("B", (0, 5)), ("D", (2, 5))):
        check(f"antigravity {cond}", r3.get(("antigravity", cond)), want)

    print("ruler 5 — published: antigravity A/B/D = 167/42/144 flagged nodes; claude-code = 369/0/0")
    for agent, cond, want in (
        ("antigravity", "A", 167), ("antigravity", "B", 42), ("antigravity", "D", 144),
        ("claude-code", "A", 369), ("claude-code", "B", 0), ("claude-code", "D", 0),
    ):
        check(f"{agent} {cond}", r5.get((agent, cond)), want)

    print("kill class — published: exactly one D journey carries the ladder (98 structural nodes + the 7-screen children rule)")
    check("antigravity D journeys", kt.get(("antigravity", "D"), (0, 0))[0], 1)
    check("claude-code D journeys", kt.get(("claude-code", "D"), (0, 0))[0], 0)

    print("floor panel — published: contrast in 3/5 antigravity D journeys, 0/5 claude-code D; image-alt and label at zero in all D")
    check("antigravity D color-contrast", fl.get(("antigravity", "D"), {}).get("color-contrast", 0), 3)
    check("claude-code D color-contrast", fl.get(("claude-code", "D"), {}).get("color-contrast", 0), 0)
    check("antigravity D image-alt", fl.get(("antigravity", "D"), {}).get("image-alt", 0), 0)
    check("claude-code D image-alt", fl.get(("claude-code", "D"), {}).get("image-alt", 0), 0)
    check("antigravity D label", fl.get(("antigravity", "D"), {}).get("label", 0), 0)
    check("claude-code D label", fl.get(("claude-code", "D"), {}).get("label", 0), 0)

    print("D-loses fixtures (the rulers must be able to score against the standard):")
    check("ruler 1: antigravity D (38) worse than B (13)", r1.get(("antigravity", "D"), 0) > r1.get(("antigravity", "B"), 0), True)
    check("ruler 5: antigravity D (144) worse than B (42)", r5.get(("antigravity", "D"), 0) > r5.get(("antigravity", "B"), 0), True)

    print("self-test:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verify_dir", nargs="?", help="directory of verify *.jsonl files")
    ap.add_argument("--self-test", action="store_true", help="validate against Round 1's published numbers")
    args = ap.parse_args()
    if args.self_test:
        self_test()
    if not args.verify_dir:
        ap.print_help()
        sys.exit(0)
    report(Path(args.verify_dir))


if __name__ == "__main__":
    main()

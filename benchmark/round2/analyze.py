#!/usr/bin/env python3
"""
analyze.py — Round 2 registered analysis. Instrumentation for
PROTOCOL.md: every judgment here is dictated by the protocol's
outcomes section and canonical panel; this file adds none.

Descriptive and estimation-oriented by declaration — point estimates, seeded
bootstrap intervals (resampling BY JOURNEY CLUSTER — screens within a session
are correlated), Cliff's delta, no p-values. Primary contrast: D20 vs D18,
same-agent, never pooled. Secondary: D20 vs B, D20 vs A.

Outcomes per journey, all via frozen instruments:
  ruler1  screen×error pairs        (axe critical+serious; rulers.py judgment)
  ruler2  distinct wrong decisions  (per journey; rulers.py judgment)
  ruler5  flagged nodes             (rulers.py judgment)
  excess_v2 + families_counted      (classifier_v2 — quoted only as a pair)
  excess_v1                         (frozen v1, sensitivity analysis)
  fresh/total tokens per screen     (explicit per-schema field lists — the
                                     defect-#4 discipline, carried forward)
Panel (canonical mapping, same-agent, two-agent adjudication — the LESS
favorable verdict leads): floors (image-alt, label), generalized floors,
the contrast bet, the governance pair, the kill criterion with its 2×2.

    python3 analyze.py            # reads ../runs/round2, writes analysis.json
    python3 analyze.py --self-test  # synthetic 40-run fixture, planted numbers

Stdlib only. Ruler 3 (clean journeys) is printed as base rates, descriptive.
"""
import argparse, json, random, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = REPO / "benchmark" / "runs" / "round2"
SEED = 20260921
B = 10_000
CONDITIONS = ("A", "B", "D18", "D20")
CONTRASTS = (("D20_vs_D18", "D20", "D18"),   # primary
             ("D20_vs_B", "D20", "B"), ("D20_vs_A", "D20", "A"))
METRICS = ("ruler1", "ruler2", "ruler5", "excess_v2", "excess_v1",
           "fresh_per_screen", "total_per_screen")
# Ruler-4 cross-vocabulary rule (classifier panel, bias lens): variant excess
# is only measurable inside the semantic vocabulary the standard prescribes,
# so it enters the CONTRAST table only where both cells share that vocabulary
# — the primary D20 vs D18. In secondary contrasts (vs A/B) it stays in the
# per-condition medians as descriptive data, families_counted beside it,
# never as a contrast estimand.
VOCABULARY_BOUND = ("excess_v2", "excess_v1")

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "benchmark" / "study2"))
from rulers import KILL_CLASS, FLOOR_CLASSES, parse_run, serious_violations  # noqa: E402
from classifier_v2 import classify as classify_v2  # noqa: E402
from classifier import classify as classify_v1  # noqa: E402


# ---- per-journey outcomes (rulers' judgments, journey grain) ----

def journeys(out_dir: Path):
    """Retained journeys from the collection log (latest record per id wins)."""
    seen = {}
    for line in (out_dir / "log.jsonl").read_text().splitlines():
        r = json.loads(line)
        seen[r["id"]] = r
    return {k: v for k, v in seen.items() if v.get("retained")}


def verify_outcomes(out_dir: Path, rid: str):
    screens = parse_run(out_dir / "verify" / f"{rid}.jsonl")
    pairs = sum(len(serious_violations(s)) for s in screens)
    decisions = len({v["id"] for s in screens for v in serious_violations(s)})
    nodes = sum(v.get("nodes", 0) for s in screens for v in serious_violations(s))
    clean = not any(serious_violations(s) for s in screens)
    kill_nodes = sum(v.get("nodes", 0) for s in screens
                     for v in s.get("violations", []) if v["id"] in KILL_CLASS)
    floors_hit = {cls for s in screens for v in s.get("violations", [])
                  for cls, ids in FLOOR_CLASSES.items()
                  if v["id"] in ids and v.get("nodes", 0) > 0}
    zero_classes_pool = {v["id"] for s in screens for v in serious_violations(s)}
    return {"ruler1": pairs, "ruler2": decisions, "ruler5": nodes, "clean": clean,
            "kill_nodes": kill_nodes, "floors_hit": floors_hit,
            "violated_classes": zero_classes_pool}


def token_outcomes(out_dir: Path, rid: str, n_screens: int = 7):
    u = json.loads((out_dir / "raw" / f"{rid}.json").read_text() or "{}").get("usage", {})
    # Defect-#4 discipline (Study 2, DEVIATIONS.md 2026-08-24): explicit
    # per-schema field lists — the Antigravity client reports total_tokens
    # (= input + output) ALONGSIDE its components; never sum by field-name.
    if "total_tokens" in u:  # antigravity client schema
        cache = u.get("cache_read_tokens", 0)
        fresh = (u.get("input_tokens", 0) + u.get("output_tokens", 0)
                 + u.get("thinking_tokens", 0))
    else:                    # claude-code client schema
        cache = u.get("cache_read_input_tokens", 0)
        fresh = (u.get("input_tokens", 0) + u.get("output_tokens", 0)
                 + u.get("cache_creation_input_tokens", 0))
    return {"fresh_per_screen": fresh / n_screens,
            "total_per_screen": (fresh + cache) / n_screens}


def consistency_outcomes(out_dir: Path, rid: str):
    r2 = classify_v2(out_dir / "screens" / rid)
    r1 = classify_v1(out_dir / "screens" / rid)
    if r2.get("status") != "ok":
        return {"excess_v2": None, "families_counted": None, "excess_v1": None}
    return {"excess_v2": r2["variant_excess"],
            "families_counted": r2["richness"]["families_counted"],
            "excess_v1": r1["variant_excess"]}


def governance(out_dir: Path, rid: str):
    names = [p.name.lower() for p in (out_dir / "screens" / rid).rglob("*.md")]
    return {"report": any("report" in n for n in names),
            "decisions": any("decisions" in n for n in names)}


# ---- estimation (journey = the resampling cluster) ----

def bootstrap_median_diff(x, y, seed=SEED):
    rng = random.Random(seed)
    diffs = []
    for _ in range(B):
        xs = [rng.choice(x) for _ in x]
        ys = [rng.choice(y) for _ in y]
        diffs.append(statistics.median(xs) - statistics.median(ys))
    diffs.sort()
    return diffs[int(B * 0.025)], diffs[int(B * 0.975)]


def cliff(x, y):
    gt = sum(1 for a in x for b in y if a > b)
    lt = sum(1 for a in x for b in y if a < b)
    return (lt - gt) / (len(x) * len(y))   # positive = x typically smaller


def wilson95(k, n):
    if n == 0: return [0.0, 0.0]
    z = 1.959964
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round(max(0.0, c - h), 3), round(min(1.0, c + h), 3)]


# ---- the canonical panel (verbatim rules from the protocol table) ----

FAVOR = {  # adjudication order: index 0 is the LEAST favorable verdict
    "floors": ("regression", "isolated-inspect", "pass"),
    "contrast": ("refuted", "not-corroborated", "corroborated"),
    "kill": ("fail", "pass"),
}

def floor_verdict(journeys_affected: int) -> str:
    if journeys_affected == 0: return "pass"
    if journeys_affected == 1: return "isolated-inspect"
    return "regression"

def contrast_verdict(d18_affected: int, d20_affected: int) -> str:
    if d20_affected > d18_affected: return "refuted"
    if (d18_affected > 0 and d20_affected < d18_affected) or (d18_affected == 0 and d20_affected == 0):
        return "corroborated"
    return "not-corroborated"   # tie at >0

def panel_for_agent(vouts: dict):
    """vouts: {cond: {rid: verify_outcomes}} for one agent."""
    d20, d18 = vouts.get("D20", {}), vouts.get("D18", {})
    out = {}
    for cls in ("image-alt", "label"):
        affected = sum(1 for o in d20.values() if cls in o["floors_hit"])
        out[f"floor_{cls}"] = {"d20_journeys_affected": affected,
                               "verdict": floor_verdict(affected)}
    c18 = sum(1 for o in d18.values() if "color-contrast" in o["floors_hit"])
    c20 = sum(1 for o in d20.values() if "color-contrast" in o["floors_hit"])
    out["contrast_bet"] = {"d18_journeys_affected": c18, "d20_journeys_affected": c20,
                           "verdict": contrast_verdict(c18, c20)}
    if d18:
        all18 = set().union(*(o["violated_classes"] for o in d18.values())) if d18 else set()
        all20 = set().union(*(o["violated_classes"] for o in d20.values())) if d20 else set()
        candidates = all20 - all18
        reappeared = {cls: sum(1 for o in d20.values() if cls in o["violated_classes"])
                      for cls in candidates}
        regressions = {c: n for c, n in reappeared.items() if n >= 2}
        out["generalized_floor"] = {
            "classes_regressed": regressions,
            "isolated": {c: n for c, n in reappeared.items() if n == 1},
            "verdict": "regression" if regressions else (
                "isolated-inspect" if any(n == 1 for n in reappeared.values()) else "pass")}
    kill20 = sum(1 for o in d20.values() if o["kill_nodes"] > 0)
    kill18 = sum(1 for o in d18.values() if o["kill_nodes"] > 0)
    out["kill_criterion"] = {
        "verdict": "pass" if kill20 == 0 else "fail",
        "two_by_two": {"d18_journeys_with_ladder": kill18, "d18_n": len(d18),
                       "d20_journeys_with_ladder": kill20, "d20_n": len(d20)}}
    return out


def adjudicate(panels: dict):
    """Two-agent rule: report both; the LESS favorable verdict leads."""
    led = {}
    for check in set().union(*(p.keys() for p in panels.values())):
        verdicts = {a: p[check]["verdict"] for a, p in panels.items() if check in p}
        kind = ("contrast" if check == "contrast_bet"
                else "kill" if check == "kill_criterion" else "floors")
        order = FAVOR[kind]
        lead = min(verdicts.values(), key=order.index)
        led[check] = {"per_agent": verdicts, "leads": lead}
    return led


# ---- main ----

def analyze(out_dir: Path):
    recs = journeys(out_dir)
    data = defaultdict(lambda: defaultdict(dict))     # agent -> cond -> rid -> outcomes
    vdata = defaultdict(lambda: defaultdict(dict))    # verify outcomes (panel inputs)
    gov = defaultdict(lambda: defaultdict(dict))
    versions = defaultdict(set)
    for rid, rec in sorted(recs.items()):
        agent, _, cond, _ = rid.split("__")
        v = verify_outcomes(out_dir, rid)
        o = {**{k: v[k] for k in ("ruler1", "ruler2", "ruler5", "clean")},
             **token_outcomes(out_dir, rid),
             **consistency_outcomes(out_dir, rid)}
        data[agent][cond][rid] = o
        vdata[agent][cond][rid] = v
        gov[agent][cond][rid] = governance(out_dir, rid)
        versions[(agent, rec.get("agent_version", "?"))].add(cond)

    report = {"seed": SEED, "bootstrap": B, "resampling_unit": "journey cluster",
              "posture": "descriptive and estimation-oriented — not confirmatory at this n",
              "agents": {}, "panel": {}, "version_by_condition": {
                  f"{a} · {v}": sorted(c) for (a, v), c in sorted(versions.items())}}

    panels = {}
    for agent, conds in sorted(data.items()):
        block = {"n": {c: len(v) for c, v in sorted(conds.items())},
                 "medians": {}, "clean_journeys": {}, "contrasts": {}}
        for c, v in sorted(conds.items()):
            vals = list(v.values())
            block["medians"][c] = {
                m: (statistics.median(o[m] for o in vals) if all(o[m] is not None for o in vals) else None)
                for m in METRICS}
            block["medians"][c]["families_counted"] = (
                statistics.median(o["families_counted"] for o in vals)
                if all(o["families_counted"] is not None for o in vals) else None)
            block["clean_journeys"][c] = f"{sum(1 for o in vals if o['clean'])}/{len(vals)}"
        for label, hi, lo in CONTRASTS:
            if hi not in conds or lo not in conds: continue
            entry = {}
            metrics = METRICS if lo.startswith("D") else tuple(
                m for m in METRICS if m not in VOCABULARY_BOUND)
            for m in metrics:
                x = [o[m] for o in conds[hi].values()]
                y = [o[m] for o in conds[lo].values()]
                if any(v is None for v in x + y): continue
                ci = bootstrap_median_diff(x, y)
                entry[m] = {"median_diff": round(statistics.median(x) - statistics.median(y), 2),
                            "ci95": [round(ci[0], 1), round(ci[1], 1)],
                            "cliff": round(cliff(x, y), 2)}
            block["contrasts"][label] = entry
        g20 = list(gov[agent].get("D20", {}).values())
        pair = sum(1 for g in g20 if g["report"] and g["decisions"])
        others = [g for c in ("A", "B") for g in gov[agent].get(c, {}).values()]
        block["governance"] = {
            "d20_pair": f"{pair}/{len(g20)}", "d20_ci95": wilson95(pair, len(g20)),
            "ab_pair": f"{sum(1 for g in others if g['report'] and g['decisions'])}/{len(others)}"}
        panels[agent] = panel_for_agent(vdata[agent])
        panels[agent]["governance_pair"] = {
            "verdict": "pass" if pair == len(g20) and g20 else
                       ("isolated-inspect" if pair == len(g20) - 1 else "regression"),
            "d20_pair": f"{pair}/{len(g20)}"}
        report["agents"][agent] = block

    report["panel"] = {"per_agent": panels, "adjudication": adjudicate(panels)}
    return report


def main():
    report = analyze(OUT)
    (OUT / "analysis.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    for agent, blk in report["agents"].items():
        print(f"== {agent} · n {blk['n']} · clean {blk['clean_journeys']}")
        for lbl, e in blk["contrasts"].items():
            if "ruler1" in e:
                line = (f"   {lbl}: ruler1 Δ{e['ruler1']['median_diff']:+.0f} IC{e['ruler1']['ci95']} "
                        f"Cliff {e['ruler1']['cliff']:+.2f}")
                if "excess_v2" in e:
                    line += (f" · excess_v2 Δ{e['excess_v2']['median_diff']:+.0f} "
                             f"Cliff {e['excess_v2']['cliff']:+.2f}")
                print(line)
    print("panel (less favorable leads):")
    for check, v in sorted(report["panel"]["adjudication"].items()):
        print(f"   {check}: {v['per_agent']} -> leads: {v['leads']}")


# ---------------------------------------------------------------------------
# --self-test: synthetic 40-run fixture with planted numbers
# ---------------------------------------------------------------------------

SCREENS7 = ("index", "search", "book", "cart", "sell", "dashboard", "orders")

def _mk_verify(path, rows):
    lines = []
    for sid, viols in rows:
        lines.append(json.dumps({"id": sid, "violations": viols}))
    path.write_text("\n".join(lines) + "\n")

def _viol(vid, nodes, impact="serious"):
    return {"id": vid, "impact": impact, "nodes": nodes}

def build_fixture(root: Path):
    """40 runs, 2 agents × 4 conditions × 5. Planted so every panel branch
    and every contrast sign is known in advance.
      fake-clean  : D20 wins everything (contrast corroborated, kill pass
                    with an informative 2×2, floors pass, governance 5/5)
      fake-dirty  : the unfavorable twin (contrast refuted, kill fail,
                    image-alt floor regression, governance 3/5)"""
    (root / "raw").mkdir(parents=True); (root / "verify").mkdir(); (root / "screens").mkdir()
    log = []
    nav = ('<nav aria-label="Main"><ul><li><a href="index.html">Home</a></li>'
           '<li><a href="search.html">Search</a></li><li><a href="cart.html">Cart</a></li>'
           '</ul></nav>')
    for agent in ("fake-clean", "fake-dirty"):
        for cond in CONDITIONS:
            for run in range(1, 6):
                rid = f"{agent}__journey__{cond}__run{run}"
                d = root / "screens" / rid; d.mkdir()
                for s in SCREENS7:
                    (d / f"{s}.html").write_text(
                        f'<!doctype html><html lang="en"><body>{nav}<main><h1>{s}</h1></main></body></html>')
                base = {"A": 20, "B": 10, "D18": 6, "D20": 2}[cond]
                viols = [("index", [_viol("link-name", base + run)]),
                         ("search", [_viol("region", 2)] if cond in ("A", "B") else [])]
                if agent == "fake-clean":
                    if cond == "D18" and run <= 3:
                        viols.append(("cart", [_viol("color-contrast", 3)]))
                    if cond == "D18" and run == 2:
                        viols.append(("sell", [_viol("aria-required-children", 4, "critical")]))
                    if cond == "D20":
                        viols = [("index", [_viol("color-contrast", 0)])]  # zero nodes = not affected
                        viols.append(("search", []))
                else:
                    if cond == "D18" and run == 1:
                        viols.append(("cart", [_viol("color-contrast", 3)]))
                    if cond == "D20" and run <= 3:
                        viols.append(("cart", [_viol("color-contrast", 5)]))
                    if cond == "D20" and run == 1:
                        viols.append(("sell", [_viol("listitem", 2, "critical")]))
                    if cond == "D20" and run <= 2:
                        viols.append(("book", [_viol("image-alt", 1, "critical")]))
                _mk_verify(root / "verify" / f"{rid}.jsonl",
                           [(s, next((v for n, v in viols if n == s), [])) for s in SCREENS7])
                if agent == "fake-clean":
                    usage = {"input_tokens": 1000 * base, "output_tokens": 400,
                             "cache_creation_input_tokens": 100, "cache_read_input_tokens": 7000}
                else:  # antigravity-style schema: total_tokens must NOT be summed
                    usage = {"total_tokens": 1400 * base, "input_tokens": 1000 * base,
                             "output_tokens": 400 * base, "thinking_tokens": 0,
                             "cache_read_tokens": 7000}
                (root / "raw" / f"{rid}.json").write_text(json.dumps({"usage": usage}))
                if cond == "D20" and not (agent == "fake-dirty" and run > 3):
                    (d / "REPORT.md").write_text("# report\n")
                    (d / "A11Y-DECISIONS.md").write_text("# decisions\n")
                log.append({"id": rid, "agent": agent, "condition": cond, "run": run,
                            "attempt": 1, "agent_version": "fake 1.0.0",
                            "screens": 7, "retained": True, "files_created": []})
    (root / "log.jsonl").write_text("\n".join(json.dumps(r) for r in log) + "\n")


def self_test():
    import tempfile
    ok = True
    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  {name}: got {got!r} want {want!r} {'ok' if good else 'SELF-TEST FAILURE'}")

    td = Path(tempfile.mkdtemp(prefix="round2-analyze-selftest-"))
    build_fixture(td)
    rep1 = analyze(td)
    rep2 = analyze(td)
    print("determinism — same fixture, same seed, same report:")
    check("byte-identical reports", json.dumps(rep1, sort_keys=True) == json.dumps(rep2, sort_keys=True), True)

    print("planted contrasts (fake-clean): D20 beats D18, sign and magnitude:")
    c = rep1["agents"]["fake-clean"]["contrasts"]["D20_vs_D18"]
    check("ruler5 Cliff = +1.0 (all D20 < all D18)", c["ruler5"]["cliff"], 1.0)
    check("ruler1 median_diff negative", c["ruler1"]["median_diff"] < 0, True)
    check("fresh tokens: D20 cheaper (schema fields, not name-matching)",
          c["fresh_per_screen"]["median_diff"] < 0, True)
    check("excess_v2 present with families_counted beside it",
          rep1["agents"]["fake-clean"]["medians"]["D20"]["families_counted"] is not None, True)
    check("ruler-4 vocabulary rule: excess in the primary contrast only",
          ("excess_v2" in rep1["agents"]["fake-clean"]["contrasts"]["D20_vs_D18"],
           "excess_v2" in rep1["agents"]["fake-clean"]["contrasts"]["D20_vs_B"],
           "excess_v2" in rep1["agents"]["fake-clean"]["contrasts"]["D20_vs_A"]),
          (True, False, False))

    print("planted panel — fake-clean (the favorable twin):")
    p = rep1["panel"]["per_agent"]["fake-clean"]
    check("contrast bet corroborated (3 -> 0)", p["contrast_bet"]["verdict"], "corroborated")
    check("kill pass with informative 2x2 (D18 had the ladder)",
          (p["kill_criterion"]["verdict"], p["kill_criterion"]["two_by_two"]["d18_journeys_with_ladder"]),
          ("pass", 1))
    check("floors pass", (p["floor_image-alt"]["verdict"], p["floor_label"]["verdict"]), ("pass", "pass"))
    check("governance 5/5", p["governance_pair"]["d20_pair"], "5/5")

    print("planted panel — fake-dirty (the unfavorable twin):")
    p = rep1["panel"]["per_agent"]["fake-dirty"]
    check("contrast bet refuted (1 -> 3)", p["contrast_bet"]["verdict"], "refuted")
    check("kill fail", p["kill_criterion"]["verdict"], "fail")
    check("image-alt floor regression (2 journeys)", p["floor_image-alt"]["verdict"], "regression")
    check("governance 3/5 = regression", p["governance_pair"]["verdict"], "regression")

    print("adjudication — the less favorable verdict leads:")
    adj = rep1["panel"]["adjudication"]
    check("contrast bet led by refuted", adj["contrast_bet"]["leads"], "refuted")
    check("kill led by fail", adj["kill_criterion"]["leads"], "fail")
    check("image-alt led by regression", adj["floor_image-alt"]["leads"], "regression")
    check("both agents reported beside the lead",
          sorted(adj["contrast_bet"]["per_agent"]), ["fake-clean", "fake-dirty"])

    print("posture printed:")
    check("descriptive posture in the report",
          rep1["posture"].startswith("descriptive and estimation-oriented"), True)

    print("self-test:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
    main()

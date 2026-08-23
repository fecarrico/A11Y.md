#!/usr/bin/env python3
"""
analyze.py — Study 2 registered analysis. Descriptive by declaration:
point estimates, seeded bootstrap intervals, Cliff's delta for the decisive
contrast (D vs B) and D vs A — per agent, never pooled. No hypothesis tests,
no p-values (PROTOCOL.md §Engines). Exploratory: error topology, labeled.

Reads benchmark/runs/study2/; writes analysis.json beside the data.
"""
import json, random, statistics, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
S2 = REPO / "benchmark" / "runs" / "study2"
SEED = 20260823
B = 10_000

def bootstrap_median_diff(x, y):
    rng = random.Random(SEED)
    diffs = []
    for _ in range(B):
        xs = [rng.choice(x) for _ in x]
        ys = [rng.choice(y) for _ in y]
        diffs.append(statistics.median(xs) - statistics.median(ys))
    diffs.sort()
    return diffs[int(B*0.025)], diffs[int(B*0.975)]

def cliff(x, y):
    gt = sum(1 for a in x for b in y if a > b)
    lt = sum(1 for a in x for b in y if a < b)
    return (lt - gt) / (len(x) * len(y))   # positivo = x tipicamente menor

def journeys():
    seen = {}
    for line in (S2 / "log.jsonl").read_text().splitlines():
        r = json.loads(line)
        if "error" not in r and r.get("screens", 0) == 7:
            seen[r["id"]] = r
    return seen

def outcomes(rec):
    rid = rec["id"]
    out = subprocess.run(["python3", str(REPO / "benchmark/study2/classifier.py"),
                          str(S2 / "screens" / rid)], capture_output=True, text=True)
    excess = list(json.loads(out.stdout).values())[0]["variant_excess"]
    axe = 0
    for line in (S2 / "verify" / f"{rid}.jsonl").read_text().splitlines():
        v = json.loads(line)
        if "counts" in v:
            axe += v["counts"]["critical"] + v["counts"]["serious"]
    u = json.loads((S2 / "raw" / f"{rid}.json").read_text() or "{}").get("usage", {})
    total = sum(v for k, v in u.items() if isinstance(v, int) and "token" in k)
    cache = u.get("cache_read_input_tokens", u.get("cache_read_tokens", 0))
    return {"excess": excess, "axe": axe,
            "total_per_screen": total / 7, "fresh_per_screen": (total - cache) / 7}

def topology(rid):
    rules = {}
    screens_hit = set()
    for line in (S2 / "verify" / f"{rid}.jsonl").read_text().splitlines():
        v = json.loads(line)
        for viol in v.get("violations", []):
            if viol.get("impact") in ("critical", "serious"):
                rules[viol["id"]] = rules.get(viol["id"], 0) + viol.get("nodes", 0)
                screens_hit.add(v["id"])
    total = sum(rules.values())
    if not total:
        return None
    top_rule, top_n = max(rules.items(), key=lambda kv: kv[1])
    return {"rules": rules, "total_nodes": total, "screens_affected": len(screens_hit),
            "top_rule": top_rule, "concentration": round(top_n / total, 2)}

def main():
    recs = journeys()
    data = {}
    for rid, rec in recs.items():
        agent, _, cond, _ = rid.split("__")
        data.setdefault(agent, {}).setdefault(cond, {})[rid] = outcomes(rec)

    report = {"seed": SEED, "bootstrap": B, "agents": {}}
    for agent, conds in sorted(data.items()):
        block = {"n": {c: len(v) for c, v in conds.items()}, "medians": {}, "contrasts": {}}
        for c, v in sorted(conds.items()):
            block["medians"][c] = {m: statistics.median(o[m] for o in v.values())
                                   for m in ("excess", "axe", "total_per_screen", "fresh_per_screen")}
        for label, other in (("D_vs_B", "B"), ("D_vs_A", "A")):
            entry = {}
            for m in ("excess", "axe", "total_per_screen", "fresh_per_screen"):
                d = [o[m] for o in conds["D"].values()]
                x = [o[m] for o in conds[other].values()]
                lo, hi = bootstrap_median_diff(d, x)
                entry[m] = {"median_diff": statistics.median(d) - statistics.median(x),
                            "ci95": [round(lo, 1), round(hi, 1)], "cliff": round(cliff(d, x), 2)}
            block["contrasts"][label] = entry
        report["agents"][agent] = block

    report["exploratory_error_topology"] = {
        rid: t for rid in sorted(recs) if (t := topology(rid))}

    (S2 / "analysis.json").write_text(json.dumps(report, indent=1))
    for agent, blk in report["agents"].items():
        print(f"== {agent} · medianas:", json.dumps(blk["medians"]))
        for lbl, e in blk["contrasts"].items():
            print(f"   {lbl}: excesso Δ{e['excess']['median_diff']:+.0f} "
                  f"IC{e['excess']['ci95']} Cliff {e['excess']['cliff']:+.2f} · "
                  f"axe Δ{e['axe']['median_diff']:+.0f} IC{e['axe']['ci95']} "
                  f"Cliff {e['axe']['cliff']:+.2f}")
    topo = report["exploratory_error_topology"]
    print(f"topologia: {len(topo)} jornadas com falha · concentrações:",
          {r.split("journey__")[1]: t["concentration"] for r, t in topo.items()})

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""confirmatory.py — the registered primary analysis, operationalized.

Registered: negative-binomial mixed regression, violations ~ condition +
(1 | task), IRRs with 95% CIs, Holm-corrected pre-registered contrasts.
Operationalization: statsmodels has no frequentist NB mixed model; with only
ten task levels, the standard alternatives are task fixed effects or
cluster-robust errors by task. We fit NB2 GLM with condition + task fixed
effects AND report cluster-robust (by task) errors as sensitivity — both
sides shown, divergence reported, decision logged in DEVIATIONS.md.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats as sps

RUNS = Path(__file__).resolve().parent.parent
log = {json.loads(l)["id"]: json.loads(l) for l in (RUNS/"log.jsonl").read_text().splitlines()}
axe = {json.loads(l)["id"]: json.loads(l) for l in (RUNS/"verify"/"arm1-axe.jsonl").read_text().splitlines() if "error" not in l[:200] or True}

rows = []
for gid, g in log.items():
    if "error" in g or g.get("output_chars", 0) == 0: continue
    a = axe.get(gid)
    if not a or "counts" not in a: continue
    rows.append({"cs": a["counts"]["critical"] + a["counts"]["serious"],
                 "cond": g["condition"], "task": g["task"]})
df = pd.DataFrame(rows)
print(f"n = {len(df)} · por condição: {df.cond.value_counts().to_dict()}")

# alpha do NB2 por perfil de verossimilhança simples (grid)
def fit(alpha):
    return smf.glm("cs ~ C(cond, Treatment('D')) + C(task)", df,
                   family=sm.families.NegativeBinomial(alpha=alpha)).fit()
alphas = np.linspace(0.05, 8, 60)
lls = [fit(a).llf for a in alphas]
alpha = float(alphas[int(np.argmax(lls))])
m = fit(alpha)
m_rob = smf.glm("cs ~ C(cond, Treatment('D')) + C(task)", df,
                family=sm.families.NegativeBinomial(alpha=alpha)
               ).fit(cov_type="cluster", cov_kwds={"groups": df["task"]})
print(f"alpha (dispersão) ≈ {alpha:.2f}")

def contrasts(model, tag):
    out = {}
    for other in ["B", "C", "A"]:
        name = f"C(cond, Treatment('D'))[T.{other}]"
        beta, se = model.params[name], model.bse[name]
        # coeficiente é other vs D; invertemos para D vs other
        irr = float(np.exp(-beta))
        lo, hi = float(np.exp(-beta - 1.96*se)), float(np.exp(-beta + 1.96*se))
        p = float(2 * (1 - sps.norm.cdf(abs(beta / se))))
        out[f"D vs {other}"] = {"IRR": irr, "lo": min(lo,hi), "hi": max(lo,hi), "p": p}
    # Holm nas três comparações pré-registradas
    ordered = sorted(out.items(), key=lambda kv: kv[1]["p"])
    for rank, (k, v) in enumerate(ordered):
        v["p_holm"] = min(1.0, max(v["p"] * (3 - rank),
                          *[ordered[j][1].get("p_holm", 0) for j in range(rank)] or [0]))
    print(f"\n[{tag}]")
    for k in ["D vs B", "D vs C", "D vs A"]:
        v = out[k]
        print(f"  {k}: IRR {v['IRR']:.2f} [{v['lo']:.2f}, {v['hi']:.2f}] · p {v['p']:.4f} · p-Holm {v['p_holm']:.4f}")
    return out

res = {"n": len(df), "alpha": alpha,
       "fixed_effects": contrasts(m, "efeitos fixos de tarefa"),
       "cluster_robust": contrasts(m_rob, "sensibilidade: erros robustos por cluster de tarefa")}
Path(__file__).parent.joinpath("confirmatory.json").write_text(json.dumps(res, indent=2))
print("\nsalvo em confirmatory.json")

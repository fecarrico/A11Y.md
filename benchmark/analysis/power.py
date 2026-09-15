#!/usr/bin/env python3
"""power.py — o que este desenho consegue enxergar.

METHODOLOGY.md justifica as 400 gerações por viabilidade de coleta ("free-tier
daily caps"), nunca por tamanho de efeito detectável. Nenhum cálculo de poder
foi feito antes ou depois. Isto é a análise post-hoc, e ela é declarada como
post-hoc: não legitima o n escolhido, apenas diz o que ele permitia ver.

O método é simulação, não fórmula, porque o desfecho não é normal: são contagens
raras (a maioria das páginas em zero) e super-dispersas (variância várias vezes
a média). Reamostra-se a condição de referência observada, aplica-se uma redução
real por thinning binomial — que preserva a natureza de contagem — e testa-se a
diferença exatamente como o plano registrado testa: bootstrap percentílico da
diferença de médias, rejeitando quando o IC95% exclui zero.

    python3 analysis/power.py --arm runs/overnight/summary.json
    python3 analysis/power.py --arm <summary.json> --trials 2000

Requer numpy (analysis/requirements.txt).
"""
import argparse, json
import numpy as np

def detect_rate(base, reduction, trials, boots, n, rng):
    hits = 0
    for _ in range(trials):
        ref = rng.choice(base, n)
        trt = rng.binomial(rng.choice(base, n).astype(int), 1 - reduction)
        diffs = np.array([rng.choice(trt, n).mean() - rng.choice(ref, n).mean()
                          for _ in range(boots)])
        if np.percentile(diffs, 97.5) < 0:
            hits += 1
    return hits / trials

def main():
    ap = argparse.ArgumentParser(description="Poder post-hoc do desenho registrado.")
    ap.add_argument("--arm", default="runs/overnight/summary.json")
    ap.add_argument("--refs", default="A,B,C")
    ap.add_argument("--trials", type=int, default=1000)
    ap.add_argument("--boots", type=int, default=300)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260914)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    cs = json.load(open(args.arm))["cs_by_cond"]
    grid = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7)
    out = {"arm": args.arm, "n_per_cell": args.n, "trials": args.trials,
           "seed": args.seed, "contrasts": {}}

    for ref in [r.strip() for r in args.refs.split(",")]:
        base = np.array(cs[ref], float)
        row = {"reference_mean": round(float(base.mean()), 3),
               "share_zero": round(float((base == 0).mean()), 3),
               "variance": round(float(base.var(ddof=1)), 3), "power": {}}
        print(f"\nD − {ref}  ·  referência: média {base.mean():.2f}, "
              f"{(base == 0).mean()*100:.0f}% em zero, variância {base.var(ddof=1):.2f}")
        for red in grid:
            p = detect_rate(base, red, args.trials, args.boots, args.n, rng)
            row["power"][f"{int(red*100)}%"] = round(p, 3)
            print(f"   redução real de {int(red*100):>3}%  →  detectada em {p*100:>5.1f}% das vezes")
        out["contrasts"][f"D-{ref}"] = row

    path = args.arm.replace("summary.json", "power.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nsalvo em {path}")

if __name__ == "__main__":
    raise SystemExit(main())

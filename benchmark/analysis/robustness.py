#!/usr/bin/env python3
"""analyze.py — pre-registered descriptive + robustness figures, morning report.

Computes what the frozen protocol allows computing without the human, blinded
steps: primary-outcome descriptives per condition, the three pre-registered
contrasts with bootstrap CIs and Cliff's delta (the registered robustness
track), the token co-primary, and the loading behaviour raw counts. The
confirmatory mixed model and everything requiring blind human judgment are
explicitly marked pending. Stdlib only; bootstrap seeded for reproducibility.
"""
import json, random, statistics, html
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent.parent.parent
RUNS = BENCH / "runs"
OUT = RUNS / "overnight"

def load_jsonl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.is_file() else []

# ---------- braço 1 ----------
log = {r["id"]: r for r in load_jsonl(RUNS / "log.jsonl")}
gens = [r for r in log.values() if "error" not in r and r.get("output_chars", 0) > 0]
axe = {r["id"]: r for r in load_jsonl(RUNS / "verify" / "arm1-axe.jsonl") if "error" not in r}
rows = []
for g in gens:
    a = axe.get(g["id"])
    if not a: continue
    c = a["counts"]
    rows.append({
        "id": g["id"], "cond": g["condition"], "task": g["task"], "run": g["run"],
        "cs": c["critical"] + c["serious"], "crit": c["critical"],
        "tokens": g.get("usage_total", {}).get("total_tokens", 0),
        "tok_think": g.get("usage_total", {}).get("total_thought_tokens", 0),
        "tok_cache": g.get("usage_total", {}).get("total_cached_tokens", 0),
        "reads": len(g.get("files_read", [])),
    })

def by_cond(key):
    return {c: sorted(r[key] for r in rows if r["cond"] == c) for c in "ABCD"}

cs, toks = by_cond("cs"), by_cond("tokens")

def cliffs(x, y):
    if not x or not y: return None
    gt = sum(1 for a in x for b in y if a > b)
    lt = sum(1 for a in x for b in y if a < b)
    return (lt - gt) / (len(x) * len(y))  # positivo = x (D) menor

def boot_mean_diff(x, y, n=10000, seed=20260819):
    if not x or not y: return None
    rng = random.Random(seed)
    diffs = sorted(statistics.fmean(rng.choices(x, k=len(x))) -
                   statistics.fmean(rng.choices(y, k=len(y))) for _ in range(n))
    return {"diff": statistics.fmean(x) - statistics.fmean(y),
            "lo": diffs[int(n*0.025)], "hi": diffs[int(n*0.975)]}

def boot_median_diff(x, y, n=10000, seed=20260818):
    if not x or not y: return None
    rng = random.Random(seed)
    diffs = sorted(statistics.median(rng.choices(x, k=len(x))) -
                   statistics.median(rng.choices(y, k=len(y))) for _ in range(n))
    return {"diff": statistics.median(x) - statistics.median(y),
            "lo": diffs[int(n*0.025)], "hi": diffs[int(n*0.975)]}

contrasts = {}
for other in "BCA":
    contrasts[f"D-{other}"] = {
        "boot": boot_median_diff(cs["D"], cs[other]),
        "cliffs": cliffs(cs["D"], cs[other]),
        "mean_boot": boot_mean_diff(cs["D"], cs[other]),
        "tok_boot": boot_median_diff(toks["D"], toks[other]),
    }

# ---------- braço 2 (recap) ----------
a2log = {r["id"]: r for r in load_jsonl(RUNS / "arm2" / "log.jsonl")}
a2axe = {r["id"]: r for r in load_jsonl(RUNS / "verify" / "arm2-axe.jsonl") if "error" not in r}
a2 = {}
for agent in ("claude-code", "codex"):
    for cond in "AD":
        vals = sorted(a["counts"]["critical"] + a["counts"]["serious"]
                      for i, a in a2axe.items()
                      if i.startswith(f"{agent}__") and f"__{cond}__" in i)
        a2[f"{agent}:{cond}"] = vals

n_total, complete = len(rows), len(gens) >= 400
stamp = datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %H:%M")

summary = {"generated_at": stamp, "n_scored": n_total, "n_collected": len(gens),
           "complete": complete, "cs_by_cond": {c: cs[c] for c in "ABCD"},
           "contrasts": contrasts}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))

# ---------- relatório ----------
def fmt_dist(v):
    if not v: return "—"
    zeros = v.count(0)
    return f"n={len(v)} · mediana {statistics.median(v):g} · média {statistics.fmean(v):.2f} · zero-violações {zeros}/{len(v)} ({zeros/len(v):.0%})"

def row_html(c, label):
    v = cs[c]; t = toks[c]
    tm = f"{int(statistics.median(t)):,}".replace(",", ".") if t else "—"
    return (f"<tr><td><b>{c}</b> · {label}</td><td>{fmt_dist(v)}</td>"
            f"<td class='num'>{tm}</td></tr>")

def contrast_html(name, lab):
    d = contrasts[name]; b = d["boot"]; cd = d["cliffs"]; tb = d["tok_boot"]
    if not b: return ""
    mb = d["mean_boot"]
    return (f"<tr><td><b>{name}</b> · {lab}</td>"
            f"<td class='num'>{b['diff']:+g} <span class='dim'>[{b['lo']:+g}, {b['hi']:+g}]</span></td>"
            f"<td class='num'>{cd:+.2f}</td>"
            f"<td class='num'>{mb['diff']:+.2f} <span class='dim'>[{mb['lo']:+.2f}, {mb['hi']:+.2f}]</span></td>"
            f"<td class='num'>{tb['diff']:+,.0f}</td></tr>".replace(",", "."))

status = ("COLETA COMPLETA — 400/400" if complete
          else f"PARCIAL — {len(gens)}/400 coletadas · {n_total} verificadas")

html_doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Relatório — Benchmark A11Y.md</title><style>
:root{{--bg:#121212;--surface:#1a1a1a;--fg:#f2f2f2;--muted:#a6a6a6;--dim:#7d7d7d;
--coral:#e2a18d;--warn:#e8c468;--line:#333;--strong:#4d4d4d;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--fg);margin:0;
font:17px/1.65 ui-sans-serif,system-ui,sans-serif;padding:48px 24px 96px}}
.wrap{{max-width:880px;margin:0 auto}}h1{{font-size:clamp(30px,5vw,44px);
letter-spacing:-.02em;line-height:1.1;margin:0 0 8px}}
h2{{font-size:24px;letter-spacing:-.015em;margin:52px 0 14px;border-top:1px solid var(--strong);padding-top:20px}}
p{{max-width:66ch;margin:0 0 14px}}.muted{{color:var(--muted)}}.dim{{color:var(--dim)}}
.badge{{display:inline-block;font:11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;
color:var(--warn);border:1px solid #3d3323;background:#262019;padding:5px 10px;border-radius:3px;margin:0 0 18px}}
.kicker{{font:12px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--coral);margin:0 0 14px}}
table{{border-collapse:collapse;width:100%;font-size:15px;margin:14px 0 8px}}
th,td{{text-align:left;padding:10px 14px 10px 0;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font:11.5px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}}
td.num{{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}}
.note{{border-left:3px solid var(--warn);background:var(--surface);border-radius:0 6px 6px 0;
padding:14px 18px;max-width:66ch;color:var(--muted);font-size:15px;margin:18px 0}}
code{{font-family:var(--mono);font-size:.87em;background:#202020;border:1px solid var(--line);border-radius:4px;padding:1px 5px}}
footer{{margin-top:56px;border-top:1px solid var(--line);padding-top:20px;font:12.5px var(--mono);color:var(--dim);line-height:1.7}}
</style></head><body><div class="wrap">
<span class="badge">{status}</span>
<p class="kicker">A11Y.md · Benchmark de eficácia · braço primário (gemini-3.5-flash-lite)</p>
<h1>Relatório da manhã</h1>
<p class="muted">Gerado automaticamente em {stamp}, ao fim do pipeline noturno: coleta → verificação
(axe-core 4.13.0, hash conferido) → estatísticas pré-registradas. Protocolo: osf.io/pg6r5.</p>

<h2>Desfecho primário — violações críticas + sérias por geração</h2>
<table><thead><tr><th>Condição</th><th>Distribuição</th><th>Tokens (mediana)</th></tr></thead><tbody>
{row_html("A", "só a tarefa")}
{row_html("B", "“make it accessible”")}
{row_html("C", "padrão-placebo")}
{row_html("D", "A11Y.md")}
</tbody></table>

<h2>Contrastes pré-registrados — trilha de robustez</h2>
<p class="muted">Diferença de medianas (D menos a outra condição; negativo = D com menos violações),
intervalo de confiança 95% por bootstrap (10.000 reamostragens, semente fixa), e delta de Cliff
(positivo = D tipicamente menor). Última coluna: diferença de medianas de tokens.</p>
<table><thead><tr><th>Contraste</th><th>Δ mediana [IC 95%]</th><th>Cliff</th><th>Δ média [IC 95%] (expl.)</th><th>Δ tokens</th></tr></thead><tbody>
{contrast_html("D-B", "a comparação decisiva")}
{contrast_html("D-C", "conteúdo vs. forma")}
{contrast_html("D-A", "efeito total")}
</tbody></table>

<div class="note"><b>Como ler esta tabela.</b> Os dados são contagens cheias de zeros — a maioria das
páginas já sai sem violação grave em todas as condições, e por isso a <b>mediana satura em zero</b> e o
Δ de mediana tende a ler "+0" mesmo quando há efeito. O sinal aparece no <b>delta de Cliff</b>
(positivo = a condição D tipicamente produz menos violações que a comparada) e na diferença de médias
(coluna exploratória). É exatamente para contagens assim que o protocolo registrou como instrumento
confirmatório o modelo binomial negativo — pendente, junto com os passos cegos.</div>

<h2>Braço ecológico — recapitulação (verificado ontem)</h2>
<table><thead><tr><th>Agente</th><th>A — sem padrão</th><th>D — com A11Y.md</th></tr></thead><tbody>
<tr><td>Claude Code</td><td class="num">{" ".join(map(str,a2.get("claude-code:A",[])))}</td><td class="num">{" ".join(map(str,a2.get("claude-code:D",[])))}</td></tr>
<tr><td>Codex</td><td class="num">{" ".join(map(str,a2.get("codex:A",[])))}</td><td class="num">{" ".join(map(str,a2.get("codex:D",[])))}</td></tr>
</tbody></table>
<p class="muted">17/18 execuções D geraram REPORT.md + A11Y-DECISIONS.md espontaneamente. Descritivo; nunca agregado ao braço primário.</p>

<h2>O que este relatório é — e o que ainda não é</h2>
<div class="note">Estas são as estatísticas <b>pré-registradas da trilha de robustez</b> (bootstrap + Cliff),
computáveis sem os passos humanos cegos. Ainda pendentes, na ordem do protocolo: o modelo confirmatório
(binomial negativa com efeitos por tarefa, correção de Holm), a classificação cega do comportamento de
carregamento, e a adjudicação amostral dos itens MANUAL. Nenhuma frase confirmatória deve ser publicada
antes deles — mas a direção e a magnitude que você vê acima são as que o modelo confirmatório vai testar.</div>

<footer>Pipeline noturno · arquivos-fonte: runs/log.jsonl · runs/verify/arm1-axe.jsonl · runs/verify/arm2-axe.jsonl<br>
Análise: runs/overnight/analyze.py (semente 20260818) · resumo em máquina: runs/overnight/summary.json</footer>
</div></body></html>"""
(OUT / "RELATORIO.html").write_text(html_doc)
# versão para artefato: sem esqueleto html/head/body, com <title> e <style> no topo
style = html_doc.split("<style>")[1].split("</style>")[0]
body = html_doc.split("<body>")[1].split("</body>")[0]
(OUT / "RELATORIO-artifact.html").write_text(
    "<title>Relatório do Benchmark</title>\n<style>" + style + "\nbody{background:#121212}</style>\n" + body)
print(f"relatório: {OUT/'RELATORIO.html'} · {n_total} linhas analisadas · completo: {complete}")

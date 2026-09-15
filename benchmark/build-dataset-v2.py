#!/usr/bin/env python3
"""build-dataset-v2.py — o pacote v2 do dataset do Estudo 1.

O v2 é, por construção, **o v1 mais os arquivos que faltavam**: o pacote é
montado copiando entrada por entrada do zip publicado e só então acrescentando
os novos. Nada é remontado a partir do diretório de trabalho, porque uma
remontagem silenciosamente incorporaria qualquer coisa que tenha mudado por
aqui desde agosto — e o que está publicado é o que precisa ser preservado.

Ao final, cada entrada herdada é conferida contra o SHA-256 que tinha no v1.
A verificação é o ponto do script; o zip é o subproduto.

    python3 build-dataset-v2.py            # monta e verifica
    python3 build-dataset-v2.py --check    # só verifica um v2 já montado
"""
import argparse, hashlib, json, zipfile
from datetime import date
from pathlib import Path

BENCH = Path(__file__).resolve().parent
RUNS = BENCH / "runs"
V1 = RUNS / "dataset" / "a11ymd-benchmark-dataset-v1.zip"
V2 = RUNS / "dataset" / "a11ymd-benchmark-dataset-v2.zip"

# O que a errata acrescenta: os dois instrumentos registrados que nunca rodaram,
# a auditoria exploratória de alvos, a análise de alcance e o texto da errata.
NEW = [
    (RUNS / "verify" / "arm1-checklist.jsonl", "verify/arm1-checklist.jsonl"),
    (RUNS / "verify" / "arm1-pa11y.jsonl",     "verify/arm1-pa11y.jsonl"),
    (RUNS / "verify" / "arm1-pa11y-full.jsonl","verify/arm1-pa11y-full.jsonl"),
    (RUNS / "verify" / "arm1-targets.jsonl",   "verify/arm1-targets.jsonl"),
    (RUNS / "overnight" / "power.json",        "analysis/power.json"),
    (BENCH / "errata" / "ERRATA-study1.md",    "ERRATA-study1.md"),
    (BENCH / "errata" / "README-dataset-v2.md","dataset/README-v2.md"),
]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def build():
    src = zipfile.ZipFile(V1)
    inherited = {}
    with zipfile.ZipFile(V2, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            data = src.read(info.filename)
            out.writestr(info, data)
            if not info.filename.endswith("/"):
                inherited[info.filename] = sha256(data)
        added = {}
        for path, arc in NEW:
            if not path.is_file():
                raise SystemExit(f"ausente, não dá para montar: {path}")
            data = path.read_bytes()
            out.writestr(arc, data)
            added[arc] = sha256(data)
        manifest = {
            "dataset": "A11Y.md efficacy benchmark — raw outputs",
            "version": 2,
            "issued": str(date.today()),
            "supersedes": "a11ymd-benchmark-dataset-v1.zip",
            "protocol": "https://osf.io/pg6r5",
            "repo": "https://github.com/fecarrico/A11Y.md",
            "erratum": "ERRATA-study1.md",
            "change": ("Adds the two registered instruments that were never run — the "
                       "deterministic per-task checklist (co-primary nº 2) and the second "
                       "engine (HTML_CodeSniffer) — over the same 400 pages, plus the "
                       "exploratory target audit and the post-hoc power analysis. No file "
                       "from v1 is modified or removed."),
            "n_files": len(inherited) + len(added),
            "inherited_from_v1": len(inherited),
            "added_in_v2": len(added),
            "files": ([{"path": p, "sha256": h, "from": "v1"} for p, h in sorted(inherited.items())] +
                      [{"path": p, "sha256": h, "from": "v2"} for p, h in sorted(added.items())]),
        }
        out.writestr("dataset/MANIFEST-v2.json", json.dumps(manifest, indent=2))
    return inherited, added

def check(inherited):
    """Toda entrada herdada tem que bater byte a byte com o v1 publicado."""
    a, b = zipfile.ZipFile(V1), zipfile.ZipFile(V2)
    names = [n for n in a.namelist() if not n.endswith("/")]
    bad = [n for n in names if sha256(a.read(n)) != sha256(b.read(n))]
    return len(names), bad

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        inherited, added = build()
        print(f"montado: {V2.name}")
        print(f"  herdadas do v1 : {len(inherited)}")
        print(f"  novas no v2    : {len(added)}")
        for arc in added: print(f"     + {arc}")
    total, bad = check({})
    print(f"\nverificação · {total} entradas herdadas conferidas contra o v1")
    print(f"  divergentes: {bad if bad else 'nenhuma'}")
    print(f"  tamanho: {V2.stat().st_size / 1e6:.2f} MB (v1: {V1.stat().st_size / 1e6:.2f} MB)")

#!/bin/bash
# score-arm.sh <slug-do-modelo> — o encadeamento de pontuação de um braço, na ordem
# que o protocolo exige, com o mesmo instrumento do Estudo 1.
#
#   reparo  → css/js que o extrator descartou, devolvidos do raw da própria geração
#   axe     → build pinada, SHA conferido; sobre o original E sobre o reparado
#   análise → robustness.py e confirmatory.py, os scripts registrados, via flags
#
# Nada aqui é específico deste braço: são os scripts do Arm 1 apontados para
# outro diretório. Um segundo analisador "parecido" seria outro estudo.
set -euo pipefail
cd "$(dirname "$0")"
SLUG="$1"
M="runs/arm1ext/$SLUG"
[ -d "$M" ] || { echo "não existe: $M"; exit 1; }

echo "── 1/4 reparo de artefatos"
python3 verify/repair-artifacts.py --html "$M/html" --raw "$M/raw" --out "$M/html-repaired"

echo "── 2/4 axe sobre as páginas coletadas"
( cd verify && node verify.js --dir "../$M/html" --out "../$M/verify/axe.jsonl" \
      --shots "../$M/verify/screenshots" --resume )

if compgen -G "$M/html-repaired/*.html" > /dev/null; then
  echo "── 2b/4 axe sobre as páginas reparadas (relato duplo, como em 2026-08-23)"
  ( cd verify && node verify.js --dir "../$M/html-repaired" --out "../$M/verify/axe-repaired.jsonl" )
fi

echo "── 3/4 identificadores no log (derivados de task/condition/run)"
python3 - "$M" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1]) / "log.jsonl"
rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
n = 0
for r in rows:
    if "id" not in r:
        r["id"] = f"{r['task']}__{r['condition']}__run{r['run']}"; n += 1
if n:
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
print(f"   id acrescentado a {n} registros")
PY

echo "── 4/4 análises registradas"
mkdir -p "$M/analysis"
python3 analysis/robustness.py --log "$M/log.jsonl" --axe "$M/verify/axe.jsonl" \
    --arm2-log /dev/null --arm2-axe /dev/null --out "$M/analysis"
runs/venv/bin/python analysis/confirmatory.py --log "$M/log.jsonl" \
    --axe "$M/verify/axe.jsonl" --out "$M/analysis/confirmatory.json"
echo "── pronto: $M/analysis"

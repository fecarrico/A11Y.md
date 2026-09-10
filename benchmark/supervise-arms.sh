#!/bin/bash
# supervise-arms.sh — roda os braços restantes em fila, sem depender de vigilância humana.
#
# O que cada mecanismo aqui existe para impedir, todos observados nesta coleta:
#   1. processo morto e ninguém percebe  → reinício automático com --resume
#   2. modelo inalcançável arrastando por horas → --abort-if-slower-than no runner
#   3. um braço quebrado travando os outros    → aborto passa ao próximo da fila
#   4. dois braços concorrendo pelo mesmo limite de taxa → estritamente sequencial
#   5. estado invisível → status.json por braço, atualizado a cada geração
#
# Reinício NÃO é o mesmo que insistir: o runner só volta se o motivo da parada
# foi morte do processo. Se ele mesmo abortou por inviabilidade (código 2), a
# fila respeita a decisão e segue em frente.
set -u
cd "$(dirname "$0")"
MODELS=("openai/gpt-oss-20b" "minimaxai/minimax-m3")
MAX_RESTARTS=5

for M in "${MODELS[@]}"; do
  SLUG=$(echo "$M" | tr -c 'a-z0-9' '-' | sed 's/--*/-/g; s/^-//; s/-$//')
  echo "════════ $M · início $(date -Is) ════════"
  for ((try=1; try<=MAX_RESTARTS; try++)); do
    python3 -u arm1ext.py --model "$M" --resume
    CODE=$?
    case $CODE in
      0) echo "── $M concluído (tentativa $try)"; break ;;
      2) echo "── $M ABORTADO pelo disjuntor — inviável, seguindo para o próximo"; break ;;
      *) echo "── $M caiu com código $CODE na tentativa $try; reiniciando em 60s"
         sleep 60 ;;
    esac
  done
  echo "════════ $M · fim $(date -Is) ════════"
done
echo "FILA CONCLUÍDA $(date -Is)"

#!/usr/bin/env python3
"""Regenera verify/checklist-registered.js a partir do harness registrado.

O checklist determinístico é desfecho co-primário (METHODOLOGY.md §Measurement 2)
e vive em harness/index.html, escrito para rodar num browser aberto à mão. Estes
braços foram coletados por API, então as páginas precisam ser pontuadas em lote —
e a única forma honesta de fazer isso é injetar a MESMA função, extraída do
arquivo registrado, em vez de reescrevê-la para o novo contexto.
"""
import re
from pathlib import Path
src = Path(__file__).resolve().parent.parent / "harness" / "index.html"
out = Path(__file__).resolve().parent / "checklist-registered.js"
block = re.search(r"(/\* ---- pre-registered deterministic checklist.*?\n\}\n)(?=\n/\* ---- runner)",
                  src.read_text(encoding="utf-8"), re.S).group(1)
out.write_text("// EXTRAÍDO VERBATIM de benchmark/harness/index.html.\n"
               "// Gerado por verify/extract-checklist.py — não editar à mão.\n\n"
               + block + "\nwindow.__checklist = checklist;\n", encoding="utf-8")
print(f"regenerado: {out}")

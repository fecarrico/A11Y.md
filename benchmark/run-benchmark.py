#!/usr/bin/env python3
"""run-benchmark.py — serve the harness and analyze the results.

Two modes, both stdlib-only:

  python3 run-benchmark.py            build runs/manifest.json from runs/**/*.html,
                                      serve this folder and open the harness
  python3 run-benchmark.py --analyze results/results.json
                                      completeness check (against the 54-cell design)
                                      + the pre-registered analysis: median
                                      critical+serious per condition and model,
                                      checklist pass-rate, share of zero-critical runs

File naming convention (see RUNBOOK.md):
  runs/<model>/<task>/<condition>/run<N>.html
  model ∈ {claude, gemini, gpt} · task ∈ {task1, task2, task3}
  condition ∈ {bare, grounded} · N ∈ {1, 2, 3}
"""

import http.server
import json
import re
import statistics
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).parent
MODELS, TASKS, CONDITIONS, RUNS = ("claude", "gemini", "gpt"), ("task1", "task2", "task3"), ("bare", "grounded"), (1, 2, 3)
PATTERN = re.compile(r"^(claude|gemini|gpt)/(task[123])/(bare|grounded)/run([123])\.html$")


def build_manifest() -> list[dict]:
    entries = []
    for path in sorted((HERE / "runs").rglob("*.html")):
        rel = path.relative_to(HERE / "runs").as_posix()
        match = PATTERN.match(rel)
        if not match:
            print(f"⚠️  {rel} does not follow the naming convention — skipped (see RUNBOOK.md)")
            continue
        model, task, condition, run = match.groups()
        entries.append({"file": rel, "model": model, "task": task, "condition": condition, "run": int(run)})
    (HERE / "runs" / "manifest.json").write_text(json.dumps(entries, indent=1))
    print(f"manifest.json: {len(entries)} run(s) of {len(MODELS) * len(TASKS) * len(CONDITIONS) * len(RUNS)} cells")
    return entries


def serve() -> None:
    build_manifest()
    if not (HERE / "harness" / "axe.min.js").is_file():
        print("axe.min.js missing — run: python3 harness/fetch-axe.py")
        sys.exit(1)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(HERE), **kwargs)

        def log_message(self, *_):
            pass

    port = 8471
    print(f"Serving http://localhost:{port}/harness/ — Ctrl+C to stop")
    webbrowser.open(f"http://localhost:{port}/harness/")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


def analyze(results_path: str) -> None:
    data = json.loads(Path(results_path).read_text())
    results = [r for r in data["results"] if "error" not in r]
    errored = [r for r in data["results"] if "error" in r]

    message = f"axe {data.get('axeVersion', '?')} · {len(results)} run(s) analyzed"
    if errored:
        message += f" · ⚠️ {len(errored)} errored"
    print(message)

    # completeness against the pre-registered 54-cell design
    seen = {(r["model"], r["task"], r["condition"], r["run"]) for r in results}
    missing = [c for c in ((m, t, c_, n) for m in MODELS for t in TASKS for c_ in CONDITIONS for n in RUNS)
               if c not in seen]
    print(f"cells: {len(seen)}/54" + (f" — missing: {missing}" if missing else " — complete ✓"))

    def crit_serious(r):
        return r["counts"]["critical"] + r["counts"]["serious"]

    print("\nPRIMARY — median critical+serious violations")
    print(f"{'':10}{'bare':>8}{'grounded':>10}")
    for model in MODELS:
        row = []
        for condition in CONDITIONS:
            values = [crit_serious(r) for r in results if r["model"] == model and r["condition"] == condition]
            row.append(f"{statistics.median(values):.1f}" if values else "—")
        print(f"{model:10}{row[0]:>8}{row[1]:>10}")

    print("\nSECONDARY — share of runs with zero critical violations")
    for condition in CONDITIONS:
        values = [r for r in results if r["condition"] == condition]
        zero = sum(1 for r in values if r["counts"]["critical"] == 0)
        print(f"  {condition:9} {zero}/{len(values)}" if values else f"  {condition:9} —")

    print("\nSECONDARY — checklist pass-rate (PASS / applicable)")
    for condition in CONDITIONS:
        passed = applicable = 0
        for r in results:
            if r["condition"] != condition:
                continue
            for verdict in r["checklist"].values():
                if verdict == "N/A" or verdict.startswith("MANUAL"):
                    continue
                applicable += 1
                passed += verdict.startswith("PASS")
        print(f"  {condition:9} {passed}/{applicable}" if applicable else f"  {condition:9} —")

    print("\nRaw medians are the pre-registered outcome; anything beyond this table is exploratory.")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--analyze":
        analyze(sys.argv[2])
    else:
        serve()

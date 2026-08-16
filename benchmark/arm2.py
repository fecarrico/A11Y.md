#!/usr/bin/env python3
"""
arm2.py — the ecological arm: the standard inside a real coding agent.

Arm 1 simulates lazy loading with one scoped tool over a raw API. This arm runs
the standard the way an adopter actually uses it: a project directory, the Quick
Start rule in CLAUDE.md, and Claude Code (official client, `claude -p`) doing
whatever it does. Design frozen in ARM2.md before the first run.

    python3 arm2.py --plan          # what would run, without running
    python3 arm2.py                 # all 18 runs, sequential
    python3 arm2.py --resume        # skip runs already on disk

Stdlib only, no dependencies. Requires the `claude` CLI authenticated with a
subscription; each run is a fresh non-interactive session in a fresh workspace.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BENCH = REPO / "benchmark"
OUT = BENCH / "runs" / "arm2"

sys.path.insert(0, str(BENCH))
from collect import load_tasks  # the same frozen prompts, the same parser

TASKS = ("signup-form", "destructive-confirmation-modal", "dashboard-chart")
CONDITIONS = ("A", "D")
TIMEOUT_S = 40 * 60

# Verbatim Quick Start rule, pointed at the local copy (ARM2.md §Workspaces).
RULE = ("When developing the frontend, follow strictly the accessibility rules "
        "defined in A11Y.md: ./A11Y.md\n")

LINK_CSS = re.compile(r"<link\s+[^>]*rel=[\"']stylesheet[\"'][^>]*>", re.I)
HREF = re.compile(r"href=[\"']([^\"']+)[\"']", re.I)
SCRIPT_SRC = re.compile(r"<script\s+[^>]*src=[\"']([^\"']+)[\"'][^>]*>\s*</script>", re.I)


def build_workspace(condition: str, parent: Path) -> tuple[Path, set[str]]:
    """Create a fresh workspace; return it and the seeded files' relative paths."""
    ws = Path(tempfile.mkdtemp(prefix=f"arm2-{condition}-", dir=parent))
    seeded: set[str] = set()
    if condition == "D":
        src = REPO / "docs" / "en"
        shutil.copy2(src / "A11Y.md", ws / "A11Y.md")
        shutil.copytree(src / "references", ws / "references")
        shutil.copytree(src / "templates", ws / "templates")
        (ws / "CLAUDE.md").write_text(RULE, encoding="utf-8")
        seeded = {str(p.relative_to(ws)) for p in ws.rglob("*") if p.is_file()}
    return ws, seeded


def created_files(ws: Path, seeded: set[str]) -> list[dict]:
    out = []
    for p in sorted(ws.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(ws))
        if rel in seeded or rel.startswith(".claude"):
            continue
        out.append({"path": rel, "bytes": p.stat().st_size})
    return out


def inline_local_assets(html_path: Path) -> str:
    """Mechanical assembly, per the runbook's rule: locally-referenced CSS/JS
    are folded into the page so the harness mounts one file. No editing."""
    ws = html_path.parent
    html = html_path.read_text(encoding="utf-8", errors="replace")

    def css(match):
        href = HREF.search(match.group(0))
        if href:
            f = ws / href.group(1)
            if f.is_file():
                return "<style>\n" + f.read_text(encoding="utf-8", errors="replace") + "\n</style>"
        return match.group(0)

    def js(match):
        f = ws / match.group(1)
        if f.is_file():
            return "<script>\n" + f.read_text(encoding="utf-8", errors="replace") + "\n</script>"
        return match.group(0)

    return SCRIPT_SRC.sub(js, LINK_CSS.sub(css, html))


def pick_html(files: list[dict], ws: Path) -> Path | None:
    candidates = [f for f in files if f["path"].lower().endswith((".html", ".htm"))]
    if not candidates:
        return None
    return ws / max(candidates, key=lambda f: f["bytes"])["path"]


def run_agent(task_prompt: str, ws: Path) -> tuple[dict | None, str, float]:
    started = time.monotonic()
    try:
        proc = subprocess.run(
            ["claude", "-p", task_prompt,
             "--output-format", "json", "--permission-mode", "acceptEdits"],
            cwd=ws, capture_output=True, text=True, timeout=TIMEOUT_S,
        )
        raw = proc.stdout
    except subprocess.TimeoutExpired:
        return None, f"timeout after {TIMEOUT_S}s", time.monotonic() - started
    elapsed = time.monotonic() - started
    if proc.returncode != 0:
        return None, f"exit {proc.returncode}: {proc.stderr[:300]}", elapsed
    try:
        return json.loads(raw), "", elapsed
    except json.JSONDecodeError:
        return {"unparsed_stdout": raw[:20000]}, "stdout was not JSON", elapsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the ecological arm (ARM2.md).")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-workspaces", action="store_true",
                        help="do not delete workspaces after capture (debugging)")
    args = parser.parse_args()

    tasks = load_tasks(BENCH / "PROMPTS.md")
    missing = [t for t in TASKS if t not in tasks]
    if missing:
        print(f"error: tasks not found in PROMPTS.md: {missing}", file=sys.stderr)
        return 2

    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()

    jobs = [(t, c, r) for r in range(1, args.runs + 1) for t in TASKS for c in CONDITIONS]
    html_dir, raw_dir = OUT / "html", OUT / "raw"
    log_path = OUT / "log.jsonl"

    def slug(t, c, r):
        return f"claude-code__{t}__{c}__run{r}"

    if args.resume:
        jobs = [j for j in jobs if not (html_dir / f"{slug(*j)}.html").is_file()]

    print(f"{len(jobs)} run(s) · agent: {version or 'claude (version unknown)'}")
    if args.plan:
        for j in jobs:
            print(f"  {slug(*j)}")
        return 0
    if not jobs:
        print("nothing to do")
        return 0

    html_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="arm2-workspaces-"))
    failures = 0

    for index, (task, condition, run) in enumerate(jobs, 1):
        name = slug(task, condition, run)
        print(f"[{index}/{len(jobs)}] {name}", flush=True)
        ws, seeded = build_workspace(condition, scratch)

        response, error, elapsed = run_agent(tasks[task], ws)
        files = created_files(ws, seeded)
        html_path = pick_html(files, ws)

        record = {
            "id": name, "task": task, "condition": condition, "run": run,
            "agent_version": version,
            "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "duration_s": round(elapsed, 1),
            "files_created": files,
            "html": html_path.name if html_path else None,
        }
        if error:
            failures += 1
            record["error"] = error
            print(f"    FAILED: {error}", flush=True)
        if response is not None:
            (raw_dir / f"{name}.json").write_text(
                json.dumps(response, indent=2, ensure_ascii=False), encoding="utf-8")
            for key in ("total_cost_usd", "usage", "modelUsage", "num_turns", "subtype"):
                if key in response:
                    record[key] = response[key]
        if html_path is not None:
            (html_dir / f"{name}.html").write_text(inline_local_assets(html_path),
                                                   encoding="utf-8")
        with log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(record, ensure_ascii=False) + "\n")

        made = ", ".join(f["path"] for f in files) or "—"
        print(f"    {elapsed:.0f}s · created: {made}", flush=True)

        if not args.keep_workspaces:
            shutil.rmtree(ws, ignore_errors=True)

    if not args.keep_workspaces:
        shutil.rmtree(scratch, ignore_errors=True)
    print(f"\ndone · {len(jobs)} run(s) · {failures} failure(s)\nlog: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

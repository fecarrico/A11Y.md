#!/usr/bin/env python3
"""
run.py — Study 2 collection runner (journeys, single session per run).

Design frozen in PROTOCOL.md (registered; URL in §Registration) and the
consistency instrument in classifier.py (hash in CLASSIFIER.md). This file is
instrumentation, not protocol: every behaviour it implements is dictated by
the frozen documents. Collection opens only after the registration is public
and the agents are named in DEVIATIONS.md.

    python3 run.py --plan                      # what would run
    python3 run.py --agent claude-code --resume
    python3 run.py --agent codex --resume

Stdlib only. One run = one fresh workspace + one fresh session + the whole
journey prompt. Wall clock: 90 minutes, symmetric (PROTOCOL.md §Engines).
"""
import argparse, json, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
S2 = REPO / "benchmark" / "study2"
OUT = REPO / "benchmark" / "runs" / "study2"
TIMEOUT_S = 90 * 60
CONDITIONS = ("A", "B", "D")
RUNS_DEFAULT = 5

RULE = ("When developing the frontend, follow strictly the accessibility rules "
        "defined in A11Y.md: ./A11Y.md\n")
GENERIC = "Make it accessible.\n\n"

AGENTS = {
    "claude-code": {
        "rule_file": "CLAUDE.md",
        "version": ["claude", "--version"],
        "command": lambda prompt: ["claude", "-p", prompt, "--output-format", "json",
                                   "--permission-mode", "acceptEdits"],
    },
    "codex": {
        "rule_file": "AGENTS.md",
        "version": ["codex", "--version"],
        "command": lambda prompt: ["codex", "exec", prompt, "--json",
                                   "--sandbox", "workspace-write",
                                   "--skip-git-repo-check"],
    },
    # Declared reserve (DEVIATIONS.md naming entry): antigravity — fresh
    # profile + --new-project per Study 1's dated amendment, added here only
    # if a quota wall forces the swap, with its own dated entry.
}


def journey_prompt() -> str:
    text = (S2 / "PROMPTS.md").read_text()
    return text[text.index("## `bookstore-journey`"):].split("\n", 1)[1].strip()


def build_workspace(condition: str, parent: Path, rule_file: str):
    ws = Path(tempfile.mkdtemp(prefix=f"study2-{condition}-", dir=parent))
    if condition == "D":
        src = REPO / "docs" / "en"
        shutil.copy2(src / "A11Y.md", ws / "A11Y.md")
        shutil.copytree(src / "references", ws / "references")
        shutil.copytree(src / "templates", ws / "templates")
        (ws / rule_file).write_text(RULE, encoding="utf-8")
    seeded = {str(p.relative_to(ws)) for p in ws.rglob("*") if p.is_file()}
    return ws, seeded


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="claude-code", choices=sorted(AGENTS))
    ap.add_argument("--runs", type=int, default=RUNS_DEFAULT)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    agent = AGENTS[args.agent]

    prompt = journey_prompt()
    version = subprocess.run(agent["version"], capture_output=True, text=True).stdout.strip()
    jobs = [(c, r) for r in range(1, args.runs + 1) for c in CONDITIONS]

    def slug(c, r): return f"{args.agent}__journey__{c}__run{r}"
    if args.resume:
        jobs = [j for j in jobs if not (OUT / "raw" / f"{slug(*j)}.json").is_file()]
    print(f"{len(jobs)} run(s) · agent: {version or args.agent}")
    if args.plan:
        for j in jobs: print(f"  {slug(*j)}")
        return 0

    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    (OUT / "screens").mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="study2-workspaces-"))
    log = OUT / "log.jsonl"

    for i, (condition, run) in enumerate(jobs, 1):
        name = slug(condition, run)
        print(f"[{i}/{len(jobs)}] {name}", flush=True)
        ws, seeded = build_workspace(condition, scratch, agent["rule_file"])
        full = (GENERIC + prompt) if condition == "B" else prompt
        t0 = time.time()
        try:
            r = subprocess.run(agent["command"](full), cwd=ws, capture_output=True,
                               text=True, timeout=TIMEOUT_S)
            raw, err = r.stdout, ("" if r.returncode == 0 else f"exit {r.returncode}")
        except subprocess.TimeoutExpired:
            raw, err = "", "TIMEOUT 90m"
        elapsed = round(time.time() - t0, 1)

        dest = OUT / "screens" / name
        dest.mkdir(parents=True, exist_ok=True)
        produced = []
        for p in sorted(ws.rglob("*")):
            if not p.is_file(): continue
            rel = str(p.relative_to(ws))
            if rel in seeded or rel.split("/")[0].startswith("."): continue
            tgt = dest / rel
            tgt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, tgt)
            produced.append({"path": rel, "bytes": p.stat().st_size})
        (OUT / "raw" / f"{name}.json").write_text(raw or "{}", encoding="utf-8")
        record = {"id": name, "agent": args.agent, "condition": condition, "run": run,
                  "agent_version": version, "duration_s": elapsed,
                  "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  "screens": sum(1 for f in produced if f["path"].endswith(".html")),
                  "files_created": produced}
        if err: record["error"] = err
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"    {elapsed/60:.1f} min · {record['screens']} telas"
              + (f" · {err}" if err else ""), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

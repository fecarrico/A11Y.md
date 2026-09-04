#!/usr/bin/env python3
"""
run.py — Round 2 collection runner (4 conditions, tag-archived treatments).

Instrumentation for PROTOCOL.md — every behaviour here is dictated by
the protocol; this file adds none. Frozen by hash before registration;
collection opens only after the registration is public.

    python3 run.py --plan
    python3 run.py --agent claude-code --pinned-version "2.1.233 (Claude Code)" \
                   --home /path/to/sanitized-home --resume
    python3 run.py --agent claude-code --pinned-version ... --home ... --gate-probe
    python3 run.py --self-test

What the protocol dictates, implemented here:
  * Conditions A · B · D18 (tag v1.8.0) · D20 (tag v2.0.0); slugs keep the
    4-field shape agent__journey__COND__runN.
  * Treatment = closed path list from `git archive <tag> -- docs/en/A11Y.md
    docs/en/references docs/en/templates tools`, laid out exactly like Round
    1's workspaces (A11Y.md, references/, templates/ — plus tools/ — at the
    workspace root). Per-condition SHA-256 over the archive's files
    concatenated in path order is computed at start, printed by --plan and
    written into every log record.
  * Interleaved collection: for each run index 1..N, conditions run in the
    order A, B, D18, D20 before the next index — including under --resume.
  * Version pinning: --pinned-version is required for collection; the client
    version is re-read before EVERY run and the runner aborts on mismatch
    (auto-update mid-collection is the failure this guards against).
  * Sanitized HOME: --home is required for collection; the subprocess runs
    with HOME (and USERPROFILE) pointed there; the path is logged per run.
  * Retention (mechanical): a run is retained iff it produces 7 non-empty
    screens within the 90-minute clock. Not-retained is DATA, not a retry.
  * Retry (mechanical, infra only): non-zero exit AND zero screens produced
    → retry, max 2; timeouts never retry; every attempt's raw output and log
    record are preserved (nothing deleted).
  * Gate probe (--gate-probe): one B-style single-screen probe per agent,
    stored under probes/, with the audit instruction printed — retained only
    if the transcript shows no reference to, or search for, the standard or
    the operator's files (audited by grep + human eye, journaled).

Stdlib only. One run = one fresh workspace + one fresh session + the whole
journey prompt, verbatim from ../study2/PROMPTS.md.
"""
import argparse, hashlib, io, json, os, shutil, subprocess, sys, tarfile, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
S2 = REPO / "benchmark" / "study2"
OUT = REPO / "benchmark" / "runs" / "round2"
TIMEOUT_S = 90 * 60
CONDITIONS = ("A", "B", "D18", "D20")   # interleaving order within each index
TAGS = {"D18": "v1.8.0", "D20": "v2.0.0"}
TREATMENT_PATHS = ("docs/en/A11Y.md", "docs/en/references", "docs/en/templates", "tools")
RUNS_DEFAULT = 5
MAX_RETRIES = 2

RULE = ("When developing the frontend, follow strictly the accessibility rules "
        "defined in A11Y.md: ./A11Y.md\n")
GENERIC = "Make it accessible.\n\n"

PROBE_PROMPT = (GENERIC +
    "Build the home page of a small online bookstore called \"Loop Books\" as a "
    "static site: a single index.html with plain HTML, CSS and JavaScript, no "
    "build step, no external libraries or fonts. Header with the site name, "
    "main navigation, and a grid of six featured book cards (cover image, "
    "title, author, price, \"Add to cart\" button) from realistic hardcoded "
    "data.")

AGENTS = {
    "claude-code": {
        "rule_file": "CLAUDE.md",
        "version": ["claude", "--version"],
        "command": lambda prompt: ["claude", "-p", prompt, "--output-format", "json",
                                   "--permission-mode", "acceptEdits"],
    },
    # Reserve naming per protocol; command shape inherited unchanged from the
    # Round-1 swap entry (fresh profile via --home, --new-project per run,
    # rule as prompt preamble per ARM2.md's bridge-cell translation).
    "antigravity": {
        "rule_file": None,
        "prompt_rule": True,
        "version": ["agy", "--version"],
        # 2026-09-04 deviations (both journaled): client 1.1.26 first
        # rejected --effort for gemini-3.5-flash, then revealed the model
        # itself was RETIRED from the catalog (only 3.6/3.7/3.8 Flash
        # remain). Successor chosen by the Round-1 rule (the CURRENT
        # mainline flash at collection time, low effort): gemini-3.8-flash
        # + --effort low. Zero runs were ever collected under the old
        # command — every failed attempt was a CLI rejection.
        "command": lambda prompt: ["agy", "-p", prompt,
                                   "--model", "gemini-3.8-flash",
                                   "--effort", "low",
                                   "--output-format", "json",
                                   "--mode", "accept-edits",
                                   "--print-timeout", "90m",
                                   "--new-project"],
    },
}
# Codex rule (closed in the protocol): skip — quota resets 2026-09-16,
# colliding with the calendar; named a Round-3 candidate. Not listed above.


def journey_prompt() -> str:
    text = (S2 / "PROMPTS.md").read_text()
    return text[text.index("## `bookstore-journey`"):].split("\n", 1)[1].strip()


def archive_bytes(tag: str) -> bytes:
    r = subprocess.run(["git", "-C", str(REPO), "archive", tag, "--"] + list(TREATMENT_PATHS),
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git archive {tag} failed: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


def treatment_hash(tar_bytes: bytes) -> str:
    """SHA-256 over the archive's file contents concatenated in path order —
    the per-condition hash the registration carries."""
    h = hashlib.sha256()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tf:
        members = sorted((m for m in tf.getmembers() if m.isfile()), key=lambda m: m.name)
        for m in members:
            h.update(tf.extractfile(m).read())
    return h.hexdigest()


def build_workspace(condition: str, parent: Path, rule_file: str, archives: dict):
    """Fresh workspace per run. D conditions are laid out like Round 1's:
    A11Y.md, references/, templates/ at the root — plus the tag's tools/."""
    ws = Path(tempfile.mkdtemp(prefix=f"round2-{condition}-", dir=parent))
    if condition in TAGS:
        with tarfile.open(fileobj=io.BytesIO(archives[condition])) as tf:
            tf.extractall(ws, filter="data")
        en = ws / "docs" / "en"
        (en / "A11Y.md").rename(ws / "A11Y.md")
        for d in ("references", "templates"):
            if (en / d).is_dir(): (en / d).rename(ws / d)
        shutil.rmtree(ws / "docs")
        # tools/ (when the tag has it) is already at the root — the standard
        # points at tools/contrast-check.py relative to the workspace root.
        if rule_file:
            (ws / rule_file).write_text(RULE, encoding="utf-8")
    seeded = {str(p.relative_to(ws)) for p in ws.rglob("*") if p.is_file()}
    return ws, seeded


def client_version(agent: dict, env: dict) -> str:
    r = subprocess.run(agent["version"], capture_output=True, text=True, env=env)
    return r.stdout.strip()


def collect_produced(ws: Path, seeded: set, dest: Path):
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
    return produced


def screens_in(produced: list) -> int:
    return sum(1 for f in produced if f["path"].endswith(".html") and f["bytes"] > 0)


def one_attempt(agent, full_prompt, ws, env):
    t0 = time.time()
    try:
        r = subprocess.run(agent["command"](full_prompt), cwd=ws, capture_output=True,
                           text=True, timeout=TIMEOUT_S, env=env)
        raw = r.stdout
        err = "" if r.returncode == 0 else f"exit {r.returncode}: {(r.stderr or r.stdout)[-500:].strip()}"
        rc = r.returncode
    except subprocess.TimeoutExpired:
        raw, err, rc = "", "TIMEOUT 90m", None
    return raw, err, rc, round(time.time() - t0, 1)


def run_collection(args):
    agent = AGENTS[args.agent]
    prompt = journey_prompt()
    archives = {c: archive_bytes(t) for c, t in TAGS.items()}
    hashes = {c: treatment_hash(archives[c]) for c in TAGS}

    jobs = [(c, r) for r in range(1, args.runs + 1) for c in CONDITIONS]
    def slug(c, r): return f"{args.agent}__journey__{c}__run{r}"
    if args.resume:
        jobs = [j for j in jobs if not (OUT / "raw" / f"{slug(*j)}.json").is_file()]

    print(f"{len(jobs)} run(s) · agent: {args.agent}")
    for c in TAGS:
        print(f"  treatment {c} = {TAGS[c]} · sha256 {hashes[c]}")
    if args.plan:
        for j in jobs: print(f"  {slug(*j)}")
        return 0

    if not args.pinned_version:
        sys.exit("collection requires --pinned-version (the registered client version)")
    if not args.home:
        sys.exit("collection requires --home (the sanitized per-agent HOME)")
    env = {**os.environ, "HOME": args.home, "USERPROFILE": args.home}

    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    (OUT / "screens").mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="round2-workspaces-"))
    log = OUT / "log.jsonl"

    for i, (condition, run) in enumerate(jobs, 1):
        name = slug(condition, run)
        version = client_version(agent, env)
        if version != args.pinned_version:
            sys.exit(f"ABORT before {name}: client version {version!r} != pinned "
                     f"{args.pinned_version!r} (protocol: version changes only between "
                     f"complete cycles, logged)")
        print(f"[{i}/{len(jobs)}] {name}", flush=True)

        full = (GENERIC + prompt) if condition == "B" else prompt
        if condition in TAGS and agent.get("prompt_rule"):
            full = RULE + "\n" + full

        for attempt in range(1, MAX_RETRIES + 2):
            ws, seeded = build_workspace(condition, scratch, agent["rule_file"], archives)
            raw, err, rc, elapsed = one_attempt(agent, full, ws, env)
            produced = collect_produced(ws, seeded, OUT / "screens" / name)
            screens = screens_in(produced)
            infra = (rc is not None and rc != 0 and screens == 0)
            final = (not infra) or (attempt == MAX_RETRIES + 1)
            raw_name = f"{name}.json" if final else f"{name}__attempt{attempt}.json"
            (OUT / "raw" / raw_name).write_text(raw or "{}", encoding="utf-8")
            record = {"id": name, "agent": args.agent, "condition": condition, "run": run,
                      "attempt": attempt, "agent_version": version,
                      "treatment_sha256": hashes.get(condition),
                      "home": args.home, "duration_s": elapsed,
                      "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "screens": screens, "retained": final and screens == 7 and not err,
                      "files_created": produced}
            if err: record["error"] = err
            with log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"    attempt {attempt}: {elapsed/60:.1f} min · {screens} telas"
                  + (f" · {err}" if err else "")
                  + ("" if final else " · infra error — mechanical retry"), flush=True)
            if final: break
    return 0


def run_gate_probe(args):
    agent = AGENTS[args.agent]
    if not args.home:
        sys.exit("--gate-probe requires --home (the sanitized per-agent HOME)")
    env = {**os.environ, "HOME": args.home, "USERPROFILE": args.home}
    version = client_version(agent, env)
    probes = OUT / "probes"; probes.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="round2-probe-"))
    ws, seeded = build_workspace("A", scratch, agent["rule_file"], {})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{args.agent}__gate-probe__{stamp}"
    print(f"gate probe: {name} (agent {version})")
    raw, err, rc, elapsed = one_attempt(agent, PROBE_PROMPT, ws, env)
    produced = collect_produced(ws, seeded, probes / name)
    (probes / f"{name}.json").write_text(raw or "{}", encoding="utf-8")
    (probes / f"{name}.meta.json").write_text(json.dumps(
        {"id": name, "agent": args.agent, "agent_version": version, "home": args.home,
         "duration_s": elapsed, "error": err or None,
         "screens": screens_in(produced),
         "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {elapsed/60:.1f} min · {screens_in(produced)} tela(s)" + (f" · {err}" if err else ""))
    print("AUDIT (protocol): the agent's HOME passes only if the probe transcript "
          "contains no reference to, or search for, the standard or the operator's "
          "files. Grep the raw capture for e.g. 'A11Y', 'a11y', 'vault', 'readme', "
          "'Documentos', then read it whole; journal the verdict in DEVIATIONS.md "
          "before any retained run.")
    return 0


# ---------------------------------------------------------------------------
# --self-test: the mechanics against a synthetic 40-run fixture (fake client)
# ---------------------------------------------------------------------------

FAKE_CLIENT = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
if "--version" in sys.argv:
    print(os.environ.get("FAKE_VERSION", "fake 1.0.0")); sys.exit(0)
marker = Path(os.environ["FAKE_STATE"]) / "fail-once"
if marker.is_file():
    marker.unlink()
    sys.stderr.write("simulated infra failure: connection reset\n")
    sys.exit(2)
n = int(os.environ.get("FAKE_SCREENS", "7"))
for i in range(n):
    Path(f"screen{i}.html").write_text(f"<html><body>tela {i}</body></html>")
print(json.dumps({"ok": True}))
'''

def self_test():
    global OUT, TIMEOUT_S
    ok = True
    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  {name}: got {got!r} want {want!r} {'ok' if good else 'SELF-TEST FAILURE'}")

    td = Path(tempfile.mkdtemp(prefix="round2-selftest-"))
    fake = td / "fake-client.py"
    fake.write_text(FAKE_CLIENT); fake.chmod(0o755)
    state = td / "state"; state.mkdir()
    home = td / "home"; home.mkdir()
    os.environ["FAKE_STATE"] = str(state)
    os.environ["FAKE_VERSION"] = "fake 1.0.0"

    AGENTS["fake"] = {
        "rule_file": "CLAUDE.md",
        "version": [sys.executable, str(fake), "--version"],
        "command": lambda prompt: [sys.executable, str(fake), prompt],
    }
    out_orig = OUT
    OUT = td / "out"

    print("treatment archives — layout and per-condition hash:")
    archives = {c: archive_bytes(t) for c, t in TAGS.items()}
    h1 = {c: treatment_hash(archives[c]) for c in TAGS}
    h2 = {c: treatment_hash(archive_bytes(t)) for c, t in TAGS.items()}
    check("hash deterministic across re-archives", h1, h2)
    check("D18 and D20 hashes differ", h1["D18"] != h1["D20"], True)
    ws, seeded = build_workspace("D20", td, "CLAUDE.md", archives)
    check("D20 root layout", sorted(p.name for p in ws.iterdir()),
          sorted(["A11Y.md", "references", "templates", "tools", "CLAUDE.md"]))
    check("D20 ships the contrast tool", (ws / "tools" / "contrast-check.py").is_file(), True)
    ws18, _ = build_workspace("D18", td, "CLAUDE.md", archives)
    check("D18 has no contrast tool (the asymmetry IS the treatment)",
          (ws18 / "tools" / "contrast-check.py").is_file(), False)
    check("A workspace is empty of treatment",
          build_workspace("A", td, "CLAUDE.md", archives)[1], set())

    print("interleaving — order and resume:")
    jobs = [(c, r) for r in range(1, 6) for c in CONDITIONS]
    check("20 jobs per agent (40 total across the 2 agents)", len(jobs), 20)
    check("first cycle order", jobs[:4], [("A",1),("B",1),("D18",1),("D20",1)])
    check("second cycle starts after full first", jobs[4], ("A", 2))

    print("collection mechanics on the synthetic fixture (fake client, 20 runs/agent):")
    class A: pass
    a = A(); a.agent = "fake"; a.runs = 5; a.plan = False; a.resume = False
    a.pinned_version = "fake 1.0.0"; a.home = str(home)
    TIMEOUT_S = 60
    rc = run_collection(a)
    check("run_collection exits 0", rc, 0)
    log_lines = [json.loads(l) for l in (OUT / "log.jsonl").read_text().splitlines()]
    check("20 records", len(log_lines), 20)
    check("all retained (7 screens, no error)", all(r["retained"] for r in log_lines), True)
    check("interleaved order in the log",
          [r["condition"] for r in log_lines[:4]], ["A", "B", "D18", "D20"])
    check("D records carry the treatment hash",
          all(r["treatment_sha256"] == h1[r["condition"]] for r in log_lines
              if r["condition"] in TAGS), True)
    check("A/B records carry no treatment hash",
          all(r["treatment_sha256"] is None for r in log_lines
              if r["condition"] not in TAGS), True)
    check("HOME logged on every record", all(r["home"] == str(home) for r in log_lines), True)

    print("resume — skips existing, preserves order:")
    (OUT / "raw" / "fake__journey__A__run1.json").is_file() or check("raw exists", False, True)
    a.resume = True
    jobs_left = [(c, r) for r in range(1, 6) for c in CONDITIONS
                 if not (OUT / "raw" / f"fake__journey__{c}__run{r}.json").is_file()]
    check("nothing left after full collection", jobs_left, [])

    print("mechanical retry — infra failure retried, everything preserved:")
    (state / "fail-once").write_text("")
    shutil.rmtree(OUT); a.resume = False; a.runs = 1
    rc = run_collection(a)
    log_lines = [json.loads(l) for l in (OUT / "log.jsonl").read_text().splitlines()]
    check("first job failed once then succeeded",
          [r["attempt"] for r in log_lines[:2]], [1, 2])
    check("failed attempt logged, not retained",
          (log_lines[0]["retained"], "error" in log_lines[0]), (False, True))
    check("failed attempt's raw preserved",
          (OUT / "raw" / "fake__journey__A__run1__attempt1.json").is_file(), True)
    check("retained attempt's raw at the canonical name",
          (OUT / "raw" / "fake__journey__A__run1.json").is_file(), True)

    print("retention — short runs are data, never retried:")
    os.environ["FAKE_SCREENS"] = "5"
    shutil.rmtree(OUT); a.runs = 1
    rc = run_collection(a)
    log_lines = [json.loads(l) for l in (OUT / "log.jsonl").read_text().splitlines()]
    check("5-screen run logged once (no retry), not retained",
          [(r["attempt"], r["retained"]) for r in log_lines[:1]], [(1, False)])
    os.environ["FAKE_SCREENS"] = "7"

    print("version pinning — mismatch aborts before running:")
    a.pinned_version = "fake 9.9.9"
    shutil.rmtree(OUT)
    try:
        run_collection(a); check("abort on version mismatch", "no exit", "SystemExit")
    except SystemExit as e:
        check("abort on version mismatch", "ABORT" in str(e.code), True)

    OUT = out_orig
    print("self-test:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="claude-code", choices=sorted(AGENTS))
    ap.add_argument("--runs", type=int, default=RUNS_DEFAULT)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--pinned-version", default=None,
                    help="registered client version; runner aborts if the live client differs")
    ap.add_argument("--home", default=None,
                    help="sanitized per-agent HOME (required for collection and probes)")
    ap.add_argument("--gate-probe", action="store_true",
                    help="run the B-style contamination probe instead of collecting")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
    if args.gate_probe:
        return run_gate_probe(args)
    return run_collection(args)


if __name__ == "__main__":
    sys.exit(main())

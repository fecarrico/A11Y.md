#!/usr/bin/env python3
"""
build_home.py — build the sanitized per-agent HOME the protocol requires.

PROTOCOL-DRAFT.md §Environment hygiene: "Dedicated sanitized HOME per agent —
credentials and client configuration only; no user skills, no personal
CLAUDE.md, no vault grants, no additionalDirectories. The profile's full
contents are listed in the frozen snapshot."

This script is the auditable answer to Round 1's leakage entry
(study2/DEVIATIONS.md, 2026-08-29): the operator's live HOME carried a skill
that named the standard in every system prompt and a permission grant
pre-approving reads of the operator's vault. Round 2 agents get a HOME built
from an explicit allow-list — nothing else — and the build emits a MANIFEST
(path, size, sha256) that goes into the frozen snapshot verbatim.

    python3 build_home.py --agent claude-code --dest ~/benchmark-homes/claude-code
    python3 build_home.py --agent antigravity --dest ~/benchmark-homes/antigravity

The manifest deliberately lists EVERY file in the built HOME, so any later
addition is visible as a snapshot mismatch. Validation of sufficiency is the
gate probe (`run.py --gate-probe`), not this script: if the client cannot
authenticate from this HOME, extend the allow-list, rebuild, re-run the
probe, and journal the change.

Stdlib only.
"""
import argparse, hashlib, json, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

# Closed allow-list: credentials and client configuration ONLY.
# Sources are relative to the operator's real HOME; missing sources are
# reported, not silently skipped.
ALLOW = {
    "claude-code": [
        ".claude/.credentials.json",   # OAuth credentials
    ],
    # The gate probe (2026-08-30) proved the empty HOME insufficient for
    # client 1.1.18: it demands interactive OAuth. The credential lives at
    # ~/.gemini/antigravity-cli/antigravity-oauth-token — ONLY that file
    # enters. Deliberately excluded, found in the live profile during this
    # very extension: ~/.gemini/GEMINI.md (the operator's global context,
    # whose FIRST line points the client at the standard — the same channel
    # class as the Round-1 Claude Code leakage), plus brain/, conversations/,
    # knowledge/, settings.json. The sanitized HOME cuts them by construction.
    "antigravity": [
        ".gemini/antigravity-cli/antigravity-oauth-token",
    ],
}

# Written fresh into the sanitized HOME (never copied from the real one):
# a minimal settings file with NO hooks, NO additional directories, and a
# single narrow permission — so the leakage channel cannot re-enter by
# copy. The one grant (author's directive, 2026-08-30, pre-freeze:
# "everything that came after must be tested" — the contrast checker was
# born from the earlier studies' findings): pre-approve executing
# tools/contrast-check.py and nothing else. The grant is UNIFORM across
# conditions; only the D20 workspace ships the file, so the asymmetry
# remains the treatment. It simulates the approval an interactive user
# gives when the agent asks to run the standard's own tool; both spellings
# cover the cwd-relative and absolute-path invocations the pilot observed.
CLAUDE_SETTINGS = {
    "permissions": {
        "allow": [
            "Bash(python3 tools/contrast-check.py:*)",
            "Bash(python tools/contrast-check.py:*)",
            "Bash(python3 */tools/contrast-check.py:*)",
            "Bash(python */tools/contrast-check.py:*)",
        ],
        "deny": [],
    },
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, choices=sorted(ALLOW))
    ap.add_argument("--dest", required=True, help="target HOME directory (must not exist)")
    ap.add_argument("--source-home", default=str(Path.home()),
                    help="operator HOME to copy credentials from")
    args = ap.parse_args()

    dest = Path(args.dest).expanduser().resolve()
    src_home = Path(args.source_home).expanduser().resolve()
    if dest.exists():
        sys.exit(f"ABORT: {dest} already exists — a sanitized HOME is built once, "
                 f"snapshotted, and never edited in place (rebuild under a new path).")
    dest.mkdir(parents=True)

    copied, missing = [], []
    for rel in ALLOW[args.agent]:
        src = src_home / rel
        if not src.is_file():
            missing.append(rel); continue
        tgt = dest / rel
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, tgt)
        copied.append(rel)

    if args.agent == "claude-code":
        s = dest / ".claude" / "settings.json"
        s.parent.mkdir(parents=True, exist_ok=True)
        s.write_text(json.dumps(CLAUDE_SETTINGS, indent=1) + "\n", encoding="utf-8")

    manifest = {
        "agent": args.agent,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "allow_list": ALLOW[args.agent],
        "copied": copied,
        "missing_sources": missing,
        "files": [
            {"path": str(p.relative_to(dest)), "bytes": p.stat().st_size,
             "sha256": sha256(p)}
            for p in sorted(dest.rglob("*")) if p.is_file()
        ],
    }
    (dest / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"built {dest} for {args.agent}: {len(manifest['files'])} file(s)")
    for f in manifest["files"]:
        print(f"  {f['path']}  {f['bytes']}B  {f['sha256'][:16]}…")
    if missing:
        print(f"MISSING sources (extend or accept, then journal): {missing}")
    print("Next: run the gate probe against this HOME before any retained run:\n"
          f"  python3 run.py --agent {args.agent} --home {dest} --gate-probe")
    return 0


if __name__ == "__main__":
    sys.exit(main())

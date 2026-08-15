#!/usr/bin/env python3
"""fetch-axe.py — vendor the pinned axe-core build for the benchmark harness.

The methodology pre-registers a *pinned* axe version. This script downloads
exactly that build and verifies its SHA-256 against `axe.lock`, so every run
of the benchmark — on any machine, at any date — measures with the same
engine. The file itself is gitignored (580KB of minified vendor code); the
lock, which is what makes it reproducible, is committed.

Usage:
    python3 fetch-axe.py           # download + verify against axe.lock

Stdlib only, no dependencies.
"""

import hashlib
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent


def read_lock() -> dict:
    lock = {}
    for line in (HERE / "axe.lock").read_text().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            lock[key.strip()] = value.strip()
    return lock


def main() -> int:
    lock = read_lock()
    target = HERE / "axe.min.js"

    print(f"Fetching axe-core {lock['version']} …")
    data = urllib.request.urlopen(lock["url"] if "://" in lock["url"] else "https:" + lock["url"], timeout=60).read()

    digest = hashlib.sha256(data).hexdigest()
    if digest != lock["sha256"]:
        print(f"✗ SHA-256 mismatch!\n  expected {lock['sha256']}\n  got      {digest}", file=sys.stderr)
        print("  The published file changed. Do NOT proceed — investigate before running the benchmark.",
              file=sys.stderr)
        return 1

    target.write_bytes(data)
    print(f"✓ {target.name} ({len(data):,} bytes) — SHA-256 verified against axe.lock")
    return 0


if __name__ == "__main__":
    sys.exit(main())

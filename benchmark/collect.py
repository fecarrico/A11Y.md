#!/usr/bin/env python3
"""
collect.py — runs the efficacy benchmark against the Gemini API, unattended.

The standard is loaded lazily: the core is read first, and a reference guide is
consulted only when the task calls for it (A11Y.md §2.1). A plain prompt cannot
reproduce that — paste everything and the mechanism is gone; paste the core alone
and the model has no way to open the guide it was told to open. So this collector
gives the model ONE tool, `read_file`, scoped to a single directory, and lets the
mechanism run. Which files it opens is itself a measurement.

Every response is written to disk verbatim before anything is parsed, so a wrong
field name costs a re-parse, never a re-collection.

    python3 collect.py --probe                 # one call, dumps the raw response
    python3 collect.py --plan                  # what would run, without running
    python3 collect.py --conditions A,B,D --tasks form,modal --runs 3
    python3 collect.py --resume                # skip generations already on disk

Set GEMINI_API_KEY in the environment or in benchmark/.env (git-ignored).
Free-tier limits differ per model and change — check yours at
https://aistudio.google.com/rate-limit and pass --rpm / --daily-cap to match.

Stdlib only, no dependencies.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_MODEL = "gemini-3.5-flash-lite"

REPO = Path(__file__).resolve().parent.parent
BENCH = REPO / "benchmark"

# The four prompt conditions. Only D gets the real standard; C is the placebo —
# same size, same shape, same tool, different subject. Without it, "the model did
# better because a long organised document was in context" stays unfalsified.
CONDITIONS = {
    "A": {"label": "bare", "preamble": None, "docs": None},
    "B": {"label": "generic", "preamble": "Make it accessible.", "docs": None},
    "C": {"label": "control", "preamble": None, "docs": "control"},
    "D": {"label": "a11ymd", "preamble": None, "docs": "standard"},
}

# Each document set carries its own entry file and its own invocation sentence.
#
# The standard's sentence is verbatim from its Quick Start, which is how adopters
# are actually told to invoke it. Nothing is added: no hint that reference files
# exist, no instruction to load selectively. Lazy loading has to emerge from
# reading the core, or the benchmark is teaching the behaviour it claims to
# measure. The only concession to the harness is naming the tool, since the model
# cannot discover it otherwise.
#
# The control's sentence is the same sentence with the subject swapped — same
# shape, same verb, same strictness, different domain. If it read "accessibility"
# too, the placebo would be cueing the very thing it exists to rule out.
DOC_SETS = {
    "standard": {
        "root": REPO / "docs" / "en",
        "entry": "A11Y.md",
        "grounding": ("When developing the frontend, follow strictly the accessibility "
                      "rules defined in A11Y.md. Read it with the read_file tool at `{entry}`."),
    },
    "control": {
        "root": BENCH / "control-standard",
        "entry": "PERF.md",
        "grounding": ("When developing the frontend, follow strictly the performance "
                      "rules defined in PERF.md. Read it with the read_file tool at `{entry}`."),
    },
}

READ_FILE_TOOL = {
    "type": "function",
    "name": "read_file",
    "description": (
        "Read a UTF-8 text file from the standard's directory. "
        "Paths are relative to the standard's root, e.g. 'A11Y.md' or "
        "'references/guide-forms.md'."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path relative to the standard's root directory.",
            }
        },
        "required": ["path"],
    },
}


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def slugify(heading: str) -> str:
    """Derive a short id from a task heading.

    'Task 1 — Signup form' -> 'signup-form'. The pre-registered PROMPTS.md is not
    edited to suit this script: it names tasks for humans, and the part after the
    dash is the name worth keeping.
    """
    tail = re.split(r"\s+[—–-]\s+", heading.strip(), maxsplit=1)[-1]
    slug = re.sub(r"[^a-z0-9]+", "-", tail.lower()).strip("-")
    return slug or re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def load_tasks(path: Path) -> dict[str, str]:
    """Read task prompts: any '## heading' followed by a fenced block."""
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    tasks = {}
    for match in re.finditer(r"^##\s+(.+?)\s*$\n+```[a-z]*\n(.*?)\n```",
                             text, re.M | re.S):
        tasks[slugify(match.group(1))] = match.group(2).strip()
    return tasks


# --------------------------------------------------------------------------
# Response shape discovery.
#
# The Interactions API is new and its field names are not pinned here. Rather
# than hard-code a guess, walk the response and recognise things by shape. If
# Google renames a wrapper, this keeps working; if it renames the leaves, --probe
# shows you exactly what to adjust.
# --------------------------------------------------------------------------

def walk(node):
    """Yield every dict nested anywhere in a JSON structure."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


def find_function_calls(response: dict) -> list[dict]:
    calls = []
    for node in walk(response):
        if node.get("type") == "function_call" and node.get("name"):
            calls.append(node)
        elif "functionCall" in node and isinstance(node["functionCall"], dict):
            fc = node["functionCall"]
            calls.append({"type": "function_call", "name": fc.get("name"),
                          "arguments": fc.get("args") or fc.get("arguments") or {},
                          "id": fc.get("id") or node.get("id")})
    return calls


def find_text(response: dict) -> str:
    """Concatenate assistant text, ignoring text that belongs to a tool result."""
    chunks = []
    for node in walk(response):
        if node.get("type") in ("function_result", "function_call"):
            continue
        text = node.get("text")
        if isinstance(text, str) and text.strip():
            chunks.append(text)
    # De-duplicate while preserving order: nested containers can repeat a leaf.
    seen, unique = set(), []
    for chunk in chunks:
        if chunk not in seen:
            seen.add(chunk)
            unique.append(chunk)
    return "\n".join(unique)


def find_usage(response: dict) -> dict:
    for key in ("usage", "usageMetadata", "usage_metadata"):
        value = response.get(key)
        if isinstance(value, dict):
            return value
    for node in walk(response):
        for key in ("usage", "usageMetadata", "usage_metadata"):
            value = node.get(key)
            if isinstance(value, dict):
                return value
    numeric = {}
    for node in walk(response):
        for key, value in node.items():
            if isinstance(value, int) and "token" in key.lower():
                numeric[key] = value
    return numeric


def sum_usage(usages: list[dict]) -> dict:
    """Add up the per-call usage of one generation.

    A generation is several API calls when the model opens a guide, so the cost of
    a task is the sum, not the last call. Only integer fields are summed; the
    by-modality breakdown is a list and is left to the raw responses.

    Worth watching in the totals: `total_thought_tokens` (this model reasons by
    default, and reasoning is billed) and `total_cached_tokens` (the standard's
    core repeats across calls, so anything cached is cost that did not recur).
    """
    total: dict[str, int] = {}
    for usage in usages:
        for key, value in usage.items():
            if isinstance(value, int) and not isinstance(value, bool):
                total[key] = total.get(key, 0) + value
    return total


def find_interaction_id(response: dict) -> str | None:
    for key in ("id", "interaction_id", "interactionId", "name"):
        value = response.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def extract_html(text: str) -> str:
    """Prefer a fenced html block; fall back to the raw text, unedited."""
    fences = re.findall(r"```(?:html)?\s*\n(.*?)```", text, re.S)
    if fences:
        return max(fences, key=len).strip()
    return text.strip()


# --------------------------------------------------------------------------


class RateLimiter:
    def __init__(self, rpm: int):
        self.interval = 60.0 / rpm if rpm > 0 else 0.0
        self.last = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        elapsed = time.monotonic() - self.last
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last = time.monotonic()


def post(body: dict, api_key: str, timeout: int, retries: int = 4) -> dict:
    payload = json.dumps(body).encode("utf-8")
    delay = 5.0
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            API_URL, data=payload, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:400]
            if error.code in (429, 500, 502, 503, 504) and attempt < retries:
                print(f"    HTTP {error.code}, retrying in {delay:.0f}s", flush=True)
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"HTTP {error.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt < retries:
                print(f"    {error}, retrying in {delay:.0f}s", flush=True)
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(str(error)) from None
    raise RuntimeError("exhausted retries")


def read_scoped(root: Path, relative: str) -> tuple[str, bool]:
    """Read a file, refusing anything that escapes the standard's directory."""
    try:
        target = (root / relative).resolve()
        target.relative_to(root.resolve())
    except (ValueError, OSError):
        return f"error: path outside the standard's directory: {relative}", False
    if not target.is_file():
        return f"error: no such file: {relative}", False
    return target.read_text(encoding="utf-8", errors="replace"), True


def generate(task_prompt: str, condition: str, model: str, api_key: str,
             limiter: RateLimiter, timeout: int, max_tool_calls: int):
    """Run one generation to completion. Returns (record, [raw responses])."""
    spec = CONDITIONS[condition]
    docs = DOC_SETS[spec["docs"]] if spec["docs"] else None
    root = docs["root"] if docs else None

    parts = []
    if spec["preamble"]:
        parts.append(spec["preamble"])
    if docs is not None:
        parts.append(docs["grounding"].format(entry=docs["entry"]))
    parts.append(task_prompt)

    body = {"model": model, "input": "\n\n".join(parts)}
    if root is not None:
        body["tools"] = [READ_FILE_TOOL]

    raws, files_read, usages = [], [], []
    for step in range(max_tool_calls + 1):
        limiter.wait()
        print(f"    → call {step + 1}, waiting for the model…", end="", flush=True)
        started = time.monotonic()
        response = post(body, api_key, timeout)
        elapsed = time.monotonic() - started
        raws.append(response)
        usage = find_usage(response)
        usages.append(usage)

        calls = find_function_calls(response)
        summary = (f" {elapsed:.0f}s · {usage.get('total_tokens', 0):,} tokens · "
                   f"{len(calls)} file(s) requested" if calls
                   else f" {elapsed:.0f}s · {usage.get('total_tokens', 0):,} tokens · answered")
        print(summary, flush=True)

        if not calls or root is None:
            break

        results = []
        for call in calls:
            arguments = call.get("arguments") or {}
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            requested = str(arguments.get("path", ""))
            content, ok = read_scoped(root, requested)
            files_read.append({"path": requested, "found": ok, "chars": len(content)})
            print(f"      {'read ' if ok else 'MISS '} {requested} "
                  f"({len(content):,} chars)", flush=True)
            results.append({
                "type": "function_result",
                "name": call.get("name", "read_file"),
                "call_id": call.get("id"),
                "result": [{"type": "text", "text": content}],
            })

        interaction_id = find_interaction_id(response)
        if not interaction_id:
            print("    warning: no interaction id in response — stopping the tool loop",
                  flush=True)
            break
        body = {"model": model, "previous_interaction_id": interaction_id,
                "tools": [READ_FILE_TOOL], "input": results}
    else:
        print(f"    warning: hit --max-tool-calls ({max_tool_calls})", flush=True)

    text = find_text(raws[-1])
    record = {
        "model": model,
        "condition": condition,
        "condition_label": spec["label"],
        "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files_read": files_read,
        "tool_calls": len(files_read),
        "api_calls": len(raws),
        "usage_total": sum_usage(usages),
        "usage_per_call": usages,
        "output_chars": len(text),
    }
    return record, raws, extract_html(text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect benchmark generations from the Gemini API.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--tasks", default="", help="comma-separated task ids (default: all)")
    parser.add_argument("--conditions", default="A,B,D",
                        help="comma-separated: A,B,C,D (C needs benchmark/control-standard/)")
    parser.add_argument("--runs", type=int, default=3, help="repetitions per combination")
    parser.add_argument("--out", type=Path, default=BENCH / "runs")
    parser.add_argument("--prompts", type=Path, default=BENCH / "PROMPTS.md")
    parser.add_argument("--rpm", type=int, default=10, help="requests per minute ceiling")
    parser.add_argument("--daily-cap", type=int, default=0,
                        help="stop after N API calls (0 = no cap)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="seconds per API call; this model reasons before "
                             "answering, so a grounded generation is slow")
    parser.add_argument("--max-tool-calls", type=int, default=6)
    parser.add_argument("--resume", action="store_true", help="skip generations already on disk")
    parser.add_argument("--plan", action="store_true", help="list what would run, then exit")
    parser.add_argument("--probe", action="store_true",
                        help="one minimal call; dump the raw response to calibrate parsing")
    args = parser.parse_args()

    load_dotenv(BENCH / ".env")
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if args.probe:
        if not api_key:
            print("error: GEMINI_API_KEY not set", file=sys.stderr)
            return 2
        body = {"model": args.model, "input": "Reply with the single word: ok.",
                "tools": [READ_FILE_TOOL]}
        response = post(body, api_key, args.timeout)
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("\n--- what this script found in it ---", file=sys.stderr)
        print(f"interaction id : {find_interaction_id(response)}", file=sys.stderr)
        print(f"function calls : {len(find_function_calls(response))}", file=sys.stderr)
        print(f"usage          : {json.dumps(find_usage(response))}", file=sys.stderr)
        print(f"text           : {find_text(response)[:120]!r}", file=sys.stderr)
        return 0

    tasks = load_tasks(args.prompts)
    if not tasks:
        print(f"error: no tasks found in {args.prompts} "
              "(expected '## id' followed by a fenced block)", file=sys.stderr)
        return 2

    wanted = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(tasks)
    unknown = [t for t in wanted if t not in tasks]
    if unknown:
        print(f"error: unknown task(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"available: {', '.join(tasks)}", file=sys.stderr)
        return 2

    conditions = [c.strip().upper() for c in args.conditions.split(",") if c.strip()]
    for condition in conditions:
        if condition not in CONDITIONS:
            print(f"error: unknown condition {condition}", file=sys.stderr)
            return 2
        docs = CONDITIONS[condition]["docs"]
        if docs and not (DOC_SETS[docs]["root"] / DOC_SETS[docs]["entry"]).is_file():
            print(f"error: condition {condition} needs "
                  f"{DOC_SETS[docs]['root'] / DOC_SETS[docs]['entry']}, which is missing",
                  file=sys.stderr)
            return 2

    # Interleaved, as the registered protocol requires (METHODOLOGY.md §Size):
    # within a wave, each task cycles through every condition before any
    # condition repeats — a day's cap can never land on one condition's block,
    # so interface drift cannot load onto a condition. Runs are the outermost
    # layer: run 1 of the whole design completes before run 2 begins.
    jobs = [(task, condition, run)
            for run in range(1, args.runs + 1)
            for task in wanted for condition in conditions]

    html_dir = args.out / "html"
    raw_dir = args.out / "raw"
    log_path = args.out / "log.jsonl"

    def slug(task, condition, run):
        return f"{args.model}__{task}__{condition}__run{run}"

    if args.resume:
        jobs = [j for j in jobs if not (html_dir / f"{slug(*j)}.html").is_file()]

    print(f"{len(jobs)} generation(s) · model {args.model} · "
          f"conditions {','.join(conditions)} · {args.rpm} req/min ceiling")
    if args.plan:
        for task, condition, run in jobs:
            print(f"  {slug(task, condition, run)}")
        return 0
    if not jobs:
        print("nothing to do — everything is already on disk")
        return 0
    if not api_key:
        print("error: GEMINI_API_KEY not set (environment or benchmark/.env)", file=sys.stderr)
        return 2

    html_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    limiter = RateLimiter(args.rpm)
    api_calls = failures = 0

    for index, (task, condition, run) in enumerate(jobs, 1):
        name = slug(task, condition, run)
        print(f"[{index}/{len(jobs)}] {name}", flush=True)
        try:
            record, raws, html = generate(
                tasks[task], condition, args.model, api_key,
                limiter, args.timeout, args.max_tool_calls)
        except RuntimeError as error:
            failures += 1
            print(f"    FAILED: {error}", flush=True)
            with log_path.open("a", encoding="utf-8") as log:
                log.write(json.dumps({"id": name, "task": task, "condition": condition,
                                      "run": run, "error": str(error)}) + "\n")
            continue

        api_calls += record["api_calls"]
        record.update({"id": name, "task": task, "run": run})
        (raw_dir / f"{name}.json").write_text(
            json.dumps(raws, indent=2, ensure_ascii=False), encoding="utf-8")
        (html_dir / f"{name}.html").write_text(html, encoding="utf-8")
        with log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(record, ensure_ascii=False) + "\n")

        opened = ", ".join(f["path"] for f in record["files_read"]) or "—"
        used = record["usage_total"]
        print(f"    {record['api_calls']} call(s) · read: {opened}", flush=True)
        print(f"    tokens: {used.get('total_tokens', 0):,} total · "
              f"{used.get('total_input_tokens', 0):,} in · "
              f"{used.get('total_output_tokens', 0):,} out · "
              f"{used.get('total_thought_tokens', 0):,} thinking · "
              f"{used.get('total_cached_tokens', 0):,} cached", flush=True)

        if args.daily_cap and api_calls >= args.daily_cap:
            print(f"\nreached --daily-cap ({args.daily_cap} API calls). "
                  "Re-run with --resume to continue tomorrow.")
            break

    print(f"\ndone · {api_calls} API call(s) · {failures} failure(s)")
    print(f"html:  {html_dir}\nraw:   {raw_dir}\nlog:   {log_path}")
    if failures:
        print("Failed generations are logged with their error and skipped by --resume "
              "only once they succeed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

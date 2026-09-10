#!/usr/bin/env python3
"""
arm1ext.py — the pre-registered extension arm (METHODOLOGY.md, Arms table).

Arm 1 ran the factorial on one model family. The protocol registered the remedy
in advance: "the identical protocol runs on additional models if and when usable
API credits exist. Extension arms replicate; they do not alter the design."
This is that runner, pointed at an OpenAI-compatible endpoint (NVIDIA NIM).

What is deliberately NOT re-decided here: the conditions, their preambles, the
grounding sentences, the task prompts, the tool's shape and its scoping rule.
All of those are imported from the frozen `collect.py` — if a sentence differs
by a character, the arm stops being a replication. Only transport changes.

Three transport differences, each with a consequence for the record:

  1. The endpoint is stateless. Arm 1 chained calls with `previous_interaction_id`
     and the provider held the conversation; here every call resends the whole
     message list, core file included. Input tokens therefore inflate with each
     tool round-trip, and `total_cached_tokens` is whatever this provider reports
     (often nothing). The token co-primary is NOT paired with Arm 1's — that is
     an instrument difference, not a model effect, and DEVIATIONS.md says so
     before collection, not after.
  2. `max_tokens` must be sent. Arm 1 sent no output cap; several NIM models
     default to a cap far below a full HTML page, which would truncate
     generations and look like a model failure. Declared harness concession:
     --max-tokens, logged per generation, with finish_reason recorded so a
     truncation is visible in the data instead of inferred from it.
  3. Sampling controls are still not sent, matching Arm 1's request exactly.
     The provider's own defaults apply. The protocol promises a reproducible
     process, never reproducible outputs.

The documents come from a worktree pinned to the commit Arm 1 actually read
(`benchmark-protocol-v2.0`, A11Y.md = 36,367 chars, verified against the
collection log). Running against HEAD would move the model AND the standard at
the same time, and the arm would answer neither question.

    git worktree add ../a11y-arm1ext benchmark-protocol-v2.0
    python3 arm1ext.py --plan                     # what would run
    python3 arm1ext.py --probe                    # the gate: 1 task x 4 conditions
    python3 arm1ext.py                            # the full factorial
    python3 arm1ext.py --resume                   # skip what is already on disk

Set NVIDIA_API_KEY in the environment or in benchmark/.env (git-ignored).
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

REPO = Path(__file__).resolve().parent.parent
BENCH = REPO / "benchmark"
OUT_ROOT = BENCH / "runs" / "arm1ext"

sys.path.insert(0, str(BENCH))
# The frozen instrument. Everything that defines the experiment comes from here.
from collect import (CONDITIONS, DOC_SETS, READ_FILE_TOOL, RateLimiter,
                     extract_html, load_dotenv, load_tasks, read_scoped,
                     sum_usage)

# Two free routes to the same weights. The arm may need both: NVIDIA's tier is
# metered in total credits, OpenRouter's in requests per day, and neither alone
# covers 400 generations. Where cells come from a different route, the route is
# recorded per generation — the analysis can then show that the split changes
# nothing, or that it does.
ROUTES = {
    "nim": {
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "key_env": "NVIDIA_API_KEY",
        "model": "nvidia/nemotron-3-super-120b-a12b",
        "extra": {},
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        # Pinned to NVIDIA with fallbacks off: same weights, same server family
        # as the NIM cells. Without this the router could silently serve the
        # generation from a different host and the arm would mix instruments.
        "extra": {"provider": {"order": ["nvidia"], "allow_fallbacks": False}},
    },
}
DEFAULT_MODEL = ROUTES["nim"]["model"]
DEFAULT_DOCS = REPO.parent / "a11y-arm1ext"
DEFAULT_MAX_TOKENS = 16000
PROBE_TASK = "signup-form"

# The OpenAI wire format nests what the frozen tool declares flat. Same name,
# same description, same schema — rewrapped, not rewritten.
TOOL = {"type": "function", "function": {
    "name": READ_FILE_TOOL["name"],
    "description": READ_FILE_TOOL["description"],
    "parameters": READ_FILE_TOOL["parameters"],
}}


def model_slug(model: str) -> str:
    """One output directory per model, or a second model silently overwrites the first."""
    return re.sub(r"[^a-z0-9]+", "-", model.lower()).strip("-")


def doc_sets(docs_root: Path) -> dict:
    """Arm 1's document sets, re-rooted at the pinned worktree.

    `entry` and `grounding` are copied from the frozen collect.py untouched;
    only `root` moves. Both the standard and the placebo travel together, since
    the placebo is versioned in the same commit.
    """
    return {
        "standard": {**DOC_SETS["standard"], "root": docs_root / "docs" / "en"},
        "control": {**DOC_SETS["control"],
                    "root": docs_root / "benchmark" / "control-standard"},
    }


def normalise_usage(usage: dict) -> dict:
    """Map OpenAI-style usage onto Arm 1's field names, so one analysis reads both.

    The raw block is kept alongside: a provider that reports something Arm 1 had
    no name for must not lose it in translation.
    """
    prompt_details = usage.get("prompt_tokens_details") or {}
    completion_details = usage.get("completion_tokens_details") or {}
    return {
        "total_tokens": usage.get("total_tokens", 0),
        "total_input_tokens": usage.get("prompt_tokens", 0),
        "total_output_tokens": usage.get("completion_tokens", 0),
        "total_cached_tokens": prompt_details.get("cached_tokens", 0),
        "total_thought_tokens": completion_details.get("reasoning_tokens", 0),
    }


def post(body: dict, url: str, api_key: str, timeout: int, retries: int = 6) -> dict:
    payload = json.dumps(body).encode("utf-8")
    delay = 5.0
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            url, data=payload, method="POST",
            headers={"Content-Type": "application/json",
                     "Accept": "application/json",
                     "Authorization": f"Bearer {api_key}"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:400]
            # 404 is in this list deliberately. A wrong model id also returns
            # 404, and retrying that is pointless — but it fails loudly on the
            # first cell, whereas the endpoint's transient 404s (empty body,
            # model present in the catalog throughout) silently cost 27 cells
            # before this was noticed. Retrying is the cheaper mistake.
            # Everything except a genuine client error is treated as transient. Three
            # separate codes (404, 529, and the 5xx family) have already turned out
            # to be the endpoint saying "busy" rather than "wrong", and each one
            # that was missing from this list cost collected cells.
            transient = error.code in (404, 408, 425, 429, 529) or error.code >= 500
            if transient and attempt < retries:
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


def generate(task_prompt, condition, model, route, api_key, docs, limiter,
             timeout, max_tool_calls, max_tokens):
    """One generation, from scratch. Returns (record, raws, html)."""
    spec = CONDITIONS[condition]
    doc = docs[spec["docs"]] if spec["docs"] else None
    root = doc["root"] if doc else None

    parts = []
    if spec["preamble"]:
        parts.append(spec["preamble"])
    if doc is not None:
        parts.append(doc["grounding"].format(entry=doc["entry"]))
    parts.append(task_prompt)

    messages = [{"role": "user", "content": "\n\n".join(parts)}]
    raws, files_read, usages, elapsed_s, finish = [], [], [], [], None

    for step in range(max_tool_calls + 1):
        body = {"model": model, "messages": messages, "max_tokens": max_tokens,
                **route["extra"]}
        if root is not None:
            body["tools"] = [TOOL]

        limiter.wait()
        print(f"    → call {step + 1}, waiting for the model…", end="", flush=True)
        started = time.monotonic()
        response = post(body, route["url"], api_key, timeout)
        elapsed = time.monotonic() - started
        elapsed_s.append(round(elapsed, 1))
        raws.append(response)

        usage = normalise_usage(response.get("usage") or {})
        usages.append(usage)
        choice = (response.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        finish = choice.get("finish_reason")
        calls = message.get("tool_calls") or []

        print(f" {elapsed:.0f}s · {usage['total_tokens']:,} tokens · "
              f"{len(calls) if calls else 0} file(s) requested"
              if calls else f" {elapsed:.0f}s · {usage['total_tokens']:,} tokens · "
                            f"answered ({finish})", flush=True)

        if not calls or root is None:
            break

        # The assistant turn must go back verbatim, tool_calls included, or the
        # provider cannot match the results to the requests.
        messages.append({k: v for k, v in message.items() if v is not None
                         and k in ("role", "content", "tool_calls")})
        for call in calls:
            function = call.get("function") or {}
            arguments = function.get("arguments")
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            requested = str((arguments or {}).get("path", ""))
            content, ok = read_scoped(root, requested)
            files_read.append({"path": requested, "found": ok, "chars": len(content)})
            print(f"      {'read ' if ok else 'MISS '} {requested} "
                  f"({len(content):,} chars)", flush=True)
            messages.append({"role": "tool", "tool_call_id": call.get("id"),
                             "name": function.get("name", "read_file"),
                             "content": content})
    else:
        print(f"    warning: hit --max-tool-calls ({max_tool_calls})", flush=True)

    text = ((raws[-1].get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    if finish == "length":
        print("    WARNING: finish_reason=length — output was capped, not finished",
              flush=True)
    record = {
        "arm": "1-ext",
        "model": model,
        "endpoint": route["url"],
        "route": route["name"],
        "served_by": raws[-1].get("provider") if raws else None,
        "condition": condition,
        "condition_label": spec["label"],
        "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files_read": files_read,
        "tool_calls": len(files_read),
        "api_calls": len(raws),
        "finish_reason": finish,
        "max_tokens": max_tokens,
        "elapsed_s": elapsed_s,
        "elapsed_total_s": round(sum(elapsed_s), 1),
        "usage_total": sum_usage(usages),
        "usage_per_call": usages,
        "output_chars": len(text),
    }
    return record, raws, extract_html(text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect the pre-registered extension arm from an "
                    "OpenAI-compatible endpoint (default: NVIDIA NIM).")
    parser.add_argument("--via", choices=sorted(ROUTES), default="nim",
                        help="free route to use: nim (credit-metered) or "
                             "openrouter (request-metered, 50/day unfunded)")
    parser.add_argument("--model", default=None,
                        help="overrides the route's default model id")
    parser.add_argument("--daily-cap", type=int, default=0,
                        help="stop after N successful calls (0 = no cap)")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS,
                        help="worktree pinned to the commit Arm 1 read")
    parser.add_argument("--conditions", default="A,B,C,D")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--rpm", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--max-tool-calls", type=int, default=12)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--probe", action="store_true",
                        help=f"the gate: '{PROBE_TASK}' x 4 conditions x 1 run")
    parser.add_argument("--abort-if-slower-than", type=float, default=12.0,
                        help="abort the arm if it averages more than N minutes "
                             "per generation (default 12 → ~80h for 400 cells)")
    parser.add_argument("--abort-after-failures", type=int, default=15,
                        help="abort after N generations lost outright")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    route = {"name": args.via, **ROUTES[args.via]}
    args.model = args.model or route["model"]

    load_dotenv(BENCH / ".env")
    tasks = load_tasks(BENCH / "PROMPTS.md")
    if not tasks:
        print("error: no tasks parsed from PROMPTS.md", file=sys.stderr)
        return 1

    if args.probe:
        selected, conditions, runs = [PROBE_TASK], ["A", "B", "C", "D"], 1
    else:
        selected = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(tasks)
        conditions = [c.strip().upper() for c in args.conditions.split(",") if c.strip()]
        runs = args.runs

    unknown = [t for t in selected if t not in tasks]
    if unknown:
        print(f"error: unknown task(s): {', '.join(unknown)}\n"
              f"known: {', '.join(tasks)}", file=sys.stderr)
        return 1

    core = args.docs / "docs" / "en" / "A11Y.md"
    if not core.is_file():
        print(f"error: no standard at {core}\n"
              f"       git worktree add {args.docs} benchmark-protocol-v2.0",
              file=sys.stderr)
        return 1
    core_chars = len(core.read_text(encoding="utf-8"))

    # Run-major order, and the reason matters: on a metered free tier the
    # collection can stop at any point. Task-major order would spend the whole
    # budget on the first tasks and leave the last ones with zero cells — a
    # truncated collection would be missing entire tasks. Sweeping run by run
    # means an interruption costs repetitions, not tasks: 10x4x8 survives as a
    # factorial, 8x4x10 does not. Conditions stay interleaved either way, which
    # is what the protocol's wave rule asks for.
    cells = [(t, c, r) for r in range(1, runs + 1)
             for t in selected for c in conditions]
    print(f"route      {route['name']} · {route['url']}")
    print(f"model      {args.model}")
    print(f"docs       {args.docs}  (A11Y.md = {core_chars:,} chars)")
    print(f"cells      {len(cells)}  ({len(selected)} tasks x "
          f"{len(conditions)} conditions x {runs} runs)")
    if args.plan:
        for task, condition, run in cells:
            print(f"  {task:34} {condition}  run {run}")
        return 0

    api_key = os.environ.get(route["key_env"], "").strip()
    if not api_key:
        print(f"error: {route['key_env']} not set (environment or benchmark/.env)",
              file=sys.stderr)
        return 1

    out = OUT_ROOT / model_slug(args.model.removesuffix(":free"))
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "html").mkdir(parents=True, exist_ok=True)
    docs = doc_sets(args.docs)
    limiter = RateLimiter(args.rpm)
    log = out / "log.jsonl"
    failures = spent = done_now = throttle_hits = 0
    started_at = time.monotonic()

    for index, (task, condition, run) in enumerate(cells, 1):
        stem = f"{task}__{condition}__run{run}"
        html_path = out / "html" / f"{stem}.html"
        if args.resume and html_path.is_file():
            print(f"[{index}/{len(cells)}] {stem} — on disk, skipping", flush=True)
            continue
        print(f"[{index}/{len(cells)}] {stem}", flush=True)
        try:
            record, raws, html = generate(
                tasks[task], condition, args.model, route, api_key, docs,
                limiter, args.timeout, args.max_tool_calls, args.max_tokens)
        except RuntimeError as error:
            failures += 1
            if "429" in str(error) or "529" in str(error):
                throttle_hits += 1
            print(f"    FAILED: {error}", flush=True)
            # Circuit breaker. A model that cannot be reached at this study's
            # scale should cost minutes to discover, not hours: Kimi K3 produced
            # 7 generations in 294 minutes before anyone looked.
            if failures >= args.abort_after_failures:
                print(f"\nABORTED: {failures} failed generations — the endpoint is not "
                      f"serving this model reliably. --resume continues if it recovers.",
                      flush=True)
                return 2
            continue
        if done_now >= 3:
            pace = (time.monotonic() - started_at) / done_now / 60
            if pace > args.abort_if_slower_than:
                print(f"\nABORTED: {pace:.1f} min per generation, over the "
                      f"--abort-if-slower-than {args.abort_if_slower_than} limit. "
                      f"Projected {len(cells) * pace / 60:.0f} h for the arm.", flush=True)
                return 2
        record.update({"task": task, "run": run, "core_chars": core_chars,
                       "docs_commit": "benchmark-protocol-v2.0"})
        (out / "raw" / f"{stem}.json").write_text(
            json.dumps(raws, indent=2, ensure_ascii=False), encoding="utf-8")
        html_path.write_text(html, encoding="utf-8")
        with log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

        # Vital signs on disk after every generation. Without this, judging
        # whether a run is healthy meant parsing logs by hand — which is how an
        # unusable model was allowed to burn five hours before anyone noticed.
        done_now += 1
        pace = (time.monotonic() - started_at) / done_now / 60
        (out / "status.json").write_text(json.dumps({
            "model": args.model, "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "collected": index, "total": len(cells), "this_session": done_now,
            "minutes_per_generation": round(pace, 1),
            "throttle_events": throttle_hits, "failures": failures,
            "eta_hours": round((len(cells) - index) * pace / 60, 1),
        }, indent=2), encoding="utf-8")
        spent += record["api_calls"]
        if args.daily_cap and spent >= args.daily_cap:
            print(f"\ndaily cap reached ({spent} calls) — stopping; --resume continues")
            break

    print(f"\ndone · {len(cells) - failures}/{len(cells)} collected · output in {out}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

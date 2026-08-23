#!/usr/bin/env python3
"""
repair-artifacts.py — mechanical repair of the extract_html asset drop.

Discovery (2026-08-23, during blind adjudication — see DEVIATIONS.md): the
frozen collector's extract_html() keeps the largest fenced block of a raw
response and silently drops the ```css / ```js fences the model delivered
alongside. 32/400 Arm-1 artifacts reference a stylesheet that the model DID
write and the extractor discarded.

Rule, identical for every generation, blind to condition: for each Arm-1
artifact that links an external stylesheet and contains no <style>, re-read
its own raw response; every ```css fence is injected as <style> before
</head>, every ```js/javascript fence as <script> before </body>. Content is
only added, never removed; a comment marks the repair. Output goes to
runs/html-repaired/ — the as-collected originals are untouched, and every
outcome is reported under both versions (frozen instrument · repaired
sensitivity).

Prints aggregates only: no generation ids, no conditions.
"""
import json, re, sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "runs"
HTML, RAW, OUT = RUNS / "html", RUNS / "raw", RUNS / "html-repaired"
MARK = "<!-- repaired 2026-08-23: css/js fences restored from this generation's own raw response; see DEVIATIONS.md -->"

def strings(node):
    if isinstance(node, str): yield node
    elif isinstance(node, dict):
        for v in node.values(): yield from strings(v)
    elif isinstance(node, list):
        for v in node: yield from strings(v)

def fences(raw_text, tag):
    return re.findall(rf"```{tag}\s*\n(.*?)```", raw_text, re.S)

def repair(html, raw_text):
    css = "\n".join(fences(raw_text, "css"))
    js = "\n".join(fences(raw_text, "(?:js|javascript)"))
    if css:
        block = f"{MARK}\n<style>\n{css}\n</style>"
        html = html.replace("</head>", block + "\n</head>", 1) if "</head>" in html else block + "\n" + html
    if js and "<script" not in html:
        block = f"<script>\n{js}\n</script>"
        html = html.replace("</body>", block + "\n</body>", 1) if "</body>" in html else html + "\n" + block
    return html, bool(css)

def main():
    OUT.mkdir(exist_ok=True)
    total = repaired = no_css_found = 0
    for f in sorted(HTML.glob("*.html")):
        t = f.read_text(errors="replace")
        if not (re.search(r'rel="stylesheet"', t) and "<style" not in t):
            continue
        total += 1
        raw = RAW / f"{f.stem}.json"
        raw_text = "\n".join(strings(json.loads(raw.read_text()))) if raw.is_file() else ""
        fixed, had_css = repair(t, raw_text)
        if had_css:
            (OUT / f.name).write_text(fixed, encoding="utf-8")
            repaired += 1
        else:
            no_css_found += 1
    print(f"artefatos com o traço: {total} · reparados: {repaired} · sem css no raw: {no_css_found}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Study 2 — consistency classifier, v1.0 (pilot-calibrated).

Deterministic, DOM-only, stdlib-only. Spec: benchmark/study2/CLASSIFIER.md.
Input: a directory of screen HTML files (one run). Output: JSON — per-family
instances with structural signatures, distinct-variant counts, variant excess.
"""
import json, sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}

class Node:
    __slots__ = ("tag","attrs","children","parent","text")
    def __init__(self, tag, attrs, parent):
        self.tag, self.parent = tag, parent
        self.attrs = {k.lower(): (v or "") for k, v in attrs}
        self.children, self.text = [], ""
    def get(self, k, d=""): return self.attrs.get(k, d)
    def walk(self):
        yield self
        for c in self.children: yield from c.walk()
    def find_all(self, pred): return [n for n in self.walk() if pred(n)]
    def role(self): return self.get("role").strip().lower()

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None); self.cur = self.root
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur); self.cur.children.append(n)
        if tag not in VOID: self.cur = n
    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))
    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag: n = n.parent
        if n is not self.root: self.cur = n.parent
    def handle_data(self, data):
        self.cur.text += data

def parse(path: Path) -> Node:
    tb = TreeBuilder(); tb.feed(path.read_text(errors="replace")); return tb.root

# ---- signature helpers (categories recorded, never judged) ----

def naming_of(n: Node, doc: Node) -> str:
    if n.get("aria-labelledby"): return "aria-labelledby"
    if n.get("aria-label"): return "aria-label"
    return "none"

def field_naming(form: Node, doc: Node) -> str:
    """Dominant naming mechanism across the form's fields."""
    ids = {n.get("for") for n in doc.find_all(lambda x: x.tag == "label")}
    votes = []
    for f in form.find_all(lambda x: x.tag in ("input","select","textarea") and x.get("type") != "hidden"):
        if f.get("id") and f.get("id") in ids: votes.append("label-for")
        elif any(a.tag == "label" for a in _ancestors(f)): votes.append("label-wrap")
        elif f.get("aria-label") or f.get("aria-labelledby"): votes.append("aria")
        elif f.get("placeholder"): votes.append("placeholder-only")
        else: votes.append("none")
    if not votes: return "no-fields"
    return max(sorted(set(votes)), key=votes.count)

def _ancestors(n: Node):
    p = n.parent
    while p is not None: yield p; p = p.parent

# ---- family detectors: (anchor, signature) ----

def dialogs(doc):
    out = []
    for n in doc.find_all(lambda x: x.tag == "dialog" or x.role() in ("dialog","alertdialog")):
        container = "dialog-element" if n.tag == "dialog" else f"role-{n.role()}"
        out.append(("dialog", (container, "modal" if (n.tag=="dialog" or n.get("aria-modal")=="true") else "non-modal", naming_of(n, doc))))
    return out

def navs(doc):
    out = []
    cands = doc.find_all(lambda x: x.tag == "nav")
    if not cands:  # pilot lesson: div-built headers — outermost cluster of >=3 internal links
        raw = [n for n in doc.find_all(lambda x: x.tag in ("header","div","ul"))
               if len([a for a in n.find_all(lambda a: a.tag == "a")
                       if ".html" in a.get("href","") or a.get("href","").startswith("#") is False]) >= 3]
        cands = [n for n in raw if not any(p in raw for p in _ancestors(n))][:1]
    for n in cands:
        expandable = n.find_all(lambda x: x.get("aria-expanded") != "" or x.tag in ("details",))
        drop = ("details" if any(x.tag == "details" for x in expandable)
                else "aria-expanded" if expandable else "static-or-css")
        out.append(("nav", (f"{n.tag}-element", drop, naming_of(n, doc))))
    return out

def forms(doc):
    out = []
    cands = doc.find_all(lambda x: x.tag == "form")
    if not cands:
        cands = [d for d in doc.find_all(lambda x: x.tag in ("div","section"))
                 if len([i for i in d.children if i.tag in ("input","select","textarea","label")]) >= 3]
    for n in cands:
        live = n.find_all(lambda x: x.role() in ("alert","status") or x.get("aria-live"))
        invalid = n.find_all(lambda x: x.get("aria-invalid") != "")
        err = "live-region" if live else ("aria-invalid" if invalid else "none-visible")
        out.append(("form", (f"{n.tag}-element", field_naming(n, doc), err)))
    return out

def tables(doc):
    out = []
    for n in doc.find_all(lambda x: x.tag == "table" or x.role() in ("table","grid")):
        ths = n.find_all(lambda x: x.tag == "th")
        heads = ("th-scope" if any(t.get("scope") for t in ths) else "th") if ths else "none"
        sortm = ("aria-sort" if n.find_all(lambda x: x.get("aria-sort"))
                 else "button-in-header" if any(t.find_all(lambda b: b.tag == "button") for t in ths)
                 else "other")
        container = "table-element" if n.tag == "table" else f"role-{n.role()}"
        out.append(("table", (container, heads, sortm)))
    return out

def toasts(doc):
    out = []
    for n in doc.find_all(lambda x: x.role() in ("status","alert") or x.get("aria-live")):
        mech = f"role-{n.role()}" if n.role() else f"aria-live-{n.get('aria-live')}"
        out.append(("toast", (n.tag, mech)))
    return out

def cards(doc):
    out, seen = [], set()
    for n in doc.find_all(lambda x: x.tag in ("ul","ol","div","section")):
        kids = [c for c in n.children if c.tag in ("li","article","div","a")]
        if len(kids) < 3: continue
        shaped = [k for k in kids
                  if k.find_all(lambda i: i.tag == "img")
                  and (k.tag == "a" or k.find_all(lambda b: b.tag in ("button","a")))]
        if len(shaped) >= 3:
            k = shaped[0]
            act = "button" if k.find_all(lambda b: b.tag == "button") else ("link-wrapper" if k.tag == "a" else "link")
            sig = (k.tag, act)
            key = (id(n),)
            if key not in seen:
                seen.add(key); out.append(("card", sig))
    return out

import re
CONFIRM_RE = re.compile(r"(?:window\.|(?<![.\w]))confirm\s*\(")

def script_dialogs(screen: Path, doc: Node):
    """window.confirm() leaves no DOM footprint — static-scan inline and linked local JS."""
    src, base = "", screen.parent.resolve()
    for s in doc.find_all(lambda x: x.tag == "script"):
        if s.get("src"):
            js = (base / s.get("src")).resolve()
            if js.is_file() and base in js.parents: src += js.read_text(errors="replace")
        else:
            src += s.text
    if CONFIRM_RE.search(src):
        return [("dialog", ("window-confirm", "native-blocking", "n/a"))]
    return []

DETECTORS = (dialogs, navs, forms, tables, toasts, cards)
COUNTED = ("nav", "card", "form", "dialog", "toast", "table")

def classify(run_dir: Path) -> dict:
    fam: dict = {f: [] for f in COUNTED}
    script_refs: list = []   # native-confirm references; instances only if no DOM dialog in the run
    screens = sorted(run_dir.glob("*.html"))
    for screen in screens:
        doc = parse(screen)
        for det in DETECTORS:
            for family, sig in det(doc):
                fam[family].append({"screen": screen.name, "signature": list(sig)})
        for family, sig in script_dialogs(screen, doc):
            script_refs.append({"screen": screen.name, "signature": list(sig)})
    # Dominance rule (pilot-calibrated): a run with DOM dialogs keeps script-confirm
    # references as metadata; a run with none gets them as its dialog instances.
    if fam["dialog"]:
        confirm_meta = script_refs
    else:
        fam["dialog"] = script_refs; confirm_meta = []
    report = {"screens": len(screens), "families": {}, "variant_excess": 0,
              "script_confirm_refs": confirm_meta}
    for family, instances in fam.items():
        screens_with = {i["screen"] for i in instances}
        variants = {tuple(i["signature"]) for i in instances}
        entry = {"instances": instances, "screens_with_family": len(screens_with),
                 "variants": len(variants), "counted": len(screens_with) >= 2}
        if entry["counted"] and variants:
            report["variant_excess"] += len(variants) - 1
        report["families"][family] = entry
    return report

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        r = classify(Path(arg))
        print(json.dumps({arg: r}, indent=1, ensure_ascii=False))

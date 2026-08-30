#!/usr/bin/env python3
"""Round 2 — consistency classifier, v2 (calibrated against Round 1's corpus,
then adversarially verified and hardened before the freeze).

Deterministic, DOM+local-JS static analysis, stdlib-only, condition-blind:
the input is a directory of screen HTML files and nothing else — no run name,
no condition label, no network. Same input → same output.

v2 exists because calibrating v1 against Round 1's 30 real journeys exposed
four instrument defects (spec: CLASSIFIER-v2.md), and an independent
adversarial panel (three lenses — gaming, condition bias, regressions — with
skeptic verification per finding) then confirmed 16 further defects in the
first v2 draft. All are fixed or documented here; the spec carries the ledger.

Core design (the four calibration cases):
  A. tables   capability gate: sort signalling is compared only among tables
              that are sortable; claiming aria-sort can only ADD a table to
              the pool (anti-circularity).
  B. cards    two lanes: static DOM (css-cover accepted, per-shape grouping)
              + static JS-factory analysis (template/concat/builder styles,
              receiver-bound per factory), per-SCREEN dominance, signatures
              normalized to rendered shape (authoring style is metadata).
  C. validity broken composite structure (required parent/children) excludes
              the instance from variant comparison and is counted as an
              exclusion; interactive elements carry their real implicit
              roles; a composite with element content but no owned items is
              broken too.
  D. richness a sibling block beside the excess, never fused: the denominator
              (families counted), instances, coverage, provenance — with
              substance predicates so contentless stubs are reported apart.

Partitioned comparison (like is compared with like):
  nav    partitioned by slot: the primary nav (most links) across screens;
         secondary navs (footer, breadcrumb) by accessible name.
  toast  partitioned by announcement channel (polite vs assertive) — the
         status/alert pair a standard may prescribe is purpose, not
         dispersion; dispersion is measured within each channel.
  table  structure dimension over all valid tables; state dimension over
         capable tables only.

The Node/TreeBuilder core is from study2/classifier.py v1 (frozen, sha256
485d4064…) with two browser-faithfulness amendments measured to be
judgment-neutral on the whole Round-1 corpus (duplicate attributes keep the
FIRST value; <li>/<p>/<dt>/<dd>/<tr>/<td>/<th>/<option> auto-close their open
sibling, per HTML5 optional end tags). v1 itself stays untouched and runs as
a sensitivity analysis.

  --self-test  validates every calibrated behavior against Round 1's
               published screens (real fixtures) and the held-out synthetic
               fixtures in fixtures/consistency/ — including counterfactuals
               from the adversarial panel. A missing fixture directory is a
               FAILURE, never a skip.
"""
import json
import re
import sys
from pathlib import Path

from html.parser import HTMLParser

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}

# HTML5 optional end tags: opening tag T auto-closes an open element whose
# tag is in AUTOCLOSE[T]. Judgment-neutral on Round 1's corpus (measured);
# fixes sibling card items written without </li> being parsed as nested.
# The close walks UP through non-structural open elements (round-2 panel:
# an unclosed <p> at the end of a <li> must not defeat the li-sibling
# rule), stopping at any structural container so a nested list's items
# stay inside it.
AUTOCLOSE = {
    "li": {"li"}, "p": {"p"}, "dt": {"dt", "dd"}, "dd": {"dt", "dd"},
    "tr": {"tr"}, "td": {"td", "th"}, "th": {"td", "th"}, "option": {"option"},
}
STRUCTURAL = {"ul", "ol", "table", "thead", "tbody", "tfoot", "div", "section",
              "article", "nav", "main", "header", "footer", "form", "dialog",
              "select", "template", "body"}

class Node:
    __slots__ = ("tag","attrs","children","parent","text")
    def __init__(self, tag, attrs, parent):
        self.tag, self.parent = tag, parent
        self.attrs = {}
        for k, v in attrs:
            k = k.lower()
            if k not in self.attrs:      # browsers keep the FIRST duplicate
                self.attrs[k] = v or ""
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
        close = AUTOCLOSE.get(tag)
        if close:
            n = self.cur
            while n is not self.root and n.tag not in STRUCTURAL:
                if n.tag in close:
                    self.cur = n.parent
                    break
                n = n.parent
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

def _ancestors(n: Node):
    p = n.parent
    while p is not None: yield p; p = p.parent

def _desc(n: Node):
    for c in n.children:
        yield c; yield from _desc(c)

# ---- signature helpers (categories recorded, never judged) — from v1 ----

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

# =====================================================================
# Case C — structural validity gate (exclusion, never variant-counting)
# =====================================================================
# Scope is deliberately narrow (it does not duplicate axe): required
# children/parents of ARIA composite containers plus the native content
# model of ul/ol/dl/table — the minimum needed to decide "does this
# instance enter the comparison". Empty containers are vacuously valid
# (client-side population is not static evidence of a broken ladder), but a
# composite with element content and NO owned item anywhere is broken (an
# AT user gets an announced menu/tablist with zero entries). Hidden
# subtrees ARE checked: the calibration's target case is a closed dropdown
# (ul[role=menu][hidden]) whose broken ladder a rendered-DOM scan would
# only see with the menu open.

SKIP_TAGS = {"script", "template", "style"}

ALLOWED = {
    "menu":       {"menuitem", "menuitemcheckbox", "menuitemradio", "separator", "group"},
    "menubar":    {"menuitem", "menuitemcheckbox", "menuitemradio", "separator", "group"},
    "listbox":    {"option", "group"},
    "tablist":    {"tab"},
    "radiogroup": {"radio"},
    "tree":       {"treeitem", "group"},
    "table":      {"row", "rowgroup", "caption"},
    "grid":       {"row", "rowgroup", "caption"},
    "rowgroup":   {"row"},
    "row":        {"cell", "gridcell", "columnheader", "rowheader"},
    "list":       {"listitem"},
}

IMPLICIT = {
    "li": "listitem", "tr": "row", "td": "cell", "th": "columnheader",
    "option": "option", "ul": "list", "ol": "list",
    "thead": "rowgroup", "tbody": "rowgroup", "tfoot": "rowgroup",
    "caption": "caption",
    # Adversarial-panel amendment: interactive/semantic elements carry their
    # real implicit roles, so a div[role=menu] full of plain links/buttons is
    # a broken composite, exactly like ul[role=menu] > li. Only genuinely
    # role-less tags (div, span, p, legend, label, …) stay generic and
    # therefore transparent.
    "button": "button", "summary": "button", "select": "listbox",
    "textarea": "textbox", "table": "table", "nav": "navigation",
    "form": "form", "dialog": "dialog", "hr": "separator",
    "h1": "heading", "h2": "heading", "h3": "heading",
    "h4": "heading", "h5": "heading", "h6": "heading",
}

HTML_KIDS = {
    "ul": {"li"}, "ol": {"li"},
    "dl": {"dt", "dd", "div"},
    "table": {"caption", "colgroup", "thead", "tbody", "tfoot", "tr"},
    "thead": {"tr"}, "tbody": {"tr"}, "tfoot": {"tr"}, "tr": {"td", "th"},
}

def resolved_role(n: Node) -> str:
    r = n.role()
    if r: return r
    if n.tag == "a":
        return "link" if n.get("href") else "generic"
    if n.tag == "img":
        return "presentation" if n.get("alt", None) == "" else "img"
    if n.tag == "input":
        t = n.get("type", "text").lower()
        if t == "radio": return "radio"
        if t == "checkbox": return "checkbox"
        if t == "hidden": return "generic"
        return "textbox"
    return IMPLICIT.get(n.tag, "generic")

def check_composite(container: Node, expect_key: str, errors: list) -> int:
    """Direct element children must resolve into ALLOWED[expect_key].
    role=none/presentation delegates down (the correct APG ladder rung);
    GENERIC elements are transparent (ARIA 1.2 allows generics as
    intermediate structural descendants — a radiogroup's legend/hint/div
    wrappers are fine, while li inside role=menu errors because its
    implicit role is listitem, and a[href]/button error because their
    implicit roles are link/button — panel amendment); group is
    transparent for the same expectation; rowgroup/row descend into their
    own models. Returns the count of owned items found (for the
    content-but-no-items check). No children ⇒ vacuously valid."""
    allowed = ALLOWED[expect_key]
    found = 0
    for k in container.children:
        if k.tag in SKIP_TAGS: continue
        r = resolved_role(k)
        if r in ("presentation", "none", "generic"):
            found += check_composite(k, expect_key, errors)
        elif r in allowed:
            found += 1
            if r == "group":
                found += check_composite(k, expect_key, errors)
            elif r == "rowgroup":
                check_composite(k, "rowgroup", errors)
            elif r == "row":
                check_composite(k, "row", errors)
        else:
            errors.append(f"<{k.tag} role={k.role() or '(implicit)' + r}> child of "
                          f"<{container.tag}> expecting {sorted(allowed)}")
    return found

def html_check(container: Node, errors: list):
    ok = HTML_KIDS[container.tag]
    for k in container.children:
        if k.tag in SKIP_TAGS: continue
        if k.tag not in ok:
            errors.append(f"<{k.tag}> child of <{container.tag}> (HTML content model)")

def instance_errors(anchor: Node) -> list:
    """Local validity of one family instance: walk its subtree, check every
    composite-role container and every native list/table container found.
    Documented scope limit: a native container carrying a NON-composite role
    (e.g. ul[role=navigation]) is checked by neither path — mirroring axe,
    whose list rule also stands down when the role is overridden."""
    errors = []
    for n in anchor.walk():
        r = n.role()
        if r in ALLOWED:
            elems = [k for k in n.children if k.tag not in SKIP_TAGS]
            found = check_composite(n, r, errors)
            if elems and not found and not errors:
                errors.append(f"<{n.tag} role={r}> has element content but no "
                              f"owned {sorted(ALLOWED[r])} anywhere (announced "
                              f"composite with zero items)")
        elif not r and n.tag in HTML_KIDS:
            html_check(n, errors)
    return errors

# =====================================================================
# Case A — tables: capability gate before state comparison
# =====================================================================
# Structure dimension: (container, heads) over ALL valid tables.
# State dimension: sort signalling compared ONLY among tables that are
# sortable. Capability is judged primarily WITHOUT aria-sort: interactive
# descendant in a column-header cell, or handler/focus affordance anywhere
# in the header cell's subtree. The claim term (aria-sort present) can only
# ADD a table to the compared pool, never remove one — a run cannot exit
# the comparison by deleting its own honest markup (anti-circularity).
# Signal scope is the whole header-cell subtree: aria-sort placed on the
# button inside the th (invalid placement, real signal) still counts, and
# presence is what counts, not value (aria-sort="none" means "sortable,
# not sorted now"; a bare valueless aria-sort attribute also counts).

def _has_aria_sort(n: Node) -> bool:
    return "aria-sort" in n.attrs

def _first_row(table: Node):
    for n in table.walk():
        if n is not table and n.tag == "tr":
            return n
    return None

def col_header_cells(table: Node):
    """Column header cells: th (thead ancestor, scope=col ASCII
    case-insensitive, or sitting in the table's FIRST row without
    scope=row — bare-th markup heads columns by HTML convention, so the
    gate does not depend on the thead/scope idiom), and any element with
    role=columnheader — so ARIA grids (div[role=grid]) get the same gate
    and the same anti-circularity term as native tables (both panel
    rounds)."""
    out = []
    first = _first_row(table)
    for th in table.find_all(lambda x: x.tag == "th"):
        scope = th.get("scope").strip().lower()
        if (any(a.tag == "thead" for a in _ancestors(th))
                or scope == "col"
                or (first is not None and th.parent is first and scope != "row")):
            out.append(th)
    for ch in table.find_all(lambda x: x.tag != "th" and x.role() == "columnheader"):
        out.append(ch)
    return out

def table_sortable(table: Node):
    """(capable, evidence). Known blind spot, documented in the spec:
    JS-attached listeners with no DOM footprint (addEventListener on plain
    th) are invisible — those tables stay out of the state pool unless
    they claim aria-sort."""
    ths = col_header_cells(table)
    for th in ths:
        if [n for n in th.walk() if n is not th and
                (n.tag == "button" or n.role() == "button"
                 or (n.tag == "a" and n.get("href")))]:
            return True, "interactive-descendant-in-header"
        for n in th.walk():   # handler/focus affordance anywhere in the cell
            # round-2 amendment: a form control in the header (select-all
            # checkbox, filter input) is a selection/filter affordance,
            # not a sort affordance — its handlers do not open the gate
            if resolved_role(n) in ("checkbox", "radio", "textbox", "listbox"):
                continue
            if n.get("onclick") or n.get("onkeydown") or n.get("onkeypress"):
                return True, "handler-in-header"
            if n.role() == "button":
                return True, "role-button-in-header"
            ti = n.get("tabindex")
            if ti and not ti.strip().startswith("-"):
                return True, "focusable-header"
    if any(_has_aria_sort(th) for th in ths):
        return True, "aria-sort-claim-only"
    return False, "static"

def table_sort_signal(table: Node) -> str:
    for th in col_header_cells(table):
        if any(_has_aria_sort(n) for n in th.walk()):
            return "aria-sort"
    return "none"

def tables(doc: Node):
    out = []
    for n in doc.find_all(lambda x: x.tag == "table" or x.role() in ("table","grid")):
        ths = n.find_all(lambda x: x.tag == "th" or x.role() == "columnheader")
        heads = ("th-scope" if any(t.get("scope") for t in ths) else "th") if ths else "none"
        container = "table-element" if n.tag == "table" else f"role-{n.role()}"
        capable, evidence = table_sortable(n)
        out.append(("table", (container, heads), n,
                    {"sort_capable": capable, "sort_evidence": evidence,
                     "sort_signal": table_sort_signal(n)}))
    return out

# =====================================================================
# Families carried from v1, with panel-driven partitioning
# =====================================================================

def dialogs(doc: Node):
    out = []
    for n in doc.find_all(lambda x: x.tag == "dialog" or x.role() in ("dialog","alertdialog")):
        container = "dialog-element" if n.tag == "dialog" else f"role-{n.role()}"
        out.append(("dialog", (container,
                    "modal" if (n.tag=="dialog" or n.get("aria-modal")=="true") else "non-modal",
                    naming_of(n, doc)), n, None))
    return out

def navs(doc: Node):
    """Panel amendments, both rounds (like-with-like): navs are PARTITIONED
    before variant comparison, and identity comes from the nav's own
    accessible name — a NAMED nav is never promoted to some other slot, so
    a footer nav on a footer-only screen, or a breadcrumb on a screen whose
    main nav is client-rendered, stays in its own pool instead of being
    charged against the main nav (two confirmed round-2 findings). Pools:
    `label:<normalized accessible name>` for named navs; the link-richest
    UNNAMED nav of a screen is `unnamed-main` (DOM order breaks ties);
    remaining unnamed navs share `unnamed-other`. The dropdown axis records
    the SET of mechanisms present."""
    cands = doc.find_all(lambda x: x.tag == "nav")
    if not cands:  # pilot lesson (v1): div-built headers — outermost cluster of >=3 internal links
        raw = [n for n in doc.find_all(lambda x: x.tag in ("header","div","ul"))
               if len([a for a in n.find_all(lambda a: a.tag == "a")
                       if ".html" in a.get("href","") or a.get("href","").startswith("#") is False]) >= 3]
        cands = [n for n in raw if not any(p in raw for p in _ancestors(n))][:1]
    if not cands: return []
    def links(n): return len([a for a in n.find_all(lambda a: a.tag == "a") if a.get("href")])
    unnamed = [n for n in cands
               if not (n.get("aria-label") or n.get("aria-labelledby")).strip()]
    unnamed_main = max(unnamed, key=links) if unnamed else None
    out = []
    for n in cands:
        mechs = sorted({("details" if x.tag == "details" else "aria-expanded")
                        for x in n.find_all(lambda x: x.get("aria-expanded") != "" or x.tag == "details")})
        drop = "+".join(mechs) if mechs else "static-or-css"
        label = (n.get("aria-label") or n.get("aria-labelledby")).strip().lower()
        if label:
            slot = f"label:{label}"
        elif n is unnamed_main:
            slot = "unnamed-main"
        else:
            slot = "unnamed-other"
        out.append(("nav", (f"{n.tag}-element", drop, naming_of(n, doc)), n,
                    {"partition": slot}))
    return out

def forms(doc: Node):
    out = []
    cands = doc.find_all(lambda x: x.tag == "form")
    if not cands:
        cands = [d for d in doc.find_all(lambda x: x.tag in ("div","section"))
                 if len([i for i in d.children if i.tag in ("input","select","textarea","label")]) >= 3]
    for n in cands:
        live = n.find_all(lambda x: x.role() in ("alert","status") or x.get("aria-live"))
        invalid = n.find_all(lambda x: x.get("aria-invalid") != "")
        err = "live-region" if live else ("aria-invalid" if invalid else "none-visible")
        out.append(("form", (f"{n.tag}-element", field_naming(n, doc), err), n, None))
    return out

def toasts(doc: Node):
    """Panel amendment: announcement severity is PURPOSE, not convention —
    a run using role=status for success and role=alert for errors (the
    pair a standard may prescribe) is not dispersing. Instances are
    partitioned by channel (polite vs assertive) and dispersion is
    measured within each channel (role=status vs aria-live=polite IS
    dispersion — two conventions for the same channel).
    Second-round amendment: a live-region WRAPPER around a live-region
    toast is one widget, not two conventions (the belt-and-suspenders
    idiom a real D run was charged +1 for) — when a matched element
    contains a matched descendant, only the innermost is an instance;
    aria-live values compare case-insensitively (HTML enumerated
    attributes)."""
    matched = doc.find_all(lambda x: x.role() in ("status","alert") or x.get("aria-live"))
    matched_ids = {id(n) for n in matched}
    out = []
    for n in matched:
        if any(id(d) in matched_ids for d in _desc(n)):
            continue   # wrapper around an inner live region: one widget
        live = n.get("aria-live").strip().lower()
        mech = f"role-{n.role()}" if n.role() else f"aria-live-{live}"
        channel = ("polite" if n.role() == "status" or live == "polite"
                   else "assertive" if n.role() == "alert" or live == "assertive"
                   else "other")
        out.append(("toast", (n.tag, mech), n, {"partition": channel}))
    return out

# =====================================================================
# Case B — cards: DOM lane + receiver-bound JS-factory lane
# =====================================================================

COVER_RE = re.compile(r'(?:^|[\s_-])(cover|thumb|capa)\b|__cover|cover__|book-cover', re.I)

def imageish(k: Node):
    """Ranked (round-2 amendment): a real cover (img/picture/css-cover)
    outranks an svg, and a decorative aria-hidden svg never defines the
    card's image class — a wishlist-star badge must not split an
    otherwise uniform grid into two conventions."""
    best = None
    RANK = {"img": 0, "picture": 1, "css-cover": 2, "svg": 3}
    def consider(label):
        nonlocal best
        if best is None or RANK[label] < RANK[best]: best = label
    for d in _desc(k):
        if d.tag == "img": consider("img")
        elif d.tag == "picture": consider("picture")
        elif d.tag == "svg" and d.get("aria-hidden").strip().lower() != "true":
            consider("svg")
        elif d.tag in ("div","span","i") and COVER_RE.search(d.get("class","")):
            consider("css-cover")
    return best

def actionish(k: Node):
    if any(d.tag == "button" for d in _desc(k)): return "button"
    if k.tag == "a" and k.get("href"): return "link-wrapper"
    if any(d.tag == "a" and d.get("href") for d in _desc(k)): return "link"
    return None

def card_shape(k: Node):
    img, act = imageish(k), actionish(k)
    return (img, act) if img and act else None

def item_shape(k: Node) -> str:
    inner = next((d for d in _desc(k) if d.tag == "article"), None)
    return f"{k.tag}>article" if (inner and k.tag != "article") else k.tag

def _has_substance(k: Node) -> bool:
    """A card item with no text anywhere and no real image source is a stub."""
    if any((d.text or "").strip() for d in [k] + list(_desc(k))): return True
    return any(d.tag == "img" and d.get("src") for d in _desc(k))

def cards_dom(doc: Node):
    """DOM lane: sibling repetition (>=3) of card-shaped items grouped by
    (tag, first class token) and THEN by full shape — two conventions
    sharing one grid are two variants (panel amendment). Innermost
    qualifying container wins; inert <template> subtrees are skipped."""
    out = []
    def visit(n):
        if n.tag == "template": return False
        below = any([visit(c) for c in n.children])
        if n.tag not in ("ul","ol","div","section") or below: return below
        groups = {}
        for c in n.children:
            if c.tag in ("li","article","div","a"):
                key = (c.tag, (c.get("class","").split() or [""])[0])
                groups.setdefault(key, []).append(c)
        hit = False
        for grp in groups.values():
            by_shape = {}
            for k in grp:
                s = card_shape(k)
                if s: by_shape.setdefault((item_shape(k),) + s, []).append(k)
            for shape, ks in by_shape.items():
                if len(ks) >= 3:
                    substantive = any(_has_substance(k) for k in ks)
                    out.append(((f"{n.tag}-grid",) + shape, n, substantive))
                    hit = True
        return hit or below
    visit(doc)
    return out

# --- JS lane (precedent: v1's script_dialogs static scan) ---

LIT_RE = re.compile(r"`((?:\\.|[^`\\])*)`|'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\"", re.S)
MK_RE = re.compile(r"\b[A-Za-z_$][\w$.]*\(\s*['\"](article|li|img|svg|button|a|div|span|h[1-6]|p)['\"]\s*[,)]")
ITER_RE = re.compile(r"\.forEach\(|\.map\(|\bfor\s*\(|\bwhile\s*\(")
INTERP_COVER_RE = re.compile(r"\$\{[^}]*(cover|svg|img|thumb|capa)[^}]*\}", re.I)
MAX_FACTORY_UNIT = 6000   # a >6KB "unit" is an IIFE aggregating a whole file, not a card factory

REGEX_PRECEDERS = set("=(,:[!&|?{;+-*%<>^~")

def _js_scan(src: str, keep_plain_strings: bool, collect):
    """One shared JS lexer (panel round 2): walks src tracking template
    literals WITH their ${…} interpolations (interpolation code is real
    code — strings/templates/regexes inside it are handled recursively via
    a mode stack), plain strings, comments, and regex literals (a '/'
    whose previous expression cannot continue starts a regex — the
    heuristic that fixed the real .replace(/"/g,…) misread). `collect`
    receives every literal TEXT body (plain strings and template text
    chunks, in source order, inner templates included) so fragment
    parsing sees nested card templates. Returns the blanked text:
    literal bodies/comments/regex bodies spaced out, interpolation code
    kept; with keep_plain_strings, '…'/"…" bodies survive for the
    binding scans. Documented limit: '}' after a block is read as a
    possible division, never a regex start."""
    out = list(src)
    i, n = 0, len(src)
    prev = ""
    stack = []          # "tpl" entries: inside a template literal's text
    depth = []          # brace depth per open interpolation
    KEYWORDS = ("return", "typeof", "case", "in", "of", "new", "delete", "void", "do", "else")
    def regex_position():
        if not prev: return True
        if prev in REGEX_PRECEDERS: return True
        tail = src[max(0, i-8):i].rstrip()
        return any(tail.endswith(k) and (len(tail) == len(k) or not tail[-len(k)-1].isalnum())
                   for k in KEYWORDS)
    while i < n:
        c = src[i]
        in_tpl = bool(stack) and stack[-1] == "tpl"
        if in_tpl:
            if c == "\\":
                out[i] = " "
                if i + 1 < n: out[i+1] = " "
                i += 2; continue
            if c == "`":
                stack.pop(); prev = "`"; i += 1; continue
            if c == "$" and i + 1 < n and src[i+1] == "{":
                stack.append("interp"); depth.append(0)
                collect("${")           # interpolation text stays visible to
                prev = ""; i += 2; continue   # the fragment parser (${coverMarkup})
            collect(c)
            out[i] = " "
            i += 1; continue
        # code mode (top level or inside an interpolation)
        if c == "`":
            stack.append("tpl"); i += 1; continue
        if stack and stack[-1] == "interp":
            if c == "{": depth[-1] += 1
            elif c == "}":
                if depth[-1] == 0:
                    stack.pop(); depth.pop()
                    collect("}")
                    i += 1; continue
                depth[-1] -= 1
        if c in "'\"":
            q = c; j = i + 1
            body = []
            while j < n:
                if src[j] == "\\": body.append(src[j:j+2]); j += 2; continue
                if src[j] == q: break
                body.append(src[j]); j += 1
            collect("".join(body))
            if not keep_plain_strings:
                for k in range(i + 1, min(j, n)): out[k] = " "
            prev = q; i = j + 1; continue
        if c == "/" and i + 1 < n and src[i+1] == "/":
            j = src.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j): out[k] = " "
            i = j; continue
        if c == "/" and i + 1 < n and src[i+1] == "*":
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, min(j, n)): out[k] = " "
            i = j; continue
        if c == "/" and regex_position():
            j, in_class = i + 1, False
            while j < n:
                d = src[j]
                if d == "\\": j += 2; continue
                if d == "\n": break
                if in_class:
                    if d == "]": in_class = False
                elif d == "[": in_class = True
                elif d == "/": break
                j += 1
            if j < n and src[j] == "/":
                for k in range(i + 1, j): out[k] = " "
                while j + 1 < n and src[j+1].isalpha(): j += 1
                prev = "/"; i = j + 1; continue
            prev = c; i += 1; continue
        if "interp" in stack: collect(c)   # interpolation code is template text too
        if not c.isspace(): prev = c
        i += 1
    return "".join(out)

def blank_code(src: str, keep_plain_strings: bool = False) -> str:
    return _js_scan(src, keep_plain_strings, lambda _: None)

def literals(src: str) -> str:
    """All literal text bodies in source order — plain strings and template
    TEXT chunks, nested templates included (the second panel round's
    nested-map catalog idiom lives one interpolation deep)."""
    parts = []
    _js_scan(src, True, parts.append)
    return "".join(parts)

def units_of(src: str, blanked: str):
    """(start, body) for each brace-matched function body, smallest first —
    smallest-first means a card factory inside a big IIFE is still found.
    Matching runs on the BLANKED text (braces in strings/comments ignored);
    the returned body is the ORIGINAL text at the same offsets."""
    out = []
    for m in re.finditer(r"\bfunction\b[^{]*|=>\s*", blanked):
        i = blanked.find("{", m.end()-1)
        if i < 0 or i - m.end() > 3: continue
        depth, j = 0, i
        while j < len(blanked):
            if blanked[j] == "{": depth += 1
            elif blanked[j] == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        out.append((m.start(), src[i:j+1]))
    return sorted(out, key=lambda t: len(t[1]))

def _frag_imageish(n: Node):
    img = imageish(n)
    if img: return img
    for d in [n] + list(_desc(n)):
        # interpolated image markup normalizes to the plain image class —
        # authoring style must not create a variant (panel amendment)
        if INTERP_COVER_RE.search(d.text or ""): return "img"
    return None

def fragment_card(frag_src: str):
    """Parse the unit's concatenated string literals as HTML; look for a
    card-shaped element. Fragment forests (wrapper element created via
    createElement outside the template) yield shape=None — indeterminate,
    excluded from variant identity but still an instance."""
    if "<" not in frag_src: return None
    tb = TreeBuilder(); tb.feed(frag_src)
    for n in tb.root.walk():
        if n.tag in ("li","article","div","a","section"):
            img, act = _frag_imageish(n), actionish(n)
            if img and act: return (item_shape(n), img, act)
    img, act = _frag_imageish(tb.root), actionish(tb.root)
    if img and act and any(c.tag for c in tb.root.children):
        return (None, img, act)
    return None

def _name_before(src: str, start: int):
    """Factory/helper name from the text before a function unit: covers
    `function NAME(`, `ui.NAME = function`, `NAME: function`, and
    arrow assignments `const NAME = (a) =>` / `NAME = a =>` (panel
    amendment — arrow factories were nameless before)."""
    m2 = re.match(r"\s*function\s+([\w$]+)", src[start:start+60])
    if m2: return m2.group(1)
    head = src[max(0, start-100):start].rstrip()
    m = re.search(r"[.\s]([\w$]+)\s*[:=]$", head)
    if m: return m.group(1)
    m = re.search(r"(?:const|let|var)?\s*[\w$.]*?([\w$]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[\w$]+)\s*$", head)
    if m: return m.group(1)
    return None

def factories(src: str, blanked_full: str):
    """[(name_or_None, unit_src, sig, start, style)] — card factories in one
    script. sig = (shape_or_None, image, action); authoring style
    (template vs builder) is metadata, never variant identity (panel
    amendment)."""
    found = []
    for start, unit in units_of(src, blanked_full):
        if len(unit) > MAX_FACTORY_UNIT: continue
        sig, style = fragment_card(literals(unit)), "template"
        if not sig:
            tags = set(MK_RE.findall(unit))   # builder style: el('article', …)
            if "img" in tags and ({"button","a"} & tags) and ({"article","li","div"} & tags):
                root = "article" if "article" in tags else ("li" if "li" in tags else "div")
                sig, style = (root, "img", "button" if "button" in tags else "link"), "builder"
        if sig:
            found.append((_name_before(src, start), unit, sig, start, style))
    seen, out = set(), []
    for name, unit, sig, start, style in found:
        if sig not in seen: seen.add(sig); out.append((name, unit, sig, start, style))
    return out

def bindings(src_binding: str) -> dict:
    """var -> host key, over the binding-blanked text (template literals and
    comments removed; plain quotes kept — the ids live inside them).
    Host keys: ('id', x) from getElementById/'#x' selectors, ('attr', name)
    from querySelector('[data-…]') attribute selectors, ('class', name)
    from querySelector('.class') (round-2 amendment)."""
    b = {}
    for m in re.finditer(r"\b([\w$]+)\s*=\s*[^;\n]{0,80}?(?:getElementById\(\s*['\"]|querySelector\(\s*['\"]#|qs\(\s*['\"]#)([\w-]+)", src_binding):
        b[m.group(1)] = ("id", m.group(2))
    for m in re.finditer(r"\b([\w$]+)\s*=\s*[^;\n]{0,80}?querySelector\(\s*['\"]\[([\w-]+)[^\]]*\]", src_binding):
        b[m.group(1)] = ("attr", m.group(2))
    for m in re.finditer(r"\b([\w$]+)\s*=\s*[^;\n]{0,80}?querySelector\(\s*['\"]\.([\w-]+)", src_binding):
        b[m.group(1)] = ("class", m.group(2))
    return b

# A render statement referencing the factory: NAME( call, bare NAME as a
# callback (.map(NAME), .forEach(NAME)), or ns.NAME — round-2 amendment.
def _use_re(name):
    return r"(?:[\w$]+\.)?" + re.escape(name) + r"\b"

def _chained_keys(src_b, name):
    """Receivers used inline with no variable: document.getElementById('x')
    .innerHTML = …NAME…  (round-2 amendment)."""
    keys = set()
    pat = (r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)\s*\.\s*"
           r"(?:innerHTML\s*[+]?=|appendChild\(|append\(|prepend\(|insertAdjacentHTML\()"
           r"[^;]{0,300}?" + _use_re(name))
    for m in re.finditer(pat, src_b, re.S):
        keys.add(("id", m.group(1)))
    pat2 = (r"querySelector\(\s*['\"]#([\w-]+)['\"]\s*\)\s*\.\s*"
            r"(?:innerHTML\s*[+]?=|appendChild\(|append\(|prepend\(|insertAdjacentHTML\()"
            r"[^;]{0,300}?" + _use_re(name))
    for m in re.finditer(pat2, src_b, re.S):
        keys.add(("id", m.group(1)))
    return keys

def render_helpers(src: str, factory_name: str) -> set:
    """Depth-2 indirection for ONE factory: names of functions that take a
    container parameter and append/insert that factory's output
    (ui.renderGrid(container, …)). The factory-use gate accepts calls AND
    bare callback references (.map(bookCard)) — round-2 amendment."""
    helpers = set()
    blanked_full = blank_code(src)
    for start, unit in units_of(src, blanked_full):
        if len(unit) > MAX_FACTORY_UNIT: continue
        unit_b = blank_code(unit, keep_plain_strings=True)
        if not re.search(_use_re(factory_name), unit_b): continue
        if re.search(r"[\w$]+\.(?:appendChild|append|prepend|insertAdjacentHTML)\(|[\w$]+\.innerHTML\s*[+]?=", unit_b):
            name = _name_before(src, start)
            if name and name != factory_name: helpers.add(name)
    return helpers

def receiver_keys_for(all_scripts, name, unit, start, own_idx, name_owners):
    """Host keys of elements that receive THIS factory's output (both panel
    rounds: resolution is per factory, and name-based resolution in a
    FOREIGN script is only trusted when that script does not define its own
    factory of the same name — a dead same-name factory elsewhere must not
    borrow this one's render sites). Paths in: named factory at a render
    site (incl. bare-callback .map(name) and ns.name forms); chained
    no-variable receivers; anonymous factory with a receiver inside/just
    before its unit; depth-2 helper called with a bound container."""
    keys = set()
    helper_names = set()
    if name:
        for idx, (_, src, _sb) in enumerate(all_scripts):
            if idx != own_idx and idx in name_owners.get(name, set()): continue
            helper_names |= render_helpers(src, name)
    for idx, (_, src, src_b) in enumerate(all_scripts):
        binds = bindings(src_b)
        if name and (idx == own_idx or idx not in name_owners.get(name, set())):
            for m in re.finditer(r"([\w$]+)\.(?:appendChild|append|prepend)\(\s*(?:\.\.\.)?[^)]{0,200}?" + _use_re(name), src_b):
                if m.group(1) in binds: keys.add(binds[m.group(1)])
            for m in re.finditer(r"([\w$]+)\.(?:innerHTML\s*[+]?=|insertAdjacentHTML\()[^;]{0,300}?" + _use_re(name), src_b, re.S):
                if m.group(1) in binds: keys.add(binds[m.group(1)])
            keys |= _chained_keys(src_b, name)
            for helper in helper_names:
                for m in re.finditer(r"(?:[\w$]+\.)?" + re.escape(helper) + r"\s*\(\s*([\w$]+)", src_b):
                    if m.group(1) in binds: keys.add(binds[m.group(1)])
        if unit in src:
            u_start = src.find(unit)
            unit_b = blank_code(unit, keep_plain_strings=True)
            zones = [unit_b, src_b[max(0, u_start-250):u_start]]
            for zone in zones:
                for m in re.finditer(r"([\w$]+)\.(?:appendChild|append|prepend|insertAdjacentHTML)\(|([\w$]+)\.innerHTML\s*[+]?=", zone):
                    r = m.group(1) or m.group(2)
                    if r in binds: keys.add(binds[r])
    return keys

def script_sources(screen: Path, doc: Node):
    out, base = [], screen.parent.resolve()
    for s in doc.find_all(lambda x: x.tag == "script"):
        if s.get("src"):
            js = (base / s.get("src")).resolve()
            if js.is_file() and base in js.parents:
                src = js.read_text(errors="replace")
                out.append((js.name, src, blank_code(src, keep_plain_strings=True)))
        elif s.text.strip():
            out.append(("<inline>", s.text, blank_code(s.text, keep_plain_strings=True)))
    return out

def _host_matches(el: Node, keys: set) -> bool:
    for kind, val in keys:
        if kind == "id" and el.get("id") == val: return True
        if kind == "attr" and val in el.attrs: return True
        if kind == "class" and val in el.get("class", "").split(): return True
    return False

PLACEHOLDER_RE = re.compile(r"loading|empty|placeholder|skeleton|spinner|carregando", re.I)

def _near_empty(el: Node) -> bool:
    """A grid host waiting for JS: no element children, or only noscript /
    loading-placeholder children (round-2 amendment — a skeleton item or a
    noscript fallback must not disqualify the real host)."""
    real = [c for c in el.children if c.tag
            and c.tag != "noscript"
            and not PLACEHOLDER_RE.search(c.get("class", ""))
            and not PLACEHOLDER_RE.search(c.get("id", ""))]
    return len(real) <= 1

def cards_js(screen: Path, doc: Node):
    """JS lane: a factory's signature counts for this screen iff the DOM
    holds a bound, (near-)empty grid container that receives THAT factory's
    output. The container axis comes from the receiving host element, so
    DOM-lane and JS-lane signatures share one vocabulary. Top-level render
    code with no enclosing function is scanned as one pseudo-unit."""
    scripts = script_sources(screen, doc)
    facs = []
    name_owners = {}
    for idx, (_, src, _sb) in enumerate(scripts):
        blanked = blank_code(src)
        if not ITER_RE.search(blanked): continue   # repetition proxy
        found = factories(src, blanked)
        if not found and len(src) <= MAX_FACTORY_UNIT:
            # round-2 amendment: catalog rendered by top-level code
            # (grid.innerHTML = `…${books.map(b => `…`)}…`) has no
            # function unit — treat the whole script as one
            sig = fragment_card(literals(src))
            if sig:
                found = [(None, src, sig, 0, "template")]
        for f in found:
            facs.append((idx,) + f)
            if f[0]:
                name_owners.setdefault(f[0], set()).add(idx)
    if not facs: return []
    out = []
    for own_idx, name, unit, sig, start, style in facs:
        keys = receiver_keys_for(scripts, name, unit, start, own_idx, name_owners)
        if not keys: continue
        hosts = [el for el in doc.walk()
                 if el.tag in ("ul","ol","div","section")
                 and _host_matches(el, keys)
                 and el.role() != "listbox"
                 and _near_empty(el)]
        if not hosts: continue
        shape, img, act = sig
        container = f"{hosts[0].tag}-grid"
        out.append((container, shape, img, act, style))
    return out[:2]   # distinct bound factories, capped per screen

# =====================================================================
# Script-confirm scan — verbatim judgment from v1
# =====================================================================

CONFIRM_RE = re.compile(r"(?:window\.|(?<![.\w]))confirm\s*\(")

def script_dialogs(screen: Path, doc: Node):
    src = "".join(s for _, s, _b in script_sources(screen, doc))
    if CONFIRM_RE.search(src):
        return [("dialog", ("window-confirm", "native-blocking", "n/a"))]
    return []

# =====================================================================
# Substance predicates (panel amendment: contentless stubs are reported
# apart and do not feed the richness denominator)
# =====================================================================

def substantive(family: str, anchor: Node) -> bool:
    if anchor is None: return True          # script-lane instances render content
    if family == "table":
        # headers are substance: a thead-only table whose tbody is populated
        # client-side is legitimate static-analysis credit (Round-1 corpus:
        # the antigravity D orders tables); only the fully empty shell stubs
        return any(n.tag in ("td", "th", "caption")
                   or resolved_role(n) in ("cell", "gridcell", "columnheader")
                   for n in anchor.walk() if n is not anchor)
    if family == "dialog":
        return (any(k.tag not in SKIP_TAGS for k in anchor.children)
                or bool(anchor.text.strip())
                or bool(anchor.get("aria-label") or anchor.get("aria-labelledby")))
    if family == "form":
        # a button-only form is real (the canonical <form method="dialog">
        # confirm form in a real D run; cart-line remove forms) — only the
        # truly empty <form></form> shell stubs (round-2 amendment)
        return any((n.tag in ("input", "select", "textarea") and n.get("type") != "hidden")
                   or n.tag == "button"
                   or (n.tag == "input" and n.get("type") in ("submit", "button", "image"))
                   for n in anchor.walk())
    if family == "nav":
        return any(n.tag == "a" and n.get("href") for n in anchor.walk())
    return True   # toast: an empty live-region placeholder is the correct idiom

# =====================================================================
# Case D — richness census helper
# =====================================================================

NONSEM_RE = re.compile(r"modal|overlay|toast|snackbar|janela|aviso|notificacao", re.I)

def nonsemantic_census(doc: Node, family_anchors: set):
    """div/section whose class or id lexically claims modal/overlay/toast but
    that is not (inside/containing) any detected family instance. Lexical, so
    it is metadata with lower evidential weight — never a metric."""
    hits = 0
    for n in doc.find_all(lambda x: x.tag in ("div","section")):
        if not (NONSEM_RE.search(n.get("class","")) or NONSEM_RE.search(n.get("id",""))):
            continue
        lineage = {id(n)} | {id(a) for a in _ancestors(n)} | {id(d) for d in _desc(n)}
        if lineage & family_anchors: continue
        hits += 1
    return hits

# =====================================================================
# classify — the run-level report
# =====================================================================

DETECTORS = (dialogs, navs, forms, tables, toasts)
COUNTED = ("nav", "card", "form", "dialog", "toast", "table")

def _family_excess(family: str, entry: dict) -> int:
    """Variant excess of one counted family. Partitioned families (nav by
    slot, toast by channel) sum per-partition excess; tables sum a
    structure dimension and a capability-gated state dimension; the rest
    compare one global pool. Shape-indeterminate card signatures stay out
    of variant identity."""
    instances = entry["instances"]
    if family == "table":
        structure = {tuple(i["signature"]) for i in instances}
        signals = {i["sort_signal"] for i in instances if i.get("sort_capable")}
        excess = 0
        if structure: excess += len(structure) - 1
        if signals: excess += len(signals) - 1
        return excess
    pools = {}
    for i in instances:
        if i.get("shape_indeterminate"): continue
        pools.setdefault(i.get("partition", ""), set()).add(tuple(i["signature"]))
    return sum(len(v) - 1 for v in pools.values() if v)

def classify(run_dir: Path) -> dict:
    if not run_dir.is_dir():
        return {"status": "missing", "screens": 0}
    screens = sorted(run_dir.glob("*.html"))
    if not screens:
        return {"status": "no-data", "screens": 0}

    fam = {f: [] for f in COUNTED}
    excluded = {f: [] for f in COUNTED}
    stubs = {f: [] for f in COUNTED}
    script_refs, cards_js_meta = [], []
    nonsem = 0
    per_screen_records = []

    for screen in screens:
        doc = parse(screen)
        anchors = set()
        for det in DETECTORS:
            for family, sig, anchor, extra in det(doc):
                errs = instance_errors(anchor) if anchor is not None else []
                rec = {"screen": screen.name, "signature": list(sig), "source": "dom"}
                if extra: rec.update(extra)
                if errs:
                    rec["invalid_reason"] = errs[:3]
                    excluded[family].append(rec)
                elif not substantive(family, anchor):
                    stubs[family].append(rec)
                else:
                    fam[family].append(rec)
                if anchor is not None: anchors.add(id(anchor))
        dom_cards = cards_dom(doc)
        for sig, anchor, has_substance in dom_cards:
            errs = instance_errors(anchor)
            rec = {"screen": screen.name, "signature": list(sig), "source": "dom"}
            if errs:
                rec["invalid_reason"] = errs[:3]
                excluded["card"].append(rec)
            elif not has_substance:
                stubs["card"].append(rec)
            else:
                fam["card"].append(rec)
            anchors.add(id(anchor))
        # Per-SCREEN dominance (panel amendment): a screen whose DOM already
        # shows a card grid keeps its JS hits as metadata (no double count);
        # screens without one adopt their bound factories as instances.
        js_here = [{"screen": screen.name,
                    "signature": [c, s if s else "unknown", i, a],
                    "source": "script", "style": st,
                    "shape_indeterminate": s is None}
                   for (c, s, i, a, st) in cards_js(screen, doc)]
        dom_here = any(r["screen"] == screen.name for r in fam["card"])
        if dom_here:
            cards_js_meta.extend(js_here)
        else:
            fam["card"].extend(js_here)
        for family, sig in script_dialogs(screen, doc):
            script_refs.append({"screen": screen.name, "signature": list(sig), "source": "script"})
        per_screen_records.append((screen, doc, anchors))

    # Dialog dominance stays run-level, mirroring frozen v1's pilot-calibrated
    # window.confirm rule (a run with DOM dialogs keeps confirm refs as
    # metadata; a run with none adopts them).
    if fam["dialog"]:
        confirm_meta = script_refs
    else:
        fam["dialog"] = script_refs; confirm_meta = []

    for screen, doc, anchors in per_screen_records:
        nonsem += nonsemantic_census(doc, anchors)

    report = {"status": "ok", "screens": len(screens), "families": {},
              "variant_excess": 0, "per_family_excess": {},
              "script_confirm_refs": confirm_meta, "cards_js_refs": cards_js_meta}

    for family, instances in fam.items():
        screens_with = {i["screen"] for i in instances}
        entry = {"instances": instances,
                 "excluded": len(excluded[family]),
                 "excluded_detail": excluded[family],
                 "stubs": len(stubs[family]),
                 "stub_detail": stubs[family],
                 "screens_with_family": len(screens_with),
                 "counted": len(screens_with) >= 2}
        entry["variants"] = len({tuple(i["signature"]) for i in instances
                                 if not i.get("shape_indeterminate")})
        if family == "table":
            capable = [i for i in instances if i.get("sort_capable")]
            entry["state_variants_among_capable"] = len({i["sort_signal"] for i in capable})
            entry["capable_instances"] = len(capable)
        # round-2 amendment: a counted family whose every instance is
        # shape-indeterminate has no measurable variant pool — reporting 0
        # would present an unmeasured cell as a measured zero. It is
        # flagged, excluded from the excess sum AND from families_counted.
        entry["unmeasurable"] = bool(
            entry["counted"] and instances
            and all(i.get("shape_indeterminate") for i in instances))
        if entry["unmeasurable"]:
            report["per_family_excess"][family] = None
        else:
            excess = _family_excess(family, entry) if entry["counted"] else 0
            report["per_family_excess"][family] = excess
            report["variant_excess"] += excess
        report["families"][family] = entry

    # richness: sibling block, computed from the SAME substantive instances
    per_family = {}
    per_screen_fams = {s.name: set() for s in screens}
    for family, instances in fam.items():
        with_screens = {i["screen"] for i in instances}
        sources = {"dom": sum(1 for i in instances if i["source"] == "dom"),
                   "script": sum(1 for i in instances if i["source"] == "script")}
        per_family[family] = {"instances": len(instances),
                              "screens_with": len(with_screens),
                              "stubs": len(stubs[family]),
                              "sources": sources}
        for s in with_screens: per_screen_fams[s].add(family)
    n_screens = len(screens)
    coverage_cells = sum(v["screens_with"] for v in per_family.values())
    report["richness"] = {
        "families_instantiated": sum(1 for v in per_family.values() if v["instances"]),
        "families_counted": sum(1 for f in COUNTED
                                if report["families"][f]["counted"]
                                and not report["families"][f]["unmeasurable"]),
        "families_unmeasurable": sum(1 for f in COUNTED if report["families"][f]["unmeasurable"]),
        "total_instances": sum(v["instances"] for v in per_family.values()),
        "coverage_cells": coverage_cells,
        "coverage_ratio": round(coverage_cells / (len(COUNTED) * n_screens), 4),
        "screens_multi_family": sum(1 for fams in per_screen_fams.values() if len(fams) >= 2),
        "stub_instances": sum(len(v) for v in stubs.values()),
        "per_family": per_family,
        "nonsemantic_candidates": nonsem,
    }
    return report

# =====================================================================
# self-test
# =====================================================================

def self_test():
    """Validate every calibrated behavior: real fixtures (Round 1's published
    screens) + held-out synthetic counterfactuals (fixtures/consistency/),
    including the adversarial panel's counter-fixtures. Missing fixtures are
    a FAILURE, not a skip."""
    here = Path(__file__).resolve().parent
    screens_root = here.parent / "runs" / "study2" / "screens"
    fixtures = here / "fixtures" / "consistency"
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  {name}: got {got!r} want {want!r} {'ok' if good else 'SELF-TEST FAILURE'}")

    if not screens_root.is_dir():
        sys.exit(f"self-test needs Round 1 screens at {screens_root} (published on Zenodo)")
    if not fixtures.is_dir():
        sys.exit(f"self-test needs the held-out fixtures at {fixtures}")

    runs = {p.name: classify(p) for p in sorted(screens_root.iterdir()) if p.is_dir()}
    live = {k: v for k, v in runs.items() if v["status"] == "ok"}

    print("case D0 — empty runs are no-data, never 'perfectly consistent':")
    empty = [k for k, v in runs.items() if v["status"] == "no-data"]
    check("codex dirs report no-data", all(k.startswith("codex") for k in empty) and len(empty) == 15, True)
    check("live runs", len(live), 30)
    check("a nonexistent path is 'missing', not 'no-data'",
          classify(screens_root / "does-not-exist")["status"], "missing")

    print("case A — capability gate: no run is punished for honest aria-sort:")
    state_excess = {k: max(0, v["families"]["table"]["state_variants_among_capable"] - 1)
                    for k, v in live.items() if v["families"]["table"]["counted"]}
    check("table state dimension adds zero across all 30 real runs",
          sum(state_excess.values()), 0)
    d_runs = [k for k in live if "__D__" in k]
    check("all 10 D runs carry a counted table family",
          sum(1 for k in d_runs if live[k]["families"]["table"]["counted"]), 10)

    print("case C — validity gate: exactly one run's main-nav ladder is excluded:")
    excl = {k: sum(v["families"][f]["excluded"] for f in COUNTED) for k, v in live.items()}
    check("antigravity D run3 exclusions", excl.get("antigravity__journey__D__run3"), 7)
    check("exclusions anywhere else", sum(n for k, n in excl.items() if k != "antigravity__journey__D__run3"), 0)
    r3 = live["antigravity__journey__D__run3"]["families"]["nav"]
    check("run3 nav valid instances", len(r3["instances"]), 8)
    check("run3 nav excess after exclusion",
          live["antigravity__journey__D__run3"]["per_family_excess"]["nav"], 0)

    print("case B — cards: the JS-rendered catalogs are visible:")
    with_cards = [k for k, v in live.items() if v["families"]["card"]["instances"]]
    check("runs with a detected card grid", len(with_cards), 30)
    dom_lane = [k for k, v in live.items()
                if any(i["source"] == "dom" for i in v["families"]["card"]["instances"])]
    check("DOM-lane runs (v1 saw 3 of these)", len(dom_lane), 5)

    print("case D — richness travels beside excess:")
    ric_ok = all(set(v["richness"]) >= {"families_counted", "stub_instances", "per_family"}
                 for v in live.values())
    check("richness block complete on every live run", ric_ok, True)
    poor = live["antigravity__journey__A__run1"]["richness"]
    rich = live["claude-code__journey__D__run3"]["richness"]
    check("calibration pair (families, instances, cells): antigravity A run1",
          (poor["families_instantiated"], poor["total_instances"], poor["coverage_cells"]),
          (4, 17, 17))
    check("calibration pair (families, instances, cells): claude-code D run3",
          (rich["families_instantiated"], rich["total_instances"], rich["coverage_cells"]),
          (6, 32, 23))
    check("nonsemantic census sees antigravity A run1's fake modals/toasts",
          poor["nonsemantic_candidates"] > 0, True)

    print("condition-blindness — same content, different directory name, same output:")
    import shutil, tempfile
    src = fixtures / "blind-probe"
    check("blind-probe fixture present (mandatory)", src.is_dir(), True)
    if src.is_dir():
        with tempfile.TemporaryDirectory() as td:
            a, d = Path(td) / "agent__journey__A__run1", Path(td) / "agent__journey__D__run1"
            shutil.copytree(src, a); shutil.copytree(src, d)
            check("classify(A-named) == classify(D-named)", classify(a) == classify(d), True)

    print("synthetic counterfactuals (held out — behaviors the real corpus lacks):")
    def fx(name): return classify(fixtures / name)
    r = fx("table-signals-diverge")
    check("two capable tables, divergent signals -> state excess 1",
          r["per_family_excess"]["table"], 1)
    check("  (and their structure agrees)", r["families"]["table"]["variants"], 1)
    r = fx("table-static-vs-sorted")
    check("static table vs honest sortable -> no state excess",
          r["per_family_excess"]["table"], 0)
    r = fx("table-span-onclick")
    check("onclick on a span inside th -> capable (divergent signals score)",
          r["per_family_excess"]["table"], 1)
    r = fx("table-role-grid")
    check("ARIA grid with role=columnheader -> capable, signals compared",
          r["per_family_excess"]["table"], 1)
    r = fx("ladder-broken")
    check("broken menu ladder -> excluded, not a variant", r["families"]["nav"]["excluded"], 2)
    check("  remaining nav excess", r["per_family_excess"]["nav"], 0)
    r = fx("ladder-delegated")
    check("role=none delegation ladder -> valid", r["families"]["nav"]["excluded"], 0)
    r = fx("ladder-div-links")
    check("div[role=menu] of plain links/buttons -> excluded (implicit roles)",
          r["families"]["nav"]["excluded"], 2)
    r = fx("composite-no-items")
    check("announced composite with content but zero items -> excluded",
          r["families"]["nav"]["excluded"], 2)
    r = fx("cards-css-cover")
    check("static grid with CSS covers -> detected", r["families"]["card"]["instances"] != [], True)
    r = fx("cards-js-template")
    check("empty grid + JS factory -> detected via script lane",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-authoring-styles")
    check("same rendered card, template vs builder authoring -> 0 excess",
          r["per_family_excess"]["card"], 0)
    r = fx("cards-mixed-grid")
    check("two conventions inside ONE grid -> both seen, excess 1",
          r["per_family_excess"]["card"], 1)
    r = fx("cards-dead-factory")
    check("unbound second factory does not score",
          r["families"]["card"]["variants"], 1)
    r = fx("cards-minified")
    check("minified one-line JS still binds the factory",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-arrow-factory")
    check("arrow-assigned factory with render site after it -> detected",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-brace-in-string")
    check("'}' inside a string/comment does not truncate the factory",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-template-inert")
    check("<template> sample card is not a DOM instance; JS lane scores",
          (any(i["source"] == "dom" for i in r["families"]["card"]["instances"]),
           any(i["source"] == "script" for i in r["families"]["card"]["instances"])),
          (False, True))
    r = fx("cards-screen-dominance")
    check("per-screen dominance: DOM screen + JS screens all count",
          r["families"]["card"]["screens_with_family"], 3)
    r = fx("toast-dual-severity")
    check("uniform status+alert pair (prescribed purpose split) -> 0 excess",
          r["per_family_excess"]["toast"], 0)
    r = fx("toast-channel-diverge")
    check("two conventions in ONE channel -> excess 1",
          r["per_family_excess"]["toast"], 1)
    r = fx("nav-secondary-static")
    check("dropdown main + static footer navs (both uniform) -> 0 excess",
          r["per_family_excess"]["nav"], 0)
    r = fx("nav-primary-diverge")
    check("primary nav changing mechanism across screens -> excess 1",
          r["per_family_excess"]["nav"], 1)
    r = fx("richness-stubs")
    check("contentless stubs feed stub_instances, not the denominator",
          (r["richness"]["families_counted"], r["richness"]["stub_instances"] > 0),
          (1, True))
    r = fx("poor-consistent")
    check("2-family run: excess 0 with denominator visible",
          (r["variant_excess"], r["richness"]["families_counted"]), (0, 2))

    print("second panel round — the amended behaviors, held out:")
    r = fx("toast-nested-region")
    check("live-region wrapper + inner toast = ONE widget -> 0 excess",
          (r["per_family_excess"]["toast"], len(r["families"]["toast"]["instances"])), (0, 2))
    r = fx("toast-case-mech")
    check("aria-live value compares case-insensitively -> 1 variant",
          r["families"]["toast"]["variants"], 1)
    r = fx("cards-nested-template")
    check("nested template + concise-arrow .map (the modern idiom) -> detected",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-chained-receiver")
    check("chained no-variable receiver -> detected",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-class-receiver")
    check("querySelector('.class') receiver -> detected",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-placeholder-host")
    check("skeleton/noscript children do not disqualify the host",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("cards-name-collision")
    check("dead same-name factory in a second script does not score",
          r["families"]["card"]["variants"], 1)
    r = fx("cards-svg-badge")
    check("decorative svg badge does not split a uniform grid",
          (r["families"]["card"]["variants"], r["per_family_excess"]["card"]), (1, 0))
    r = fx("cards-all-indeterminate")
    check("all-indeterminate card pool -> unmeasurable, out of the denominator",
          (r["per_family_excess"]["card"], r["families"]["card"]["unmeasurable"],
           r["richness"]["families_unmeasurable"]), (None, True, 1))
    r = fx("cards-regex-literal")
    check("regex literal with a quote above the factory -> still detected",
          any(i["source"] == "script" for i in r["families"]["card"]["instances"]), True)
    r = fx("table-checkbox-th")
    check("select-all checkbox in th does not open the sort gate",
          r["per_family_excess"]["table"], 0)
    r = fx("table-bare-th")
    check("bare first-row th heads columns (idiom-independent gate) -> +1",
          r["per_family_excess"]["table"], 1)
    r = fx("form-button-only")
    check("button-only dialog-method form is substantive",
          (r["families"]["form"]["stubs"], r["families"]["form"]["counted"]), (0, True))
    r = fx("nav-footer-only-screen")
    check("footer-only screen promotes nothing -> 0 excess",
          r["per_family_excess"]["nav"], 0)
    r = fx("single-screen-family")
    check("one-screen family is not counted (real falsifiable denominator check)",
          (r["families"]["dialog"]["counted"], r["richness"]["families_counted"]), (False, 1))

    print("self-test:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    args = [a for a in sys.argv[1:] if a != "--self-test"]
    if not args:
        print(__doc__); sys.exit(0)
    for arg in args:
        r = classify(Path(arg))
        print(json.dumps({arg: r}, indent=1, ensure_ascii=False))

<!-- Thank you! Two minutes here saves a review round trip. -->

## What this changes

<!-- One paragraph: what the change obliges, permits or corrects — and why now. -->

## Evidence

<!-- The claim behind the change. An SC number, a primary source, a field report,
     a reproducible defect. "It seems better" is not evidence in a normative repo. -->

## Checklist

- [ ] **Both languages:** `docs/en/` and `docs/pt-BR/` updated together (or the PR says which half needs the maintainer)
- [ ] **Linter passes:** `python3 tools/lint-standard.py .` runs clean locally
- [ ] **Traceability:** every new requirement cites a WCAG SC by number **or** is labeled a House Rule†
- [ ] **Placement:** anything the AI must *do* lives in the AI Behavior Contract with an **event** trigger (no phase triggers); guides carry depth, never the sole copy of an obligation
- [ ] **Discoverability:** a new or renamed guide has its row in the §2.1 loading map, in both languages
- [ ] **CHANGELOG** entry added
- [ ] **Tools:** any new check in `tools/` has a fixture proving it catches the defect it claims to catch

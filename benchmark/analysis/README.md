# analysis/

The pre-registered analysis, as executable scripts.

- **`robustness.py`** — the registered robustness track: per-condition distributions, bootstrap CIs on median differences (seed 20260818), Cliff's delta, token co-primary, and the morning report generator. Stdlib only.
- **`confirmatory.py`** — the registered primary model, operationalized: NB2 GLM, `violations ~ condition + task` (fixed effects), IRRs with 95% CIs, Holm-corrected pre-registered contrasts, plus a cluster-robust-by-task sensitivity fit. See DEVIATIONS.md for why fixed effects stand in for the registered random intercepts. Requires `requirements.txt` (`python3 -m venv venv && venv/bin/pip install -r requirements.txt`).

Inputs are the collection log (`runs/log.jsonl`) and the verifier output (`runs/verify/*.jsonl`); outputs land next to the inputs. Anyone can rerun both against the published dataset without re-collecting anything.

"""CI quality gate: fail the pipeline if the measured AI quality drops below agreed thresholds.

  python eval/report.py && python eval/run_private_eval.py report && python eval/quality_gate.py

The two report commands re-score the stored model outputs with the *current* scoring and pipeline code
(no model needed), so a change to retrieval, prompts parsing, refusal detection or metrics that would
silently worsen the results makes this script exit non-zero and blocks deployment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

# Thresholds sit a little below the measured values (eval 1: 97.4% / 100%; eval 2: 100% / 100%), so normal
# re-runs pass and a real regression fails. Change them only together with a note in docs/REPORT.md.
GATES = [
    # (evaluation, system key, metric, operator, threshold, label)
    ("eval1", "rag_hybrid__llama3.2-3b", "overall_accuracy", ">=", 0.95, "Vaultwise overall accuracy (policies)"),
    ("eval1", "rag_hybrid__llama3.2-3b", "refusal_accuracy_unanswerable", ">=", 0.95, "Vaultwise correct refusals (policies)"),
    ("eval1", "rag_hybrid__llama3.2-3b", "unsupported_number_rate", "<=", 0.08, "Vaultwise answers with unsupported numbers"),
    ("eval1", "rag_hybrid__llama3.2-3b", "citation_precision", ">=", 0.85, "Vaultwise citation precision"),
    ("eval2", "vaultwise", "overall", ">=", 0.95, "Vaultwise overall accuracy (private documents)"),
    ("eval2", "vaultwise", "refusal", ">=", 0.80, "Vaultwise correct refusals (private documents)"),
    ("eval2", "vaultwise", "held_out", ">=", 0.90, "Vaultwise accuracy on the held-out document"),
]
MARGINS = [  # Vaultwise must stay well ahead of the no-retrieval baseline
    ("eval1", "rag_hybrid__llama3.2-3b", "llm_only__llama3.2-3b", "overall_accuracy", 0.50),
    ("eval2", "vaultwise", "no_search", "overall", 0.50),
]


def load() -> dict:
    e1 = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))["runs"]
    e2 = json.loads((RESULTS / "private_summary.json").read_text(encoding="utf-8"))["systems"]
    def metrics(s: dict) -> dict:  # {"mean": ...} entries become plain numbers; nested tables are skipped
        return {m: (x["mean"] if isinstance(x, dict) else x) for m, x in s.items()
                if isinstance(x, (int, float)) or (isinstance(x, dict) and "mean" in x)}
    return {"eval1": {k: metrics(s) for k, s in e1.items()},
            "eval2": {k: s for k, s in e2.items() if isinstance(s, dict)}}


def main() -> None:
    data, failed = load(), 0
    print(f"{'check':58s} {'value':>8s}   {'gate':>9s}   result")
    for ev, system, metric, op, thr, label in GATES:
        v = data[ev][system][metric]
        ok = v >= thr if op == ">=" else v <= thr
        failed += not ok
        print(f"{label:58s} {v:8.3f}   {op} {thr:5.2f}   {'PASS' if ok else 'FAIL'}")
    for ev, system, base, metric, margin in MARGINS:
        d = data[ev][system][metric] - data[ev][base][metric]
        ok = d >= margin
        failed += not ok
        print(f"{'Margin over ' + base + ' (' + ev + ')':58s} {d:8.3f}   >= {margin:5.2f}   {'PASS' if ok else 'FAIL'}")
    if failed:
        sys.exit(f"\nQuality gate FAILED: {failed} check(s) below threshold")
    print("\nQuality gate passed")


if __name__ == "__main__":
    main()

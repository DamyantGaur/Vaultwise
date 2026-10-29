"""Validate the automatic scorer against human judgement.

  python eval/audit.py sample [--n 20]   # writes results/audit_sample.csv (n answers per system, seeded)
  # fill the `human_correct` column with 1/0 (correct, complete and faithful to the policy?)
  python eval/audit.py score             # agreement, Cohen's kappa, confusion matrix -> results/audit.json
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SAMPLE = RESULTS / "audit_sample.csv"


def sample(n: int, seed: int = 7) -> None:
    rows = list(csv.DictReader(open(RESULTS / "per_question.csv", encoding="utf-8")))
    rng = random.Random(seed)
    out = []
    for system in sorted({(r["system"], r["model"]) for r in rows}):
        pool = [r for r in rows if (r["system"], r["model"]) == system]
        out += rng.sample(pool, min(n, len(pool)))
    questions = {json.loads(l)["id"]: json.loads(l) for l in
                 (ROOT / "data/eval/questions.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    with open(SAMPLE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["system", "model", "id", "category", "question", "reference_answer", "answer", "auto_correct",
                    "human_correct", "note"])
        for r in out:
            w.writerow([r["system"], r["model"], r["id"], r["category"], r["question"],
                        questions[r["id"]]["reference_answer"], r["answer"], r["correct"], "", ""])
    print(f"Wrote {len(out)} rows to {SAMPLE}; fill in human_correct (1/0) and run `audit.py score`.")


def cohen_kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def score() -> None:
    rows = [r for r in csv.DictReader(open(SAMPLE, encoding="utf-8")) if r["human_correct"].strip() in ("0", "1")]
    auto = [int(r["auto_correct"]) for r in rows]
    human = [int(r["human_correct"]) for r in rows]
    tp = sum(a and h for a, h in zip(auto, human))
    tn = sum((not a) and (not h) for a, h in zip(auto, human))
    fp = sum(a and not h for a, h in zip(auto, human))
    fn = sum((not a) and h for a, h in zip(auto, human))
    res = {"n": len(rows), "agreement": (tp + tn) / len(rows), "cohen_kappa": cohen_kappa(auto, human),
           "scorer_false_positive": fp, "scorer_false_negative": fn, "both_correct": tp, "both_wrong": tn,
           "by_system": {}, "disagreements": [
               {k: r[k] for k in ("system", "model", "id", "auto_correct", "human_correct", "note")}
               for r in rows if r["auto_correct"] != r["human_correct"]]}
    for s in sorted({(r["system"], r["model"]) for r in rows}):
        sr = [r for r in rows if (r["system"], r["model"]) == s]
        res["by_system"][f"{s[0]}__{s[1]}"] = {
            "n": len(sr), "auto_acc": sum(int(r["auto_correct"]) for r in sr) / len(sr),
            "human_acc": sum(int(r["human_correct"]) for r in sr) / len(sr)}
    (RESULTS / "audit.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "disagreements"}, indent=2))
    for d in res["disagreements"]:
        print(d)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["sample", "score"])
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    sample(args.n) if args.action == "sample" else score()

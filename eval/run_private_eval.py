"""Evaluation 2: private company documents (the way Vaultwise is used in practice).

  python eval/run_private_eval.py answers      # 38 questions x 3 systems (resumable)
  python eval/run_private_eval.py summaries    # whole-document summaries, 3B vs 8B
  python eval/run_private_eval.py report       # tables -> results/private_results.md

Three fictional documents are loaded into an isolated evaluation vault (never the user's real vault):
an employment contract and a confidential memo (both seen while the document prompt was developed, split
"dev_doc"), and a vendor agreement written only for this test (split "held_out"). None of the 38 questions
was used during development. Each question is answered with retrieval restricted to its document.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from vaultwise.config import load_config  # noqa: E402
from vaultwise.documents import save_user_document  # noqa: E402
from vaultwise.metrics import bootstrap_ci, fact_recall, mcnemar_exact, score_answer, unsupported_numbers  # noqa: E402
from vaultwise.pipeline import RAGPipeline  # noqa: E402

OUT = ROOT / "results" / "private"
QUESTIONS = ROOT / "data" / "eval" / "private_questions.jsonl"
FIXED_DATE = "2026-01-01"  # stored in each document header, fixed so the index is identical on every run

DOCS = {  # key: (title, category, source file, split)
    "contract": ("My employment contract", "Contract", "samples/sample-employment-contract.txt", "dev_doc"),
    "memo": ("Project Nimbus memo", "Confidential document", "samples/sample-confidential-memo.txt", "dev_doc"),
    "vendor": ("Vendor services agreement", "Contract", "samples/sample-vendor-agreement.txt", "held_out"),
}
SYSTEMS = {  # (retrieval mode, prompt style); all restricted to the question's document
    "no_search": ("none", "grounded"),     # baseline 1: the model never sees the document
    "vanilla_rag": ("dense", "vanilla"),   # baseline 2: base paper (Lewis et al., 2020) - dense + plain prompt
    "vaultwise": ("hybrid", "grounded"),   # proposed: hybrid RRF + document-scoped grounded prompt
}
# Facts a good summary of each document must contain (number-normalised matching, as in evaluation 1).
SUMMARY_FACTS = {
    "contract": [["1800000"], ["21 days", "21 day"], ["60 days", "60-day", "60 day"], ["3 months", "three months"],
                 ["12 months", "12-month"], ["3 years", "three years"], ["10 percent", "10%"],
                 ["15 july 2026", "july 15, 2026"]],
    "memo": [["4.2 crore"], ["15 december 2026"], ["12 november 2026"], ["17-18 april", "17 and 18 april"],
             ["30 june 2027"], ["march 2027"], ["10 lakh"], ["public ai chatbot", "external tool"]],
    "vendor": [["3 years", "three years"], ["650000"], ["99.9"], ["30 minutes"], ["24 hours"], ["90 days"],
               ["25 percent", "25%"], ["15 days"]],
}
SUMMARY_MODELS = ["llama3.2:3b", "llama3.1:8b"]


def setup(with_pipeline: bool = True) -> tuple[RAGPipeline | None, dict[str, str], dict[str, str]]:
    """Build the isolated evaluation vault and return (pipeline, doc key -> doc id, doc id -> stored text)."""
    cfg = load_config()
    base = Path(cfg["private_dir"]) / "index" / "eval_private"
    uploads = base / "uploads"
    shutil.rmtree(uploads, ignore_errors=True)
    ids = {}
    for key, (title, category, src, _) in DOCS.items():
        ids[key] = save_user_document(uploads, title, (ROOT / src).read_text(encoding="utf-8"), category, FIXED_DATE)
    cfg.update(upload_dir=str(uploads), index_dir=str(base / "index"))
    pipe = RAGPipeline(cfg) if with_pipeline else None  # scoring needs no model, so CI can re-score without Ollama
    texts = {i: (uploads / f"{i}.md").read_text(encoding="utf-8") for i in ids.values()}
    return pipe, ids, texts


def load_items() -> list[dict]:
    return [json.loads(l) for l in QUESTIONS.read_text(encoding="utf-8").splitlines() if l.strip()]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def stage_answers(args) -> None:
    pipe, ids, _ = setup()
    model = pipe.cfg["generation"]["model"]
    (OUT / "runs").mkdir(parents=True, exist_ok=True)
    for system in args.systems.split(","):
        mode, style = SYSTEMS[system]
        path = OUT / "runs" / f"{system}.jsonl"
        done = {r["id"] for r in read_jsonl(path)}
        todo = [q for q in load_items() if q["id"] not in done]
        print(f"[{system}] {len(done)} done, {len(todo)} to run", flush=True)
        with open(path, "a", encoding="utf-8") as f:
            for q in todo:
                r = pipe.answer(q["question"], mode=mode, model=model, prompt_style=style, doc_ids=[ids[q["doc"]]])
                r.update(id=q["id"], system=system)
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                f.flush()


def stage_summaries(args) -> None:
    pipe, ids, _ = setup()
    path = OUT / "summaries.jsonl"
    OUT.mkdir(parents=True, exist_ok=True)
    done = {(r["doc"], r["model"]) for r in read_jsonl(path)}
    with open(path, "a", encoding="utf-8") as f:
        for model in SUMMARY_MODELS:
            for key in DOCS:
                if (key, model) in done:
                    continue
                r = pipe.summarize(ids[key], model=model)
                r.update(doc=key, requested_model=model)
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                f.flush()
                print(f"  summary {key} {model}: {r['latency_s']['total']:.0f}s", flush=True)


def pct(x: float) -> str:
    return "n/a" if x != x else f"{100 * x:.1f}%"


def ci(vals) -> str:
    m, lo, hi = bootstrap_ci(vals)
    return "n/a" if m != m else f"{100 * m:.1f}% [{100 * lo:.0f}-{100 * hi:.0f}]"


def stage_report(args) -> None:
    _, ids, texts = setup(with_pipeline=False)
    items = {q["id"]: q for q in load_items()}
    rows_by_system = {}
    for system in SYSTEMS:
        rows = []
        for r in read_jsonl(OUT / "runs" / f"{system}.jsonl"):
            q = items[r["id"]]
            item = {"id": q["id"], "category": q["category"], "question": q["question"], "key_facts": q["key_facts"],
                    "gold_doc_ids": [] if q["category"] == "unanswerable" else [ids[q["doc"]]]}
            row = score_answer(item, r, texts)
            row.update(split=q["split"], doc=q["doc"], answer=r["answer"])
            rows.append(row)
        rows_by_system[system] = rows
    md = ["# Vaultwise - Evaluation 2: private company documents", "",
          "38 new questions on 3 fictional documents; retrieval restricted to the question's document; generator "
          "`llama3.2:3b`. `dev_doc` = contract and memo (seen while the document prompt was developed; these questions "
          "were not); `held_out` = vendor agreement written only for this test. 95% bootstrap CIs.", "",
          "| System | Overall acc. | Answerable acc. | Correct refusal | False refusal | Unsupported-number rate | "
          "Held-out doc acc. | p50 latency |", "|---|---|---|---|---|---|---|---|"]
    summary = {}
    for system, rows in rows_by_system.items():
        if not rows:
            continue
        ans = [r for r in rows if r["answerable"]]
        una = [r for r in rows if not r["answerable"]]
        held = [r for r in rows if r["split"] == "held_out"]
        s = {"n": len(rows), "overall": np.mean([r["correct"] for r in rows]),
             "answerable": np.mean([r["correct"] for r in ans]), "refusal": np.mean([r["refused"] for r in una]),
             "false_refusal": np.mean([r["false_refusal"] for r in ans]),
             "unsupported": np.mean([r["has_unsupported_number"] for r in rows]),
             "held_out": np.mean([r["correct"] for r in held]),
             "p50": float(np.percentile([r["latency_s"] for r in rows], 50)),
             "by_category": {c: float(np.mean([r["correct"] for r in rows if r["category"] == c]))
                             for c in sorted({r["category"] for r in rows})},
             "by_split": {sp: float(np.mean([r["correct"] for r in rows if r["split"] == sp]))
                          for sp in ("dev_doc", "held_out")}}
        summary[system] = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in s.items()}
        md.append(f"| {system} | {ci([float(r['correct']) for r in rows])} | {ci([float(r['correct']) for r in ans])} "
                  f"| {ci([float(r['refused']) for r in una])} | {ci([float(r['false_refusal']) for r in ans])} "
                  f"| {ci([float(r['has_unsupported_number']) for r in rows])} "
                  f"| {ci([float(r['correct']) for r in held])} | {s['p50']:.1f}s |")
    cats = ["factual", "paraphrase", "general_rule", "unanswerable"]
    md += ["", "Accuracy by category and split:", "", "| System | " + " | ".join(cats) + " | dev_doc | held_out |",
           "|---|---|---|---|---|---|---|"]
    for system, s in summary.items():
        md.append(f"| {system} | " + " | ".join(pct(s["by_category"].get(c, float("nan"))) for c in cats)
                  + f" | {pct(s['by_split']['dev_doc'])} | {pct(s['by_split']['held_out'])} |")
    md += ["", "Paired significance (exact McNemar, Vaultwise vs baseline):", "",
           "| Comparison | n | only Vaultwise correct | only baseline correct | p |", "|---|---|---|---|---|"]
    tests = {}
    if rows_by_system.get("vaultwise"):
        a = {r["id"]: r["correct"] for r in rows_by_system["vaultwise"]}
        for system in ("vanilla_rag", "no_search"):
            b = {r["id"]: r["correct"] for r in rows_by_system.get(system, [])}
            common = sorted(set(a) & set(b))
            if common:
                t = mcnemar_exact([a[i] for i in common], [b[i] for i in common])
                tests[system] = t
                md.append(f"| Vaultwise vs {system} | {len(common)} | {t['a_only_correct']} | {t['b_only_correct']} "
                          f"| {t['p_value']:.4f} |")

    sums = read_jsonl(OUT / "summaries.jsonl")
    md += ["", "## Whole-document summaries", "",
           "Key-fact coverage = share of 8 pre-defined facts per document present in the summary; unsupported numbers "
           "= numbers in the summary that do not appear in the document.", "",
           "| Document | Model | Key-fact coverage | Unsupported numbers | Latency |", "|---|---|---|---|---|"]
    summary["summaries"] = []
    for r in sums:
        cov = fact_recall(r["answer"], SUMMARY_FACTS[r["doc"]])
        bad = sorted(unsupported_numbers(r["answer"], [texts[ids[r["doc"]]]]))
        summary["summaries"].append({"doc": r["doc"], "model": r["model"], "coverage": cov, "unsupported": bad,
                                     "latency_s": r["latency_s"]["total"]})
        md.append(f"| {r['doc']} | {r['model']} | {pct(cov)} | {', '.join(bad) or 'none'} | {r['latency_s']['total']:.0f}s |")
    for m in SUMMARY_MODELS:
        ss = [s for s in summary["summaries"] if s["model"] == m]
        if ss:
            md.append(f"| **mean** | {m} | {pct(np.mean([s['coverage'] for s in ss]))} | "
                      f"{sum(len(s['unsupported']) for s in ss)} total | {np.mean([s['latency_s'] for s in ss]):.0f}s |")

    audit_path = ROOT / "results" / "private_audit.csv"
    if audit_path.exists():  # manual audit of the Vaultwise answers (facts + clause attribution)
        import csv
        au = list(csv.DictReader(open(audit_path, encoding="utf-8")))
        named = [r for r in au if r["clause_named"]]
        ok = [r for r in named if r["clause_correct"] == "1"]
        n_ans = sum(1 for r in au if r["category"] != "unanswerable")
        md += ["", "## Manual audit of the Vaultwise answers (`results/private_audit.csv`)", "",
               f"- Facts correct (human judgement): {sum(int(r['human_facts_correct']) for r in au)}/{len(au)} "
               "(agrees with the automatic scorer on every question)",
               f"- Answers that name a clause or section: {len(named)}/{n_ans} answerable",
               f"- Named clause is the right one: {len(ok)}/{len(named)}; wrong: "
               + "; ".join(f"{r['id']} ({r['note']})" for r in named if r["clause_correct"] != "1")]
        summary["audit"] = {"facts_correct": sum(int(r["human_facts_correct"]) for r in au), "n": len(au),
                            "clause_named": len(named), "clause_correct": len(ok), "answerable": n_ans}

    fails = ["# Evaluation 2 - failure cases", ""]
    for system, rows in rows_by_system.items():
        bad = [r for r in rows if not r["correct"]]
        fails += [f"## {system} - {len(bad)} failures", ""]
        for r in bad:
            fails += [f"- **{r['id']}** ({r['doc']}, {r['category']}, `{r['error_type']}`): {items[r['id']]['question']}",
                      f"  - expected: {items[r['id']]['reference_answer']}",
                      f"  - answer: {r['answer'].strip()[:400]}", ""]
    (ROOT / "results" / "private_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ROOT / "results" / "private_failures.md").write_text("\n".join(fails) + "\n", encoding="utf-8")
    (ROOT / "results" / "private_summary.json").write_text(json.dumps({"systems": summary, "mcnemar": tests},
                                                                      indent=2, default=float), encoding="utf-8")
    print("\n".join(md))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["answers", "summaries", "report"])
    ap.add_argument("--systems", default=",".join(SYSTEMS))
    args = ap.parse_args()
    {"answers": stage_answers, "summaries": stage_summaries, "report": stage_report}[args.stage](args)


if __name__ == "__main__":
    main()

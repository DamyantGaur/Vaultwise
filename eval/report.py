"""Score every run in results/runs/ and write tables, charts, significance tests and failure analysis.

  python eval/report.py

Outputs: results/summary.json, results/results.md, results/failures.md, results/per_question.csv,
results/figures/*.png
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from vaultwise.config import load_config  # noqa: E402
from vaultwise.ingest import load_documents  # noqa: E402
from vaultwise.metrics import mcnemar_exact, score_answer, summarize  # noqa: E402

RESULTS = ROOT / "results"
FIG = RESULTS / "figures"
QUESTIONS = ROOT / "data" / "eval" / "questions.jsonl"

SYSTEM_ORDER = ["llm_only", "rag_vanilla", "rag_bm25", "rag_dense", "rag_hybrid"]
SYSTEM_LABEL = {"llm_only": "LLM only (no retrieval)", "rag_vanilla": "Vanilla RAG (base paper)",
                "rag_bm25": "RAG + BM25", "rag_dense": "RAG + dense", "rag_hybrid": "Vaultwise: hybrid RRF + grounded"}
CATEGORIES = ["factual", "paraphrase", "multi_doc", "unanswerable"]
# validated categorical palette (dataviz skill, light mode), fixed order - never cycled
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def run_key(path: Path) -> tuple[str, str]:
    system, model = path.stem.split("__", 1)
    return system, model


def label(system: str, model: str, default_model: str) -> str:
    base = SYSTEM_LABEL.get(system, system)
    return base if model == default_model.replace(":", "-") else f"{base} [{model}]"


def style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def pct(x: float) -> str:
    return "n/a" if x != x else f"{100 * x:.1f}%"


def ci_str(m: dict) -> str:
    if m["mean"] != m["mean"]:
        return "n/a"
    return f"{100 * m['mean']:.1f}% [{100 * m['ci_low']:.0f}-{100 * m['ci_high']:.0f}]"


def main() -> None:
    cfg = load_config()
    default_model = cfg["generation"]["model"]
    items = {q["id"]: q for q in (json.loads(l) for l in QUESTIONS.read_text(encoding="utf-8").splitlines() if l.strip())}
    doc_texts = {d.doc_id: d.text for d in load_documents(cfg["corpus_dir"])}

    runs = {}
    for path in sorted((RESULTS / "runs").glob("*.jsonl")):
        results = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        rows = [score_answer(items[r["id"]], r, doc_texts) for r in results]
        runs[run_key(path)] = {"results": {r["id"]: r for r in results}, "rows": rows, "summary": summarize(rows)}
    if not runs:
        sys.exit("No runs found in results/runs - run eval/run_eval.py generate first.")

    def order(k):
        s, m = k
        return (m != default_model.replace(":", "-"), m, SYSTEM_ORDER.index(s) if s in SYSTEM_ORDER else 99)
    keys = sorted(runs, key=order)

    # ---------------------------------------------------------------- significance (paired, same questions)
    tests = []
    ref = ("rag_hybrid", default_model.replace(":", "-"))
    for k in keys:
        if k == ref or ref not in runs:
            continue
        common = sorted(set(runs[ref]["results"]) & set(runs[k]["results"]))
        a = {r["id"]: r["correct"] for r in runs[ref]["rows"]}
        b = {r["id"]: r["correct"] for r in runs[k]["rows"]}
        t = mcnemar_exact([a[i] for i in common], [b[i] for i in common])
        t.update(a=label(*ref, default_model), b=label(*k, default_model), n=len(common))
        tests.append(t)

    retrieval = json.loads((RESULTS / "retrieval.json").read_text(encoding="utf-8")) \
        if (RESULTS / "retrieval.json").exists() else None

    summary = {"runs": {f"{s}__{m}": runs[(s, m)]["summary"] for s, m in keys}, "significance": tests}
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # ---------------------------------------------------------------- per-question CSV
    with open(RESULTS / "per_question.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["system", "model", "id", "category", "correct", "fact_recall", "refused", "error_type",
                    "citations", "unsupported_numbers", "latency_s", "question", "answer"])
        for s, m in keys:
            for row in runs[(s, m)]["rows"]:
                r = runs[(s, m)]["results"][row["id"]]
                w.writerow([s, m, row["id"], row["category"], int(row["correct"]),
                            "" if row["fact_recall"] != row["fact_recall"] else round(row["fact_recall"], 3),
                            int(row["refused"]), row["error_type"], ";".join(r["citations"]),
                            ";".join(row["unsupported_numbers"]), r["latency_s"]["total"],
                            items[row["id"]]["question"], r["answer"]])

    # ---------------------------------------------------------------- markdown tables
    md = ["# Vaultwise - Evaluation Results", "",
          f"Questions: {len(items)} ({', '.join(f'{c}: {sum(q['category'] == c for q in items.values())}' for c in CATEGORIES)}). "
          f"Default generator: `{default_model}`. Values are means with 95% bootstrap confidence intervals.", ""]
    if retrieval:
        md += ["## 1. Retrieval quality (answerable questions, document level)", "",
               "| Retriever | Hit@1 | Hit@3 | Hit@4 (used) | Recall@4 | Hit@10 | MRR |", "|---|---|---|---|---|---|---|"]
        for mode in ("bm25", "dense", "hybrid"):
            o = retrieval["main"][mode]["overall"]
            md.append(f"| {mode} | {pct(o['hit@1'])} | {pct(o['hit@3'])} | {pct(o['hit@4'])} | {pct(o['recall@4'])} "
                      f"| {pct(o['hit@10'])} | {o['mrr']:.3f} |")
        md += ["", "Hit@4 by question category:", "", "| Retriever | " + " | ".join(CATEGORIES[:3]) + " |",
               "|---|---|---|---|"]
        for mode in ("bm25", "dense", "hybrid"):
            bc = retrieval["main"][mode]["by_category"]
            md.append(f"| {mode} | " + " | ".join(pct(bc[c]["hit@4"]) for c in CATEGORIES[:3]) + " |")
        md += ["", "Chunking ablation (Hit@1 / Recall@4; `section` = heading-aware with title > section prefix, "
               "`fixed` = naive word windows, `document` = whole file):", "",
               "| Chunking (words/overlap) | # chunks | mean words | BM25 | Dense | Hybrid |", "|---|---|---|---|---|---|"]
        for cs, a in retrieval["chunk_ablation"].items():
            cells = " | ".join(f"{pct(a[m]['hit@1'])} / {pct(a[m]['recall@4'])}" for m in ("bm25", "dense", "hybrid"))
            md.append(f"| {cs} | {a['n_chunks']} | {a['mean_chunk_words']:.0f} | {cells} |")
        md.append("")

    md += ["## 2. End-to-end answer quality", "",
           "| System | Overall acc. | Answerable acc. | Key-fact recall | Correct refusal (unanswerable) | "
           "False refusal | Unsupported-number rate | Citation precision | p50 / p95 latency |",
           "|---|---|---|---|---|---|---|---|---|"]
    for s, m in keys:
        x = runs[(s, m)]["summary"]
        md.append(f"| {label(s, m, default_model)} | {ci_str(x['overall_accuracy'])} | {ci_str(x['answer_accuracy'])} "
                  f"| {ci_str(x['fact_recall'])} | {ci_str(x['refusal_accuracy_unanswerable'])} "
                  f"| {ci_str(x['false_refusal_rate'])} | {ci_str(x['unsupported_number_rate'])} "
                  f"| {ci_str(x['citation_precision'])} | {x['latency_p50_s']:.1f}s / {x['latency_p95_s']:.1f}s |")
    md += ["", "Citation hygiene (answerable questions; RAG systems only):", "",
           "| System | Answers with >=1 valid citation | Citation precision | Citation recall | "
           "Answers citing a non-existent doc id |", "|---|---|---|---|---|"]
    for s, m in keys:
        if s == "llm_only":
            continue
        x = runs[(s, m)]["summary"]
        md.append(f"| {label(s, m, default_model)} | {ci_str(x['answers_with_citation'])} "
                  f"| {ci_str(x['citation_precision'])} | {ci_str(x['citation_recall'])} "
                  f"| {ci_str(x['fabricated_citation_rate'])} |")
    md += ["", "Accuracy by category:", "", "| System | " + " | ".join(CATEGORIES) + " |", "|---|---|---|---|---|"]
    for s, m in keys:
        bc = runs[(s, m)]["summary"]["by_category"]
        md.append(f"| {label(s, m, default_model)} | " + " | ".join(pct(bc[c]["mean"]) if c in bc else "-"
                                                                   for c in CATEGORIES) + " |")
    md += ["", "## 3. Paired significance (exact McNemar test on per-question correctness)", "",
           "| Comparison | n | only A correct | only B correct | p-value |", "|---|---|---|---|---|"]
    for t in tests:
        md.append(f"| A = {t['a']} vs B = {t['b']} | {t['n']} | {t['a_only_correct']} | {t['b_only_correct']} "
                  f"| {t['p_value']:.4f} |")
    md += ["", "## 4. Error attribution", "", "| System | " + " | ".join(
        ["ok", "retrieval_miss", "generation_error", "partial_answer", "false_refusal", "answered_unanswerable"]) + " |",
           "|---|---|---|---|---|---|---|"]
    etypes = ["ok", "retrieval_miss", "generation_error", "partial_answer", "false_refusal", "answered_unanswerable"]
    for s, m in keys:
        e = runs[(s, m)]["summary"]["error_types"]
        md.append(f"| {label(s, m, default_model)} | " + " | ".join(str(e.get(t, 0)) for t in etypes) + " |")
    md.append("")
    (RESULTS / "results.md").write_text("\n".join(md), encoding="utf-8")

    # ---------------------------------------------------------------- failure cases
    fm = ["# Failure cases", "", "Every incorrect answer, grouped by system, with the automatic error attribution.", ""]
    for s, m in keys:
        bad = [r for r in runs[(s, m)]["rows"] if not r["correct"]]
        fm += [f"## {label(s, m, default_model)} - {len(bad)} failures", ""]
        for row in bad:
            r = runs[(s, m)]["results"][row["id"]]
            q = items[row["id"]]
            fm += [f"### {row['id']} ({row['category']}) - `{row['error_type']}`",
                   f"- **Question:** {q['question']}",
                   f"- **Expected:** {q['reference_answer']} (gold docs: {', '.join(q['gold_doc_ids']) or 'none'})",
                   f"- **Retrieved:** {', '.join(x['chunk_id'] for x in r['sources']) or '(no retrieval)'}",
                   f"- **Answer:** {r['answer'].strip()}",
                   f"- fact recall: {pct(row['fact_recall'])}; unsupported numbers: {row['unsupported_numbers'] or 'none'}",
                   ""]
    (RESULTS / "failures.md").write_text("\n".join(fm), encoding="utf-8")

    make_figures(runs, keys, default_model, retrieval)
    print((RESULTS / "results.md").read_text(encoding="utf-8"))


def make_figures(runs, keys, default_model, retrieval) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "text.color": INK,
                         "axes.labelcolor": INK2, "figure.facecolor": SURFACE})
    colors = {k: PALETTE[i] for i, k in enumerate(keys)}
    labels = {k: label(*k, default_model) for k in keys}

    # accuracy by category, grouped bars
    fig, ax = plt.subplots(figsize=(11.5, 4.2))
    groups = CATEGORIES + ["overall"]
    width = 0.8 / len(keys)
    for i, k in enumerate(keys):
        x = runs[k]["summary"]
        vals = [x["by_category"].get(c, {"mean": 0})["mean"] for c in CATEGORIES] + [x["overall_accuracy"]["mean"]]
        pos = [g + (i - (len(keys) - 1) / 2) * width for g in range(len(groups))]
        ax.bar(pos, [100 * v for v in vals], width=width - 0.03, color=colors[k], label=labels[k], zorder=2)
    ax.set_xticks(range(len(groups)), [g.replace("_", " ") for g in groups])
    ax.set_ylabel("Correct (%)")
    ax.set_ylim(0, 105)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
    ax.set_title("Answer accuracy by question category", loc="left", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "accuracy_by_category.png", dpi=160)
    plt.close(fig)

    # trust metrics: refusal accuracy, false refusal, unsupported numbers, citation precision
    metrics = [("refusal_accuracy_unanswerable", "Correct refusal\n(unanswerable)"),
               ("false_refusal_rate", "False refusal\n(answerable)"),
               ("unsupported_number_rate", "Answers with an\nunsupported number"),
               ("citation_precision", "Citation\nprecision")]
    fig, ax = plt.subplots(figsize=(11.5, 4.2))
    for i, k in enumerate(keys):
        x = runs[k]["summary"]
        vals = [x[m]["mean"] for m, _ in metrics]
        vals = [0 if v != v else 100 * v for v in vals]
        pos = [g + (i - (len(keys) - 1) / 2) * width for g in range(len(metrics))]
        ax.bar(pos, vals, width=width - 0.03, color=colors[k], label=labels[k], zorder=2)
    ax.set_xticks(range(len(metrics)), [l for _, l in metrics])
    ax.set_ylabel("%")
    ax.set_ylim(0, 105)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
    ax.set_title("Grounding and refusal behaviour (citation precision n/a without retrieval)", loc="left",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "trust_metrics.png", dpi=160)
    plt.close(fig)

    # latency distribution
    fig, ax = plt.subplots(figsize=(9, 3.6))
    data = [[r["latency_s"] for r in runs[k]["rows"]] for k in keys]
    bp = ax.boxplot(data, vert=False, patch_artist=True, widths=0.5, medianprops={"color": INK})
    for patch, k in zip(bp["boxes"], keys):
        patch.set_facecolor(colors[k])
        patch.set_edgecolor(SURFACE)
    ax.set_yticks(range(1, len(keys) + 1), [labels[k] for k in keys])
    ax.set_xlabel("End-to-end latency per question (s)")
    style_axes(ax)
    ax.xaxis.grid(True, color=GRID)
    ax.yaxis.grid(False)
    ax.set_title("Latency, CPU-only inference (Ryzen 5 4600H laptop, Ollama)", loc="left", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "latency.png", dpi=160)
    plt.close(fig)

    if retrieval:
        fig, ax = plt.subplots(figsize=(6.5, 3.8))
        ks = [1, 3, 4, 5, 10]
        for i, mode in enumerate(("bm25", "dense", "hybrid")):
            o = retrieval["main"][mode]["overall"]
            ys = [100 * o[f"hit@{k}"] for k in ks]
            ax.plot(ks, ys, color=PALETTE[i + 1], linewidth=2, marker="o", markersize=6, label=mode, zorder=3)
            ax.annotate(mode, (ks[-1], ys[-1]), xytext=(6, 0), textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        ax.set_xticks(ks)
        ax.set_xlabel("k (top-k chunks)")
        ax.set_ylabel("Hit@k (%)")
        style_axes(ax)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
        ax.set_title("Retrieval: gold document in top-k", loc="left", fontsize=11)
        fig.tight_layout()
        fig.savefig(FIG / "retrieval_hit_at_k.png", dpi=160)
        plt.close(fig)


if __name__ == "__main__":
    main()

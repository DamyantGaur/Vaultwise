"""Run the Vaultwise experiments.

  python eval/run_eval.py retrieval                       # retrieval metrics + chunk-size ablation (no LLM)
  python eval/run_eval.py generate                        # 4 systems with the default model
  python eval/run_eval.py generate --systems rag_hybrid,llm_only --model llama3.1:8b
  python eval/report.py                                   # tables, charts, failure analysis

Generation is resumable: finished questions are skipped, so an interrupted run can be restarted.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from vaultwise.config import load_config  # noqa: E402
from vaultwise.llm import Embedder, OllamaClient  # noqa: E402
from vaultwise.metrics import retrieval_scores  # noqa: E402
from vaultwise.pipeline import RAGPipeline  # noqa: E402
from vaultwise.retrieval import Index  # noqa: E402

RESULTS = ROOT / "results"
QUESTIONS = ROOT / "data" / "eval" / "questions.jsonl"

SYSTEMS = {                               # (retrieval mode, prompt style)
    "llm_only": ("none", "grounded"),     # baseline 1: same LLM, no retrieval
    "rag_vanilla": ("dense", "vanilla"),  # baseline 2: base paper (Lewis et al., 2020) - dense retrieval, plain prompt
    "rag_bm25": ("bm25", "grounded"),     # ablation: lexical retrieval only
    "rag_dense": ("dense", "grounded"),   # ablation: dense retrieval + grounded prompt
    "rag_hybrid": ("hybrid", "grounded"), # proposed: BM25 + dense fused with RRF + grounded prompt
}
# (strategy, size, overlap). Sections in this corpus are <= 51 words, so section-aware chunking only
# changes with sizes below that; the informative comparison is against heading-unaware windows.
CHUNK_ABLATION = [("section", 120, 30), ("section", 40, 10), ("fixed", 40, 10), ("fixed", 80, 20),
                  ("fixed", 150, 30), ("document", 0, 0)]


def load_questions(limit: int | None = None) -> list[dict]:
    items = [json.loads(line) for line in QUESTIONS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return items[:limit] if limit else items


def safe(name: str) -> str:
    return name.replace(":", "-").replace("/", "-")


def record_metadata(cfg: dict, client: OllamaClient) -> None:
    RESULTS.mkdir(exist_ok=True)
    meta_path = RESULTS / "run_metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    try:
        digests = client.list_models()
    except Exception:  # metadata is best effort
        digests = {}
    meta.update({
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "config": cfg, "ollama_model_digests": digests,
        "n_questions": len(load_questions()),
    })
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


# ----------------------------------------------------------------------------- retrieval stage

def eval_retrieval(index: Index, items: list[dict], depth: int = 10) -> dict:
    answerable = [q for q in items if q["category"] != "unanswerable"]
    out = {}
    for mode in ("bm25", "dense", "hybrid"):
        rows = []
        for q in answerable:
            hits = index.retriever(mode).search(q["question"], depth)
            s = retrieval_scores([h.chunk.doc_id for h in hits], q["gold_doc_ids"])
            s.update(id=q["id"], category=q["category"])
            rows.append(s)
        keys = [k for k in rows[0] if k not in ("id", "category")]
        out[mode] = {
            "overall": {k: float(np.mean([r[k] for r in rows])) for k in keys},
            "by_category": {c: {k: float(np.mean([r[k] for r in rows if r["category"] == c])) for k in keys}
                            for c in sorted({r["category"] for r in rows})},
            "per_question": rows,
        }
    return out


def stage_retrieval(cfg: dict, args) -> None:
    client = OllamaClient(cfg["ollama"]["base_url"], cfg["ollama"]["timeout_s"])
    e = cfg["embedding"]
    embedder = Embedder(client, e["model"], e["query_prefix"], e["document_prefix"], e["batch_size"])
    items = load_questions(args.limit)
    record_metadata(cfg, client)

    index = Index.build_or_load(cfg, embedder)
    main = eval_retrieval(index, items)
    ablation = {}
    for strategy, size, overlap in CHUNK_ABLATION:
        name = f"{strategy}" if strategy == "document" else f"{strategy} {size}/{overlap}"
        acfg = dict(cfg, chunking={"strategy": strategy, "chunk_size_words": size, "overlap_words": overlap},
                    index_dir=str(Path(cfg["index_dir"]) / f"ablation_{strategy}_{size}_{overlap}"))
        aidx = Index.build_or_load(acfg, embedder)
        res = eval_retrieval(aidx, items)
        ablation[name] = {"n_chunks": len(aidx.chunks),
                          "mean_chunk_words": float(np.mean([len(c.text.split()) for c in aidx.chunks])),
                          **{m: res[m]["overall"] for m in res}}
        print(f"  chunks {name}: n={len(aidx.chunks)} "
              + " ".join(f"{m} hit@4={res[m]['overall']['hit@4']:.3f}" for m in res))
    (RESULTS / "retrieval.json").write_text(json.dumps({"main": main, "chunk_ablation": ablation}, indent=2),
                                            encoding="utf-8")
    for m in main:
        o = main[m]["overall"]
        print(f"{m:7s} hit@1={o['hit@1']:.3f} hit@4={o['hit@4']:.3f} recall@4={o['recall@4']:.3f} mrr={o['mrr']:.3f}")
    print(f"Saved {RESULTS / 'retrieval.json'}")


# ----------------------------------------------------------------------------- generation stage

def stage_generate(cfg: dict, args) -> None:
    pipe = RAGPipeline(cfg)
    record_metadata(cfg, pipe.client)
    model = args.model or cfg["generation"]["model"]
    items = load_questions(args.limit)
    run_dir = RESULTS / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    pipe.client.chat([{"role": "user", "content": "hi"}], model=model, max_tokens=1)  # warm-up: load model

    for system in args.systems.split(","):
        mode, prompt_style = SYSTEMS[system]
        path = run_dir / f"{system}__{safe(model)}.jsonl"
        done = set()
        if path.exists():
            done = {json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
        todo = [q for q in items if q["id"] not in done]
        print(f"[{system} | {model}] {len(done)} done, {len(todo)} to run")
        t0 = time.time()
        with open(path, "a", encoding="utf-8") as f:
            for i, q in enumerate(todo, 1):
                r = pipe.answer(q["question"], mode=mode, model=model, prompt_style=prompt_style)
                r.update(id=q["id"], system=system)
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                f.flush()
                if i % 10 == 0 or i == len(todo):
                    print(f"  {i}/{len(todo)}  ({(time.time() - t0) / i:.1f}s/question)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["retrieval", "generate"])
    ap.add_argument("--systems", default=",".join(SYSTEMS))
    ap.add_argument("--model", default=None)
    ap.add_argument("--limit", type=int, default=None, help="evaluate only the first N questions (smoke test)")
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    cfg = load_config(args.config)
    # evaluation uses only the fixed company corpus, never documents uploaded through the UI
    cfg.update(upload_dir=None, index_dir=str(Path(cfg["index_dir"]) / "eval"))
    {"retrieval": stage_retrieval, "generate": stage_generate}[args.stage](cfg, args)


if __name__ == "__main__":
    main()

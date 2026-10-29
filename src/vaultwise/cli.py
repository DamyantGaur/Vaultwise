"""Command line entry point.

  python -m vaultwise.cli index [--force]
  python -m vaultwise.cli ask "How many sick days do I get?" [--mode hybrid]
"""

from __future__ import annotations

import argparse
import json

from .config import load_config
from .pipeline import MODES, RAGPipeline


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="vaultwise")
    ap.add_argument("--config", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_index = sub.add_parser("index", help="build (or rebuild) the retrieval index")
    p_index.add_argument("--force", action="store_true")
    p_ask = sub.add_parser("ask", help="ask a question")
    p_ask.add_argument("question")
    p_ask.add_argument("--mode", choices=MODES, default=None)
    p_ask.add_argument("--json", action="store_true", help="print the full JSON result")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    pipe = RAGPipeline(cfg)
    if args.cmd == "index":
        if args.force:
            pipe.reindex(force=True)
        print(f"{len(pipe.index.doc_ids)} documents, {len(pipe.index.chunks)} chunks")
    elif args.cmd == "ask":
        r = pipe.answer(args.question, mode=args.mode)
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print(r["answer"])
            print(f"\n[mode={r['mode']} model={r['model']} citations={r['citations']} "
                  f"refused={r['refused']} {r['latency_s']['total']:.1f}s]")
            for s in r["sources"]:
                print(f"  {s['rank']}. {s['chunk_id']} ({s['section']}) score={s['score']}")


if __name__ == "__main__":
    main()

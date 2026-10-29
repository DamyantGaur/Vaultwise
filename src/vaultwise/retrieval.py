"""Lexical (BM25), dense (embedding cosine) and hybrid (Reciprocal Rank Fusion) retrieval,
plus an on-disk index that is rebuilt automatically when the corpus or settings change."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from .ingest import Chunk, chunk_documents, load_all_documents

STOPWORDS = set("""
a an and are as at be by can do does for from has have how i if in is it its my of on or our
the their there this to was what when where which who will with you your am me we us should
would could may any all about into than then them they so not no yes per
""".split())


def tokenize(text: str) -> list[str]:
    text = re.sub(r"(?<=\d),(?=\d)", "", text.lower())  # "2,00,000" -> "200000"
    tokens = []
    for tok in re.findall(r"[a-z0-9]+", text):
        if tok in STOPWORDS:
            continue
        if len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]  # crude plural folding: "days" -> "day"
        tokens.append(tok)
    return tokens


@dataclass
class Hit:
    chunk: Chunk
    score: float
    rank: int  # 1-based

    def to_dict(self) -> dict:
        return {"chunk_id": self.chunk.chunk_id, "doc_id": self.chunk.doc_id, "section": self.chunk.section,
                "score": round(float(self.score), 5), "rank": self.rank, "text": self.chunk.text}


def _restrict(scores: np.ndarray, chunks: list[Chunk], doc_ids) -> np.ndarray:
    """Keep only chunks of the selected documents (e.g. "answer only from my contract")."""
    if doc_ids is None:
        return scores
    mask = np.array([c.doc_id in doc_ids for c in chunks])
    return np.where(mask, scores, -np.inf)


def _top(scores: np.ndarray, k: int) -> list[int]:
    return [int(i) for i in np.argsort(-scores)[:k] if np.isfinite(scores[i])]


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(c.text) for c in chunks])

    def search(self, query: str, k: int, doc_ids=None) -> list[Hit]:
        scores = _restrict(np.asarray(self.bm25.get_scores(tokenize(query)), dtype=float), self.chunks, doc_ids)
        order = _top(scores, k)
        return [Hit(self.chunks[i], float(scores[i]), r + 1) for r, i in enumerate(order)]


class DenseRetriever:
    def __init__(self, chunks: list[Chunk], embeddings: np.ndarray, embedder):
        self.chunks = chunks
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.matrix = embeddings / np.clip(norms, 1e-12, None)
        self.embedder = embedder

    def search(self, query: str, k: int, doc_ids=None) -> list[Hit]:
        q = np.asarray(self.embedder.embed_query(query), dtype=np.float32)
        q /= max(np.linalg.norm(q), 1e-12)
        scores = _restrict((self.matrix @ q).astype(float), self.chunks, doc_ids)
        order = _top(scores, k)
        return [Hit(self.chunks[i], float(scores[i]), r + 1) for r, i in enumerate(order)]


def reciprocal_rank_fusion(rankings: list[list[Hit]], k: int, rrf_k: int = 60) -> list[Hit]:
    """RRF (Cormack et al., 2009): score(d) = sum over rankings of 1 / (rrf_k + rank(d))."""
    scores: dict[str, float] = {}
    by_id: dict[str, Chunk] = {}
    for ranking in rankings:
        for hit in ranking:
            cid = hit.chunk.chunk_id
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + hit.rank)
            by_id[cid] = hit.chunk
    order = sorted(scores, key=lambda c: (-scores[c], c))[:k]
    return [Hit(by_id[c], scores[c], r + 1) for r, c in enumerate(order)]


class HybridRetriever:
    def __init__(self, bm25: BM25Retriever, dense: DenseRetriever, candidate_pool: int = 20, rrf_k: int = 60):
        self.bm25, self.dense = bm25, dense
        self.candidate_pool, self.rrf_k = candidate_pool, rrf_k

    def search(self, query: str, k: int, doc_ids=None) -> list[Hit]:
        return reciprocal_rank_fusion(
            [self.bm25.search(query, self.candidate_pool, doc_ids),
             self.dense.search(query, self.candidate_pool, doc_ids)],
            k=k, rrf_k=self.rrf_k)


class Index:
    """Chunks + embeddings persisted under index_dir, keyed by a fingerprint of corpus and settings."""

    def __init__(self, chunks: list[Chunk], embeddings: np.ndarray, embedder, cfg: dict):
        self.chunks = chunks
        self.embeddings = embeddings
        self.doc_ids = sorted({c.doc_id for c in chunks})
        r = cfg["retrieval"]
        self.bm25 = BM25Retriever(chunks)
        self.dense = DenseRetriever(chunks, embeddings, embedder)
        self.hybrid = HybridRetriever(self.bm25, self.dense, r["candidate_pool"], r["rrf_k"])

    def retriever(self, mode: str):
        try:
            return {"bm25": self.bm25, "dense": self.dense, "hybrid": self.hybrid}[mode]
        except KeyError:
            raise ValueError(f"Unknown retrieval mode '{mode}' (use bm25, dense or hybrid)") from None

    @staticmethod
    def fingerprint(cfg: dict) -> str:
        h = hashlib.sha256()
        for d in (cfg["corpus_dir"], cfg.get("upload_dir")):
            if not d or not Path(d).is_dir():
                continue
            for p in sorted(Path(d).iterdir()):
                if p.is_file():
                    h.update(p.name.encode())
                    h.update(p.read_bytes())
        h.update(json.dumps([cfg["chunking"], cfg["embedding"]["model"], cfg["embedding"]["document_prefix"]],
                            sort_keys=True).encode())
        return h.hexdigest()[:16]

    @classmethod
    def build_or_load(cls, cfg: dict, embedder, force: bool = False, log=print) -> "Index":
        index_dir = Path(cfg["index_dir"])
        fp = cls.fingerprint(cfg)
        manifest_path = index_dir / "manifest.json"
        cached: dict[str, np.ndarray] = {}
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            old_chunks = [Chunk(**c) for c in json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))]
            old_emb = np.load(index_dir / "embeddings.npy")
            if not force and manifest.get("fingerprint") == fp:
                log(f"Loaded index {fp}: {len(old_chunks)} chunks from {manifest['n_documents']} documents")
                return cls(old_chunks, old_emb, embedder, cfg)
            if manifest.get("embedding_model") == embedder.model and not force:
                cached = {c.text: e for c, e in zip(old_chunks, old_emb)}  # reuse unchanged chunks
        docs = load_all_documents(cfg)
        ch = cfg["chunking"]
        chunks = chunk_documents(docs, ch["chunk_size_words"], ch["overlap_words"], ch.get("strategy", "section"))
        new_texts = [c.text for c in chunks if c.text not in cached]
        log(f"Building index: {len(docs)} documents -> {len(chunks)} chunks; "
            f"embedding {len(new_texts)} new chunks with {embedder.model} ...")
        fresh = dict(zip(new_texts, embedder.embed_documents(new_texts))) if new_texts else {}
        emb = np.asarray([cached[c.text] if c.text in cached else fresh[c.text] for c in chunks], dtype=np.float32)
        index_dir.mkdir(parents=True, exist_ok=True)
        (index_dir / "chunks.json").write_text(json.dumps([c.to_dict() for c in chunks], indent=1), encoding="utf-8")
        np.save(index_dir / "embeddings.npy", emb)
        manifest_path.write_text(json.dumps({
            "fingerprint": fp, "n_documents": len(docs), "n_chunks": len(chunks),
            "embedding_model": embedder.model, "embedding_dim": int(emb.shape[1]), "chunking": cfg["chunking"],
        }, indent=2), encoding="utf-8")
        log(f"Index {fp} saved to {index_dir}")
        return cls(chunks, emb, embedder, cfg)

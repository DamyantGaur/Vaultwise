"""REST API and web UI.

Run:  python -m uvicorn vaultwise.api:app --app-dir src --port 8000
(uvicorn listens on 127.0.0.1 by default, so the app is reachable only from this computer.)

Every question about the company policies is appended to <log_dir>/queries.jsonl as an audit trail.
Questions that touch the user's private documents are logged as metadata only (no question or answer
text, no document names) unless privacy.log_private_text is enabled.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional
from urllib.parse import urlparse

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import __version__
from .config import LOCAL_HOSTS, PROJECT_ROOT, PrivacyError, load_config
from .documents import (CATEGORIES, MAX_UPLOAD_BYTES, UPLOAD_PREFIX, delete_user_document, extract_text,
                        read_user_document, save_user_document)
from .llm import OllamaClient, OllamaError
from .pipeline import RAGPipeline, is_summary_request

STATIC_DIR = Path(__file__).parent / "static"


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    mode: Literal["none", "bm25", "dense", "hybrid"] = "hybrid"
    top_k: Optional[int] = Field(None, ge=1, le=10)
    doc_ids: Optional[list[str]] = Field(None, description="answer only from these documents, e.g. ['user-my-contract']")


class SummaryRequest(BaseModel):
    focus: str = Field("", max_length=500, description="optional: what the summary should concentrate on")


class FeedbackRequest(BaseModel):
    query_id: str
    helpful: bool
    comment: str = Field("", max_length=2000)


class JsonlLog:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def write(self, record: dict) -> None:
        with self._lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def is_private(doc_id: str) -> bool:
    return doc_id.startswith(UPLOAD_PREFIX)


SAMPLES = [  # fictional documents shipped in samples/, loaded into the cloud demo so it is usable at once
    ("My employment contract", "Contract", "sample-employment-contract.txt"),
    ("Project Nimbus memo", "Confidential document", "sample-confidential-memo.txt"),
    ("Vendor services agreement", "Contract", "sample-vendor-agreement.txt"),
]


def preload_samples(upload_dir: str) -> None:
    """Add the fictional sample documents to an empty vault (cloud demo only)."""
    samples_dir = PROJECT_ROOT / "samples"
    if any(Path(upload_dir).glob(f"{UPLOAD_PREFIX}*.md")) or not samples_dir.is_dir():
        return
    for title, category, name in SAMPLES:
        if (samples_dir / name).exists():
            save_user_document(upload_dir, title, (samples_dir / name).read_text(encoding="utf-8"), category)


def create_app(pipeline: RAGPipeline | None = None, cfg: dict | None = None) -> FastAPI:
    cfg = cfg or (pipeline.cfg if pipeline else load_config())
    app = FastAPI(title="Vaultwise", version=__version__,
                  description="Private, grounded question answering over company policies and your own documents.")
    state = {"pipeline": pipeline}
    query_log = JsonlLog(Path(cfg["log_dir"]) / "queries.jsonl")
    feedback_log = JsonlLog(Path(cfg["log_dir"]) / "feedback.jsonl")
    upload_dir = cfg.get("upload_dir")
    log_private_text = cfg.get("privacy", {}).get("log_private_text", False)
    if cfg.get("preload_samples") and upload_dir:
        preload_samples(upload_dir)

    def get_pipeline() -> RAGPipeline:
        if state["pipeline"] is None:
            try:
                state["pipeline"] = RAGPipeline(cfg)
            except (OllamaError, PrivacyError) as e:
                raise HTTPException(503, str(e)) from e
        return state["pipeline"]

    def log_query(result: dict) -> None:
        touched = (result.get("doc_filter") or []) + [s["doc_id"] for s in result["sources"]] + result["citations"]
        record = {"ts": datetime.now(timezone.utc).isoformat(), "query_id": result["query_id"],
                  "mode": result["mode"], "model": result["model"], "refused": result["refused"],
                  "latency_s": result["latency_s"]}
        if any(is_private(d) for d in touched) and not log_private_text:
            record["private"] = True  # never write confidential questions, answers or document names to disk
        else:
            record.update(question=result["question"], answer=result["answer"], doc_filter=result.get("doc_filter"),
                          citations=result["citations"], retrieved=[s["chunk_id"] for s in result["sources"]])
        query_log.write(record)

    @app.get("/", include_in_schema=False)
    def ui():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health")
    def health():
        p = state["pipeline"]
        client = p.client if p else OllamaClient(cfg["ollama"]["base_url"], cfg["ollama"]["timeout_s"])
        host = (urlparse(cfg["ollama"]["base_url"]).hostname or "").lower()
        n_private = len(list(Path(upload_dir).glob(f"{UPLOAD_PREFIX}*.md"))) if upload_dir and Path(upload_dir).is_dir() else 0
        return {"status": "ok", "version": __version__, "deployment": cfg.get("deployment", "local"),
                "uploads_need_key": bool(os.environ.get("VAULTWISE_ADMIN_KEY")),
                "ollama_reachable": client.is_alive(),
                "index_loaded": p is not None, "n_chunks": len(p.index.chunks) if p else None,
                "generation_model": cfg["generation"]["model"], "embedding_model": cfg["embedding"]["model"],
                "summary_model": cfg["generation"].get("summary_model") or cfg["generation"]["model"],
                "privacy": {"model_server_on_this_machine": host in LOCAL_HOSTS,
                            "private_data_dir": cfg.get("private_dir"), "private_documents": n_private,
                            "private_text_logged": bool(log_private_text)}}

    @app.get("/documents")
    def documents():
        p = get_pipeline()
        counts: dict[str, dict] = {}
        for c in p.index.chunks:
            d = counts.setdefault(c.doc_id, {"doc_id": c.doc_id, "title": c.title, "chunks": 0,
                                             "uploaded": is_private(c.doc_id), "category": "Sample policy (demo)"})
            d["chunks"] += 1
        for d in counts.values():
            if d["uploaded"] and upload_dir:
                meta = read_user_document(upload_dir, d["doc_id"]) or {}
                d.update(category=meta.get("category", "Other"), added=meta.get("added", ""))
        return sorted(counts.values(), key=lambda d: d["doc_id"])

    @app.get("/documents/{doc_id}")
    def view_document(doc_id: str):
        """Read back the stored text of one of your private documents."""
        if not upload_dir:
            raise HTTPException(400, "private documents are disabled")
        try:
            doc = read_user_document(upload_dir, doc_id)
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
        if doc is None:
            raise HTTPException(404, f"no private document '{doc_id}'")
        return doc

    def run_summary(doc_id: str, focus: str) -> dict:
        p = get_pipeline()
        try:
            result = p.summarize(doc_id, focus=focus or None)
        except OllamaError as e:
            raise HTTPException(503, str(e)) from e
        except ValueError as e:
            raise HTTPException(404, str(e)) from e
        result["query_id"] = str(uuid.uuid4())
        log_query(result)
        return result

    @app.post("/documents/{doc_id}/summary")
    def summarize_document(doc_id: str, req: SummaryRequest | None = None):
        return run_summary(doc_id, req.focus if req else "")

    @app.post("/ask")
    def ask(req: AskRequest):
        # "summarise this", "give me the key points" with one document selected -> whole-document summary
        if req.doc_ids and len(req.doc_ids) == 1 and is_summary_request(req.question):
            return run_summary(req.doc_ids[0], req.question)
        p = get_pipeline()
        try:
            result = p.answer(req.question, mode=req.mode, top_k=req.top_k, doc_ids=req.doc_ids)
        except OllamaError as e:
            raise HTTPException(503, str(e)) from e
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
        result["query_id"] = str(uuid.uuid4())
        log_query(result)
        return result

    @app.post("/feedback")
    def feedback(req: FeedbackRequest):
        feedback_log.write({"ts": datetime.now(timezone.utc).isoformat(), **req.model_dump()})
        return {"status": "recorded"}

    def check_admin(key: str | None) -> None:
        expected = os.environ.get("VAULTWISE_ADMIN_KEY")
        if expected and key != expected:
            raise HTTPException(401, "invalid admin key")

    @app.post("/documents/upload")
    async def upload_document(title: str = Form("", max_length=120), text: str = Form(""),
                              category: str = Form("Other"), file: UploadFile | None = File(None),
                              x_admin_key: str | None = Header(None)):
        """Add a private document (PDF, DOCX, TXT, MD file, or pasted text) and index it."""
        check_admin(x_admin_key)
        if upload_dir is None:
            raise HTTPException(400, "uploads are disabled (upload_dir is not set in config.yaml)")
        if category not in CATEGORIES:
            raise HTTPException(400, f"category must be one of: {', '.join(CATEGORIES)}")
        try:
            if file is not None and file.filename:
                data = await file.read()
                if len(data) > MAX_UPLOAD_BYTES:
                    raise ValueError("file is larger than 10 MB")
                content = extract_text(file.filename, data)
                title = title.strip() or Path(file.filename).stem
            elif text.strip():
                content = text
                if not title.strip():
                    raise ValueError("please give pasted text a title")
            else:
                raise ValueError("upload a file or paste some text")
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
        p = get_pipeline()
        doc_id = save_user_document(upload_dir, title, content, category)
        try:
            p.reindex(log=lambda *_: None)
        except OllamaError as e:
            delete_user_document(upload_dir, doc_id)
            raise HTTPException(503, str(e)) from e
        n = sum(1 for c in p.index.chunks if c.doc_id == doc_id)
        sections = sorted({c.section for c in p.index.chunks if c.doc_id == doc_id})
        return {"doc_id": doc_id, "title": title, "category": category, "chunks": n, "sections": sections,
                "words": len(content.split())}

    @app.delete("/documents/{doc_id}")
    def delete_document(doc_id: str, x_admin_key: str | None = Header(None)):
        check_admin(x_admin_key)
        if upload_dir is None:
            raise HTTPException(400, "uploads are disabled")
        try:
            found = delete_user_document(upload_dir, doc_id)
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
        if not found:
            raise HTTPException(404, f"no uploaded document '{doc_id}'")
        get_pipeline().reindex(log=lambda *_: None)  # also removes its text and embeddings from the index
        return {"status": "deleted", "doc_id": doc_id}

    @app.post("/admin/reindex")
    def reindex(x_admin_key: str | None = Header(None)):
        check_admin(x_admin_key)
        p = get_pipeline()
        p.reindex(log=lambda *_: None)
        return {"status": "reindexed", "n_documents": len(p.index.doc_ids), "n_chunks": len(p.index.chunks)}

    return app


app = create_app()

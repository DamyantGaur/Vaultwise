import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from conftest import FakeClient
from vaultwise.api import create_app
from vaultwise.config import PrivacyError, check_private_endpoint, load_config
from vaultwise.documents import read_user_document, save_user_document
from vaultwise.llm import Embedder
from vaultwise.pipeline import RAGPipeline, is_summary_request

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = (ROOT / "samples" / "sample-employment-contract.txt").read_text(encoding="utf-8")
SECRET = "Project Falcon acquisition price is INR 900 crore"


def make_pipeline(cfg, reply="Overview: an employment contract [user-my-contract]."):
    client = FakeClient(reply)
    return RAGPipeline(cfg, client=client, embedder=Embedder(client, "fake"), log=lambda *_: None), client


def test_private_data_lives_outside_project_by_default(monkeypatch, tmp_path):
    cfg = load_config()
    assert not cfg["upload_dir"].startswith(str(ROOT)) and not cfg["index_dir"].startswith(str(ROOT))
    monkeypatch.setenv("VAULTWISE_DATA_DIR", str(tmp_path / "vault"))
    cfg = load_config()
    assert cfg["upload_dir"] == str(tmp_path / "vault" / "uploads")


def test_remote_model_server_is_refused():
    cfg = load_config(overrides={"ollama": {"base_url": "https://llm.example.com"}})
    with pytest.raises(PrivacyError):
        check_private_endpoint(cfg)
    check_private_endpoint(load_config(overrides={"ollama": {"base_url": "https://llm.example.com"},
                                                  "privacy": {"allow_remote_llm": True}}))
    check_private_endpoint(load_config())  # localhost is fine


def test_category_is_stored_and_read_back(tmp_path):
    doc_id = save_user_document(tmp_path, "Travel policy 2026", "1. Booking\nBook 14 days ahead.", "Company policy")
    d = read_user_document(tmp_path, doc_id)
    assert d["title"] == "Travel policy 2026" and d["category"] == "Company policy" and "14 days" in d["text"]
    with pytest.raises(ValueError):
        read_user_document(tmp_path, "../config")


def test_summary_intent():
    assert is_summary_request("Summarise this document")
    assert is_summary_request("give me the key points")
    assert not is_summary_request("What is my notice period?")


def test_short_document_summarised_in_one_call(cfg):
    save_user_document(cfg["upload_dir"], "My contract", SAMPLE, "Contract")
    pipe, client = make_pipeline(cfg)
    r = pipe.summarize("user-my-contract")
    assert len(client.calls) == 1 and r["mode"] == "summary" and r["citations"] == ["user-my-contract"]
    sent = client.calls[0][1]["content"]
    assert "10. Termination and Notice Period" in sent and "11. Governing Law" in sent  # whole document, not top-k


def test_long_document_is_summarised_in_parts_then_merged(cfg):
    long_text = "\n".join(f"{i}. Section {i}\n" + ("word " * 400) for i in range(1, 9))  # ~3,200 words
    save_user_document(cfg["upload_dir"], "Long policy", long_text, "Company policy")
    pipe, client = make_pipeline(cfg)
    r = pipe.summarize("user-long-policy")
    assert r["summary_of"]["parts"] >= 3
    assert len(client.calls) == r["summary_of"]["parts"] + 1  # one call per part + one merge


def test_summary_falls_back_when_summary_model_missing(cfg):
    from vaultwise.llm import OllamaError
    save_user_document(cfg["upload_dir"], "My contract", SAMPLE, "Contract")
    pipe, client = make_pipeline(cfg)
    orig = client.chat

    def chat(messages, model, **kw):
        if model == "llama3.1:8b":
            raise OllamaError("Ollama /api/chat returned 404: model 'llama3.1:8b' not found")
        return orig(messages, model, **kw)
    client.chat = chat
    assert pipe.summarize("user-my-contract")["model"] == cfg["generation"]["model"]


def test_ask_routes_summary_and_private_questions_are_not_logged(cfg):
    save_user_document(cfg["upload_dir"], "Deal memo", f"1. Terms\n{SECRET}.", "Confidential document")
    pipe, _ = make_pipeline(cfg)
    api = TestClient(create_app(pipe))
    s = api.post("/ask", json={"question": "Summarise this", "doc_ids": ["user-deal-memo"]}).json()
    assert s["mode"] == "summary"
    api.post("/ask", json={"question": f"Is the {SECRET}?", "doc_ids": ["user-deal-memo"]})
    api.post("/ask", json={"question": "How much annual leave do I get?"})
    log = (Path(cfg["log_dir"]) / "queries.jsonl").read_text(encoding="utf-8")
    assert "Falcon" not in log and "deal-memo" not in log      # no confidential text or document name
    rows = [json.loads(l) for l in log.splitlines()]
    assert sum(1 for r in rows if r.get("private")) >= 2
    assert any(r.get("question") == "How much annual leave do I get?" for r in rows)  # normal policy Q logged


def test_view_document_and_health_privacy(cfg):
    save_user_document(cfg["upload_dir"], "My contract", SAMPLE, "Contract")
    pipe, _ = make_pipeline(cfg)
    api = TestClient(create_app(pipe))
    v = api.get("/documents/user-my-contract").json()
    assert v["category"] == "Contract" and "Non-Solicitation" in v["text"]
    assert api.get("/documents/hr-leave-policy").status_code == 400
    docs = {d["doc_id"]: d for d in api.get("/documents").json()}
    assert docs["user-my-contract"]["category"] == "Contract"
    p = api.get("/health").json()["privacy"]
    assert p["model_server_on_this_machine"] and p["private_documents"] == 1 and not p["private_text_logged"]


def test_cloud_mode_settings_and_sample_preload(monkeypatch, tmp_path):
    monkeypatch.setenv("VAULTWISE_MODE", "cloud")
    monkeypatch.setenv("VAULTWISE_PRELOAD_SAMPLES", "1")
    monkeypatch.setenv("VAULTWISE_SUMMARY_MODEL", "llama3.2:3b")
    cfg = load_config(overrides={"index_dir": str(tmp_path / "index"), "log_dir": str(tmp_path / "logs"),
                                 "upload_dir": str(tmp_path / "uploads")})
    assert cfg["deployment"] == "cloud" and cfg["preload_samples"]
    assert cfg["generation"]["summary_model"] == "llama3.2:3b"
    pipe, _ = make_pipeline(cfg)
    api = TestClient(create_app(pipe))  # preloads the three fictional samples into the empty vault
    mine = [d["doc_id"] for d in api.get("/documents").json() if d["uploaded"]]
    assert mine == []  # pipeline index was built before preload; a reindex picks them up
    pipe.reindex(log=lambda *_: None)
    mine = sorted(d["doc_id"] for d in api.get("/documents").json() if d["uploaded"])
    assert mine == ["user-my-employment-contract", "user-project-nimbus-memo", "user-vendor-services-agreement"]
    assert api.get("/health").json()["deployment"] == "cloud"
    create_app(pipe)  # preloading again must not duplicate documents
    assert len(list((tmp_path / "uploads").glob("user-*.md"))) == 3


def test_local_mode_is_default():
    assert load_config()["deployment"] == "local" and not load_config()["preload_samples"]

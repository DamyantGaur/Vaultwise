from fastapi.testclient import TestClient

from conftest import FakeClient
from vaultwise.api import create_app
from vaultwise.llm import Embedder
from vaultwise.pipeline import RAGPipeline, extract_citations, is_refusal

DOC_IDS = ["hr-leave-policy", "it-device-policy"]


def make_pipeline(cfg, reply="Employees get 24 days [hr-leave-policy]."):
    client = FakeClient(reply)
    return RAGPipeline(cfg, client=client, embedder=Embedder(client, "fake"), log=lambda *_: None), client


def test_citation_parsing_variants():
    text = "24 days [hr-leave-policy]. Report within 1 hour [Source: it-device-policy, hr-leave-policy] [1] [made-up-doc]"
    valid, invalid = extract_citations(text, DOC_IDS)
    assert valid == ["hr-leave-policy", "it-device-policy"]
    assert invalid == ["made-up-doc"]
    assert extract_citations("Within 1 hour [2].", DOC_IDS, ["hr-leave-policy", "it-device-policy"]) == \
        (["it-device-policy"], [])
    # a real document id that was not in the model's context is not a valid citation
    assert extract_citations("21 days [hr-leave-policy].", DOC_IDS, ["it-device-policy"])[0] == []


def test_refusal_detection():
    assert is_refusal("I don't have enough information in the company documents to answer that.")
    assert is_refusal("The context does not mention bereavement leave.")
    assert is_refusal("There is no specific mention of blood donation in the provided context.")
    assert is_refusal("There is no mileage reimbursement rate specified in the provided policies.")
    assert is_refusal("There is no information provided in the context passages regarding a shuttle bus.")
    assert not is_refusal("You get 12 days of sick leave [hr-leave-policy].")
    assert not is_refusal("No, you cannot bring your dog to the office.")


def test_rag_prompt_contains_retrieved_context(cfg):
    pipe, client = make_pipeline(cfg)
    r = pipe.answer("How many days of annual leave?", mode="bm25")
    user_msg = client.calls[-1][1]["content"]
    assert "Context:" in user_msg and "[hr-leave-policy]" in user_msg
    assert r["citations"] == ["hr-leave-policy"] and not r["refused"]
    assert len(r["sources"]) == cfg["retrieval"]["top_k"]


def test_no_retrieval_baseline_sends_no_context(cfg):
    pipe, client = make_pipeline(cfg)
    r = pipe.answer("How many days of annual leave?", mode="none")
    assert r["sources"] == [] and "Context:" not in client.calls[-1][1]["content"]


def test_api_ask_feedback_and_logging(cfg, tmp_path):
    pipe, _ = make_pipeline(cfg)
    api = TestClient(create_app(pipe))
    assert api.get("/health").json()["index_loaded"] is True
    r = api.post("/ask", json={"question": "How much annual leave do I get?", "mode": "hybrid"})
    assert r.status_code == 200
    body = r.json()
    assert body["query_id"] and body["citations"] == ["hr-leave-policy"]
    assert api.post("/feedback", json={"query_id": body["query_id"], "helpful": True}).status_code == 200
    assert api.post("/ask", json={"question": "hi", "mode": "bogus"}).status_code == 422
    assert len(api.get("/documents").json()) == 18
    logs = (tmp_path / "logs" / "queries.jsonl").read_text(encoding="utf-8")
    assert body["query_id"] in logs


def test_admin_reindex_requires_key(cfg, monkeypatch):
    pipe, _ = make_pipeline(cfg)
    api = TestClient(create_app(pipe))
    monkeypatch.setenv("VAULTWISE_ADMIN_KEY", "secret")
    assert api.post("/admin/reindex").status_code == 401
    assert api.post("/admin/reindex", headers={"x-admin-key": "secret"}).json()["n_documents"] == 18

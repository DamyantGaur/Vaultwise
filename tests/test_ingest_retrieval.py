import pytest

from vaultwise.ingest import Chunk, chunk_documents, load_documents, split_sections, window_words
from vaultwise.llm import Embedder
from vaultwise.retrieval import BM25Retriever, Hit, Index, reciprocal_rank_fusion, tokenize


def test_corpus_loads_with_titles(cfg):
    docs = load_documents(cfg["corpus_dir"])
    assert len(docs) == 18
    assert {d.doc_id for d in docs} >= {"hr-leave-policy", "it-vpn-remote-access"}
    assert next(d for d in docs if d.doc_id == "hr-leave-policy").title == "Leave Policy"


def test_split_sections_keeps_headings():
    secs = split_sections("# T\nmeta line\n## A\nalpha\n## B\nbeta")
    assert secs == [("Overview", "meta line"), ("A", "alpha"), ("B", "beta")]


def test_window_words_overlap_and_coverage():
    words = [str(i) for i in range(25)]
    wins = window_words(words, 10, 3)
    assert wins[0] == words[:10] and wins[1][0] == "7"
    assert wins[-1][-1] == "24"
    with pytest.raises(ValueError):
        window_words(words, 10, 10)


def test_chunks_carry_title_and_section(cfg):
    chunks = chunk_documents(load_documents(cfg["corpus_dir"]), 120, 30)
    c = next(c for c in chunks if c.doc_id == "hr-leave-policy" and c.section == "Sick Leave")
    assert c.text.startswith("Leave Policy > Sick Leave")
    assert len({c.chunk_id for c in chunks}) == len(chunks)


def test_tokenize_normalizes_numbers_and_plurals():
    assert tokenize("Purchases above INR 2,00,000 need quotes") == ["purchase", "above", "inr", "200000", "need", "quote"]


def test_bm25_finds_lexical_match(cfg):
    chunks = chunk_documents(load_documents(cfg["corpus_dir"]))
    hits = BM25Retriever(chunks).search("minimum password length characters", 3)
    assert hits[0].chunk.doc_id == "it-password-policy"


def _hit(cid, rank):
    return Hit(Chunk(cid, cid.split("#")[0], "t", "s", "x"), 0.0, rank)


def test_rrf_rewards_agreement():
    a = [_hit("a#0", 1), _hit("b#0", 2), _hit("x#0", 3), _hit("c#0", 4)]
    b = [_hit("c#0", 1), _hit("b#0", 2), _hit("d#0", 3)]
    fused = reciprocal_rank_fusion([a, b], k=5, rrf_k=60)
    assert fused[0].chunk.chunk_id == "b#0"          # 2nd in both (2/62) beats 1st + 4th (1/61 + 1/64)
    assert fused[1].chunk.chunk_id == "c#0"          # found by both beats any single-list item
    assert {h.chunk.chunk_id for h in fused} == {"a#0", "b#0", "c#0", "d#0", "x#0"}
    assert [h.rank for h in fused] == [1, 2, 3, 4, 5]


def test_index_is_cached_and_rebuilt_on_change(cfg, fake_client):
    emb = Embedder(fake_client, "fake")
    logs = []
    Index.build_or_load(cfg, emb, log=logs.append)
    Index.build_or_load(cfg, emb, log=logs.append)
    assert logs[0].startswith("Building") and logs[-1].startswith("Loaded")
    cfg2 = dict(cfg, chunking={"chunk_size_words": 60, "overlap_words": 10})
    Index.build_or_load(cfg2, emb, log=logs.append)
    assert logs[-1].startswith("Index") and any(l.startswith("Building") for l in logs[2:])

import json
import math
from pathlib import Path

from vaultwise.metrics import (attribute_error, bootstrap_ci, extract_numbers, fact_recall, mcnemar_exact,
                                 retrieval_scores, score_answer, unsupported_numbers)

ROOT = Path(__file__).resolve().parents[1]


def test_fact_recall_number_normalization():
    assert fact_recall("The stipend is INR 15,000.", [["15000"]]) == 1.0
    assert fact_recall("The stipend is ₹15,000.", [["15000"]]) == 1.0
    assert fact_recall("It is 150000 rupees", [["15000"]]) == 0.0          # word boundaries
    assert fact_recall("Rate is **24** days", [["24"], ["sick"]]) == 0.5
    assert fact_recall("Costs $75 per day", [["$"]]) == 1.0
    assert math.isnan(fact_recall("anything", []))
    # regression: "Rs." currency handling must not corrupt words ending in "rs."
    assert fact_recall("The term runs for 3 years. It renews.", [["3 years"]]) == 1.0
    assert fact_recall("Response within 24 hours.", [["24 hours"]]) == 1.0
    assert fact_recall("A fee of Rs. 500 applies", [["inr 500"]]) == 1.0


def test_numbers_and_unsupported():
    assert extract_numbers("SEV1 within 15 minutes [1], 24x7, 2,00,000") == {"15", "200000"}
    assert unsupported_numbers("Cap is INR 9,000 per night", ["capped at INR 7,000 per night"]) == {"9000"}
    assert unsupported_numbers("Cap is INR 7,000", ["capped at INR 7,000 per night"]) == set()


def test_retrieval_scores_count_chunks_not_documents():
    s = retrieval_scores(["a", "a", "b", "c"], ["b", "c"], ks=(1, 2, 3, 4))
    assert s["hit@2"] == 0 and s["hit@3"] == 1 and s["recall@3"] == 0.5 and s["recall@4"] == 1
    assert abs(s["mrr"] - 1 / 3) < 1e-9


def test_score_unanswerable_and_attribution():
    item = {"id": "u", "category": "unanswerable", "question": "Dress code?", "gold_doc_ids": [], "key_facts": []}
    res = {"answer": "I don't have enough information.", "refused": True, "citations": [], "sources": [],
           "latency_s": {"total": 1.0}}
    row = score_answer(item, res, {})
    assert row["correct"] and row["error_type"] == "ok"
    res2 = dict(res, answer="Business casual, Monday to Friday 5 days.", refused=False)
    row2 = score_answer(item, res2, {})
    assert not row2["correct"] and row2["error_type"] == "answered_unanswerable" and row2["has_unsupported_number"]


def test_attribute_retrieval_miss():
    row = {"correct": False, "answerable": True, "gold_in_context": False, "false_refusal": True, "fact_recall": 0}
    assert attribute_error(row) == "retrieval_miss"


def test_stats():
    m, lo, hi = bootstrap_ci([1, 0, 1, 1])
    assert m == 0.75 and lo <= m <= hi
    t = mcnemar_exact([True] * 10 + [False] * 5, [False] * 10 + [False] * 5)
    assert t["a_only_correct"] == 10 and t["p_value"] < 0.01


def test_eval_set_is_well_formed():
    docs = {p.stem for p in (ROOT / "data" / "corpus").glob("*.md")}
    items = [json.loads(l) for l in (ROOT / "data" / "eval" / "questions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len({i["id"] for i in items}) == len(items) == 76
    for i in items:
        assert set(i["gold_doc_ids"]) <= docs, i["id"]
        if i["category"] == "unanswerable":
            assert not i["gold_doc_ids"] and not i["key_facts"]
        else:
            assert i["gold_doc_ids"] and i["key_facts"]


def test_private_eval_set_labels_are_consistent():
    """Evaluation 2: every key fact must occur in its document; summary facts too; ids unique."""
    from vaultwise.metrics import contains_variant, normalize
    sys_path = ROOT / "eval"
    import sys
    sys.path.insert(0, str(sys_path))
    from run_private_eval import DOCS, SUMMARY_FACTS
    texts = {k: normalize((ROOT / src).read_text(encoding="utf-8")) for k, (_, _, src, _) in DOCS.items()}
    items = [json.loads(l) for l in (ROOT / "data" / "eval" / "private_questions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len({i["id"] for i in items}) == len(items) == 38
    for i in items:
        assert i["doc"] in DOCS and i["split"] == DOCS[i["doc"]][3]
        assert bool(i["key_facts"]) == (i["category"] != "unanswerable"), i["id"]
        for fact in i["key_facts"]:
            assert any(contains_variant(texts[i["doc"]], v) for v in fact), (i["id"], fact)
    for doc, facts in SUMMARY_FACTS.items():
        for fact in facts:
            assert any(contains_variant(texts[doc], v) for v in fact), (doc, fact)


def test_every_key_fact_is_supported_by_gold_docs():
    """Guards against label errors: each key fact (except computed ones) must appear in a gold document."""
    from vaultwise.metrics import contains_variant, normalize
    texts = {p.stem: normalize(p.read_text(encoding="utf-8")) for p in (ROOT / "data" / "corpus").glob("*.md")}
    computed = {"m04"}
    items = [json.loads(l) for l in (ROOT / "data" / "eval" / "questions.jsonl").read_text(encoding="utf-8").splitlines()]
    for i in items:
        if i["id"] in computed:
            continue
        gold = " ".join(texts[d] for d in i["gold_doc_ids"])
        for fact in i["key_facts"]:
            if i["category"] == "paraphrase" and fact[0] in ("never", "blocked"):
                continue  # judgement facts phrased by the answer, not quoted
            assert any(contains_variant(gold, v) for v in fact), (i["id"], fact)

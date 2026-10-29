"""Deterministic evaluation metrics, statistics and error attribution.

All answer-level metrics are rule-based (no LLM judge) so that a re-run on the same outputs
gives identical scores. The scorer itself is validated against a manual audit (docs/REPORT.md).
"""

from __future__ import annotations

import re

import numpy as np
from scipy.stats import binomtest

from .pipeline import is_refusal

# ----------------------------------------------------------------------------- text matching

def normalize(text: str) -> str:
    t = text.lower().replace("₹", " inr ")
    t = re.sub(r"\brs\.?\s*(?=\d)", " inr ", t)  # currency "Rs. 500" / "Rs 500" only; not "years." or "hours."
    t = t.replace("’", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"(?<=\d),(?=\d)", "", t)          # 2,00,000 -> 200000
    t = re.sub(r"\*\*|__", "", t)                  # markdown bold
    return re.sub(r"\s+", " ", t)


def contains_variant(norm_text: str, variant: str) -> bool:
    v = normalize(variant).strip()
    left = r"(?<![a-z0-9])" if v[:1].isalnum() else ""
    if v[-1:].isalpha():
        right = r"(?:s|es|d|ed|ing)?(?![a-z0-9])"  # "director" matches "Directors", "return" matches "returned"
    elif v[-1:].isdigit():
        right = r"(?![0-9])(?!\.[0-9])"             # "15" must not match "150" or "15.5"
    else:
        right = ""
    return re.search(left + re.escape(v) + right, norm_text) is not None


def fact_recall(answer: str, key_facts: list[list[str]]) -> float:
    """Fraction of key facts present; each fact is a list of acceptable surface variants."""
    if not key_facts:
        return float("nan")
    norm = normalize(answer)
    return sum(any(contains_variant(norm, v) for v in fact) for fact in key_facts) / len(key_facts)


def extract_numbers(text: str) -> set[str]:
    t = re.sub(r"\[[^\]]*\]", " ", normalize(text))  # ignore bracketed citations like [1]
    nums = re.findall(r"(?<![a-z0-9:.\-])(\d+(?:\.\d+)?)(?![a-z0-9])", t)
    return {n.lstrip("0") or "0" for n in nums}


def unsupported_numbers(answer: str, evidence_texts: list[str]) -> set[str]:
    """Numbers stated in the answer that appear in none of the evidence texts (hallucination proxy)."""
    supported: set[str] = set()
    for e in evidence_texts:
        supported |= extract_numbers(e)
    return extract_numbers(answer) - supported


# ----------------------------------------------------------------------------- retrieval

def retrieval_scores(ranked_doc_ids: list[str], gold: list[str], ks=(1, 3, 4, 5, 10)) -> dict:
    """Metrics over the top-k *chunks* (what the LLM actually receives), judged at document level:
    hit@k = a gold document is among the first k chunks; recall@k = share of gold documents covered;
    mrr = 1 / rank of the first chunk from a gold document."""
    out = {}
    gold_set = set(gold)
    for k in ks:
        top = set(ranked_doc_ids[:k])
        out[f"hit@{k}"] = float(bool(top & gold_set))
        out[f"recall@{k}"] = len(top & gold_set) / len(gold_set)
    out["mrr"] = next((1.0 / i for i, d in enumerate(ranked_doc_ids, 1) if d in gold_set), 0.0)
    return out


# ----------------------------------------------------------------------------- per-answer scoring

def score_answer(item: dict, result: dict, doc_texts: dict[str, str]) -> dict:
    """item: evaluation question; result: pipeline output. Returns a flat per-question score row."""
    answerable = item["category"] != "unanswerable"
    ans = result["answer"]
    refused = is_refusal(ans)  # recomputed from text so detector fixes apply to stored runs
    row = {"id": item["id"], "category": item["category"], "answerable": answerable, "refused": refused,
           "latency_s": result["latency_s"]["total"]}

    evidence = [doc_texts[d] for d in item["gold_doc_ids"]] + [item["question"]]
    evidence += [v for fact in item["key_facts"] for v in fact]  # e.g. computed totals in reasoning items
    bad_nums = unsupported_numbers(ans, evidence)
    row["unsupported_numbers"] = sorted(bad_nums)
    row["has_unsupported_number"] = bool(bad_nums)

    if answerable:
        fr = fact_recall(ans, item["key_facts"])
        row["fact_recall"] = fr
        row["correct"] = fr == 1.0
        row["false_refusal"] = refused and fr < 1.0
    else:
        row["fact_recall"] = float("nan")
        row["correct"] = refused           # the right behaviour is to decline
        row["false_refusal"] = False

    cited = result.get("citations", [])
    gold = set(item["gold_doc_ids"])
    row["n_citations"] = len(cited)
    row["n_invalid_citations"] = len(result.get("invalid_citations", []))
    row["citation_precision"] = (len(set(cited) & gold) / len(cited)) if (answerable and cited) else float("nan")
    row["citation_recall"] = (len(set(cited) & gold) / len(gold)) if answerable else float("nan")

    sources = result.get("sources", [])
    if answerable and sources:
        row.update({f"ret_{k}": v for k, v in retrieval_scores([s["doc_id"] for s in sources], item["gold_doc_ids"],
                                                               ks=(len(sources),)).items()})
        row["gold_in_context"] = bool(set(s["doc_id"] for s in sources) & gold)
    else:
        row["gold_in_context"] = None
    row["error_type"] = attribute_error(row)
    return row


def attribute_error(row: dict) -> str:
    """Locate where a wrong answer came from, so failures point at the component to fix."""
    if row["correct"]:
        return "ok"
    if not row["answerable"]:
        return "answered_unanswerable"     # should have declined
    if row["gold_in_context"] is False:
        return "retrieval_miss"            # no gold document reached the LLM
    if row["false_refusal"]:
        return "false_refusal"             # evidence was there but model declined
    if row["fact_recall"] > 0:
        return "partial_answer"            # some key facts missing
    return "generation_error"              # evidence retrieved (or no retrieval) but wrong answer


# ----------------------------------------------------------------------------- statistics

def bootstrap_ci(values, n_boot: int = 5000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float, float]:
    v = np.asarray([x for x in values if x == x], dtype=float)  # drop NaN
    if len(v) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = rng.choice(v, size=(n_boot, len(v)), replace=True).mean(axis=1)
    return float(v.mean()), float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))


def mcnemar_exact(a: list[bool], b: list[bool]) -> dict:
    """Exact McNemar test on paired binary outcomes (same questions, two systems)."""
    assert len(a) == len(b)
    a_only = sum(1 for x, y in zip(a, b) if x and not y)
    b_only = sum(1 for x, y in zip(a, b) if y and not x)
    n = a_only + b_only
    p = 1.0 if n == 0 else binomtest(a_only, n, 0.5, alternative="two-sided").pvalue
    return {"a_only_correct": a_only, "b_only_correct": b_only, "p_value": float(p)}


def summarize(rows: list[dict]) -> dict:
    """Aggregate metrics with 95% bootstrap confidence intervals."""
    ans = [r for r in rows if r["answerable"]]
    una = [r for r in rows if not r["answerable"]]

    def ci(vals):
        m, lo, hi = bootstrap_ci(vals)
        return {"mean": m, "ci_low": lo, "ci_high": hi, "n": sum(1 for x in vals if x == x)}

    lat = np.array([r["latency_s"] for r in rows])
    out = {
        "n_questions": len(rows),
        "overall_accuracy": ci([float(r["correct"]) for r in rows]),
        "answer_accuracy": ci([float(r["correct"]) for r in ans]),
        "fact_recall": ci([r["fact_recall"] for r in ans]),
        "refusal_accuracy_unanswerable": ci([float(r["refused"]) for r in una]),
        "false_refusal_rate": ci([float(r["false_refusal"]) for r in ans]),
        "unsupported_number_rate": ci([float(r["has_unsupported_number"]) for r in rows]),
        "citation_precision": ci([r["citation_precision"] for r in ans]),
        "citation_recall": ci([r["citation_recall"] for r in ans]),
        "answers_with_citation": ci([float(r["n_citations"] > 0) for r in ans]),
        "fabricated_citation_rate": ci([float(r["n_invalid_citations"] > 0) for r in ans]),
        "latency_p50_s": float(np.percentile(lat, 50)),
        "latency_p95_s": float(np.percentile(lat, 95)),
        "by_category": {},
        "error_types": {},
    }
    for cat in sorted({r["category"] for r in rows}):
        cr = [r for r in rows if r["category"] == cat]
        out["by_category"][cat] = ci([float(r["correct"]) for r in cr])
    for r in rows:
        out["error_types"][r["error_type"]] = out["error_types"].get(r["error_type"], 0) + 1
    return out

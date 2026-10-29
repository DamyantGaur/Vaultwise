# Vaultwise - Evaluation Results

Questions: 76 (factual: 30, paraphrase: 20, multi_doc: 10, unanswerable: 16). Default generator: `llama3.2:3b`. Values are means with 95% bootstrap confidence intervals.

## 1. Retrieval quality (answerable questions, document level)

| Retriever | Hit@1 | Hit@3 | Hit@4 (used) | Recall@4 | Hit@10 | MRR |
|---|---|---|---|---|---|---|
| bm25 | 85.0% | 93.3% | 95.0% | 93.3% | 96.7% | 0.893 |
| dense | 96.7% | 100.0% | 100.0% | 100.0% | 100.0% | 0.981 |
| hybrid | 93.3% | 98.3% | 98.3% | 98.3% | 100.0% | 0.958 |

Hit@4 by question category:

| Retriever | factual | paraphrase | multi_doc |
|---|---|---|---|
| bm25 | 100.0% | 85.0% | 100.0% |
| dense | 100.0% | 100.0% | 100.0% |
| hybrid | 100.0% | 95.0% | 100.0% |

Chunking ablation (Hit@1 / Recall@4; `section` = heading-aware with title > section prefix, `fixed` = naive word windows, `document` = whole file):

| Chunking (words/overlap) | # chunks | mean words | BM25 | Dense | Hybrid |
|---|---|---|---|---|---|
| section 120/30 | 116 | 36 | 85.0% / 93.3% | 96.7% / 100.0% | 93.3% / 98.3% |
| section 40/10 | 138 | 33 | 85.0% / 94.2% | 96.7% / 100.0% | 91.7% / 98.3% |
| fixed 40/10 | 126 | 38 | 86.7% / 94.2% | 96.7% / 97.5% | 93.3% / 97.5% |
| fixed 80/20 | 65 | 72 | 85.0% / 94.2% | 93.3% / 99.2% | 91.7% / 98.3% |
| fixed 150/30 | 37 | 116 | 83.3% / 92.5% | 90.0% / 96.7% | 90.0% / 98.3% |
| document | 18 | 207 | 83.3% / 95.0% | 86.7% / 97.5% | 86.7% / 98.3% |

## 2. End-to-end answer quality

| System | Overall acc. | Answerable acc. | Key-fact recall | Correct refusal (unanswerable) | False refusal | Unsupported-number rate | Citation precision | p50 / p95 latency |
|---|---|---|---|---|---|---|---|---|
| LLM only (no retrieval) | 18.4% [11-28] | 10.0% [3-18] | 17.9% [10-27] | 50.0% [25-75] | 25.0% [15-37] | 48.7% [38-59] | n/a | 5.6s / 7.2s |
| Vanilla RAG (base paper) | 94.7% [89-99] | 96.7% [92-100] | 98.3% [96-100] | 87.5% [69-100] | 0.0% [0-0] | 9.2% [4-16] | n/a | 10.0s / 13.1s |
| RAG + BM25 | 84.2% [76-92] | 80.0% [70-90] | 82.8% [73-91] | 100.0% [100-100] | 3.3% [0-8] | 2.6% [0-7] | 91.8% [85-97] | 7.9s / 10.8s |
| RAG + dense | 96.1% [91-100] | 95.0% [88-100] | 96.4% [91-100] | 100.0% [100-100] | 0.0% [0-0] | 3.9% [0-9] | 90.3% [84-96] | 8.9s / 12.1s |
| Vaultwise: hybrid RRF + grounded | 97.4% [93-100] | 96.7% [92-100] | 96.7% [92-100] | 100.0% [100-100] | 0.0% [0-0] | 3.9% [0-9] | 93.1% [87-98] | 6.3s / 9.6s |
| LLM only (no retrieval) [llama3.1-8b] | 13.2% [5-21] | 16.7% [8-27] | 23.9% [14-34] | 0.0% [0-0] | 0.0% [0-0] | 65.8% [55-76] | n/a | 11.7s / 14.6s |
| Vaultwise: hybrid RRF + grounded [llama3.1-8b] | 96.1% [91-100] | 95.0% [88-100] | 95.0% [88-100] | 100.0% [100-100] | 3.3% [0-8] | 5.3% [1-11] | 97.4% [94-100] | 18.4s / 26.6s |

Citation hygiene (answerable questions; RAG systems only):

| System | Answers with >=1 valid citation | Citation precision | Citation recall | Answers citing a non-existent doc id |
|---|---|---|---|---|
| Vanilla RAG (base paper) | 0.0% [0-0] | n/a | 0.0% [0-0] | 0.0% [0-0] |
| RAG + BM25 | 91.7% [83-98] | 91.8% [85-97] | 86.1% [77-94] | 6.7% [2-13] |
| RAG + dense | 88.3% [80-95] | 90.3% [84-96] | 86.1% [77-94] | 5.0% [0-12] |
| Vaultwise: hybrid RRF + grounded | 85.0% [75-93] | 93.1% [87-98] | 83.3% [73-92] | 11.7% [5-20] |
| Vaultwise: hybrid RRF + grounded [llama3.1-8b] | 96.7% [92-100] | 97.4% [94-100] | 96.1% [91-100] | 0.0% [0-0] |

Accuracy by category:

| System | factual | paraphrase | multi_doc | unanswerable |
|---|---|---|---|---|
| LLM only (no retrieval) | 13.3% | 10.0% | 0.0% | 50.0% |
| Vanilla RAG (base paper) | 100.0% | 90.0% | 100.0% | 87.5% |
| RAG + BM25 | 100.0% | 60.0% | 60.0% | 100.0% |
| RAG + dense | 96.7% | 100.0% | 80.0% | 100.0% |
| Vaultwise: hybrid RRF + grounded | 100.0% | 90.0% | 100.0% | 100.0% |
| LLM only (no retrieval) [llama3.1-8b] | 23.3% | 10.0% | 10.0% | 0.0% |
| Vaultwise: hybrid RRF + grounded [llama3.1-8b] | 100.0% | 85.0% | 100.0% | 100.0% |

## 3. Paired significance (exact McNemar test on per-question correctness)

| Comparison | n | only A correct | only B correct | p-value |
|---|---|---|---|---|
| A = Vaultwise: hybrid RRF + grounded vs B = LLM only (no retrieval) | 76 | 60 | 0 | 0.0000 |
| A = Vaultwise: hybrid RRF + grounded vs B = Vanilla RAG (base paper) | 76 | 4 | 2 | 0.6875 |
| A = Vaultwise: hybrid RRF + grounded vs B = RAG + BM25 | 76 | 10 | 0 | 0.0020 |
| A = Vaultwise: hybrid RRF + grounded vs B = RAG + dense | 76 | 3 | 2 | 1.0000 |
| A = Vaultwise: hybrid RRF + grounded vs B = LLM only (no retrieval) [llama3.1-8b] | 76 | 64 | 0 | 0.0000 |
| A = Vaultwise: hybrid RRF + grounded vs B = Vaultwise: hybrid RRF + grounded [llama3.1-8b] | 76 | 1 | 0 | 1.0000 |

## 4. Error attribution

| System | ok | retrieval_miss | generation_error | partial_answer | false_refusal | answered_unanswerable |
|---|---|---|---|---|---|---|
| LLM only (no retrieval) | 14 | 0 | 31 | 8 | 15 | 8 |
| Vanilla RAG (base paper) | 72 | 0 | 0 | 2 | 0 | 2 |
| RAG + BM25 | 64 | 3 | 6 | 3 | 0 | 0 |
| RAG + dense | 73 | 0 | 1 | 2 | 0 | 0 |
| Vaultwise: hybrid RRF + grounded | 74 | 1 | 1 | 0 | 0 | 0 |
| LLM only (no retrieval) [llama3.1-8b] | 10 | 0 | 41 | 9 | 0 | 16 |
| Vaultwise: hybrid RRF + grounded [llama3.1-8b] | 73 | 1 | 1 | 0 | 1 | 0 |

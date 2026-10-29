# Vaultwise - Evaluation 2: private company documents

38 new questions on 3 fictional documents; retrieval restricted to the question's document; generator `llama3.2:3b`. `dev_doc` = contract and memo (seen while the document prompt was developed; these questions were not); `held_out` = vendor agreement written only for this test. 95% bootstrap CIs.

| System | Overall acc. | Answerable acc. | Correct refusal | False refusal | Unsupported-number rate | Held-out doc acc. | p50 latency |
|---|---|---|---|---|---|---|---|
| no_search | 15.8% [5-29] | 6.1% [0-15] | 80.0% [40-100] | 78.8% [64-91] | 7.9% [0-18] | 20.0% [0-40] | 3.0s |
| vanilla_rag | 97.4% [92-100] | 100.0% [100-100] | 80.0% [40-100] | 0.0% [0-0] | 2.6% [0-8] | 93.3% [80-100] | 8.3s |
| vaultwise | 100.0% [100-100] | 100.0% [100-100] | 100.0% [100-100] | 0.0% [0-0] | 5.3% [0-13] | 100.0% [100-100] | 6.4s |

Accuracy by category and split:

| System | factual | paraphrase | general_rule | unanswerable | dev_doc | held_out |
|---|---|---|---|---|---|---|
| no_search | 4.3% | 14.3% | 0.0% | 80.0% | 13.0% | 20.0% |
| vanilla_rag | 100.0% | 100.0% | 100.0% | 80.0% | 100.0% | 93.3% |
| vaultwise | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Paired significance (exact McNemar, Vaultwise vs baseline):

| Comparison | n | only Vaultwise correct | only baseline correct | p |
|---|---|---|---|---|
| Vaultwise vs vanilla_rag | 38 | 1 | 0 | 1.0000 |
| Vaultwise vs no_search | 38 | 32 | 0 | 0.0000 |

## Whole-document summaries

Key-fact coverage = share of 8 pre-defined facts per document present in the summary; unsupported numbers = numbers in the summary that do not appear in the document.

| Document | Model | Key-fact coverage | Unsupported numbers | Latency |
|---|---|---|---|---|
| contract | llama3.2:3b | 87.5% | none | 46s |
| memo | llama3.2:3b | 87.5% | none | 33s |
| vendor | llama3.2:3b | 100.0% | none | 45s |
| contract | llama3.1:8b | 87.5% | none | 106s |
| memo | llama3.1:8b | 100.0% | none | 66s |
| vendor | llama3.1:8b | 100.0% | none | 91s |
| **mean** | llama3.2:3b | 91.7% | 0 total | 41s |
| **mean** | llama3.1:8b | 95.8% | 0 total | 88s |

## Manual audit of the Vaultwise answers (`results/private_audit.csv`)

- Facts correct (human judgement): 38/38 (agrees with the automatic scorer on every question)
- Answers that name a clause or section: 19/33 answerable
- Named clause is the right one: 15/19; wrong: c07 (says the allowance is in 4. Compensation; it is in 6. Benefits (also lists two irrelevant clauses first)); n04 (invents sub-clause 3.2; the memo has section 3 only); n06 (cites 2. Timeline; the fact is in 1. Purpose); v13 (invents sub-clause 10.1; the agreement has clause 10 only)

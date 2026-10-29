# Vaultwise — private answers from your company documents

Companies share long documents with their employees: contracts, policies, project briefs, vendor
agreements, confidential memos. Nobody has time to read them end to end, and many of them must not be
pasted into online AI tools. **Vaultwise** lets you add those documents to a private vault on your own
computer and **find the specific information you need in seconds**. It answers only from your documents,
shows the exact passage each answer came from, gives whole-document summaries, and says plainly when a
document does not contain the answer instead of guessing.

**Nothing leaves your computer.** The AI models run locally in [Ollama](https://ollama.com) (`llama3.2:3b`
for answers, `llama3.1:8b` for summaries, `nomic-embed-text` for search). Documents are stored outside the
cloud-synced project folder, questions about them are not logged, and the app refuses to use a model server on
another machine. It runs on an ordinary laptop CPU; no GPU or internet connection is needed once the models
are downloaded.

| Search method (in the app) | What happens to your answer |
|---|---|
| **Hybrid** (recommended) | keyword and meaning search combined; the most reliable answers, quoting and citing your document |
| **Semantic** | finds the same meaning in other words ("pay" finds "salary"); may miss exact codes or numbers |
| **Keyword** | finds your exact words, names, clause numbers and amounts; can miss reworded questions |
| **No search** (baseline) | the AI does not read your documents and answers from memory; usually cannot answer or is wrong, so it is for comparison only |

> **Name.** The project was developed as *PolicyPilot* and renamed *Vaultwise* when its focus moved from
> company-policy Q&A to a private vault for any company document. The evaluated method is unchanged; the two
> evaluated prompts keep the original name so the results below stay exactly reproducible.

The method was evaluated as a research study on a fictional company's policy set ("Veridian Systems", shipped
in `data/corpus/` and available in the app as *Demo: sample company policies*):

**Base paper:** Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS 2020).
Its RAG design retrieves passages with a single dense retriever, always generates an answer, and gives no
sources. **Vaultwise improves on it in three measured ways:** (1) hybrid BM25 + dense retrieval fused
with Reciprocal Rank Fusion (Cormack et al., SIGIR 2009), (2) explicit abstention when the documents do not
contain the answer, and (3) validated document citations.

**Research question.** *Compared with the base-paper RAG setup and with an LLM without retrieval, does
Vaultwise give answers to employee policy questions that are equally correct and more trustworthy
(correct refusals, fewer invented facts, verifiable citations) at helpdesk-acceptable latency?*

### Results at a glance (76 questions, `llama3.2:3b`, CPU-only laptop)

| System | Overall accuracy | Correct refusal (unanswerable) | Answers with invented numbers | Answers with a citation | Median latency |
|---|---|---|---|---|---|
| LLM without retrieval | 18.4% | 50.0% | 48.7% | – | 5.6 s |
| Vanilla RAG (base paper) | 94.7% | 87.5% | 9.2% | 0% | 10.0 s |
| **Vaultwise** | **97.4%** | **100%** | **3.9%** | **85%** | **6.3 s** |

Vaultwise is significantly better than no retrieval (McNemar p < 0.0001) and BM25-only RAG (p = 0.002).
Against the base paper, answer accuracy is equal (96.7% on answerable questions, p = 0.69); the gain is in
**trustworthiness**: every unanswerable question is declined, invented numbers are more than halved, and
answers cite their source. The automatic scorer agrees with manual labels on 98.3% of 60 audited answers (κ = 0.96).

**Evaluation 2: private company documents** (contract, confidential memo, and a held-out vendor agreement; 38 new questions):

| System | Overall accuracy | Correct refusal | Held-out document | Summary key-fact coverage |
|---|---|---|---|---|
| No document search | 15.8% | 80% | 20% | – |
| Vanilla RAG (base paper) | 97.4% | 80% | 93.3% | – |
| **Vaultwise** | **100%** | **100%** | **100%** | 95.8% (8B), 91.7% (3B) |

A manual audit confirms the facts in all 38 Vaultwise answers; 4 of its 19 clause references are wrong or invented,
a limitation discussed in the report.

The full write-up (method, results, failure analysis, limitations) is in **[docs/REPORT.md](docs/REPORT.md)**.
Generated numbers are in [results/results.md](results/results.md) and every failure is listed in
[results/failures.md](results/failures.md).

---

## Architecture

```
                    ┌────────────── offline: indexing ──────────────┐
 data/corpus/*.md ──► load ──► section-aware chunking ──► BM25 index   │
                    │        (title > section header,  └► nomic-embed ─► embeddings.npy
                    │         120 words, 30 overlap)       (cached, auto-rebuilt on change)
                    └────────────────────────────────────────────────┘

 question ──► BM25 top-20 ─┐
          └─► dense top-20 ─┴─► Reciprocal Rank Fusion ─► top-4 chunks
                                                            │
             grounded prompt (cite [doc-id], refuse if absent) ▼
                                         llama3.2:3b (Ollama, T=0, seed 42)
                                                            │
                     answer + citations + refusal flag + sources + latency
                                                            │
                FastAPI  /ask  /feedback  /documents  /health  /admin/reindex
                web UI at /  ·  audit log logs/queries.jsonl  ·  feedback log
```

| Component | File |
|---|---|
| Document loading, section-aware chunking | [src/vaultwise/ingest.py](src/vaultwise/ingest.py) |
| BM25, dense, hybrid (RRF) retrieval; cached index | [src/vaultwise/retrieval.py](src/vaultwise/retrieval.py) |
| Ollama client (chat + embeddings) | [src/vaultwise/llm.py](src/vaultwise/llm.py) |
| Prompting, citation parsing, refusal detection | [src/vaultwise/pipeline.py](src/vaultwise/pipeline.py) |
| REST API + audit/feedback logging | [src/vaultwise/api.py](src/vaultwise/api.py) |
| Web UI | [src/vaultwise/static/index.html](src/vaultwise/static/index.html) |
| Metrics, bootstrap CIs, McNemar test, error attribution | [src/vaultwise/metrics.py](src/vaultwise/metrics.py) |
| Experiment runner / report generator | [eval/run_eval.py](eval/run_eval.py), [eval/report.py](eval/report.py) |
| Evaluation set (76 labelled questions) | [data/eval/questions.jsonl](data/eval/questions.jsonl) |
| All settings | [config.yaml](config.yaml) |

---

## Quick start

**Windows, one command** (full step-by-step guide: [RUN_GUIDE.md](RUN_GUIDE.md)). From the project folder:

```powershell
.\run.bat
```

It checks Python and the packages, starts Ollama if needed, downloads missing models the first time, starts
Vaultwise on `127.0.0.1:8000` and opens the browser. That one command is all it takes; nothing else needs to be
installed or started.

**Manual / macOS / Linux.** Prerequisites: Python 3.10+, [Ollama](https://ollama.com/download).

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull llama3.1:8b        # optional: more accurate summaries

pip install -r requirements.txt

# build the index (≈20 s; cached afterwards and rebuilt automatically when documents change)
cd src
python -m vaultwise.cli index

# ask from the command line
python -m vaultwise.cli ask "I left my laptop in a taxi. What should I do?"

# start the API + web UI on http://localhost:8000 (from the project root)
cd ..
python -m uvicorn vaultwise.api:app --app-dir src --port 8000
```

Open <http://localhost:8000> for the web UI or <http://localhost:8000/docs> for interactive API docs.

### Continuous integration (GitHub Actions)

Every push and pull request runs `.github/workflows/ci-cd.yml` on GitHub:

1. **Test:** lint (ruff), 39 unit/API tests, and an **AI quality gate** (`eval/quality_gate.py`). The gate
   re-scores the stored evaluation answers with the current code and fails if accuracy, refusals, citation
   precision or the margin over the no-retrieval baseline drop below set thresholds.
2. **Start-up check:** installs the app the way a user does, starts the server, and checks that the API and
   dashboard respond.

A failing stage marks the commit red on GitHub, so a broken or lower-quality change is caught before it's used.
Vaultwise is deployed by running it locally (`run.bat`), which keeps confidential documents on the user's computer.

### Competitors

24 products in four groups (cloud assistants, enterprise search, local document AI, contract AI), with verified
pricing and data handling: [docs/COMPETITORS.md](docs/COMPETITORS.md). The closest are Kotaemon, AnythingLLM and
Open WebUI. Vaultwise's difference is the combination: local, strict refusals, clause citations, hybrid search,
and published trust measurements.

### API

```bash
curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
     -d '{"question": "What is the per diem for international travel?", "mode": "hybrid"}'
```

Response (abridged):

```json
{
  "answer": "The per diem for international travel is USD 75 per day [fin-travel-policy].",
  "refused": false,
  "citations": ["fin-travel-policy"],
  "sources": [{"chunk_id": "fin-travel-policy#4", "section": "Per Diem", "score": 0.0328, "text": "..."}],
  "latency_s": {"retrieval": 0.31, "generation": 3.9, "total": 4.2},
  "query_id": "6f0c..."
}
```

| Endpoint | Purpose |
|---|---|
| `POST /ask` | `{question, mode: hybrid\|dense\|bm25\|none, top_k?, doc_ids?}` → answer, citations, sources, refusal flag, latency. `doc_ids` restricts answers to those documents |
| `POST /feedback` | `{query_id, helpful, comment}` — thumbs up/down from the UI, appended to `logs/feedback.jsonl` |
| `GET /documents` | indexed documents, chunk counts, category, and whether each is private |
| `GET /documents/{doc_id}` | read back the stored text of one of your private documents |
| `POST /documents/{doc_id}/summary` | `{focus?}` → whole-document summary (also triggered by "summarise …" in `/ask` with one document selected) |
| `POST /documents/upload` | multipart form: `file` (PDF, DOCX, TXT, MD; max 10 MB) or `text`, plus `title` and `category` (Contract, Company policy, Confidential document, Other) → indexed in seconds |
| `DELETE /documents/{doc_id}` | remove an uploaded document (`user-…` ids only; policies cannot be deleted) |
| `GET /health` | Ollama reachability, index status, model names, privacy status |
| `POST /admin/reindex` | re-read the corpus after documents change (header `x-admin-key` if `VAULTWISE_ADMIN_KEY` is set) |

---

## Your private documents: contracts, company policies, confidential files

The web UI's **Your private documents** section is a personal, offline document assistant. You can add:

- your **contract** (offer letter, employment agreement, NDA),
- **company policies** your employer shared with you (travel, leave, IT, code of conduct),
- **confidential documents** that the company does not allow you to upload to online tools
  (internal memos, project briefs, client documents you are authorised to keep),

and then, whenever you want:

| You want to | How |
|---|---|
| Ask a question | choose *Answer from: Only <document>* and type it. The answer comes only from that document, names the clause or section used, and says so when the document does not cover it |
| Get a summary | choose the document and type "summarise this" or "key points" in the chat box, or click **Summarise**. The **whole** document is read (long ones in parts, then merged), and the summary gives an Overview, Key points with section names, and Watch out for (deadlines, prohibitions, penalties) |
| Read it again | click **View** to see the stored text |
| Compare with policy | choose *All documents* (e.g. your contract gives 21 leave days, the company policy 24) |
| Remove it | click **Delete**: the file, its index entries and its embeddings are removed |

Supported: PDF, DOCX, TXT, MD (max 10 MB) or pasted text. Clause headings such as `10. Termination and
Notice Period`, `Clause 7 - Confidentiality` or ALL-CAPS titles become sections. Scanned PDFs need OCR first.

### Privacy: how confidential documents stay on this computer

| Risk | What Vaultwise does |
|---|---|
| Sending text to an online AI service | All models run locally in Ollama. The app **refuses to start** if `ollama.base_url` is not on this machine, unless `privacy.allow_remote_llm: true` is set (only for a server inside your company network) |
| Cloud sync (this project is in OneDrive) | Uploads, the search index (which contains document text) and logs live in `~/.vaultwise/` (`C:\Users\<you>\.vaultwise`), **outside** OneDrive. Change it with `VAULTWISE_DATA_DIR` |
| Logs | Questions and answers that touch your private documents are logged as metadata only: no question, answer or document name (`privacy.log_private_text: false`) |
| Other people on the network | `uvicorn` listens on `127.0.0.1` by default, so only this computer can open the app |
| External web resources | The web page loads no CDN scripts, fonts or trackers |
| Mixing with the evaluation | Evaluation runs use a separate index and never read your documents |

The web page shows the current privacy status at the top (model location, storage folder, logging).
These protections cover this software; whether you may keep a document at all is decided by your company's policy.

Summaries use `llama3.1:8b` (`generation.summary_model`). On the sample memo the 3B model invented a date
("30 March 2027" where the memo says only "March 2027"), while the 8B summary was accurate. That makes a summary
take about 1.5 minutes instead of 40 s. Answers to questions stay on the faster 3B model. Summaries are
AI-generated, so check important dates and amounts with **View** before relying on them.

Try it with the two fictional samples:

- [samples/sample-employment-contract.txt](samples/sample-employment-contract.txt): "What is my notice period?" →
  60 days (clause 10); "Is there a non-compete clause?" → no, only a 12-month non-solicitation clause (9);
  "Is there a gym allowance?" → declined, even though the company policy has one.
- [samples/sample-confidential-memo.txt](samples/sample-confidential-memo.txt) (category *Confidential document*):
  "Summarise this"; "What do I have to do and by when?" → inventory by 15 Dec 2026, training on 12 Nov 2026;
  "Can I use ChatGPT to rewrite this memo?" → no, under the ban on public AI chatbots (section 5).

> Uploads are not authenticated unless `VAULTWISE_ADMIN_KEY` is set (the UI then asks for the key). For a
> shared company deployment, put the app behind SSO and give each employee access only to their own documents.

---

## Using it in a company

1. Replace the files in `data/corpus/` with your own policies as `.md` or `.txt` (one file per policy; the
   file name becomes the citation id, `##` headings become sections). Exports from Confluence, SharePoint or
   Google Docs as Markdown work directly.
2. Call `POST /admin/reindex` (or restart). The index fingerprint changes and embeddings are rebuilt.
3. Put the API behind your SSO reverse proxy; point a Slack/Teams bot or the intranet at `/ask`.
4. Review `logs/queries.jsonl` and `logs/feedback.jsonl` weekly: refused questions reveal missing
   documentation; thumbs-down answers become new rows in `data/eval/questions.jsonl`, so the evaluation
   grows with real traffic and every change is re-tested before release.
5. Re-run the evaluation (below) whenever you change the model, prompt, chunking or documents.

---

## Reproducing the evaluation

```bash
python -m pytest -q                                   # 39 unit tests (no Ollama needed)

# Evaluation 1 - company-policy benchmark (76 questions)
python eval/run_eval.py retrieval                     # retrieval metrics + chunking ablation (~15 min on CPU embeddings)
python eval/run_eval.py generate                      # 5 systems x 76 questions with llama3.2:3b (~55 min, CPU-only laptop)
python eval/run_eval.py generate --systems llm_only,rag_hybrid --model llama3.1:8b   # model ablation
python eval/report.py                                 # tables, figures, significance tests, failures
python eval/audit.py score                            # automatic scorer vs manual labels

# Evaluation 2 - private company documents (38 questions on 3 documents, one held out)
python eval/run_private_eval.py answers               # Vaultwise vs vanilla RAG vs no search (~20 min)
python eval/run_private_eval.py summaries             # whole-document summaries, 3B vs 8B (~8 min)
python eval/run_private_eval.py report                # results/private_results.md, private_failures.md
```

All generation uses temperature 0 and a fixed seed; `results/run_metadata.json` records the configuration,
Python/OS versions and the exact Ollama model digests. Raw model outputs are kept in `results/runs/*.jsonl`,
so every metric can be recomputed (or re-scored with a different scorer) without re-running the LLM.

## Project structure

```
run.bat / run.ps1           one-command launcher (see RUN_GUIDE.md)
config.yaml                 all hyper-parameters and privacy settings
data/corpus/                18 policy documents of a fictional company (Veridian Systems; evaluation 1 + demo)
data/eval/questions.jsonl   76 labelled policy questions (factual, paraphrase, multi-doc, unanswerable)
data/eval/private_questions.jsonl  38 labelled questions on the 3 sample documents (evaluation 2)
samples/                    fictional contract, confidential memo and vendor agreement
src/vaultwise/              application package (ingest, documents, retrieval, llm, pipeline, api, metrics, cli)
eval/                       experiment runners (run_eval, run_private_eval), report generator, scorer audit
tests/                      unit + API tests with a fake LLM
results/                    raw runs, tables, failure lists, per-question CSV, figures (both evaluations)
docs/REPORT.md              project report
docs/COMPETITORS.md         competitor analysis with sources
RUN_GUIDE.md                how to start Vaultwise from the terminal
.github/workflows/ci-cd.yml the CI pipeline: lint + tests + quality gate -> app start-up check
eval/quality_gate.py        the AI quality thresholds the pipeline enforces
```

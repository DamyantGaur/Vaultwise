"""Question answering: retrieval -> grounded prompt -> local LLM -> citation and refusal parsing.

mode="none" is the no-retrieval baseline: the same LLM answers from its own parametric knowledge.
"""

from __future__ import annotations

import re
import time

from .config import check_private_endpoint
from .ingest import load_all_documents, split_sections
from .llm import Embedder, OllamaClient, OllamaError
from .retrieval import Index

MODES = ("none", "bm25", "dense", "hybrid")

# RAG_SYSTEM_PROMPT and BASELINE_SYSTEM_PROMPT are the prompts evaluated in docs/REPORT.md on the sample company
# "Veridian Systems". They are kept verbatim (including the project's original name) so those results stay
# reproducible. Questions about the user's own documents use DOCUMENT_SCOPE_PROMPT below.
RAG_SYSTEM_PROMPT = """You are PolicyPilot, the internal helpdesk assistant of Veridian Systems.
Answer the employee's question using ONLY the context passages below. Each passage starts with its
document id in square brackets.
Rules:
1. Every fact you state must come from the context. Do not use outside knowledge or guess.
2. After each sentence, cite the document id in square brackets, e.g. [hr-leave-policy]. Never cite by number.
3. Include the exact numbers, limits and deadlines from the context.
4. If the context does not contain the answer, reply with exactly: "{refusal}"
5. Be concise: at most 4 sentences."""

BASELINE_SYSTEM_PROMPT = """You are PolicyPilot, the internal helpdesk assistant of Veridian Systems.
Answer the employee's question about company policy.
If you do not know the company-specific answer, reply with exactly: "{refusal}"
Be concise: at most 4 sentences."""

# Base-paper style (Lewis et al., 2020): condition the generator on retrieved passages and answer.
# No abstention rule and no citation requirement - the two things Vaultwise adds.
VANILLA_RAG_SYSTEM_PROMPT = """You are the internal helpdesk assistant of Veridian Systems.
Answer the employee's question using the context passages below.
Be concise: at most 4 sentences."""

PROMPT_STYLES = ("grounded", "vanilla")

# Used when the user restricts answers to their own private documents (a contract, a company policy shared
# with them, a confidential report...). Same grounding and refusal rules as RAG_SYSTEM_PROMPT; the citation
# example uses the real document id (a small model copies the example id otherwise) and the answer must name
# the clause or section it relies on.
DOCUMENT_REFUSAL = "I don't have enough information in your document to answer that."
DOCUMENT_SCOPE_PROMPT = """You are Vaultwise, a private assistant that answers questions about documents the
user added, such as contracts, company policies or confidential reports. Use ONLY the context passages below;
each starts with its document id in square brackets and contains a clause or section heading.
Rules:
1. Every fact you state must come from the context. Do not use outside knowledge or guess.
2. Name the clause or section your answer comes from, and cite the document id, e.g. [{example}].
3. Include the exact numbers, amounts, periods and dates from the context.
4. If a general rule in the context covers the question, apply it and say which rule (for example, a ban on
   "external tools" or "public AI chatbots" covers any named chatbot or app). But a clause on a different
   subject is not the same thing (for example, a non-solicitation clause is not a non-compete clause): then
   say the document does not contain it. If nothing relevant is in the context, reply with exactly: "{refusal}"
5. Be concise: at most 4 sentences."""

# "No document search" baseline in the app: the model sees no document text at all.
NO_SEARCH_PROMPT = """You are Vaultwise. You have NO access to the user's documents in this mode; answer only
from general knowledge. If the question is about a specific document, company, person or contract, reply with
exactly: "{refusal}" Be concise: at most 4 sentences."""

SUMMARY_PROMPT = """You summarise a private document for the person who owns it. Use ONLY the document
text below; do not add outside knowledge. {focus}
Write:
- Overview: 1-2 sentences on what the document is and who it concerns.
- Key points: up to 8 bullets with the exact numbers, amounts, dates, periods and obligations,
  each ending with the full section heading it comes from in parentheses, e.g. (3. Budget).
- Watch out for: every deadline, prohibition, penalty or required action in the text, as bullets.
  Write "None" only if the text truly contains none.
Do not invent sections or values that are not in the text."""

COMBINE_PROMPT = """Below are summaries of consecutive parts of one private document. Merge them into a
single summary in the same format (Overview, Key points, Watch out for). Keep exact numbers, dates and
section names; remove duplicates; do not add anything new. {focus}"""

_SUMMARY_RE = re.compile(r"\b(summar(y|ise|ize|ies|ising|izing)|overview|tl;?dr|key points|main points|"
                         r"gist|brief me|outline)\b", re.IGNORECASE)


def is_summary_request(question: str) -> bool:
    return bool(_SUMMARY_RE.search(question))


REFUSAL_PATTERNS = [
    r"(do not|don't|does not|doesn't) have enough information",
    r"not enough information",
    r"(context|documents?|passages?) (do|does) not (contain|mention|provide|specify|include|cover)",
    r"(is|are) not (mentioned|covered|specified|provided|addressed) in the (context|documents?|passages?)",
    r"no information (about|on|regarding)",
    r"no (specific |explicit )?mention of",
    r"(is|are) not (specifically |explicitly )?mentioned",
    # free-form refusals, as produced when no exact refusal sentence is prescribed (vanilla RAG)
    r"no information (is )?(provided|available|given)",
    r"there is no [\w\s-]{1,40}? (specified|mentioned|stated)",
    r"(unable|not able) to (assist|provide|answer|help)",
    r"not (explicitly )?stated",
    r"i'?m not aware of",
    r"i (do not|don't) know",
]
_REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)


def is_refusal(answer: str) -> bool:
    return bool(_REFUSAL_RE.search(answer))


def extract_citations(answer: str, known_doc_ids: list[str],
                      passage_doc_ids: list[str] | None = None) -> tuple[list[str], list[str]]:
    """Return (valid_doc_ids, invalid_tokens) from bracketed citations such as [hr-leave-policy].
    Numeric citations like [2] are resolved to the document of the 2nd context passage."""
    valid, invalid = [], []
    known = set(known_doc_ids)
    passage_doc_ids = passage_doc_ids or []
    shown = set(passage_doc_ids)
    for group in re.findall(r"\[([^\[\]]{1,120})\]", answer):
        for token in re.split(r"[,;]|\s+and\s+", group):
            token = token.strip().strip("'\"`").replace("Source:", "").replace("source:", "").strip()
            token = token.split("|")[0].split("#")[0].strip().lower()
            if token.isdigit() and 1 <= int(token) <= len(passage_doc_ids):
                token = passage_doc_ids[int(token) - 1]
            if not token or token.isdigit():
                continue
            if token in known and (not shown or token in shown):  # must be a document the model was shown
                if token not in valid:
                    valid.append(token)
            elif re.fullmatch(r"[a-z]+-[a-z0-9-]+", token):
                invalid.append(token)  # looks like a doc id but does not exist -> fabricated citation
    return valid, invalid


def format_context(hits) -> str:
    blocks = []
    for h in hits:
        blocks.append(f"[{h.chunk.doc_id}]\n{h.chunk.text}")
    return "\n\n".join(blocks)


class RAGPipeline:
    def __init__(self, cfg: dict, client: OllamaClient | None = None, index: Index | None = None,
                 embedder: Embedder | None = None, log=print):
        check_private_endpoint(cfg)  # never send document text to a model server off this machine
        self.cfg = cfg
        self.client = client or OllamaClient(cfg["ollama"]["base_url"], cfg["ollama"]["timeout_s"])
        e = cfg["embedding"]
        self.embedder = embedder or Embedder(self.client, e["model"], e["query_prefix"], e["document_prefix"],
                                             e["batch_size"])
        self.index = index or Index.build_or_load(cfg, self.embedder, log=log)
        self.refusal = cfg["refusal_message"]

    def reindex(self, log=print, force: bool = False) -> None:
        """Re-read documents. Unchanged chunks reuse their embeddings unless force=True."""
        self.index = Index.build_or_load(self.cfg, self.embedder, force=force, log=log)

    def retrieve(self, question: str, mode: str, top_k: int | None = None, doc_ids=None):
        return self.index.retriever(mode).search(question, top_k or self.cfg["retrieval"]["top_k"], doc_ids)

    def summarize(self, doc_id: str, focus: str | None = None, model: str | None = None) -> dict:
        """Summarise a whole document (not just the top-k passages). Long documents are summarised in
        parts of ~summary_batch_words, and the partial summaries are merged (map-reduce)."""
        doc = next((d for d in load_all_documents(self.cfg) if d.doc_id == doc_id), None)
        if doc is None:
            raise ValueError(f"Unknown document id: {doc_id}")
        g = self.cfg["generation"]
        model = model or g.get("summary_model") or g["model"]
        batch_words = g.get("summary_batch_words", 1500)
        focus_txt = f'The reader asked: "{focus.strip()}". Cover that first.' if focus and focus.strip() else ""
        sections = split_sections(doc.text)
        parts, buf, n = [], [], 0
        for heading, body in sections:
            words = len(body.split())
            if buf and n + words > batch_words:
                parts.append("\n\n".join(buf))
                buf, n = [], 0
            buf.append(f"## {heading}\n{body}")
            n += words
        if buf:
            parts.append("\n\n".join(buf))

        def call(system: str, content: str) -> dict:
            nonlocal model
            messages = [{"role": "system", "content": system}, {"role": "user", "content": content}]
            opts = dict(temperature=g["temperature"], seed=g["seed"], num_ctx=g["num_ctx"],
                        max_tokens=g.get("summary_max_tokens", 600))
            try:
                return self.client.chat(messages, model=model, **opts)
            except OllamaError as e:
                if "not found" not in str(e) or model == g["model"]:
                    raise
                model = g["model"]  # summary model not installed: use the default model
                return self.client.chat(messages, model=model, **opts)

        t0 = time.perf_counter()
        prompt_tokens = completion_tokens = 0
        summaries = []
        for i, part in enumerate(parts, 1):
            label = f" (part {i} of {len(parts)})" if len(parts) > 1 else ""
            out = call(SUMMARY_PROMPT.format(focus=focus_txt), f"Document: {doc.title}{label}\n\n{part}")
            summaries.append(out["text"])
            prompt_tokens += out["prompt_tokens"]
            completion_tokens += out["completion_tokens"]
        while len(summaries) > 1:  # merge four partial summaries at a time so the context never overflows
            merged = []
            for j in range(0, len(summaries), 4):
                group = summaries[j:j + 4]
                if len(group) == 1:
                    merged.append(group[0])
                    continue
                out = call(COMBINE_PROMPT.format(focus=focus_txt),
                           f"Document: {doc.title}\n\n" + "\n\n---\n\n".join(group))
                merged.append(out["text"])
                prompt_tokens += out["prompt_tokens"]
                completion_tokens += out["completion_tokens"]
            summaries = merged
        total = time.perf_counter() - t0
        return {
            "question": focus or f"Summarise {doc.title}",
            "mode": "summary",
            "prompt_style": "summary",
            "doc_filter": [doc_id],
            "model": model,
            "answer": summaries[0].strip(),
            "refused": False,
            "citations": [doc_id],
            "invalid_citations": [],
            "sources": [],
            "summary_of": {"doc_id": doc_id, "title": doc.title, "sections": [h for h, _ in sections],
                           "words": len(doc.text.split()), "parts": len(parts)},
            "latency_s": {"retrieval": 0.0, "generation": round(total, 3), "total": round(total, 3)},
            "tokens": {"prompt": prompt_tokens, "completion": completion_tokens},
        }

    def answer(self, question: str, mode: str | None = None, model: str | None = None,
               top_k: int | None = None, prompt_style: str = "grounded",
               doc_ids: list[str] | None = None) -> dict:
        """doc_ids restricts retrieval to those documents (e.g. only the uploaded contract)."""
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        mode = mode or self.cfg["retrieval"]["default_mode"]
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if prompt_style not in PROMPT_STYLES:
            raise ValueError(f"prompt_style must be one of {PROMPT_STYLES}")
        if doc_ids:
            unknown = set(doc_ids) - set(self.index.doc_ids)
            if unknown:
                raise ValueError(f"Unknown document id(s): {', '.join(sorted(unknown))}")
        doc_filter = set(doc_ids) if doc_ids else None
        scoped = bool(doc_filter) and all(d.startswith("user-") for d in doc_filter)
        g = self.cfg["generation"]
        model = model or g["model"]

        t0 = time.perf_counter()
        hits = [] if mode == "none" else self.retrieve(question, mode, top_k, doc_filter)
        retrieval_s = time.perf_counter() - t0

        if mode == "none":
            # no retrieval: the model never sees any document (baseline, for comparison)
            baseline = (NO_SEARCH_PROMPT.format(refusal=DOCUMENT_REFUSAL) if scoped
                        else BASELINE_SYSTEM_PROMPT.format(refusal=self.refusal))
            messages = [{"role": "system", "content": baseline}, {"role": "user", "content": question}]
        else:
            system = (RAG_SYSTEM_PROMPT.format(refusal=self.refusal) if prompt_style == "grounded"
                      else VANILLA_RAG_SYSTEM_PROMPT)
            if scoped and prompt_style == "grounded":
                system = DOCUMENT_SCOPE_PROMPT.format(refusal=DOCUMENT_REFUSAL,
                                                      example=hits[0].chunk.doc_id if hits else sorted(doc_filter)[0])
            messages = [{"role": "system", "content": system},
                        {"role": "user", "content": f"Context:\n{format_context(hits)}\n\nQuestion: {question}"}]
        out = self.client.chat(messages, model=model, temperature=g["temperature"], seed=g["seed"],
                               num_ctx=g["num_ctx"], max_tokens=g["max_tokens"])
        text = out["text"]
        # drop a bare leading "[doc-id]" or "[doc-id] > Section" line; citations are shown separately
        citations, invalid = extract_citations(text, self.index.doc_ids, [h.chunk.doc_id for h in hits])
        if doc_filter:
            text = re.sub(r"^\s*\[[a-z0-9-]+\][^\n]{0,80}\n+", "", text).strip() or text
        refused = is_refusal(text)
        source_docs = sorted({h.chunk.doc_id for h in hits})
        if doc_filter and not citations and not refused and len(source_docs) == 1:
            citations = source_docs  # the model saw only this document, so the provenance is certain
        return {
            "question": question,
            "mode": mode,
            "prompt_style": prompt_style,
            "doc_filter": sorted(doc_filter) if doc_filter else None,
            "model": model,
            "answer": text,
            "refused": refused,
            "citations": citations,
            "invalid_citations": invalid,
            "sources": [h.to_dict() for h in hits],
            "latency_s": {"retrieval": round(retrieval_s, 4), "generation": round(out["latency_s"], 3),
                          "total": round(time.perf_counter() - t0, 3)},
            "tokens": {"prompt": out["prompt_tokens"], "completion": out["completion_tokens"]},
        }

"""Document loading and section-aware chunking.

Documents are Markdown (or plain text) files; the file stem is the document id used in citations.
Each chunk is prefixed with "<document title> > <section heading>" so that both the lexical and
the dense retriever see the context a bare paragraph would otherwise lose.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".txt"}


@dataclass
class Document:
    doc_id: str
    title: str
    text: str
    path: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    text: str          # text shown to the LLM and used for indexing (includes title/section header)

    def to_dict(self) -> dict:
        return asdict(self)


def load_documents(corpus_dir: str | Path, allow_empty: bool = False) -> list[Document]:
    corpus_dir = Path(corpus_dir)
    if not corpus_dir.is_dir():
        if allow_empty:
            return []
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")
    docs = []
    for path in sorted(corpus_dir.iterdir()):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        title = m.group(1).strip() if m else path.stem.replace("-", " ").title()
        docs.append(Document(doc_id=path.stem, title=title, text=text, path=str(path)))
    if not docs and not allow_empty:
        raise ValueError(f"No .md/.txt documents found in {corpus_dir}")
    return docs


def load_all_documents(cfg: dict) -> list[Document]:
    """Company corpus plus any user-uploaded documents."""
    docs = load_documents(cfg["corpus_dir"])
    if cfg.get("upload_dir"):
        docs += load_documents(cfg["upload_dir"], allow_empty=True)
    return docs


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split Markdown into (heading, body) pairs on '##' headings. Text before the first '##'
    (title line and metadata) becomes an 'Overview' section."""
    sections: list[tuple[str, str]] = []
    heading = "Overview"
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("# "):
            continue  # document title is carried separately
        m = re.match(r"^#{2,6}\s+(.+)$", line)
        if m:
            if " ".join(buf).strip():
                sections.append((heading, "\n".join(buf).strip()))
            heading, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if " ".join(buf).strip():
        sections.append((heading, "\n".join(buf).strip()))
    return sections


def window_words(words: list[str], size: int, overlap: int) -> list[list[str]]:
    if size <= 0:
        raise ValueError("chunk size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must be >= 0 and smaller than chunk size")
    if len(words) <= size:
        return [words]
    step = size - overlap
    windows = []
    for start in range(0, len(words), step):
        windows.append(words[start:start + size])
        if start + size >= len(words):
            break
    return windows


def chunk_documents(docs: list[Document], chunk_size_words: int = 120, overlap_words: int = 30,
                    strategy: str = "section") -> list[Chunk]:
    """strategy="section": split on headings, window long sections, prefix 'title > section'.
    strategy="fixed":   naive baseline - sliding windows over the raw document, no headers.
    strategy="document": one chunk per document."""
    if strategy == "document":
        return [Chunk(f"{d.doc_id}#0", d.doc_id, d.title, "Full document", d.text) for d in docs]
    if strategy == "fixed":
        return [Chunk(f"{d.doc_id}#{i}", d.doc_id, d.title, f"window {i}", " ".join(w))
                for d in docs for i, w in enumerate(window_words(d.text.split(), chunk_size_words, overlap_words))]
    if strategy != "section":
        raise ValueError(f"unknown chunking strategy '{strategy}'")
    chunks = []
    for doc in docs:
        n = 0
        for heading, body in split_sections(doc.text):
            for words in window_words(body.split(), chunk_size_words, overlap_words):
                header = f"{doc.title} > {heading}"
                chunks.append(Chunk(
                    chunk_id=f"{doc.doc_id}#{n}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    section=heading,
                    text=f"{header}\n{' '.join(words)}",
                ))
                n += 1
    return chunks

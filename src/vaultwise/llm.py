"""Thin client for a local Ollama server (chat generation + embeddings).

Running the models locally means no company document or employee question leaves the machine,
which is the main deployment constraint for an internal policy assistant.
"""

from __future__ import annotations

import time

import requests


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", timeout_s: int = 300):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def _post(self, path: str, payload: dict) -> dict:
        try:
            r = requests.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout_s)
        except requests.ConnectionError as e:
            raise OllamaError(f"Cannot reach Ollama at {self.base_url}. Is `ollama serve` running?") from e
        if r.status_code != 200:
            raise OllamaError(f"Ollama {path} returned {r.status_code}: {r.text[:300]}")
        return r.json()

    def is_alive(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/api/tags", timeout=5).status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> dict[str, str]:
        """Return {model_name: digest}, recorded in experiment metadata for reproducibility."""
        r = requests.get(f"{self.base_url}/api/tags", timeout=10)
        r.raise_for_status()
        return {m["name"]: m.get("digest", "") for m in r.json().get("models", [])}

    def embed(self, texts: list[str], model: str) -> list[list[float]]:
        return self._post("/api/embed", {"model": model, "input": texts})["embeddings"]

    def chat(self, messages: list[dict], model: str, temperature: float = 0.0, seed: int = 42,
             num_ctx: int = 4096, max_tokens: int = 300) -> dict:
        t0 = time.perf_counter()
        data = self._post("/api/chat", {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "seed": seed, "num_ctx": num_ctx, "num_predict": max_tokens},
        })
        return {
            "text": data["message"]["content"].strip(),
            "latency_s": time.perf_counter() - t0,
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
        }


class Embedder:
    """Applies the model-specific task prefixes (nomic-embed-text expects them) and batching."""

    def __init__(self, client: OllamaClient, model: str, query_prefix: str = "", document_prefix: str = "",
                 batch_size: int = 32):
        self.client = client
        self.model = model
        self.query_prefix = query_prefix
        self.document_prefix = document_prefix
        self.batch_size = batch_size
        self._query_cache: dict[str, list[float]] = {}

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        out = []
        for i in range(0, len(texts), self.batch_size):
            batch = [self.document_prefix + t for t in texts[i:i + self.batch_size]]
            out.extend(self.client.embed(batch, self.model))
        return out

    def embed_query(self, text: str) -> list[float]:
        # hybrid search embeds the same query once per call; repeated questions are common in helpdesks
        if text not in self._query_cache:
            if len(self._query_cache) > 10_000:
                self._query_cache.clear()
            self._query_cache[text] = self.client.embed([self.query_prefix + text], self.model)[0]
        return self._query_cache[text]

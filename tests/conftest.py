import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vaultwise.config import load_config  # noqa: E402


class FakeClient:
    """Stands in for Ollama: deterministic bag-of-words embeddings and a scripted chat reply."""

    def __init__(self, reply="Employees get 24 days of annual leave [hr-leave-policy]."):
        self.reply = reply
        self.calls = []

    def embed(self, texts, model):
        out = []
        for t in texts:
            v = np.zeros(64)
            for w in t.lower().split():
                v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 64] += 1
            out.append(v.tolist())
        return out

    def chat(self, messages, model, **kw):
        self.calls.append(messages)
        return {"text": self.reply, "latency_s": 0.01, "prompt_tokens": 10, "completion_tokens": 5}

    def is_alive(self):
        return True


@pytest.fixture
def cfg(tmp_path):
    return load_config(overrides={"index_dir": str(tmp_path / "index"), "log_dir": str(tmp_path / "logs"),
                                  "upload_dir": str(tmp_path / "uploads")})  # never touch real uploads


@pytest.fixture
def fake_client():
    return FakeClient()

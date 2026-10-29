"""Configuration loading. Relative paths in the YAML are resolved against the project root;
"{private_dir}" and "~" are expanded so private data can live outside the (cloud-synced) project folder."""

from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yaml"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "ollama"}  # "ollama" = the private docker-compose service


class PrivacyError(RuntimeError):
    pass


def load_config(path: str | os.PathLike | None = None, overrides: dict[str, Any] | None = None) -> dict:
    """Load the YAML config, apply nested overrides, and resolve directory paths."""
    path = Path(path or os.environ.get("VAULTWISE_CONFIG", DEFAULT_CONFIG_PATH))
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if overrides:
        cfg = deep_merge(cfg, overrides)
    if os.environ.get("OLLAMA_BASE_URL"):
        cfg["ollama"]["base_url"] = os.environ["OLLAMA_BASE_URL"]
    private = os.environ.get("VAULTWISE_DATA_DIR") or cfg.get("private_dir") or ".vaultwise"
    cfg["private_dir"] = _resolve(private)
    for key in ("corpus_dir", "upload_dir", "index_dir", "log_dir"):
        if not cfg.get(key):
            cfg[key] = None
            continue
        cfg[key] = _resolve(str(cfg[key]).replace("{private_dir}", cfg["private_dir"]))
    cfg.setdefault("privacy", {"allow_remote_llm": False, "log_private_text": False})
    return cfg


def _resolve(p: str) -> str:
    path = Path(os.path.expandvars(os.path.expanduser(p)))
    return str(path if path.is_absolute() else PROJECT_ROOT / path)


def check_private_endpoint(cfg: dict) -> None:
    """Document text is sent to the model server, so by default it must run on this machine."""
    host = (urlparse(cfg["ollama"]["base_url"]).hostname or "").lower()
    if host not in LOCAL_HOSTS and not cfg.get("privacy", {}).get("allow_remote_llm", False):
        raise PrivacyError(
            f"The model server {cfg['ollama']['base_url']} is not on this machine, so confidential document "
            "text would leave it. Use a local Ollama, or set privacy.allow_remote_llm: true in config.yaml "
            "only if that server is inside your company network.")


def deep_merge(base: dict, overrides: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in overrides.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

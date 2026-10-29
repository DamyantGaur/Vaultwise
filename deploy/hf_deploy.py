"""Deployment helper for the Hugging Face Space (used by the CI/CD pipeline; can also be run by hand).

  python deploy/hf_deploy.py bundle build/space          # assemble the Space's files into a folder
  python deploy/hf_deploy.py deploy build/space          # create/update the Space (needs HF_TOKEN, HF_SPACE)
  python deploy/hf_deploy.py wait                        # wait until it is running, then smoke-test it
  python deploy/hf_deploy.py smoke http://localhost:7860 # smoke-test any running instance (no token needed)

HF_SPACE is "<username>/<space-name>", e.g. "DamyantGaur/vaultwise". HF_TOKEN needs write access.
VAULTWISE_ADMIN_KEY (optional) is stored as a Space secret so only you can upload or delete documents.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = [  # (source relative to ROOT, destination inside the Space)
    ("deploy/huggingface/Dockerfile", "Dockerfile"),
    ("deploy/huggingface/start.sh", "start.sh"),
    ("deploy/huggingface/README.md", "README.md"),
    ("requirements.txt", "requirements.txt"),
    ("config.yaml", "config.yaml"),
    ("src", "src"),
    ("data/corpus", "data/corpus"),
    ("samples", "samples"),
]
SMOKE_QUESTION = {"question": "What is my notice period?", "doc_ids": ["user-my-employment-contract"]}


def _remove(path: Path) -> None:
    """Delete a folder; on Windows, clear read-only flags and retry (OneDrive/antivirus can hold files briefly)."""
    def force(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    for attempt in range(5):
        try:
            shutil.rmtree(path, onerror=force)
            return
        except OSError:
            time.sleep(1 + attempt)
    shutil.rmtree(path, onerror=force)


def bundle(out: Path) -> None:
    if out.exists():
        _remove(out)
    out.mkdir(parents=True)
    for src, dst in BUNDLE:
        s, d = ROOT / src, out / dst
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_dir():
            shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(s, d)
    # shell scripts must keep Unix line endings, whatever git did on Windows
    sh = out / "start.sh"
    sh.write_bytes(sh.read_bytes().replace(b"\r\n", b"\n"))
    print(f"Bundle ready in {out} ({sum(1 for p in out.rglob('*') if p.is_file())} files)")


def space_id() -> str:
    sid = os.environ.get("HF_SPACE", "").strip()
    if "/" not in sid:
        sys.exit("Set HF_SPACE to '<username>/<space-name>'.")
    return sid


def space_url(sid: str) -> str:
    return "https://" + sid.replace("/", "-").replace("_", "-").replace(".", "-").lower() + ".hf.space"


def deploy(folder: Path) -> None:
    from huggingface_hub import HfApi
    token = os.environ.get("HF_TOKEN") or sys.exit("Set HF_TOKEN.")
    sid, api = space_id(), HfApi(token=token)
    api.create_repo(sid, repo_type="space", space_sdk="docker", private=True, exist_ok=True)
    if os.environ.get("VAULTWISE_ADMIN_KEY"):
        api.add_space_secret(sid, "VAULTWISE_ADMIN_KEY", os.environ["VAULTWISE_ADMIN_KEY"])
    sha = os.environ.get("GITHUB_SHA", "manual")[:12]
    api.upload_folder(repo_id=sid, repo_type="space", folder_path=str(folder), delete_patterns="*",
                      commit_message=f"Deploy {sha} from CI/CD")
    print(f"Uploaded to https://huggingface.co/spaces/{sid}; the Space is now building.")


def http(url: str, data: dict | None = None, token: str | None = None, timeout: int = 30):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read().decode() or "{}")


def smoke(base: str, token: str | None = None, wait_s: int = 600) -> None:
    """The deployed app must answer /health, list the sample documents and answer one real question."""
    deadline = time.time() + wait_s
    while True:
        try:
            status, h = http(f"{base}/health", token=token)
            if status == 200 and h.get("ollama_reachable"):
                break
        except (urllib.error.URLError, OSError, ValueError):
            pass
        if time.time() > deadline:
            sys.exit(f"FAIL: {base}/health not ready after {wait_s}s")
        time.sleep(10)
    print(f"health ok: deployment={h.get('deployment')} model={h.get('generation_model')}")
    _, a = http(f"{base}/ask", SMOKE_QUESTION, token=token, timeout=600)
    print(f"answer ({a['latency_s']['total']:.0f}s): {a['answer'][:160]}")
    if "60" not in a["answer"] or a["refused"]:
        sys.exit("FAIL: the deployed app did not answer the smoke question correctly (expected 60 days)")
    print("SMOKE TEST PASSED")


def wait_and_smoke() -> None:
    from huggingface_hub import HfApi
    token = os.environ.get("HF_TOKEN") or sys.exit("Set HF_TOKEN.")
    sid, api = space_id(), HfApi(token=token)
    deadline, stage = time.time() + 45 * 60, None  # first build downloads ~2.5 GB of models
    while time.time() < deadline:
        stage = api.get_space_runtime(sid).stage
        print(f"Space stage: {stage}", flush=True)
        if stage == "RUNNING":
            break
        if stage in ("BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR"):
            sys.exit(f"FAIL: Space is {stage}; see the build logs at https://huggingface.co/spaces/{sid}")
        time.sleep(30)
    else:
        sys.exit(f"FAIL: Space not running after 45 minutes (last stage {stage})")
    smoke(space_url(sid), token=token)
    print(f"Live at {space_url(sid)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "bundle":
        bundle(Path(sys.argv[2] if len(sys.argv) > 2 else "build/space"))
    elif cmd == "deploy":
        deploy(Path(sys.argv[2] if len(sys.argv) > 2 else "build/space"))
    elif cmd == "wait":
        wait_and_smoke()
    elif cmd == "smoke":
        smoke(sys.argv[2].rstrip("/"))
    else:
        sys.exit(__doc__)

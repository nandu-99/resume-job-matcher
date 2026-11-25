"""Fetch only the selected model files from a pinned Hub snapshot."""

import os
from pathlib import Path
import re

from huggingface_hub import snapshot_download


DOWNLOAD_FILES = (
    "config.json", "model.safetensors", "tokenizer.json", "tokenizer_config.json",
)


def provision_model(directory: str | Path) -> None:
    directory = Path(directory)
    if all((directory / name).is_file() for name in DOWNLOAD_FILES):
        return
    repo = os.environ.get("RESUME_MATCHER_HF_REPO", "").strip()
    revision = os.environ.get("RESUME_MATCHER_HF_REVISION", "").strip()
    if not repo:
        return  # Local-only setup retains the existing missing-files error.
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Set a full 40-character model repository commit revision.")
    # Pin the model to an immutable revision and download only inference files.
    snapshot_download(
        repo_id=repo, revision=revision,
        token=os.environ.get("HF_TOKEN") or False,
        allow_patterns=list(DOWNLOAD_FILES), local_dir=directory,
        max_workers=2,
    )

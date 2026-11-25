"""Inference for the DistilBERT checkpoint selected before M4 test evaluation."""

from contextlib import nullcontext
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
from threading import Lock
import unicodedata

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from m5.validation import InputValidationError, validate_inputs
from m5.deployment import provision_model


LABELS = ("Good Fit", "Potential Fit", "No Fit")
MAX_LENGTH = 512
DEFAULT_MODEL_DIR = Path(__file__).parent / "artifacts" / "distilbert_weighted_v1"
SELECTION_PATH = Path(__file__).parents[1] / "m4" / "evaluation" / "model_selection.json"
MODEL_FILES = ("config.json", "model.safetensors", "tokenizer.json", "tokenizer_config.json")

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{8,}\d)(?!\w)")


def prepare_text(text: str) -> str:
    """Apply the original M3 preparation without section selection."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = EMAIL_PATTERN.sub(" email ", text)
    text = URL_PATTERN.sub(" url ", text)
    text = PHONE_PATTERN.sub(
        lambda match: " phone "
        if sum(character.isdigit() for character in match.group()) >= 10
        else match.group(),
        text,
    )
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[^\S\n]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n", text).strip()


def prepare_inputs(resume_text: str, job_text: str) -> tuple[str, str]:
    validate_inputs(resume_text, job_text)
    resume, job = prepare_text(resume_text), prepare_text(job_text)
    for name, text in (("Resume", resume), ("Job description", job)):
        if not text or not any(character.isalnum() for character in text):
            raise InputValidationError(f"{name} must contain text after preparation.")
    return resume, job


def resolve_model_dir(model_dir: str | Path | None = None) -> Path:
    location = model_dir or os.environ.get("RESUME_MATCHER_MODEL_DIR") or DEFAULT_MODEL_DIR
    return Path(location).expanduser().resolve()


class ResumeJobMatcher:
    """Load once and reuse. CPU inference uses FP32; CUDA uses FP16 autocast."""

    def __init__(self, model_dir: str | Path | None = None, device: str = "cpu"):
        self.model_dir = resolve_model_dir(model_dir)
        missing = [name for name in MODEL_FILES if not (self.model_dir / name).is_file()]
        if missing:
            raise FileNotFoundError(
                f"Missing trained model files in {self.model_dir}: {', '.join(missing)}. "
                "Extract distilbert_weighted_v1_model.zip into that folder."
            )

        # Verify the input policy and weight hash against the model selected in M4.
        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        policy = selection["input_policy"]
        if (
            selection["selected_run_id"] != "distilbert_weighted_v1"
            or policy["max_length"] != MAX_LENGTH
            or policy["truncation"] != "longest_first"
            or policy["truncation_side"] != "right"
            or policy["pair_order"] != ["resume", "job"]
        ):
            raise ValueError("The recorded selection does not match this inference policy.")

        with (self.model_dir / "model.safetensors").open("rb") as model_file:
            self.weights_sha256 = hashlib.file_digest(model_file, "sha256").hexdigest()
        if self.weights_sha256 != selection["selected_weights_sha256"]:
            raise ValueError("The checkpoint does not match the frozen M4 selection.")

        self.device = torch.device(device)
        if self.device.type not in {"cpu", "cuda"}:
            raise ValueError("Supported devices are 'cpu' and 'cuda'.")
        if self.device.type == "cuda" and not torch.cuda.is_available():
            raise ValueError("CUDA is unavailable. Use device='cpu'.")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_dir, local_files_only=True, trust_remote_code=False
        )
        self.tokenizer.truncation_side = "right"
        self.tokenizer.padding_side = "right"
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_dir,
            local_files_only=True,
            trust_remote_code=False,
            use_safetensors=True,
            dtype=torch.float32,
        )
        expected_labels = {label: index for index, label in enumerate(LABELS)}
        if (
            self.model.config.model_type != "distilbert"
            or self.model.config.label2id != expected_labels
            or self.model.config.id2label != dict(enumerate(LABELS))
            or self.model.config.max_position_embeddings != MAX_LENGTH
            or self.tokenizer.num_special_tokens_to_add(pair=True) != 3
        ):
            raise ValueError("Model architecture, labels, or input limit do not match M4.")

        self.model.to(self.device).eval()
        self._lock = Lock()

    def predict_match(self, resume_text: str, job_text: str) -> dict:
        resume, job = prepare_inputs(resume_text, job_text)

        # Tokenizer settings are mutable, so shared instances serialise prediction calls.
        with self._lock:
            original_tokens = self.tokenizer.num_special_tokens_to_add(pair=True)
            for text in (resume, job):
                original_tokens += len(self.tokenizer(
                    text, add_special_tokens=False, truncation=False,
                    return_attention_mask=False, return_token_type_ids=False,
                    verbose=False,
                )["input_ids"])

            # Preserve training-time pair order; shorten the longer document to fit 512 tokens.
            inputs = self.tokenizer(
                resume, job,
                add_special_tokens=True,
                truncation="longest_first", max_length=MAX_LENGTH,
                padding=True, pad_to_multiple_of=8,
                return_token_type_ids=False, return_attention_mask=True,
                return_tensors="pt",
            )
            input_tokens = int(inputs["attention_mask"].sum().item())
            inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
            precision = (
                torch.autocast("cuda", dtype=torch.float16)
                if self.device.type == "cuda" else nullcontext()
            )
            # Predict one of the three trained labels without updating model weights.
            with torch.inference_mode(), precision:
                label_id = int(self.model(**inputs).logits.argmax(dim=-1).item())

        return {
            "label": LABELS[label_id],
            "truncated": original_tokens > MAX_LENGTH,
            "input_tokens": input_tokens,
            "original_tokens": original_tokens,
        }


@lru_cache(maxsize=1)
def _cached_matcher(model_dir: str, device: str) -> ResumeJobMatcher:
    provision_model(model_dir)
    return ResumeJobMatcher(model_dir, device=device)


def load_matcher(
    model_dir: str | Path | None = None, *, device: str = "cpu"
) -> ResumeJobMatcher:
    """Reuse one loaded model per process; cache no user inputs or predictions."""
    return _cached_matcher(str(resolve_model_dir(model_dir)), device)


def clear_matcher_cache() -> None:
    """Discard the cached instance so the next request can reload the model."""
    _cached_matcher.cache_clear()


def predict_match(
    resume_text: str, job_text: str, *,
    model_dir: str | Path | None = None, device: str = "cpu",
) -> dict:
    prepare_inputs(resume_text, job_text)
    return load_matcher(model_dir, device=device).predict_match(resume_text, job_text)

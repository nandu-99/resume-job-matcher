"""Guard a matching request and log operational metadata without document text."""

import json
import logging
import time
from uuid import uuid4

from m5.inference import LABELS, MAX_LENGTH, clear_matcher_cache, load_matcher, prepare_inputs
from m5.validation import InputValidationError


LOGGER = logging.getLogger("resume_job_matcher.requests")
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False


class MatchError(RuntimeError):
    def __init__(self, message: str, request_id: str):
        super().__init__(message)
        self.request_id = request_id


class ModelUnavailableError(MatchError):
    """The selected model could not be loaded or verified."""


class PredictionError(MatchError):
    """A model call failed or returned an invalid result."""


def _valid_result(result) -> bool:
    if not isinstance(result, dict):
        return False
    label = result.get("label")
    truncated = result.get("truncated")
    used = result.get("input_tokens")
    original = result.get("original_tokens")
    return (
        label in LABELS
        and type(truncated) is bool
        and type(used) is int
        and type(original) is int
        and 3 <= used <= MAX_LENGTH
        and original >= used
        and truncated == (original > MAX_LENGTH)
        and used == min(original, MAX_LENGTH)
    )


def analyse_match(resume_text: str, job_text: str) -> dict:
    request_id = uuid4().hex[:12]
    started = time.perf_counter()
    resume_chars = len(resume_text) if isinstance(resume_text, str) else None
    job_chars = len(job_text) if isinstance(job_text, str) else None

    # Log timing and counts only, keeping document text and raw exceptions out of logs.
    def record(event, *, truncated=None):
        metadata = {
            "event": event,
            "request_id": request_id,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "resume_chars": resume_chars,
            "job_chars": job_chars,
        }
        if truncated is not None:
            metadata["truncated"] = truncated
        LOGGER.info(json.dumps(metadata, sort_keys=True))

    # Reject invalid requests before spending time loading the model.
    try:
        prepare_inputs(resume_text, job_text)
    except (TypeError, InputValidationError) as error:
        record("validation_failed")
        raise InputValidationError(str(error)) from None

    try:
        matcher = load_matcher(device="cpu")
    except Exception:
        clear_matcher_cache()
        record("model_load_failed")
        raise ModelUnavailableError(
            "The matching model is unavailable. Your text has been kept. "
            "Try Analyse match again; if the problem continues, share the reference with the maintainer.",
            request_id,
        ) from None

    try:
        result = matcher.predict_match(resume_text, job_text)
        if not _valid_result(result):
            raise RuntimeError("Invalid prediction response.")
    except InputValidationError as error:
        record("validation_failed")
        raise InputValidationError(str(error)) from None
    except Exception:
        clear_matcher_cache()
        record("prediction_failed")
        raise PredictionError(
            "We couldn't finish this analysis. Your text has been kept. "
            "Try Analyse match again; if the problem continues, share the reference with the maintainer.",
            request_id,
        ) from None

    record("prediction_completed", truncated=result["truncated"])
    return {key: result[key] for key in ("label", "truncated", "input_tokens", "original_tokens")}

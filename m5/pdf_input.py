"""Bounded PDF extraction in a disposable worker process."""

from dataclasses import dataclass
import json
import subprocess
import sys
from threading import BoundedSemaphore

from m5.validation import MAX_INPUT_CHARACTERS


MAX_PDF_BYTES = 10 * 1024 * 1024
MAX_PDF_PAGES = 10
PDF_TIMEOUT_SECONDS = 60
_EXTRACTION_SLOT = BoundedSemaphore(1)


class PDFInputError(ValueError):
    """A safe PDF error that can be shown without document or system details."""


@dataclass(frozen=True)
class ExtractedPDF:
    text: str
    pages: int
    ocr_pages: tuple[int, ...]
    empty_pages: tuple[int, ...]


def extract_pdf(content: bytes, *, force_ocr: bool = False) -> ExtractedPDF:
    if not _EXTRACTION_SLOT.acquire(blocking=False):
        raise PDFInputError("The PDF reader is busy. Please try again shortly.")
    try:
        return _extract_pdf(content, force_ocr=force_ocr)
    finally:
        _EXTRACTION_SLOT.release()


def _extract_pdf(content: bytes, *, force_ocr: bool = False) -> ExtractedPDF:
    if not isinstance(content, bytes) or not content:
        raise PDFInputError("Choose a PDF containing text or scanned pages.")
    if len(content) > MAX_PDF_BYTES:
        raise PDFInputError("The PDF is too large. Upload a file no larger than 10 MB.")
    if not content[:1024].lstrip().startswith(b"%PDF-"):
        raise PDFInputError("This file is not a readable PDF. Export it as PDF and try again.")
    command = [sys.executable, "-m", "m5.pdf_worker"]
    if force_ocr:
        command.append("--force-ocr")
    try:
        completed = subprocess.run(
            command, input=content, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=PDF_TIMEOUT_SECONDS, check=False,
        )
        response = json.loads(completed.stdout) if completed.returncode == 0 else {}
    except subprocess.TimeoutExpired:
        raise PDFInputError("Reading this PDF took too long. Use fewer pages or paste the text.") from None
    except (OSError, ValueError):
        raise PDFInputError("The PDF reader is unavailable. Try again or paste the text.") from None
    if not isinstance(response, dict):
        raise PDFInputError("The PDF could not be read. Try another PDF or paste the text.")
    if response.get("error"):
        # Only fixed messages from our worker are exposed, never native parser output.
        raise PDFInputError(response["error"])
    text = response.get("text", "")
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_INPUT_CHARACTERS:
        raise PDFInputError("The PDF could not be read. Try another PDF or paste the text.")
    return ExtractedPDF(text, response["pages"], tuple(response["ocr_pages"]), tuple(response["empty_pages"]))

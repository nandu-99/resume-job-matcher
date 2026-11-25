"""Private PDF worker. Document bytes enter stdin; extracted text leaves stdout."""

from contextlib import closing
import io
import json
import math
import os
import subprocess
import sys
import time
import unicodedata

import pypdfium2 as pdfium

from m5.pdf_input import MAX_PDF_BYTES, MAX_PDF_PAGES, PDFInputError
from m5.validation import MAX_INPUT_CHARACTERS


OCR_PAGE_SECONDS = 12
WORK_SECONDS = 45
MAX_RENDER_EDGE = 2200


def clean_text(text):
    return "".join(
        character for character in text
        if unicodedata.category(character) != "Cc" or character in "\n\r\t"
    ).replace("\r\n", "\n").strip()


def needs_ocr(text):
    return sum(character.isalnum() for character in text) < 30 or text.count("\ufffd") > max(2, len(text) * 0.02)


def read_ocr(page, remaining):
    width, height = page.get_size()
    if not all(math.isfinite(value) and value > 0 for value in (width, height)):
        raise PDFInputError("A PDF page has an invalid size. Export the document again.")
    # Bound image dimensions before OCR to limit per-page memory and processing cost.
    scale = min(2.5, MAX_RENDER_EDGE / max(width, height))
    with closing(page.render(scale=scale)) as bitmap:
        with bitmap.to_pil().convert("RGB") as image:
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
    try:
        result = subprocess.run(
            ["tesseract", "stdin", "stdout", "-l", "eng", "--oem", "1", "--psm", "3"],
            input=buffer.getvalue(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=min(OCR_PAGE_SECONDS, max(0.1, remaining)), check=False,
            env={**os.environ, "OMP_THREAD_LIMIT": "1"},
        )
    except FileNotFoundError:
        raise PDFInputError("Scanned-PDF reading is unavailable. Ask the maintainer to install Tesseract, or paste the text.") from None
    except subprocess.TimeoutExpired:
        raise PDFInputError("A scanned page took too long to read. Use a clearer scan, fewer pages, or paste the text.") from None
    if result.returncode:
        raise PDFInputError("Scanned-PDF reading failed. Try a clearer English document or paste the text.")
    return clean_text(result.stdout.decode("utf-8", errors="replace"))


def read_document(content, *, force_ocr=False):
    started = time.monotonic()
    try:
        document = pdfium.PdfDocument(content)
    except Exception:
        raise PDFInputError("The PDF is damaged or password-protected. Upload an unlocked PDF or paste its text.") from None
    with closing(document):
        count = len(document)
        if not 1 <= count <= MAX_PDF_PAGES:
            raise PDFInputError("Upload a PDF with 1 to 10 pages. Split longer documents first.")
        texts, ocr_pages, empty_pages = [], [], []
        characters = 0
        for index in range(count):
            remaining = WORK_SECONDS - (time.monotonic() - started)
            if remaining <= 0:
                raise PDFInputError("Reading this PDF took too long. Use fewer pages or paste the text.")
            with closing(document[index]) as page:
                with closing(page.get_textpage()) as textpage:
                    if textpage.count_chars() > MAX_INPUT_CHARACTERS:
                        raise PDFInputError("The PDF contains too much text. Use at most 50,000 characters.")
                    text = clean_text(textpage.get_text_bounded())
                # Prefer embedded text; use English OCR for scans or explicit user requests.
                if force_ocr or needs_ocr(text):
                    text = read_ocr(page, remaining)
                    ocr_pages.append(index + 1)
                if not any(character.isalnum() for character in text):
                    empty_pages.append(index + 1)
                texts.append(text)
                characters += len(text) + (2 if index else 0)
                if characters > MAX_INPUT_CHARACTERS:
                    raise PDFInputError("The PDF contains too much text. Use at most 50,000 characters.")
        text = "\n\n".join(texts).strip()
        if not any(character.isalnum() for character in text):
            raise PDFInputError("No readable text was found, including after OCR. Use a clearer English scan or paste the text.")
        return {"text": text, "pages": count, "ocr_pages": ocr_pages, "empty_pages": empty_pages}


def main():
    # No document filenames, PDF contents, or native stderr are logged.
    try:
        content = sys.stdin.buffer.read(MAX_PDF_BYTES + 1)
        if not content or len(content) > MAX_PDF_BYTES:
            raise PDFInputError("Upload a PDF no larger than 10 MB.")
        response = read_document(content, force_ocr="--force-ocr" in sys.argv)
    except PDFInputError as error:
        response = {"error": str(error)}
    except Exception:
        response = {"error": "The PDF could not be read. Try another PDF or paste the text."}
    sys.stdout.write(json.dumps(response))


if __name__ == "__main__":
    main()

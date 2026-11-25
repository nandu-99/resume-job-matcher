"""Synthetic PDF/OCR integration and failure checks. No personal documents."""

import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw, ImageFont

from m5.pdf_input import MAX_PDF_BYTES, PDFInputError, _EXTRACTION_SLOT, extract_pdf
from m5.pdf_worker import read_ocr

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.pdfencrypt import StandardEncryption
except ImportError:
    canvas = None


SYNTHETIC_LINE = "Python developer with SQL skills and five years of software experience."


def scan_image():
    image = Image.new("RGB", (1600, 600), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=34)
    draw.text((60, 90), "Python developer", fill="black", font=font)
    draw.text((60, 160), "Skills: Python SQL Docker", fill="black", font=font)
    draw.text((60, 230), "Five years of software experience", fill="black", font=font)
    return image


def make_pdf(*, scan=False, pages=1, encrypted=False, mixed=False):
    stream = io.BytesIO()
    encryption = StandardEncryption("test-only-password") if encrypted else None
    document = canvas.Canvas(stream, pagesize=(612, 792), encrypt=encryption)
    for index in range(pages):
        if scan or (mixed and index == 1):
            with scan_image() as image:
                document.drawImage(ImageReader(image), 20, 400, width=570, height=214)
        else:
            document.drawString(35, 700, SYNTHETIC_LINE)
        document.showPage()
    document.save()
    return stream.getvalue()


class PDFBoundaryTests(unittest.TestCase):
    def test_empty_wrong_type_and_oversized_inputs(self):
        for content in (b"", b"not pdf", b"%PDF-" + b"a" * MAX_PDF_BYTES):
            with self.subTest(size=len(content)), patch("m5.pdf_input.subprocess.run") as runner:
                with self.assertRaises(PDFInputError):
                    extract_pdf(content)
                runner.assert_not_called()

    def test_busy_worker_returns_retry_message(self):
        _EXTRACTION_SLOT.acquire()
        try:
            with self.assertRaisesRegex(PDFInputError, "busy"):
                extract_pdf(b"%PDF-test")
        finally:
            _EXTRACTION_SLOT.release()

    def test_crash_timeout_and_invalid_worker_output_are_safe(self):
        cases = (
            subprocess.CompletedProcess([], 1, b"", b"PRIVATE INTERNAL DETAIL"),
            subprocess.CompletedProcess([], 0, b"invalid json", b"PRIVATE INTERNAL DETAIL"),
        )
        for result in cases:
            with patch("m5.pdf_input.subprocess.run", return_value=result):
                with self.assertRaises(PDFInputError) as raised:
                    extract_pdf(b"%PDF-test")
                self.assertNotIn("PRIVATE", str(raised.exception))
        with patch("m5.pdf_input.subprocess.run", side_effect=subprocess.TimeoutExpired([], 60)):
            with self.assertRaisesRegex(PDFInputError, "too long"):
                extract_pdf(b"%PDF-test")


@unittest.skipIf(canvas is None, "Install m5/requirements-test.txt for synthetic PDF integration checks.")
class PDFIntegrationTests(unittest.TestCase):
    def test_worker_reads_pdf_when_app_is_launched_outside_repository(self):
        repo = Path(__file__).resolve().parent.parent
        script = (
            "import json, sys; "
            f"sys.path.insert(0, {str(repo)!r}); "
            "from m5.pdf_input import extract_pdf; "
            "report = extract_pdf(sys.stdin.buffer.read()); "
            "print(json.dumps({'text': report.text, 'pages': report.pages}))"
        )
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-c", script], input=make_pdf(),
                capture_output=True, cwd=directory, env=env, timeout=70,
            )
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        report = json.loads(result.stdout)
        self.assertEqual(report["pages"], 1)
        self.assertIn(SYNTHETIC_LINE, report["text"])

    def test_embedded_text_needs_no_ocr(self):
        report = extract_pdf(make_pdf())
        self.assertIn(SYNTHETIC_LINE, report.text)
        self.assertEqual(report.pages, 1)
        self.assertEqual(report.ocr_pages, ())

    def test_rejects_page_limit_corruption_and_password(self):
        for content in (make_pdf(pages=11), make_pdf(encrypted=True), b"%PDF-corrupt"):
            with self.assertRaises(PDFInputError):
                extract_pdf(content)

    @unittest.skipUnless(shutil.which("tesseract"), "Install Tesseract with English data for real OCR checks.")
    def test_scanned_and_mixed_pages_use_real_ocr(self):
        for content, expected_pages in ((make_pdf(scan=True), (1,)), (make_pdf(pages=2, mixed=True), (2,))):
            report = extract_pdf(content)
            self.assertIn("python", report.text.lower())
            self.assertIn("sql", report.text.lower())
            self.assertEqual(report.ocr_pages, expected_pages)

    @unittest.skipUnless(shutil.which("tesseract"), "Install Tesseract with English data for real OCR checks.")
    def test_force_ocr_reads_text_based_pdf(self):
        report = extract_pdf(make_pdf(), force_ocr=True)
        self.assertEqual(report.ocr_pages, (1,))
        self.assertIn("python", report.text.lower())

    def test_ocr_installation_errors_and_timeout_are_safe(self):
        from contextlib import closing
        import pypdfium2 as pdfium
        with closing(pdfium.PdfDocument(make_pdf(scan=True))) as document:
            with closing(document[0]) as page:
                for failure in (FileNotFoundError(), subprocess.TimeoutExpired([], 12)):
                    with patch("m5.pdf_worker.subprocess.run", side_effect=failure):
                        with self.assertRaises(PDFInputError):
                            read_ocr(page, 20)
                with patch("m5.pdf_worker.subprocess.run", return_value=subprocess.CompletedProcess(
                    [], 1, b"", b"PRIVATE DOCUMENT DETAIL",
                )):
                    with self.assertRaises(PDFInputError) as raised:
                        read_ocr(page, 20)
                    self.assertNotIn("PRIVATE", str(raised.exception))

    def test_blank_pdf_is_rejected_after_ocr(self):
        with Image.new("RGB", (600, 800), "white") as image:
            stream = io.BytesIO()
            image.save(stream, format="PDF")
        with self.assertRaises(PDFInputError):
            extract_pdf(stream.getvalue())


if __name__ == "__main__":
    unittest.main()

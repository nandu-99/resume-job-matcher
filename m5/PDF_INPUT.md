# PDF upload and scanned-document OCR

Resume and job description each support **Paste text** or **Upload PDF** independently. A PDF resume can be compared with a pasted job description, or both documents can be PDFs.

## Workflow

1. Choose Upload PDF for the relevant input, open Choose PDF, and select a PDF.
2. Select Read PDF. Pages with useful embedded text use that text. Pages with little readable text are rendered and passed to English neural OCR.
3. Review and correct the extracted text, including reading order, skills, dates, and names.
4. Select Analyse match. The existing preparation, input validation, original 512-token policy, and selected DistilBERT checkpoint are applied to the reviewed text.

Open **PDF source** to replace a read document or adjust OCR. Enable **Use OCR on every page** if a PDF has an incomplete or unreadable text layer, such as an embedded heading above an otherwise scanned page. Changing the document, OCR setting, or input method invalidates its extracted text and previous result. Editing reviewed text clears the prediction. Clear and Use an example reset the upload controls and PDF reports.

Unreadable pages are explicitly identified. An entirely unreadable document is rejected. The app does not silently trim oversized documents or treat a reader failure as a match prediction.

## Model choice

The OCR engine is **Tesseract 5 with its public English LSTM language model** (`eng.traineddata`, neural engine `--oem 1`). Automatic page segmentation (`--psm 3`) handles printed page text. The Cloud system packages supply the engine and English model; no second Hugging Face model or OCR API key is needed.

| Public option checked | Fit for this prototype |
|---|---|
| Tesseract English LSTM models | Selected for CPU full-page OCR and straightforward system-package installation. Debian packages normally use the smaller `tessdata_fast` models. |
| Microsoft TrOCR base printed | The published model expects single text-line images. Full resumes would require layout detection and line cropping, plus another transformer runtime workload. |

This is an engineering choice based on documented capabilities, not a measured accuracy comparison between OCR models. Tesseract uses a trained neural OCR model; no OCR or classifier training is added.

Sources: [Tesseract models and trade-offs](https://tesseract-ocr.github.io/tessdoc/Data-Files.html), [neural engine and page segmentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html), [TrOCR model card](https://huggingface.co/microsoft/trocr-base-printed), [PDFium Python API](https://pypdfium2.readthedocs.io/en/stable/python_api.html).

## Bounds and failure handling

- PDF only; maximum 10 MB and 10 pages per input.
- Extracted text must fit the existing 50,000-character bound. Shortening the document is left to the user.
- OCR is intended for English printed scans. Handwriting, rotated pages, unusual fonts, tables, complex columns, and poor scans may be read incorrectly.
- Rendered images have a maximum edge of 2,200 pixels. One page is processed at a time; the app admits one extraction worker per process and asks another caller to retry if it is busy.
- Each OCR subprocess has at most 12 seconds. The worker checks a 45-second document budget; the parent caps the complete worker at 60 seconds. These bounds reject slow files rather than guarantee a response time.
- Missing OCR installation, damaged or password-protected files, empty documents, excessive pages/text, worker failures, and timeouts produce safe messages. No raw parser or OCR stderr is displayed.

PDF parsing and rendering run in a disposable subprocess so a native parser error does not directly terminate the Streamlit interpreter. This is process isolation with bounded work, not a hardened untrusted-document sandbox or a guarantee against all memory exhaustion. OCR memory/time depends on the document and must be checked on the deployed host.

## Privacy

Uploaded PDF bytes remain in the Streamlit upload/session machinery. The app sends the bytes through a local worker's stdin and sends page images to a local Tesseract subprocess through stdin. Extracted text returns through stdout. No document content is sent to a third-party OCR service, written to application files, logged, or placed in a shared document cache. Framework, operating-system, and hosting memory handling are outside the application's secure-erasure guarantees.

## Installation and verification

Community Cloud reads the root `packages.txt`, which installs `tesseract-ocr` and `tesseract-ocr-eng`. Python dependencies add PDFium and Pillow. Pushing these changes requires a dependency rebuild; verify a scanned PDF after deployment. The existing Hub model secrets remain unchanged.

For local macOS development:

```bash
brew install tesseract
python -m pip install -r m5/requirements-test.txt
python -m unittest discover -s m5 -v
```

On Debian/Ubuntu, install the two packages from `packages.txt` through the system package manager. ReportLab is a test-only dependency used to generate synthetic text, scanned, mixed, encrypted, and over-limit PDFs. It is not installed by the Cloud runtime requirements. Real OCR integration tests need the Tesseract executable; test skips explicitly identify missing dependencies.

The tests use synthetic documents, not personal resumes. They check readable content and correct extraction routes, not field-level accuracy, character error rate, or recruiter quality. Existing M4 evaluation and classifier weights remain unchanged. Existing hosted timing reports cover text-service requests; they exclude PDF upload, rendering, and OCR. Recheck hosted PDF performance and layout after deploying this addition.

Local verification includes agreement with 30 saved M4 predictions and real OCR on synthetic image-only, mixed and forced-OCR PDFs. The evidence summary is consolidated in the [M5 guide](README.md#consolidated-local-verification); executable regression tests remain in this folder. Cloud PDF/OCR verification remains pending.

Local headless Chrome checks also passed with the saved CPU model: scanned resume plus pasted job, both PDF fields, editable review, replacement-file invalidation, safe damaged-file errors, and Clear. A 390-pixel viewport with dark system preference retained white app/upload backgrounds and no horizontal overflow. These are local checks, not evidence that the deployed app has received this update.

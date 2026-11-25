# Resume-job Matching Prototype

The Streamlit interface accepts pasted text or PDFs for the resume and job description, including English scanned PDFs through neural OCR, calls the existing inference pipeline, and displays the predicted fit. White backgrounds, neutral borders, and dark text are used throughout, including when the system prefers dark mode.

The inference module loads the class-weighted DistilBERT checkpoint selected before M4 test evaluation. It provides the prediction function for the Streamlit application. The [selection record](../m4/evaluation/model_selection.json) remains the source of the expected weight hash and input policy.

## Deployment

Use the root `streamlit_app.py` entry point for Community Cloud. Follow the [deployment guide](DEPLOYMENT.md) for private model hosting, pinned downloads, secrets, publishing, and the protected hosted performance check. The [performance report](performance/README.md) records local and maintainer-supplied hosted results, with remaining acceptance checks. The default local-file workflow below still works.

## Interface layout

The [interface design notes](UI_DESIGN.md) describe the compact white document workspace, loading states, keyboard focus, and mobile layout. PDF source controls stay in a compact popover; extracted text stays editable and both editors stay aligned. While reading or analysing, controls are disabled and the result area shows the active operation.

## PDF inputs

See the [PDF and OCR guide](PDF_INPUT.md) for the workflow, public model choice, limits, privacy, system dependencies, and verification. Each field has its own input method. Read a PDF, review and correct the extracted text, then analyse it using the unchanged matching pipeline.

## Files

| File | Purpose |
|---|---|
| [app.py](app.py) | Streamlit inputs, example and clear actions, loading state, results, and truncation notice |
| [styles.css](styles.css) | White-only appearance and mobile input layout |
| [Theme configuration](../.streamlit/config.toml) | Light theme, white surfaces, minimal toolbar, and disabled usage telemetry |
| [inference.py](inference.py) | Model loading, original text preparation, tokenization, prediction, and truncation information |
| [validation.py](validation.py) | Shared input bounds and correctable input errors |
| [service.py](service.py) | Guarded requests, safe failure categories, cache recovery, and metadata logging |
| [requirements.txt](requirements.txt) | Pinned dependencies for the verified local CPU environment |
| [test_inference.py](test_inference.py) | Preparation, checkpoint, CPU prediction, input, and truncation checks |
| [test_app.py](test_app.py) | Analysis, clearing, stale-result invalidation, truncation display, and unavailable-model UI checks |
| [test_service.py](test_service.py) | Input boundaries, failure/retry behaviour, response validation, and log-privacy checks |
| [verification.json](verification.json) | Recorded CPU agreement with saved M4 validation predictions |

## Setup

Use Python 3.11 or later. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r m5/requirements.txt
```

Obtain `distilbert_weighted_v1_model.zip` from the team's saved model artifacts. It is the trained checkpoint, not the original pretrained model or the reports archive. Extract it to:

```text
m5/artifacts/distilbert_weighted_v1/
  config.json
  model.safetensors
  tokenizer.json
  tokenizer_config.json
  weighted_run_config.json
```

The existing Git ignore rules exclude `artifacts/`. Keep the model archive and private review CSV outside Git. No public model download link is configured. Optional deployment settings provision the four inference files from a pinned private Hub snapshot. Loading verifies the weights against the frozen selection before accepting the model.

To use another local location, set `RESUME_MATCHER_MODEL_DIR` to the extracted folder or pass `model_dir` explicitly. Keep the repository's `m4/evaluation/model_selection.json` alongside this module when deploying.

## Run the interface

From the repository root, with the environment activated and model files installed:

```bash
python -m streamlit run m5/app.py
```

Open the local address printed by Streamlit, normally `http://localhost:8501`. Launch from the repository root so the project theme configuration is applied. Streamlit 1.67.0 is pinned alongside the existing inference dependencies.

1. Paste a resume and job description, or choose Upload PDF for either field and select Read PDF. Review extracted text before analysis. Both fields must contain text, and selected PDFs must have been read.
2. Select **Analyse match**. A loading message is shown while the CPU model runs.
3. Review Good Fit, Potential Fit, or No Fit alongside the full documents. A shortened-input notice and token counts appear when truncation occurs.
4. Edit either field to clear the previous result, or select **Clear** to reset both inputs and the result.

**Use an example** fills both fields with a synthetic pair. It still calls the real model when analysed; it does not supply a hardcoded prediction. The interface displays no match percentage or generated skill explanation.

The inference API reuses the loaded model across requests. Text and the current result stay in Streamlit session memory and are not written to files, added to query parameters, or passed to a shared data cache. Clear resets the active inputs and result; it is not a guarantee of secure memory erasure.

The interface validates requests before loading the model, keeps entered text after failures, and displays a support reference for model or prediction failures. Internal paths, exception details, and tracebacks are not displayed. See the deployment guide for console monitoring and recovery.

## Validation and failure handling

Each field accepts at most **50,000 characters** before preparation. The same bound applies to UI requests and direct inference calls. Oversized text is rejected rather than silently clipped, so the user can choose what to remove. The UI shows current character counts; the 512-token model window still applies separately.

Inputs must be strings with text and at least one letter or number. Newlines, carriage returns, and tabs are accepted; other control characters are rejected. Both fields must still contain letters or numbers after the unchanged M3 preparation. These are input-format checks, not a judgement of resume quality or eligibility.

Streamlit calls the guarded service:

```python
from m5.service import analyse_match

result = analyse_match("Python developer", "Python and SQL")
```

The successful response has the same four fields as the inference API below. The service checks the label, token-count types, token bounds, and truncation flag before the UI can display a prediction.

| Outcome | Behaviour |
|---|---|
| Invalid input | Show a field-level correction message; do not load or call the model |
| Model loading or checkpoint verification fails | Show an unavailable message and request reference; keep entered text |
| Prediction fails or returns an invalid result | Show a retry message and request reference; remove any previous result |
| Successful request | Display the verified response and any shortened-input notice |

Model-load and prediction failures clear the model cache. Selecting **Analyse match** again attempts a fresh load. No error is converted into a fit label, and there is no automatic retry loop. Permanent configuration problems still require a maintainer to fix the model files or environment. Editing inputs and Clear also remove the error reference.

### Operational logs

One JSON event is written to standard error for each handled request:

- `validation_failed`
- `model_load_failed`
- `prediction_failed`
- `prediction_completed`

Every event contains `event`, `request_id`, `duration_ms`, `resume_chars`, and `job_chars`. Successful events also include `truncated`. Character counts describe raw input; duration includes validation, any model loading, and prediction, rather than only the neural-network forward pass. Non-string fields have a null character count.

Logs exclude document text, predicted labels, exception messages, paths, and tracebacks. There is no application log file. The deployment platform may retain console output, so its retention settings still need configuration. A reference shown to the user can be matched with `request_id` without asking for document text.

For `model_load_failed`, check that the selected model archive is extracted at the configured location, its files match the frozen M4 checkpoint, and dependencies are installed. For `prediction_failed`, retry once after checking the runtime; persistent failures require maintainer investigation. Do not add document text or full exception payloads to logs when troubleshooting. The deployment guide covers hosting and manual monitoring; automated alerts and hard request timeouts are not implemented.

## Prediction API

Run Python from the repository root:

```python
from m5.inference import predict_match

result = predict_match(
    resume_text="Python developer",
    job_text="Python and SQL",
)
print(result)
```

The returned dictionary contains:

| Field | Meaning |
|---|---|
| `label` | Good Fit, Potential Fit, or No Fit |
| `truncated` | Whether the prepared pair exceeded the 512-token limit |
| `input_tokens` | Tokens passed to the model, including special tokens but excluding padding |
| `original_tokens` | Prepared pair tokens before truncation, including three pair special tokens |

No user text, scores, or predictions are cached. The convenience function reuses one loaded model per process. For an explicit reusable object:

```python
from m5.inference import load_matcher

matcher = load_matcher(device="cpu")
result = matcher.predict_match("Python developer", "Python and SQL")
```

CPU is the default and uses FP32. `device="cuda"` is available when CUDA exists and uses FP16 autocast. CPU integration is verified locally; this module's CUDA path has not been rerun locally. Shared instances serialise prediction calls so concurrent callers do not change tokenizer settings during another request.

## Input policy

Preparation is copied from the original M3 workflow: Unicode NFKC, visible Markdown link text, contact placeholders, and whitespace normalisation. Case, line breaks, and technical punctuation are preserved by preparation. This is not full anonymisation.

The resume is the first sequence and the job is the second. Tokenization uses right-side `longest_first` truncation, at most 512 tokens including special tokens, and dynamic padding to a multiple of eight. DistilBERT receives input IDs and attention masks without token-type IDs. No section-aware selection is applied. Evaluation mode and inference mode disable dropout and gradient recording.

Class weights and the custom Trainer are required for training reproduction, not prediction. The module rejects missing or incorrect model artifacts and invalid or oversized inputs. `prepare_inputs` shares pre-load preparation checks with the service. `clear_matcher_cache` supports reloading after a failed request. Application callers should use `analyse_match` when they need safe errors and operational logging; the lower-level inference API remains available.

## Verification

```bash
python -m unittest discover -s m5 -v
```

The seven Streamlit application tests use controlled inference responses to verify UI behaviour without treating those responses as model-quality evidence. They cover prediction and clearing, removing an old result after editing, the example/truncation flow, an unavailable model, oversized inputs before loading, retrying, and removing stale results after prediction errors. Run just these checks with:

```bash
python -m unittest discover -s m5 -p test_app.py -v
```

Model-dependent checks run when the model is installed at the configured location. To include the private 30-case M4 validation review sample:

```bash
RESUME_MATCHER_REVIEW_CSV="/absolute/path/to/error_review_with_text.csv" \
  python -m unittest discover -s m5 -v
```

The private CSV contains source text and stays outside the repository. The tests print case identifiers and label differences on failures, rather than document text. Without the CSV, the saved-prediction check is skipped; without model files, CPU integration checks are skipped.

The seven request-service tests check both field limits, invalid inputs without model loading, exact-boundary acceptance, safe failure categories, retry/cache reset, invalid model responses, and successful/failing log privacy. With the configured model, private sample, Tesseract, and test dependencies installed, the current suite runs 38 tests including PDF/OCR checks. The earlier inference-only verification record remains unchanged.

The recorded local run uses Python 3.14.0, PyTorch 2.10.0, Transformers 5.3.0, and Tokenizers 0.22.2. These are CPU inference dependencies, separate from the unchanged Colab training environment. Predictions agree with all 30 saved FP16 validation labels on this selected sample. This does not establish complete validation-set equivalence or unchanged logits across hardware and versions. No training or official-test evaluation is repeated for this check.

## Use in the prototype

The Streamlit interface calls `analyse_match()`, which validates the request before reusing the inference pipeline. It displays the label and truncation information, with a brief description of the tool's limits and the need for human review. The module supplies no calibrated match percentage or generated explanation.

Browser checks used local Chrome and the actual saved CPU model, including the synthetic example, long-input notice, editing, and clearing. A 390-pixel viewport with a dark system preference retained white page/input backgrounds, stacked fields, and no horizontal overflow. These checks do not establish hosted response times or production concurrency performance.

The [final evaluation](../m4/evaluation/evaluation_report.md) records low suitable-candidate recall and a higher official-test macro-F1 for the TF-IDF comparator. Retaining the recorded transformer selection here does not establish transformer superiority or deployment readiness. The deployment guide records manual monitoring and recovery steps. The performance report includes hosted measurements; browser acceptance and deployment metadata still require confirmation.

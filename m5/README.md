# Resume-job Matching Prototype

The Streamlit interface accepts resume and job-description text, calls the existing inference pipeline, and displays the predicted fit. White backgrounds, neutral borders, and dark text are used throughout, including when the system prefers dark mode.

The inference module loads the class-weighted DistilBERT checkpoint selected before M4 test evaluation. It provides the prediction function for the Streamlit application. The [selection record](../m4/evaluation/model_selection.json) remains the source of the expected weight hash and input policy.

## Files

| File | Purpose |
|---|---|
| [app.py](app.py) | Streamlit inputs, example and clear actions, loading state, results, and truncation notice |
| [styles.css](styles.css) | White-only appearance and mobile input layout |
| [Theme configuration](../.streamlit/config.toml) | Light theme, white surfaces, minimal toolbar, and disabled usage telemetry |
| [inference.py](inference.py) | Model loading, original text preparation, tokenization, prediction, and truncation information |
| [requirements.txt](requirements.txt) | Pinned dependencies for the verified local CPU environment |
| [test_inference.py](test_inference.py) | Preparation, checkpoint, CPU prediction, input, and truncation checks |
| [test_app.py](test_app.py) | Analysis, clearing, stale-result invalidation, truncation display, and unavailable-model UI checks |
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

The existing Git ignore rules exclude `artifacts/`. Keep the model archive and private review CSV outside Git. No public model download link is configured. Loading uses local files and verifies the weights against the frozen selection before accepting the model.

To use another local location, set `RESUME_MATCHER_MODEL_DIR` to the extracted folder or pass `model_dir` explicitly. Keep the repository's `m4/evaluation/model_selection.json` alongside this module when deploying.

## Run the interface

From the repository root, with the environment activated and model files installed:

```bash
python -m streamlit run m5/app.py
```

Open the local address printed by Streamlit, normally `http://localhost:8501`. Launch from the repository root so the project theme configuration is applied. Streamlit 1.67.0 is pinned alongside the existing inference dependencies.

1. Paste a resume and job description. Both fields must contain text before Analyse match is enabled.
2. Select **Analyse match**. A loading message is shown while the CPU model runs.
3. Review Good Fit, Potential Fit, or No Fit alongside the full documents. A shortened-input notice and token counts appear when truncation occurs.
4. Edit either field to clear the previous result, or select **Clear** to reset both inputs and the result.

**Use an example** fills both fields with a synthetic pair. It still calls the real model when analysed; it does not supply a hardcoded prediction. The interface displays no match percentage or generated skill explanation.

The inference API reuses the loaded model across requests. Text and the current result stay in Streamlit session memory and are not written to files, added to query parameters, or passed to a shared data cache. Clear resets the active inputs and result; it is not a guarantee of secure memory erasure.

The interface includes basic empty-field handling and neutral messages if a model cannot load or prediction fails. Internal paths and tracebacks are not displayed to the user. Detailed limits, recovery behaviour, operational logging, and deployment monitoring remain separate integration work.

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

Class weights and the custom Trainer are required for training reproduction, not prediction. The module rejects missing or incorrect model artifacts and non-string or empty inputs. Application limits, user-facing errors, operational logging, and recovery behaviour belong to the application integration work.

## Verification

```bash
python -m unittest discover -s m5 -v
```

The four Streamlit application tests use controlled inference responses to verify UI behaviour without treating those responses as model-quality evidence. They cover prediction and clearing, removing an old result after editing, the example/truncation flow, and an unavailable model without internal details. Run just these checks with:

```bash
python -m unittest discover -s m5 -p test_app.py -v
```

Model-dependent checks run when the model is installed at the configured location. To include the private 30-case M4 validation review sample:

```bash
RESUME_MATCHER_REVIEW_CSV="/absolute/path/to/error_review_with_text.csv" \
  python -m unittest discover -s m5 -v
```

The private CSV contains source text and stays outside the repository. The tests print case identifiers and label differences on failures, rather than document text. Without the CSV, the saved-prediction check is skipped; without model files, CPU integration checks are skipped.

The recorded local run uses Python 3.14.0, PyTorch 2.10.0, Transformers 5.3.0, and Tokenizers 0.22.2. These are CPU inference dependencies, separate from the unchanged Colab training environment. Predictions agree with all 30 saved FP16 validation labels on this selected sample. This does not establish complete validation-set equivalence or unchanged logits across hardware and versions. No training or official-test evaluation is repeated for this check.

## Use in the prototype

The Streamlit interface calls `load_matcher()` and reuses its `predict_match` method. It displays the label and truncation information, with a brief description of the tool's limits and the need for human review. The module supplies no calibrated match percentage or generated explanation.

Browser checks used local Chrome and the actual saved CPU model, including the synthetic example, long-input notice, editing, and clearing. A 390-pixel viewport with a dark system preference retained white page/input backgrounds, stacked fields, and no horizontal overflow. These checks do not establish hosted response times or production concurrency performance.

The [final evaluation](../m4/evaluation/evaluation_report.md) records low suitable-candidate recall and a higher official-test macro-F1 for the TF-IDF comparator. Retaining the recorded transformer selection here does not establish transformer superiority or deployment readiness. Detailed failure handling, monitoring, and hosted performance measurements remain separate contributions.

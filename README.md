# Resume-Job Matching System

A Streamlit application that compares an English resume with a job description and predicts **Good Fit**, **Potential Fit**, or **No Fit**. It supports pasted text, PDF uploads, and English OCR for scanned documents.

The application uses a fine-tuned, class-weighted DistilBERT checkpoint. The repository includes the data preparation, baseline methods, transformer training, experiments, and evaluation behind the prototype. Predictions support human review and do not make hiring decisions.

[Live application](https://resume-job-matcher-nlp.streamlit.app/) · [Technical report](m6/ieee-report.pdf) · [Presentation PDF](m6/presentation.pdf)

## Features

- Independent text or PDF input for the resume and job description.
- Embedded PDF text extraction with local English OCR for scanned pages.
- Editable extracted text before analysis.
- Three-class predictions with input coverage and truncation warnings.
- Loading states, input limits, safe error messages, and stale-result clearing.
- CPU inference with checkpoint verification and reusable model loading.
- Repeatable dataset splits, saved experiment settings, and evaluation artifacts.

## How it works

1. **Provide documents:** paste text or upload a PDF for each input.
2. **Extract and review:** read embedded text with `pypdfium2`; use Tesseract OCR for scanned pages. Review and correct the extracted text.
3. **Prepare inputs:** validate size and format, normalise text, and replace contact details with placeholders.
4. **Run inference:** tokenize the resume and job together and pass them to the saved DistilBERT classifier. The highest-scoring class becomes the prediction.
5. **Display the result:** show the fit label and whether the model shortened the input.

The combined model input is limited to **512 tokens**, including special tokens. PDF extraction can read more text than the classifier can process. The interface reports this distinction rather than silently implying full coverage. The matching pipeline does not call an external assessment API.

## Run locally

Use Python 3.11 or later. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r m5/requirements.txt
```

Extract the team's selected `distilbert_weighted_v1_model.zip` archive into a local directory containing:

```text
distilbert_weighted_v1/
  config.json
  model.safetensors
  tokenizer.json
  tokenizer_config.json
  weighted_run_config.json
```

Point the application to that directory and start Streamlit:

```bash
export RESUME_MATCHER_MODEL_DIR="/absolute/path/to/distilbert_weighted_v1"
python -m streamlit run streamlit_app.py
```

Open the address printed by Streamlit, normally `http://localhost:8501`.

Model weights are excluded from Git. Loading verifies them against the [recorded model selection](m4/evaluation/model_selection.json). For scanned PDFs, install Tesseract using the [PDF/OCR guide](m5/PDF_INPUT.md). Private Hugging Face model provisioning and Streamlit Community Cloud configuration are covered in the [deployment guide](m5/DEPLOYMENT.md).

## Data and training

The project uses the public Hugging Face dataset [`cnamuangtoun/resume-job-description-fit`](https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit), with 8,000 labelled resume-job pairs. A [review of five papers](m1/related-work.md) informed the dataset and baseline choices.

Preparation removes conflicting-label pairs and extra duplicate copies from the original training pool. The shared experiment splits contain 5,081 training, 1,147 validation, and 1,759 official-test pairs. No jobs or prepared pairs overlap across these splits, although some resumes are shared. This evaluates new jobs against a largely known candidate pool, rather than entirely new applicants.

The experiments include TF-IDF cosine similarity, paired TF-IDF with SGD, MiniLM, and DistilBERT. Transformer runs use validation macro-F1 for checkpoint selection. Later experiments test section-aware input preparation and class-weighted loss. Training environments and model revisions are recorded separately from the CPU application dependencies.

## Results

Class-weighted DistilBERT was selected using validation macro-F1 before official-test evaluation. Original DistilBERT and TF-IDF + SGD were fixed comparators; no model reselection or threshold tuning followed the test.

| Model | Validation macro-F1 | Official-test macro-F1 |
|---|---:|---:|
| Class-weighted DistilBERT | 0.3582 | 0.3563 |
| Original DistilBERT | 0.3540 | 0.3626 |
| TF-IDF + SGD | 0.2923 | 0.4058 |

**TF-IDF + SGD achieved the highest test macro-F1.** The weighted model's small validation gain did not carry over to the test. MiniLM and section-aware DistilBERT reached validation macro-F1 of 0.3081 and 0.3258 respectively and were not included in the final official-test comparison.

The [evaluation report](m4/evaluation/evaluation_report.md) includes per-class results, confusion matrices, 30 qualitatively reviewed validation cases, and robustness tests on 300 balanced validation pairs. Earlier M2 results use a different split protocol and are documented separately.

## Repository structure

| Directory | Contents |
|---|---|
| [m1/](m1/) | Problem definition, feasibility, related work, and paper reviews |
| [m2/](m2/README.md) | Original data preparation, baseline notebooks, and reproduction results |
| [m3/](m3/README.md) | Shared splits, tokenization, MiniLM and DistilBERT training, and experiment artifacts |
| [m4/](m4/README.md) | Improvement experiments, error analysis, robustness tests, and final evaluation |
| [m5/](m5/README.md) | Streamlit application, PDF/OCR processing, inference, validation, tests, and deployment |
| [m6/](m6/) | IEEE report and LaTeX source, HTML/PDF presentation, and project documentation |

The [MiniLM and DistilBERT notebook](m3/notebooks/m3-distilbert-finetuning.ipynb) contains both transformer runs. The [combined evaluation notebook](m4/notebooks/m4-final-evaluation.ipynb) contains the later reference evaluation, improvement experiments, and final assessment.

## Tests

```bash
python -m unittest discover -s m5 -v
```

The suite covers inference, input validation, service failures, UI behaviour, model provisioning, and PDF/OCR handling. Model-dependent checks require the selected model files; OCR checks require Tesseract. The optional private review fixture is documented in the [application guide](m5/README.md). Software tests verify implementation behaviour and do not measure matching quality.

## Limitations and data handling

- Long pairs are truncated to 512 combined tokens, which can remove relevant information.
- Suitable-candidate recall remains low, and the original quality targets were not met. The model can return incorrect labels, including for irrelevant inputs that pass format checks.
- Predictions are not calibrated suitability percentages or verified explanations of individual requirements.
- Recruiter agreement, time savings, demographic fairness, and performance on entirely new applicants have not been established.
- Raw resume records, dataset caches, private review text, model weights, and credentials stay outside Git. Contact replacement is not complete anonymisation.
- The dataset's licence and collection details remain unresolved; public availability alone does not establish reuse rights.

The [performance record](m5/performance/README.md) distinguishes model/service benchmarks from browser and PDF/OCR work and records remaining hosted acceptance checks. The system remains a prototype requiring human review.

## Team

Pottabathini Vivekananda · Vikas Eranki · Manasa · Bhavani Shanker

Newton School of Technology, Rishihood University

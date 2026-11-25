# Resume-Job Matching System

NLP · Industry Track

We are building a recruiter support tool that compares a resume with a job description and predicts **Good Fit**, **Potential Fit**, or **No Fit**. A recruiter reviews the result and makes the final decision.

Our evaluation focuses on an existing candidate pool matched with new job descriptions. It does not establish performance on completely new applicants.

## Approach

We began by reviewing five papers to understand existing resume-job matching methods, their results, and their practical limits. The comparison covered shared text representations, sentence embeddings, contrastive learning, and accessible lexical baselines. Data access, task fit, and CPU requirements led us to a public three-class dataset and TF-IDF reference methods.

We then examined the dataset for class imbalance, inconsistent labels, duplicate pairs, document lengths, and overlap between splits. The preparation pipeline turns those findings into repeatable cleaning and split decisions. Model comparison and evaluation build on this foundation, with human review at the centre of the recruiter workflow.

The [related-work overview](m1/related-work.md) connects the paper reviews to these choices.

## Presentation and code walkthrough

Open these files in order when explaining the project. M3 and M4 notebook section headings explain each stage; M1 and M2 remain as they were before cleanup. Executable code and saved outputs are preserved.

| Stage | Open this file | What to show |
|---|---|---|
| M1: problem and feasibility | [Problem brief](m1/problem-brief.md) and [feasibility](m1/feasibility-analysis.md) | Users, business objective, success targets and practical limits |
| M1: existing work | [Related work](m1/related-work.md) | Five paper reviews, source links and model-selection rationale |
| M2: data preparation | [Preparation notebook](m2/notebooks/m2-data-preparation.ipynb) | Quality checks, duplicate handling, cleaning and historical splits |
| M2: original baseline | [Baseline notebook](m2/notebooks/m2-baseline-reproduction.ipynb) | TF-IDF cosine similarity and SGD; original notebook preserved unchanged |
| M3: shared splits | [Data setup notebook](m3/notebooks/m3-model-development.ipynb) | Job-grouped validation and reproducible source-row selection |
| M3: transformer training | [Combined training notebook](m3/notebooks/m3-distilbert-finetuning.ipynb) | Input tokenization, MiniLM and DistilBERT training, checkpoint selection and comparison |
| M4: experiments and evaluation | [Combined evaluation notebook](m4/notebooks/m4-final-evaluation.ipynb) | TF-IDF reference, section-aware inputs, weighted loss, errors, robustness and final test |
| M4: findings | [Evaluation report](m4/evaluation/evaluation_report.md) | Measured results, frozen model selection and limitations |
| M5: user interface | [app.py](m5/app.py) | Input modes, editable text, loading states and result display |
| M5: PDF and OCR | [pdf_input.py](m5/pdf_input.py) and [pdf_worker.py](m5/pdf_worker.py) | Bounded extraction and local English OCR fallback |
| M5: model prediction | [inference.py](m5/inference.py) | Selected-weight verification, cleaning, 512-token encoding and classifier prediction |
| M5: request handling | [service.py](m5/service.py) and [validation.py](m5/validation.py) | Input bounds, metadata-only logging and safe failures |
| M6: technical report | [IEEE report PDF](m6/ieee-report.pdf) and [LaTeX source](m6/ieee-report.tex) | Methods, results, error analysis, system design, deployment and limitations |

The filename `m3-distilbert-finetuning.ipynb` is retained for continuity; it contains both MiniLM and DistilBERT. M4 similarly has one combined notebook rather than duplicate snapshots of its earlier stages. Notebooks that need Colab uploads document their inputs in the opening sections. Full GPU workflows are for reproduction; use their saved outputs during the presentation.

Supporting guides: [M2](m2/README.md), [M3](m3/README.md), [M4](m4/README.md), [M5](m5/README.md), [PDF/OCR](m5/PDF_INPUT.md), [deployment](m5/DEPLOYMENT.md) and [performance](m5/performance/README.md). Configurations, histories, prediction tables and checks remain in the corresponding milestone folders.

[Original presentation](m2/presentation.pdf) retains the earlier ten-slide content and design. It is not a substitute for the final delivery presentation. [Baseline results](m2/reproduction-results.md) and [reproduction observations](m2/reproduction-observations.md) remain separate original documents. [M2 requirements](m2/requirements.txt) preserve the baseline environment; training and CPU deployment use their separately documented environments.

## Run the prototype locally

From the repository root, install the runtime dependencies in a virtual environment and point the application to the selected model files:

```bash
python -m pip install -r m5/requirements.txt
export RESUME_MATCHER_MODEL_DIR="/absolute/path/to/distilbert_weighted_v1"
python -m streamlit run streamlit_app.py
```

For scanned PDFs, install Tesseract as described in the [PDF guide](m5/PDF_INPUT.md). For hosted model downloads and secrets, follow [deployment setup](m5/DEPLOYMENT.md). The model files stay outside Git; inference verifies them against [the frozen M4 selection](m4/evaluation/model_selection.json).

## Data handling

Download the dataset through the notebook. Do not commit raw or cleaned resume records, local dataset caches, or personal data. The dataset's licence and collection details have not been established by this project; public access alone does not establish permission for reuse or redistribution.

## Shared-protocol reference evaluation

Paired TF-IDF with SGD achieves validation macro-F1 0.2923 on the M3 splits, compared with MiniLM at 0.3081 and DistilBERT at 0.3540. TF-IDF retains the highest Potential Fit recall, while MiniLM has the highest Good Fit recall. All three approaches miss many suitable candidates. The [comparison notes](m4/comparison/comparison_notes.md) explain preprocessing differences and limitations. These validation results preceded the separately recorded final selection and official-test evaluation.

The section-aware DistilBERT experiment achieves validation macro-F1 0.3258, below the original 0.3540. Potential Fit recall increases, while Good Fit recall falls to 0.0500. The original input policy remains the stronger candidate. The [M4 guide](m4/README.md) records this improvement attempt, its configuration, and its limitations.

Class-weighted DistilBERT with the original input policy reaches validation macro-F1 0.3582, compared with 0.3540 for the unweighted run. The small gain comes with lower Good Fit recall and accuracy. It was selected before official-test inference using validation macro-F1; the final results below retain that recorded selection.

## Final evaluation

The class-weighted DistilBERT checkpoint was selected using validation macro-F1 before the official test was evaluated. Original DistilBERT and TF-IDF were fixed comparators. Test results were reported without model reselection or threshold tuning.

| Model | Evaluation role | Validation macro-F1 | Official-test macro-F1 |
|---|---|---:|---:|
| Class-weighted DistilBERT | Selected before test | 0.3582 | 0.3563 |
| Original DistilBERT | Fixed comparator | 0.3540 | 0.3626 |
| TF-IDF + SGD | Fixed comparator | 0.2923 | 0.4058 |

TF-IDF has the highest test macro-F1 among these fixed comparisons. The weighted run's small validation gain does not carry over to the test set, and transformer superiority is not established. The recorded selection remains unchanged; it does not establish a deployment recommendation.

The [evaluation report](m4/evaluation/evaluation_report.md) documents 30 qualitatively reviewed validation cases, robustness tests on 300 balanced validation pairs, and model-only GPU inference measurements. Suitable-candidate recall remains low, so further use is limited to a prototype with human review. Earlier historical M2 test scores use a different split protocol.

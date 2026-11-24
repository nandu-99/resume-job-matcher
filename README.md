<<<<<<< HEAD
# resume-job-matcher

NLP course project on three-class resume–job matching. Each resume–job pair is
classified as **Good Fit**, **Potential Fit**, or **No Fit**, with **macro-F1**
as the primary metric.

The anchor paper is B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job
Matching for Trustworthy LLM-Assisted Recruiter Screening," 2025.

## Dataset

Source: `cnamuangtoun/resume-job-description-fit` (revision
`08978e21714984bb417547d2c0f9b477f5298163`), 6,241 original training rows and
1,759 official test rows. Labels are `Good Fit: 0`, `Potential Fit: 1`,
`No Fit: 2`.

## Milestones

| Milestone | Focus |
|---|---|
| [M1](m1/) | Research gap, anchor-paper justification, project scope, reproducibility checklist |
| [M2](m2/) | TF-IDF baselines (cosine similarity and paired TF-IDF + SGD) |
| [M3](m3/) | Transformer fine-tuning: MiniLM and DistilBERT on shared job-grouped splits |

## M3: transformer models

M3 fine-tunes two transformers on shared, job-grouped splits so their results
are directly comparable. Jobs are grouped by a SHA-256 of their prepared text
and split with the first fold of `StratifiedGroupKFold(n_splits=5, shuffle=True,
random_state=42)`, giving a single held-out validation set with **no job or
resume–job pair overlap** across splits.

| Split | Good Fit | Potential Fit | No Fit | Total | Unique jobs |
|---|---:|---:|---:|---:|---:|
| Training | 1,258 | 1,223 | 2,600 | 5,081 | 229 |
| Validation | 280 | 331 | 536 | 1,147 | 51 |
| Official test | 458 | 444 | 857 | 1,759 | 71 |

Both models share the same 512-token `longest_first` input policy, label
mapping, seed 42, unweighted cross-entropy, effective batch size 16, learning
rate 2e-5, FP16, three epochs, and validation macro-F1 checkpoint selection.
Both select epoch 2 (`checkpoint-636`).

### Results (validation)

| Model | Macro-F1 | Accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
|---|---:|---:|---:|---:|---:|
| MiniLM | 0.3081 | 0.4682 | 0.2643 | 0.0000 | 0.8638 |
| DistilBERT | 0.3540 | 0.4752 | 0.2107 | 0.1088 | 0.8396 |

DistilBERT leads on validation macro-F1 by 0.0459 absolute and predicts all
three classes; MiniLM keeps higher Good Fit recall. Both still miss many
suitable candidates. These are single-seed validation results — **neither
transformer has been evaluated on the official test set**, and historical M2
test scores use a different split protocol, so the two are not directly
comparable.

### M3 contents

- [M3 README](m3/README.md) — full data-preparation, split, tokenization, and training write-up
- [Experiment log](m3/experiment-log.csv) — comparable run summaries for both models
- [DistilBERT notebook](m3/notebooks/m3-distilbert-finetuning.ipynb) — executed Colab notebook (shared prep, MiniLM reference, DistilBERT training, export checks, comparison)
- [Model comparison](m3/comparison/comparison_notes.md) — findings, [CSV](m3/comparison/model_comparison.csv), and [figure](m3/comparison/model_comparison.png)
- [DistilBERT experiment evidence](m3/experiments/distilbert-v1/) — training history, validation reports, run settings, and reload checks

Trained model weights and raw records are **not** stored in this repository.
The reports capture metrics and export-integrity checks; loading a trained model
requires its separately stored archive.

## Reproducing M3

Open the DistilBERT notebook in a fresh Colab T4 runtime, run the cells in
order, and upload `m3_data_setup.zip` when prompted. The notebook also runs
MiniLM to provide the comparison reference. Check the dataset and model
revisions against the saved configuration; record any new run separately if
results change. GPU training is not required just to review the saved outputs.

## Next steps (M4)

Error analysis, separate trials of class-weighted loss and section-aware inputs,
a TF-IDF reference under the same M3 splits, and robustness checks. Official
test evaluation is held back until model selection is fixed.
=======
# Resume–Job Matching System

NLP · Industry Track

We are building a recruiter support tool that compares a resume with a job description and predicts **Good Fit**, **Potential Fit**, or **No Fit**. A recruiter reviews the result and makes the final decision.

Our evaluation focuses on an existing candidate pool matched with new job descriptions. It does not establish performance on completely new applicants.

## Approach

We began by reviewing five papers to understand existing resume-job matching methods, their results, and their practical limits. The comparison covered shared text representations, sentence embeddings, contrastive learning, and accessible lexical baselines. Data access, task fit, and CPU requirements led us to a public three-class dataset and TF-IDF reference methods.

We then examined the dataset for class imbalance, inconsistent labels, duplicate pairs, document lengths, and overlap between splits. The preparation pipeline turns those findings into repeatable cleaning and split decisions. Model comparison and evaluation build on this foundation, with human review at the centre of the recruiter workflow.

The [related-work overview](m1/related-work.md) connects the paper reviews to these choices.

## Project files

- [Related work](m1/related-work.md): five paper reviews, comparison, and design rationale.
- [Problem brief](m1/problem-brief.md): users, workflow, business objective, and success measures.
- [Feasibility analysis](m1/feasibility-analysis.md): data, tools, cost, and project risks.
- [Project presentation](m2/presentation.pdf): 10 slides covering the problem, data, methods, and findings.
- [Data preparation guide](m2/README.md): dataset reports, preparation steps, and notebook instructions.
- [Baseline models](m2/notebooks/m2-baseline-reproduction.ipynb): TF-IDF cosine similarity and paired TF-IDF with SGD, with the original saved results.
- [Transformer data setup](m3/README.md): the Colab notebook, shared job-grouped splits, and reproduction instructions for model development.
- [Transformer inputs](m3/notebooks/m3-transformer-models.ipynb): the executed MiniLM and DistilBERT tokenization workflow, truncation reports, and batch checks.
- [MiniLM fine-tuning](m3/notebooks/m3-minilm-finetuning.ipynb): the executed training workflow and validation evidence, summarised in the [experiment log](m3/experiment-log.csv).

The preparation notebook provides the data workflow and additional cleaned-pair checks. The baseline notebook retains the existing model implementation so candidate approaches can build on it. Its saved test macro-F1 values are 0.3708 for cosine similarity and 0.4100 for paired TF-IDF with SGD.

[requirements.txt](m2/requirements.txt) preserves the original baseline dependencies. The preparation notebook records newer versions in its setup cell and saved environment output; it has not been validated against the original baseline dependencies. The original baseline notebook and five paper summaries are kept exactly as committed.

## Data handling

Download the dataset through the notebook. Do not commit raw or cleaned resume records, local dataset caches, or personal data. The dataset's licence and collection details have not been established by this project; public access alone does not establish permission for reuse or redistribution.
>>>>>>> origin/main

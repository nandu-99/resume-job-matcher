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

# Data Understanding and Preparation

Industry Track - Resume-Job Matching System

The dataset contains resume text, job-description text, and a match label. The preparation pipeline studies data quality, removes inconsistent pairs, cleans text, and creates reproducible splits for model development.

## Connection to existing work

The [initial paper review](../m1/related-work.md) guided the dataset and baseline choices. The selected reference uses the same three labels and provides preparation details that we can check. Our pipeline examines the actual records and documents the quality and split limits rather than assuming the published setup is sufficient for every recruitment scenario.

## Data reports

| File | Contents |
|---|---|
| [Data card](data-card.md) | Source, fields, labels, counts, intended use, and limits |
| [Exploratory and statistical analysis](data-analysis.md) | Class balance, missing values, duplicates, document lengths, and overlap |
| [Cleaning and split report](preprocessing.md) | Duplicate handling, text cleaning, split settings, and checks |
| [Privacy report](privacy.md) | Personal data, handling rules, and responsible use |
| [Preparation notebook](notebooks/m2-data-preparation.ipynb) | Executable code and aggregate results |
| [Baseline notebook](notebooks/m2-baseline-reproduction.ipynb) | Existing model code, threshold selection, and saved results |
| [Threshold selection](figures/threshold-selection.png) | Validation search for the cosine-similarity thresholds |
| [Project presentation](presentation.pdf) | The original 10-slide presentation, with its content and design unchanged |
| [Dataset overview](figures/dataset-overview.png) and [split distribution](figures/split-label-distribution.png) | Supporting figures |

## Dataset and preparation

The original dataset has 8,000 labelled pairs, with no missing or empty required values. Good Fit and Potential Fit each account for 25% of the data; No Fit accounts for 50%.

The pipeline removes 12 rows with conflicting labels and one extra duplicate copy. The resulting splits contain 4,982 training rows, 1,246 validation rows, and 1,759 test rows. Neither original-text nor cleaned-text pairs are duplicated within a split or shared across splits.

The official test jobs are unseen, but most test resumes occur in the original training pool. Training and validation also share resumes and jobs. Job-grouped validation would better represent the new-job scenario during candidate selection. Dataset licence and collection details remain unresolved.

## Run the notebook

1. Open [m2-data-preparation.ipynb](notebooks/m2-data-preparation.ipynb) in Google Colab with a CPU runtime.
2. Run every cell from the beginning. Internet access is required to download the dataset and install packages.
3. Check that the validation tables pass and the counts match the reports. Investigate any differences before using the prepared data.
4. Keep only aggregate outputs. Do not add real resume samples or dataset files to the repository.

The preparation notebook specifies its tested package versions in its setup cell and prints the environment versions. [requirements.txt](requirements.txt) preserves the original baseline dependencies.

## Baseline models

The [baseline notebook](notebooks/m2-baseline-reproduction.ipynb) retains the implementation from commit `229b0ff`. It uses the same three labels and fits text transformations and models on training data. Cosine thresholds are selected using validation data.

| Model | Saved test macro-F1 | Saved test accuracy |
|---|---:|---:|
| TF-IDF cosine similarity | 0.3708 | 0.4110 |
| Paired TF-IDF with SGD | 0.4100 | 0.5088 |

The baseline notebook is restored exactly as committed, including its code, setup cell, markdown, outputs, and original dataset preview. These are the original recorded results, not a new training run.

The baseline's recorded runtime was Python 3.13.16, with packages listed in [requirements.txt](requirements.txt). Its original setup cell installs `datasets` without pinning the full environment. To target the recorded results, install the listed versions in a separate runtime before running the notebook. Use a separate runtime for each notebook: the preparation notebook was verified with newer packages, including scikit-learn 1.8.0, while the original baseline used scikit-learn 1.6.1. Installing one environment over the other can change results.

The files remain under `m2/` to preserve the existing project structure. For the Industry Track, data preparation supports M2; the baseline and candidate comparisons support M3. Candidate development can build on this implementation and record changes in an experiment log. The additional cleaned-pair assertions are in the preparation notebook; they have not been added to the historical baseline.

## Verification

The preparation code was run from the beginning on Python 3.14.0 using the installed package versions. All audit, preprocessing, and cleaned-pair checks passed. The preparation notebook contains the resulting aggregate outputs, and the dataset overview and split-distribution figures use that run. Package installation itself was not rerun during this verification. The baseline notebook was verified byte for byte against Git; its saved model results and threshold figure come from the earlier committed run.

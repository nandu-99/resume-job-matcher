# Reproducibility Notes

The initial review checked whether the selected reference methods could be implemented with accessible data, clear settings, and available compute. These notes describe the reference paper; the preparation notebook prints the actual environment used in our project.

## Data and preparation

| Item | Information recorded from the reference |
|---|---|
| Dataset | `cnamuangtoun/resume-job-description-fit` |
| Original size | 8,000 labelled pairs |
| Required inputs | Resume text and job-description text |
| Labels | Good Fit, Potential Fit, No Fit |
| Duplicate handling | Remove conflicting groups and collapse repeated same-label pairs |
| Clean training pool | 6,228 rows |
| Split | 4,982 training, 1,246 validation, 1,759 test rows; seed 42 |
| Cleaning | Lowercase, retain visible link text, replace contacts, remove unwanted characters, normalise spaces |

Our [preparation report](../m2/preprocessing.md) and [notebook](../m2/notebooks/m2-data-preparation.ipynb) provide the implementation and data checks.

The [baseline notebook](../m2/notebooks/m2-baseline-reproduction.ipynb) preserves the committed model implementation and its saved results. Its original dependencies are preserved in [requirements.txt](../m2/requirements.txt). The preparation notebook records its newer tested versions in its setup cell and saved output.

## Reference model settings

| Setting | TF-IDF cosine similarity | Paired TF-IDF with SGD |
|---|---|---|
| Input | Separate resume and job vectors | Joined resume and job text |
| N-grams | Words, unigrams and bigrams | Words, unigrams and bigrams |
| Maximum features | 30,000 | 50,000 |
| Minimum document frequency | 3 | 3 |
| Maximum document frequency | Not specified here | 0.98 |
| Stop words | English | English |
| Sublinear term frequency | Not specified here | Enabled |
| Prediction | Two validation-selected thresholds | SGD with logistic loss, alpha 0.00001, seed 42 |
| Paper-reported test macro-F1 | 0.359 | 0.436 |

## Details that limit exact reproduction

The paper does not provide the exact cleaning expressions, placeholder words, threshold-search procedure, or every SGD setting. It mentions a code archive without a clear public link. The full 108-skill list and title rules for its hybrid model are also unavailable in the reviewed material.

These limits favour a clearly documented implementation of the simple baselines. Any comparison should record actual package versions, preprocessing, model settings, validation choices, and differences from the reference. Published results are comparison points rather than guaranteed outcomes.

## Evaluation principles

Fit text transformations and classifiers on training data only. Select thresholds and candidate settings using validation data. Reserve test labels for evaluation after settings are fixed. Report macro-F1, per-class precision and recall, confusion matrices, and runtime.

The project's split audit also reveals shared jobs between training and validation. A job-grouped validation design better represents new-job matching when selecting candidates. Public data access alone does not establish permission to use or redistribute resume records.

## Reference

[Calibrated Resume-Job Matching](https://doi.org/10.51903/jtie.v4i3.529). See the [paper review](papers/05-calibrated-resume-job-matching.md) for the detailed method and reported results.

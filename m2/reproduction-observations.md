# Reproduction Observations

## Main Finding

Both baseline models were reproduced successfully. Their exact results differ from the paper, but they keep the same main pattern: paired TF-IDF with SGD performs better than cosine similarity.

| Model | Paper test macro-F1 | Reproduced test macro-F1 | Absolute gap | Relative gap |
|---|---:|---:|---:|---:|
| TF-IDF cosine similarity | 0.359 | 0.3708 | 0.0118 | +3.29% |
| Paired TF-IDF with SGD | 0.436 | 0.4100 | 0.0260 | -5.97% |

## Cosine Similarity

The reproduced cosine baseline is 0.0118 higher than the paper result. Its validation macro-F1 of 0.4174 is also close to the paper's 0.416.

The paper does not report the exact threshold-search range or step size. This reproduction uses a coarse search followed by a finer search on validation data. The selected thresholds are 0.045 and 0.074.

The model has weak results for Good Fit and Potential Fit. Its F1 scores for those classes are 0.2676 and 0.2901. The No Fit F1 is higher at 0.5548.

## Paired TF-IDF with SGD

The reproduced SGD validation macro-F1 is 0.6513, which is close to the paper's 0.658. The test macro-F1 is 0.4100, which is 0.0260 lower than the paper's 0.436.

The classifier predicts No Fit too often:

- 250 Good Fit rows are predicted as No Fit.
- 287 Potential Fit rows are predicted as No Fit.
- 685 No Fit rows are predicted correctly.

This behaviour improves No Fit recall to 0.7993 but reduces Good Fit recall to 0.1616. Macro-F1 decreases because it gives equal importance to every class.

## Possible Reasons for the Gaps

### Text Cleaning

The paper describes its cleaning steps but does not publish the exact regular expressions or placeholder words. Small cleaning differences change the TF-IDF vocabulary and feature weights.

### Threshold Search

The paper says that two similarity thresholds were selected on validation data, but it does not provide the search method or final values.

### SGD Defaults

The paper reports logistic loss and alpha 0.00001, but it does not list every SGD setting. This reproduction uses the defaults from the installed scikit-learn version for settings that are not reported.

### Software Versions

The paper reports Python 3.13.5 and scikit-learn 1.8.0. The Colab run used Python 3.13.16 and scikit-learn 1.6.1. Package differences can change numerical behaviour and SGD convergence.

### Dataset Version

The public dataset may have changed after the paper experiment. The current dataset matches the reported row counts and duplicate groups, but its exact file version is not identified by the paper.

## Data Limits

The official split contains no repeated complete resume-job pairs. However, many resumes appear in more than one split. This means the results do not fully measure performance on completely new resumes.

The No Fit class contains 50% of the full dataset. This class imbalance helps explain why the SGD model predicts No Fit frequently.

The dataset page does not provide clear licence, citation, or collection details. The project is limited to academic evaluation and should not be used for real hiring decisions.

## Reproducibility Assessment

The two baselines are reproducible at the method level:

- Public data is available.
- Final split sizes match the paper.
- Model settings are mostly reported.
- Both methods run on a Colab CPU.
- Validation results are close to the paper.
- Test gaps are small enough to compare and explain.

Exact numerical reproduction is limited by missing cleaning code, missing threshold details, unreported SGD settings, and different software versions.

# Exploratory and Statistical Analysis

## Purpose

This analysis checks whether the dataset is complete, balanced enough for modelling, free from conflicting duplicate pairs, and suitable for the stated business use case.

## Dataset Size

The dataset contains 8,000 resume-job pairs:

- 6,241 original training rows
- 1,759 official test rows

## Missing and Empty Values

No missing or empty value was found in either split for:

- Resume text
- Job-description text
- Label

This means no row needs to be removed for a missing required field.

## Class Distribution

| Label | Total rows | Percentage |
|---|---:|---:|
| Good Fit | 2,000 | 25% |
| Potential Fit | 2,000 | 25% |
| No Fit | 4,000 | 50% |

The largest class is twice the size of either smaller class. A model that predicts No Fit too often can obtain reasonable accuracy while performing poorly for the other classes.

For this reason:

- Macro-F1 is the main metric.
- Precision, recall, and F1 are reported for every class.
- A confusion matrix is required.

## Duplicate Analysis

The original training split contains seven duplicate pair groups with two rows in each group.

| Duplicate type | Groups | Rows |
|---|---:|---:|
| Conflicting labels | 6 | 12 |
| Same label | 1 | 2 |

Four conflicting pairs have Good Fit and No Fit labels, and two have Potential Fit and No Fit labels. The same-label duplicate pair contains two No Fit rows.

Six pairs have different labels for exactly the same resume and job description. These rows provide contradictory learning signals, so all 12 conflicting rows are removed.

One pair is repeated with the same label. One copy is kept and one is removed.

The official test split contains no duplicate pair group.

## Document Length Analysis

Word counts use whitespace-separated words before cleaning.

| Split | Mean resume words | Median resume words | Maximum resume words | Mean job words | Median job words | Maximum job words |
|---|---:|---:|---:|---:|---:|---:|
| Training | 708.1 | 618.0 | 3,134 | 371.5 | 328.0 | 1,079 |
| Test | 691.4 | 618.0 | 2,738 | 402.9 | 308.0 | 1,254 |

Main findings:

- Resumes are longer than job descriptions in both splits.
- The mean test resume is 16.7 words shorter than the mean training resume.
- The mean test job description is 31.4 words longer than the mean training job description.
- Maximum lengths are much larger than medians, so the data contains long documents.

The differences suggest a small length shift between training and test job descriptions. Long documents can also create noise for word-based models.

## Character-Length Analysis

| Split | Mean resume characters | Mean job characters |
|---|---:|---:|
| Training | 5,804.4 | 2,731.3 |
| Test | 5,663.3 | 2,939.2 |

The character statistics support the same finding: resumes are longer overall, while test job descriptions are slightly longer than training job descriptions.

## Overlap Analysis

| Text unit | Unique in training | Unique in test | Shared unique values | Test rows with overlap |
|---|---:|---:|---:|---:|
| Resume text | 642 | 477 | 476 | 1,758 |
| Job description | 280 | 71 | 0 | 0 |
| Complete resume-job pair | 6,234 | 1,759 | 0 | 0 |

Interpretation:

- No complete pair is repeated between training and test.
- No test job description appears in training.
- Almost every test row uses a resume represented in the original training pool, before cleaning and validation splitting.

Therefore, the test set measures matching known resumes with new jobs. It does not measure performance on completely new resumes.

## Prepared Split Distribution

| Split | Good Fit | Potential Fit | No Fit | Total |
|---|---:|---:|---:|---:|
| Training | 1,230 | 1,243 | 2,509 | 4,982 |
| Validation | 308 | 311 | 627 | 1,246 |
| Test | 458 | 444 | 857 | 1,759 |

The stratified split keeps similar class percentages across training, validation, and test data.

## Statistical Conclusion

The dataset is complete and large enough for baseline modelling. The main statistical concerns are:

1. A 2:1 class imbalance between No Fit and each smaller class.
2. Contradictory duplicate labels in the original training data.
3. Very long documents.
4. A small document-length shift between training and test job descriptions.
5. Very high resume reuse across training and test.

These findings directly affect metric selection, duplicate cleaning, split interpretation, and the limits of the final claim.

## Figures

- [Dataset overview](figures/dataset-overview.png)
- [Split label distribution](figures/split-label-distribution.png)


# Reproduction Results

## Objective

The M2 work reproduces two three-class resume-job matching baselines from the anchor paper:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier

The classes are Good Fit, Potential Fit, and No Fit. Macro-F1 is the main metric.

## Final Data Splits

| Split | Good Fit | Potential Fit | No Fit | Total |
|---|---:|---:|---:|---:|
| Training | 1,230 | 1,243 | 2,509 | 4,982 |
| Validation | 308 | 311 | 627 | 1,246 |
| Test | 458 | 444 | 857 | 1,759 |

The split sizes and label counts match the anchor paper.

## TF-IDF Cosine Similarity

The vectorizer uses:

- Word unigrams and bigrams
- 30,000 maximum features
- Minimum document frequency of 3
- English stop words

The vectorizer is fitted only on training resumes and job descriptions. Row-wise cosine similarity gives one score for each pair.

Two thresholds are selected using validation macro-F1:

| Threshold | Value |
|---|---:|
| Lower threshold | 0.045 |
| Upper threshold | 0.074 |

The lower threshold separates No Fit from Potential Fit. The upper threshold separates Potential Fit from Good Fit.

### Overall Results

| Split | Macro-F1 | Accuracy | Weighted F1 |
|---|---:|---:|---:|
| Validation | 0.4174 | 0.4960 | 0.4788 |
| Test | 0.3708 | 0.4110 | 0.4132 |

### Test Class Results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Good Fit | 0.2893 | 0.2489 | 0.2676 | 458 |
| Potential Fit | 0.2638 | 0.3221 | 0.2901 | 444 |
| No Fit | 0.5662 | 0.5438 | 0.5548 | 857 |

### Test Confusion Matrix

Rows are true labels and columns are predicted labels.

| True label | Good Fit | Potential Fit | No Fit |
|---|---:|---:|---:|
| Good Fit | 114 | 144 | 200 |
| Potential Fit | 144 | 143 | 157 |
| No Fit | 136 | 255 | 466 |

## Paired TF-IDF with SGD

Every pair is joined as:

```text
resume [resume text] job [job description text]
```

The vectorizer uses:

- Word unigrams and bigrams
- 50,000 maximum features
- Minimum document frequency of 3
- Maximum document frequency of 0.98
- Sublinear term frequency
- English stop words

The classifier uses logistic loss, alpha 0.00001, and random seed 42. The vectorizer and classifier are fitted only on training data.

### Overall Results

| Split | Macro-F1 | Accuracy | Weighted F1 |
|---|---:|---:|---:|
| Validation | 0.6513 | 0.6701 | 0.6677 |
| Test | 0.4100 | 0.5088 | 0.4671 |

### Test Class Results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Good Fit | 0.5248 | 0.1616 | 0.2471 | 458 |
| Potential Fit | 0.3434 | 0.3063 | 0.3238 | 444 |
| No Fit | 0.5606 | 0.7993 | 0.6590 | 857 |

### Test Confusion Matrix

| True label | Good Fit | Potential Fit | No Fit |
|---|---:|---:|---:|
| Good Fit | 74 | 134 | 250 |
| Potential Fit | 21 | 136 | 287 |
| No Fit | 46 | 126 | 685 |

## Paper and Reproduced Results

| Model | Paper test macro-F1 | Reproduced test macro-F1 | Gap |
|---|---:|---:|---:|
| TF-IDF cosine similarity | 0.359 | 0.3708 | +0.0118 |
| Paired TF-IDF with SGD | 0.436 | 0.4100 | -0.0260 |

The paired TF-IDF with SGD model remains the better reproduced baseline.

## Figures

- [Dataset overview](figures/dataset-overview.png)
- [Split label distribution](figures/split-label-distribution.png)
- [Threshold selection](figures/threshold-selection.png)
- [Confusion matrices](figures/confusion-matrices.png)
- [Paper and reproduced result comparison](figures/result-comparison.png)

## Test Use

The official test split is not used to train the vectorizers, train the classifier, or select similarity thresholds. It is used only for final evaluation.

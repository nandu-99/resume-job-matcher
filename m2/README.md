# M2: Baseline Reproduction

## Project

This milestone reproduces two baseline methods for three-class resume-job matching:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier

The output labels are Good Fit, Potential Fit, and No Fit. Macro-F1 is the main metric.

## Anchor Paper

B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," 2025.

DOI: <https://doi.org/10.51903/jtie.v4i3.529>

## Dataset

The project uses the public `resume-job-description-fit` dataset:

<https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

The original dataset contains 6,241 training rows and 1,759 official test rows. After duplicate cleaning, 6,228 training rows remain. They are divided into 4,982 training rows and 1,246 validation rows with stratification and random seed 42.

## Main Notebook

All executable work is in one Google Colab notebook:

```text
notebooks/m2-baseline-reproduction.ipynb
```

The notebook contains dataset checks, preprocessing, reproducible splits, both baseline models, detailed evaluation, graphs, and reproduction observations.

## Final Test Results

| Model | Paper macro-F1 | Reproduced macro-F1 | Accuracy | Weighted F1 |
|---|---:|---:|---:|---:|
| TF-IDF cosine similarity | 0.359 | 0.3708 | 0.4110 | 0.4132 |
| Paired TF-IDF with SGD | 0.436 | 0.4100 | 0.5088 | 0.4671 |

## Files

```text
m2/
|-- README.md
|-- dataset-documentation.md
|-- preprocessing.md
|-- reproduction-observations.md
|-- reproduction-results.md
|-- requirements.txt
|-- figures/
|   |-- confusion-matrices.png
|   |-- dataset-overview.png
|   |-- result-comparison.png
|   |-- split-label-distribution.png
|   `-- threshold-selection.png
`-- notebooks/
    `-- m2-baseline-reproduction.ipynb
```

## Documentation

- [Dataset documentation](dataset-documentation.md)
- [Preprocessing and data splits](preprocessing.md)
- [Reproduction results](reproduction-results.md)
- [Reproduction observations](reproduction-observations.md)

## Run in Colab

1. Open the notebook in Google Colab.
2. Use the default CPU runtime.
3. Run every cell from the beginning in order.
4. Keep random seed 42.
5. Confirm that every final check passes.

The official test split must not be used for training, threshold selection, or model setting selection.

# M2: Baseline Reproduction

## Project

This milestone reproduces two baseline methods for three-class resume-job matching:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier

The three output labels are:

- Good Fit
- Potential Fit
- No Fit

## Anchor Paper

B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," 2025.

DOI: <https://doi.org/10.51903/jtie.v4i3.529>

## Dataset

The project uses the public `resume-job-description-fit` dataset:

<https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

The original dataset contains 8,000 resume-job pairs:

| Split | Rows |
|---|---:|
| Training | 6,241 |
| Test | 1,759 |

Detailed findings are recorded in [dataset-documentation.md](dataset-documentation.md).

## Main Notebook

The complete M2 work will be developed in one Google Colab notebook:

```text
notebooks/m2-baseline-reproduction.ipynb
```

The notebook contains the dataset audit, text preprocessing, and reproducible data splits. Baseline models, evaluation, and reproduction observations will be added to the same notebook.

## Current Files

```text
m2/
|-- README.md
|-- dataset-documentation.md
|-- requirements.txt
|-- figures/
|   `-- dataset-overview.png
`-- notebooks/
    `-- m2-baseline-reproduction.ipynb
```

## Paper Results to Reproduce

| Model | Paper test macro-F1 |
|---|---:|
| TF-IDF cosine similarity | 0.359 |
| Paired TF-IDF with SGD | 0.436 |

Macro-F1 is the main metric because the No Fit class is larger than the other two classes.

## Colab Instructions

1. Open the notebook in Google Colab.
2. Use the default CPU runtime.
3. Run the cells from the beginning in their given order.
4. Keep random seed 42 for all data splits and models.
5. Use the official test split only for final evaluation.

# Transformer Model Comparison

## Evaluation setup

Both models use the same dataset revision, job-grouped splits, label mapping,
512-token input policy, and training recipe. Checkpoints are selected by
validation macro-F1. Each model was trained once with seed 42.

## Findings

- MiniLM validation macro-F1: 0.3081.
- DistilBERT validation macro-F1: 0.3540.
- DistilBERT's absolute macro-F1 gain: 0.0459.
- Good Fit recall changes from 0.2643 to 0.2107.
- Potential Fit recall changes from 0.0000 to 0.1088.
- No Fit recall changes from 0.8638 to 0.8396.
- Training takes 4.66 and 4.67 minutes respectively.
- Peak PyTorch GPU allocations are 1.42 and 1.95 GB respectively.

## Interpretation

DistilBERT leads on validation macro-F1 and accuracy. MiniLM has higher Good Fit
recall. DistilBERT is the stronger candidate for further optimization under the
chosen primary metric, but both models still miss many suitable candidates.

The recorded times are single-run measurements, not a controlled inference-speed
benchmark. The official test set has not been evaluated for either transformer.

## Limitations and further investigation

Nearly all pairs require truncation, and only about 35-38% of original content
tokens remain on average. Class imbalance and lost input context are possible
contributors to the errors; their effects have not been isolated.

Test class-weighted loss and a documented section-aware input policy separately.
A direct comparison with the historical TF-IDF results also requires evaluating
that baseline approach under this same M3 split protocol.

See model_comparison.csv for the numeric comparison and model_comparison.png
for the figure. Detailed validation reports accompany each experiment.

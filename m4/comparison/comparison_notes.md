# Reference Model Evaluation

## Evaluation setup

The TF-IDF reference and both transformers use the same M3 source rows,
dataset revision, labels, and job-grouped validation split.
No jobs or prepared resume-job pairs overlap between splits.
Some resumes are shared, so this evaluates matching a largely known
candidate pool against unseen jobs.

TF-IDF retains its original baseline cleaning and uses full documents.
The transformers use their recorded preparation and 512-token truncation.
This compares complete approaches; it does not isolate architecture alone.

TF-IDF vocabulary and classifier fitting use training rows only.
The original baseline settings are retained without a validation search.

## Findings

- TF-IDF + SGD validation macro-F1: 0.2923.
- MiniLM validation macro-F1: 0.3081.
- DistilBERT validation macro-F1: 0.3540.
- DistilBERT's absolute gain over the reference: 0.0618.
- TF-IDF identifies 4 of 280 Good Fit examples and 65 of 331 Potential Fit examples.
- TF-IDF has the highest Potential Fit recall among these runs.
- MiniLM has the highest Good Fit recall.
- DistilBERT leads on macro-F1 and accuracy.

## Limitations and next steps

These are single-seed validation results, not final test results.
All approaches miss many suitable candidates.
Historical M2 test scores use a different split and are not directly comparable.

The saved TF-IDF pipeline reproduces all 1,147 validation predictions.
It expects cleaned pair text, not raw resume and job fields.

Keep this run as the fixed reference for class-weighted training and
section-aware input experiments. Select settings using validation data.
Evaluate the official test set after model selection is fixed.

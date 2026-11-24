# Model Evaluation and Selection

## Evaluation setup

The task predicts Good Fit, Potential Fit, or No Fit for resume-job pairs.
Evaluation uses the saved M3 dataset revision and job-grouped splits:
5,081 training, 1,147 validation, and 1,759 official-test pairs.
Jobs and prepared pairs do not overlap across splits, but some resumes do.
Results therefore concern largely known candidates matched against unseen jobs.

Macro-F1 is the primary selection metric. TF-IDF uses full documents with its
original cleaning; transformers use their documented 512-token input policies.
This compares complete approaches rather than architecture alone.

## Validation and improvement iterations

| Model | Validation macro-F1 | Validation accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
| --- | --- | --- | --- | --- | --- |
| DistilBERT class-weighted | 0.3582 | 0.4673 | 0.1679 | 0.1662 | 0.8097 |
| DistilBERT | 0.354 | 0.4752 | 0.2107 | 0.1088 | 0.8396 |
| DistilBERT section-aware | 0.3258 | 0.4786 | 0.05 | 0.1813 | 0.8862 |
| MiniLM | 0.3081 | 0.4682 | 0.2643 | 0.0 | 0.8638 |
| TF-IDF + SGD | 0.2923 | 0.4429 | 0.0143 | 0.1964 | 0.819 |

Section-aware preparation reduced macro-F1 relative to original DistilBERT.
Class weighting with original inputs produced a small 0.0042 validation gain.
These are single-seed experiments, with class-recall trade-offs.

## Frozen selection and official-test results

The weighted DistilBERT model was selected by validation macro-F1 before test
inference. Its weight hash, input policy, fixed comparators, and decision are
recorded in [model_selection.json](model_selection.json).
No threshold tuning or model reselection followed test evaluation.

| Model | Role | Test macro-F1 | Test accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
| --- | --- | --- | --- | --- | --- | --- |
| DistilBERT class-weighted | Selected | 0.3563 | 0.4304 | 0.1921 | 0.2342 | 0.6593 |
| DistilBERT | Fixed comparator | 0.3626 | 0.4929 | 0.2555 | 0.0856 | 0.8308 |
| TF-IDF + SGD | Fixed comparator | 0.4058 | 0.5009 | 0.1856 | 0.2658 | 0.7911 |

TF-IDF has the highest official-test macro-F1 among the fixed comparisons.
The weighted model's validation advantage over original DistilBERT does not
carry over to the test set. Transformer superiority is not established.

The selected model correctly identifies 88 of 458 Good Fit examples and
104 of 444 Potential Fit examples. It predicts No Fit for 221 Good Fit and
254 Potential Fit examples. These failures limit its usefulness for screening.
The recorded evaluation selection remains unchanged.

## Error review

Across validation, weighting fixes 59 original errors but introduces 68 regressions.
The qualitative review covers 30 deliberately balanced cases across 19 unique
job texts. Four Potential Fit regressions share one job, so observations are
correlated and category counts are not population prevalence estimates.

[Review findings](error_review_findings.md) describe specialist requirements,
label/evidence tensions, missing context, and text-quality issues.
This assistant-assisted review does not establish model causation or replace
recruiter adjudication. Dataset labels remain unchanged.

## Robustness testing

Tests use 300 validation pairs, with 100 per class. Whitespace and ASCII-case
changes yield identical tokenized inputs; their predictions are reused.
This verifies preparation behaviour rather than semantic model robustness.

| Model | Variant | Changed inputs | Change rate (%) | Change rate on changed inputs (%) |
| --- | --- | --- | --- | --- |
| DistilBERT | block_order | 300 | 15.67 | 15.67 |
| DistilBERT | skills_removed | 133 | 4.33 | 9.77 |
| DistilBERT | long_prefix | 300 | 26.67 | 26.67 |
| DistilBERT class-weighted | block_order | 300 | 22.67 | 22.67 |
| DistilBERT class-weighted | skills_removed | 133 | 4.67 | 10.53 |
| DistilBERT class-weighted | long_prefix | 300 | 31.0 | 31.0 |

Block-order tests reverse newline-separated blocks. Skills removal uses the
recorded heading rules, changing prepared text in 234 cases but tokenized input
in only 133. Long-prefix tests prepend 80 repetitions of review boilerplate
to the resume. These are diagnostic stress tests, not ordinary traffic estimates.

The weighted model changes more predictions in all three stress tests.
Prediction changes are sensitivity measurements, not automatically errors;
content removal can change the information needed to judge suitability.

## Inference measurements

| Model | Batch size | Median batch ms | P95 batch ms | Examples per second | Peak allocated GB | Additional peak GB |
| --- | --- | --- | --- | --- | --- | --- |
| DistilBERT class-weighted | 1 | 8.804 | 22.064 | 93.596 | 0.282 | 0.014 |
| DistilBERT class-weighted | 16 | 47.271 | 48.602 | 337.781 | 0.431 | 0.164 |
| DistilBERT | 1 | 10.185 | 14.229 | 94.673 | 0.282 | 0.014 |
| DistilBERT | 16 | 47.894 | 52.491 | 330.391 | 0.431 | 0.164 |

Both saved models are measured separately on one T4 with FP16 autocast,
three warmup batches, and 30 timed repeats at batch sizes 1 and 16.
Inputs are already on the GPU. Timings exclude preparation, tokenization,
transfers, API handling, and output processing.
Memory is PyTorch allocation in 1024^3-byte units, not total device usage.

The models have the same architecture and similar measurements. One run does
not establish a speed advantage. CPU and end-to-end application performance
remain unmeasured.

## Limitations and further use

Findings depend on one seed, one dataset, shared resumes, substantial truncation,
and labels that need further review. The small validation gain is not evidence
of a reliable improvement or business impact. Suitable-candidate recall remains low.

Use the model only as a prototype with human review. Keep the frozen assessment
separate from future experiments; further tuning requires independent evaluation.

## Reproduction and evidence

Use the saved notebook, pinned dataset revision, M3 split archive, recorded
package versions, M3 transformer reports, and original DistilBERT model archive.
Keep trained models and the text-containing review CSV outside the reports archive.

The selection record predates test inference. Prediction CSVs, class reports,
confusion matrices, robustness records, and raw inference timings support
the reported calculations. See [the evaluation figure](figures/final_evaluation.png).

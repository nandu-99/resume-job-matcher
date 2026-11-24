# Evaluation and Optimization

Evaluation uses the shared M3 job-grouped splits for the TF-IDF reference, section-aware DistilBERT inputs, and class-weighted DistilBERT training. The reference evaluation reruns paired TF-IDF with SGD on these splits. This provides a validation comparison with MiniLM and DistilBERT using the same source rows. Earlier M2 results use a different split and remain historical results.

## Files

| File | Purpose |
|---|---|
| [Reference evaluation notebook](notebooks/m4-reference-evaluation.ipynb) | Uploaded Colab notebook, including executed cells and outputs, unchanged |
| [Reference experiment reports](experiments/tfidf-sgd-v1/) | Configuration, metrics, class report, confusion matrix, validation predictions, preparation checks, and reload verification |
| [Experiment log](experiment-log.csv) | Reference, section-aware, and class-weighted run summaries, measured results, and timings |
| [Comparison notes](comparison/comparison_notes.md) | Findings, approach differences, and limitations |
| [Comparison CSV](comparison/reference_model_comparison.csv) | Exact validation scores for all three approaches |
| [Comparison figure](comparison/reference_model_comparison.png) | Macro-F1 and class recall comparison |
| [Section-aware notebook](notebooks/m4-section-aware-inputs.ipynb) | Uploaded Colab continuation with section preparation, training, and saved checks unchanged |
| [Section-aware experiment reports](experiments/distilbert-section-v1/) | Input policy, training settings, section audits, selected-checkpoint validation reports, and reload checks |
| [Input-policy comparison](comparison/section-aware-v1/comparison_notes.md) | Original versus section-aware DistilBERT results, decision, CSV, and figure |
| [Class-weighted notebook](notebooks/m4-class-weighted-distilbert.ipynb) | Uploaded continuation with original-input reconstruction, weighted training, and export checks unchanged |
| [Class-weighted experiment reports](experiments/distilbert-weighted-v1/) | Class weights, run settings, input audit, history, validation evidence, and reload check |
| [Loss comparison](comparison/class-weighted-v1/comparison_notes.md) | Original versus weighted loss results, trade-offs, CSV, and figure |

The reference notebook and all 12 files from its uploaded reports archive are preserved unchanged. The section-aware notebook and all 17 files from its reports archive are also preserved unchanged. The class-weighted notebook and all 14 files from its reports archive are preserved unchanged. The report folders contain source row identifiers and labels rather than resume or job text. Trained model files and downloaded ZIPs stay outside Git.

## Shared evaluation protocol

The dataset is `cnamuangtoun/resume-job-description-fit`, revision `08978e21714984bb417547d2c0f9b477f5298163`. The notebook reconstructs the saved source row identifiers from the [M3 split manifest](../m3/splits/split_manifest.json), verifies the class counts, and repeats the M3 preparation and overlap checks.

Training has 5,081 rows, validation 1,147, and the official test 1,759. No jobs or prepared resume-job pairs overlap between splits. Some resumes are shared, so results describe a largely known candidate pool matched against unseen jobs. The configuration stores a SHA-256 hash of the canonical, sorted JSON representation of the manifest.

## Reference model

The reference retains the original M2 baseline cleaning and model settings. Raw text is lowercased, contact details are replaced, unwanted characters are removed, and whitespace is normalised. Pairs use `resume {cleaned_resume} job {cleaned_job}`. Full documents are retained without token truncation.

TF-IDF uses word unigrams and bigrams, up to 50,000 features, `min_df=3`, `max_df=0.98`, English stop words, and sublinear term frequency. The vectorizer fits only the training pairs. `SGDClassifier` uses logistic loss, `alpha=0.00001`, and seed 42. Its remaining settings are recorded in [reference_config.json](experiments/tfidf-sgd-v1/reference_config.json); no validation parameter search is performed.

The run learns 50,000 vocabulary entries and takes 48 classifier iterations. Vectorization takes 16.63 seconds, including the validation transform, and classifier fitting takes 6.66 seconds in the recorded CPU runtime. These are single-run measurements, not inference benchmarks or hardware-matched transformer speed comparisons.

## Validation results

| Model | Macro-F1 | Accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
|---|---:|---:|---:|---:|---:|
| TF-IDF + SGD | 0.2923 | 0.4429 | 0.0143 | 0.1964 | 0.8190 |
| MiniLM | 0.3081 | 0.4682 | 0.2643 | 0.0000 | 0.8638 |
| DistilBERT | 0.3540 | 0.4752 | 0.2107 | 0.1088 | 0.8396 |

The reference correctly classifies 508 of 1,147 validation pairs. It identifies 4 of 280 Good Fit examples, 65 of 331 Potential Fit examples, and 439 of 536 No Fit examples. Predicted counts are 35 Good Fit, 196 Potential Fit, and 916 No Fit.

DistilBERT leads on macro-F1 by 0.0618 absolute over the reference. MiniLM has the highest Good Fit recall, while TF-IDF has the highest Potential Fit recall among these runs. All three miss many suitable candidates.

The notebook imports transformer reports and checks their dataset revision, seed, split counts, and labels. The comparison uses common validation rows, while preprocessing and available document content differ across approaches. It compares complete approaches and does not isolate the effect of architecture. These are single-seed validation results. The official test set is not evaluated in this contribution.

## Reproduction and saved model

1. Open the reference notebook in a Colab CPU runtime. The recorded environment is Python 3.13.16, NumPy 2.4.6, pandas 2.2.3, scikit-learn 1.6.1, and Datasets 4.8.5. Full model settings are in the configuration.
2. Run cells in order and upload `m3_data_setup.zip` when prompted. It contains the three existing files under `m3/splits/` at the archive root.
3. Confirm source row counts, preparation checks, and zero job/pair overlap before fitting. The training-only vectorizer and original classifier settings produce the reference result.
4. Upload `minilm_v1_reports.zip` and `distilbert_v1_reports.zip` together when prompted. The comparison reads the recorded M3 metrics without retraining the transformers.
5. Check the saved-report verification and model reload outputs. The notebook writes files beneath `/content/m4_reference/tfidf_sgd_v1/` and downloads `tfidf_sgd_v1_reports.zip` and `tfidf_sgd_v1_model.zip`.

The model archive contains a fitted TF-IDF/classifier pipeline and its configuration. Its input is cleaned pair text produced by `baseline_clean_text` and `create_baseline_pairs` in the notebook. It does not include raw-field cleaning inside the saved pipeline. Keep the model archive separately for later use.

The [reload report](experiments/tfidf-sgd-v1/reload_check.json) records equal vocabulary and classifier weights and identical predictions across all 1,147 validation examples. This checks export integrity rather than model quality.

## Further evaluation

Use the fixed reference and recorded original DistilBERT results when assessing further changes. Keep class-weighted training separate from the section-aware input experiment. Categorise validation errors, test robustness, and measure inference performance. Freeze model and preparation settings before official-test evaluation. The recorded section-aware policy is not selected because it lowers macro-F1.

## Section-aware input experiment

The [section-aware notebook](notebooks/m4-section-aware-inputs.ipynb) continues the reference notebook, so it includes the earlier CPU reference work before the transformer cells. The uploaded code and outputs are unchanged. The existing reference notebook remains a separate reference.

The experiment starts from the same pretrained DistilBERT revision, `12040accade4e8a0f71eabdb258fecc2e7e948be`, rather than continuing a fine-tuned model. Training arguments match the original DistilBERT run except for the output directory. Both use seed 42, unweighted cross-entropy, effective batch size 16, learning rate 0.00002, FP16, a three-epoch limit, validation macro-F1 selection, and early-stopping patience one. This keeps class weighting out of the input-policy comparison.

### Input policy and audits

The shared M3 text preparation is followed by heading detection. Training-only inspection revealed headings joined to content, such as `SkillsGuest services`, so detection supports joined headings and same-line content. The final rules recognise headings in 632 of 632 unique training resumes and 156 of 229 unique training jobs. Recognition coverage is not a manual accuracy score for section boundaries.

The policy adds section labels and prioritises skills, experience, summary, education, projects, and certifications in resumes. Job inputs prioritise requirements and responsibilities. Initial content budgets are 304 resume tokens and 205 job tokens, with three pair special tokens. Each document receives section quotas first; unused space is filled in priority order and can be reassigned between documents. Unrecognised lines stay in the current section or preamble. Documents with no recognised headings use their preamble text.

Only training and validation documents are prepared with this policy. The cache holds 642 unique resume texts and 280 unique job texts across those splits; 93 job texts use preamble-only fallback. These exact-text counts differ from grouping counts because group identifiers collapse case and whitespace.

The [input configuration](experiments/distilbert-section-v1/section_input_config.json) records the regular expressions, priorities, quotas, package versions, and canonical manifest hash. The [allocation report](experiments/distilbert-section-v1/section_allocation.csv) records per-pair section token counts without document text. Every input fits within 512 tokens. Mean selected resume/job token counts are 316.40/192.44 for training and 327.51/181.30 for validation. Counts include inserted section labels and do not measure original-content retention. Dynamic-padding checks use an `(8, 512)` batch with 485 padding tokens and integer labels.

### Measured results and decision

The run reaches three epochs and 954 optimizer updates. Epoch 2, `checkpoint-636`, has the highest validation macro-F1. Training takes 275.77 seconds, about 4.60 minutes, with peak PyTorch GPU allocation of 1.95 GB. These are recorded single-run training measurements.

| Input policy | Validation macro-F1 | Accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
|---|---:|---:|---:|---:|---:|
| Original longest_first | 0.3540 | 0.4752 | 0.2107 | 0.1088 | 0.8396 |
| Section-aware v1 | 0.3258 | 0.4786 | 0.0500 | 0.1813 | 0.8862 |

Macro-F1 falls by 0.0282 absolute. The section-aware model correctly identifies 14 of 280 Good Fit examples, 60 of 331 Potential Fit examples, and 475 of 536 No Fit examples. It predicts 57 Good Fit, 138 Potential Fit, and 952 No Fit pairs. The small accuracy gain does not offset the macro-F1 and Good Fit recall losses, so the original input policy remains the stronger candidate.

See the [metrics](experiments/distilbert-section-v1/validation_metrics.json), [confusion matrix](experiments/distilbert-section-v1/validation_confusion_matrix.csv), and [comparison notes](comparison/section-aware-v1/comparison_notes.md). The [comparison CSV](comparison/section-aware-v1/input_policy_comparison.csv) and [figure](comparison/section-aware-v1/input_policy_comparison.png) preserve the numeric and visual evidence. This is an unsuccessful improvement iteration rather than evidence that section-aware methods cannot help.

The policy changes section selection, ordering, inserted labels, and document budget allocation together. The experiment does not isolate their individual effects. Heading rules can misinterpret unusual formats, and no specific cause of the score decrease has been established. These are single-seed validation results. Neither the original nor section-aware transformer is evaluated on official test labels here; the section policy does not process official test documents.

### Reproduction and model storage

1. Use a fresh Colab T4 runtime with the recorded package versions. The environment installation cell appears after the reference cells in this continuation notebook; prepare the environment before the full run if needed, and restart if loaded versions differ from installed versions.
2. Run the notebook in order. Upload `m3_data_setup.zip` and both M3 transformer reports archives when prompted by the reference workflow. The section-aware workflow reuses the DistilBERT archive if it is still available.
3. Verify split counts, overlaps, parser checks, section allocations, and batch shapes before training. Run the training cell once per independent experiment, starting from the pretrained checkpoint.
4. Review selected-checkpoint validation and export checks. The notebook writes to `/content/m4_training/distilbert_section_v1/` and downloads `distilbert_section_v1_reports.zip` and `distilbert_section_v1_model.zip`.
5. Keep the model archive separately. It contains model weights, tokenizer files, and the input configuration. Loading the checkpoint alone does not apply section preparation: inference also needs the notebook's `prepare_text`, heading parsing, section extraction, selection, and pair-building functions with the recorded policy.

The [reload check](experiments/distilbert-section-v1/reload_check.json) confirms exact equality of all 104 state tensors, matching tokenizer/labels and input configuration, and zero logit difference on two validation examples under aligned FP16 autocast. This verifies export integrity. Repository validation checks the saved artifacts and calculations without repeating GPU training.

## Class-weighted DistilBERT experiment

The [class-weighted notebook](notebooks/m4-class-weighted-distilbert.ipynb) continues the earlier notebook and retains the reference and section-aware work before adding weighted training. It is copied unchanged from the uploaded Colab notebook. Earlier notebooks, reports, and comparisons remain unchanged.

### Inputs, weights, and training

Weighted training starts from the same original pretrained DistilBERT revision as M3, not either fine-tuned model. It rebuilds the original resume-first/job-second input pairs using `longest_first`, a 512-token limit, and dynamic padding to a multiple of eight. Section selection is not applied. Training and validation labels and source row order match the saved M3 splits. The input audit records minimum lengths of 334 and 437, maximum lengths of 512, and an `(8, 512)` mixed-length batch with 475 padding tokens.

Weights use training labels only: `training_rows / (number_of_classes * class_count)`.

| Label | Training examples | Class weight |
|---|---:|---:|
| Good Fit | 1,258 | 1.3463 |
| Potential Fit | 1,223 | 1.3848 |
| No Fit | 2,600 | 0.6514 |

The [configuration](experiments/distilbert-weighted-v1/weighted_run_config.json) records the exact float32 weights used, training counts, input policy, revisions, canonical manifest hash, and environment versions. The [weight report](experiments/distilbert-weighted-v1/class_weights.csv) contains the calculated values before the float32 conversion.

`ClassWeightedTrainer` computes cross-entropy as a weighted mean within each microbatch. It excludes labels from the model forward call, computes loss from float32 logits, and sets `model_accepts_loss_kwargs=False` so Trainer handles gradient accumulation. A synthetic example verifies the weighted loss against a manual calculation. The custom loss path and its normalisation are part of this experiment; weighted and unweighted loss values are not directly comparable.

Saved training arguments match the original DistilBERT run except the output directory: seed 42, three maximum epochs, effective batch size 16, learning rate 0.00002, FP16, validation macro-F1 selection, and early-stopping patience one. The run reaches 954 optimizer updates and selects epoch 2, `checkpoint-636`. Recorded training wall time is 307.42 seconds, about 5.12 minutes, with peak PyTorch GPU allocation of 1.95 GB. These are single-run training measurements rather than inference benchmarks.

### Validation result and trade-offs

| Training loss | Macro-F1 | Accuracy | Good Fit recall | Potential Fit recall | No Fit recall |
|---|---:|---:|---:|---:|---:|
| Unweighted cross-entropy | 0.3540 | 0.4752 | 0.2107 | 0.1088 | 0.8396 |
| Class-weighted cross-entropy | 0.3582 | 0.4673 | 0.1679 | 0.1662 | 0.8097 |

The weighted run improves validation macro-F1 by 0.0042 absolute. It correctly identifies 47 of 280 Good Fit examples, 55 of 331 Potential Fit examples, and 434 of 536 No Fit examples. Predicted counts are 160 Good Fit, 166 Potential Fit, and 821 No Fit.

The [class report](experiments/distilbert-weighted-v1/validation_class_report.csv), [confusion matrix](experiments/distilbert-weighted-v1/validation_confusion_matrix.csv), and [comparison notes](comparison/class-weighted-v1/comparison_notes.md) show the trade-off. Potential Fit recall improves while Good Fit recall, No Fit recall, and accuracy decrease. The [CSV](comparison/class-weighted-v1/loss_comparison.csv) and [figure](comparison/class-weighted-v1/loss_comparison.png) preserve the comparison.

This is the highest recorded validation macro-F1 among these DistilBERT variants, but the gain is small and comes from one seed. It does not establish a reliable improvement or a final deployment choice. Keep both original-input candidates available for error analysis, robustness checks, and inference measurements. Freeze the selection before official-test evaluation; the official test remains unevaluated in this contribution.

### Reproduction and export

Use a fresh Colab T4 runtime with the recorded package versions and the shared data-setup archive. The uploaded continuation includes the earlier reference and section-aware cells and their archive prompts. Prepare dependencies before the full run if needed. Weighted cells explicitly rebuild original inputs and move the finished section-aware model and optimizer state to CPU before loading a fresh pretrained model. Run each training cell once per independent experiment.

The notebook writes artifacts under `/content/m4_training/distilbert_weighted_v1/` and downloads `distilbert_weighted_v1_reports.zip` and `distilbert_weighted_v1_model.zip`. Keep model weights separately from Git. The model archive contains the classifier, tokenizer, and weighted-run configuration. Inference uses the original M3 `prepare_text` function and paired tokenization. Class weights and the custom trainer are needed for training reproduction rather than ordinary prediction.

The [reload check](experiments/distilbert-weighted-v1/reload_check.json) records exact equality of 104 state tensors, matching tokenizer/labels and configuration, and zero logit difference on two validation examples under aligned FP16 autocast. This checks export integrity. Handoff validation checks saved reports and calculations without repeating GPU training or inference.

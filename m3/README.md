# Model Development

The transformer experiments use a shared data-preparation workflow before tokenization and training. The [notebook](notebooks/m3-model-development.ipynb) records the Colab environment, audits the data, prepares model text, and creates reproducible job-grouped splits for MiniLM and DistilBERT.

## Files

| File | Purpose |
|---|---|
| [Model-development notebook](notebooks/m3-model-development.ipynb) | Uploaded Colab notebook with its executed cells and saved outputs unchanged |
| [Split manifest](splits/split_manifest.json) | Dataset revision, source row identifiers, splitter settings, labels, and environment versions |
| [Split counts](splits/split_counts.csv) | Rows and class counts for each split |
| [Split overlap](splits/split_overlap.csv) | Shared jobs, resumes, and pairs between splits |
| [Transformer-input notebook](notebooks/m3-transformer-models.ipynb) | Uploaded notebook with executed preparation, tokenization, and batch checks unchanged |
| [Tokenization configuration](tokenization/tokenization_config.json) | Model revisions, label mapping, input policy, and package versions |
| [Input lengths](tokenization/input_lengths.csv) | Untruncated training and validation token statistics |
| [Tokenization report](tokenization/tokenization_report.csv) | Tokenized row counts, lengths, and training/validation retention |
| [Batch report](tokenization/batch_report.csv) | Dynamic-padding checks and label tensor types |
| [MiniLM fine-tuning notebook](notebooks/m3-minilm-finetuning.ipynb) | Uploaded training notebook and saved outputs unchanged |
| [Experiment log](experiment-log.csv) | Comparable run summaries using the shared M3 split protocol |
| [MiniLM experiment evidence](experiments/minilm-v1/) | Training history, selected-checkpoint validation reports, run settings, and reload checks |
| [DistilBERT fine-tuning notebook](notebooks/m3-distilbert-finetuning.ipynb) | Uploaded Colab notebook with training, export checks, and comparison outputs unchanged |
| [DistilBERT experiment evidence](experiments/distilbert-v1/) | Training history, validation reports, run settings, and reload checks |
| [Model comparison](comparison/comparison_notes.md) | Findings with the numeric comparison and figure |

The three split files are the extracted contents of the Colab setup archive. The ZIP is not duplicated in the repository. No resume or job-description records are included in these artifacts.

## Data preparation

The source is `cnamuangtoun/resume-job-description-fit`, revision `08978e21714984bb417547d2c0f9b477f5298163`. It has 6,241 original training rows and 1,759 official test rows.

Preparation removes all 12 rows from six conflicting-label pair groups and one extra same-label copy. This leaves a training pool of 6,228 rows. The official test records and labels remain unchanged.

Transformer text preparation normalises Unicode and whitespace, keeps visible Markdown link text, and replaces emails, URLs, and phone numbers. It preserves case, line breaks, and technical punctuation such as C++, C#, and .NET. It does not fully anonymise resumes.

## Shared split design

The notebook groups job descriptions by a SHA-256 identifier of their prepared text after case-folding and whitespace normalisation. It uses the first fold of `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` as validation. This is a single held-out split, not five separate training runs.

| Split | Good Fit | Potential Fit | No Fit | Total | Unique jobs |
|---|---:|---:|---:|---:|---:|
| Training | 1,258 | 1,223 | 2,600 | 5,081 | 229 |
| Validation | 280 | 331 | 536 | 1,147 | 51 |
| Official test | 458 | 444 | 857 | 1,759 | 71 |

Validation contains 18.4% of the cleaned training pool. Whole-job grouping determines the exact size. No jobs or prepared resume-job pairs are shared across splits. Original-text duplicate checks and prepared-pair checks also pass.

Resumes are shared: 429 unique resumes between training and validation, 473 between training and test, and 357 between validation and test. This reflects new jobs matched against a largely known candidate pool; it does not establish performance on entirely new applicants.

The historical M2 split has different counts. Use these M3 splits consistently for candidate selection and document any comparison with the historical results separately.

## Run the data setup in Colab

1. Open the notebook in a GPU runtime. The recorded run used a Tesla T4 with 14.6 GB GPU memory.
2. Run the cells in order. Internet access is required for packages and the public dataset.
3. Compare the dataset revision with the saved manifest before accepting regenerated artifacts. The uploaded notebook resolves the current Hub revision when it starts; the manifest fixes the revision used for the recorded results.
4. Confirm the row counts, zero job/pair overlap, and exact split reconstruction checks.
5. Download the notebook and setup archive when saving the Colab session. The notebook writes artifacts under `/content/m3_artifacts` and downloads `/content/m3_data_setup.zip`.

The recorded runtime was Python 3.13.16 with NumPy 2.4.6, pandas 2.2.3, Datasets 4.8.5, scikit-learn 1.6.1, and PyTorch 2.14.1+cu130. The full versions are in the manifest. The existing `m2/requirements.txt` describes the historical baseline environment rather than this Colab run.

## Reuse for model training

Keep the same dataset revision, preparation functions, source row identifiers, and labels for both transformer models. Source row identifiers refer to positions in the original dataset splits, before cleaning or resetting indexes. Training and validation identifiers both refer to the original `train` split; test identifiers refer to `test`.

Rebuild the prepared pool, select rows by their saved identifiers in the recorded order, and verify the split counts and overlap. Use validation to select settings and leave official test labels out of training and model selection. The recorded notebook verifies that saved identifiers reconstruct every split exactly.

The transformer-input notebook reconstructs these exact source rows and prepares both models' inputs. The MiniLM fine-tuning experiment described below uses these datasets and collators. The input-preparation notebook remains a separate, unchanged reference.

## Transformer input preparation

The [transformer notebook](notebooks/m3-transformer-models.ipynb) starts in a fresh Colab GPU runtime. It uses the recorded dataset revision and the existing split manifest rather than generating another split. It checks the class counts, unique jobs, shared resumes, and zero job/pair overlap against the saved reports before tokenization.

The split manifest included in the uploaded tokenization archive matches [splits/split_manifest.json](splits/split_manifest.json). The repository keeps that single canonical copy. The four tokenization files are copied unchanged from the archive; neither the ZIP nor a second split manifest is added.

### Models and labels

| Model | Checkpoint | Architecture | Actual input limit | Token-type IDs |
|---|---|---|---:|---|
| MiniLM | `microsoft/MiniLM-L12-H384-uncased` | BERT | 512 | Included |
| DistilBERT | `distilbert/distilbert-base-uncased` | DistilBERT | 512 | Omitted |

The exact checkpoint revisions are recorded in the tokenization configuration. The notebook checks positional limits from each model configuration, including MiniLM's missing tokenizer limit metadata.

Both models use the same label mapping: `Good Fit: 0`, `Potential Fit: 1`, and `No Fit: 2`.

### Input policy and limitations

Resume text is the first sequence and job-description text is the second. The tokenizer uses `longest_first` truncation from the right, with a combined limit of 512 tokens including special tokens. Padding is deferred until batch collation and rounded to a multiple of eight.

| Measurement | Training | Validation |
|---|---:|---:|
| Mean resume tokens before truncation | 1,153.7 | 1,169.9 |
| Mean job tokens before truncation | 530.9 | 404.0 |
| Median pair tokens before truncation | 1,576 | 1,443 |
| Pairs above 512 tokens | 99.63% | 99.39% |
| Mean original content tokens retained | 34.76% | 37.84% |

Both tokenizers produced the same reported lengths. Retention measures the fraction of content tokens kept per pair, not the amount of useful meaning preserved. The policy discards substantial text and needs to be considered when interpreting later model results. Test inputs use the fixed policy; test retention was not audited to choose the policy and is intentionally blank in the report.

Tokenized datasets retain 5,081 training rows, 1,147 validation rows, and 1,759 test rows per model. Checks verify input lengths, attention-mask lengths, label order, required fields, and architecture-specific token-type IDs. Mixed-length sample batches for both models have shape `(8, 512)`, 475 padding tokens, and `torch.int64` labels. These are input-pipeline checks, not model accuracy results.

### Run the transformer notebook

1. Use a fresh GPU runtime, then run the notebook cells in order. Its setup cell pins Transformers 5.24.0, Hugging Face Hub 1.33.0, and Accelerate 1.15.0 alongside the data libraries. Keep Colab's compatible PyTorch installation; the recorded run used PyTorch 2.14.1+cu130 and a T4.
2. When prompted, upload `m3_data_setup.zip` from the data-setup notebook. It contains the three canonical files under `m3/splits/` at the ZIP root.
3. Confirm that reconstructed counts and overlap match the saved reports before accepting tokenized inputs.
4. Compare resolved model revisions with [tokenization_config.json](tokenization/tokenization_config.json). The uploaded notebook resolves revisions when it starts; use the recorded revisions as the reference for repeatable experiments.
5. Inspect the length, retention, and batch reports. The notebook downloads `m3_tokenization_setup.zip` after checking that the exported settings and reports round-trip correctly.
6. Save the notebook and archive. Keep the runtime connected when continuing into fine-tuning, since `tokenized_datasets` and `collators` are in memory.

Tokenization and collation settings are stored in the configuration; complete package versions are also recorded there. Tokenized sequences and resume/job text are not exported in these repository artifacts. The original M1/M2 notebooks and the data-setup notebook remain unchanged.

## MiniLM fine-tuning

The [training notebook](notebooks/m3-minilm-finetuning.ipynb) fine-tunes all 33,361,155 parameters of `microsoft/MiniLM-L12-H384-uncased`, including a newly initialised three-class head. It builds on the shared split and input policy without changing either earlier notebook. Its code and saved outputs are copied unchanged from the uploaded Colab notebook.

### Training setup

| Setting | Recorded value |
|---|---|
| Model revision | `44acabbec0ef496f6dbc93adadea57f376b7c0ec` |
| Data | Shared M3 splits: 5,081 training, 1,147 validation, 1,759 test rows |
| Input policy | 512 tokens, `longest_first`, dynamic padding |
| Training batch size | 8 |
| Gradient accumulation | 2; effective batch size 16 |
| Optimizer | AdamW; learning rate 0.00002; weight decay 0.01 |
| Loss | Unweighted cross-entropy |
| Precision | FP16 mixed precision |
| Warmup | 96 optimizer updates, followed by linear learning-rate decay |
| Epoch limit | 3 |
| Checkpoint selection | Highest validation macro-F1 after each epoch |
| Early stopping | Patience of one evaluation without improvement |
| Seed | 42 |

The run reached three epochs and 954 optimizer updates. Training wall time was 279.61 seconds, about 4.66 minutes, with a peak PyTorch GPU allocation of 1.42 GB. This allocation is not a measurement of total device memory use by every process.

### Validation results

| Epoch | Validation loss | Accuracy | Macro-F1 | Good Fit recall | Potential Fit recall | No Fit recall |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1.0458 | 0.4673 | 0.2123 | 0.0000 | 0.0000 | 1.0000 |
| 2 | 1.0560 | 0.4682 | 0.3081 | 0.2643 | 0.0000 | 0.8638 |
| 3 | 1.0312 | 0.4664 | 0.3042 | 0.2500 | 0.0000 | 0.8675 |

The selected checkpoint is epoch 2, `checkpoint-636`, because selection uses macro-F1 rather than validation loss. Its exact validation macro-F1 is 0.3081366354246464. The [metrics](experiments/minilm-v1/validation_metrics.json), [class report](experiments/minilm-v1/validation_class_report.csv), and [confusion matrix](experiments/minilm-v1/validation_confusion_matrix.csv) describe that selected checkpoint; the [history](experiments/minilm-v1/training_history.csv) contains all recorded evaluations and training logs.

The selected model predicts Good Fit for 271 validation pairs and No Fit for 876, with no Potential Fit predictions. It correctly identifies 74 of 280 Good Fit examples and 463 of 536 No Fit examples. This class-level failure must remain visible when selecting a final model. The experiment does not establish an improvement, and its grouped-validation score cannot be compared directly with historical M2 test scores from a different split protocol. The effect of class imbalance, input truncation, and other possible causes needs a controlled comparison rather than an assumed explanation.

No official-test predictions or metrics were produced for this MiniLM run. Tokenizing test inputs in the shared input workflow is separate from evaluating a trained model on test labels.

### Reproduction and saved model

1. Open the fine-tuning notebook in a fresh Colab T4 runtime and run its environment and data-reconstruction cells. Upload the data-setup ZIP when prompted and verify the shared split checks.
2. Reuse the model and tokenizer revisions recorded in the shared [tokenization configuration](tokenization/tokenization_config.json). The copy in the uploaded reports is identical, so the repository keeps one canonical copy.
3. Follow the forward-pass check, throughput benchmark, training configuration, and training cells in order. The benchmark does not perform optimizer steps. Run the training cell once per experiment; rerunning it without reinitialising the model is not an independent repeat.
4. Validate the selected checkpoint, then export the model and reports. The notebook writes them beneath `/content/m3_training/minilm/` and downloads `minilm_v1_model.zip` and `minilm_v1_reports.zip`.
5. Keep model weights in local or approved artifact storage. They are not included in this repository. To use the trained model later, extract the model ZIP into a folder and load that folder with `AutoModelForSequenceClassification.from_pretrained` and `AutoTokenizer.from_pretrained`.

The [training arguments](experiments/minilm-v1/training_arguments.json) and [run summary](experiments/minilm-v1/run_summary.json) record the actual run. [Reload verification](experiments/minilm-v1/reload_check.json) confirms that all 201 saved state tensors match the Trainer model exactly, the tokenizer and labels match, and logits match on two validation examples under aligned FP16 autocast. The maximum recorded logit difference is zero. This checks export integrity, not model quality.

The [experiment log](experiment-log.csv) records both transformer runs. Any targeted improvement should use the same shared data protocol and report measured class-level trade-offs before a model is selected for deployment.

## DistilBERT fine-tuning and comparison

The [DistilBERT notebook](notebooks/m3-distilbert-finetuning.ipynb) contains the shared preparation workflow, the MiniLM reference run, DistilBERT training, export verification, and the model comparison. It is copied unchanged from the uploaded Colab notebook. The earlier notebooks remain separate references.

DistilBERT uses revision `12040accade4e8a0f71eabdb258fecc2e7e948be` and fine-tunes all 66,955,779 parameters. Its [training arguments](experiments/distilbert-v1/training_arguments.json) match MiniLM's except for the output directory, including three maximum epochs, seed 42, unweighted cross-entropy, effective batch size 16, learning rate 0.00002, FP16, and validation macro-F1 selection. Both use early-stopping patience one. MiniLM and its optimizer tensors were moved to CPU before measuring DistilBERT GPU use.

The run reached three epochs and 954 optimizer updates. Epoch 2, `checkpoint-636`, has the highest validation macro-F1. The [history](experiments/distilbert-v1/training_history.csv), [metrics](experiments/distilbert-v1/validation_metrics.json), and [confusion matrix](experiments/distilbert-v1/validation_confusion_matrix.csv) preserve the measured results.

| Model | Validation macro-F1 | Accuracy | Good Fit recall | Potential Fit recall | No Fit recall | Training minutes | Peak GPU GB |
|---|---:|---:|---:|---:|---:|---:|---:|
| MiniLM | 0.3081 | 0.4682 | 0.2643 | 0.0000 | 0.8638 | 4.66 | 1.42 |
| DistilBERT | 0.3540 | 0.4752 | 0.2107 | 0.1088 | 0.8396 | 4.67 | 1.95 |

DistilBERT improves validation macro-F1 by 0.0459 absolute and predicts all three classes. It correctly identifies 59 of 280 Good Fit examples, 36 of 331 Potential Fit examples, and 450 of 536 No Fit examples. MiniLM retains higher Good Fit recall. DistilBERT is the stronger candidate for further experiments under macro-F1, while the low suitable-candidate recalls still need attention.

The [comparison notes](comparison/comparison_notes.md), [CSV](comparison/model_comparison.csv), and [figure](comparison/model_comparison.png) show the trade-offs. These are single-seed validation results. Recorded training times and peak PyTorch allocations are single-run measurements, not inference benchmarks. Neither transformer has official-test metrics. Historical M2 test scores use another split protocol and cannot establish which method is better on this task without a shared-protocol comparison.

### Reproduction and export

Run the uploaded notebook in order in a fresh Colab T4 runtime, uploading `m3_data_setup.zip` when prompted. The notebook includes the MiniLM run needed by its comparison cells. Check the saved dataset and checkpoint revisions against the canonical configurations when reproducing the run.

DistilBERT files are written beneath `/content/m3_training/distilbert/`; comparison files are written beneath `/content/m3_comparison/`. The notebook downloads `distilbert_v1_model.zip` and `distilbert_v1_reports.zip`, with comparison files inside the reports archive. Keep the model archive in artifact storage and load its extracted folder through `AutoModelForSequenceClassification.from_pretrained` and `AutoTokenizer.from_pretrained` when needed. Model weights and archives are excluded from this repository handoff.

The [reload check](experiments/distilbert-v1/reload_check.json) confirms exact equality of all 104 saved state tensors, matching tokenizer and label mappings, and zero logit difference on two validation examples using aligned FP16 autocast. This verifies export integrity. The duplicate tokenization configuration from the reports archive matches the canonical [configuration](tokenization/tokenization_config.json), so it is not copied again.

Further evaluation should examine class-weighted loss and section-aware inputs as separate changes, compare a TF-IDF reference under the same M3 splits, and keep official test evaluation until model selection is fixed.

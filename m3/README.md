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

The transformer-input notebook reconstructs these exact source rows and prepares both models' inputs. Model fine-tuning builds on the resulting datasets and collators; no transformer weights have been trained in this workflow yet.

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

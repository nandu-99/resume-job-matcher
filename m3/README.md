# Model Development

The transformer experiments use a shared data-preparation workflow before tokenization and training. The [notebook](notebooks/m3-model-development.ipynb) records the Colab environment, audits the data, prepares model text, and creates reproducible job-grouped splits for MiniLM and DistilBERT.

## Files

| File | Purpose |
|---|---|
| [Model-development notebook](notebooks/m3-model-development.ipynb) | Uploaded Colab notebook with its executed cells and saved outputs unchanged |
| [Split manifest](splits/split_manifest.json) | Dataset revision, source row identifiers, splitter settings, labels, and environment versions |
| [Split counts](splits/split_counts.csv) | Rows and class counts for each split |
| [Split overlap](splits/split_overlap.csv) | Shared jobs, resumes, and pairs between splits |

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

## Run in Colab

1. Open the notebook in a GPU runtime. The recorded run used a Tesla T4 with 14.6 GB GPU memory.
2. Run the cells in order. Internet access is required for packages and the public dataset.
3. Compare the dataset revision with the saved manifest before accepting regenerated artifacts. The uploaded notebook resolves the current Hub revision when it starts; the manifest fixes the revision used for the recorded results.
4. Confirm the row counts, zero job/pair overlap, and exact split reconstruction checks.
5. Download the notebook and setup archive when saving the Colab session. The notebook writes artifacts under `/content/m3_artifacts` and downloads `/content/m3_data_setup.zip`.

The recorded runtime was Python 3.13.16 with NumPy 2.4.6, pandas 2.2.3, Datasets 4.8.5, scikit-learn 1.6.1, and PyTorch 2.14.1+cu130. The full versions are in the manifest. The existing `m2/requirements.txt` describes the historical baseline environment rather than this Colab run.

## Reuse for model training

Keep the same dataset revision, preparation functions, source row identifiers, and labels for both transformer models. Source row identifiers refer to positions in the original dataset splits, before cleaning or resetting indexes. Training and validation identifiers both refer to the original `train` split; test identifiers refer to `test`.

Rebuild the prepared pool, select rows by their saved identifiers in the recorded order, and verify the split counts and overlap. Use validation to select settings and leave official test labels out of training and model selection. The recorded notebook verifies that saved identifiers reconstruct every split exactly.

Tokenization, truncation analysis, and transformer fine-tuning build on these prepared dataframes. The supplied notebook covers environment and data preparation; no transformer has been trained in this workflow yet.

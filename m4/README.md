# Evaluation and Optimization

The reference evaluation reruns paired TF-IDF with SGD on the shared M3 job-grouped splits. This provides a validation comparison with MiniLM and DistilBERT using the same source rows. Earlier M2 results use a different split and remain historical results.

## Files

| File | Purpose |
|---|---|
| [Reference evaluation notebook](notebooks/m4-reference-evaluation.ipynb) | Uploaded Colab notebook, including executed cells and outputs, unchanged |
| [Reference experiment reports](experiments/tfidf-sgd-v1/) | Configuration, metrics, class report, confusion matrix, validation predictions, preparation checks, and reload verification |
| [Experiment log](experiment-log.csv) | Reference run settings, measured results, and timings |
| [Comparison notes](comparison/comparison_notes.md) | Findings, approach differences, and limitations |
| [Comparison CSV](comparison/reference_model_comparison.csv) | Exact validation scores for all three approaches |
| [Comparison figure](comparison/reference_model_comparison.png) | Macro-F1 and class recall comparison |

The notebook and all 12 files from the uploaded reports archive are preserved unchanged. The report folders contain source row identifiers and labels rather than resume or job text. Trained model files and downloaded ZIPs stay outside Git.

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

Use this fixed reference when comparing class-weighted DistilBERT training and section-aware transformer inputs. Categorise validation errors, test robustness, and measure inference performance. Freeze model and preparation settings before official-test evaluation. This reference contribution supports M4; optimization and robustness evidence still require their own experiments.

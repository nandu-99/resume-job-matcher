# Preprocessing and Data Splits

## Purpose

This pipeline prepares the public resume–job dataset for model development. It records the cleaning steps and split settings needed to repeat the work.

## Original Data

| Split | Rows |
|---|---:|
| Training | 6,241 |
| Official test | 1,759 |

The original columns are:

- `resume_text`
- `job_description_text`
- `label`

## Duplicate Handling

Duplicate checks use the complete resume and job-description text as a pair.

The original training split contains seven duplicate pair groups:

- Six groups contain conflicting labels.
- One group contains the same label.

All 12 rows from the conflicting groups are removed. One row is kept from the same-label group.

| Step | Rows |
|---|---:|
| Original training rows | 6,241 |
| Conflicting rows removed | 12 |
| Same-label duplicate removed | 1 |
| Clean training rows | 6,228 |

No duplicate pair remains after this step. The official test split contains no duplicate pairs.

## Text Cleaning

The same cleaning function is applied to resume and job-description text.

The function:

1. Converts text to lowercase.
2. Replaces Markdown links with their visible text.
3. Replaces email addresses with `email`.
4. Replaces URLs with `url`.
5. Replaces phone numbers with `phone`.
6. Removes unwanted characters.
7. Keeps letters, numbers, whitespace, periods, plus signs, and number signs.
8. Replaces repeated whitespace with one space.
9. Removes spaces from the beginning and end.

No resume or job description becomes empty after cleaning. All cleaned text passes checks for lowercase text, allowed characters, repeated spaces, and outer spaces.

C++ and C# are preserved in cleaned text. Model tokenization needs a separate check: preserving a term during cleaning does not guarantee that TF-IDF keeps it as a feature.

## Stratified Split

The 6,228 clean training rows are divided using `train_test_split` with:

- Validation size: 20%
- Stratification column: `label`
- Random seed: 42

The official test split is not divided or used for model selection. Its original rows and labels remain unchanged. Cleaning only adds the text used by the models.

## Final Split Sizes

| Split | Rows |
|---|---:|
| Training | 4,982 |
| Validation | 1,246 |
| Test | 1,759 |
| Total | 7,987 |

The split is repeatable with random seed 42.

## Final Label Counts

| Split | Good Fit | Potential Fit | No Fit | Total |
|---|---:|---:|---:|---:|
| Training | 1,230 | 1,243 | 2,509 | 4,982 |
| Validation | 308 | 311 | 627 | 1,246 |
| Test | 458 | 444 | 857 | 1,759 |

Class percentages remain similar across all splits.

The split-distribution figure is available at [figures/split-label-distribution.png](figures/split-label-distribution.png).

## Split Overlap

| Comparison | Shared pairs | Shared resumes | Shared job descriptions |
|---|---:|---:|---:|
| Training and validation | 0 | 441 | 246 |
| Training and test | 0 | 473 | 0 |
| Validation and test | 0 | 368 | 0 |

No complete resume-job pair appears in more than one split.

The pair-level split still shares many resumes and job descriptions between training and validation. Many test resumes also appear in training or validation. The official test set supports evaluation on new jobs against a largely known candidate pool. It does not establish performance on completely new candidates. Validation shares job descriptions with training, so job-grouped validation would better represent unseen jobs during model selection.

## Validation Checks

The notebook confirms that:

- The clean training data has 6,228 rows.
- Split sizes are 4,982 training, 1,246 validation, and 1,759 test rows.
- Class counts match the reported split table.
- Every split has no duplicate pairs.
- Complete pairs do not overlap across splits.
- Official test rows and labels are unchanged.
- Running the split again with seed 42 gives the same rows.

## Cleaned-pair checks

Duplicate and overlap checks cover both original and cleaned text. There are no duplicate pairs within a split and no shared pairs across splits. The notebook stops if these checks fail. Shared resumes and job descriptions still limit the evaluation, so exact-pair separation does not establish independence between candidates or jobs.

Prepared records remain in notebook memory and are recreated by running the notebook. Raw and cleaned datasets are not stored in the repository.

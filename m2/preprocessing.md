# Preprocessing and Data Splits

## Purpose

This preprocessing pipeline prepares the public resume-job dataset for the two baseline models. It follows the steps reported in the anchor paper and records the details needed to repeat the work.

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

The paper does not provide its exact regular expressions or placeholder words. This implementation follows the written method, but small cleaning differences may affect the reproduced result.

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

These sizes match the anchor paper.

## Final Label Counts

| Split | Good Fit | Potential Fit | No Fit | Total |
|---|---:|---:|---:|---:|
| Training | 1,230 | 1,243 | 2,509 | 4,982 |
| Validation | 308 | 311 | 627 | 1,246 |
| Test | 458 | 444 | 857 | 1,759 |

The label counts match the anchor paper. The class percentages also remain similar across all splits.

The split-distribution figure is available at [figures/split-label-distribution.png](figures/split-label-distribution.png).

## Split Overlap

| Comparison | Shared pairs | Shared resumes | Shared job descriptions |
|---|---:|---:|---:|
| Training and validation | 0 | 441 | 246 |
| Training and test | 0 | 473 | 0 |
| Validation and test | 0 | 368 | 0 |

No complete resume-job pair appears in more than one split.

The pair-level split still shares many resumes and job descriptions between training and validation. Many test resumes also appear in training or validation. This matches the paper's split method, but it limits how strongly the results show performance on completely new resumes.

## Validation Checks

The notebook confirms that:

- The clean training data has 6,228 rows.
- Final split sizes match the paper.
- Label counts match the paper.
- Every split has no duplicate pairs.
- Complete pairs do not overlap across splits.
- Official test rows and labels are unchanged.
- Running the split again with seed 42 gives the same rows.

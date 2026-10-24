# Dataset Documentation

## Dataset Name

`cnamuangtoun/resume-job-description-fit`

Dataset page: <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

## Purpose

The dataset contains paired resume and job-description text. Each pair has a label that describes how well the resume matches the job.

The labels are:

- Good Fit
- Potential Fit
- No Fit

## Dataset Structure

The dataset provides official training and test splits.

| Split | Rows |
|---|---:|
| Training | 6,241 |
| Test | 1,759 |
| Total | 8,000 |

Each row contains:

| Column | Description |
|---|---|
| `resume_text` | Resume content |
| `job_description_text` | Job-description content |
| `label` | Match class |

All three columns are loaded as text values.

## Label Distribution

| Label | Training | Test | Total | Total percentage |
|---|---:|---:|---:|---:|
| Good Fit | 1,542 | 458 | 2,000 | 25% |
| Potential Fit | 1,556 | 444 | 2,000 | 25% |
| No Fit | 3,143 | 857 | 4,000 | 50% |

The No Fit class contains half of the data. Accuracy alone may hide poor performance on the two smaller classes. Macro-F1 is therefore the main metric.

## Missing and Empty Values

No missing or empty values were found in either split.

| Check | Training | Test |
|---|---:|---:|
| Missing resume text | 0 | 0 |
| Empty resume text | 0 | 0 |
| Missing job description | 0 | 0 |
| Empty job description | 0 | 0 |
| Missing label | 0 | 0 |
| Empty label | 0 | 0 |

## Duplicate Resume-Job Pairs

The training split contains seven duplicate pair groups with two rows in each group.

| Duplicate type | Groups | Rows |
|---|---:|---:|
| Conflicting labels | 6 | 12 |
| Same label | 1 | 2 |
| Total | 7 | 14 |

The six conflicting groups contain these label combinations:

- Four groups contain Good Fit and No Fit.
- Two groups contain Potential Fit and No Fit.

The same-label group contains two No Fit rows.

The test split contains no duplicate resume-job pairs.

These findings match the anchor paper. The preprocessing step will remove all 12 rows from the conflicting groups and keep one row from the same-label group. This should reduce the training split from 6,241 rows to 6,228 clean rows.

## Training and Test Overlap

| Text unit | Unique in training | Unique in test | Shared unique values | Test rows with overlap | Test overlap |
|---|---:|---:|---:|---:|---:|
| Resume text | 642 | 477 | 476 | 1,758 | 99.94% |
| Job description | 280 | 71 | 0 | 0 | 0% |
| Complete resume-job pair | 6,234 | 1,759 | 0 | 0 | 0% |

No complete pair appears in both splits. No job description appears in both splits.

However, 1,758 of the 1,759 test rows use resume text that also appears in training. The official test split therefore mainly evaluates known resumes against new job descriptions. This is an important limit when interpreting the final results.

## Text-Length Statistics

The statistics below use simple whitespace-separated word counts before preprocessing.

| Split | Mean resume words | Median resume words | Maximum resume words | Mean job words | Median job words | Maximum job words |
|---|---:|---:|---:|---:|---:|---:|
| Training | 708.1 | 618.0 | 3,134 | 371.5 | 328.0 | 1,079 |
| Test | 691.4 | 618.0 | 2,738 | 402.9 | 308.0 | 1,254 |

| Split | Mean resume characters | Mean job characters |
|---|---:|---:|
| Training | 5,804.4 | 2,731.3 |
| Test | 5,663.3 | 2,939.2 |

Resumes are generally longer than job descriptions. Test job descriptions are slightly longer on average than training job descriptions.

The dataset overview figure is available at [figures/dataset-overview.png](figures/dataset-overview.png).

## Dataset Information Limits

The Hugging Face metadata does not provide:

- A detailed dataset description
- Licence information
- An official homepage
- A recommended citation
- Clear information about data collection

The missing licence and collection details limit how the data should be used outside this academic project.

## Privacy and Responsible Use

Resume data may contain personal, education, and employment information. The project will use the text only for academic model evaluation.

The system is a research prototype. It should not make final hiring decisions. Model results can be affected by class imbalance, repeated resumes, unclear data collection, and possible bias in the labels.

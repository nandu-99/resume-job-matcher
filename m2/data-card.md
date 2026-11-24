# Data Card

## Dataset Name

`cnamuangtoun/resume-job-description-fit`

Dataset page: <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

Data card version: 1.0

Project: Resume-Job Matching System

## Dataset Purpose

The dataset supports three-class matching between a resume and a job description. It is used to prepare and evaluate a recruiter review-support model.

## Intended Use

- Academic NLP experiments
- Data-quality and preprocessing studies
- Matching known resumes with new job descriptions
- Comparing baseline models using the same prepared splits

## Uses That Are Not Supported

- Automatic hiring or rejection
- Production recruitment decisions
- Ranking people using protected or sensitive information
- Claims about performance on completely unseen candidates
- Commercial use without confirming the licence and lawful data source

## Data Structure

| Field | Type | Meaning |
|---|---|---|
| `resume_text` | Text | Resume content |
| `job_description_text` | Text | Job-description content |
| `label` | Text | Good Fit, Potential Fit, or No Fit |

## Original Dataset Size

| Split | Rows |
|---|---:|
| Training | 6,241 |
| Official test | 1,759 |
| Total | 8,000 |

## Original Label Distribution

| Label | Training | Test | Total | Total percentage |
|---|---:|---:|---:|---:|
| Good Fit | 1,542 | 458 | 2,000 | 25% |
| Potential Fit | 1,556 | 444 | 2,000 | 25% |
| No Fit | 3,143 | 857 | 4,000 | 50% |

The No Fit class is twice the size of each other class. Macro-F1 is used as the main model metric so each class has equal importance.

## Source and Collection

The dataset is available from Hugging Face. Its metadata does not provide enough information about:

- Original data collection
- Who created the labels
- Labelling instructions
- Consent from the people represented
- Geographic or industry coverage
- Time period
- Official citation
- Licence

These missing details are important limitations.

## Data-Quality Findings

| Check | Finding |
|---|---|
| Missing required values | 0 |
| Empty required values | 0 |
| Training duplicate pair groups | 7 |
| Conflicting duplicate groups | 6, containing 12 rows |
| Same-label duplicate groups | 1, containing 2 rows |
| Test duplicate pairs | 0 |
| Duplicate cleaned pairs within each prepared split | 0 |
| Shared cleaned pairs across prepared splits | 0 |

The cleaning process removes all 12 rows from conflicting pairs and removes one repeated row from the same-label pair. The clean training pool contains 6,228 rows.

## Prepared Splits

| Split | Good Fit | Potential Fit | No Fit | Total |
|---|---:|---:|---:|---:|
| Training | 1,230 | 1,243 | 2,509 | 4,982 |
| Validation | 308 | 311 | 627 | 1,246 |
| Test | 458 | 444 | 857 | 1,759 |

The clean training pool is divided with an 80:20 stratified split using random seed 42. The official test set is kept for final evaluation.

## Split and Leakage Information

| Check | Finding |
|---|---:|
| Complete pair overlap between training and test | 0 |
| Job-description overlap between training and test | 0 |
| Test rows with a resume also found in the original training pool, before cleaning and validation splitting | 1,758 of 1,759 |

The official test split evaluates new job descriptions against a largely known resume pool. It does not establish performance on completely unseen candidates. Training and validation share 441 resumes and 246 job descriptions; validation therefore does not fully represent the unseen-job test scenario. Job-grouped validation would better represent unseen jobs during candidate selection.

Fit models and text transformations on training data only. Use validation for settings and reserve test labels for final evaluation.

## Cleaning Summary

The same cleaning function is applied to both text fields. It:

1. Converts text to lowercase.
2. Keeps visible text from Markdown links.
3. Replaces emails with `email`.
4. Replaces URLs with `url`.
5. Replaces phone numbers with `phone`.
6. Keeps letters, numbers, spaces, periods, plus signs, and number signs.
7. Removes repeated and outer spaces.

C++ and C# remain available after cleaning. No text becomes empty.

## Text-Length Summary

| Split | Mean resume words | Median resume words | Maximum resume words | Mean job words | Median job words | Maximum job words |
|---|---:|---:|---:|---:|---:|---:|
| Training | 708.1 | 618.0 | 3,134 | 371.5 | 328.0 | 1,079 |
| Test | 691.4 | 618.0 | 2,738 | 402.9 | 308.0 | 1,254 |

Resume documents are generally longer than job descriptions. Test job descriptions are longer on average than training job descriptions.

## Privacy

Resume text may contain personal, education, and employment information. Direct contact details are replaced during cleaning, but names and other identifying information may remain.

Raw data must not be committed to the repository or copied into public reports. See [privacy.md](privacy.md) for the full policy.

## Bias and Representation Limits

- Class labels may reflect human judgement and bias.
- The No Fit class is larger than the other classes.
- Demographic coverage is unknown.
- Industry and geographic coverage are unknown.
- Protected characteristics are not available for a proper group fairness study.
- Repeated resumes limit the evaluation claim.

## Maintenance and Versioning

The prepared split uses random seed 42. Any change to cleaning, duplicate handling, or splitting must create a new data-card version and report new row and label counts.

## Supporting Files

- [Exploratory and statistical analysis](data-analysis.md)
- [Cleaning and split report](preprocessing.md)
- [Privacy and responsible use](privacy.md)
- [Preparation notebook](notebooks/m2-data-preparation.ipynb)
- [Dataset overview](figures/dataset-overview.png)
- [Split distribution](figures/split-label-distribution.png)

# Problem Definition and Business Case

## Problem and users

Recruiters spend time comparing resumes with job requirements. Keyword searches may miss relevant experience when candidates use different wording.

The primary user is a recruiter. Hiring managers use the shortlisted results, while applicants are affected by the recommendations.

## Background and direction

We reviewed five resume-job matching papers to understand the existing methods and the resources they require. The review covers learned similarity, sentence embeddings, contrastive learning, and lexical classifiers. It led us to an accessible three-class dataset and CPU-friendly baselines, with semantic methods as candidates for comparison. The [related-work overview](related-work.md) explains how those findings inform the system design.

## Proposed solution

Given English resume text and job-description text, predict one of three labels:

- **Good Fit:** strong matching evidence.
- **Potential Fit:** some matching evidence, with gaps that need review.
- **No Fit:** limited matching evidence in the supplied text.

These are model suggestions, not hiring decisions.

## Business objective and workflow

Reduce the effort needed to organise applications for human review, using a low-cost and repeatable NLP pipeline.

1. The recruiter provides a new job description.
2. The system compares it with resumes from an existing candidate pool.
3. The system suggests a match label for each pair.
4. The recruiter reviews the evidence and decides the next step.

## Scope

The project includes data preparation, baseline and candidate models, evaluation, a deployed prototype, and a final business presentation.

It excludes automatic rejection, final hiring decisions, and claims about completely new applicants without a separate evaluation. The prototype is intended for evaluation rather than real hiring.

## Success measures

| Area | Target |
|---|---|
| Data quality | No missing required fields or conflicting exact pairs after preparation |
| Split integrity | No exact resume–job pair shared across training, validation, and test |
| Main model metric | Macro-F1, supported by per-class precision, recall, F1, and confusion matrices |
| Final model target | Test macro-F1 of at least 0.45 |
| Class coverage | Recall of at least 0.35 for every class |
| Processing speed | Process 1,000 pairs in under 30 seconds on a standard Colab CPU after model loading |
| Business value | Target at least 30% less first-screen comparison time and 70% recruiter agreement in a small pilot |
| Human oversight | No automatic acceptance or rejection |

These targets define how the model and business workflow will be evaluated. Their values must be supported by model tests, timing measurements, and a recruiter pilot.

## Main risks

The dataset has class imbalance, inconsistent labels, repeated resumes across splits, and unclear licence and collection details. Resume text can contain personal data. The data card and privacy report explain these limits.

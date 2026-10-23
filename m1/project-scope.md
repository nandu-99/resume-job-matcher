# Project Scope

## Project Title

**Intelligent Resume-Job Matching System**

## Research Area

This project is about NLP-based resume-job matching. It uses text from a resume and a job description to estimate how well they match.

## Why This Project Is Needed

Recruiters may receive many resumes for one job. Reading and comparing every resume takes time. Basic keyword matching can also miss good candidates when the resume and job description use different words for the same skill.

For example, a job may ask for "machine learning development," while a resume may say "built prediction models using Python." The words are different, but the meaning is similar.

## Problem Statement

Given a resume and a job description, the system should predict how well the candidate matches the job. It should consider skills, education, experience, and responsibilities found in both texts.

## Main Objective

The main objective is to build and evaluate a simple, reproducible NLP system that places each resume-job pair into one of these classes:

- Good Fit
- Potential Fit
- No Fit

We will first reproduce an existing TF-IDF baseline. Later, we will test whether a semantic model can understand similar meanings expressed with different words.

## Specific Objectives

1. Review five papers about resume-job matching.
2. Compare their datasets, methods, results, strengths, and limitations.
3. Select one paper that can be used as the anchor paper.
4. Reproduce a baseline from the anchor paper.
5. Evaluate the model with suitable metrics.
6. Study incorrect predictions and explain why they happened.
7. Design one controlled experiment after completing the baseline.

## Input and Output

### Input

- Resume text
- Job description text

### Output

- **Good Fit:** The resume matches most job requirements.
- **Potential Fit:** The resume matches some requirements but has important gaps.
- **No Fit:** The resume does not match enough requirements.

## Dataset

We plan to use the public `resume-job-description-fit` dataset. It contains 8,000 resume-job pairs with the three labels listed above.

Dataset: <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

Before training, we will check:

- Missing values
- Class distribution
- Duplicate pairs
- Conflicting labels
- Repeated resumes across data splits

We will clearly report any data-quality problems we find.

## Anchor Paper

Our planned anchor paper is:

> Jiaying Jin, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," Journal of Technology Informatics and Engineering, vol. 4, no. 3, pp. 625-648, 2025. DOI: 10.51903/jtie.v4i3.529.

We selected this paper because it:

- Directly matches resumes with job descriptions
- Uses our selected public dataset
- Reports clear evaluation metrics
- Has a baseline that can run on Google Colab without a GPU

For M2, we will reproduce its TF-IDF and SGD classifier. We will also implement TF-IDF with cosine similarity as a simpler baseline.

## Project Plan

### M1: Literature Survey

Review five papers, compare them, select the anchor paper, and check whether its work can be reproduced.

### M2: Baseline Reproduction

Prepare the dataset, reproduce the baseline, compare our result with the paper, and explain any difference.

### M3: Research Gap and Hypothesis

Use the papers and M2 results to find a research gap. Write one hypothesis and expected result before running the new experiment.

### M4: Controlled Experiment

Change one main part of the system at a time. A possible experiment is to compare TF-IDF with semantic sentence embeddings.

### M5: Failure Analysis

Study the confusion matrix, class results, and incorrect predictions. Check errors caused by missing skills, different wording, experience gaps, and long documents.

### M6: Final Paper and Defence

Write the final work in IEEE format and clearly separate reproduced work from our own experiment.

## Evaluation

The main metric will be **macro-F1** because it gives equal importance to all three classes. We will also report:

- Accuracy
- Weighted F1
- Precision, recall, and F1 for each class
- Confusion matrix
- Difference between the paper's result and our result

The test set will not be used for training or parameter selection. TF-IDF will be fitted only on training data to avoid data leakage.

## Project Limits

This project is a research prototype. It should support human review and should not make final hiring decisions. We will not use sensitive personal details as matching features. We will also discuss data bias, label quality, and limits of the results.

## Initial Research Question

How well can lexical and semantic NLP methods match resumes with job descriptions, and what types of resume-job pairs are difficult for these methods?

The final hypothesis will be written after the M2 baseline is completed.

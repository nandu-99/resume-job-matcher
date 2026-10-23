# Anchor Paper Justification

## Selected Paper

Our anchor paper is:

> B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," *Journal of Technology Informatics and Engineering*, vol. 4, no. 3, pp. 625-648, 2025.

DOI: <https://doi.org/10.51903/jtie.v4i3.529>

## Why We Selected It

We selected this paper because it gives the best practical base for our project.

| Selection point | Why it matters |
|---|---|
| Direct task match | It compares resume text with job-description text. |
| Same output labels | It predicts Good Fit, Potential Fit, and No Fit. |
| Public main dataset | The selected dataset can be downloaded from Hugging Face. |
| Clear data split | It reports cleaned training, validation, and test sizes. |
| Clear baseline | It gives TF-IDF and SGD classifier settings. |
| Useful metric | It reports macro-F1, our main project metric. |
| Low compute | The baseline can run on a CPU in Google Colab. |
| Clear target result | The paired TF-IDF with SGD model reports 0.436 test macro-F1. |
| Room for new work | We can later compare lexical TF-IDF with a semantic model. |

Main dataset: <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

## What We Will Reproduce in M2

We will reproduce two three-class methods from the paper:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier using logistic loss

The main reproduction target is the paired TF-IDF with SGD model.

Reported target results:

| Method | Test macro-F1 |
|---|---:|
| TF-IDF cosine similarity | 0.359 |
| Paired TF-IDF with SGD | 0.436 |

We will use the official test split only for final evaluation. Model settings and thresholds will be selected with the validation split.

## Why We Did Not Select the Other Papers

### Deep Siamese Network

The paper is directly related, but its dataset and code are not public. Important training details are also missing.

### conSultantBERT

The semantic method is useful for our later experiment, but its recruitment dataset is private and official code was not found.

### ConFit

It provides public code and strong research ideas. However, its real text data is private or difficult to obtain, and its main training setup needs more compute.

### ConFit v2

It is a strong and recent paper, but its datasets are unavailable, its main task is ranking, and its full method uses an A100 GPU and a paid LLM service.

## Scientific Value and Practical Limit

The other four papers are useful for understanding stronger semantic and ranking methods. The selected anchor paper is from a less established venue than RecSys or ACL Findings, so we will not treat it as the strongest paper in the field. We selected it because its task, public data, reported settings, and compute needs fit our M2 work.

The paper says its code and input files were archived, but it does not give a public archive link. Also, the complete skill list and title rules are missing. We can reproduce the paired TF-IDF with SGD baseline, but exact reproduction of the full title hybrid is uncertain.

## Final Decision

This paper is the most suitable anchor for a student reproduction project. It gives us a public dataset, a clear three-class baseline, a measurable target, and a method that can run in Colab. It also supports a later controlled experiment on semantic matching.

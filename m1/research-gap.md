# Initial Research Gap and Problem

## 1. What Existing Papers Have Done

The selected papers show how resume-job matching has developed over time.

| Paper | Main idea | Main limitation for our project |
|---|---|---|
| Deep Siamese Network | Uses a shared CNN to learn resume-job similarity | Dataset and code are not public |
| conSultantBERT | Fine-tunes multilingual SBERT on resume-vacancy pairs | Large private dataset and no official code |
| ConFit | Uses data augmentation and contrastive learning | Real text is private and training needs high compute |
| ConFit v2 | Uses generated resumes and runner-up hard negatives | Datasets are unavailable and the method needs an LLM and A100 GPU |
| Calibrated Resume-Job Matching | Uses public data and simple TF-IDF classifiers | Mainly uses lexical features and reports modest three-class performance |

All five papers directly study resume-job matching, but they solve slightly different tasks. Some classify a pair, while others rank many resumes or jobs.

## 2. Main Research Gap

There is no clear, low-cost, and reproducible comparison between a lexical baseline and a semantic text model for three-class resume-job matching on a public paired dataset.

The strongest semantic papers use private recruitment data, expensive GPUs, or paid LLM services. This makes their results difficult for students and other researchers to reproduce.

The public and feasible anchor paper uses mainly TF-IDF and hand-made overlap features. These methods can work well when the same skill words appear in both documents. They may fail when the resume and job description express similar meaning with different words.

For example:

- Job description: "experience building machine learning systems"
- Resume: "developed prediction models and deployed them with Python"

The meaning may match even though many exact words are different.

## 3. Supporting Gaps

### 3.1 Public Reproducibility Gap

Most neural papers use private resumes and recruitment records. Their papers may be public, but their main experiments cannot be repeated exactly.

Our project will use a public paired dataset and clearly report preprocessing, data splits, model settings, and results.

### 3.2 Task Gap

ConFit and ConFit v2 mainly focus on ranking. Our project needs to predict:

- Good Fit
- Potential Fit
- No Fit

A method that performs well in ranking may not perform equally well in three-class classification.

### 3.3 Semantic Gap

TF-IDF mainly depends on shared words. It does not fully capture synonyms, related skills, or different ways of describing the same experience.

Semantic embeddings may help, but this must be tested on the same data split and with the same evaluation method.

### 3.4 Evaluation Gap

Accuracy alone can hide poor results for smaller classes. Our dataset also needs checks for duplicate pairs and repeated resumes across training and test data.

Our evaluation will use macro-F1 as the main metric and will also include per-class results, a confusion matrix, and error examples.

### 3.5 Compute Gap

Recent methods use large encoders, paid LLMs, and A100 GPUs. A useful student experiment should run on Google Colab with limited resources.

Our baseline will use TF-IDF and SGD. A later semantic model will be selected based on its ability to run within the available compute.

## 4. Initial Research Problem

The initial problem is:

> How well can a lightweight semantic text representation improve three-class resume-job matching compared with a reproduced TF-IDF baseline on a public dataset, especially when matching pairs use different words with similar meanings?

This is an initial problem statement, not the final hypothesis. The exact model change, expected direction, and predicted improvement will be written in M3 before running the new experiment.

## 5. Planned Baseline

For M2, we will reproduce the anchor paper's methods on the public `resume-job-description-fit` dataset:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier using logistic loss

The main target is the PairSGDLog baseline, with a reported test macro-F1 of about 0.436.

Dataset: <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

## 6. Possible Later Investigation

After M2, a controlled experiment may replace the lexical representation with a lightweight sentence embedding. Everything else should remain as similar as possible.

The comparison should use:

- The same cleaned dataset
- The same training, validation, and test splits
- The same target labels
- The same main metric
- The same error-analysis method

This will help show whether any change comes from the text representation rather than from a different split or evaluation setup.

## 7. Research Questions

The project will later examine:

1. Can the reported TF-IDF baseline be reproduced on the public dataset?
2. Which class is most difficult for the baseline?
3. Does the baseline fail more often when word overlap is low?
4. Can a lightweight semantic representation improve these difficult cases?
5. What errors remain after using semantic information?

Only the first three questions belong to the baseline and error study. The semantic comparison will become the controlled experiment after the M3 hypothesis is recorded.

## 8. Expected Value of the Project

The project will provide:

- A reproducible baseline on public data
- A clear comparison between lexical and semantic text representations
- Careful checks for duplicates and data leakage
- Results for every class, not only overall accuracy
- Error analysis with real resume-job examples
- An experiment that can run with limited computing resources

The main value is a clear and honest experiment, not only a higher score.

## References

1. S. Maheshwary and H. Misra, "Matching Resumes to Jobs via Deep Siamese Network," WWW Companion, 2018. <https://doi.org/10.1145/3184558.3186942>
2. D. Lavi, V. Medentsiy, and D. Graus, "conSultantBERT: Fine-tuned Siamese Sentence-BERT for Matching Jobs and Job Seekers," RecSys in HR, 2021. <https://arxiv.org/abs/2109.06501>
3. X. Yu, J. Zhang, and Z. Yu, "ConFit: Improving Resume-Job Matching using Data Augmentation and Contrastive Learning," RecSys, 2024. <https://doi.org/10.1145/3640457.3688108>
4. X. Yu, R. Xu, C. Xue, J. Zhang, X. Ma, and Z. Yu, "ConFit v2: Improving Resume-Job Matching using Hypothetical Resume Embedding and Runner-Up Hard-Negative Mining," ACL Findings, 2025. <https://doi.org/10.18653/v1/2025.findings-acl.661>
5. J. Jin, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," Journal of Technology Informatics and Engineering, vol. 4, no. 3, 2025. <https://doi.org/10.51903/jtie.v4i3.529>

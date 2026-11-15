# Comparison of Five Resume-Job Matching Papers

## Main Comparison

| Paper | Task | Dataset access | Main method | Main reported result | Code access | Compute | Reproducibility for our project |
|---|---|---|---|---|---|---|---|
| Deep Siamese Network, 2018 | Binary pair classification | Private data with 1,314 resumes and 3,809 jobs | Doc2Vec with a Siamese CNN | 81.34% and 83.19% accuracy on two test sets | Not found | Not reported | Low |
| conSultantBERT, 2021 | Binary matching and embedding | Private data with 274,407 pairs | Multilingual Siamese SBERT | 0.8459 ROC-AUC and 0.7677 macro-F1 | Not found | Not reported | Low |
| ConFit, 2024 | Ranking and binary classification | Intellipro is private; AliYun is difficult to obtain | Data augmentation and contrastive learning | Up to 19 points higher nDCG for job ranking and 31 points higher for resume ranking | Public | A100 GPU used | Medium for code, low for full results |
| ConFit v2, 2025 | Resume and job ranking | Recruiting is private; AliYun is no longer public | HYRE and runner-up hard-negative mining | Average gains of 13.8 points in recall and 17.5 points in nDCG | Public | A100 80 GB and GPT-4o-mini | Low |
| Calibrated Resume-Job Matching, 2025 | Three-class matching and binary screening | Two public datasets | TF-IDF, linear classifiers, hybrid features, calibration, and refusal | 0.450 best three-class macro-F1; 0.436 for paired TF-IDF with SGD | Archive mentioned, public link unclear | CPU-friendly baseline | **High for the selected baseline** |

## Detailed Comparison

### 1. Task Fit

The Deep Siamese Network and conSultantBERT papers classify whether a resume and job match. ConFit and ConFit v2 mainly study ranking. The calibrated matching paper directly uses our required labels:

- Good Fit
- Potential Fit
- No Fit

This makes its task the closest match to our project.

### 2. Data Access

The first four papers depend on private or unavailable recruitment data for their main results. Their papers are public, but their full experiments cannot be repeated with the original data.

The calibrated matching paper uses `resume-job-description-fit`, which is publicly available:

<https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

This makes it a practical reference for our data preparation and baseline models.

### 3. Method Complexity

| Paper | Main complexity |
|---|---|
| Deep Siamese Network | Needs Doc2Vec training and a CNN. |
| conSultantBERT | Needs BERT fine-tuning on long documents. |
| ConFit | Needs contrastive learning, data augmentation, and a strong GPU. |
| ConFit v2 | Needs transformer training, an LLM service, hard-negative mining, and a strong GPU. |
| Calibrated matching | The selected TF-IDF with SGD baseline can run on a CPU. |

### 4. Evaluation

The papers use different tasks and metrics, so their result numbers should not be compared directly.

- Deep Siamese Network reports accuracy and class scores.
- conSultantBERT reports ROC-AUC and macro scores.
- ConFit reports MAP, nDCG, and weighted F1.
- ConFit v2 reports recall and nDCG.
- Calibrated matching reports macro-F1, accuracy, weighted F1, calibration, and refusal results.

Macro-F1 is suitable for our three-class task because it gives equal importance to each class.

### 5. Main Strength of Each Paper

| Paper | Useful idea for our project |
|---|---|
| Deep Siamese Network | A shared model can learn a common space for resumes and jobs. |
| conSultantBERT | Fine-tuned sentence embeddings can capture semantic matches. |
| ConFit | Contrastive learning and careful data augmentation can improve matching. |
| ConFit v2 | Generated examples and hard negatives can improve ranking. |
| Calibrated matching | A simple public baseline can be reproduced and checked carefully. |

### 6. Main Limitation of Each Paper

| Paper | Main limitation |
|---|---|
| Deep Siamese Network | Private dataset, missing code, and missing training details. |
| conSultantBERT | Private dataset, missing official code, and possible split leakage. |
| ConFit | Real text is private or difficult to obtain, and training needs high compute. |
| ConFit v2 | Data is unavailable, the task is ranking, and the full method is expensive. |
| Calibrated matching | Modest three-class result and incomplete access to code and hand-made resources. |

## Baseline Reference

We selected **Calibrated Resume-Job Matching** as the anchor paper because it gives the best balance of:

- Direct task match
- Public data
- Clear split sizes
- Clear model settings
- Suitable metrics
- Low compute needs
- A known result to reproduce

The anchor choice is based on project fit and reproducibility. The neural papers provide useful candidate ideas for model development, subject to available data and compute.

## From the comparison to our approach

The review led us to a public three-class dataset and two CPU-friendly reference methods: TF-IDF cosine similarity and paired TF-IDF with SGD. Their reported test macro-F1 values are 0.359 and 0.436 respectively. These are results reported by the reference paper, not measurements from the preparation notebook.

The semantic approaches remain useful options for candidate development. They need to be tested on our selected data; results from different papers and tasks are not directly comparable.

## References

1. S. Maheshwary and H. Misra, "Matching Resumes to Jobs via Deep Siamese Network," *The Web Conference Companion*, 2018. <https://doi.org/10.1145/3184558.3186942>
2. D. Lavi, V. Medentsiy, and D. Graus, "conSultantBERT: Fine-tuned Siamese Sentence-BERT for Matching Jobs and Job Seekers," *RecSys in HR*, 2021. <https://arxiv.org/abs/2109.06501>
3. X. Yu, J. Zhang, and Z. Yu, "ConFit: Improving Resume-Job Matching using Data Augmentation and Contrastive Learning," *RecSys*, 2024. <https://doi.org/10.1145/3640457.3688108>
4. X. Yu, R. Xu, C. Xue, J. Zhang, X. Ma, and Z. Yu, "ConFit v2: Improving Resume-Job Matching using Hypothetical Resume Embedding and Runner-Up Hard-Negative Mining," *Findings of ACL*, 2025. <https://doi.org/10.18653/v1/2025.findings-acl.661>
5. B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening," *Journal of Technology Informatics and Engineering*, 2025. <https://doi.org/10.51903/jtie.v4i3.529>

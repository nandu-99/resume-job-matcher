# Paper Review: ConFit

## 1. Paper Details

**Title:** ConFit: Improving Resume-Job Matching using Data Augmentation and Contrastive Learning  
**Authors:** Xiao Yu, Jinzhong Zhang, and Zhou Yu  
**Venue:** ACM Conference on Recommender Systems, RecSys 2024  
**Pages:** 601-611  
**DOI:** <https://doi.org/10.1145/3640457.3688108>  
**Paper page:** <https://arxiv.org/abs/2401.16349>  
**Full text:** <https://arxiv.org/pdf/2401.16349>  
**Official code:** <https://github.com/jasonyux/ConFit>

## 2. Research Problem

Resume-job datasets are usually sparse. A candidate applies to only a small number of jobs, so most resume-job pairs do not have labels.

Earlier systems often use complex models made for one dataset or one task. Some focus only on classification and may not work well for ranking many resumes or jobs. ConFit aims to create one useful embedding model for:

- Ranking resumes for a job
- Ranking jobs for a resume
- Classifying a resume-job pair
- Handling new resumes and jobs

## 3. Proposed Method

ConFit combines **data augmentation** with **contrastive learning**.

### Data Augmentation

The authors create new versions of resumes and jobs by changing selected text fields. They use:

- EDA, which inserts, removes, swaps, or replaces words
- ChatGPT, which rewrites text while keeping its meaning

The new document receives the same labels as the original document. The authors augment 500 resumes and 500 jobs with each method for each dataset.

### Contrastive Learning

For every matched resume-job pair, the model learns to:

- Move the matched pair closer in the embedding space
- Move unsuitable resumes and jobs farther away

The method uses other examples in the same batch as negative examples. It also uses rejected applications as hard negatives. This increases the number of training comparisons from about B pairs to about B squared pairs per batch.

### Matching

The model produces one dense vector for every resume and job. It calculates their matching score with the inner product. These vectors can be searched quickly with FAISS.

## 4. Datasets

The paper uses two datasets.

### Intellipro Dataset

This dataset comes from Intellipro Group and contains English and Chinese documents.

| Item | Count |
|---|---:|
| Jobs | 1,794 |
| Resumes | 6,435 |
| Labels | 6,751 |
| Accepted pairs | 2,809 |
| Rejected pairs | 3,942 |

The dataset is private. Sensitive identity information was removed.

### AliYun Dataset

This Chinese dataset comes from the 2019 Alibaba job-resume matching competition.

| Item | Count |
|---|---:|
| Jobs | 19,542 |
| Resumes | 2,718 |
| Labels | 22,124 |
| Accepted pairs | 10,185 |
| Rejected pairs | 11,939 |

The paper describes AliYun as publicly available. However, obtaining and preparing the original competition data may not be simple.

## 5. Data Split and Tasks

The authors create separate training, validation, and test sets. Resumes and jobs used in validation or testing are removed from training. This prevents the model from seeing the same resume or job during training.

The paper evaluates three tasks:

1. Rank 100 resumes for a job.
2. Rank 100 jobs for a resume.
3. Classify whether a pair was accepted or rejected for an interview.

The Intellipro test set has 120 samples for each task. The AliYun test set has 300 samples for each task.

## 6. Model and Training

ConFit first encodes each text field in a resume or job. Attention combines the field information, and a linear layer produces one dense vector.

Main training settings include:

| Setting | Value |
|---|---|
| Optimizer | AdamW |
| Weight decay | 0.01 |
| Warm-up | First 5% of training steps |
| Batch size B | 8 |
| Hard negatives | 8 |
| Training epochs | 10 |
| Hardware | One A100 80 GB GPU |

Reported training time:

| Encoder size | Intellipro | AliYun |
|---|---:|---:|
| Small encoder | About 1.5 hours | About 4.5 hours |
| Large encoder | About 3 hours | About 9 hours |

The best checkpoint is selected using validation loss.

## 7. Baseline Models

The paper compares ConFit with:

- Bag of Words with XGBoost
- TF-IDF with XGBoost
- Raw pretrained embeddings
- BM25
- MV-CoN
- InEXIT
- DPGNN
- OpenAI `text-ada-002`

It uses different BERT and E5 encoders to compare small and large models.

## 8. Evaluation Metrics

For ranking, the paper reports:

- MAP
- nDCG@10

For classification, it reports:

- Weighted F1
- Precision for the positive class
- Recall for the positive class

Results from models with randomness are averaged over three runs.

## 9. Main Results

With the large E5 encoder, the following nDCG@10 results are reported:

| Dataset and task | BM25 | ConFit |
|---|---:|---:|
| Intellipro, rank resumes | 44.96 | **50.28** |
| Intellipro, rank jobs | 43.15 | **51.74** |
| AliYun, rank resumes | 40.56 | **71.71** |
| AliYun, rank jobs | 31.18 | **65.91** |

The paper reports improvements of up to 19 percentage points for ranking jobs and 31 percentage points for ranking resumes.

ConFit is strongest mainly on ranking tasks. It remains useful for classification, but models designed only for classification can sometimes achieve a higher F1. For example, on AliYun with a small encoder, ConFit reports a weighted F1 of 47.16, while MV-CoN reports 74.25.

This difference is important because it shows that one model may not be best for every task.

## 10. Ablation Findings

The ablation study removes or changes parts of ConFit.

The main findings are:

- Contrastive learning gives a large improvement.
- Adding hard negatives usually improves ranking.
- Data augmentation improves several results.
- Combining ChatGPT and EDA often works better than using only one method.
- A TF-IDF and XGBoost version remains competitive with some neural baselines.

These tests help show which parts of the method are useful.

## 11. Error Analysis

The authors manually study wrong predictions from the Intellipro dataset. They divide them into four groups:

| Error type | Share |
|---|---:|
| Information outside the documents | 44% |
| Candidate met requirements but was less competitive | 28% |
| Clearly unsuitable candidate | 20% |
| Possibly suitable but had no positive label | 8% |

The analysis shows that resume and job text alone cannot explain every hiring decision. It also shows that missing labels may cause some correct matches to look like errors.

## 12. Strengths

- It directly studies resume-job matching.
- It supports both resume ranking and job ranking.
- It evaluates classification as a separate task.
- Test resumes and jobs are not included in training.
- It compares many strong baselines.
- It includes ablation, runtime, and error analysis.
- Results from random methods are averaged over three runs.
- Dense vectors allow fast search with FAISS.
- Official code is publicly available.

## 13. Limitations

- The Intellipro dataset is private.
- Real text in the official repository is replaced with placeholders.
- The AliYun data may be difficult to download and prepare.
- Full training requires a powerful GPU.
- ChatGPT augmentation may require paid API access.
- Augmented examples automatically inherit labels, which may create noise.
- Unlabelled pairs are not always true negative pairs.
- The classification test sets are small.
- The paper does not provide a complete fairness evaluation.
- Recruitment decisions may depend on information missing from the resume and job text.

## 14. Reproducibility Check

| Item | Status | Reason |
|---|---|---|
| Public paper | Yes | The full paper is available online. |
| Dataset sizes given | Yes | Training and test statistics are reported. |
| Public dataset | Partial | AliYun is described as public, but Intellipro is private. |
| Public code | Yes | The official implementation is on GitHub. |
| Public pretrained models | Yes | BERT and E5 base models are public. |
| Preprocessing given | Yes | Fields and text preparation are described. |
| Training settings given | Yes | Main hyperparameters are reported. |
| Hardware known | Yes | The paper reports one A100 80 GB GPU. |
| Training time known | Yes | Approximate times are reported. |
| Dependencies listed | Yes | The official repository has a requirements file. |
| Metrics clear | Yes | Ranking and classification metrics are defined. |
| Exact reproduction possible | Partial | Code is public, but the main real-world data is not fully available. |
| Free Colab reproduction | Difficult | The full setup is too heavy for a normal free Colab session. |

## 15. Relation to Our Project

ConFit is directly related to our project because it learns semantic resume and job embeddings. It shows how data augmentation, contrastive learning, and hard negatives can improve ranking.

It is useful for understanding advanced matching methods and possible later experiments. However, it is not our M2 anchor because its real data is not fully available and its full training setup needs more computing power than our TF-IDF baseline.

## 16. Possible Extension

A smaller experiment could use a public sentence transformer with hard negative pairs from our public dataset. We could compare it with TF-IDF while keeping the same data split and evaluation metrics.

This idea should be finalized only after M2 and before running the M3 experiment.

## 17. Summary

ConFit combines data augmentation and contrastive learning to create useful resume and job embeddings. It gives strong ranking results and includes careful ablation and error analysis. Its public code is valuable, but private text data and high compute needs make full reproduction difficult for our project.

## Reference

X. Yu, J. Zhang, and Z. Yu, "ConFit: Improving Resume-Job Matching using Data Augmentation and Contrastive Learning," in *Proceedings of the 18th ACM Conference on Recommender Systems*, Bari, Italy, 2024, pp. 601-611, doi: 10.1145/3640457.3688108.

# Paper Review: ConFit v2

## 1. Paper Details

**Title:** ConFit v2: Improving Resume-Job Matching using Hypothetical Resume Embedding and Runner-Up Hard-Negative Mining  
**Authors:** Xiao Yu, Ruize Xu, Chengyuan Xue, Jinzhong Zhang, Xu Ma, and Zhou Yu  
**Venue:** Findings of the Association for Computational Linguistics, ACL 2025  
**Pages:** 12775-12790  
**DOI:** <https://doi.org/10.18653/v1/2025.findings-acl.661>  
**Paper page:** <https://aclanthology.org/2025.findings-acl.661/>  
**Full text:** <https://aclanthology.org/2025.findings-acl.661.pdf>  
**Official code:** <https://github.com/jasonyux/ConFit-v2>

## 2. Research Problem

Resume-job datasets contain very few labelled pairs. A candidate applies to only a small number of jobs, so less than 0.05% of all possible resume-job pairs have labels in the paper's datasets.

ConFit already uses contrastive learning to create resume and job embeddings. However, ConFit v2 identifies two remaining problems:

1. A resume and a job description have different formats and levels of detail.
2. Good hard-negative examples are difficult to find because many unlabelled pairs may actually be suitable matches.

ConFit v2 tries to improve both resume ranking and job ranking while keeping the model useful for new resumes and jobs.

## 3. Proposed Method

ConFit v2 has three main parts.

### 3.1 Simpler Encoder

The earlier ConFit model processes different document fields separately. ConFit v2 treats the full resume or job as one text sequence and uses a transformer encoder to create one vector.

This reduces manual feature design and allows the encoder to learn useful information directly from the text.

### 3.2 Hypothetical Resume Embedding

Hypothetical Resume Embedding is called **HYRE**.

For each job description:

1. GPT-4o-mini generates an example of an ideal resume.
2. The generated resume is joined with the original job description.
3. The encoder creates a job vector from the combined text.
4. A real resume is encoded directly.
5. Cosine similarity measures how well they match.

The generated resume helps make the job representation more similar in form to a real resume.

### 3.3 Runner-Up Mining

Runner-Up Mining is called **RUM**. It creates difficult negative examples for contrastive learning.

The highest-scoring unlabelled pairs may be real matches where the candidate never applied. Treating all of them as negative examples could harm training. RUM therefore chooses examples from a lower runner-up range, mainly the top 3% to 4% by similarity.

These examples are difficult enough to improve the model but are less likely to be hidden positive matches.

## 4. Datasets

The paper uses two datasets.

### Recruiting Dataset

| Item | Count |
|---|---:|
| Jobs | 9,469 |
| Resumes | 41,279 |
| Labels | 48,096 |
| Accepted pairs | 19,042 |
| Rejected pairs | 29,054 |

The data comes from a recruitment company and contains English and Chinese text. Names, contact details, college names, and company names are removed or replaced with IDs.

This dataset is private.

### AliYun Dataset

| Item | Count |
|---|---:|
| Jobs | 19,542 |
| Resumes | 2,718 |
| Labels | 22,124 |
| Accepted pairs | 10,185 |
| Rejected pairs | 11,939 |

This Chinese dataset comes from the 2019 Alibaba job-resume matching competition. The paper states that the dataset was no longer publicly available as of September 11, 2023.

## 5. Tasks and Test Data

The paper evaluates two tasks:

1. Rank resumes for a job.
2. Rank jobs for a resume.

| Dataset | Rank-resume test samples | Rank-job test samples |
|---|---:|---:|
| Recruiting | 200 | 200 |
| AliYun | 300 | 300 |

Unlike the first ConFit paper, ConFit v2 focuses on ranking and does not report a separate classification task.

## 6. Model and Training Settings

| Setting | Value |
|---|---|
| Encoders | E5-base and Jina-v2-base |
| LLM used by HYRE | GPT-4o-mini |
| Similarity | Cosine similarity |
| Learning rate | 0.00001 |
| Batch size | 4 |
| Hard negatives per batch | 2 |
| RUM range | Top 3% to 4% |
| Search library | FAISS |
| Hardware | One A100 80 GB GPU |

The paper does not clearly report the number of epochs or total training time for the main model.

## 7. Baseline Models

ConFit v2 is compared with:

- Raw E5-base embeddings
- Raw Jina-v2-base embeddings
- OpenAI `text-embedding-3-large`
- BM25
- MV-CoN
- InEXIT
- ConFit

This comparison includes keyword matching, pretrained embeddings, earlier person-job models, and the first ConFit model.

## 8. Evaluation Metrics

The paper uses:

- Recall@K
- nDCG@K

Recall measures how many correct items appear in the top results. nDCG also gives more importance to correct items placed near the top.

Results from methods with randomness are averaged over three runs.

## 9. Main Results

### E5-base Encoder

| Dataset and task | ConFit nDCG | ConFit v2 nDCG |
|---|---:|---:|
| Recruiting, rank resumes | 28.74 | **48.40** |
| Recruiting, rank jobs | 40.85 | **66.61** |
| AliYun, rank resumes | 70.39 | **82.20** |
| AliYun, rank jobs | 43.45 | **67.96** |

### Jina-v2-base Encoder

| Dataset and task | ConFit nDCG | ConFit v2 nDCG |
|---|---:|---:|
| Recruiting, rank resumes | 34.79 | **51.90** |
| Recruiting, rank jobs | 52.57 | **73.32** |
| AliYun, rank resumes | 65.06 | **83.11** |
| AliYun, rank jobs | 56.12 | **68.02** |

Across both datasets and both ranking tasks, the paper reports an average improvement of:

- 13.8 percentage points in recall
- 17.5 percentage points in nDCG

ConFit v2 also performs better than BM25, earlier person-job models, and OpenAI `text-embedding-3-large` in the reported tests.

## 10. Ablation Findings

The ablation study adds one part at a time using Jina-v2-base.

The main findings are:

- Simplifying the encoder improves ConFit.
- Adding HYRE gives another improvement.
- Adding RUM gives the best overall result.
- The top 3% to 4% RUM range works better than choosing only the highest-scoring pairs.
- Repeating RUM more times gives only small extra gains and can lead to overfitting.

This study clearly shows the effect of each part of ConFit v2.

## 11. Error Analysis

The authors manually inspect 30 high-ranked negative pairs.

| Error type | Share |
|---|---:|
| Information outside the documents | 43.3% |
| Candidate met requirements but was less competitive | 33.3% |
| Candidate missed clear requirements | 16.7% |
| Candidate may be suitable but has no positive label | 6.7% |

Many errors cannot be explained using resume and job text alone. Some decisions may depend on interviews, competition, availability, or other information that is not in the dataset.

## 12. Bias Analysis

The paper also studies gender balance. About 72% of candidates in the training data are male and 28% are female.

Adding gender information increases the difference between male and female candidates in the top-ranked results. RUM reduces part of this difference, but it does not remove the main dataset imbalance.

The authors advise against using the model in real hiring without stronger bias checks and reduction methods.

## 13. Strengths

- It directly studies resume-job ranking.
- It improves both resume ranking and job ranking.
- It tests two different encoder models.
- It reports results over three runs.
- It provides a clear ablation study.
- It includes error and gender-bias analysis.
- RUM considers the risk of false negatives in unlabelled data.
- Official code is publicly available.
- The paper is published in ACL Findings.

## 14. Limitations

- Both main datasets are not openly available now.
- The official code does not provide unrestricted access to the complete real data.
- HYRE depends on GPT-4o-mini and may create API costs.
- Full training requires a powerful A100 GPU.
- The number of training epochs and training time are unclear.
- Generated resumes may contain incorrect or unrealistic details.
- The model focuses on ranking, while our project needs three-class classification.
- The test sets are small compared with the training datasets.
- Dataset imbalance can produce gender bias.
- Text alone cannot explain every recruitment decision.

## 15. Reproducibility Check

| Item | Status | Reason |
|---|---|---|
| Public paper | Yes | ACL Anthology provides the full paper. |
| Dataset sizes given | Yes | Training and test statistics are reported. |
| Public dataset | No | Recruiting is private, and AliYun is no longer public. |
| Public code | Yes | The official code is on GitHub. |
| Public pretrained models | Yes | E5-base and Jina-v2-base are public. |
| Model settings given | Partial | Main settings are given, but epochs and training time are unclear. |
| Hardware known | Yes | One A100 80 GB GPU is reported. |
| Training time known | No | Main training time is not reported. |
| Metrics clear | Yes | Recall and nDCG are clearly defined. |
| Exact reproduction possible | No | The complete datasets are unavailable. |
| Free Colab reproduction | Difficult | The model needs more compute and paid LLM access. |

## 16. Relation to Our Project

ConFit v2 is directly related to our project because it creates semantic vectors for resumes and jobs. HYRE shows how generated text can reduce the format difference between the two documents. RUM shows how careful negative selection can improve contrastive learning.

However, it is not suitable as our M2 anchor. The datasets are unavailable, the task is ranking instead of three-class classification, and the complete method requires more computing power and paid LLM access.

## 17. Possible Extension

A smaller future experiment could create hard negative pairs from our public dataset and compare a sentence-transformer model with TF-IDF. This would test one idea from ConFit v2 without copying its full expensive pipeline.

The final experiment and expected result must be written in M3 before running it.

## 18. Summary

ConFit v2 improves ConFit by simplifying the encoder, generating hypothetical resumes, and selecting runner-up hard negatives. It reports strong ranking improvements and includes useful ablation, error, and bias analysis. Its ideas are valuable for our project, but its data and computing needs prevent exact reproduction.

## Reference

X. Yu, R. Xu, C. Xue, J. Zhang, X. Ma, and Z. Yu, "ConFit v2: Improving Resume-Job Matching using Hypothetical Resume Embedding and Runner-Up Hard-Negative Mining," in *Findings of the Association for Computational Linguistics: ACL 2025*, Vienna, Austria, 2025, pp. 12775-12790, doi: 10.18653/v1/2025.findings-acl.661.

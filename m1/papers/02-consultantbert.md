# Paper Review: conSultantBERT

## 1. Paper Details

**Title:** conSultantBERT: Fine-tuned Siamese Sentence-BERT for Matching Jobs and Job Seekers  
**Authors:** Dor Lavi, Volodymyr Medentsiy, and David Graus  
**Venue:** RecSys in HR 2021  
**Year:** 2021  
**Paper page:** <https://arxiv.org/abs/2109.06501>  
**Full text:** <https://ceur-ws.org/Vol-2967/paper_8.pdf>

## 2. Research Problem

The paper studies how to create useful text embeddings for resumes and job vacancies. These embeddings can help a larger recommendation system find suitable candidates for a job or suitable jobs for a candidate.

The authors focus on four problems:

- Resumes are noisy because they come from different file formats.
- Resumes and vacancies have different structures.
- The two documents may use different words for related ideas.
- One model should support several languages and cross-language matching.

For example, the system should match an English resume with a Dutch vacancy when their meanings are related.

## 3. Proposed Method

The authors propose **conSultantBERT**, a Siamese Sentence-BERT model based on `bert-base-multilingual-cased`.

The model has two shared branches:

- One branch encodes the resume.
- The other branch encodes the vacancy.
- Both branches use the same BERT weights.

The authors test two training objectives:

1. **Classification objective:** Predict whether a resume and vacancy form a positive or negative pair.
2. **Regression objective:** Make cosine similarity close to the true match label.

They also test a Random Forest classifier on top of the learned embeddings.

## 4. Dataset

The dataset comes from Randstad's recruitment records. It contains:

- 274,407 resume-vacancy pairs
- 156,256 unique resumes
- 23,080 unique vacancies
- 126,679 positive pairs
- 109,724 recruiter-defined negative pairs
- 38,004 randomly created negative pairs

A positive pair means there was contact between the candidate and a consultant, such as a call, interview, or job offer. A negative pair means a consultant rejected the profile without further contact. Random negative pairs were added to improve class balance.

The dataset is not public because it contains private recruitment information.

## 5. Data Split

The authors use:

| Split | Number of pairs |
|---|---:|
| Training | 219,525 |
| Validation | 27,441 |
| Test | 27,441 |

This is an 80:10:10 split.

The paper does not say whether the same resume or vacancy can appear in more than one split. Because one vacancy may be paired with many resumes, this could create data leakage if the split was made only at pair level.

## 6. Preprocessing

Resumes are parsed from PDF files using Apache Tika. The authors remove some non-text content caused by parsing errors.

The final model uses only the first 512 tokens from each resume and vacancy. This is important because the paper reports that resumes contain about 2,500 tokens on average and vacancies contain about 2,100 tokens on average. Useful information near the end of a document may be lost.

## 7. Model Settings

| Setting | Value |
|---|---|
| Base model | `bert-base-multilingual-cased` |
| Model type | Siamese SBERT bi-encoder |
| Maximum input length | 512 tokens |
| Pooling | Mean pooling |
| Training epochs | 5 |
| Batch size | 4 pairs |
| Objectives tested | Classification and regression |
| Similarity measure | Cosine similarity |

The paper does not clearly list the learning rate, random seed, hardware, training time, or complete software versions.

## 8. Baseline Models

The authors compare conSultantBERT with:

1. BERT embeddings with cosine similarity
2. TF-IDF with cosine similarity
3. BERT embeddings with Random Forest
4. TF-IDF with Random Forest

The TF-IDF vectors have 768 dimensions so that their size matches the BERT embeddings.

## 9. Evaluation Metrics

The main metric is **ROC-AUC**. The paper also reports macro-averaged:

- Precision
- Recall
- F1-score

The authors use statistical tests with a significance level of 0.01.

## 10. Main Results

| Model | ROC-AUC | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| BERT + Cosine | 0.5325 | 0.5057 | 0.5006 | 0.3379 |
| TF-IDF + Cosine | 0.5730 | 0.5890 | 0.5016 | 0.3564 |
| BERT + Random Forest | 0.6978 | 0.6421 | 0.6363 | 0.6360 |
| TF-IDF + Random Forest | 0.7174 | 0.6581 | 0.6526 | 0.6527 |
| conSultantBERT Classifier + Cosine | 0.7474 | 0.7001 | 0.6426 | 0.5994 |
| conSultantBERT Classifier + Random Forest | 0.8366 | 0.7642 | 0.7643 | 0.7643 |
| conSultantBERT Regressor + Cosine | **0.8459** | **0.7714** | **0.7664** | **0.7677** |
| conSultantBERT Regressor + Random Forest | 0.8389 | 0.7684 | 0.7658 | 0.7666 |

The regression model with cosine similarity gives the best result. It also works well without an extra classifier.

## 11. Main Finding

Fine-tuning multilingual SBERT on real resume-vacancy pairs works much better than using plain BERT or TF-IDF embeddings. The regression objective creates the strongest embeddings for direct cosine-similarity matching.

The paper also gives examples showing that the model can connect related English and Dutch text. This supports multilingual and cross-language matching.

## 12. Strengths

- It directly studies resume-vacancy matching.
- It uses a large real-world dataset.
- It compares lexical, pretrained, and fine-tuned models.
- It reports ROC-AUC, precision, recall, and F1.
- It compares classification and regression objectives.
- It studies multilingual and cross-language matching.
- A bi-encoder can precompute embeddings and search large candidate pools quickly.

## 13. Limitations

- The dataset is private.
- Official code and trained model files were not found.
- The paper does not give all training settings.
- It is unclear whether resumes and vacancies are separated across data splits.
- Only the first 512 tokens of long documents are used.
- Contact with a consultant is only a proxy for job fit.
- Random negative pairs may be easier than real rejected pairs.
- The paper does not report detailed error analysis.
- The paper does not provide a full fairness evaluation.

## 14. Reproducibility Check

| Item | Status | Reason |
|---|---|---|
| Public paper | Yes | The full paper is available online. |
| Dataset size given | Yes | Pair, resume, and vacancy counts are reported. |
| Public dataset | No | Randstad recruitment data is private. |
| Public code | No | Official code was not found. |
| Public trained model | No | A public trained model was not found. |
| Preprocessing given | Partial | Parsing, cleaning, and truncation are described briefly. |
| Model settings given | Partial | Base model, epochs, batch size, and pooling are given. |
| Hardware known | No | Hardware is not reported. |
| Training time known | No | Training time is not reported. |
| Metrics clear | Yes | ROC-AUC and macro scores are clearly reported. |
| Exact reproduction possible | No | The data, code, and some settings are unavailable. |

## 15. Relation to Our Project

This paper is directly related to our project. It shows that semantic embeddings can understand matches that simple word overlap may miss. It also gives a clear comparison between TF-IDF, plain BERT, and fine-tuned SBERT.

It supports a possible later experiment using sentence embeddings. However, it is not suitable as our M2 anchor because its dataset and code are private.

## 16. Possible Extension

A useful extension is to compare TF-IDF and a public sentence-transformer model on our three-class dataset. We can also study cases where the two texts have low word overlap but similar meaning.

The exact hypothesis will be written after completing the M2 baseline.

## 17. Summary

conSultantBERT uses a multilingual Siamese SBERT model for resume-vacancy matching. Its best model reaches a ROC-AUC of 0.8459 and an F1-score of 0.7677. The paper is strongly related to our project, but exact reproduction is not possible because the data and official code are unavailable.

## Reference

D. Lavi, V. Medentsiy, and D. Graus, "conSultantBERT: Fine-tuned Siamese Sentence-BERT for Matching Jobs and Job Seekers," in *Proceedings of the RecSys in HR Workshop*, Amsterdam, The Netherlands, 2021.

# Paper Review: Matching Resumes to Jobs via Deep Siamese Network

## 1. Paper Details

**Title:** Matching Resumes to Jobs via Deep Siamese Network  
**Authors:** Saket Maheshwary and Hemant Misra  
**Venue:** Companion Proceedings of The Web Conference 2018  
**Pages:** 87-88  
**DOI:** <https://doi.org/10.1145/3184558.3186942>  
**Official page:** <https://research.ibm.com/publications/matching-resumes-to-jobs-via-deep-siamese-network>  
**Full text:** <https://www.researchgate.net/publication/324223036_Matching_Resumes_to_Jobs_via_Deep_Siamese_Network>

## 2. Research Problem

The paper studies how to recommend suitable jobs by matching a candidate's resume with job descriptions. It uses known matched and unmatched resume-job pairs to learn this task.

Older systems often depend on exact keywords and fixed rules. They may miss a match when a resume and a job description use different words with similar meanings. The paper tries to solve this problem with a neural network that learns text similarity.

## 3. Proposed Method

The authors use a **Siamese CNN**. It has two identical CNN branches:

- One branch processes the resume.
- The other branch processes the job description.
- Both branches share the same weights.

The method works as follows:

1. Clean the resume and job-description text.
2. Convert each document into a 200-dimensional Doc2Vec vector.
3. Pass both vectors through the shared CNN.
4. Create a semantic vector for each document.
5. Measure the distance between the two vectors.
6. Use contrastive loss to move matched pairs closer and unmatched pairs farther apart.

The CNN uses convolution, max pooling, leaky ReLU, and a fully connected layer. Shared weights reduce the number of parameters and help place resumes and jobs in the same vector space.

## 4. Dataset

The dataset contains:

- 1,314 resumes
- 3,809 job descriptions
- 5,005,026 resume-job pairs
- Match and non-match labels

The resumes came from IBM Research summer internship applications. The job descriptions came from an Indian job website.

Forty interns reviewed some job descriptions. The authors also labelled some examples. They used label propagation to create labels for the remaining pairs.

### Label Problem

The paper gives two different meanings for the labels. It first says label 0 means Match and label 1 means Not Match. Later, it calls matched examples class 1. Because of this conflict, we cannot be sure what class 0 and class 1 mean in the class-level results.

## 5. Data Split

The authors divided the 40 interns into two groups:

- Resumes from 30 interns were used for training.
- Resumes from 10 different interns were used for test set A.
- The remaining pairs created through label propagation were used for test set B.

Using different interns for training and test set A is useful because it tests the model on unseen resumes. However, the paper does not give the exact number of pairs in each split.

## 6. Preprocessing

The paper reports three steps:

- Lowercase the text
- Apply stemming
- Remove special characters

It does not name the tokenizer, stemming tool, or Doc2Vec settings.

## 7. Model Settings

| Setting | Value |
|---|---:|
| Doc2Vec input size | 200 |
| Semantic vector size | 256 |
| CNN depth | 4 |
| Batch size | 128 |
| Convolution kernel width | 10 |
| Max-pooling kernel width | 100 |
| Learning rate | 0.01 |
| Optimizer | Adam |
| Loss | Contrastive loss |

The paper does not report the number of epochs, random seed, dropout, early stopping, full layer sizes, software versions, hardware, or training time.

## 8. Baseline Models

The authors compare their model with:

1. Bag of Words
2. Word n-grams
3. TF-IDF
4. Bag of Means using Word2Vec
5. Doc2Vec
6. A CNN without shared weights

The baseline methods use cosine similarity. The authors select its threshold from 0.10 to 0.80 in steps of 0.05.

## 9. Evaluation Metrics

The paper reports:

- Accuracy
- Precision for each class
- Recall for each class
- F1-score for each class

It does not report macro-F1, weighted F1, results from multiple runs, or significance tests.

## 10. Main Results

| Method | Test set A | Test set B |
|---|---:|---:|
| Bag of Words | 56.92% | 57.06% |
| Word n-gram | 58.24% | 59.01% |
| TF-IDF | 60.46% | 61.23% |
| Bag of Means | 62.34% | 63.92% |
| Doc2Vec | 65.24% | 67.24% |
| CNN | 73.31% | 74.68% |
| Deep Siamese CNN | **81.34%** | **83.19%** |

The Deep Siamese CNN improves accuracy over the normal CNN by:

- 8.03 percentage points on test set A
- 8.51 percentage points on test set B

The proposed model reports these class-level F1 scores:

| Test set | Class 0 F1 | Class 1 F1 |
|---|---:|---:|
| Test set A | 0.92 | 0.78 |
| Test set B | 0.92 | 0.80 |

These class results must be treated carefully because the paper gives conflicting label meanings.

## 11. Main Finding

The shared Siamese CNN performs better than all six reported baselines. It also performs better than a normal CNN without shared weights. This suggests that learning a shared space for resumes and jobs can improve matching.

## 12. Strengths

- It directly matches resumes with job descriptions.
- It compares the proposed model with several baselines.
- The Siamese structure is suitable for comparing two documents.
- Shared weights reduce the number of parameters.
- Test set A contains resumes that are not used for training.
- The reported improvement over the baselines is clear.

## 13. Limitations

- The dataset is not public.
- Official code and a trained model are not available.
- Label propagation may create incorrect labels.
- The label meanings are inconsistent.
- The exact data splits are missing.
- Important model and training details are missing.
- Only one run is reported.
- The paper does not explain the class balance.
- Accuracy may be misleading if the classes are unbalanced.
- Most resumes are from research internship applicants.
- The paper has no error or fairness analysis.
- The paper is only two pages long, so many details are missing.

## 14. Reproducibility Check

| Item | Status | Reason |
|---|---|---|
| Public paper | Yes | The full paper is available online. |
| Dataset size given | Yes | Resume, job, and pair counts are given. |
| Public dataset | No | The original data is not released. |
| Public code | No | Official code was not found. |
| Public trained model | No | A trained model was not found. |
| Preprocessing given | Partial | Only three basic steps are listed. |
| Model settings given | Partial | Some settings are reported, but many are missing. |
| Hardware known | No | Hardware is not reported. |
| Training time known | No | Training time is not reported. |
| Dependencies listed | No | Libraries and versions are not given. |
| Metrics clear | Partial | Metrics are given, but label meanings conflict. |
| Exact reproduction possible | No | Data, code, and important settings are missing. |

## 15. Relation to Our Project

This paper is directly related to our project because it compares resumes with job descriptions. It also explains why semantic matching may work better than basic keyword matching.

The paper gives useful background for newer models such as conSultantBERT and ConFit. However, we will not use it as our M2 anchor because its dataset and code are unavailable. Our selected anchor paper uses a public dataset and a simpler baseline that can run in Google Colab.

## 16. Possible Extension

One possible extension is to replace Doc2Vec and the CNN with a pretrained sentence transformer. We can then compare it with TF-IDF on the same public dataset. This can test whether semantic embeddings help when the resume and job description use different words.

We will finalize this experiment only after completing M2 and writing the M3 hypothesis.

## 17. Summary

This paper presents an early neural method for resume-job matching. Its Siamese CNN gives better reported results than the six baselines. However, the private dataset, missing code, missing settings, and label conflict make exact reproduction difficult.

## Reference

S. Maheshwary and H. Misra, "Matching Resumes to Jobs via Deep Siamese Network," in *Companion Proceedings of The Web Conference 2018*, Lyon, France, 2018, pp. 87-88, doi: 10.1145/3184558.3186942.

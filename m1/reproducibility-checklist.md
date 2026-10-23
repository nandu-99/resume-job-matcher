# Reproducibility Checklist

## Anchor Paper

**Paper:** Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening  
**DOI:** <https://doi.org/10.51903/jtie.v4i3.529>  
**Main dataset:** <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>

## Overall Decision

**Reproducibility level: Partial**

The paired TF-IDF with SGD baseline can be reproduced with public data and the reported settings. Exact reproduction of the complete title hybrid is uncertain because its full skill list, title rules, code archive link, hardware, and training time are not provided.

## 1. Dataset Checklist

| Item | Status | Recorded information |
|---|---|---|
| Main dataset is public | Yes | Hugging Face dataset page is available. |
| Dataset size is given | Yes | 8,000 original pairs. |
| Input fields are clear | Yes | Resume text and job-description text. |
| Labels are clear | Yes | Good Fit, Potential Fit, and No Fit. |
| Official test split exists | Yes | The official test has 1,759 rows. |
| Cleaned training size is given | Yes | 6,228 rows after duplicate cleaning. |
| Validation method is given | Yes | Stratified split with random seed 42. |
| Final split sizes are given | Yes | 4,982 training, 1,246 validation, and 1,759 test rows. |
| Duplicate handling is given | Yes | Six conflicting groups removed and one same-label group collapsed. |
| Dataset provenance is complete | Unclear | The dataset page gives limited collection and licence details. |

## 2. Preprocessing Checklist

| Item | Status | Recorded information |
|---|---|---|
| Lowercasing | Yes | All text is lowercased. |
| Link cleaning | Yes | Markdown links keep their visible text. |
| Private text replacement | Yes | Emails, URLs, and phone numbers become placeholders. |
| Character cleaning | Yes | Most non-alphanumeric characters are removed. |
| Whitespace cleaning | Yes | Repeated spaces are collapsed. |
| Pair format | Yes | `resume [text] job [text]` |
| Exact regex patterns | Unclear | The paper describes them but does not provide code. |

## 3. Main M2 Model Checklist

The main M2 target is the paired TF-IDF with SGD classifier.

| Item | Status | Reported value |
|---|---|---|
| Text input | Yes | Joined resume and job text. |
| TF-IDF unit | Yes | Words. |
| N-gram range | Yes | Unigrams and bigrams. |
| Maximum features | Yes | 50,000. |
| Minimum document frequency | Yes | 3. |
| Maximum document frequency | Yes | 0.98. |
| Sublinear term frequency | Yes | Enabled. |
| Stop words | Yes | English stop words. |
| Classifier | Yes | SGDClassifier with logistic loss. |
| Alpha | Yes | 0.00001 for the selected three-class model. |
| Random seed | Yes | 42 for the experiments. |
| Other SGD settings | Unclear | Unreported settings must use documented library defaults. |
| Pretrained model | Not needed | This baseline does not use one. |

## 4. Similarity Baseline Checklist

| Item | Status | Reported value |
|---|---|---|
| TF-IDF unit | Yes | Words. |
| N-gram range | Yes | Unigrams and bigrams. |
| Maximum features | Yes | 30,000. |
| Minimum document frequency | Yes | 3. |
| Stop words | Yes | English stop words. |
| Similarity function | Yes | Row-wise cosine similarity. |
| Class mapping | Yes | Two thresholds produce the three labels. |
| Exact threshold values | No | They must be selected again on validation data. |

## 5. Evaluation Checklist

| Item | Status | Recorded information |
|---|---|---|
| Main metric | Yes | Macro-F1. |
| Other metrics | Yes | Accuracy and weighted F1. |
| Per-class report | Planned | We will add precision, recall, and F1 for each class. |
| Confusion matrix | Planned | We will include it in M2. |
| Test set protected | Yes | It must be used only for final evaluation. |
| Target similarity result | Yes | Test macro-F1 0.359. |
| Target SGD result | Yes | Test macro-F1 0.436. |
| Result comparison rule | Yes | Report our score, paper score, and the difference. |

## 6. Software and Hardware Checklist

| Item | Status | Recorded information |
|---|---|---|
| Python version | Yes | 3.13.5. |
| scikit-learn version | Yes | 1.8.0. |
| pandas version | Yes | 2.2.3. |
| NumPy version | Yes | 2.3.5. |
| SciPy version | Yes | 1.17.0. |
| Hardware | No | Not reported. |
| Training time | No | Not reported. |
| GPU required | No | The selected baseline is CPU-friendly. |
| Free Colab use | Yes | Expected to fit within normal Colab resources. |
| Version verification | Required | We must check that the reported versions install together. |

## 7. Code and Resource Checklist

| Item | Status | Reason |
|---|---|---|
| Public paper | Yes | Article and PDF pages are available. |
| Public main dataset | Yes | It is hosted on Hugging Face. |
| Public code link | Unclear | The paper says files were archived but gives no archive link. |
| Complete skill lexicon | No | The 108 skills are described but not listed. |
| Complete title rules | No | Feature types are given, but all rules are not listed. |
| Saved model | Not located | No public trained file is linked. |
| Input CSV archive | Not located | It is mentioned but not linked. |

## 8. M2 Reproduction Procedure

1. Download the public dataset.
2. Check fields, missing values, labels, and official splits.
3. Find exact duplicate resume-job pairs in the training split.
4. Remove conflicting duplicate groups and collapse same-label duplicates.
5. Create a stratified training and validation split with random seed 42.
6. Apply the reported text cleaning.
7. Train the cosine similarity baseline.
8. Select its two class thresholds only on validation data.
9. Train paired TF-IDF with SGD logistic loss.
10. Evaluate both final models once on the official test split.
11. Report macro-F1, accuracy, weighted F1, class results, and confusion matrices.
12. Compare our results with 0.359 and 0.436 test macro-F1.
13. Record every difference from the paper.

## 9. Expected Sources of Difference

Our result may differ because:

- The exact cleaning regex is not available.
- The paper does not list every SGD parameter.
- Package versions may behave differently.
- The dataset hosted online may have changed.
- Duplicate detection details may differ.
- The original code and input archive are not publicly linked.

## Final Reproducibility Statement

The selected paired TF-IDF with SGD baseline is practical to reproduce in Colab. We can follow the reported data sizes, seed, TF-IDF settings, classifier, and metrics. We must describe the result as a reproduction attempt because some implementation details and the public code location are missing.

# Paper Review: Calibrated Resume-Job Matching

## 1. Paper Details

**Full title:** Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets  
**Authors:** Binghua Zhou, Jiaying Jin, and David Zhao  
**Venue:** Journal of Technology Informatics and Engineering, Volume 4, Number 3  
**Year:** 2025  
**Pages:** 625-648  
**DOI:** <https://doi.org/10.51903/jtie.v4i3.529>  
**Article page:** <https://jtie.stekom.ac.id/index.php/jtie/article/view/529>  
**Main dataset:** <https://huggingface.co/datasets/cnamuangtoun/resume-job-description-fit>  
**Second dataset:** <https://huggingface.co/datasets/AzharAli05/Resume-Screening-Dataset>

## 2. Research Problem

The paper studies how to match a resume with a job description and make the result safer for recruiter use. It asks three main questions:

1. How well can simple and clear models predict resume-job fit?
2. Can model scores be changed into more reliable probabilities?
3. Can the model send uncertain cases to a human reviewer instead of forcing a decision?

This is directly related to our project because both use resume and job-description text to predict match quality.

## 3. Datasets

### 3.1 resume-job-description-fit

This is the main dataset for pair matching.

- 8,000 original resume-job pairs
- Labels: Good Fit, Potential Fit, and No Fit
- Official training and test splits
- Used for the three-class and binary experiments

The authors found seven duplicate groups in the official training split. They removed six groups with conflicting labels and kept one copy from a same-label duplicate group. This produced 6,228 clean training rows. The official test split stayed unchanged with 1,759 rows.

The cleaned training data was split with stratification and random seed 42:

| Split | Rows |
|---|---:|
| Training | 4,982 |
| Validation | 1,246 |
| Official test | 1,759 |

The final total used was 7,987 rows because 13 problematic duplicate rows were removed from the original training data.

### 3.2 Resume-Screening-Dataset

The second dataset contains 10,174 rows with role, resume, job description, decision, and decision reason fields. It was used for a separate in-domain test and to check whether a model trained on the first dataset works on different data.

## 4. Preprocessing

The paper reports these steps:

1. Convert text to lowercase.
2. Replace Markdown links with their visible text.
3. Replace email addresses, URLs, and phone numbers with placeholders.
4. Remove non-alphanumeric characters, except plus signs, number signs, and periods.
5. Replace repeated spaces with one space.
6. Join each pair as `resume [resume text] job [job text]`.

These steps are simple enough to implement in Google Colab.

## 5. Methods

The paper compares three groups of methods.

### 5.1 Similarity Baseline

Resume and job text are converted separately into TF-IDF vectors. Cosine similarity gives one score for each pair. Two thresholds selected on the validation set convert the score into the three fit classes.

Settings:

- Word unigrams and bigrams
- 30,000 maximum features
- Minimum document frequency of 3
- English stop-word removal

### 5.2 Paired-Text Classifiers

The resume and job description are joined before TF-IDF is applied.

TF-IDF settings:

- Word unigrams and bigrams
- 50,000 maximum features
- Minimum document frequency of 3
- Maximum document frequency of 0.98
- Sublinear term frequency
- English stop-word removal

The classifiers are:

- Complement Naive Bayes with alpha 0.5
- SGD classifier with logistic loss and alpha 0.00001
- LinearSVC with C 2.0

### 5.3 Hybrid Models

The paper also adds 16 text-alignment features, such as token overlap, skill overlap, text length, number overlap, and experience gap. A larger model adds eight title features, giving 24 structured features in total.

The skill features use a hand-made list of 108 skills. The paper describes the feature groups but does not publish the complete skill list or every title rule.

## 6. Evaluation Metrics

For the three-class task, the paper reports:

- Macro-F1
- Accuracy
- Weighted F1

For binary shortlist-versus-reject screening, it reports:

- Balanced accuracy
- Accuracy
- Precision
- Recall
- Specificity
- F1
- AUROC
- AUPRC

It also reports Brier score, negative log-likelihood, and expected calibration error for probability quality.

## 7. Main Three-Class Results

| Model | Validation macro-F1 | Test macro-F1 | Test accuracy | Test weighted F1 |
|---|---:|---:|---:|---:|
| Hybrid with title features | 0.592 | **0.450** | 0.480 | 0.484 |
| Paired TF-IDF with SGD | **0.658** | 0.436 | **0.501** | **0.484** |
| TF-IDF with 16 alignment features | 0.607 | 0.434 | 0.505 | 0.483 |
| Paired TF-IDF with LinearSVC | 0.648 | 0.433 | 0.492 | 0.480 |
| Paired TF-IDF with ComplementNB | 0.584 | 0.402 | 0.474 | 0.450 |
| TF-IDF cosine similarity | 0.416 | 0.359 | 0.382 | 0.393 |

The title hybrid gives the best test macro-F1. The paired TF-IDF with SGD model is easier to reproduce and gives a test macro-F1 of 0.436. We will use that model as the main M2 target.

## 8. Calibration and Refusal Results

For binary screening, Good Fit and Potential Fit are combined as shortlist, while No Fit becomes reject.

The title hybrid reaches:

- Balanced accuracy: 0.654
- F1: 0.647
- AUROC: 0.699

Platt scaling improves probability quality on the first dataset:

- Brier score changes from 0.232 to 0.226
- Negative log-likelihood changes from 0.772 to 0.675

Sending low-confidence cases for human review improves in-domain accuracy. However, transfer to the second dataset is weak, with AUROC values near 0.47 to 0.51. This shows that a model trained on one recruitment dataset may not work safely on another dataset.

## 9. Software and Compute

The paper reports:

| Item | Reported value |
|---|---|
| Python | 3.13.5 |
| scikit-learn | 1.8.0 |
| pandas | 2.2.3 |
| NumPy | 2.3.5 |
| SciPy | 1.17.0 |
| Random seed | 42 |

Exact hardware and training time are not reported. The main TF-IDF and SGD baseline is lightweight and should run on a CPU in Google Colab.

The reported version combination should be checked when we create the M2 environment because package availability can change.

## 10. Strengths

- It directly studies resume-job matching.
- It uses public datasets.
- It uses the same three labels as our project.
- It gives exact split sizes and a random seed.
- It reports clear TF-IDF and classifier settings.
- It checks duplicates and conflicting labels.
- It reports class-aware metrics instead of accuracy alone.
- The main baseline can run without a GPU.
- It studies confidence and human review.
- It tests the model on a different dataset.

## 11. Limitations

- The best three-class macro-F1 is only 0.450.
- The models mainly depend on word overlap and hand-made features.
- The complete 108-skill list and all title rules are not provided.
- The paper says code and input files were archived, but it does not provide a public archive link.
- Exact hardware and training time are missing.
- The source and licence details of the main dataset are limited on its dataset page.
- The model performs poorly when moved to a different dataset.
- The work should support human review and should not make final hiring decisions.

## 12. Reproducibility Assessment

The simple paired TF-IDF with SGD baseline is reproducible with public data and the reported settings. Exact reproduction of the complete title hybrid is uncertain because some hand-made resources and the archive location are missing.

Our M2 work will therefore reproduce:

1. TF-IDF with cosine similarity
2. Paired TF-IDF with an SGD classifier using logistic loss

We will compare our test macro-F1 with the reported values of 0.359 and 0.436.

## 13. Relation to Our Project

This paper is our anchor paper because it uses our selected public dataset, the same three-class task, clear evaluation metrics, and models that can run in Colab. It also leaves a clear research gap: lexical TF-IDF models may miss semantic matches when similar skills are written with different words.

## 14. Summary

The paper builds a clear resume-job matching benchmark with public data. Its best three-class result is 0.450 macro-F1, while the simpler paired TF-IDF with SGD model reaches 0.436. The simple baseline is suitable for M2, but the full hybrid cannot be copied exactly because some resources and the public code location are unclear.

## Reference

B. Zhou, J. Jin, and D. Zhao, "Calibrated Resume-Job Matching for Trustworthy LLM-Assisted Recruiter Screening: Pairwise Matching, Probability Calibration, and Selective Refusal on Two Public Recruitment Datasets," *Journal of Technology Informatics and Engineering*, vol. 4, no. 3, pp. 625-648, 2025, doi: 10.51903/jtie.v4i3.529.

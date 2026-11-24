# Design Considerations from the Literature

The paper review identifies practical questions for our system. These are observations from the reviewed work and possible design choices, rather than a claim that no other research addresses them.

## Word overlap and meaning

TF-IDF is an accessible starting point, but shared words do not always capture related experience. For example, a job may ask for "machine learning systems" while a resume describes "prediction models deployed with Python." Sentence embeddings are a candidate way to represent this relationship.

A semantic model should be compared with the lexical baseline on consistent data, labels, and metrics. An improvement must be supported by results, including the cases where it fails.

## Task fit

Some reviewed methods rank candidates or predict a binary match. Our workflow uses Good Fit, Potential Fit, and No Fit. A strong result on ranking or binary matching does not establish performance on these three classes.

## Access and computing cost

Several reviewed approaches depend on private data, large GPUs, or an external language-model service. Candidate selection must account for accessible data, available compute, runtime, and the ability to document the implementation.

## Evaluation and applicant impact

Accuracy can hide weak performance on a smaller class. Macro-F1, per-class recall, and confusion matrices help show which labels the model misses. Suitable applicants predicted as No Fit deserve particular attention because those errors can affect review order.

Entity overlap changes the meaning of an evaluation. The official test jobs are unseen, but most test resumes occur in the original training pool. Training and validation also share jobs, making job-grouped validation a better match for candidate selection in the intended scenario.

## Practical direction

Use the public three-class dataset, document its preparation and limits, and establish CPU-friendly lexical baselines. Compare candidate representations where they address observed errors. Record settings and results, examine anonymised or artificial error examples, and keep a recruiter responsible for every hiring decision.

The [paper comparison](paper-comparison.md) explains the supporting literature. The [data preparation guide](../m2/README.md) connects these considerations to the dataset and pipeline.

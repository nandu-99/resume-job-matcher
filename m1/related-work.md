# Related Work and Project Direction

We began by reviewing existing work on resume-job matching to understand how the problem has already been approached. We compared the tasks, datasets, methods, evaluation measures, and computing needs in five papers. This helped us choose a practical direction for a recruiter support system.

## What we learned from existing work

| Paper | Main idea | Relevance to our project |
|---|---|---|
| [Deep Siamese Network](papers/01-deep-siamese-network.md) | Learn a shared representation of resumes and jobs | Introduces learned similarity between the two texts |
| [conSultantBERT](papers/02-consultantbert.md) | Fine-tune sentence embeddings for matching | Suggests ways to handle similar experience described with different words |
| [ConFit](papers/03-confit.md) | Use data augmentation and contrastive learning | Shows how training examples and matching objectives affect results |
| [ConFit v2](papers/04-confit-v2.md) | Use hypothetical resumes and hard negatives | Provides ideas for distinguishing relevant candidates from difficult alternatives |
| [Calibrated Resume-Job Matching](papers/05-calibrated-resume-job-matching.md) | Combine accessible baselines with careful evaluation | Provides a public three-class dataset and CPU-friendly reference methods |

The papers study related but different tasks. Binary matching, ranking, and three-class classification use different evaluation settings, so their scores should not be treated as a single leaderboard. Access to recruitment data and computing resources also affects which methods we can evaluate reliably.

## How the review shaped our decisions

We selected `resume-job-description-fit` because it provides resume text, job-description text, and the three labels needed for our workflow. The calibrated matching paper gives a practical reference for its preparation and baseline methods. Public availability does not resolve the dataset's missing licence and collection details; those limits are documented in the data card.

TF-IDF cosine similarity gives a simple word-overlap reference. Paired TF-IDF with SGD provides a trainable classifier using the same labels. The embedding-based papers suggest candidate approaches for cases where related skills or experience use different wording. Their usefulness for our dataset must be measured rather than assumed.

The review also highlighted the importance of reproducible splits, class-level metrics, data access, and compute cost. We carried these considerations into the dataset audit and preparation pipeline, which checks conflicting labels, duplicates, class balance, document lengths, and overlap between splits.

## Supporting material

- [Paper comparison](paper-comparison.md): tasks, data access, reported results, and practical constraints.
- [Baseline reference and rationale](anchor-paper-justification.md): why the selected methods fit our use case.
- [Reproducibility notes](reproducibility-checklist.md): reported settings and details that are missing.
- [Design considerations](research-gap.md): how the review informs candidate selection and evaluation.
- [Paper sources](papers/source/README.md): original papers and references.
- [Data understanding and preparation](../m2/README.md): the resulting data workflow and evidence.
- [Baseline implementation](../m2/notebooks/m2-baseline-reproduction.ipynb): the existing cosine-similarity and SGD models, with saved aggregate results.

This background supports the Industry Track business case and engineering choices. The aim is a useful, evaluated recruiter support tool; the paper review explains how we arrived at its data and modelling approach.

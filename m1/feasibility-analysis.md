# Feasibility Analysis

| Area | Assessment |
|---|---|
| Data | A public dataset contains 8,000 labelled resume–job pairs with the required three classes. Duplicate and conflicting labels need cleaning. |
| Technical approach | Python, pandas, Hugging Face Datasets, and scikit-learn support preparation and CPU-based baselines. Candidate models can be compared using the same data and metrics. |
| Compute and cost | Data preparation and TF-IDF baselines can run on a Colab CPU using open-source tools. No paid API is required. |
| Delivery | Build in stages: prepare data, develop models, evaluate, deploy a prototype, and present results. |
| Operational use | The prototype can support review order, but a recruiter must make every hiring decision. |
| Privacy | Contact details are replaced during cleaning. Names, employers, schools, and other identifiers may remain. |
| Data rights | The project has not established the dataset licence, collection method, or consent. Resolve these before broader use; public availability is not permission. |
| Evaluation limits | Test jobs are unseen, but most test resumes occur in the original training pool. Results cannot establish performance on entirely new applicants. |
| Fairness | Reliable protected-group labels are unavailable. Do not claim demographic fairness. |

## Decision

The technical approach is feasible for a CPU-based prototype. Its use depends on the documented data limits and human review. Any real hiring use requires confirmed data rights, suitable privacy controls, fairness evaluation, and operational validation.

## Basis for the approach

The [paper comparison](paper-comparison.md) informed the feasibility assessment. It distinguishes the practical baseline from methods whose original experiments depend on private recruitment data, large GPUs, or paid model services. The [reference notes](reproducibility-checklist.md) identify the settings we can follow and the details that need explicit implementation decisions.

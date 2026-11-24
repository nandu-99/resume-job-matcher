# Resume-Job Matching System

NLP · Industry Track

We are building a recruiter support tool that compares a resume with a job description and predicts **Good Fit**, **Potential Fit**, or **No Fit**. A recruiter reviews the result and makes the final decision.

Our evaluation focuses on an existing candidate pool matched with new job descriptions. It does not establish performance on completely new applicants.

## Approach

We began by reviewing five papers to understand existing resume-job matching methods, their results, and their practical limits. The comparison covered shared text representations, sentence embeddings, contrastive learning, and accessible lexical baselines. Data access, task fit, and CPU requirements led us to a public three-class dataset and TF-IDF reference methods.

We then examined the dataset for class imbalance, inconsistent labels, duplicate pairs, document lengths, and overlap between splits. The preparation pipeline turns those findings into repeatable cleaning and split decisions. Model comparison and evaluation build on this foundation, with human review at the centre of the recruiter workflow.

The [related-work overview](m1/related-work.md) connects the paper reviews to these choices.

## Project files

- [Related work](m1/related-work.md): five paper reviews, comparison, and design rationale.
- [Problem brief](m1/problem-brief.md): users, workflow, business objective, and success measures.
- [Feasibility analysis](m1/feasibility-analysis.md): data, tools, cost, and project risks.
- [Project presentation](m2/presentation.pdf): 10 slides covering the problem, data, methods, and findings.
- [Data preparation guide](m2/README.md): dataset reports, preparation steps, and notebook instructions.
- [Baseline models](m2/notebooks/m2-baseline-reproduction.ipynb): TF-IDF cosine similarity and paired TF-IDF with SGD, with the original saved results.
- [Transformer data setup](m3/README.md): the Colab notebook, shared job-grouped splits, and reproduction instructions for model development.
- [Transformer inputs](m3/notebooks/m3-transformer-models.ipynb): the executed MiniLM and DistilBERT tokenization workflow, truncation reports, and batch checks.
- [MiniLM fine-tuning](m3/notebooks/m3-minilm-finetuning.ipynb): the executed training workflow and validation evidence, summarised in the [experiment log](m3/experiment-log.csv).

- [DistilBERT fine-tuning](m3/notebooks/m3-distilbert-finetuning.ipynb): the executed training workflow and selected-checkpoint validation reports.
- [Transformer comparison](m3/comparison/comparison_notes.md): shared-protocol results and class-level trade-offs.
- [Evaluation and optimization](m4/README.md): the TF-IDF reference on shared M3 splits, saved validation predictions, and comparison with both transformers.

The preparation notebook provides the data workflow and additional cleaned-pair checks. The baseline notebook retains the existing model implementation so candidate approaches can build on it. Its saved test macro-F1 values are 0.3708 for cosine similarity and 0.4100 for paired TF-IDF with SGD.

[requirements.txt](m2/requirements.txt) preserves the original baseline dependencies. The preparation notebook records newer versions in its setup cell and saved environment output; it has not been validated against the original baseline dependencies. The original baseline notebook and five paper summaries are kept exactly as committed.

## Data handling

Download the dataset through the notebook. Do not commit raw or cleaned resume records, local dataset caches, or personal data. The dataset's licence and collection details have not been established by this project; public access alone does not establish permission for reuse or redistribution.

## Shared-protocol reference evaluation

Paired TF-IDF with SGD achieves validation macro-F1 0.2923 on the M3 splits, compared with MiniLM at 0.3081 and DistilBERT at 0.3540. TF-IDF retains the highest Potential Fit recall, while MiniLM has the highest Good Fit recall. All three approaches miss many suitable candidates. The [comparison notes](m4/comparison/comparison_notes.md) explain preprocessing differences and limitations. Official-test evaluation remains held back until model selection is fixed.

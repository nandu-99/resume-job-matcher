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
- [Evaluation and optimization](m4/README.md): shared-split reference evaluation, a section-aware input experiment, saved predictions, and model comparisons.
- [Section-aware input comparison](m4/comparison/section-aware-v1/comparison_notes.md): the input-policy experiment, class-level results, and the decision to retain the original DistilBERT policy.
- [Class-weighted training comparison](m4/comparison/class-weighted-v1/comparison_notes.md): training-only class weights, recorded validation gains, and class-recall trade-offs.
- [Final evaluation](m4/evaluation/evaluation_report.md): reviewed validation errors, robustness tests, GPU inference measurements, frozen selection, and official-test results.
- [Final evaluation notebook](m4/notebooks/m4-final-evaluation.ipynb): the unchanged executed Colab continuation and saved outputs.

The preparation notebook provides the data workflow and additional cleaned-pair checks. The baseline notebook retains the existing model implementation so candidate approaches can build on it. Its saved test macro-F1 values are 0.3708 for cosine similarity and 0.4100 for paired TF-IDF with SGD.

[requirements.txt](m2/requirements.txt) preserves the original baseline dependencies. The preparation notebook records newer versions in its setup cell and saved environment output; it has not been validated against the original baseline dependencies. The original baseline notebook and five paper summaries are kept exactly as committed.

## Data handling

Download the dataset through the notebook. Do not commit raw or cleaned resume records, local dataset caches, or personal data. The dataset's licence and collection details have not been established by this project; public access alone does not establish permission for reuse or redistribution.

## Shared-protocol reference evaluation

Paired TF-IDF with SGD achieves validation macro-F1 0.2923 on the M3 splits, compared with MiniLM at 0.3081 and DistilBERT at 0.3540. TF-IDF retains the highest Potential Fit recall, while MiniLM has the highest Good Fit recall. All three approaches miss many suitable candidates. The [comparison notes](m4/comparison/comparison_notes.md) explain preprocessing differences and limitations. These validation results preceded the separately recorded final selection and official-test evaluation.

The section-aware DistilBERT experiment achieves validation macro-F1 0.3258, below the original 0.3540. Potential Fit recall increases, while Good Fit recall falls to 0.0500. The original input policy remains the stronger candidate. The [M4 guide](m4/README.md) records this improvement attempt, its configuration, and its limitations.

Class-weighted DistilBERT with the original input policy reaches validation macro-F1 0.3582, compared with 0.3540 for the unweighted run. The small gain comes with lower Good Fit recall and accuracy. It was selected before official-test inference using validation macro-F1; the final results below retain that recorded selection.

## Final evaluation

The class-weighted DistilBERT checkpoint was selected using validation macro-F1 before the official test was evaluated. Original DistilBERT and TF-IDF were fixed comparators. Test results were reported without model reselection or threshold tuning.

| Model | Evaluation role | Validation macro-F1 | Official-test macro-F1 |
|---|---|---:|---:|
| Class-weighted DistilBERT | Selected before test | 0.3582 | 0.3563 |
| Original DistilBERT | Fixed comparator | 0.3540 | 0.3626 |
| TF-IDF + SGD | Fixed comparator | 0.2923 | 0.4058 |

TF-IDF has the highest test macro-F1 among these fixed comparisons. The weighted run's small validation gain does not carry over to the test set, and transformer superiority is not established. The recorded selection remains unchanged; it does not establish a deployment recommendation.

The [evaluation report](m4/evaluation/evaluation_report.md) documents 30 qualitatively reviewed validation cases, robustness tests on 300 balanced validation pairs, and model-only GPU inference measurements. Suitable-candidate recall remains low, so further use is limited to a prototype with human review. Earlier historical M2 test scores use a different split protocol.

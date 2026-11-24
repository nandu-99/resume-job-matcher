# Validation Error Review

## Scope and method

This qualitative review covers 30 reproducibly selected validation cases: ten per true class, consisting of four shared failures, four weighted regressions and two weighted fixes. Selection is deliberately balanced by case type rather than representative of natural error prevalence. Each case has at least one incorrect model prediction; weighted fixes are correct for the weighted model and incorrect for the original model.

The review compared prepared resume/job text with the decoded 512-token model input and checked targeted qualifications in the full prepared text. It records textual observations and possible explanations. It does not establish which features caused a model decision, validate the dataset's hiring labels, or prove that an applicant lacks a skill not documented in the resume. This is an assistant-assisted qualitative review rather than an independent recruiter adjudication.

The sample spans 19 unique job texts. In particular, all four Potential Fit weighted regressions share the same joint-interest-accounting job. Their similar findings are correlated and should not be treated as four independent job-level discoveries. The official test set was not used.

## Review categories

Each case has one primary category for reporting; observations can overlap.

| Primary category | Cases |
|---|---:|
| input_context_loss | 5 |
| label_evidence_tension | 7 |
| specialist_requirements_not_established | 15 |
| text_quality_or_profile_conflict | 3 |

These counts describe this selected sample only. They are not estimates of category frequencies across validation data or future applicants.

## Findings

- Context loss: cases 4703 and 5997 contain relevant development experience outside the retained resume prefix, and the corresponding job input loses detailed requirements. Case 4403 loses later accounting/reconciliation detail while the job's specialist requirements are also outside the retained input. These observations motivate input audits but do not establish truncation as the cause of the predictions. The recorded section-aware experiment reduced macro-F1, so reordering sections is not presented as an established fix.
- Specialist requirements: several cases share broad accounting, software, testing or data vocabulary with a job, while the text does not establish its specific industry, seniority or tool requirements. Examples include 689, 1105, 1233, 3784 and 4252. Unmentioned requirements are unresolved evidence, not proof that the applicant is unqualified.
- Text quality: case 3607 has repeated address-like text inserted inside words. Cases 3672 and 4602 open with generic retail profiles despite later technical experience. These are directly observable document inconsistencies, with no measured causal effect assigned.
- Label/evidence tension: cases such as 5311, 6187 and 5863 have Good Fit labels despite substantial apparent gaps between the supplied role and the resume evidence. Case 2030 has an accounting background that overlaps the accountant role despite its No Fit label. These warrant human label review; the original labels remain unchanged.

## Model comparison

Across the full 1,147-row validation set, weighting fixes 59 original errors but introduces 68 regressions. Good Fit has 12 fixes and 24 regressions; Potential Fit has 31 fixes and 12 regressions; No Fit has 16 fixes and 32 regressions. These are paired prediction counts rather than explanations of individual decisions.

The weighted model's validation macro-F1 is 0.3582 versus the original 0.3540, while accuracy and Good Fit recall decrease. The qualitative observations do not establish that the small macro-F1 gain is reliable or sufficient to select a deployment model. Complete robustness and inference measurements before freezing the choice and evaluating the official test.

## Handling and follow-up

The annotations retain source row identifiers, labels, predictions, case types and short paraphrased evidence notes. Full document text, decoded inputs, contact details, names and addresses are excluded. Keep the text-containing review CSV outside Git and the final reports archive.

Retain the original dataset labels and validation split. Treat label checks, improved text handling and specialist-requirement checks as future candidates for evaluation rather than silently changing the evaluation target. No causal ablation or independent recruiter review was performed.

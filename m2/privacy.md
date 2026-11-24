# Privacy and Responsible Use

## Data risks

Resume text may include names, contact details, locations, education, employers, and employment dates. The dataset's collection method, consent process, and licence have not been established by this project.

## Implemented controls

- Replace email addresses, URLs, and phone numbers during cleaning.
- Keep downloaded raw and cleaned dataset files out of the repository.
- The preparation notebook shows aggregate statistics and an artificial cleaning example.
- Recreate prepared records in notebook memory instead of publishing a dataset copy.

The original baseline notebook is retained exactly as committed, including its saved dataset preview. The preparation notebook follows the aggregate-output approach described above.

These steps do not fully anonymise resumes. Names, schools, employers, and other identifying details may remain.

## Handling rules

Use only authorised data access. Do not publish real resume samples, upload them to external AI APIs, or use the prototype for real hiring. Delete temporary dataset copies when no longer needed.

Public access does not establish permission to reuse or redistribute data. Confirm the licence and source before broader use. Academic use alone does not resolve missing permission.

## Fairness and human review

Labels may contain bias, and demographic fairness cannot be established without suitable evaluation data. Report every class separately and examine suitable candidates incorrectly labelled No Fit. A recruiter must make the final decision; a model label must not automatically reject an applicant.

## Evaluation limits

Most test resumes occur in the original training pool. Results concern new jobs against largely known candidates. Do not claim accuracy for entirely new applicants, demographic fairness, or production readiness.

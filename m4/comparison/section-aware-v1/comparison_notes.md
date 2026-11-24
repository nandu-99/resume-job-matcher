# Section-Aware Input Evaluation

## Experiment setup

Both runs use the same DistilBERT checkpoint revision, M3 source rows,
labels, seed, unweighted loss, and saved training arguments.
Only the output directory differs in the training arguments.
Both runs select epoch 2 using validation macro-F1.

The new input policy detects sections, adds section labels, reorders content,
and allocates 304 resume tokens and 205 job tokens before reassigning unused
space. Three special tokens complete the 512-token limit.

## Results

- Original validation macro-F1: 0.3540.
- Section-aware validation macro-F1: 0.3258.
- Absolute macro-F1 change: -0.0282.
- Good Fit recall falls from 0.2107 to 0.0500.
- Potential Fit recall rises from 0.1088 to 0.1813.
- No Fit recall rises from 0.8396 to 0.8862.
- Section-aware predictions include 57 Good Fit, 138 Potential Fit, and 952 No Fit.
- The model correctly identifies 14 of 280 Good Fit examples.

## Decision

Keep the original DistilBERT input policy as the stronger candidate.
The small accuracy increase does not offset lower macro-F1 and Good Fit recall.
Record this as an unsuccessful improvement iteration.

## Limitations

Heading detection was adjusted using training documents only.
Recognising headings does not establish correct section boundaries.
English heading rules may miss unusual layouts or interpret content as headings.

The policy changes section selection, ordering, labels, and token allocation
together. This experiment does not isolate their individual effects.
Reordering or discarding context could affect results, but no specific cause
has been established.

These are single-seed validation results. Section labels count toward the token
budget, so allocation counts are not measurements of original-content retention.
The official test set was neither processed with this policy nor evaluated.

Keep class-weighted training separate so its effect can be assessed against
the original input policy.

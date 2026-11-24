# Class-Weighted DistilBERT Evaluation

## Experiment setup

Both runs start from the same pretrained DistilBERT checkpoint revision.
They use the same M3 source rows, labels, seed, original longest_first inputs,
512-token limit, and saved training arguments except the output directory.
No section-aware preparation is applied.

Class weights are calculated from training labels only:
training_rows / (number_of_classes * class_count).

The custom trainer computes weighted-mean cross-entropy within each microbatch.
It sets model_accepts_loss_kwargs=False so Trainer handles gradient accumulation.
Both runs select epoch 2 using validation macro-F1.

## Results

- Original validation macro-F1: 0.3540.
- Weighted validation macro-F1: 0.3582.
- Absolute macro-F1 change: +0.0042.
- Accuracy falls from 0.4752 to 0.4673.
- Good Fit recall falls from 0.2107 to 0.1679.
- Potential Fit recall rises from 0.1088 to 0.1662.
- No Fit recall falls from 0.8396 to 0.8097.

The weighted model correctly identifies 47 Good Fit, 55 Potential Fit,
and 434 No Fit examples. Predicted counts are 160, 166, and 821 respectively.

## Interpretation

The weighted run has the highest validation macro-F1 among the recorded
DistilBERT variants, but its gain over the original is only 0.0042.
It improves Potential Fit recall while reducing Good Fit recall and accuracy.
Keep it as a candidate for further evaluation rather than declaring it
reliably better.

## Limitations and next steps

These are single-seed validation results. No repeated-run or statistical
uncertainty analysis establishes that the small gain is reliable.
The runs use different loss objectives, so their loss values are not directly
comparable. The custom trainer's loss normalisation is recorded explicitly.

Use error analysis, robustness checks, and inference measurements to assess
the candidates. Resolve the recall trade-offs before freezing model selection.
The official test set remains unevaluated.

Class weights and the custom loss are needed to reproduce training.
Inference uses the saved classifier with the original M3 text preparation
and paired tokenization.

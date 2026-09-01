# Independent Audit

This directory preserves the 20 paper blind audit, the pre-reconciliation scores, and the completed reconciliation worksheet.

## Main files

- `second_annotator_blind_sheet.csv` : original empty sheet sent for coding.
- `second_annotator_blind_sheet_remplis.csv` : returned independent labels.
- `second_annotator_instructions.md` : instructions supplied to the annotator.
- `primary_coding_pre_reconciliation.csv` : frozen primary labels used to reproduce pre-reconciliation agreement.
- `audit_scoring_results_pre_reconciliation.csv` : exact agreement and Cohen's kappa by field.
- `audit_disagreements_pre_reconciliation.csv`, `audit_confusion_matrices_pre_reconciliation.csv`, and `audit_transfer_stage_results_pre_reconciliation.csv` : supporting disagreement and confusion-matrix outputs.
- `audit_jaccard_pre_reconciliation.csv` : per-paper Jaccard overlap between the frozen and audit transfer-point sets; the final `MEAN` row holds the mean (0.8667).
- `audit_disagreements_for_reconciliation.csv` : evidence-backed reconciliation worksheet with normalized decisions.

Joint reconciliation is complete. All 18 rows have evidence-based notes: 11 retain the initial label and 7 accept the audit label. The pre-reconciliation scoring and disagreement files are preserved for auditability.

## Naming note

The remaining `_remplis.csv` file is the returned blind coding sheet used to reproduce pre-reconciliation agreement. The reconciliation worksheet is released only in normalized form as `audit_disagreements_for_reconciliation.csv`.

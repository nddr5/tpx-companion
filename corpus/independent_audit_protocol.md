# Independent Audit Protocol

Purpose: document an independent reliability check for a stratified subset of the TPx evidence base without modifying `papers.csv`.

Current status: the blind 20-paper coding was returned and scored against the initial labels now preserved in `second_annotator/primary_coding_pre_reconciliation.csv`. The two coders subsequently reconciled all 18 disagreements: 11 retained the initial label and 7 accepted the audit label in the canonical `papers.csv`.

Send the annotator only:

- `second_annotator/second_annotator_blind_sheet.csv`
- `second_annotator/second_annotator_instructions.md`

Do not send `papers.csv`, `scope_decisions.csv`, or the current labels before the annotator finishes.

## Audit Instructions

1. Read the title, abstract, and, when needed, the method, dataset, system, and evaluation sections of each paper.
2. Code `scope_label`, `transfer_point`, `translation_strategy`, and `resource_level` independently.
3. Use the definitions in the supplied instructions and record ambiguity in `audit_comment`.
4. Code `translation_strategy` at paper level from mechanisms actually executed, compared, or routed in the reported experiments.
5. Do not infer a runtime strategy from dataset or training-data translation, a multilingual model name, supplied contexts, or same-language evaluation.
6. Use `Hybrid` only when multiple mismatch-handling strategies are substantively implemented, compared, or routed.
7. Return the completed blind sheet before inspecting the current coding.

Allowed values:

- `scope_label`: `Core`, `Adjacent`, `Component`, `Background`
- `transfer_point`: one or more of `Retrieval`, `Generation`, `Evaluation`, joined with `|` for multi-stage papers
- `translation_strategy`: `Translate-then-retrieve`, `Retrieve-then-translate`, `Language-agnostic`, `Hybrid`, `N/A`
- `resource_level`: `High`, `Low`, `Mixed`, `N/A`

## Audit Sample

The 20-paper blind sample is stored in
`second_annotator/second_annotator_blind_sheet.csv`. It deliberately contains:

- strict cross-lingual RAG and open-retrieval QA systems;
- same-language multilingual RAG benchmarks;
- multilingual retrieval and judge components;
- low-resource and specialized-domain studies;
- boundary cases including CORA, XRAG, MIRACL, MEMERAG, Self-RAG, LegalRAG, MedExpQA, the English--Italian evaluation study, code-switched Tagalog--English RAG, and multimodal M3-RAG.

The sample is stratified to stress-test scope boundaries rather than estimate corpus-wide agreement from a random sample.

## Scoring Method

The completed blind sheet is scored as follows:

1. From `corpus/`, run:
   `python3 score_independent_audit.py --corpus second_annotator/primary_coding_pre_reconciliation.csv --audit second_annotator/second_annotator_blind_sheet_remplis.csv --summary second_annotator/audit_scoring_results_pre_reconciliation.csv --disagreements second_annotator/audit_disagreements_pre_reconciliation.csv --confusion second_annotator/audit_confusion_matrices_pre_reconciliation.csv --transfer-stage-summary second_annotator/audit_transfer_stage_results_pre_reconciliation.csv --jaccard second_annotator/audit_jaccard_pre_reconciliation.csv`.
2. Compare the current and audit labels separately for each field.
3. For `transfer_point`, the script splits on `|`, trims whitespace, sorts the labels, and counts agreement only when the two sets are identical.
4. Report exact agreement and Cohen's kappa for each field. Kappa is computed on the complete multi-label transfer-point sets, not on individual stages.
5. Report the mean per-paper Jaccard overlap between the two transfer-point sets; the per-paper values and the mean are written to `second_annotator/audit_jaccard_pre_reconciliation.csv`.
6. Inspect `second_annotator/audit_disagreements_pre_reconciliation.csv`, then adjudicate every disagreement as: keep current label, accept audit label, or revise by consensus.
7. Save adjudication notes before changing `papers.csv`.

## Reconciliation authority

The primary coder and second annotator reconcile the disagreements jointly using the released codebook and the paper evidence. Each resolved row must record one of `keep_current`, `accept_audit`, or `consensus_revision`, together with an evidence-based rationale. Because the primary coder authored the codebook, the discussion must not treat the initial label as the default solely on that basis.

If the two coders cannot reach consensus, record `unresolved` and explain the remaining interpretations. The canonical label and descriptive counts remain unchanged unless and until both coders agree to a revision; the frozen initial label remains available in `primary_coding_pre_reconciliation.csv`, and the unresolved status must remain visible in the reconciliation worksheet. No disagreement may be silently decided by either coder.

The reconciliation file is `second_annotator/audit_disagreements_for_reconciliation.csv`. The completed file records normalized `keep_current` or `accept_audit` decisions and an evidence-based note for every row.

The script writes `audit_scoring_results.csv` with this schema:

| field                | exact_matches | total | agreement_rate | cohen_kappa |
| -------------------- | ------------: | ----: | -------------: | ----------: |
| scope_label          |               |    20 |                |             |
| transfer_point       |               |    20 |                |             |
| translation_strategy |               |    20 |                |             |
| resource_level       |               |    20 |                |             |

Do not modify `papers.csv` before scoring. Reconciliation may update labels only after the pre-reconciliation kappa and disagreement log have been saved.
The pre-reconciliation agreement and kappa remain the reported reliability statistics; consensus decisions are not rescored as independent agreement.

## Results and interpretation

| field                | exact_matches | total | agreement_rate | cohen_kappa |
| -------------------- | ------------: | ----: | -------------: | ----------: |
| scope_label          |            17 |    20 |          0.850 |      0.7581 |
| transfer_point       |            13 |    20 |          0.650 |      0.5053 |
| translation_strategy |            15 |    20 |          0.750 |      0.5816 |
| resource_level       |            17 |    20 |          0.850 |      0.7143 |

The mean per-paper Jaccard overlap between the frozen and audit transfer-point sets is 0.8667 (`second_annotator/audit_jaccard_pre_reconciliation.csv`).

These remain the reported pre-reconciliation reliability results. The reconciliation resolved all 18 field-level differences across 12 papers, with 11 `keep_current` decisions and 7 `accept_audit` decisions. No row remained unresolved. The seven accepted audit labels were then applied to `papers.csv`; the original scoring outputs and pre-reconciliation disagreement log remain unchanged.

The release also includes field-level confusion matrices and binary retrieval/generation/evaluation agreement for the multi-label transfer-point field. These diagnostics are descriptive because the sample is stratified and contains only 20 papers.

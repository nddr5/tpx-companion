# TPx Corpus

This directory is the main evidence base for the TPx companion artifact. It contains the coded paper corpus and its frozen camera-ready copy, scope decisions, coding rules, search documentation, the preserved coverage-update logs, generated descriptive tables, the count-regeneration script, and independent-audit materials.

## Entry points

- `papers.csv`: canonical 116-paper coded corpus.
- `papers_frozen_camera_ready.csv`: byte-identical copy of `papers.csv` frozen at camera-ready (2026-08-30); never edited (see the root README).
- `core_papers_descriptive_table.md`: publication-facing table of the 42 Core papers.
- `scope_decisions.csv`: per-paper scope label, rationale, and confidence.
- `coding_protocol.md`: label definitions, edge-case decisions, counting unit, and known limitations.
- `search_strategy.md`: databases, complementary collection passes, query families, cutoff, and search-flow limitation.
- `coverage_check_protocol.md`, `coverage_check_candidates.csv`, `coverage_check_search_log.csv`: the June 5 coverage update; each integrated candidate carries the `paper_id` it became.
- `targeted_followup.csv`: the June 8 targeted follow-up with paper identities.
- `regenerate_paper_counts.py`: regenerates every count reported in the paper.
- `CONSISTENCY_CHECK.md`: the exact list of checks performed by the released scripts.
- `second_annotator/README.md`: independent-audit status and reconciliation files.

## Rebuildable outputs

Every count reported in the paper is regenerated from the data files (add `--json` for machine-readable output):

```bash
python3 corpus/regenerate_paper_counts.py
```

The Core descriptive tables are derived from `papers.csv` and `scope_decisions.csv`:

```bash
python3 corpus/generate_core_descriptive_table.py
```

The pre-reconciliation agreement statistics, including the per-paper Jaccard file, can be regenerated from the frozen primary labels and returned blind sheet:

```bash
python3 corpus/score_independent_audit.py \
  --corpus corpus/second_annotator/primary_coding_pre_reconciliation.csv \
  --audit corpus/second_annotator/second_annotator_blind_sheet_remplis.csv \
  --summary corpus/second_annotator/audit_scoring_results_pre_reconciliation.csv \
  --disagreements corpus/second_annotator/audit_disagreements_pre_reconciliation.csv \
  --confusion corpus/second_annotator/audit_confusion_matrices_pre_reconciliation.csv \
  --transfer-stage-summary corpus/second_annotator/audit_transfer_stage_results_pre_reconciliation.csv \
  --jaccard corpus/second_annotator/audit_jaccard_pre_reconciliation.csv
```

The generated corpus figures can be rebuilt with:

```bash
python3 corpus/generate_corpus_figures.py
```

`matplotlib` is required only for figure regeneration. The scripts in this directory use the Python standard library; the reporting-card validator in `reporting_card/` needs `PyYAML` and `jsonschema` (see `requirements.txt`).

## Corpus conventions

Paper IDs are stable rather than contiguous. `P114` was reserved for the June 8 follow-up candidate D089, which was not integrated because its full text was unavailable; later IDs were not renumbered.

`second_annotator_blind_sheet_remplis.csv` is the returned blind coding sheet used to reproduce pre-reconciliation agreement. Reconciliation decisions are released in normalized form in `second_annotator/audit_disagreements_for_reconciliation.csv`.

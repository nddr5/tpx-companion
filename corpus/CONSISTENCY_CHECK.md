# Corpus Consistency Check

This file lists exactly what the released scripts verify. Anything not listed here is not checked automatically.

## `validate_public_companion.py`

Run from the repository root (`python3 validate_public_companion.py`). The reporting-card step needs `PyYAML` and `jsonschema` from `requirements.txt`; everything else uses the Python standard library. The script exits 0 and prints `Public companion validation passed.` only when every check below holds.

### Corpus structure

- `papers.csv` has 116 rows with unique `id` and unique `citation_key` values.
- In every row, `scope_label`, each `transfer_point` stage, `translation_strategy`, `resource_level`, and `domain` belong to the label sets defined in `coding_protocol.md`.
- `scope_decisions.csv` covers exactly the corpus IDs, its `new_scope` equals `scope_label` in `papers.csv`, and every `confidence` is `high` or `medium` (no low-confidence record is integrated).
- `papers.bib` contains 116 entries whose keys equal the corpus citation keys exactly.
- `papers_frozen_camera_ready.csv` is byte-identical to `papers.csv`.
- `core_papers_descriptive_table.csv` equals the current Core rows of `papers.csv` joined with `scope_decisions.csv` (rerun `generate_core_descriptive_table.py` after any change).

### Published counts

`regenerate_paper_counts.py --json` recomputes the following from the data files, and the validator compares each value with the number stated in the paper:

- evidence base 116; scope 42 Core / 13 Adjacent / 50 Component / 11 Background;
- Core stages 38 Retrieval / 42 Generation / 15 Evaluation; stage combinations R+G 26, R+G+E 12, G+E 3, G 1; strategies 23 Language-agnostic / 10 Hybrid / 1 Translate-then-retrieve / 0 Retrieve-then-translate / 8 N/A; resource levels 33 Mixed / 5 High / 4 Low; domain 32 Open and 10 specialized;
- sensitivity: three medium-confidence Core records; without them 39 Core with 35 / 39 / 13 stages;
- June 5 coverage update 37 candidates / 27 integrated / 10 excluded; June 8 follow-up 8 assessed / 7 integrated / 1 unresolved;
- reliability audit: 18 disagreements (3 scope, 7 transfer point, 5 strategy, 3 resource), 11 resolved to the initial label and 7 to the audit label.

The report form of the same script also prints the specialized-domain breakdown and the Core+Adjacent domain profile used by `fig_domain_profile.pdf`; those are descriptive and are not compared with fixed values.

### Coverage updates

- `coverage_check_candidates.csv`: every row has a decision rationale; every `new_*` row carries a `paper_id` that exists in `papers.csv` with the same title and a scope matching the decision, and these ids are exactly `P083`--`P109`; `exclude` rows carry no `paper_id`.
- `targeted_followup.csv`: every row has a title and url; the seven integrated rows match `papers.csv` on `paper_id`, `citation_key`, `title`, and `url`; the unresolved row has no `paper_id` and records its evidence basis.
- `coverage_check_search_log.csv`: 17 passes whose `linked_candidate_rows` and `linked_core_decisions` reproduce from the candidate file.

### Reliability audit

- The blind sheet, the returned sheet, and the frozen primary sheet list the same 20 papers, stratified 11 Core / 3 Adjacent / 5 Component / 1 Background; the blind sheet is empty and the returned sheet is complete.
- `audit_scoring_results_pre_reconciliation.csv`: exact matches 17 / 13 / 15 / 17 of 20, agreement 0.85 / 0.65 / 0.75 / 0.85, Cohen's kappa 0.7581 / 0.5053 / 0.5816 / 0.7143 for scope, transfer point, strategy, and resource level.
- `audit_transfer_stage_results_pre_reconciliation.csv`: stage-wise kappa 0.5000 Retrieval / 1.0000 Generation / 0.5294 Evaluation.
- `audit_jaccard_pre_reconciliation.csv`: 20 per-paper rows and a `MEAN` row equal to 0.8667.
- The pre-reconciliation and reconciliation logs list the same 18 (paper, field) pairs; every reconciliation row has a decision and an evidence-based note; the seven accepted audit labels are applied in `papers.csv`, the eleven retained labels are unchanged, and the frozen 20-paper sheet differs from `papers.csv` in exactly those seven cells.

### Reporting cards

- `reporting_card/validate_cards.py` validates the five examples against `reporting_card.schema.json` (structure, required fields, official TPx labels, language-code pattern, URL pattern) and rejects deprecated label spellings and circular `same as L_*` references.

## Other scripts

- `score_independent_audit.py` regenerates the pre-reconciliation outputs from the frozen primary labels and the returned blind sheet; rerunning the command in the root README reproduces the committed files byte for byte.
- `generate_core_descriptive_table.py` and `generate_corpus_figures.py` regenerate the Core tables and the figures from `papers.csv`. The figure PDFs are not compared automatically; they were regenerated for the release.

## Not checked automatically

- Figure contents.
- The manuscript bibliography (41 entries); the manuscript sources are not part of this repository. `papers.csv` and `papers.bib` remain the authoritative source for corpus-level claims.
- The wording of the protocols and of `coding_protocol.md`.

## Maintenance

- Papers appearing after the March 31, 2026 cutoff go to `search_log_template.csv` before any corpus count, figure, or table is updated.
- Any edit to `papers.csv` must be accompanied by an entry in the root README changelog, an update of the published values in `validate_public_companion.py`, and a rerun of `generate_core_descriptive_table.py` and `generate_corpus_figures.py`. `papers_frozen_camera_ready.csv` is never edited.

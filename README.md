# TPx: A Pipeline-Centric Taxonomy for Cross-Lingual Retrieval-Augmented Generation

**Authors:** Nada Doulfoukar and Mehdi Adda  
**Affiliation:** Université du Québec à Rimouski (UQAR), Canada

This repository is the public camera-ready companion of the NLPIR 2026 paper *TPx: A Pipeline-Centric Taxonomy for Cross-Lingual RAG*. It provides the coded evidence base, documented scope decisions, reproducible descriptive outputs, reliability-audit materials, and machine-readable reporting cards used by the paper, together with scripts that regenerate every published count and check the release against it.

## Evidence base and scope

The publication evidence base contains **116 papers** in four mutually exclusive scope classes:

| Scope | Papers | Role in TPx |
|---|---:|---|
| Core | 42 | End-to-end RAG or open-retrieval QA with operational within-instance language transfer |
| Adjacent | 13 | Multilingual or specialized RAG without a required within-instance language mismatch |
| Component | 50 | Retrieval, generation, evaluation, model, metric, judge, or dataset contributions relevant to a TPx stage |
| Background | 11 | Foundational methods and surveys used for context |

TPx codes three primary taxonomy dimensions:

- **Transfer point:** Retrieval, Generation, and/or Evaluation.
- **Translation strategy:** Translate-then-retrieve, Retrieve-then-translate, Language-agnostic, Hybrid, or N/A.
- **Resource level:** High, Low, Mixed, or N/A.

The corpus also records domain as descriptive metadata; domain is not a fourth TPx axis.

## Historical collection record

The preserved collection and update facts are:

- Initial retained set: 82 papers (`P001`--`P082`). This is a retained-set count, not an original screening denominator.
- June 5 documented coverage update: 37 new candidates, 27 integrated (`P083`--`P109`), and 10 excluded.
- June 8 targeted follow-up: 8 candidates assessed, 7 integrated (`P110`--`P113`, `P115`--`P117`), and 1 unresolved because available evidence was insufficient for integration. The unresolved candidate, D089, is identified in `corpus/targeted_followup.csv` only by its candidate id: its title and DOI are not recoverable from the retained records.
- Final evidence base: 116 papers.

> The evidence base was assembled using a structured, taxonomy-driven protocol.
> The complete contemporaneous screened/deduplicated/excluded denominator of the
> initial iterative collection was not preserved and cannot be defensibly
> reconstructed. Descriptive counts therefore characterize the reviewed
> evidence base rather than literature-wide prevalence.

The repository does not claim exhaustive systematic coverage, a complete literature census, prevalence estimation, or a complete PRISMA denominator.

## Frozen coding sheet

`corpus/papers_frozen_camera_ready.csv` is the coding sheet frozen at camera-ready (NLPIR 2026, 2026-08-31). It is a byte-identical copy of `corpus/papers.csv` at that date and must never be edited. Any later change to the coding goes to `corpus/papers.csv` together with an entry in the [Changelog](#changelog) below. `validate_public_companion.py` reports when the two files diverge; that report is the signal that the changelog, the published values in the validator, and the generated tables and figures need updating.

## Paper claims and supporting files

| Paper claim | Supporting file(s) |
|---|---|
| Evidence base of 116 papers (42 Core / 13 Adjacent / 50 Component / 11 Background) with per-paper transfer point, translation strategy, resource level, and domain | `corpus/papers.csv`; `corpus/scope_decisions.csv`; `corpus/papers.bib` (116 entries) |
| Core TPx profile: stages 38 R / 42 G / 15 E; combinations R+G 26, R+G+E 12, G+E 3, G 1; strategies 23 Language-agnostic / 10 Hybrid / 1 Translate-then-retrieve / 0 Retrieve-then-translate / 8 N/A; resources 33 Mixed / 5 High / 4 Low; domain 32 Open + 10 specialized | `corpus/regenerate_paper_counts.py` over `corpus/papers.csv`; `corpus/core_papers_descriptive_table.md`; `figures/fig_tpx_profile.pdf`; `figures/fig_domain_profile.pdf` |
| Sensitivity: without the three medium-confidence Core records, 39 Core with 35 R / 39 G / 13 E | `corpus/scope_decisions.csv` (`confidence`); `corpus/regenerate_paper_counts.py` |
| Search protocol: databases, complementary collection passes, 12 query families, deduplication rule | `corpus/search_strategy.md`; `corpus/coverage_check_protocol.md`; `corpus/coding_protocol.md` |
| Coverage update 1 (June 5): 37 candidates, 27 integrated, 10 excluded; 17 logged search and tracing passes | `corpus/coverage_check_candidates.csv`; `corpus/coverage_check_search_log.csv`; `corpus/coverage_check_protocol.md` |
| Coverage update 2 (June 8): 8 assessed, 7 integrated, 1 unresolved | `corpus/targeted_followup.csv` |
| Exclusions with a recorded reason per candidate | `corpus/coverage_check_candidates.csv` (`decision = exclude`); `corpus/targeted_followup.csv` (D089) |
| Codebook: scope labels, transfer points, strategies, resource levels, N/A rule, Hybrid rule, counting unit | `corpus/coding_protocol.md` |
| Coding sheet frozen at camera-ready | `corpus/papers_frozen_camera_ready.csv` |
| Blind second-annotator audit on 20 stratified papers (11 Core / 3 Adjacent / 5 Component / 1 Background), raw labels, reconciliation of 18 disagreements (3 / 7 / 5 / 3; 11 initial, 7 audit) | `corpus/second_annotator/` (blind sheet, returned sheet, frozen primary labels, reconciliation log); `corpus/independent_audit_protocol.md` |
| Agreement statistics: 85% / .758, 65% / .505, 75% / .582, 85% / .714; stage-wise kappa .500 / 1.000 / .529; mean Jaccard .867 | `corpus/score_independent_audit.py`; `corpus/second_annotator/audit_scoring_results_pre_reconciliation.csv`, `audit_transfer_stage_results_pre_reconciliation.csv`, `audit_jaccard_pre_reconciliation.csv` |
| Five schema-validated reporting cards (CORA, XRAG, BERGEN, AfriQA, MEMERAG) | `reporting_card/examples/`; `reporting_card/reporting_card.schema.json`; `reporting_card/validate_cards.py` |
| Regeneration of all counts and automated checks on labels, identifiers, and bibliography | `corpus/regenerate_paper_counts.py`; `validate_public_companion.py`; `corpus/CONSISTENCY_CHECK.md` |

## Repository contents

- `corpus/papers.csv`: canonical 116-paper coded evidence base.
- `corpus/papers_frozen_camera_ready.csv`: the same sheet frozen at camera-ready; never edited.
- `corpus/papers.bib`: bibliography for all 116 corpus records.
- `corpus/coding_protocol.md`: scope and taxonomy coding rules, including the counting unit.
- `corpus/scope_decisions.csv`: paper-level scope rationales and confidence.
- `corpus/search_strategy.md`: documented collection strategy and denominator limitation.
- `corpus/coverage_check_*`: preserved June 5 protocol, candidates (each integrated candidate carries its `paper_id`), and search log.
- `corpus/targeted_followup.csv`: preserved June 8 targeted follow-up decisions with paper identities.
- `corpus/second_annotator/`: frozen reliability-audit inputs, outputs, and reconciliation record.
- `corpus/regenerate_paper_counts.py`: regenerates every count reported in the paper from the data files.
- `corpus/CONSISTENCY_CHECK.md`: the exact list of checks the released scripts perform.
- `figures/`: final publication and companion figures generated from the corpus.
- `reporting_card/`: TPx template, JSON Schema, schema validator, and five worked examples.
- `validate_public_companion.py`: checks the release against the published numbers and the artifact invariants.

## Inspect and reproduce

Install the declared dependencies once (`jsonschema` and `PyYAML` for the reporting-card validator, `matplotlib` for figure regeneration):

```bash
python3 -m pip install -r requirements.txt
```

Run the public companion checks from the repository root:

```bash
python3 validate_public_companion.py
```

Expected output:

```text
Public companion validation passed.
```

Regenerate every count reported in the paper (add `--json` for machine-readable output):

```bash
python3 corpus/regenerate_paper_counts.py
```

Validate the five reporting-card examples against the JSON Schema:

```bash
python3 reporting_card/validate_cards.py reporting_card/examples/*.yaml
```

Regenerate the pre-reconciliation agreement statistics, including the per-paper Jaccard file:

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

Regenerate the 42-paper Core table and the corpus figures:

```bash
python3 corpus/generate_core_descriptive_table.py
python3 corpus/generate_corpus_figures.py
```

## Reporting cards

Start with `reporting_card/template.yaml` and follow `reporting_card/README.md`. The five examples show how TPx coordinates and language roles can be reported for CORA, XRAG, BERGEN, AfriQA, and MEMERAG. Two optional fields, `arxiv` and `dataset_url`, may carry additional URLs. Run the validator before publishing a new or adapted card.

## Changelog

- **1.0.0 (2026-08-31)** -- NLPIR 2026 camera-ready release. `corpus/papers.csv` frozen as `corpus/papers_frozen_camera_ready.csv`.

## Citation

If you use the TPx taxonomy, corpus, or companion materials, please cite:

```bibtex
@misc{doulfoukar2026tpx,
  title   = {{TPx}: A Pipeline-Centric Taxonomy and Corpus for Cross-Lingual RAG},
  author  = {Doulfoukar, Nada and Adda, Mehdi},
  year    = {2026},
  version = {1.0.0}
}
```

Machine-readable citation metadata is available in `CITATION.cff`.

## License

- **Code:** MIT License; see `LICENSE`.
- **Data and documentation:** CC BY 4.0; see `LICENSE-data.txt`.

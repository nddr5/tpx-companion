# Search Strategy

This document records the search and selection procedure used for the TPx evidence base. The review is structured and taxonomy-driven; it is not used to estimate publication prevalence or to claim exhaustive coverage of the field.

## Coverage and cutoff

- Main publication window: January 2020 to March 31, 2026.
- One earlier evaluation paper is retained as a component.
- Cutoff-preserving update executed: June 5, 2026.
- Targeted cross-source follow-up executed: June 8, 2026.

## Sources

- ACL Anthology
- arXiv
- Google Scholar

Google Scholar was used during the initial keyword-search collection
(see `coding_protocol.md`). The two documented coverage updates followed
the source list frozen in `coverage_check_protocol.md`.

## Complementary collection passes

- Keyword searches over major NLP, IR, and ML venue proceedings
- Backward and forward citation tracing, from the initial seeds during
  the first collection and from Core papers during the first coverage
  update (passes C1–C5 in `coverage_check_search_log.csv`)

## Query families

Searches combined `cross-lingual` or `multilingual` with:

- `RAG`
- `retrieval-augmented generation`
- `open-retrieval question answering`
- `dense retrieval`
- `RAG evaluation`
- `LLM-as-judge`
- `language drift`

Canonical seeds included CORA, XOR-QA, MIRACL, BERGEN, and XRAG. Candidate papers were expanded through backward and forward citation tracing.

The June 5 update began with the eight frozen query families in
`coverage_check_protocol.md`. A same-day audit then showed that `open-retrieval QA` under-recovered papers using `open-domain QA` and `retrieve-then-read` terminology. Four additional query families were added, and all eligible records found in that update were integrated. The executed searches and candidate decisions are recorded in `coverage_check_search_log.csv` and `coverage_check_candidates.csv`.

A prospective cross-source audit on June 8 was explored as a possible denominator-producing workflow. It did not recover the existing corpus reliably and was not screened to completion, so its source totals are not used as a manuscript denominator. Eight high-priority candidates exposed by that audit were checked individually. Seven met the existing Core definition and were integrated. One was not integrated because the unavailable full text prevented auditable verification beyond the indexed abstract. Their decisions and evidence basis are recorded in `targeted_followup.csv`.

## Eligibility

A paper entered the evidence base when it materially addressed retrieval, generation, faithfulness, or evaluation in a multilingual or cross-lingual setting relevant to a RAG pipeline.

The review excluded:

- standalone machine translation without a RAG-relevant experiment;
- general multilingual pretraining without a relevant pipeline contribution;
- papers that mentioned multilinguality only as future work;
- duplicate records or versions without a distinct contribution;
- non-archival web manuscripts outside peer-reviewed proceedings, journals, and arXiv.

Inclusion in the evidence base was followed by a separate scope decision: `Core`, `Adjacent`, `Component`, or `Background`. The definitions and edge-case rules are in `coding_protocol.md`; paper-level decisions are in `scope_decisions.csv`.

## Search-flow limitation

The original collection was built iteratively from seeds, venue searches, and snowballing rather than from one exportable database query. Ranked web-search totals were also unavailable or unstable. The June 8 prospective audit did produce source-level totals, but its low recovery of the known corpus and incomplete screening mean that those totals are not a valid denominator for the final evidence base. TPx therefore reports final evidence-base and scope counts, but does not claim exhaustive coverage or estimate publication prevalence. `search_log_template.csv` remains available so future updates can record source-level hit and screening counts prospectively.

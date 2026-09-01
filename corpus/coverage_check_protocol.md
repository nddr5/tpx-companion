# Search Coverage Check Protocol

> **Status amendment, June 8, 2026:** this document preserves the June 5 protocol and its same-day results. A later targeted cross-source follow-up identified eight high-priority candidates. Seven were integrated as Core; one was not integrated because its unavailable full text prevented an auditable decision beyond the indexed abstract. Consequently, the June 5 no-add result must not be presented as evidence of exhaustive coverage. See `targeted_followup.csv` and `search_strategy.md`.

Protocol frozen before the final search on 2026-06-05.

## Terminology amendment

A same-day audit found that the frozen family using the phrase `open-retrieval question answering` under-covered papers using `open-domain question answering` or `retrieve-then-read` terminology.
The initial C2/C3 no-add result is therefore not treated as sufficient evidence of exhaustive coverage. Four additional query families (Q9--Q12) and two new confirmation passes (C4--C5) were executed and logged. All eligible additions from that expansion were integrated before corpus counts were recomputed.

## Objective

Reduce the risk that the TPx Core set depends on a narrow seed selection, without treating the search as an exhaustive prevalence estimate. The search asks whether accessible database queries and citation tracing identify any additional paper satisfying the operational Core definition.

## Core eligibility

A paper is Core when its primary contribution is a RAG or open-retrieval QA system, benchmark, or evaluation in which successful behavior requires an operational language transfer within an inference instance. At least one of the following must hold:

- query language differs from evidence language;
- evidence language differs from answer language;
- evaluation directly studies such a cross-language configuration.

Same-language multilingual RAG is Adjacent. Retriever, generator, metric, judge, or dataset papers without an end-to-end RAG or open-retrieval QA setup are Component. General methods and surveys are Background.

Translation strategy is coded at paper level from mismatch-handling mechanisms actually executed, compared, or routed in the reported experiments. Human translation used only for dataset or training-data construction, multilingual model capability alone, and supplied contexts without an attributable runtime mechanism do not establish a translation strategy.

## Sources

The final search uses sources whose records can be inspected without claiming subscription-only access:

1. ACL Anthology;
2. arXiv.

ACM Digital Library, IEEE Xplore, Scopus, and Web of Science are not claimed as independently queried databases in this coverage-check pass unless an inspectable result is recorded in the search log.

## Complementary collection passes

1. indexed scholarly web search over peer-reviewed proceedings and journals (logged as "indexed scholarly web" in `coverage_check_search_log.csv`);
2. backward and forward citation tracing from the 14 Core papers present when the protocol was frozen (see "Citation tracing" below).

## Query families

The following eight query families are frozen:

1. `"cross-lingual retrieval-augmented generation"`
2. `"cross-lingual RAG"`
3. `"multilingual retrieval-augmented generation" cross-lingual`
4. `"cross-lingual open-retrieval question answering"`
5. `"multilingual RAG" "language drift"`
6. `"cross-lingual" RAG evaluation`
7. `"cross-lingual" RAG faithfulness attribution`
8. `multilingual RAG low-resource language retrieval generation`

Syntax may be adapted to a source, but the semantic query family must be preserved and the executed query must be recorded verbatim.

The terminology amendment added:

9. `"cross-lingual open-domain question answering" retrieval generation`
10. `"multilingual open-domain question answering" retriever generator`
11. `"cross-lingual" RAG chatbot retrieval generation`
12. `multilingual vision-language retrieval augmented generation`

## Screening and decisions

1. Inspect all distinct plausible scholarly candidates returned in the accessible result set.
2. Deduplicate by DOI, arXiv identifier, normalized title, then title--first-author--year.
3. Compare candidates against `papers.csv` and `scope_decisions.csv`.
4. Read the abstract and, when needed, the method or task description.
5. Record one of:
   - `existing`;
   - `new_core`;
   - `new_adjacent`;
   - `new_component`;
   - `new_background`;
   - `exclude`.
6. Give every non-existing candidate a decision rationale and source URL.

The search log columns `linked_candidate_rows` and `linked_core_decisions` are derived directly from `coverage_check_candidates.csv`: they count rows whose pipe-delimited `discovery_search_ids` contains the search ID, and the subset of those rows whose final decision is `new_core`. Because one candidate may be linked to several searches, these columns are not additive and do not mean "first discovered in this pass." `screened_distinct` and `existing_records` remain pass-level screening counts.

The coded record set includes peer-reviewed proceedings and journal papers, plus arXiv preprints. Other non-archival web manuscripts are logged when found but are not added to the coded evidence base.

## Citation tracing

For each current Core paper:

- inspect its reference list or related-work trail for earlier candidates;
- inspect indexed citing or closely related records for later candidates;
- apply the same Core definition.

If a tracing or added-query pass adds a Core paper, run two further confirmation passes after deduplication. Two consecutive confirmation passes without a new Core paper are treated as an operational stopping rule, not proof of exhaustiveness.

## Reporting rule

The manuscript must not state that the search establishes exhaustive coverage. The artifact reports a structured, taxonomy-driven evidence base rather than a publication-prevalence denominator. Any future coverage statement would require:

- all query families to be logged;
- citation-tracing and confirmation passes to be logged;
- plausible excluded candidates to have documented decisions.

If a future update adds a Core paper, update the corpus, scope decisions, figures, abstract, tables, discussion, limitations, and conclusion before making any coverage statement. Shared-task overview papers and their system-description papers remain separate publication units, but shared benchmark reuse must be reported to prevent interpretive double counting.

## Limitations

- Search-engine result totals and ranking are not fully reproducible.
- Subscription databases are not treated as queried without direct access.
- Screening remains single-reviewer unless an independent human review is subsequently completed.
- Coverage checks reduce selection risk but do not establish exhaustive publication prevalence.

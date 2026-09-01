# Independent TPx Coding Instructions

Thank you for independently coding this 20 paper audit sample. The purpose is to assess the reliability of a taxonomy for multilingual and cross-lingual retrieval-augmented generation (RAG). There are no expected answers in the files you received.

## What to return

Complete `second_annotator_blind_sheet.csv` and return the same CSV file.
Do not rename columns, remove rows, or change the paper identifiers.

For every paper, fill:

- `audit_scope_label`
- `audit_transfer_point`
- `audit_translation_strategy`
- `audit_resource_level`
- `audit_comment` when the decision is uncertain or requires a caveat

## Reading procedure

1. Open the paper using the URL in the sheet.
2. Read the title and abstract.
3. When the label is not clear, inspect the task definition, data, system, retrieval, generation, and evaluation sections.
4. Code what the paper actually implements or evaluates, not what it only mentions in related work or future work.
5. If full text cannot be accessed, use the abstract and record `full text unavailable` in `audit_comment`.

## Scope label

Use exactly one value:

- `Core`: a RAG or open-retrieval QA system, benchmark, or evaluation in which successful behavior requires language transfer within an inference instance. Examples include query language different from evidence language, answer language different from evidence language, or direct evaluation of these mismatched configurations.
- `Adjacent`: a multilingual, non-English, low-resource, or domain-specific RAG study whose reported instances do not require a language mismatch.
- `Component`: a retriever, generator, metric, judge, dataset, or related task that informs a RAG stage but does not evaluate an end-to-end cross-lingual RAG or open-retrieval QA setup.
- `Background`: foundational or contextual work that should not be counted as multilingual or cross-lingual RAG evidence.

Important boundary rule: multilingual coverage or code-switching alone does not automatically make a paper `Core`. Look for an operational language mismatch within an individual retrieval, generation, or evaluation instance.

## Transfer point

Use one or more values joined by `|`, for example `Retrieval|Generation|Evaluation`:

- `Retrieval`: the paper contributes or evaluates retrieval under multilingual or cross-lingual conditions.
- `Generation`: it contributes or evaluates answer generation, evidence use, faithfulness, language control, or language drift.
- `Evaluation`: it contributes or evaluates multilingual metrics, judges, benchmark protocols, attribution, or end-to-end RAG assessment.

Assign a stage only when it is part of the paper's contribution, dataset, or empirical analysis, not merely a component used without analysis.

## Translation strategy

Use exactly one value:

- `Translate-then-retrieve`: the query is translated before retrieval.
- `Retrieve-then-translate`: evidence is retrieved first and then translated for downstream generation or evaluation.
- `Language-agnostic`: multilingual representations or generators handle the mismatch without explicit runtime translation.
- `Hybrid`: more than one strategy is implemented, evaluated, or routed between as part of the reported system.
- `N/A`: the paper does not prescribe a runtime pipeline strategy.

Do not infer a runtime strategy from human translation used only to construct a dataset or benchmark.

## Resource level

Use exactly one value:

- `High`: the main evaluation focuses on high-resource languages.
- `Low`: the main contribution explicitly targets scarce-data or under-represented languages.
- `Mixed`: the same study covers both high- and lower-resource languages.
- `N/A`: no meaningful resource setting can be assigned.

## Comments

Use `audit_comment` to explain:

- uncertainty between two scope labels;
- inaccessible full text;
- benchmark-versus-system ambiguity;
- multiple possible translation strategies;
- any decision that depends on a narrow interpretation of the experiment.

Please do not leave any of the four label columns empty. Thank you.

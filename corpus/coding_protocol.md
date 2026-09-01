# Coding Protocol

This document specifies how each paper in `papers.csv` was assigned its TPx labels. It is written for reproducibility and inspection of coding decisions.

## Review type and cutoff

The corpus supports a structured, taxonomy-driven survey rather than a full PRISMA-style systematic review. The goal is to make the TPx coding decisions inspectable and extensible. The corpus is frozen at a March 31, 2026 literature cutoff. A cutoff-preserving update was executed on June 5, 2026, followed by a targeted cross-source follow-up on June 8, 2026. Papers appearing after the cutoff are logged separately rather than added.

Candidate papers were collected through five passes:

1. Seed papers on RAG, cross-lingual open-retrieval QA, multilingual dense retrieval, and multilingual evaluation.
2. Keyword searches over ACL Anthology, arXiv, major NLP/IR/ML venues, Semantic Scholar, and Google Scholar.
3. Backward and forward citation tracing from central papers.
4. A final search using eight frozen query families and a corrective four-family amendment for open-domain QA terminology.
5. A targeted June 8 follow-up that checked eight high-priority candidates against the same Core definition. This follow-up was not a complete screening flow and is not used as an exhaustive denominator.

Use `search_log_template.csv` for any future extension of the corpus.

## Scope label

The evidence base uses four roles. Only `Core` papers are used for the primary TPx profile. `Core + Adjacent` is reported as a secondary sensitivity view.
`Component` and `Background` papers support the qualitative synthesis but are not counted as cross-lingual RAG systems.

- **Core**: the primary contribution is a RAG or open-retrieval QA system, benchmark, or evaluation in which successful behavior requires an operational language transfer within an inference instance. Examples include a query language different from the evidence language, an answer language different from the evidence language, or an evaluation protocol that directly compares such configurations.
- **Adjacent**: the paper directly studies RAG in a multilingual, non-English, low-resource, or domain-specific setting, but the reported setup does not require an intra-instance language mismatch. These papers inform the boundary of TPx without being counted as strict cross-lingual RAG.
- **Component**: the paper contributes a retriever, multilingual LLM, metric, judge, dataset, or adjacent task that materially informs a TPx stage, but it does not evaluate an end-to-end RAG or open-retrieval QA setting.
- **Background**: foundational methods and surveys used for context and positioning. They are excluded from corpus-level TPx counts.

The per-paper rationale and confidence are recorded in `scope_decisions.csv`.

### Scope-decision confidence

Confidence describes the evidence available for the scope decision, not the importance or quality of the paper.

- **high**: the full text or an official detailed record establishes the task, pipeline stages, and within-instance language configuration.
- **medium**: the decision is supported by an official abstract, publisher preview, or incomplete full text, but at least one boundary-relevant detail remains indirect.
- **low**: the available record does not permit an auditable scope decision. Low-confidence candidates are logged but are not integrated into `papers.csv`.

## Transfer point (non-exclusive)

A paper is labeled with a stage if it contributes a method, dataset, metric, or empirical analysis specifically targeting that stage. Multi-stage papers receive multiple labels.

- **Retrieval**: multilingual embedding models, cross-lingual dense retrieval, multilingual retrieval benchmarks where retrieval quality is the primary measured outcome.
- **Generation**: cross-lingual answer generation, language drift, multilingual instruction tuning when used as a RAG generator, or faithfulness in generated outputs.
- **Evaluation**: multilingual metrics, LLM-as-judge across languages, or end-to-end RAG meta-evaluation.

## Translation strategy (paper-level and runtime-attributable)

Use exactly one of the following five labels:

- **Translate-then-retrieve**: the reported runtime configuration translates the query before retrieval.
- **Retrieve-then-translate**: evidence is retrieved in the source language, then translated for downstream generation or evaluation.
- **Language-agnostic**: the reported runtime pipeline handles the language mismatch directly through multilingual representations or generation, without explicit runtime translation.
- **Hybrid**: the paper implements, routes between, or substantively compares more than one of the strategies above as part of its reported experimental design.
- **N/A**: the paper does not provide enough evidence to attribute one of the four runtime strategies above.

The coding unit is the paper's reported experimental design, not the general capability of a model named in the paper. Before assigning a non-`N/A` label, identify the concrete inference-time or evaluation-time mechanism that handles the language mismatch.

Assign `N/A` when translation or multilinguality appears only in:

- dataset, benchmark, or training-data construction;
- a pretrained multilingual component that is not itself evaluated as the paper's mismatch-handling mechanism;
- supplied, oracle, or preconstructed contexts with no attributable runtime transfer mechanism;
- related work, motivation, or future work;
- a monolingual or same-language multilingual configuration;
- a survey, metric, judge, dataset, or benchmark that does not execute or compare a runtime strategy.

The strategy field is applicable across scope labels only when a paper actually executes, compares, or routes a cross-language mismatch-handling mechanism. A `Component` paper may therefore receive a non-`N/A` strategy when that mechanism is its direct object of study. `Adjacent` same-language multilingual RAG and `Background` work default to `N/A`; a non-`N/A` exception requires an explicit cross-language runtime experiment documented in the row notes.

### Dominant versus auxiliary strategy

When a paper mentions several strategies but evaluates only one as its substantive mismatch-handling design, code that evaluated strategy. Use `Hybrid` when multiple strategies are actually implemented, compared, or routed within the reported experiments, even if the paper is primarily a benchmark. Do not assign `Hybrid` solely because a paper discusses translation and multilingual embeddings in related work, uses the word "hybrid" for sparse+dense retrieval, or translates data offline.

When several runtime operations occur in one pipeline, code the mechanism that determines retrieval access unless the pipeline genuinely retains multiple routes. For example, translating a query before retrieval and translating the final answer back to the user remains `Translate-then-retrieve`; selectively translating only foreign-language retrieved passages while directly using same-language passages is `Hybrid`.

## Resource level

Use exactly one of the following labels:

- **High**: focuses on high-resource pairs, such as English, French, German, Spanish, Chinese, or Japanese.
- **Low**: explicitly targets under-represented or scarce-data languages.
- **Mixed**: covers both high- and lower-resource languages within the same model, benchmark, or evaluation suite.
- **N/A**: surveys, metrics, or component-level papers without a single resource setting.

### Mixed-resource coding rule

When a benchmark or model covers both high-resource and lower-resource languages, code the resource level as `Mixed`, even if most reported results are from high-resource languages. Use `Low` only when the paper explicitly targets under-represented languages or when the main evaluation is centered on scarce-data language settings.

## Domain (descriptive metadata)

`domain` is not a fourth TPx axis. It records the primary application or evaluation setting using exactly one of these values:

- **Open**: open-domain retrieval or QA over broad corpora such as Wikipedia, news collections used as general knowledge sources, or mixed-topic web data.
- **General**: methods, surveys, metrics, or language-model studies without a specific retrieval corpus or application domain.
- **Medical**, **Legal**, **Cultural**, **News**, **Agriculture**, **Enterprise**, **Climate**, **Religious**, or **Education**: use when the paper's main data, task, or deployment setting is explicitly specialized.

The `Open`/`General` boundary follows the evaluated object: use `Open` when the paper evaluates broad-domain retrieval, QA, or RAG; use `General` when it studies a general method, model, metric, or survey without such an evaluated open-domain corpus. Do not invent a one-paper domain label without first updating this protocol and all validation code.

## Edge cases and decisions

- **CORA**: `Core`, `Language-agnostic`, and `Mixed`. It performs cross-lingual dense retrieval without a runtime translation module.
- **Language Drift (P009)**: `Core`, `Generation`, and `Language-agnostic`. Retrieved evidence differs from the intended output language, and Soft Constrained Decoding handles that mismatch directly at generation time by steering decoder tokens rather than translating the query or evidence.
- **XRAG**: `Core` and `Language-agnostic`. Human translation is part of dataset construction, but the evaluated multilingual LLM directly handles query-evidence language mismatch at runtime without a translation module.
- **MIRACL**: `Component`. Queries and corpora are in the same language and the benchmark does not contain a generation stage; its strategy is `N/A`, not `Language-agnostic`.
- **MEMERAG**: `Adjacent`. It is a native multilingual RAG meta-evaluation benchmark, but each evaluated language configuration is same-language.
- **Self-RAG**: `Background`. It is a foundational RAG architecture, not a multilingual or cross-lingual study.
- **mRAKL**: `Core` and `Language-agnostic`. It evaluates cross-lingual link prediction and high-to-low-resource transfer without runtime translation.
- **AfriQA and XOR-QA**: `Core` and `Hybrid`. Both papers substantively compare translation-based and direct multilingual runtime pipelines; the paper-level label therefore represents the comparison rather than one selected baseline.
- **MedExpQA**: `Core` and strategy `N/A`. Translation is used to construct the multilingual benchmark, but the paper does not establish an attributable runtime mismatch-handling mechanism.
- **QTT-RAG**: `Core` and `Hybrid`. Same-language passages are used directly, while foreign-language passages are translated after retrieval.
- **Bengali agricultural RAG (P090)**: `Core` and `Translate-then-retrieve`. The query is translated before retrieval; later answer translation does not change the primary retrieval-access strategy.
- **Counting unit**: the publication is the counting unit throughout the evidence base; shared-task overview papers and their system submissions are counted as separate publications and are flagged as non-independent because they share task data and evaluation setup.
- **MIA 2022 publications**: the shared-task overview and four coded system papers, including the later P116 report, are separate publication units. They remain separately coded, but their shared MIA task, adapted XOR-TyDi and MKQA data, and evaluation setup must be disclosed so paper counts are not interpreted as independent benchmark counts. P102 and P103 use related cross-lingual QA settings but are not counted as additional MIA submissions.
- **Code-switched Tagalog-English RAG (P112)**: `Core`. Code-switching alone would not satisfy the Core definition, but this study constructs English, Tagalog, and Taglish query groups for every source document irrespective of that document's language. Its evaluation therefore includes explicit within-instance query-evidence language mismatches.
- **M3-RAG (P115)**: `Core` with medium confidence. Available indexed metadata describes cross-lingual text and image retrieval with language-conditioned generation through shared multilingual and cross-modal representations; its reconciled strategy is `Language-agnostic`. The full text was not openly accessible for the initial independent audit.
- **M4-RAG**: `Core` because it explicitly evaluates within-instance language changes in prompts and retrieved evidence; its multimodal setting does not remove the operational language-transfer requirement.
- **Open-domain QA terminology**: retrieve-then-read papers are eligible when they perform cross-language retrieval and answer production, even when they do not use the later term RAG.
- **VLR-Bench**: `Adjacent` because its multilingual vision-language RAG configurations do not require a query-evidence language mismatch.
- **June 8 targeted follow-up**: eight candidates were checked; seven were integrated and one was left outside the coded corpus because its full text was unavailable. The evidence used for each decision is documented in `targeted_followup.csv`. Where full text was not openly accessible, the decision is explicitly based on publisher or indexed abstracts and its confidence reflects that limitation.
- **Stable identifier gap (P114)**: this identifier was reserved during the June 8 integration for candidate D089. The record was not integrated because its unavailable full text did not permit an auditable decision. IDs were not renumbered afterward so references to P110--P113 and P115--P117 remain stable.

## Known limitations

- The corpus supports a structured, taxonomy-driven review rather than a fully exhaustive PRISMA-style systematic review.
- Edge cases were resolved using the narrowest label supported by each paper's stated task and experiments; medium-confidence decisions are explicitly marked in `scope_decisions.csv`.
- The coding protocol is designed for auditability, but taxonomy assignment may still involve judgment for papers spanning multiple stages or strategies.
- The independent 20-paper coding was scored against frozen initial labels. All 18 disagreements were subsequently reconciled with evidence-based notes; 7 audit labels were accepted and applied to `papers.csv`.
- Coding cutoff: March 31, 2026.

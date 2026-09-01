# TPx Reporting Card

A cross-lingual RAG result is uninterpretable without an explicit specification of where cross-lingual transfer occurs and how language mismatch is handled.

This directory provides a minimal, machine-readable reporting card for cross-lingual RAG experiments: an empty template, JSON Schema, a schema validator, and five filled examples.

## Files

- `template.yaml` : empty template for new systems.
- `reporting_card.schema.json` : JSON Schema for the card structure and allowed
  TPx values. Besides the required fields, two optional URL fields are allowed:
  `arxiv` and `dataset_url`.
- `validate_cards.py` : validator that checks filled YAML cards against the JSON
  Schema (needs `PyYAML` and `jsonschema`; see `requirements.txt`).
- `examples/` : five filled cards on landmark systems:
  - `CORA.yaml` : early cross-lingual open-retrieval QA
  - `XRAG.yaml` : recent cross-lingual RAG benchmark
  - `BERGEN.yaml` : multilingual RAG empirical study
  - `AfriQA.yaml` : low-resource African-language QA
  - `MEMERAG.yaml` : multilingual meta-evaluation benchmark

## Filling a card

1. Copy `template.yaml` to `examples/<your-system>.yaml`.
2. Use ISO 639 language codes where possible (`en`, `fr`, `ja`, `ar`, …).
   BCP 47 tags are permitted for regional variants such as `zh-CN`. For lists, use YAML list syntax: `[en, ja, fi]`.
3. For `transfer_point`, list every pipeline stage the system addresses: `[Retrieval]`, `[Retrieval, Generation]`, or `[Retrieval, Generation, Evaluation]`.
4. For `translation_strategy`, pick one of the five categories defined in the taxonomy section of the survey: `Translate-then-retrieve` `Retrieve-then-translate`, `Language-agnostic`, `Hybrid`, or `N/A`.
   Report the mechanism executed by the system at runtime. Use `N/A` when translation appears only in data construction or when no runtime mechanism is attributable. Use `Hybrid` only when multiple strategies are actually implemented, compared, or routed.
5. For `resource_level`, pick `High`, `Mixed`, `Low`, or `N/A`.
6. If a metric is not reported in the paper, write `not_reported` (do not leave the field blank; explicit absence is informative).
7. Use the `notes:` block for anything that does not fit the structured fields.

## Validation

Install the validator dependencies once from the repository root (`python3 -m pip install -r requirements.txt`), then run the validator from this directory before submitting a new reporting card:

```bash
python3 validate_cards.py examples/*.yaml
```

The validator loads each card as YAML and validates it against `reporting_card.schema.json`: required fields, no unknown fields, official TPx labels, ISO 639 / BCP 47 language-code pattern, HTTP(S) URLs, and non-empty metric strings. On top of the schema it rejects deprecated label spellings (`T-then-R`, `R-then-T`, `Lang-agnostic`) and circular `same as L_*` references.

## Key fields

Each field corresponds to a reporting need discussed in the survey:

| Field                              | Why it matters                                                                                        | Survey reference |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------- |
| `language_config`                  | Cross-lingual results depend on which language roles mismatch: query, evidence, answer, and reference | §2, Rec1         |
| `transfer_point`                   | Identifies which pipeline stage carries the cross-lingual burden                                      | §3.1             |
| `translation_strategy`             | Makes explicit how language mismatch is handled operationally                                         | §3.2             |
| `resource_level`                   | Separates high-resource, low-resource, and mixed-resource evaluation settings                         | §3.3             |
| `metrics.output_language_accuracy` | Captures language drift separately from answer correctness                                            | Rec3             |

## Local use

The template and validator document the expected format for local checks. Contributions can add new examples without changing the official TPx labels enforced by the schema.

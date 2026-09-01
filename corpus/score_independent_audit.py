"""Score a returned blind coding sheet against the frozen primary labels.

Outputs (all CSV): per-field exact agreement and Cohen's kappa, the
field-level disagreement log, exact-label confusion matrices, binary
per-stage agreement for the multi-label transfer-point field, and the
per-paper Jaccard overlap between the two transfer-point sets together with
its mean. See ``independent_audit_protocol.md`` for the documented command.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


FIELDS = (
    ("scope_label", "audit_scope_label"),
    ("transfer_point", "audit_transfer_point"),
    ("translation_strategy", "audit_translation_strategy"),
    ("resource_level", "audit_resource_level"),
)

ALLOWED = {
    "scope_label": {"Core", "Adjacent", "Component", "Background"},
    "transfer_point": {"Retrieval", "Generation", "Evaluation"},
    "translation_strategy": {
        "Translate-then-retrieve",
        "Retrieve-then-translate",
        "Language-agnostic",
        "Hybrid",
        "N/A",
    },
    "resource_level": {"High", "Low", "Mixed", "N/A"},
}


def normalize(field: str, value: str) -> str:
    value = value.strip()
    if field != "transfer_point":
        return value
    labels = sorted(part.strip() for part in value.split("|") if part.strip())
    return "|".join(labels)


def stage_set(value: str) -> set[str]:
    return {part.strip() for part in value.split("|") if part.strip()}


def read_rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or key not in rows[0]:
        raise ValueError(f"{path} does not contain the required column {key!r}")
    return {row[key].strip(): row for row in rows}


def cohen_kappa(left: list[str], right: list[str]) -> float:
    total = len(left)
    observed = sum(a == b for a, b in zip(left, right)) / total
    left_counts = Counter(left)
    right_counts = Counter(right)
    labels = set(left_counts) | set(right_counts)
    expected = sum(
        (left_counts[label] / total) * (right_counts[label] / total)
        for label in labels
    )
    if expected == 1.0:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


def write_csv(path: Path, rows: list[dict], fieldnames) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=Path("papers.csv"))
    parser.add_argument(
        "--audit", type=Path, default=Path("second_annotator_blind_sheet.csv")
    )
    parser.add_argument(
        "--summary", type=Path, default=Path("audit_scoring_results.csv")
    )
    parser.add_argument(
        "--disagreements", type=Path, default=Path("audit_disagreements.csv")
    )
    parser.add_argument(
        "--confusion", type=Path, default=Path("audit_confusion_matrices.csv")
    )
    parser.add_argument(
        "--transfer-stage-summary",
        type=Path,
        default=Path("audit_transfer_stage_results.csv"),
    )
    parser.add_argument(
        "--jaccard",
        type=Path,
        default=Path("audit_jaccard.csv"),
        help="per-paper Jaccard overlap of the transfer-point sets, with a final MEAN row",
    )
    args = parser.parse_args()

    corpus = read_rows(args.corpus, "id")
    audit = read_rows(args.audit, "paper_id")
    missing_ids = sorted(set(audit) - set(corpus))
    if missing_ids:
        raise ValueError(f"Audit IDs missing from corpus: {', '.join(missing_ids)}")

    incomplete = []
    for paper_id, row in audit.items():
        for _, audit_field in FIELDS:
            if not row.get(audit_field, "").strip():
                incomplete.append(f"{paper_id}:{audit_field}")
    if incomplete:
        preview = ", ".join(incomplete[:8])
        raise ValueError(
            f"Blind audit is incomplete ({len(incomplete)} empty labels): {preview}"
        )

    invalid = []
    for paper_id, row in audit.items():
        for corpus_field, audit_field in FIELDS:
            value = normalize(corpus_field, row[audit_field])
            labels = set(value.split("|")) if corpus_field == "transfer_point" else {value}
            if not labels.issubset(ALLOWED[corpus_field]):
                invalid.append(f"{paper_id}:{audit_field}={value!r}")
    if invalid:
        preview = ", ".join(invalid[:8])
        raise ValueError(f"Blind audit contains invalid labels: {preview}")

    summary_rows = []
    disagreement_rows = []
    confusion_rows = []
    for corpus_field, audit_field in FIELDS:
        current = []
        independent = []
        exact = 0
        for paper_id, audit_row in audit.items():
            corpus_value = normalize(corpus_field, corpus[paper_id][corpus_field])
            audit_value = normalize(corpus_field, audit_row[audit_field])
            current.append(corpus_value)
            independent.append(audit_value)
            if corpus_value == audit_value:
                exact += 1
            else:
                disagreement_rows.append(
                    {
                        "paper_id": paper_id,
                        "field": corpus_field,
                        "current_label": corpus_value,
                        "audit_label": audit_value,
                        "audit_comment": audit_row.get("audit_comment", ""),
                        "adjudication_decision": "",
                        "adjudication_note": "",
                    }
                )
        total = len(current)
        summary_rows.append(
            {
                "field": corpus_field,
                "exact_matches": exact,
                "total": total,
                "agreement_rate": f"{exact / total:.4f}",
                "cohen_kappa": f"{cohen_kappa(current, independent):.4f}",
            }
        )
        pair_counts = Counter(zip(current, independent))
        for (current_label, audit_label), count in sorted(pair_counts.items()):
            confusion_rows.append(
                {
                    "field": corpus_field,
                    "current_label": current_label,
                    "audit_label": audit_label,
                    "count": count,
                }
            )

    write_csv(args.summary, summary_rows, summary_rows[0].keys())
    write_csv(
        args.disagreements,
        disagreement_rows,
        (
            "paper_id",
            "field",
            "current_label",
            "audit_label",
            "audit_comment",
            "adjudication_decision",
            "adjudication_note",
        ),
    )
    write_csv(args.confusion, confusion_rows, confusion_rows[0].keys())

    transfer_rows = []
    for stage in ("Retrieval", "Generation", "Evaluation"):
        current = []
        independent = []
        for paper_id, audit_row in audit.items():
            current_stages = stage_set(corpus[paper_id]["transfer_point"])
            audit_stages = stage_set(audit_row["audit_transfer_point"])
            current.append("present" if stage in current_stages else "absent")
            independent.append("present" if stage in audit_stages else "absent")
        pairs = Counter(zip(current, independent))
        exact = sum(left == right for left, right in zip(current, independent))
        total = len(current)
        transfer_rows.append(
            {
                "stage": stage,
                "exact_matches": exact,
                "total": total,
                "agreement_rate": f"{exact / total:.4f}",
                "cohen_kappa": f"{cohen_kappa(current, independent):.4f}",
                "true_negative": pairs[("absent", "absent")],
                "false_positive": pairs[("absent", "present")],
                "false_negative": pairs[("present", "absent")],
                "true_positive": pairs[("present", "present")],
            }
        )
    write_csv(args.transfer_stage_summary, transfer_rows, transfer_rows[0].keys())

    # Per-paper Jaccard overlap between the frozen and audit transfer-point sets.
    jaccard_rows = []
    scores = []
    for paper_id, audit_row in audit.items():
        current_stages = stage_set(corpus[paper_id]["transfer_point"])
        audit_stages = stage_set(audit_row["audit_transfer_point"])
        union = current_stages | audit_stages
        intersection = current_stages & audit_stages
        score = len(intersection) / len(union) if union else 1.0
        scores.append(score)
        jaccard_rows.append(
            {
                "paper_id": paper_id,
                "current_transfer_point": normalize("transfer_point", corpus[paper_id]["transfer_point"]),
                "audit_transfer_point": normalize("transfer_point", audit_row["audit_transfer_point"]),
                "intersection_size": len(intersection),
                "union_size": len(union),
                "jaccard": f"{score:.4f}",
            }
        )
    mean_jaccard = sum(scores) / len(scores)
    jaccard_rows.append(
        {
            "paper_id": "MEAN",
            "current_transfer_point": "",
            "audit_transfer_point": "",
            "intersection_size": "",
            "union_size": "",
            "jaccard": f"{mean_jaccard:.4f}",
        }
    )
    write_csv(args.jaccard, jaccard_rows, jaccard_rows[0].keys())

    print(
        "Wrote "
        f"{args.summary}, {args.disagreements}, {args.confusion}, "
        f"{args.transfer_stage_summary}, and {args.jaccard}"
    )
    print(f"Mean per-paper transfer-point Jaccard: {mean_jaccard:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Regenerate every descriptive count reported in the TPx paper.

No count is hard-coded. Corpus-level numbers are recomputed from
``papers.csv`` and ``scope_decisions.csv``; the two coverage-update tallies
from ``coverage_check_candidates.csv`` and ``targeted_followup.csv``; and the
reliability-audit table from
``second_annotator/audit_disagreements_for_reconciliation.csv``.

Run from anywhere::

    python3 corpus/regenerate_paper_counts.py          # readable report
    python3 corpus/regenerate_paper_counts.py --json   # machine-readable

``validate_public_companion.py`` runs the ``--json`` form and compares the
result with the values stated in the publication.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent
SCOPES = ("Core", "Adjacent", "Component", "Background")
STAGES = ("Retrieval", "Generation", "Evaluation")
STRATEGIES = (
    "Language-agnostic",
    "Hybrid",
    "Translate-then-retrieve",
    "Retrieve-then-translate",
    "N/A",
)
RESOURCES = ("Mixed", "High", "Low", "N/A")
AUDIT_FIELDS = (
    "scope_label",
    "transfer_point",
    "translation_strategy",
    "resource_level",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def stages_of(row: dict[str, str]) -> set[str]:
    return {stage.strip() for stage in row["transfer_point"].split("|") if stage.strip()}


def stage_combination(row: dict[str, str]) -> str:
    """Return the stage set of a row in canonical R/G/E order, e.g. ``R+G+E``."""
    present = stages_of(row)
    return "+".join(stage[0] for stage in STAGES if stage in present)


def sorted_counts(counter: Counter) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def tpx_profile(rows: list[dict[str, str]]) -> dict:
    return {
        "n": len(rows),
        "stages": {
            stage: sum(1 for row in rows if stage in stages_of(row)) for stage in STAGES
        },
        "stage_combinations": sorted_counts(
            Counter(stage_combination(row) for row in rows)
        ),
        "strategy": {
            label: sum(1 for row in rows if row["translation_strategy"] == label)
            for label in STRATEGIES
        },
        "resource": {
            label: sum(1 for row in rows if row["resource_level"] == label)
            for label in RESOURCES
        },
    }


def compute_counts(corpus_dir: Path = CORPUS_DIR) -> dict:
    papers = read_csv(corpus_dir / "papers.csv")
    decisions = {
        row["paper_id"]: row for row in read_csv(corpus_dir / "scope_decisions.csv")
    }
    core = [row for row in papers if row["scope_label"] == "Core"]
    adjacent = [row for row in papers if row["scope_label"] == "Adjacent"]

    core_profile = tpx_profile(core)
    core_domains = sorted_counts(Counter(row["domain"] for row in core))
    specialized = {
        domain: count for domain, count in core_domains.items() if domain != "Open"
    }
    core_profile["domain"] = core_domains
    core_profile["domain_open"] = core_domains.get("Open", 0)
    core_profile["domain_specialized_total"] = sum(specialized.values())
    core_profile["domain_specialized"] = specialized

    medium_core = [
        row["id"] for row in core if decisions[row["id"]]["confidence"] == "medium"
    ]
    sensitivity = tpx_profile([row for row in core if row["id"] not in medium_core])
    sensitivity["medium_confidence_core"] = medium_core
    sensitivity["medium_confidence_core_count"] = len(medium_core)

    candidates = read_csv(corpus_dir / "coverage_check_candidates.csv")
    followup = read_csv(corpus_dir / "targeted_followup.csv")
    reconciliation = read_csv(
        corpus_dir / "second_annotator" / "audit_disagreements_for_reconciliation.csv"
    )

    audit_fields = {}
    for field in AUDIT_FIELDS:
        rows = [row for row in reconciliation if row["field"] == field]
        audit_fields[field] = {
            "disagreements": len(rows),
            "resolved_to_initial": sum(
                1 for row in rows if row["adjudication_decision"] == "keep_current"
            ),
            "resolved_to_audit": sum(
                1 for row in rows if row["adjudication_decision"] == "accept_audit"
            ),
        }

    return {
        "evidence_base": len(papers),
        "scope": {
            scope: sum(1 for row in papers if row["scope_label"] == scope)
            for scope in SCOPES
        },
        "core": core_profile,
        "core_plus_adjacent": {
            "n": len(core) + len(adjacent),
            "domain": sorted_counts(Counter(row["domain"] for row in core + adjacent)),
        },
        "sensitivity": sensitivity,
        "coverage_update_june5": {
            "candidates": len(candidates),
            "integrated": sum(
                1 for row in candidates if row["decision"].startswith("new_")
            ),
            "excluded": sum(1 for row in candidates if row["decision"] == "exclude"),
            "decisions": dict(sorted(Counter(row["decision"] for row in candidates).items())),
        },
        "targeted_followup_june8": {
            "assessed": len(followup),
            "integrated": sum(1 for row in followup if row["decision"] == "Core"),
            "unresolved": sum(
                1 for row in followup if row["decision"] == "not_integrated"
            ),
        },
        "reliability_audit": {
            "fields": audit_fields,
            "disagreements": sum(v["disagreements"] for v in audit_fields.values()),
            "resolved_to_initial": sum(
                v["resolved_to_initial"] for v in audit_fields.values()
            ),
            "resolved_to_audit": sum(
                v["resolved_to_audit"] for v in audit_fields.values()
            ),
            "papers_with_disagreements": len(
                {row["paper_id"] for row in reconciliation}
            ),
        },
    }


def join_counts(mapping: dict[str, int]) -> str:
    return ", ".join(f"{label} {count}" for label, count in mapping.items())


def print_report(counts: dict) -> None:
    core = counts["core"]
    print(f"Evidence base: {counts['evidence_base']} papers")
    print("Scope: " + join_counts(counts["scope"]))
    print(f"Core (n={core['n']})")
    print("  Transfer points: " + join_counts(core["stages"]))
    print("  Stage combinations: " + join_counts(core["stage_combinations"]))
    print("  Strategies: " + join_counts(core["strategy"]))
    print("  Resource levels: " + join_counts(core["resource"]))
    print(
        f"  Domain: Open {core['domain_open']} vs specialized "
        f"{core['domain_specialized_total']} ({join_counts(core['domain_specialized'])})"
    )
    plus = counts["core_plus_adjacent"]
    print(f"Core+Adjacent (n={plus['n']}) domain profile: " + join_counts(plus["domain"]))
    sensitivity = counts["sensitivity"]
    print(
        f"Sensitivity: removing {sensitivity['medium_confidence_core_count']} "
        f"medium-confidence Core records ({', '.join(sensitivity['medium_confidence_core'])}) "
        f"leaves n={sensitivity['n']}: " + join_counts(sensitivity["stages"])
    )
    june5 = counts["coverage_update_june5"]
    print(
        f"June 5 coverage update: {june5['candidates']} candidates, "
        f"{june5['integrated']} integrated, {june5['excluded']} excluded "
        f"({join_counts(june5['decisions'])})"
    )
    june8 = counts["targeted_followup_june8"]
    print(
        f"June 8 targeted follow-up: {june8['assessed']} assessed, "
        f"{june8['integrated']} integrated, {june8['unresolved']} unresolved"
    )
    audit = counts["reliability_audit"]
    print(
        f"Reliability audit: {audit['disagreements']} disagreements across "
        f"{audit['papers_with_disagreements']} papers; {audit['resolved_to_initial']} "
        f"resolved to the initial label, {audit['resolved_to_audit']} to the audit label"
    )
    for field, values in audit["fields"].items():
        print(
            f"  {field}: {values['disagreements']} disagreements, "
            f"{values['resolved_to_initial']} initial, {values['resolved_to_audit']} audit"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate every descriptive count reported in the TPx paper."
    )
    parser.add_argument("--corpus-dir", type=Path, default=CORPUS_DIR)
    parser.add_argument(
        "--json", action="store_true", help="print the counts as JSON instead of a report"
    )
    args = parser.parse_args()
    counts = compute_counts(args.corpus_dir)
    if args.json:
        print(json.dumps(counts, indent=2))
    else:
        print_report(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

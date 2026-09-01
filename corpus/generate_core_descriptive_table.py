from __future__ import annotations

import csv
from pathlib import Path


CORPUS_DIR = Path(__file__).resolve().parent
PAPERS_PATH = CORPUS_DIR / "papers.csv"
DECISIONS_PATH = CORPUS_DIR / "scope_decisions.csv"
CSV_OUTPUT = CORPUS_DIR / "core_papers_descriptive_table.csv"
MARKDOWN_OUTPUT = CORPUS_DIR / "core_papers_descriptive_table.md"
EXPECTED_CORE_COUNT = 42

CSV_FIELDS = [
    "id",
    "title",
    "authors",
    "year",
    "venue",
    "url",
    "transfer_point",
    "translation_strategy",
    "resource_level",
    "domain",
    "citation_key",
    "scope_confidence",
    "scope_rationale",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def main() -> None:
    papers = read_csv(PAPERS_PATH)
    decisions = {
        row["paper_id"]: row for row in read_csv(DECISIONS_PATH)
    }
    core_papers = [row for row in papers if row["scope_label"] == "Core"]

    if len(core_papers) != EXPECTED_CORE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_CORE_COUNT} Core papers, found {len(core_papers)}"
        )

    rows = []
    for paper in core_papers:
        decision = decisions.get(paper["id"])
        if decision is None:
            raise ValueError(f"Missing scope decision for {paper['id']}")
        rows.append(
            {
                **{field: paper.get(field, "") for field in CSV_FIELDS},
                "scope_confidence": decision["confidence"],
                "scope_rationale": decision["decision_basis"],
            }
        )

    with CSV_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Descriptive Table of the 42 Core Papers",
        "",
        "This publication-facing table is generated from `papers.csv` and "
        "`scope_decisions.csv`. It reports bibliographic metadata and the "
        "predefined TPx coding dimensions without adding performance rankings "
        "or inferred labels.",
        "",
        "| ID | Paper | Year / venue | Transfer point | Strategy | Resource | Domain | Scope rationale |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        title = markdown_escape(row["title"])
        paper_link = f"[{title}]({row['url']})"
        rationale = markdown_escape(row["scope_rationale"])
        lines.append(
            "| {id} | {paper} | {year} / {venue} | {transfer} | {strategy} | "
            "{resource} | {domain} | {rationale} ({confidence}) |".format(
                id=row["id"],
                paper=paper_link,
                year=markdown_escape(row["year"]),
                venue=markdown_escape(row["venue"]),
                transfer=markdown_escape(row["transfer_point"]),
                strategy=markdown_escape(row["translation_strategy"]),
                resource=markdown_escape(row["resource_level"]),
                domain=markdown_escape(row["domain"]),
                rationale=rationale,
                confidence=markdown_escape(row["scope_confidence"]),
            )
        )

    MARKDOWN_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {len(rows)} Core rows.")


if __name__ == "__main__":
    main()

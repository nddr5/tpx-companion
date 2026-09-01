from __future__ import annotations

import argparse
import csv
import os
import tempfile
from collections import Counter
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "tpx_mpl_config")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
STAGES = ["Retrieval", "Generation", "Evaluation"]
SCOPES = ["Core", "Adjacent", "Component", "Background"]
STRATEGIES = [
    "Translate-then-retrieve",
    "Retrieve-then-translate",
    "Language-agnostic",
    "Hybrid",
]
DOMAINS = [
    "Open",
    "General",
    "Medical",
    "Legal",
    "Cultural",
    "News",
    "Agriculture",
    "Enterprise",
    "Climate",
    "Religious",
    "Education",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def years(rows: list[dict[str, str]]) -> list[int]:
    return list(
        range(
            min(int(row["year"]) for row in rows),
            max(int(row["year"]) for row in rows) + 1,
        )
    )


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 150,
            "savefig.bbox": "tight",
        }
    )


def save_scope_distribution(rows: list[dict[str, str]], out_dir: Path) -> None:
    counts = Counter(row["scope_label"] for row in rows)
    colors = ["#1d4ed8", "#0f766e", "#64748b", "#a8a29e"]
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    bars = ax.bar(SCOPES, [counts[scope] for scope in SCOPES], color=colors)
    ax.bar_label(bars, padding=3)
    ax.set_ylabel("Papers")
    ax.set_title("Role of papers in the TPx evidence base")
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(out_dir / "fig_scope_distribution.pdf")
    plt.close(fig)


def save_year_distribution(rows: list[dict[str, str]], out_dir: Path) -> None:
    year_values = years(rows)
    scopes = ["Core", "Adjacent"]
    values = {
        scope: [
            sum(
                row["scope_label"] == scope and int(row["year"]) == year
                for row in rows
            )
            for year in year_values
        ]
        for scope in scopes
    }
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    bottom = [0] * len(year_values)
    colors = {"Core": "#1d4ed8", "Adjacent": "#0f766e"}
    for scope in scopes:
        ax.bar(
            year_values,
            values[scope],
            bottom=bottom,
            label=scope,
            color=colors[scope],
            width=0.65,
        )
        bottom = [old + new for old, new in zip(bottom, values[scope])]
    ax.set_xlabel("Year")
    ax.set_ylabel("Papers")
    ax.set_title("Publication years of Core and Adjacent RAG studies")
    ax.set_xticks(year_values)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncols=2, loc="upper left")
    fig.savefig(out_dir / "fig_year_distribution.pdf")
    plt.close(fig)


def save_tpx_profile(rows: list[dict[str, str]], out_dir: Path) -> None:
    stage_counts = Counter(
        stage for row in rows for stage in row["transfer_point"].split("|")
    )
    strategy_counts = Counter(row["translation_strategy"] for row in rows)
    resource_counts = Counter(row["resource_level"] for row in rows)

    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.9))
    stage_bars = axes[0].bar(
        STAGES,
        [stage_counts[stage] for stage in STAGES],
        color=["#2563eb", "#059669", "#dc2626"],
    )
    axes[0].bar_label(stage_bars, padding=2)
    axes[0].set_title("Transfer points")
    axes[0].tick_params(axis="x", rotation=25)

    strategy_labels = ["T-then-R", "R-then-T", "Lang.-agnostic", "Hybrid", "N/A"]
    strategy_keys = STRATEGIES + ["N/A"]
    strategy_bars = axes[1].bar(
        strategy_labels,
        [strategy_counts[key] for key in strategy_keys],
        color="#7c3aed",
    )
    axes[1].bar_label(strategy_bars, padding=2)
    axes[1].set_title("Strategies")
    axes[1].tick_params(axis="x", rotation=35)

    resource_keys = ["High", "Low", "Mixed", "N/A"]
    resource_bars = axes[2].bar(
        resource_keys,
        [resource_counts[key] for key in resource_keys],
        color="#d97706",
    )
    axes[2].bar_label(resource_bars, padding=2)
    axes[2].set_title("Resource settings")

    for ax in axes:
        ax.set_ylabel("Core papers")
        ax.grid(axis="y", alpha=0.25)
    fig.savefig(out_dir / "fig_tpx_profile.pdf")
    plt.close(fig)


def save_domain_profile(
    core_rows: list[dict[str, str]],
    rag_rows: list[dict[str, str]],
    out_dir: Path,
) -> None:
    core_counts = Counter(row["domain"] for row in core_rows)
    rag_counts = Counter(row["domain"] for row in rag_rows)
    ordered_domains = [domain for domain in DOMAINS if rag_counts[domain]]
    ordered_domains.extend(
        sorted(domain for domain in rag_counts if domain not in DOMAINS)
    )
    positions = list(range(len(ordered_domains)))
    height = 0.38
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    core_values = [core_counts[domain] for domain in ordered_domains]
    rag_values = [rag_counts[domain] for domain in ordered_domains]
    core_bars = ax.barh(
        [position - height / 2 for position in positions],
        core_values,
        height=height,
        label="Core",
        color="#1d4ed8",
    )
    rag_bars = ax.barh(
        [position + height / 2 for position in positions],
        rag_values,
        height=height,
        label="Core+Adjacent",
        color="#0f766e",
    )
    ax.bar_label(
        core_bars,
        labels=[str(value) if value else "" for value in core_values],
        padding=2,
    )
    ax.bar_label(
        rag_bars,
        labels=[str(value) if value else "" for value in rag_values],
        padding=2,
    )
    ax.set_title("Domain sensitivity by scope boundary")
    ax.set_xlabel("Papers")
    ax.set_yticks(positions, ordered_domains)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.25)
    ax.legend(frameon=False, ncols=2, loc="lower right")
    fig.savefig(out_dir / "fig_domain_profile.pdf")
    plt.close(fig)


def summarize(all_rows: list[dict[str, str]], core_rows: list[dict[str, str]]) -> None:
    stage_counts = Counter()
    strategy_counts = Counter()
    resource_counts = Counter()
    domain_counts = Counter()

    for row in core_rows:
        stages = row["transfer_point"].split("|")
        strategy = row["translation_strategy"]
        for stage in stages:
            stage_counts[stage] += 1
        strategy_counts[strategy] += 1
        resource_counts[row["resource_level"]] += 1
        domain_counts[row["domain"]] += 1

    print(f"evidence_base={len(all_rows)}")
    print("scope_counts=" + repr(dict(Counter(row["scope_label"] for row in all_rows))))
    print(f"core_papers={len(core_rows)}")
    print("core_stage_counts=" + repr(dict(stage_counts)))
    print("core_strategy_counts=" + repr(dict(strategy_counts)))
    print("core_resource_counts=" + repr(dict(resource_counts)))
    print("core_domain_counts=" + repr(dict(domain_counts)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=SCRIPT_DIR / "papers.csv")
    parser.add_argument("--out-dir", type=Path, default=SCRIPT_DIR.parent / "figures")
    args = parser.parse_args()

    rows = read_rows(args.csv)
    core_rows = [row for row in rows if row["scope_label"] == "Core"]
    rag_rows = [
        row for row in rows if row["scope_label"] in {"Core", "Adjacent"}
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    setup_style()
    save_scope_distribution(rows, args.out_dir)
    save_year_distribution(rag_rows, args.out_dir)
    save_tpx_profile(core_rows, args.out_dir)
    save_domain_profile(core_rows, rag_rows, args.out_dir)
    summarize(rows, core_rows)


if __name__ == "__main__":
    main()

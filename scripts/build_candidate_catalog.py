#!/usr/bin/env python3
"""Build final official-source candidate catalog and summary outputs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TARGET_RESOURCE_TYPES = ("Patient", "Observation", "Condition")
CATALOG_FIELDS = [
    "candidate_id",
    "resource_type",
    "resource_id",
    "source_file_or_example_name",
    "json_valid",
    "likely_numeric",
    "has_value",
    "has_unit",
    "needs_linked_context",
    "complexity_guess",
    "good_for_pairing",
    "review_notes",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profiles-path",
        type=Path,
        default=root / "data" / "processed" / "official_candidate_profiles.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "official",
    )
    return parser.parse_args()


def load_profiles(path: Path) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                profiles.append(json.loads(line))
    return sorted(
        profiles,
        key=lambda row: (
            TARGET_RESOURCE_TYPES.index(row["resource_type"]),
            row["source_file_or_example_name"],
            row["resource_id"],
        ),
    )


def add_candidate_ids(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counters = defaultdict(int)
    catalog_rows: list[dict[str, Any]] = []
    for row in profiles:
        resource_type = row["resource_type"]
        counters[resource_type] += 1
        candidate_id = f"official-{resource_type.lower()}-{counters[resource_type]:04d}"
        catalog_row = {"candidate_id": candidate_id}
        for field in CATALOG_FIELDS[1:]:
            catalog_row[field] = row.get(field, "")
        catalog_rows.append(catalog_row)
    return catalog_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resource_counts_rows(catalog_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for resource_type in TARGET_RESOURCE_TYPES:
        subset = [row for row in catalog_rows if row["resource_type"] == resource_type]
        complexity_counts = Counter(row["complexity_guess"] for row in subset)
        rows.append(
            {
                "resource_type": resource_type,
                "total_candidates": len(subset),
                "json_valid": sum(row["json_valid"] == "true" for row in subset),
                "good_for_pairing": sum(row["good_for_pairing"] == "true" for row in subset),
                "needs_linked_context": sum(row["needs_linked_context"] == "true" for row in subset),
                "low_complexity": complexity_counts.get("low", 0),
                "medium_complexity": complexity_counts.get("medium", 0),
                "high_complexity": complexity_counts.get("high", 0),
            }
        )
    return rows


def observation_summary_rows(catalog_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    observations = [row for row in catalog_rows if row["resource_type"] == "Observation"]
    metrics = [
        ("total_observations", len(observations)),
        ("json_valid", sum(row["json_valid"] == "true" for row in observations)),
        ("likely_numeric_true", sum(row["likely_numeric"] == "true" for row in observations)),
        ("has_value_true", sum(row["has_value"] == "true" for row in observations)),
        ("has_unit_true", sum(row["has_unit"] == "true" for row in observations)),
        (
            "numeric_with_value_and_unit",
            sum(
                row["likely_numeric"] == "true"
                and row["has_value"] == "true"
                and row["has_unit"] == "true"
                for row in observations
            ),
        ),
        ("needs_linked_context_true", sum(row["needs_linked_context"] == "true" for row in observations)),
        ("low_complexity", sum(row["complexity_guess"] == "low" for row in observations)),
        ("medium_complexity", sum(row["complexity_guess"] == "medium" for row in observations)),
        ("high_complexity", sum(row["complexity_guess"] == "high" for row in observations)),
        ("good_for_pairing_true", sum(row["good_for_pairing"] == "true" for row in observations)),
    ]
    return [{"metric": metric, "count": count} for metric, count in metrics]


def pilot_shortlist_size(catalog_rows: list[dict[str, Any]]) -> int:
    good_total = sum(row["good_for_pairing"] == "true" for row in catalog_rows)
    return min(12, good_total) if good_total else 0


def sufficiency_statement(catalog_rows: list[dict[str, Any]]) -> str:
    good_total = sum(row["good_for_pairing"] == "true" for row in catalog_rows)
    if good_total >= 12:
        return "Yes. The official pool is sufficient for a small pilot seed subset."
    if good_total >= 6:
        return "Yes, but only for a tightly scoped pilot seed subset."
    if good_total >= 1:
        return "Partially. The official pool is usable for a very small pilot, but the ready-to-curate subset is limited."
    return "Not yet. The current official pool does not expose enough clean candidates for a pilot shortlist."


def write_summary_markdown(path: Path, catalog_rows: list[dict[str, Any]]) -> None:
    counts = {resource_type: 0 for resource_type in TARGET_RESOURCE_TYPES}
    good_counts = {resource_type: 0 for resource_type in TARGET_RESOURCE_TYPES}
    for row in catalog_rows:
        counts[row["resource_type"]] += 1
        if row["good_for_pairing"] == "true":
            good_counts[row["resource_type"]] += 1

    shortlist_size = pilot_shortlist_size(catalog_rows)
    sufficient_text = sufficiency_statement(catalog_rows)
    output_anchor_text = (
        "Yes. The official example pool is better suited as a high-quality output-anchor set than as a large-scale training backbone."
    )

    lines = [
        "# Official Source Summary",
        "",
        "## Direct answers",
        "",
        f"- Official Patient examples available: {counts['Patient']}",
        f"- Official Observation examples available: {counts['Observation']}",
        f"- Official Condition examples available: {counts['Condition']}",
        f"- Is the official pool sufficient for a pilot seed subset? {sufficient_text}",
        f"- Is the official pool better suited as a high-quality output-anchor set rather than a large-scale training backbone? {output_anchor_text}",
        f"- Recommended next pilot seed shortlist size: {shortlist_size}",
        "",
        "## Pairing readiness snapshot",
        "",
        f"- Good-for-pairing Patient candidates: {good_counts['Patient']}",
        f"- Good-for-pairing Observation candidates: {good_counts['Observation']}",
        f"- Good-for-pairing Condition candidates: {good_counts['Condition']}",
        "",
        "## Interpretation",
        "",
        "- The official corpus is useful for standards-anchored, semantically clean examples.",
        "- The pool should be treated as a quality-focused curation source, not as a high-volume training backbone.",
        "- Later shortlist selection should prefer self-contained, low-complexity examples with clear clinical meaning.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    profiles = load_profiles(args.profiles_path)
    catalog_rows = add_candidate_ids(profiles)

    write_csv(args.output_dir / "candidate_seed_catalog.csv", CATALOG_FIELDS, catalog_rows)
    write_csv(
        args.output_dir / "resource_counts_summary.csv",
        [
            "resource_type",
            "total_candidates",
            "json_valid",
            "good_for_pairing",
            "needs_linked_context",
            "low_complexity",
            "medium_complexity",
            "high_complexity",
        ],
        resource_counts_rows(catalog_rows),
    )
    write_csv(
        args.output_dir / "observation_profile_summary.csv",
        ["metric", "count"],
        observation_summary_rows(catalog_rows),
    )
    write_summary_markdown(args.output_dir / "official_source_summary.md", catalog_rows)

    print(f"Built catalog with {len(catalog_rows)} candidates")
    print(f"Outputs written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

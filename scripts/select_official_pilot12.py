#!/usr/bin/env python3
"""Select the first-pass Official-derived pilot seed shortlist of 12 examples."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SELECTED_FIELDS = [
    "selected_id",
    "resource_type",
    "resource_id",
    "source_file_or_example_name",
    "json_valid",
    "likely_numeric",
    "has_value",
    "has_unit",
    "needs_linked_context",
    "complexity_guess",
    "selection_priority",
    "selection_notes",
]

SELECTED_CANDIDATES = [
    {
        "source_file_or_example_name": "patient-example-ihe-pcd.json",
        "selection_priority": "strict-preferred",
        "selection_notes": "Low-complexity self-contained Patient example with clear identity fields and no linked-resource dependency.",
    },
    {
        "source_file_or_example_name": "patient-example-proband.json",
        "selection_priority": "strict-preferred",
        "selection_notes": "Low-complexity self-contained Patient example that broadens the pilot with a genetics-oriented but still clean standalone record.",
    },
    {
        "source_file_or_example_name": "patient-example-newborn.json",
        "selection_priority": "strict-preferred",
        "selection_notes": "Self-contained neonatal Patient example retained for age-range diversity despite thinner demographics than the adult examples.",
    },
    {
        "source_file_or_example_name": "observation-example-body-height.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Canonical numeric body measurement with direct value and unit; accepted with light subject-only context.",
    },
    {
        "source_file_or_example_name": "observation-example-body-temperature.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Canonical temperature Observation with direct numeric value and explicit unit; strong target-side gold anchor.",
    },
    {
        "source_file_or_example_name": "observation-example-heart-rate.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Canonical vital-sign Observation with unambiguous code, direct value, and unit; only light subject context.",
    },
    {
        "source_file_or_example_name": "observation-example-respiratory-rate.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Canonical vital-sign Observation with direct numeric value and unit; complements heart-rate and temperature anchors.",
    },
    {
        "source_file_or_example_name": "observation-example-mbp.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Clear hemodynamic Observation with direct numeric value and unit; chosen to diversify the vital-sign subset.",
    },
    {
        "source_file_or_example_name": "observation-example-f001-glucose.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Clean lab Observation with standard chemistry semantics and explicit units; kept to add non-vital measurement coverage.",
    },
    {
        "source_file_or_example_name": "condition-example-stroke.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Clear confirmed diagnosis example with straightforward Condition structure and only light subject linkage.",
    },
    {
        "source_file_or_example_name": "condition-example.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Simple acute Condition example with explicit diagnosis coding; suitable as a compact diagnosis anchor.",
    },
    {
        "source_file_or_example_name": "condition-example2.json",
        "selection_priority": "relaxed-light-context",
        "selection_notes": "Simple chronic Condition example centered on Asthma; retained for diagnosis-type diversity in the pilot set.",
    },
]

REJECTED_SAMPLE = [
    {
        "source_file_or_example_name": "patient-example-animal.json",
        "rejection_reason": "Semantically strong but veterinary-specific, so it was not as representative for a general human pilot anchor set.",
    },
    {
        "source_file_or_example_name": "patient-example-c.json",
        "rejection_reason": "Acceptable candidate, but it depended on linked organization context and lost to the fully self-contained Patient selections.",
    },
    {
        "source_file_or_example_name": "observation-example-bmi.json",
        "rejection_reason": "Strong candidate, but omitted to avoid over-concentrating the six-slot Observation set on overlapping body-measure examples.",
    },
    {
        "source_file_or_example_name": "observation-example-f204-creatinine.json",
        "rejection_reason": "Good numeric lab example, but glucose was preferred as the single pilot lab anchor because it is more universally familiar.",
    },
    {
        "source_file_or_example_name": "observation-example-spirometry.json",
        "rejection_reason": "Clean numeric Observation, but the device-oriented coding and patient-as-performer pattern made it less general-purpose for a first pilot.",
    },
    {
        "source_file_or_example_name": "condition-example-family-history.json",
        "rejection_reason": "Low complexity, but less ideal as a direct Condition gold anchor because the semantics skew toward family-history context.",
    },
    {
        "source_file_or_example_name": "condition-example-f205-infection.json",
        "rejection_reason": "Not selected because differential-status semantics and extra asserter linkage make it more context-dependent than the chosen Conditions.",
    },
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog-path",
        type=Path,
        default=root / "outputs" / "official" / "candidate_seed_catalog.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "official",
    )
    return parser.parse_args()


def load_catalog(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def strict_preferred_criteria_met(row: dict[str, str]) -> bool:
    if row["json_valid"] != "true" or row["complexity_guess"] not in {"low", "medium"}:
        return False
    if row["resource_type"] == "Observation":
        return (
            row["needs_linked_context"] == "false"
            and row["likely_numeric"] == "true"
            and row["has_value"] == "true"
            and row["has_unit"] == "true"
        )
    return row["needs_linked_context"] == "false"


def selected_rows(catalog_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_source = {row["source_file_or_example_name"]: row for row in catalog_rows}
    selected: list[dict[str, str]] = []

    for index, item in enumerate(SELECTED_CANDIDATES, start=1):
        source_name = item["source_file_or_example_name"]
        if source_name not in by_source:
            raise KeyError(f"Missing candidate in catalog: {source_name}")
        row = by_source[source_name]
        if row["good_for_pairing"] != "true":
            raise ValueError(f"Selected candidate is not marked good_for_pairing=true: {source_name}")
        selected.append(
            {
                "selected_id": f"official-pilot12-{index:02d}",
                "resource_type": row["resource_type"],
                "resource_id": row["resource_id"],
                "source_file_or_example_name": row["source_file_or_example_name"],
                "json_valid": row["json_valid"],
                "likely_numeric": row["likely_numeric"],
                "has_value": row["has_value"],
                "has_unit": row["has_unit"],
                "needs_linked_context": row["needs_linked_context"],
                "complexity_guess": row["complexity_guess"],
                "selection_priority": item["selection_priority"],
                "selection_notes": item["selection_notes"],
            }
        )

    counts = Counter(row["resource_type"] for row in selected)
    expected_counts = {"Patient": 3, "Observation": 6, "Condition": 3}
    if counts != expected_counts:
        raise ValueError(f"Selected counts do not match target allocation: {counts}")

    if len(selected) != 12:
        raise ValueError(f"Expected exactly 12 selections, found {len(selected)}")

    return selected


def rejected_rows(catalog_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_source = {row["source_file_or_example_name"]: row for row in catalog_rows}
    rows: list[dict[str, str]] = []
    for item in REJECTED_SAMPLE:
        source_name = item["source_file_or_example_name"]
        if source_name not in by_source:
            raise KeyError(f"Missing rejected example in catalog: {source_name}")
        catalog_row = by_source[source_name]
        rows.append(
            {
                "resource_type": catalog_row["resource_type"],
                "resource_id": catalog_row["resource_id"],
                "rejection_reason": item["rejection_reason"],
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True))
            handle.write("\n")


def write_summary(path: Path, selected: list[dict[str, str]]) -> None:
    counts = Counter(row["resource_type"] for row in selected)
    strict_rows = [row for row in selected if strict_preferred_criteria_met(row)]
    relaxed_rows = [row for row in selected if not strict_preferred_criteria_met(row)]

    lines = [
        "# Official Pilot 12 Summary",
        "",
        "## Final counts by resource type",
        "",
        f"- Patient: {counts['Patient']}",
        f"- Observation: {counts['Observation']}",
        f"- Condition: {counts['Condition']}",
        "",
        "## Strict preferred criteria coverage",
        "",
        f"- Selections meeting the strict preferred criteria exactly as written: {len(strict_rows)} of {len(selected)}",
        f"- Strict Patient selections: {sum(row['resource_type'] == 'Patient' for row in strict_rows)}",
        f"- Strict Observation selections: {sum(row['resource_type'] == 'Observation' for row in strict_rows)}",
        f"- Strict Condition selections: {sum(row['resource_type'] == 'Condition' for row in strict_rows)}",
        "",
        "## Criteria relaxations used",
        "",
        "- Nine selections required one explicit relaxation: accepting light linked context only.",
        "- This relaxation was necessary because the official Observation and Condition pools are dominated by subject and performer style references.",
        "- No selected seed relaxed away from `good_for_pairing = true`.",
        "- No selected seed relaxed away from low-or-medium complexity.",
        "- All selected Observations still satisfy `likely_numeric = true`, `has_value = true`, and `has_unit = true`.",
        "",
        "## Why these 12 work as Official-derived pilot anchors",
        "",
        "- The Patient subset is intentionally self-contained and gives the pilot a stable demographic anchor without importing graph-heavy context.",
        "- The Observation subset concentrates on common, numerically explicit measurements with clear units and straightforward target-side semantics.",
        "- The Condition subset favors simple diagnosis anchors over more ambiguous or heavily contextual examples.",
        "- Together, the set stays small, review-ready, and standards-aligned while remaining conservative about ambiguity and dependency.",
        "",
        "## Selected shortlist",
        "",
    ]

    for resource_type in ("Patient", "Observation", "Condition"):
        lines.append(f"### {resource_type}")
        lines.append("")
        for row in selected:
            if row["resource_type"] == resource_type:
                lines.append(
                    f"- `{row['selected_id']}` `{row['resource_id']}` from `{row['source_file_or_example_name']}`: {row['selection_notes']}"
                )
        lines.append("")

    if relaxed_rows:
        lines.extend(
            [
                "## Relaxed selections",
                "",
            ]
        )
        for row in relaxed_rows:
            lines.append(
                f"- `{row['selected_id']}` `{row['resource_type']}` `{row['resource_id']}`: accepted with light linked context only."
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    catalog_rows = load_catalog(args.catalog_path)
    selected = selected_rows(catalog_rows)
    rejected = rejected_rows(catalog_rows)

    write_csv(args.output_dir / "official_pilot12_selected.csv", SELECTED_FIELDS, selected)
    write_jsonl(args.output_dir / "official_pilot12_selected.jsonl", selected)
    write_summary(args.output_dir / "official_pilot12_summary.md", selected)
    write_csv(
        args.output_dir / "official_pilot12_rejected_examples.csv",
        ["resource_type", "resource_id", "rejection_reason"],
        rejected,
    )

    print(f"Selected {len(selected)} official pilot seeds")
    print(f"Outputs written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

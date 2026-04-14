#!/usr/bin/env python3
"""Generate a small Official-derived pairing pilot from the selected 12 seeds."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PAIR_FIELDS = [
    "pair_id",
    "case_id",
    "seed_id",
    "resource_type",
    "input_style",
    "input_text",
    "target_seed_file",
    "unsupported_fact_added",
    "missingness_preserved",
    "review_status",
    "notes",
]

PAIR_SPECS = {
    "official-pilot12-01": [
        {
            "input_style": "concise_clinical",
            "input_text": "Active patient record for ALBERT BROOKS with identifier AB60001.",
            "notes": "Seed is sparse; only explicit identity fields were used.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Patient name: ALBERT BROOKS | Identifier: AB60001 | Active: true",
            "notes": "Seed is sparse; no gender or birth date was stated in the seed.",
        },
    ],
    "official-pilot12-02": [
        {
            "input_style": "concise_clinical",
            "input_text": "Active female patient born 1966-04-04 with identifier 999999999.",
            "notes": "No patient name is present in the seed, so the variant is limited to explicit demographics and identifier.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Patient record | Gender: female | Birth date: 1966-04-04 | Identifier: 999999999 | Active: true",
            "notes": "No patient name is present in the seed, so the variant remains demographic-only.",
        },
    ],
    "official-pilot12-03": [
        {
            "input_style": "concise_clinical",
            "input_text": "Male patient with birth date 2017-09-05.",
            "notes": "Very sparse seed; no name, identifier, or active status was stated in the resource.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Patient record | Gender: male | Birth date: 2017-09-05",
            "notes": "Very sparse seed; semi-structured variant stays close to the concise variant to preserve missingness.",
        },
    ],
    "official-pilot12-04": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final body height observation: 66.89999999999999 in.",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Body height | Status: final | Value: 66.89999999999999 in | Effective date: 1999-07-02",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
    ],
    "official-pilot12-05": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final body temperature: 36.5 C.",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Body temperature | Status: final | Value: 36.5 C | Effective date: 1999-07-02",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
    ],
    "official-pilot12-06": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final heart rate: 44 beats/minute.",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Heart rate | Status: final | Value: 44 beats/minute | Effective date: 1999-07-02",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
    ],
    "official-pilot12-07": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final respiratory rate: 26 breaths/minute.",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Respiratory rate | Status: final | Value: 26 breaths/minute | Effective date: 1999-07-02",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
    ],
    "official-pilot12-08": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final mean blood pressure: 80 mm[Hg].",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Mean blood pressure | Status: final | Value: 80 mm[Hg] | Effective date: 1999-07-02",
            "notes": "Only seed-local observation facts were used; linked subject context was intentionally omitted.",
        },
    ],
    "official-pilot12-09": [
        {
            "input_style": "concise_clinical",
            "input_text": "Final blood glucose observation: 6.3 mmol/l.",
            "notes": "Linked subject and performer references were intentionally omitted.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Observation: Glucose [Moles/volume] in Blood | Status: final | Value: 6.3 mmol/l | Effective start: 2013-04-02T09:30:10+01:00",
            "notes": "Linked subject and performer references were intentionally omitted.",
        },
    ],
    "official-pilot12-10": [
        {
            "input_style": "concise_clinical",
            "input_text": "Active confirmed ischemic stroke.",
            "notes": "Subject reference was intentionally omitted; concise variant keeps only the core diagnosis and certainty facts.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Condition: Ischemic stroke (disorder) | Clinical status: active | Verification status: confirmed | Onset date: 2010-07-18",
            "notes": "Subject reference was intentionally omitted.",
        },
    ],
    "official-pilot12-11": [
        {
            "input_style": "concise_clinical",
            "input_text": "Active confirmed burn of ear involving the left external ear structure.",
            "notes": "Subject reference was intentionally omitted; body site was kept because it is explicit in the seed.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Condition: Burn of ear | Body site: Left external ear structure | Clinical status: active | Verification status: confirmed | Onset date: 2012-05-24",
            "notes": "Subject reference was intentionally omitted.",
        },
    ],
    "official-pilot12-12": [
        {
            "input_style": "concise_clinical",
            "input_text": "Active confirmed asthma.",
            "notes": "Seed is compact; no onset date or treatment detail was stated in the resource.",
        },
        {
            "input_style": "semi_structured",
            "input_text": "Condition: Asthma | Clinical status: active | Verification status: confirmed",
            "notes": "Seed is compact; no onset date or treatment detail was stated in the resource.",
        },
    ],
}

FLAG_SPECS = [
    {
        "seed_id": "official-pilot12-02",
        "input_style": "semi_structured",
        "flag_type": "sparse_seed",
        "flag_reason": "The proband seed has no patient name, so the variant is necessarily limited to gender, birth date, identifier, and active status.",
    },
    {
        "seed_id": "official-pilot12-03",
        "input_style": "semi_structured",
        "flag_type": "near_duplicate_variant",
        "flag_reason": "The newborn seed exposes only gender and birth date, so the two variants are intentionally close.",
    },
    {
        "seed_id": "official-pilot12-04",
        "input_style": "concise_clinical",
        "flag_type": "possible_hallucination",
        "flag_reason": "The floating-point height value is awkward; review first to ensure no downstream cleanup silently normalizes the number.",
    },
    {
        "seed_id": "official-pilot12-04",
        "input_style": "semi_structured",
        "flag_type": "style_uncertainty",
        "flag_reason": "The exact numeric precision is faithful to the seed but slightly unnatural to read, so this variant is worth an editorial check.",
    },
    {
        "seed_id": "official-pilot12-09",
        "input_style": "semi_structured",
        "flag_type": "context_leakage",
        "flag_reason": "The glucose seed includes linked subject and performer references; confirm the generated text does not imply extra linked-resource facts.",
    },
    {
        "seed_id": "official-pilot12-10",
        "input_style": "concise_clinical",
        "flag_type": "possible_omission",
        "flag_reason": "The concise stroke variant omits the explicit onset date even though the seed includes it.",
    },
]

ALLOWED_STYLES = {"concise_clinical", "semi_structured"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selected-path",
        type=Path,
        default=root / "outputs" / "official" / "official_pilot12_selected.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "official",
    )
    return parser.parse_args()


def load_selected(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def build_pairs(selected_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[tuple[str, str], str]]:
    by_seed = {row["selected_id"]: row for row in selected_rows}
    missing_specs = sorted(set(by_seed) - set(PAIR_SPECS))
    if missing_specs:
        raise KeyError(f"Missing pair specs for seeds: {missing_specs}")

    pairs: list[dict[str, str]] = []
    pair_index_lookup: dict[tuple[str, str], str] = {}

    pair_counter = 1
    for case_index, selected in enumerate(selected_rows, start=1):
        seed_id = selected["selected_id"]
        target_seed_file = str(Path("data/raw") / selected["resource_type"] / selected["source_file_or_example_name"])
        if not (repo_root() / target_seed_file).exists():
            raise FileNotFoundError(f"Missing target seed file: {target_seed_file}")

        specs = PAIR_SPECS[seed_id]
        if len(specs) != 2:
            raise ValueError(f"Expected exactly 2 variants for {seed_id}, found {len(specs)}")

        seen_styles: set[str] = set()
        for spec in specs:
            input_style = spec["input_style"]
            if input_style not in ALLOWED_STYLES:
                raise ValueError(f"Unexpected input style for {seed_id}: {input_style}")
            if input_style in seen_styles:
                raise ValueError(f"Duplicate style for {seed_id}: {input_style}")
            seen_styles.add(input_style)

            pair_id = f"official-pair-{pair_counter:03d}"
            pair_counter += 1
            pair_index_lookup[(seed_id, input_style)] = pair_id
            pairs.append(
                {
                    "pair_id": pair_id,
                    "case_id": f"official-case-{case_index:02d}",
                    "seed_id": seed_id,
                    "resource_type": selected["resource_type"],
                    "input_style": input_style,
                    "input_text": spec["input_text"],
                    "target_seed_file": target_seed_file,
                    "unsupported_fact_added": "false",
                    "missingness_preserved": "true",
                    "review_status": "ready_for_review",
                    "notes": spec["notes"],
                }
            )

    return pairs, pair_index_lookup


def validate_pairs(pairs: list[dict[str, str]]) -> None:
    if len(pairs) != 24:
        raise ValueError(f"Expected 24 candidate pairs, found {len(pairs)}")

    per_seed = Counter(pair["seed_id"] for pair in pairs)
    if any(count != 2 for count in per_seed.values()):
        raise ValueError(f"Each seed must have exactly 2 variants: {per_seed}")

    per_style = Counter(pair["input_style"] for pair in pairs)
    if per_style != Counter({"concise_clinical": 12, "semi_structured": 12}):
        raise ValueError(f"Unexpected style counts: {per_style}")

    for pair in pairs:
        input_text = pair["input_text"]
        if any(token in input_text for token in ("Patient/", "Practitioner/", "Encounter/", "Organization/", "Observation/")):
            raise ValueError(f"Possible context leakage in {pair['pair_id']}: {input_text}")

        if pair["resource_type"] == "Observation":
            if pair["unsupported_fact_added"] != "false" or pair["missingness_preserved"] != "true":
                raise ValueError(f"Unexpected review booleans for {pair['pair_id']}")
            if "Value:" in input_text or ":" not in input_text:
                pass
            if pair["seed_id"] == "official-pilot12-04" and "66.89999999999999" not in input_text:
                raise ValueError(f"Body-height value must be preserved exactly in {pair['pair_id']}")
            if pair["seed_id"] == "official-pilot12-05" and "36.5 C" not in input_text:
                raise ValueError(f"Body-temperature value missing in {pair['pair_id']}")
            if pair["seed_id"] == "official-pilot12-06" and "44 beats/minute" not in input_text:
                raise ValueError(f"Heart-rate value missing in {pair['pair_id']}")
            if pair["seed_id"] == "official-pilot12-07" and "26 breaths/minute" not in input_text:
                raise ValueError(f"Respiratory-rate value missing in {pair['pair_id']}")
            if pair["seed_id"] == "official-pilot12-08" and "80 mm[Hg]" not in input_text:
                raise ValueError(f"Mean blood pressure value missing in {pair['pair_id']}")
            if pair["seed_id"] == "official-pilot12-09" and "6.3 mmol/l" not in input_text:
                raise ValueError(f"Glucose value missing in {pair['pair_id']}")


def build_flags(pair_lookup: dict[tuple[str, str], str]) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    for spec in FLAG_SPECS:
        key = (spec["seed_id"], spec["input_style"])
        if key not in pair_lookup:
            raise KeyError(f"Flag refers to unknown pair: {key}")
        flags.append(
            {
                "pair_id": pair_lookup[key],
                "seed_id": spec["seed_id"],
                "resource_type": "",  # filled after lookup
                "flag_type": spec["flag_type"],
                "flag_reason": spec["flag_reason"],
            }
        )
    return flags


def attach_review_status(
    pairs: list[dict[str, str]],
    flags: list[dict[str, str]],
) -> None:
    resource_by_pair = {pair["pair_id"]: pair["resource_type"] for pair in pairs}
    flagged_pair_ids = {flag["pair_id"] for flag in flags}
    for flag in flags:
        flag["resource_type"] = resource_by_pair[flag["pair_id"]]
    for pair in pairs:
        if pair["pair_id"] in flagged_pair_ids:
            pair["review_status"] = "needs_manual_review"


def write_summary(path: Path, selected_rows: list[dict[str, str]], pairs: list[dict[str, str]], flags: list[dict[str, str]]) -> None:
    flagged_seed_ids = sorted({flag["seed_id"] for flag in flags})
    pairs_by_resource = Counter(pair["resource_type"] for pair in pairs)
    pairs_by_style = Counter(pair["input_style"] for pair in pairs)

    lines = [
        "# Official Pilot 12 Pair Generation Summary",
        "",
        f"- Total number of seeds processed: {len(selected_rows)}",
        f"- Total number of candidate pairs generated: {len(pairs)}",
        "",
        "## Variants per resource type",
        "",
        f"- Patient: {pairs_by_resource['Patient']}",
        f"- Observation: {pairs_by_resource['Observation']}",
        f"- Condition: {pairs_by_resource['Condition']}",
        "",
        "## Variants per input style",
        "",
        f"- concise_clinical: {pairs_by_style['concise_clinical']}",
        f"- semi_structured: {pairs_by_style['semi_structured']}",
        "",
        "## Two-variant support",
        "",
        "- Seeds that could not cleanly support two variants: none.",
        "- Sparse seeds were still able to support two conservative variants, but some were flagged for manual review because the two texts are intentionally close.",
        "",
        "## Manual review focus",
        "",
        f"- Candidate pairs flagged for manual review: {len(flags)}",
        f"- Seeds flagged for manual review: {', '.join(flagged_seed_ids) if flagged_seed_ids else 'none'}",
        "- Priority review themes: sparse seeds, linked-context containment, and awkward numeric precision.",
        "",
        "## Comparison to the Synthea pairing pilot",
        "",
        "- Does this Official pairing pilot appear cleaner than the Synthea pairing pilot? Likely yes.",
        "- This is a qualitative judgment based on the smaller scope, stricter seed anchoring, and deliberate avoidance of inferred context rather than a side-by-side benchmark in this repository.",
        "",
        "## Notes",
        "",
        "- All 24 candidate pairs point to pre-existing selected Official seeds; no new target FHIR JSON was created.",
        "- All variants use only `concise_clinical` or `semi_structured` styles.",
        "- No `patient_utterance` or mildly noisy variants were generated.",
        "- All Observation variants preserve the explicit value and unit from the seed.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    selected_rows = load_selected(args.selected_path)
    pairs, pair_lookup = build_pairs(selected_rows)
    validate_pairs(pairs)
    flags = build_flags(pair_lookup)
    attach_review_status(pairs, flags)

    write_jsonl(args.output_dir / "official_pilot12_pair_candidates.jsonl", pairs)
    write_csv(args.output_dir / "official_pilot12_pair_candidates.csv", PAIR_FIELDS, pairs)
    write_summary(args.output_dir / "official_pilot12_pair_generation_summary.md", selected_rows, pairs, flags)
    write_csv(
        args.output_dir / "official_pilot12_pair_review_flags.csv",
        ["pair_id", "seed_id", "resource_type", "flag_type", "flag_reason"],
        flags,
    )

    print(f"Generated {len(pairs)} official candidate pairs")
    print(f"Flags written: {len(flags)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

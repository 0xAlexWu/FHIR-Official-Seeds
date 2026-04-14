#!/usr/bin/env python3
"""Profile retained HL7 FHIR R4 official examples for candidate curation."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


TARGET_RESOURCE_TYPES = ("Patient", "Observation", "Condition")
NUMERIC_VALUE_KEYS = {
    "valueQuantity",
    "valueInteger",
    "valueDecimal",
    "valueRange",
    "valueRatio",
    "valueSampledData",
}
DIRECT_VALUE_KEYS = {
    "valueQuantity",
    "valueInteger",
    "valueDecimal",
    "valueRange",
    "valueRatio",
    "valueSampledData",
    "valueString",
    "valueBoolean",
    "valueDateTime",
    "valueTime",
    "valueCodeableConcept",
    "valuePeriod",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=root / "data" / "raw",
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        default=root / "data" / "raw" / "official_examples_manifest.csv",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=root / "data" / "processed" / "official_candidate_profiles.jsonl",
    )
    return parser.parse_args()


def load_manifest(manifest_path: Path) -> dict[str, dict[str, str]]:
    manifest: dict[str, dict[str, str]] = {}
    if not manifest_path.exists():
        return manifest

    with manifest_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            manifest[row["extracted_path"]] = row
    return manifest


def iter_json_files(raw_root: Path) -> list[Path]:
    files: list[Path] = []
    for resource_type in TARGET_RESOURCE_TYPES:
        resource_dir = raw_root / resource_type
        if resource_dir.exists():
            files.extend(sorted(resource_dir.glob("*.json")))
    return sorted(files)


def extract_reference_pairs(value: Any, path: str = "") -> list[tuple[str, str]]:
    references: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            next_path = f"{path}.{key}" if path else key
            if key == "reference" and isinstance(nested, str):
                references.append((path, nested))
            references.extend(extract_reference_pairs(nested, next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            next_path = f"{path}[{index}]"
            references.extend(extract_reference_pairs(item, next_path))
    return references


def external_reference_pairs(payload: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        (path, reference)
        for path, reference in extract_reference_pairs(payload)
        if reference and not reference.startswith("#")
    ]


def acceptable_reference_profile(resource_type: str, references: list[tuple[str, str]]) -> bool:
    if not references:
        return True

    if resource_type == "Patient":
        allowed_prefixes = ("managingOrganization",)
    elif resource_type == "Observation":
        allowed_prefixes = ("subject", "performer")
    elif resource_type == "Condition":
        allowed_prefixes = ("subject", "asserter")
    else:
        return False

    return all(any(path.startswith(prefix) for prefix in allowed_prefixes) for path, _ in references)


def has_unit(payload: dict[str, Any]) -> bool:
    quantity_like = []
    if isinstance(payload.get("valueQuantity"), dict):
        quantity_like.append(payload["valueQuantity"])
    for component in payload.get("component", []) if isinstance(payload.get("component"), list) else []:
        if isinstance(component.get("valueQuantity"), dict):
            quantity_like.append(component["valueQuantity"])
    for item in quantity_like:
        if any(item.get(field) for field in ("unit", "code", "system")):
            return True
    return False


def has_direct_value(payload: dict[str, Any]) -> bool:
    if any(key in payload for key in DIRECT_VALUE_KEYS):
        return True
    components = payload.get("component")
    if isinstance(components, list):
        for component in components:
            if isinstance(component, dict) and any(key in component for key in DIRECT_VALUE_KEYS):
                return True
    return False


def likely_numeric(payload: dict[str, Any]) -> bool:
    if any(key in payload for key in NUMERIC_VALUE_KEYS):
        return True
    components = payload.get("component")
    if isinstance(components, list):
        for component in components:
            if isinstance(component, dict) and any(key in component for key in NUMERIC_VALUE_KEYS):
                return True
    return False


def complexity_guess(resource_type: str, payload: dict[str, Any], external_reference_count: int) -> str:
    score = 0
    if len(payload.keys()) > 8:
        score += 1
    if payload.get("contained"):
        score += 2
    if payload.get("extension"):
        score += 2
    if external_reference_count:
        score += min(2, external_reference_count)
    if resource_type == "Observation":
        if payload.get("component"):
            score += 2
        if payload.get("hasMember") or payload.get("derivedFrom"):
            score += 2
    if resource_type == "Condition":
        if payload.get("stage") or payload.get("evidence"):
            score += 1
    if resource_type == "Patient":
        if len(payload.get("identifier", [])) > 1:
            score += 1
        if len(payload.get("contact", [])) > 0:
            score += 1

    if score <= 1:
        return "low"
    if score <= 4:
        return "medium"
    return "high"


def build_review_notes(
    resource_type: str,
    payload: dict[str, Any],
    linked_context: bool,
    acceptable_refs: bool,
    numeric_flag: bool | None,
    has_value_flag: bool | None,
    has_unit_flag: bool | None,
) -> str:
    notes: list[str] = []

    if linked_context:
        external_refs = [
            reference
            for _, reference in external_reference_pairs(payload)
        ]
        if external_refs:
            if acceptable_refs:
                notes.append("light linked context only")
            else:
                notes.append(f"external refs: {', '.join(sorted(set(external_refs))[:3])}")

    if resource_type == "Observation":
        if payload.get("component"):
            notes.append("multi-component observation")
        if payload.get("hasMember"):
            notes.append("panel/member relationship present")
        if numeric_flag:
            notes.append("likely numeric observation")
        if has_value_flag is False:
            notes.append("missing direct value")
        if numeric_flag and not has_unit_flag:
            notes.append("numeric-style value without clear unit")

    if resource_type == "Condition" and "code" not in payload:
        notes.append("missing explicit condition code")
    if resource_type == "Patient" and not any(key in payload for key in ("name", "identifier", "gender", "birthDate")):
        notes.append("thin demographic content")

    return "; ".join(notes) if notes else "clean baseline example"


def good_for_pairing(
    resource_type: str,
    payload: dict[str, Any],
    json_valid: bool,
    acceptable_refs: bool,
    complexity: str,
    numeric_flag: bool | None,
    has_value_flag: bool | None,
    has_unit_flag: bool | None,
) -> bool:
    if not json_valid or not acceptable_refs or complexity == "high":
        return False

    if resource_type == "Patient":
        return any(key in payload for key in ("name", "identifier", "gender", "birthDate")) and complexity in {"low", "medium"}

    if resource_type == "Condition":
        return "code" in payload and complexity in {"low", "medium"}

    if resource_type == "Observation":
        if payload.get("component") or payload.get("hasMember") or payload.get("derivedFrom"):
            return False
        if not has_value_flag:
            return False
        if numeric_flag:
            return bool(has_unit_flag) and complexity in {"low", "medium"}
        return complexity == "low"

    return False


def bool_string(value: bool | None) -> str:
    if value is None:
        return ""
    return "true" if value else "false"


def profile_file(path: Path, manifest: dict[str, dict[str, str]]) -> dict[str, Any]:
    relative_path = path.relative_to(repo_root())
    raw_text = path.read_text(encoding="utf-8")
    json_valid = True
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        payload = {}
        json_valid = False

    resource_type = payload.get("resourceType") if json_valid else path.parent.name
    resource_id = payload.get("id", "") if json_valid else ""
    manifest_row = manifest.get(str(relative_path), {})
    source_name = manifest_row.get("source_zip_path", str(relative_path))

    numeric_flag: bool | None = None
    has_value_flag: bool | None = None
    has_unit_flag: bool | None = None

    references = external_reference_pairs(payload) if json_valid else []
    linked_context = bool(references)
    acceptable_refs = acceptable_reference_profile(resource_type, references) if json_valid else False

    if resource_type == "Observation" and json_valid:
        numeric_flag = likely_numeric(payload)
        has_value_flag = has_direct_value(payload)
        has_unit_flag = has_unit(payload)

    complexity = complexity_guess(resource_type, payload, len(references)) if json_valid else "high"
    good_pairing = good_for_pairing(
        resource_type,
        payload,
        json_valid,
        acceptable_refs,
        complexity,
        numeric_flag,
        has_value_flag,
        has_unit_flag,
    )
    review_notes = build_review_notes(
        resource_type,
        payload,
        linked_context,
        acceptable_refs,
        numeric_flag,
        has_value_flag,
        has_unit_flag,
    )

    return {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "source_file_or_example_name": source_name,
        "json_valid": bool_string(json_valid),
        "likely_numeric": bool_string(numeric_flag),
        "has_value": bool_string(has_value_flag),
        "has_unit": bool_string(has_unit_flag),
        "needs_linked_context": bool_string(linked_context),
        "complexity_guess": complexity,
        "good_for_pairing": bool_string(good_pairing),
        "review_notes": review_notes,
        "source_path": str(relative_path),
    }


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest_path)
    args.output_path.parent.mkdir(parents=True, exist_ok=True)

    profiles = [profile_file(path, manifest) for path in iter_json_files(args.raw_root)]
    with args.output_path.open("w", encoding="utf-8") as handle:
        for profile in profiles:
            handle.write(json.dumps(profile, ensure_ascii=True, sort_keys=True))
            handle.write("\n")

    print(f"Profiled {len(profiles)} official candidates")
    print(f"Wrote {args.output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Package Official pair candidates into reviewer-ready batch prompt files."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


BATCH_SIZE = 10
PROMPT_HEADER = """You are acting as an external reviewer in a clinical-data-to-FHIR pairing evaluation workflow.

You will review multiple candidate paired samples.
Apply the same scoring rubric independently to each item.
Do not compare items with each other.
Judge each pair only on its own merits.

For each item, return:
- pair_id
- faithfulness
- unsupported_fact
- omission
- naturalness
- context_leakage
- short_rationale
- flag_type

Scoring rubric:
- faithfulness: 1 = faithful, 0 = not faithful
- unsupported_fact: 1 = yes, 0 = no
- omission: 1 = yes, 0 = no
- naturalness: 1 to 5
- context_leakage: 1 = yes, 0 = no

Allowed flag_type values:
- none
- possible_hallucination
- possible_omission
- awkward_input
- context_leakage
- style_uncertainty
- other

Review principles:
1. Only judge alignment between the shown input text and the shown target FHIR JSON.
2. Do not assume facts from linked resources unless explicitly present in the shown target JSON.
3. Do not reward unsupported extra detail.
4. Be conservative about unsupported facts.
5. Be conservative about omission of core information.
6. If the target is sparse, do not punish the input for not containing unavailable details.

Return only a JSON array.
Do not include markdown.
Do not include any text before or after the JSON array.
"""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pairs-path",
        type=Path,
        default=root / "outputs" / "official" / "official_pilot12_pair_candidates.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "official",
    )
    parser.add_argument(
        "--prompt-dir",
        type=Path,
        default=root / "outputs" / "reviewer_batch_prompts",
    )
    return parser.parse_args()


def load_pairs(path: Path) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                pairs.append(json.loads(line))
    return sorted(pairs, key=lambda row: row["pair_id"])


def chunked(items: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + batch_size] for index in range(0, len(items), batch_size)]


def render_item(item_number: int, pair: dict[str, Any], target_json_text: str) -> str:
    return (
        f"ITEM {item_number}\n"
        f"pair_id: {pair['pair_id']}\n"
        f"resource_type: {pair['resource_type']}\n"
        f"input_style: {pair['input_style']}\n"
        "input_text:\n"
        f"{pair['input_text']}\n"
        "target_fhir_json:\n"
        f"{target_json_text.rstrip()}\n"
    )


def build_prompt(batch_pairs: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    item_stats: list[dict[str, Any]] = []
    rendered_items: list[str] = []

    for item_number, pair in enumerate(batch_pairs, start=1):
        target_path = repo_root() / pair["target_seed_file"]
        if not target_path.exists():
            raise FileNotFoundError(f"Missing target seed file: {target_path}")
        target_json_text = target_path.read_text(encoding="utf-8")
        rendered = render_item(item_number, pair, target_json_text)
        rendered_items.append(rendered)
        item_stats.append(
            {
                "pair_id": pair["pair_id"],
                "resource_type": pair["resource_type"],
                "length_chars": len(rendered),
            }
        )

    prompt_text = PROMPT_HEADER.rstrip() + "\n\n" + "\n\n".join(rendered_items) + "\n"
    return prompt_text, item_stats


def unusual_long_items(item_stats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lengths = [item["length_chars"] for item in item_stats]
    if not lengths:
        return []
    if len(lengths) < 4:
        return sorted(item_stats, key=lambda row: row["length_chars"], reverse=True)[:1]

    sorted_lengths = sorted(lengths)
    midpoint = len(sorted_lengths) // 2
    lower_half = sorted_lengths[:midpoint]
    upper_half = sorted_lengths[-midpoint:]
    q1 = statistics.median(lower_half)
    q3 = statistics.median(upper_half)
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    flagged = [item for item in item_stats if item["length_chars"] > threshold]
    return sorted(flagged, key=lambda row: row["length_chars"], reverse=True)


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


def write_summary(
    path: Path,
    total_pairs: int,
    batches: list[list[dict[str, Any]]],
    long_items: list[dict[str, Any]],
) -> None:
    full_batches = sum(len(batch) == BATCH_SIZE for batch in batches)
    partial_batch = any(len(batch) < BATCH_SIZE for batch in batches)
    lines = [
        "# Reviewer Batching Summary",
        "",
        f"- Total number of Official pairs packaged: {total_pairs}",
        f"- Total number of batches created: {len(batches)}",
        f"- Full 10-item batches created: {full_batches}",
        f"- Final partial batch present: {'yes' if partial_batch else 'no'}",
        "",
        "## Unusually long items",
        "",
    ]

    if long_items:
        for item in long_items:
            lines.append(
                f"- `{item['pair_id']}` (`{item['resource_type']}`) rendered item length: {item['length_chars']} characters"
            )
    else:
        lines.append("- None detected by the batching heuristic.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    prompt_dir = args.prompt_dir
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for existing_prompt in prompt_dir.glob("review_batch_*.txt"):
        existing_prompt.unlink()

    pairs = load_pairs(args.pairs_path)
    if not pairs:
        raise ValueError("No Official pair candidates were found.")

    batches = chunked(pairs, BATCH_SIZE)
    batch_index_rows: list[dict[str, Any]] = []
    batch_manifest_rows: list[dict[str, Any]] = []
    all_item_stats: list[dict[str, Any]] = []
    seen_pair_ids: list[str] = []

    for batch_number, batch_pairs in enumerate(batches, start=1):
        batch_id = f"review_batch_{batch_number:03d}"
        file_name = f"{batch_id}.txt"
        prompt_text, item_stats = build_prompt(batch_pairs)
        (prompt_dir / file_name).write_text(prompt_text, encoding="utf-8")

        pair_ids = [pair["pair_id"] for pair in batch_pairs]
        seen_pair_ids.extend(pair_ids)
        all_item_stats.extend(item_stats)

        batch_index_rows.append(
            {
                "batch_id": batch_id,
                "file_name": file_name,
                "start_pair_id": pair_ids[0],
                "end_pair_id": pair_ids[-1],
                "item_count": len(batch_pairs),
            }
        )
        batch_manifest_rows.append(
            {
                "batch_id": batch_id,
                "file_name": file_name,
                "item_count": len(batch_pairs),
                "pair_ids": pair_ids,
            }
        )

    if sorted(seen_pair_ids) != sorted(pair["pair_id"] for pair in pairs):
        raise ValueError("Not all Official pairs were packaged exactly once.")

    long_items = unusual_long_items(all_item_stats)

    write_csv(
        args.output_dir / "reviewer_batch_index.csv",
        ["batch_id", "file_name", "start_pair_id", "end_pair_id", "item_count"],
        batch_index_rows,
    )
    write_jsonl(args.output_dir / "reviewer_batch_manifest.jsonl", batch_manifest_rows)
    write_summary(args.output_dir / "reviewer_batching_summary.md", len(pairs), batches, long_items)

    print(f"Packaged {len(pairs)} Official pairs into {len(batches)} reviewer batches")
    print(f"Full 10-item batches: {sum(len(batch) == BATCH_SIZE for batch in batches)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

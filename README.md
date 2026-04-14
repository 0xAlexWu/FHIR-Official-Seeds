# FHIR-official-seeds

Independent Official-derived curation workflow for HL7 FHIR R4 official examples.

This repository is intentionally separate from any Synthea-derived workflow. It only profiles and curates HL7 FHIR R4 official example resources for:

- Patient
- Observation
- Condition

Current scope:

- download or ingest HL7 FHIR R4 official JSON examples
- retain only Patient, Observation, and Condition
- profile candidates for pilot seed curation readiness
- build a conservative candidate catalog for later shortlist review

Out of scope in this repository:

- mixing Synthea data
- generating paired input variants
- creating final paired samples

## Source scope

Primary source:

- `https://www.hl7.org/fhir/R4/examples-json.zip`

The fetch step downloads the official HL7 FHIR R4 JSON example archive, filters it to the target resource types, and stores only those resources in this repository.

## Repository layout

```text
.
├── README.md
├── scripts/
│   ├── fetch_official_examples.py
│   ├── profile_official_examples.py
│   └── build_candidate_catalog.py
├── data/
│   ├── raw/
│   └── processed/
└── outputs/
    └── official/
        ├── resource_counts_summary.csv
        ├── observation_profile_summary.csv
        ├── candidate_seed_catalog.csv
        └── official_source_summary.md
```

## Workflow

Run the pipeline from the repository root:

```bash
python3 scripts/fetch_official_examples.py
python3 scripts/profile_official_examples.py
python3 scripts/build_candidate_catalog.py
```

The scripts are deterministic and safe to rerun. Generated files are refreshed inside this repository only.

## Output files

- `outputs/official/resource_counts_summary.csv`
  - resource-level counts and conservative pairing readiness counts
- `outputs/official/observation_profile_summary.csv`
  - aggregate Observation profiling summary for numeric/value/unit presence
- `outputs/official/candidate_seed_catalog.csv`
  - one row per official candidate example
- `outputs/official/official_source_summary.md`
  - concise judgment on scale, sufficiency, and recommended pilot shortlist size

## Candidate catalog fields

Each candidate row records:

- `candidate_id`
- `resource_type`
- `resource_id`
- `source_file_or_example_name`
- `json_valid`
- `likely_numeric`
- `has_value`
- `has_unit`
- `needs_linked_context`
- `complexity_guess`
- `good_for_pairing`
- `review_notes`

## Heuristic intent

The workflow is deliberately conservative. It favors examples that are structurally clean, semantically clear, and more likely to serve as strong target-side gold anchors later.

In practice, that means:

- self-contained resources are preferred
- heavily linked or high-complexity examples are downgraded
- Observation candidates with direct values and clear units are preferred

## Next steps

After reviewing the generated outputs:

1. Inspect `candidate_seed_catalog.csv` for likely shortlist candidates.
2. Select a small Official-derived pilot shortlist.
3. Review shortlisted candidates manually before any later pairing work.
4. Keep pairing and sample construction in a later repository stage, not here.

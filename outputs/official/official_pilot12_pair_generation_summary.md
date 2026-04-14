# Official Pilot 12 Pair Generation Summary

- Total number of seeds processed: 12
- Total number of candidate pairs generated: 24

## Variants per resource type

- Patient: 6
- Observation: 12
- Condition: 6

## Variants per input style

- concise_clinical: 12
- semi_structured: 12

## Two-variant support

- Seeds that could not cleanly support two variants: none.
- Sparse seeds were still able to support two conservative variants, but some were flagged for manual review because the two texts are intentionally close.

## Manual review focus

- Candidate pairs flagged for manual review: 6
- Seeds flagged for manual review: official-pilot12-02, official-pilot12-03, official-pilot12-04, official-pilot12-09, official-pilot12-10
- Priority review themes: sparse seeds, linked-context containment, and awkward numeric precision.

## Comparison to the Synthea pairing pilot

- Does this Official pairing pilot appear cleaner than the Synthea pairing pilot? Likely yes.
- This is a qualitative judgment based on the smaller scope, stricter seed anchoring, and deliberate avoidance of inferred context rather than a side-by-side benchmark in this repository.

## Notes

- All 24 candidate pairs point to pre-existing selected Official seeds; no new target FHIR JSON was created.
- All variants use only `concise_clinical` or `semi_structured` styles.
- No `patient_utterance` or mildly noisy variants were generated.
- All Observation variants preserve the explicit value and unit from the seed.

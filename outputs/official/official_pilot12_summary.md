# Official Pilot 12 Summary

## Final counts by resource type

- Patient: 3
- Observation: 6
- Condition: 3

## Strict preferred criteria coverage

- Selections meeting the strict preferred criteria exactly as written: 3 of 12
- Strict Patient selections: 3
- Strict Observation selections: 0
- Strict Condition selections: 0

## Criteria relaxations used

- Nine selections required one explicit relaxation: accepting light linked context only.
- This relaxation was necessary because the official Observation and Condition pools are dominated by subject and performer style references.
- No selected seed relaxed away from `good_for_pairing = true`.
- No selected seed relaxed away from low-or-medium complexity.
- All selected Observations still satisfy `likely_numeric = true`, `has_value = true`, and `has_unit = true`.

## Why these 12 work as Official-derived pilot anchors

- The Patient subset is intentionally self-contained and gives the pilot a stable demographic anchor without importing graph-heavy context.
- The Observation subset concentrates on common, numerically explicit measurements with clear units and straightforward target-side semantics.
- The Condition subset favors simple diagnosis anchors over more ambiguous or heavily contextual examples.
- Together, the set stays small, review-ready, and standards-aligned while remaining conservative about ambiguity and dependency.

## Selected shortlist

### Patient

- `official-pilot12-01` `ihe-pcd` from `patient-example-ihe-pcd.json`: Low-complexity self-contained Patient example with clear identity fields and no linked-resource dependency.
- `official-pilot12-02` `proband` from `patient-example-proband.json`: Low-complexity self-contained Patient example that broadens the pilot with a genetics-oriented but still clean standalone record.
- `official-pilot12-03` `newborn` from `patient-example-newborn.json`: Self-contained neonatal Patient example retained for age-range diversity despite thinner demographics than the adult examples.

### Observation

- `official-pilot12-04` `body-height` from `observation-example-body-height.json`: Canonical numeric body measurement with direct value and unit; accepted with light subject-only context.
- `official-pilot12-05` `body-temperature` from `observation-example-body-temperature.json`: Canonical temperature Observation with direct numeric value and explicit unit; strong target-side gold anchor.
- `official-pilot12-06` `heart-rate` from `observation-example-heart-rate.json`: Canonical vital-sign Observation with unambiguous code, direct value, and unit; only light subject context.
- `official-pilot12-07` `respiratory-rate` from `observation-example-respiratory-rate.json`: Canonical vital-sign Observation with direct numeric value and unit; complements heart-rate and temperature anchors.
- `official-pilot12-08` `mbp` from `observation-example-mbp.json`: Clear hemodynamic Observation with direct numeric value and unit; chosen to diversify the vital-sign subset.
- `official-pilot12-09` `f001` from `observation-example-f001-glucose.json`: Clean lab Observation with standard chemistry semantics and explicit units; kept to add non-vital measurement coverage.

### Condition

- `official-pilot12-10` `stroke` from `condition-example-stroke.json`: Clear confirmed diagnosis example with straightforward Condition structure and only light subject linkage.
- `official-pilot12-11` `example` from `condition-example.json`: Simple acute Condition example with explicit diagnosis coding; suitable as a compact diagnosis anchor.
- `official-pilot12-12` `example2` from `condition-example2.json`: Simple chronic Condition example centered on Asthma; retained for diagnosis-type diversity in the pilot set.

## Relaxed selections

- `official-pilot12-04` `Observation` `body-height`: accepted with light linked context only.
- `official-pilot12-05` `Observation` `body-temperature`: accepted with light linked context only.
- `official-pilot12-06` `Observation` `heart-rate`: accepted with light linked context only.
- `official-pilot12-07` `Observation` `respiratory-rate`: accepted with light linked context only.
- `official-pilot12-08` `Observation` `mbp`: accepted with light linked context only.
- `official-pilot12-09` `Observation` `f001`: accepted with light linked context only.
- `official-pilot12-10` `Condition` `stroke`: accepted with light linked context only.
- `official-pilot12-11` `Condition` `example`: accepted with light linked context only.
- `official-pilot12-12` `Condition` `example2`: accepted with light linked context only.

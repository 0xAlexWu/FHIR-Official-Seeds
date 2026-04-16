# Clinical data to FHIR evaluation workflow
_Exported on 2026/4/14 at GMT+8 15:37:10 from Cursor (2.5.20)_

---

**User**

You are acting as an external reviewer in a clinical-data-to-FHIR pairing evaluation workflow.

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

ITEM 1
pair_id: official-pair-001
resource_type: Patient
input_style: concise_clinical
input_text:
Active patient record for ALBERT BROOKS with identifier AB60001.
target_fhir_json:
{
  "active": true,
  "id": "ihe-pcd",
  "identifier": [
    {
      "type": {
        "text": "Internal Identifier"
      },
      "value": "AB60001"
    }
  ],
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "name": [
    {
      "family": "BROOKS",
      "given": [
        "ALBERT"
      ]
    }
  ],
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Albert Brooks, Id: AB60001</div>",
    "status": "generated"
  }
}


ITEM 2
pair_id: official-pair-002
resource_type: Patient
input_style: semi_structured
input_text:
Patient name: ALBERT BROOKS | Identifier: AB60001 | Active: true
target_fhir_json:
{
  "active": true,
  "id": "ihe-pcd",
  "identifier": [
    {
      "type": {
        "text": "Internal Identifier"
      },
      "value": "AB60001"
    }
  ],
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "name": [
    {
      "family": "BROOKS",
      "given": [
        "ALBERT"
      ]
    }
  ],
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Albert Brooks, Id: AB60001</div>",
    "status": "generated"
  }
}


ITEM 3
pair_id: official-pair-003
resource_type: Patient
input_style: concise_clinical
input_text:
Active female patient born 1966-04-04 with identifier 999999999.
target_fhir_json:
{
  "active": true,
  "birthDate": "1966-04-04",
  "deceasedBoolean": false,
  "gender": "female",
  "id": "proband",
  "identifier": [
    {
      "assigner": {
        "display": "Boston Massachesetts General Hospital"
      },
      "system": "urn:oid:2.16.840.1.113883.6.117",
      "type": {
        "text": "Computer-Stored Abulatory Records (COSTAR)"
      },
      "use": "usual",
      "value": "999999999"
    }
  ],
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\n      <p>\n\n        <b>Annie Proband</b>: Female, born 1966-04-04\n      </p>\n\n    </div>",
    "status": "generated"
  }
}


ITEM 4
pair_id: official-pair-004
resource_type: Patient
input_style: semi_structured
input_text:
Patient record | Gender: female | Birth date: 1966-04-04 | Identifier: 999999999 | Active: true
target_fhir_json:
{
  "active": true,
  "birthDate": "1966-04-04",
  "deceasedBoolean": false,
  "gender": "female",
  "id": "proband",
  "identifier": [
    {
      "assigner": {
        "display": "Boston Massachesetts General Hospital"
      },
      "system": "urn:oid:2.16.840.1.113883.6.117",
      "type": {
        "text": "Computer-Stored Abulatory Records (COSTAR)"
      },
      "use": "usual",
      "value": "999999999"
    }
  ],
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\n      <p>\n\n        <b>Annie Proband</b>: Female, born 1966-04-04\n      </p>\n\n    </div>",
    "status": "generated"
  }
}


ITEM 5
pair_id: official-pair-005
resource_type: Patient
input_style: concise_clinical
input_text:
Male patient with birth date 2017-09-05.
target_fhir_json:
{
  "_birthDate": {
    "extension": [
      {
        "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
        "valueDateTime": "2017-05-09T17:11:00+01:00"
      }
    ]
  },
  "birthDate": "2017-09-05",
  "extension": [
    {
      "url": "http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
      "valueString": "Everywoman"
    }
  ],
  "gender": "male",
  "id": "newborn",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "multipleBirthInteger": 2,
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: newborn</p><p><b>gender</b>: male</p><p><b>birthDate</b>: 05/09/2017</p><p><b>multipleBirth</b>: 2</p></div>",
    "status": "generated"
  }
}


ITEM 6
pair_id: official-pair-006
resource_type: Patient
input_style: semi_structured
input_text:
Patient record | Gender: male | Birth date: 2017-09-05
target_fhir_json:
{
  "_birthDate": {
    "extension": [
      {
        "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
        "valueDateTime": "2017-05-09T17:11:00+01:00"
      }
    ]
  },
  "birthDate": "2017-09-05",
  "extension": [
    {
      "url": "http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
      "valueString": "Everywoman"
    }
  ],
  "gender": "male",
  "id": "newborn",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "multipleBirthInteger": 2,
  "resourceType": "Patient",
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: newborn</p><p><b>gender</b>: male</p><p><b>birthDate</b>: 05/09/2017</p><p><b>multipleBirth</b>: 2</p></div>",
    "status": "generated"
  }
}


ITEM 7
pair_id: official-pair-007
resource_type: Observation
input_style: concise_clinical
input_text:
Final body height observation: 66.89999999999999 in.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8302-2",
        "display": "Body height",
        "system": "http://loinc.org"
      }
    ],
    "text": "Body height"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "body-height",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: body-height</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Body height <span>(Details : {LOINC code '8302-2' = 'Body height', given as 'Body height'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 66.899999999999991 in<span> (Details: UCUM code [in_i] = 'in_i')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "[in_i]",
    "system": "http://unitsofmeasure.org",
    "unit": "in",
    "value": 66.89999999999999
  }
}


ITEM 8
pair_id: official-pair-008
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Body height | Status: final | Value: 66.89999999999999 in | Effective date: 1999-07-02
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8302-2",
        "display": "Body height",
        "system": "http://loinc.org"
      }
    ],
    "text": "Body height"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "body-height",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: body-height</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Body height <span>(Details : {LOINC code '8302-2' = 'Body height', given as 'Body height'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 66.899999999999991 in<span> (Details: UCUM code [in_i] = 'in_i')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "[in_i]",
    "system": "http://unitsofmeasure.org",
    "unit": "in",
    "value": 66.89999999999999
  }
}


ITEM 9
pair_id: official-pair-009
resource_type: Observation
input_style: concise_clinical
input_text:
Final body temperature: 36.5 C.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8310-5",
        "display": "Body temperature",
        "system": "http://loinc.org"
      }
    ],
    "text": "Body temperature"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "body-temperature",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: body-temperature</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Body temperature <span>(Details : {LOINC code '8310-5' = 'Body temperature', given as 'Body temperature'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 36.5 C<span> (Details: UCUM code Cel = 'Cel')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "Cel",
    "system": "http://unitsofmeasure.org",
    "unit": "C",
    "value": 36.5
  }
}


ITEM 10
pair_id: official-pair-010
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Body temperature | Status: final | Value: 36.5 C | Effective date: 1999-07-02
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8310-5",
        "display": "Body temperature",
        "system": "http://loinc.org"
      }
    ],
    "text": "Body temperature"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "body-temperature",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: body-temperature</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Body temperature <span>(Details : {LOINC code '8310-5' = 'Body temperature', given as 'Body temperature'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 36.5 C<span> (Details: UCUM code Cel = 'Cel')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "Cel",
    "system": "http://unitsofmeasure.org",
    "unit": "C",
    "value": 36.5
  }
}



---

**Cursor**

```json
[
  {
    "pair_id": "official-pair-001",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All three input facts (active status, patient name ALBERT BROOKS, identifier AB60001) are correctly and completely represented in the FHIR. Structural additions (id, meta HTEST tag, identifier type label) are standard FHIR boilerplate, not clinical assertions.",
    "flag_type": "none"
  },
  {
    "pair_id": "official-pair-002",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All three explicitly labeled fields (name, identifier, active) map correctly to the FHIR target. Semi-structured format is clear and unambiguous. No unsupported assertions beyond standard structural metadata.",
    "flag_type": "none"
  },
  {
    "pair_id": "official-pair-003",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 1,
    "short_rationale": "Core clinical facts (active, female, birthDate 1966-04-04, identifier 999999999) are faithfully mapped. However, deceasedBoolean=false is an unsupported assertion not derivable from the input, and the identifier assigner 'Boston Massachesetts General Hospital' has no basis in the input. The name 'Annie Proband' appears in the narrative div but is absent from both the input and the structured name field, indicating leaked external context.",
    "flag_type": "context_leakage"
  },
  {
    "pair_id": "official-pair-004",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 1,
    "short_rationale": "All four stated fields (gender, birth date, identifier, active) are correctly mapped. Same issues as the concise counterpart: deceasedBoolean=false and the identifier assigner are unsupported, and the name 'Annie Proband' in the narrative div is not sourced from the input, indicating external context leakage.",
    "flag_type": "context_leakage"
  },
  {
    "pair_id": "official-pair-005",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 3,
    "context_leakage": 0,
    "short_rationale": "Gender (male) and birth date (2017-09-05) are correctly mapped. However, the FHIR contains multiple unsupported clinical facts with no basis in the sparse input: mother's maiden name 'Everywoman', multipleBirthInteger=2, and a specific birth time extension. The input is too minimal to naturally convey these details.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-006",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Both stated fields (gender, birth date) are correctly mapped. The same unsupported facts as pair-005 are present: mother's maiden name 'Everywoman', multipleBirthInteger=2, and a birth time extension, none of which are derivable from the input.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-007",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 2,
    "context_leakage": 0,
    "short_rationale": "Status (final), observation type (body height), and value (66.89999999999999 in) are faithfully preserved. The floating-point representation of the value is clinically awkward. effectiveDateTime 1999-07-02 and subject reference Patient/example appear in the FHIR with no basis in the input.",
    "flag_type": "awkward_input"
  },
  {
    "pair_id": "official-pair-008",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 3,
    "context_leakage": 0,
    "short_rationale": "All four input fields (observation type, status, value, effective date) are correctly mapped. Category vital-signs and subject reference are standard structural FHIR elements, not unsupported clinical assertions. The floating-point value remains awkward but is faithfully preserved.",
    "flag_type": "awkward_input"
  },
  {
    "pair_id": "official-pair-009",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Status (final), observation type (body temperature), and value (36.5 C) are faithfully mapped. effectiveDateTime 1999-07-02 is a specific temporal assertion appearing in the FHIR with no basis in the input, making it an unsupported fact.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-010",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All four stated fields (observation type, status, value, effective date) are faithfully and completely mapped to the FHIR target. Category vital-signs and subject reference are standard structural elements. No unsupported facts or omissions.",
    "flag_type": "none"
  }
]
```

---

**User**

You are acting as an external reviewer in a clinical-data-to-FHIR pairing evaluation workflow.

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

ITEM 1
pair_id: official-pair-011
resource_type: Observation
input_style: concise_clinical
input_text:
Final heart rate: 44 beats/minute.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8867-4",
        "display": "Heart rate",
        "system": "http://loinc.org"
      }
    ],
    "text": "Heart rate"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "heart-rate",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: heart-rate</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Heart rate <span>(Details : {LOINC code '8867-4' = 'Heart rate', given as 'Heart rate'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 44 beats/minute<span> (Details: UCUM code /min = '/min')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "/min",
    "system": "http://unitsofmeasure.org",
    "unit": "beats/minute",
    "value": 44
  }
}


ITEM 2
pair_id: official-pair-012
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Heart rate | Status: final | Value: 44 beats/minute | Effective date: 1999-07-02
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8867-4",
        "display": "Heart rate",
        "system": "http://loinc.org"
      }
    ],
    "text": "Heart rate"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "heart-rate",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: heart-rate</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Heart rate <span>(Details : {LOINC code '8867-4' = 'Heart rate', given as 'Heart rate'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 44 beats/minute<span> (Details: UCUM code /min = '/min')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "/min",
    "system": "http://unitsofmeasure.org",
    "unit": "beats/minute",
    "value": 44
  }
}


ITEM 3
pair_id: official-pair-013
resource_type: Observation
input_style: concise_clinical
input_text:
Final respiratory rate: 26 breaths/minute.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "9279-1",
        "display": "Respiratory rate",
        "system": "http://loinc.org"
      }
    ],
    "text": "Respiratory rate"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "respiratory-rate",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: respiratory-rate</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Respiratory rate <span>(Details : {LOINC code '9279-1' = 'Respiratory rate', given as 'Respiratory rate'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 26 breaths/minute<span> (Details: UCUM code /min = '/min')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "/min",
    "system": "http://unitsofmeasure.org",
    "unit": "breaths/minute",
    "value": 26
  }
}


ITEM 4
pair_id: official-pair-014
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Respiratory rate | Status: final | Value: 26 breaths/minute | Effective date: 1999-07-02
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "9279-1",
        "display": "Respiratory rate",
        "system": "http://loinc.org"
      }
    ],
    "text": "Respiratory rate"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "respiratory-rate",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ],
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: respiratory-rate</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Respiratory rate <span>(Details : {LOINC code '9279-1' = 'Respiratory rate', given as 'Respiratory rate'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 26 breaths/minute<span> (Details: UCUM code /min = '/min')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "/min",
    "system": "http://unitsofmeasure.org",
    "unit": "breaths/minute",
    "value": 26
  }
}


ITEM 5
pair_id: official-pair-015
resource_type: Observation
input_style: concise_clinical
input_text:
Final mean blood pressure: 80 mm[Hg].
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8478-0",
        "display": "Mean blood pressure",
        "system": "http://loinc.org"
      }
    ],
    "text": "Mean blood pressure"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "mbp",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: mbp</p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Mean blood pressure <span>(Details : {LOINC code '8478-0' = 'Mean blood pressure', given as 'Mean blood pressure'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 80 mm[Hg]<span> (Details: UCUM code mm[Hg] = 'mmHg')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "mm[Hg]",
    "system": "http://unitsofmeasure.org",
    "unit": "mm[Hg]",
    "value": 80
  }
}


ITEM 6
pair_id: official-pair-016
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Mean blood pressure | Status: final | Value: 80 mm[Hg] | Effective date: 1999-07-02
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "vital-signs",
          "display": "Vital Signs",
          "system": "http://terminology.hl7.org/CodeSystem/observation-category"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "code": "8478-0",
        "display": "Mean blood pressure",
        "system": "http://loinc.org"
      }
    ],
    "text": "Mean blood pressure"
  },
  "effectiveDateTime": "1999-07-02",
  "id": "mbp",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: mbp</p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span>(Details : {http://terminology.hl7.org/CodeSystem/observation-category code 'vital-signs' = 'Vital Signs', given as 'Vital Signs'})</span></p><p><b>code</b>: Mean blood pressure <span>(Details : {LOINC code '8478-0' = 'Mean blood pressure', given as 'Mean blood pressure'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 02/07/1999</p><p><b>value</b>: 80 mm[Hg]<span> (Details: UCUM code mm[Hg] = 'mmHg')</span></p></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "mm[Hg]",
    "system": "http://unitsofmeasure.org",
    "unit": "mm[Hg]",
    "value": 80
  }
}


ITEM 7
pair_id: official-pair-017
resource_type: Observation
input_style: concise_clinical
input_text:
Final blood glucose observation: 6.3 mmol/l.
target_fhir_json:
{
  "code": {
    "coding": [
      {
        "code": "15074-8",
        "display": "Glucose [Moles/volume] in Blood",
        "system": "http://loinc.org"
      }
    ]
  },
  "effectivePeriod": {
    "start": "2013-04-02T09:30:10+01:00"
  },
  "id": "f001",
  "identifier": [
    {
      "system": "http://www.bmc.nl/zorgportal/identifiers/observations",
      "use": "official",
      "value": "6323"
    }
  ],
  "interpretation": [
    {
      "coding": [
        {
          "code": "H",
          "display": "High",
          "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
        }
      ]
    }
  ],
  "issued": "2013-04-03T15:30:10+01:00",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "performer": [
    {
      "display": "A. Langeveld",
      "reference": "Practitioner/f005"
    }
  ],
  "referenceRange": [
    {
      "high": {
        "code": "mmol/L",
        "system": "http://unitsofmeasure.org",
        "unit": "mmol/l",
        "value": 6.2
      },
      "low": {
        "code": "mmol/L",
        "system": "http://unitsofmeasure.org",
        "unit": "mmol/l",
        "value": 3.1
      }
    }
  ],
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "display": "P. van de Heuvel",
    "reference": "Patient/f001"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: f001</p><p><b>identifier</b>: 6323 (OFFICIAL)</p><p><b>status</b>: final</p><p><b>code</b>: Glucose [Moles/volume] in Blood <span>(Details : {LOINC code '15074-8' = 'Glucose [Moles/volume] in Blood', given as 'Glucose [Moles/volume] in Blood'})</span></p><p><b>subject</b>: <a>P. van de Heuvel</a></p><p><b>effective</b>: 02/04/2013 9:30:10 AM --&gt; (ongoing)</p><p><b>issued</b>: 03/04/2013 3:30:10 PM</p><p><b>performer</b>: <a>A. Langeveld</a></p><p><b>value</b>: 6.3 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></p><p><b>interpretation</b>: High <span>(Details : {http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation code 'H' = 'High', given as 'High'})</span></p><h3>ReferenceRanges</h3><table><tr><td>-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td>*</td><td>3.1 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></td><td>6.2 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></td></tr></table></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "mmol/L",
    "system": "http://unitsofmeasure.org",
    "unit": "mmol/l",
    "value": 6.3
  }
}


ITEM 8
pair_id: official-pair-018
resource_type: Observation
input_style: semi_structured
input_text:
Observation: Glucose [Moles/volume] in Blood | Status: final | Value: 6.3 mmol/l | Effective start: 2013-04-02T09:30:10+01:00
target_fhir_json:
{
  "code": {
    "coding": [
      {
        "code": "15074-8",
        "display": "Glucose [Moles/volume] in Blood",
        "system": "http://loinc.org"
      }
    ]
  },
  "effectivePeriod": {
    "start": "2013-04-02T09:30:10+01:00"
  },
  "id": "f001",
  "identifier": [
    {
      "system": "http://www.bmc.nl/zorgportal/identifiers/observations",
      "use": "official",
      "value": "6323"
    }
  ],
  "interpretation": [
    {
      "coding": [
        {
          "code": "H",
          "display": "High",
          "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
        }
      ]
    }
  ],
  "issued": "2013-04-03T15:30:10+01:00",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "performer": [
    {
      "display": "A. Langeveld",
      "reference": "Practitioner/f005"
    }
  ],
  "referenceRange": [
    {
      "high": {
        "code": "mmol/L",
        "system": "http://unitsofmeasure.org",
        "unit": "mmol/l",
        "value": 6.2
      },
      "low": {
        "code": "mmol/L",
        "system": "http://unitsofmeasure.org",
        "unit": "mmol/l",
        "value": 3.1
      }
    }
  ],
  "resourceType": "Observation",
  "status": "final",
  "subject": {
    "display": "P. van de Heuvel",
    "reference": "Patient/f001"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: f001</p><p><b>identifier</b>: 6323 (OFFICIAL)</p><p><b>status</b>: final</p><p><b>code</b>: Glucose [Moles/volume] in Blood <span>(Details : {LOINC code '15074-8' = 'Glucose [Moles/volume] in Blood', given as 'Glucose [Moles/volume] in Blood'})</span></p><p><b>subject</b>: <a>P. van de Heuvel</a></p><p><b>effective</b>: 02/04/2013 9:30:10 AM --&gt; (ongoing)</p><p><b>issued</b>: 03/04/2013 3:30:10 PM</p><p><b>performer</b>: <a>A. Langeveld</a></p><p><b>value</b>: 6.3 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></p><p><b>interpretation</b>: High <span>(Details : {http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation code 'H' = 'High', given as 'High'})</span></p><h3>ReferenceRanges</h3><table><tr><td>-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td>*</td><td>3.1 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></td><td>6.2 mmol/l<span> (Details: UCUM code mmol/L = 'mmol/L')</span></td></tr></table></div>",
    "status": "generated"
  },
  "valueQuantity": {
    "code": "mmol/L",
    "system": "http://unitsofmeasure.org",
    "unit": "mmol/l",
    "value": 6.3
  }
}


ITEM 9
pair_id: official-pair-019
resource_type: Condition
input_style: concise_clinical
input_text:
Active confirmed ischemic stroke.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "encounter-diagnosis",
          "display": "Encounter Diagnosis",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "coding": [
      {
        "code": "422504002",
        "display": "Ischemic stroke (disorder)",
        "system": "http://snomed.info/sct"
      }
    ],
    "text": "Stroke"
  },
  "id": "stroke",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetDateTime": "2010-07-18",
  "resourceType": "Condition",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Ischemic stroke, July 18, 2010</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}


ITEM 10
pair_id: official-pair-020
resource_type: Condition
input_style: semi_structured
input_text:
Condition: Ischemic stroke (disorder) | Clinical status: active | Verification status: confirmed | Onset date: 2010-07-18
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "encounter-diagnosis",
          "display": "Encounter Diagnosis",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "coding": [
      {
        "code": "422504002",
        "display": "Ischemic stroke (disorder)",
        "system": "http://snomed.info/sct"
      }
    ],
    "text": "Stroke"
  },
  "id": "stroke",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetDateTime": "2010-07-18",
  "resourceType": "Condition",
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Ischemic stroke, July 18, 2010</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}



---

**Cursor**

```json
[
  {
    "pair_id": "official-pair-011",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Status (final), observation type (heart rate), and value (44 beats/minute) are faithfully mapped. effectiveDateTime 1999-07-02 and subject reference appear in the FHIR with no basis in the input.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-012",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All four stated fields (observation type, status, value, effective date) are correctly and completely mapped. Category vital-signs and subject reference are standard structural elements for this observation type.",
    "flag_type": "none"
  },
  {
    "pair_id": "official-pair-013",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Status (final), observation type (respiratory rate), and value (26 breaths/minute) are faithfully mapped. effectiveDateTime 1999-07-02 and subject reference appear in the FHIR with no basis in the input.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-014",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All four stated fields (observation type, status, value, effective date) are correctly mapped. Category vital-signs and subject reference are standard structural elements.",
    "flag_type": "none"
  },
  {
    "pair_id": "official-pair-015",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Status (final), observation type (mean blood pressure), and value (80 mm[Hg]) are faithfully mapped. effectiveDateTime 1999-07-02 and subject reference appear in the FHIR with no basis in the input.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-016",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All four stated fields (observation type, status, value, effective date) are correctly mapped. Category vital-signs and subject reference are standard structural elements.",
    "flag_type": "none"
  },
  {
    "pair_id": "official-pair-017",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 1,
    "short_rationale": "Status (final), glucose observation type, and value (6.3 mmol/l) are faithfully mapped. The FHIR contains extensive unsupported content absent from the input: a specific effective period timestamp, internal identifier 6323, interpretation High, issued timestamp, performer A. Langeveld, reference range, and named subject P. van de Heuvel. The named subject and performer constitute context leakage from an external source.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-018",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 1,
    "short_rationale": "All four stated fields (code, status, value, effective start) are correctly mapped. However, the FHIR contains multiple unsupported facts not present in the input: internal identifier 6323, interpretation High, issued timestamp, performer A. Langeveld, and reference range. Named subject P. van de Heuvel and performer A. Langeveld are not sourced from the input, indicating context leakage.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-019",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Clinical status (active), verification status (confirmed), and condition code (ischemic stroke) are faithfully mapped. onsetDateTime 2010-07-18 is a specific temporal assertion in the FHIR with no basis in the input. Category encounter-diagnosis is a structural addition.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-020",
    "faithfulness": 1,
    "unsupported_fact": 0,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All four stated fields (condition code, clinical status, verification status, onset date) are correctly and completely mapped to the FHIR target. Category encounter-diagnosis is a structural addition not contradicted by the input.",
    "flag_type": "none"
  }
]
```

---

**User**

You are acting as an external reviewer in a clinical-data-to-FHIR pairing evaluation workflow.

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

ITEM 1
pair_id: official-pair-021
resource_type: Condition
input_style: concise_clinical
input_text:
Active confirmed burn of ear involving the left external ear structure.
target_fhir_json:
{
  "bodySite": [
    {
      "coding": [
        {
          "code": "49521004",
          "display": "Left external ear structure",
          "system": "http://snomed.info/sct"
        }
      ],
      "text": "Left Ear"
    }
  ],
  "category": [
    {
      "coding": [
        {
          "code": "encounter-diagnosis",
          "display": "Encounter Diagnosis",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        },
        {
          "code": "439401001",
          "display": "Diagnosis",
          "system": "http://snomed.info/sct"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "coding": [
      {
        "code": "39065001",
        "display": "Burn of ear",
        "system": "http://snomed.info/sct"
      }
    ],
    "text": "Burnt Ear"
  },
  "id": "example",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetDateTime": "2012-05-24",
  "resourceType": "Condition",
  "severity": {
    "coding": [
      {
        "code": "24484000",
        "display": "Severe",
        "system": "http://snomed.info/sct"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Severe burn of left ear (Date: 24-May 2012)</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}


ITEM 2
pair_id: official-pair-022
resource_type: Condition
input_style: semi_structured
input_text:
Condition: Burn of ear | Body site: Left external ear structure | Clinical status: active | Verification status: confirmed | Onset date: 2012-05-24
target_fhir_json:
{
  "bodySite": [
    {
      "coding": [
        {
          "code": "49521004",
          "display": "Left external ear structure",
          "system": "http://snomed.info/sct"
        }
      ],
      "text": "Left Ear"
    }
  ],
  "category": [
    {
      "coding": [
        {
          "code": "encounter-diagnosis",
          "display": "Encounter Diagnosis",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        },
        {
          "code": "439401001",
          "display": "Diagnosis",
          "system": "http://snomed.info/sct"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "coding": [
      {
        "code": "39065001",
        "display": "Burn of ear",
        "system": "http://snomed.info/sct"
      }
    ],
    "text": "Burnt Ear"
  },
  "id": "example",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetDateTime": "2012-05-24",
  "resourceType": "Condition",
  "severity": {
    "coding": [
      {
        "code": "24484000",
        "display": "Severe",
        "system": "http://snomed.info/sct"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Severe burn of left ear (Date: 24-May 2012)</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}


ITEM 3
pair_id: official-pair-023
resource_type: Condition
input_style: concise_clinical
input_text:
Active confirmed asthma.
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "problem-list-item",
          "display": "Problem List Item",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "text": "Asthma"
  },
  "id": "example2",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetString": "approximately November 2012",
  "resourceType": "Condition",
  "severity": {
    "coding": [
      {
        "code": "255604002",
        "display": "Mild",
        "system": "http://snomed.info/sct"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Mild Asthma (Date: 12-Nov 2012)</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}


ITEM 4
pair_id: official-pair-024
resource_type: Condition
input_style: semi_structured
input_text:
Condition: Asthma | Clinical status: active | Verification status: confirmed
target_fhir_json:
{
  "category": [
    {
      "coding": [
        {
          "code": "problem-list-item",
          "display": "Problem List Item",
          "system": "http://terminology.hl7.org/CodeSystem/condition-category"
        }
      ]
    }
  ],
  "clinicalStatus": {
    "coding": [
      {
        "code": "active",
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical"
      }
    ]
  },
  "code": {
    "text": "Asthma"
  },
  "id": "example2",
  "meta": {
    "tag": [
      {
        "code": "HTEST",
        "display": "test health data",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason"
      }
    ]
  },
  "onsetString": "approximately November 2012",
  "resourceType": "Condition",
  "severity": {
    "coding": [
      {
        "code": "255604002",
        "display": "Mild",
        "system": "http://snomed.info/sct"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "text": {
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Mild Asthma (Date: 12-Nov 2012)</div>",
    "status": "generated"
  },
  "verificationStatus": {
    "coding": [
      {
        "code": "confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status"
      }
    ]
  }
}



---

**Cursor**

```json
[
  {
    "pair_id": "official-pair-021",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Clinical status (active), verification status (confirmed), condition code (burn of ear), and body site (left external ear structure) are all faithfully mapped. However, severity=Severe and onsetDateTime 2012-05-24 appear in the FHIR with no basis in the input text.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-022",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All five stated fields (condition code, body site, clinical status, verification status, onset date) are correctly mapped. severity=Severe is present in the FHIR but has no basis in the input, constituting an unsupported clinical assertion.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-023",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "Clinical status (active), verification status (confirmed), and condition code (asthma) are faithfully mapped. severity=Mild and onsetString 'approximately November 2012' appear in the FHIR with no basis in the sparse input.",
    "flag_type": "possible_hallucination"
  },
  {
    "pair_id": "official-pair-024",
    "faithfulness": 1,
    "unsupported_fact": 1,
    "omission": 0,
    "naturalness": 4,
    "context_leakage": 0,
    "short_rationale": "All three stated fields (condition code, clinical status, verification status) are correctly mapped. severity=Mild and onsetString 'approximately November 2012' are present in the FHIR but have no basis in the input.",
    "flag_type": "possible_hallucination"
  }
]
```


# Santiago Layer 1: Core Semantic Relationships Specification

## Overview

This document specifies the core semantic relationships used in Santiago Layer 1 for structured knowledge extraction from clinical text. These relationships form the foundation for representing clinical knowledge in the Santiago NeuroSymbolic knowledge graph.

The relationship types are aligned with SNOMED CT core semantic relationships (attributes) and organized by clinical domain. SNOMED CT defines approximately 50-55 core relationship types that connect concepts through attribute-value relationships rather than simple hierarchies. Santiago Layer 1 implements the most clinically relevant subset for knowledge extraction from unstructured text.

## Architecture Context

Santiago uses a four-layer architecture:
- **Layer 0**: Raw Text (document loading and preprocessing)
- **Layer 1**: Structured Knowledge (semantic relationships between clinical concepts)
- **Layer 2**: Computable Logic (clinical decision rules and workflows)
- **Layer 3**: Executable Workflows (automated clinical processes)

Layer 1 focuses on extracting and representing semantic relationships between clinical entities such as medications, conditions, diagnostic tests, and risk factors.

## Core Relationship Types

### 1. TREATS
**Definition**: A medication, therapy, or intervention treats a medical condition.

**Domain**: intervention (medication, procedure, therapy)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- evidence_levels: ["A", "B", "C", "D", "E"] (A = highest evidence)
- strength: ["first_line", "second_line", "adjunct", "alternative"]
- indications: ["approved", "off_label", "investigational"]

**Examples**:
- Metformin → Type 2 Diabetes Mellitus (evidence: A, strength: first_line)
- Aspirin → Myocardial Infarction (evidence: A, strength: secondary_prevention)
- Insulin → Diabetic Ketoacidosis (evidence: A, strength: first_line)

**Validation Rules**:
- Source must be a valid intervention
- Target must be a valid medical condition
- Evidence level must be specified (A-E)

### 2. INVESTIGATES
**Definition**: A diagnostic test or procedure investigates a medical condition.

**Domain**: diagnostic_test (laboratory test, imaging study, clinical assessment)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- sensitivity: float (0.0-1.0)
- specificity: float (0.0-1.0)
- test_type: ["laboratory", "imaging", "clinical", "pathology"]
- purpose: ["diagnosis", "screening", "monitoring", "staging"]

**Examples**:
- Hemoglobin A1c → Diabetes Mellitus (sensitivity: 0.85, specificity: 0.92, purpose: diagnosis)
- Echocardiogram → Heart Failure (sensitivity: 0.85, purpose: diagnosis)
- Colonoscopy → Colorectal Cancer (purpose: screening)

**Validation Rules**:
- Source must be a valid diagnostic test or procedure
- Target must be a valid medical condition
- Sensitivity and specificity should be within 0.0-1.0 range

### 3. COMPLICATES
**Definition**: A medical condition complicates or worsens another condition.

**Domain**: condition (disease, disorder, syndrome)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- severity: ["mild", "moderate", "severe", "life_threatening"]
- frequency: ["rare", "uncommon", "common", "very_common"]
- mechanisms: ["direct", "indirect", "iatrogenic", "progression"]

**Examples**:
- Diabetes Mellitus → Coronary Artery Disease (severity: severe, frequency: very_common)
- Chronic Kidney Disease → Hypertension (severity: moderate, frequency: very_common)
- Obesity → Sleep Apnea (severity: moderate, mechanisms: direct)

**Validation Rules**:
- Both source and target must be valid medical conditions
- Source and target should be different conditions
- Severity level should be specified

### 4. RISK_FACTOR
**Definition**: A factor increases the risk of developing a medical condition.

**Domain**: risk_factor (behavior, exposure, genetic factor, biomarker)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- relative_risk: float (> 1.0)
- odds_ratio: float (> 1.0)
- attributable_fraction: float (0.0-1.0)
- factor_type: ["modifiable", "non_modifiable", "genetic", "environmental"]

**Examples**:
- Smoking → Lung Cancer (relative_risk: 10.0, factor_type: modifiable)
- Family History → Breast Cancer (odds_ratio: 2.5, factor_type: genetic)
- Hypertension → Stroke (attributable_fraction: 0.35, factor_type: modifiable)

**Validation Rules**:
- Source must be a valid risk factor
- Target must be a valid medical condition
- Relative risk should be > 1.0 for risk factors

### 5. PRESENTS_WITH
**Definition**: A condition typically presents with a specific symptom or sign.

**Domain**: condition (disease, disorder, syndrome)  
**Range**: symptom|sign (clinical finding, vital sign abnormality)

**Properties**:
- frequency: ["rare", "occasional", "common", "hallmark"]
- specificity: float (0.0-1.0)
- sensitivity: float (0.0-1.0)

**Examples**:
- Pneumonia → Fever (frequency: common, specificity: 0.3)
- Myocardial Infarction → Chest Pain (frequency: hallmark, specificity: 0.7)
- Diabetic Ketoacidosis → Fruity Breath (frequency: hallmark, specificity: 0.95)

**Validation Rules**:
- Source must be a valid medical condition
- Target must be a valid symptom or sign
- Frequency, specificity, and sensitivity should be specified

### 6. INDICATES
**Definition**: A sign or symptom indicates the presence of a condition.

**Domain**: symptom|sign|test_result (clinical finding, laboratory result)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- diagnostic_value: ["suggestive", "highly_suggestive", "pathognomonic"]
- positive_predictive_value: float (0.0-1.0)
- negative_predictive_value: float (0.0-1.0)

**Examples**:
- Elevated Troponin → Myocardial Infarction (diagnostic_value: highly_suggestive)
- Jaundice → Liver Disease (diagnostic_value: suggestive)
- Kussmaul Respiration → Diabetic Ketoacidosis (diagnostic_value: pathognomonic)

**Validation Rules**:
- Source must be a valid symptom, sign, or test result
- Target must be a valid medical condition
- Diagnostic value, positive predictive value, and negative predictive value should be specified

### 7. PRECEDES
**Definition**: One condition typically precedes another in temporal sequence.

**Domain**: condition (disease, disorder, syndrome)  
**Range**: condition (disease, disorder, syndrome)

**Properties**:
- temporal_gap: ["immediate", "days", "weeks", "months", "years"]
- causal_relationship: ["direct", "indirect", "associative"]
- frequency: ["rare", "occasional", "common", "almost_always"]

**Examples**:
- Impaired Glucose Tolerance → Type 2 Diabetes (temporal_gap: years, causal_relationship: direct)
- Barrett Esophagus → Esophageal Cancer (temporal_gap: years, causal_relationship: direct)
- Chronic Hepatitis → Cirrhosis (temporal_gap: years, causal_relationship: direct)

**Validation Rules**:
- Both source and target must be valid medical conditions
- Source and target should be different conditions
- Temporal gap and causal relationship should be specified

### 8. FINDING_SITE
**Definition**: Anatomical location where a clinical finding is present (SNOMED CT core relationship).

**Domain**: condition|finding (clinical finding, disorder, syndrome)  
**Range**: anatomical_structure (body structure, organ, tissue)

**Properties**:
- laterality: ["left", "right", "bilateral", "unilateral"]
- specificity: ["exact", "approximate", "regional"]
- primary_site: bool

**Examples**:
- Pneumonia → Lung (laterality: bilateral, primary_site: true)
- Myocardial Infarction → Heart (laterality: left, specificity: exact)
- Skin Rash → Upper Extremity (laterality: bilateral, specificity: regional)

### 9. CAUSATIVE_AGENT
**Definition**: Agent that causes or contributes to a clinical condition (SNOMED CT core relationship).

**Domain**: condition|finding (clinical finding, disorder, syndrome)  
**Range**: organism|substance|event (bacteria, virus, chemical, trauma)

**Properties**:
- causation_type: ["infectious", "toxic", "genetic", "environmental", "iatrogenic"]
- evidence_level: ["A", "B", "C", "D", "E"]
- prevalence: float (0.0-1.0)

**Examples**:
- Pneumonia → Streptococcus pneumoniae (causation_type: infectious, evidence_level: A)
- Lung Cancer → Cigarette Smoke (causation_type: toxic, evidence_level: A)
- Diabetes Mellitus → Genetic Predisposition (causation_type: genetic, evidence_level: B)

### 10. SEVERITY
**Definition**: Severity level of a clinical condition (SNOMED CT core relationship).

**Domain**: condition|finding (clinical finding, disorder, syndrome)  
**Range**: severity_concept (mild, moderate, severe, etc.)

**Properties**:
- scale: ["mild", "moderate", "severe", "life_threatening", "fatal"]
- measurement_type: ["ordinal", "quantitative"]
- grading_system: str (e.g., "WHO", "CTCAE", "NYHA")

**Examples**:
- Hypertension → Moderate (scale: moderate, grading_system: JNC_8)
- Heart Failure → Class III (scale: severe, grading_system: NYHA)
- Diabetic Neuropathy → Severe (scale: severe, measurement_type: ordinal)

### 11. METHOD
**Definition**: Method by which a procedure is performed (SNOMED CT core relationship).

**Domain**: procedure|intervention (surgical procedure, diagnostic procedure)  
**Range**: action|technique (excision, ultrasound, endoscopy)

**Properties**:
- invasiveness: ["non_invasive", "minimally_invasive", "invasive"]
- approach: ["open", "laparoscopic", "endoscopic", "percutaneous"]
- complexity: ["simple", "moderate", "complex"]

**Examples**:
- Appendectomy → Excision (approach: open, invasiveness: invasive)
- Colonoscopy → Endoscopic Examination (approach: endoscopic, invasiveness: minimally_invasive)
- Echocardiogram → Ultrasound (approach: non_invasive, invasiveness: non_invasive)

### 12. PROCEDURE_SITE
**Definition**: Anatomical site where a procedure is performed (SNOMED CT core relationship).

**Domain**: procedure|intervention (surgical procedure, diagnostic procedure)  
**Range**: anatomical_structure (body structure, organ, tissue)

**Properties**:
- laterality: ["left", "right", "bilateral", "unilateral"]
- access_type: ["direct", "indirect", "remote"]
- primary_target: bool

**Examples**:
- Appendectomy → Appendix (laterality: right, access_type: direct)
- Coronary Angioplasty → Coronary Artery (laterality: left, access_type: remote)
- Knee Arthroscopy → Knee Joint (laterality: right, access_type: minimally_invasive)

### 13. CHARACTERIZES
**Definition**: What an observable entity or measurement characterizes (SNOMED CT core relationship).

**Domain**: observable|measurement (laboratory test, vital sign, assessment)  
**Range**: condition|property|quality (clinical condition, physiological property)

**Properties**:
- measurement_type: ["qualitative", "quantitative", "ordinal"]
- clinical_significance: ["diagnostic", "prognostic", "monitoring"]
- reference_range: str

**Examples**:
- Hemoglobin A1c → Glycemic Control (measurement_type: quantitative, clinical_significance: diagnostic)
- Blood Pressure → Cardiovascular Status (measurement_type: quantitative, reference_range: 90-120/60-80)
- Pain Scale → Pain Intensity (measurement_type: ordinal, clinical_significance: monitoring)

### 14. CASE_INFORMS_PLAN
**Definition**: Patient case (current state, history, risks) informs the clinical plan (decision-making and care processes) (FHIR-CPG conceptual architecture).

**Domain**: case (patient case, episode of care)  
**Range**: plan (clinical plan, decision logic)

**Properties**:
- case_features_used: list (case features considered in planning)
- plan_scope: ["comprehensive", "focused", "emergency"]
- decision_support: ["automated", "semi_automated", "manual"]

**Examples**:
- Diabetes Case → Diabetes Management Plan (case_features_used: ["hba1c", "complications"], plan_scope: comprehensive)
- Heart Failure Case → Heart Failure Plan (case_features_used: ["nyha_class", "ef"], decision_support: semi_automated)

**Validation Rules**:
- Source must be a valid patient case
- Target must be a valid clinical plan
- Case features used should be specified

### 15. PLAN_INSTANTIATES_CAREPLAN
**Definition**: Definitional clinical plan becomes instantiated as a patient-specific care plan (FHIR-CPG conceptual architecture).

**Domain**: plan (definitional plan, guideline plan)  
**Range**: careplan (patient-specific care plan)

**Properties**:
- instantiation_type: ["automatic", "prompted", "manual"]
- patient_specific_goals: list
- timeline: ["immediate", "short_term", "long_term"]

**Examples**:
- Diabetes Management Plan → John Doe Diabetes CarePlan (instantiation_type: automatic, timeline: long_term)
- Hypertension Plan → Jane Smith BP CarePlan (instantiation_type: prompted, patient_specific_goals: ["bp_control"])

**Validation Rules**:
- Source must be a definitional plan
- Target must be a patient-specific care plan
- Instantiation type should be specified

### 16. RECOMMENDATION_GENERATES_PROPOSAL
**Definition**: Clinical practice guideline recommendation becomes a patient-specific proposal in a care plan (FHIR-CPG).

**Domain**: recommendation (guideline recommendation)  
**Range**: proposal (patient-specific proposal)

**Properties**:
- applicability: ["applicable", "not_applicable", "conditional"]
- strength: ["strong", "weak", "conditional"]
- evidence_quality: ["high", "moderate", "low"]

**Examples**:
- Statin Recommendation → Atorvastatin Proposal (applicability: applicable, strength: strong)
- Metformin Recommendation → Metformin Proposal (applicability: conditional, evidence_quality: high)

**Validation Rules**:
- Source must be a guideline recommendation
- Target must be a patient-specific proposal
- Applicability and strength should be specified

### 17. PROPOSAL_GENERATES_REQUEST
**Definition**: Patient-specific proposal leads to a clinical request (order, prescription, referral) (FHIR-CPG).

**Domain**: proposal (patient-specific proposal)  
**Range**: request (clinical request, order)

**Properties**:
- request_type: ["medication", "procedure", "diagnostic", "referral", "lifestyle"]
- priority: ["routine", "urgent", "asap", "stat"]
- authorization_required: bool

**Examples**:
- Atorvastatin Proposal → Atorvastatin Prescription (request_type: medication, priority: routine)
- Colonoscopy Proposal → Colonoscopy Order (request_type: procedure, priority: urgent)

**Validation Rules**:
- Source must be a patient-specific proposal
- Target must be a clinical request
- Request type and priority should be specified

### 18. REQUEST_FULFILLED_BY_EVENT
**Definition**: Clinical request is fulfilled by a corresponding clinical event (administration, procedure, observation) (FHIR-CPG).

**Domain**: request (clinical request, order)  
**Range**: event (clinical event, procedure performed)

**Properties**:
- fulfillment_status: ["completed", "partially_completed", "cancelled", "failed"]
- timing: ["on_time", "delayed", "early"]
- outcome: ["successful", "unsuccessful", "complications"]

**Examples**:
- Atorvastatin Prescription → Atorvastatin Administration (fulfillment_status: completed, timing: on_time)
- Colonoscopy Order → Colonoscopy Procedure (fulfillment_status: completed, outcome: successful)

**Validation Rules**:
- Source must be a clinical request
- Target must be a clinical event
- Fulfillment status should be specified

### 19. STRATEGY_CONTAINS_RECOMMENDATION
**Definition**: Clinical strategy groups and coordinates multiple recommendations for a specific condition or clinical scenario (FHIR-CPG).

**Domain**: strategy (clinical strategy)  
**Range**: recommendation (guideline recommendation)

**Properties**:
- strategy_role: ["primary", "adjunct", "alternative", "sequential"]
- condition_focus: str
- coordination_type: ["parallel", "sequential", "conditional"]

**Examples**:
- Diabetes Management Strategy → Metformin Recommendation (strategy_role: primary, coordination_type: parallel)
- Heart Failure Strategy → ACE Inhibitor Recommendation (strategy_role: primary, condition_focus: heart_failure)

**Validation Rules**:
- Source must be a clinical strategy
- Target must be a guideline recommendation
- Strategy role should be specified

### 20. PATHWAY_CONTAINS_STRATEGY
**Definition**: Clinical pathway coordinates multiple strategies across the patient journey (FHIR-CPG).

**Domain**: pathway (clinical pathway)  
**Range**: strategy (clinical strategy)

**Properties**:
- pathway_phase: ["acute", "chronic", "preventive", "palliative"]
- temporal_sequence: ["initial", "followup", "maintenance", "end_of_life"]
- patient_state: ["stable", "unstable", "critical"]

**Examples**:
- Diabetes Pathway → Glycemic Control Strategy (pathway_phase: chronic, temporal_sequence: maintenance)
- Cancer Pathway → Chemotherapy Strategy (pathway_phase: acute, patient_state: unstable)

**Validation Rules**:
- Source must be a clinical pathway
- Target must be a clinical strategy
- Pathway phase should be specified

### 21. ACTIVITY_DEFINED_BY_DEFINITION
**Definition**: Clinical activity is defined by an ActivityDefinition specifying how it should be performed (FHIR-CPG).

**Domain**: activity (clinical activity)  
**Range**: activity_definition (activity definition)

**Properties**:
- activity_type: ["medication", "procedure", "communication", "assessment", "enrollment"]
- definition_scope: ["guideline", "institution", "protocol"]
- customization_allowed: bool

**Examples**:
- Medication Administration → Insulin Administration Definition (activity_type: medication, definition_scope: guideline)
- Patient Assessment → Diabetes Assessment Definition (activity_type: assessment, customization_allowed: true)

**Validation Rules**:
- Source must be a clinical activity
- Target must be an activity definition
- Activity type should be specified

### 22. PATIENT_ENROLLED_IN_PATHWAY
**Definition**: Patient is enrolled in a clinical pathway for management of their condition (FHIR-CPG).

**Domain**: patient (patient)  
**Range**: pathway (clinical pathway)

**Properties**:
- enrollment_type: ["automatic", "prompted", "manual", "patient_initiated"]
- enrollment_date: date
- exit_criteria: str

**Examples**:
- John Doe → Diabetes Management Pathway (enrollment_type: automatic, enrollment_date: 2024-01-15)
- Jane Smith → Heart Failure Pathway (enrollment_type: prompted, exit_criteria: ef_improved)

**Validation Rules**:
- Source must be a patient
- Target must be a clinical pathway
- Enrollment type should be specified

## Extended Relationship Types

### Treatment Relationships
- **PREVENTS**: Intervention prevents condition occurrence
- **MITIGATES**: Intervention mitigates symptom/sign
- **MANAGES**: Intervention manages chronic condition

### Diagnostic Relationships
- **DIAGNOSES**: Test diagnoses condition
- **SCREENS_FOR**: Test screens for condition
- **MONITORS**: Test monitors condition/treatment

### Pathophysiology Relationships
- **CAUSES**: Condition causes another condition
- **PREDISPOSES**: Condition predisposes to another condition
- **CO_OCCURS_WITH**: Conditions frequently co-occur

### Risk Relationships
- **PROTECTS_AGAINST**: Factor protects against condition
- **INCREASES_RISK**: Factor increases risk of condition
- **DECREASES_RISK**: Factor decreases risk of condition

### Anatomical Relationships
- **AFFECTS**: Condition affects anatomical structure
- **LOCATED_IN**: Condition located in anatomical structure
- **SPREADS_TO**: Condition spreads to anatomical structure

### Pharmacological Relationships
- **INTERACTS_WITH**: Drug interacts with drug/condition (symmetric)
- **CONTRAINDICATED_IN**: Drug contraindicated in condition
- **METABOLIZED_BY**: Drug metabolized by enzyme
- **INHIBITS**: Drug inhibits enzyme/pathway

### Clinical Presentation Relationships
- **PRESENTS_WITH**: Condition presents with symptom/sign
- **INDICATES**: Sign/symptom indicates condition
- **MANIFESTS_AS**: Condition manifests as sign/symptom

### Temporal Relationships
- **PRECEDES**: Condition typically precedes another
- **FOLLOWS**: Condition typically follows another
- **CO_OCCURS_WITH**: Conditions frequently co-occur

## Relationship Properties and Semantics

### Transitivity
- Most relationships are not transitive by default
- Some anatomical relationships may be transitive (e.g., AFFECTS)

### Symmetry
- INTERACTS_WITH is symmetric (A interacts with B ↔ B interacts with A)
- Most other relationships are directional

### Inverse Relationships
- Some relationships have defined inverses (e.g., TREATS inverse could be TREATED_BY)
- Inverses are not currently implemented but may be added for completeness

## Clinical Standards Alignment

The core relationships are designed to align with:
- **SNOMED CT**: Core semantic relationships (attributes) from the SNOMED CT Concept Model
- **HL7 FHIR**: Clinical reasoning and knowledge representation
- **Clinical Practice Guidelines**: Evidence-based medicine relationships

The implementation includes key SNOMED CT relationship types:
- **Clinical Finding domain**: finding site, causative agent, severity
- **Procedure domain**: method, procedure site
- **Observable Entity domain**: characterizes

These relationships enable Santiago to extract structured clinical knowledge that aligns with international clinical terminology standards.

## Implementation Notes

### Validation
- All relationships include validation rules
- Properties are type-checked where specified
- Domain and range constraints are enforced

### Extensibility
- New relationship types can be added following the RelationshipDefinition pattern
- Properties can be extended as needed
- Validation rules can be customized

### Usage in Santiago
- Layer 1 extraction identifies concepts and relationships from clinical text
- Relationships are stored with confidence scores and evidence
- Higher layers use these relationships for reasoning and decision support

## Future Enhancements

### Additional Relationship Types
Based on clinical standards review, potential additions include:
- **PRECEDES**: Condition typically precedes another
- **FOLLOWS**: Condition typically follows another
- **ASSOCIATED_WITH**: General association between concepts
- **INDICATES**: Sign/symptom indicates condition

### Temporal Relationships
- **TEMPORALLY_RELATED**: Concepts related in time
- **CAUSES_OVER_TIME**: Long-term causal relationships

### Probabilistic Relationships
- **INCREASES_PROBABILITY**: Factor increases probability of condition
- **DECREASES_PROBABILITY**: Factor decreases probability of condition

## Conclusion

The core semantic relationships provide a solid foundation for clinical knowledge representation in Santiago Layer 1. The twenty-two core relationships capture the most essential clinical relationships, including seven original Santiago relationships, six key SNOMED CT core relationship types, and nine FHIR-CPG clinical practice guideline relationships for comprehensive clinical knowledge extraction aligned with international standards.

This specification ensures consistency, validation, and extensibility for clinical knowledge extraction and representation across the full spectrum of clinical care from basic relationships to guideline-based care coordination.

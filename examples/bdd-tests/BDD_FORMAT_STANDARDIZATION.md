# Clinical BDD Test Format Standardization Analysis & Recommendations

## Executive Summary

After analyzing the 5 BDD test examples in `examples/bdd-tests/unsorted/`, I identified significant format inconsistencies and opportunities for standardization. The current examples use two distinct approaches: rich clinical scenarios vs. minimal reference-based scenarios. This analysis recommends a standardized format that separates human-readable clinical scenarios from technical FHIR structures.

## Current Format Analysis

### Format Categories Identified

#### 1. **Rich Clinical Format** (HFrEF Example)

- **Strengths**: Comprehensive clinical context, proper Gherkin scenarios, extensive metadata
- **File**: `1.1.2-treatment-recommendation-hfref-quadruple-therapy.feature`
- **Structure**: Detailed headers + full Gherkin scenarios with clinical logic

#### 2. **Reference-Based Format** (Most Examples)

- **Strengths**: Clean separation of concerns, references external validation
- **Files**: `JaniceDoe_BreastCancer.feature`, `JohnSmith_Diabetes_ASCVD.feature`, etc.
- **Structure**: Minimal Gherkin + external file references

### Key Inconsistencies

1. **Metadata Headers**: Inconsistent presence and structure
2. **Clinical Content**: Some rich, some minimal
3. **Gherkin Quality**: Varies from detailed scenarios to single test stubs
4. **File Organization**: Mixed approaches to supporting files
5. **ID Systems**: Multiple naming conventions

## Recommended Standardized Format

### Core Principles

1. **Separation of Concerns**: Human-readable clinical scenarios separate from technical FHIR structures
2. **Key-Value Clinical Inputs**: Use structured YAML for clinical data instead of embedded FHIR
3. **Progressive Detail**: Start with clinical intent, add technical validation separately
4. **Unique ID System**: Consistent, hierarchical ID structure
5. **Standardized Headers**: Consistent metadata format across all tests

### Proposed File Structure

```
examples/bdd-tests/scenarios/
├── {scenario-id}.yaml          # Clinical scenario definition (key-value pairs)
├── {scenario-id}.feature       # Human-readable BDD test
├── {scenario-id}.assert.yaml   # Validation assertions
└── {scenario-id}.expected.md   # Expected outputs (optional)
```

### 1. Clinical Scenario Definition (`{scenario-id}.yaml`)

**Purpose**: Human-readable clinical scenario with key-value pairs for all clinical inputs.

```yaml

```yaml
# Standard Clinical Scenario Header
scenario:
  id: "cardiology-hfref-quadruple-001"
  title: "Heart Failure with Reduced Ejection Fraction - Quadruple Therapy Initiation"
  domain: "cardiology"
  category: "treatment-recommendation"
  version: "1.0"
  created: "2025-11-08"
  author: "Clinical BDD Creator"
  guidelines:
    - "2022 AHA/ACC/HFSA Guideline for Heart Failure"
    - "URL: https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063"

# Clinical Context
clinical:
  patient:
    demographics:
      age: 65
      gender: "male"
      bmi: 28
    presentation:
      chief_complaint: "Shortness of breath on exertion"
      duration: "2 weeks"
      nyha_class: "II"
  diagnosis:
    primary: "Heart Failure with Reduced Ejection Fraction"
    lvef: 30
    etiology: "ischemic"
  vitals:
    blood_pressure: "118/72"
    heart_rate: 78
    respiratory_rate: 16
  labs:
    bnp: 850
    creatinine: 1.2
    egfr: 55
    potassium: 4.6
    hemoglobin: 13.5
  medications:
    current: []
    allergies: []
  comorbidities: []
  contraindications: []

# Expected Clinical Actions
expectations:
  recommendations:
    - type: "medication"
      drug_class: "ARNI"
      specific: "sacubitril/valsartan"
      dose: "49/51 mg twice daily"
      rationale: "First-line therapy for HFrEF"
    - type: "medication"
      drug_class: "beta-blocker"
      specific: "metoprolol succinate"
      dose: "12.5 mg daily, titrate up"
      rationale: "Evidence-based beta-blocker for HFrEF"
    - type: "medication"
      drug_class: "MRA"
      specific: "spironolactone"
      dose: "12.5 mg daily"
      rationale: "Mineralocorticoid receptor antagonist"
    - type: "medication"
      drug_class: "SGLT2i"
      specific: "dapagliflozin"
      dose: "10 mg daily"
      rationale: "Cardiorenal protection regardless of diabetes"
  monitoring:
    - type: "labs"
      frequency: "every 3-7 days initially"
      parameters: ["potassium", "creatinine", "egfr"]
    - type: "vitals"
      frequency: "at each visit"
      parameters: ["blood pressure", "weight"]
  education:
    - "Daily weight monitoring"
    - "Low sodium diet (<2g/day)"
    - "Exercise as tolerated"
    - "Symptom recognition and reporting"

# Test Metadata
testing:
  complexity: "advanced"
  fidelity: "high"
  priority: "P1"
  tags: ["guideline-adherent", "quadruple-therapy", "new-diagnosis"]
```

### 2. Human-Readable BDD Test (`{scenario-id}.feature`)

**Purpose**: Gherkin scenarios that directly represent clinical workflows.

```gherkin
# Clinical Scenario ID: cardiology-hfref-quadruple-001
# Title: Heart Failure with Reduced Ejection Fraction - Quadruple Therapy Initiation
# Domain: Cardiology | Category: Treatment Recommendation
# Guidelines: 2022 AHA/ACC/HFSA Heart Failure Guideline
# Complexity: Advanced | Fidelity: High | Priority: P1

Feature: Quadruple GDMT Initiation for Newly Diagnosed HFrEF

  As a clinical decision support system
  I want to ensure patients with newly diagnosed HFrEF receive all four foundational therapies
  So that mortality and hospitalization risk are reduced

  Background:
    Given a 65-year-old male with newly diagnosed HFrEF (LVEF 30%)
    And NYHA class II symptoms with BNP 850 pg/mL
    And no contraindications to GDMT (eGFR 55 mL/min, K+ 4.6 mEq/L)
    And no current heart failure medications

  Scenario: Complete quadruple therapy initiation during initial visit
    When evaluating treatment options for this patient
    Then recommend ARNI (sacubitril/valsartan 49/51 mg twice daily)
    And recommend evidence-based beta-blocker (metoprolol succinate 12.5 mg daily)
    And recommend MRA (spironolactone 12.5 mg daily with monitoring)
    And recommend SGLT2 inhibitor (dapagliflozin 10 mg daily)
    And provide patient education on lifestyle modifications

  Scenario: Alert for incomplete GDMT when SGLT2 inhibitor omitted
    Given a clinician ordered ARNI, beta-blocker, and MRA
    But omitted SGLT2 inhibitor without contraindication
    When finalizing the treatment plan
    Then alert that quadruple therapy is incomplete
    And recommend adding SGLT2 inhibitor as indicated

  Scenario: Appropriate monitoring plan for quadruple therapy
    When initiating quadruple GDMT
    Then schedule potassium and renal function monitoring in 3-7 days
    And schedule follow-up in 2 weeks for beta-blocker titration
    And educate patient on daily weight monitoring
```

### 3. Validation Assertions (`{scenario-id}.assert.yaml`)

**Purpose**: Technical validation rules using FHIRPath or other query languages.

```yaml
scenario_id: "cardiology-hfref-quadruple-001"
validation_level: "clinical-outcome"

assertions:
  # Medication Recommendations
  - id: "arni-recommended"
    description: "ARNI (sacubitril/valsartan) should be recommended"
    severity: "error"
    fhirpath: >
      entry.resource.ofType(MedicationRequest)
        .where(medication.coding.where(
          system='http://www.nlm.nih.gov/research/umls/rxnorm' and
          code='1731986'  # sacubitril/valsartan
        ).exists())
        .exists()
    expect: true

  - id: "beta-blocker-recommended"
    description: "Evidence-based beta-blocker should be recommended"
    severity: "error"
    fhirpath: >
      entry.resource.ofType(MedicationRequest)
        .where(medication.coding.where(
          system='http://www.nlm.nih.gov/research/umls/rxnorm' and
          (code='6918' or code='866924')  # metoprolol succinate
        ).exists())
        .exists()
    expect: true

  # Monitoring Requirements
  - id: "potassium-monitoring"
    description: "Potassium monitoring should be ordered"
    severity: "warning"
    fhirpath: >
      entry.resource.ofType(ServiceRequest)
        .where(code.coding.where(
          system='http://loinc.org' and
          code='2823-3'  # Potassium in Serum or Plasma
        ).exists())
        .exists()
    expect: true
```

## Unique ID System

### Hierarchical ID Structure
```
## Unique ID System

### Hierarchical ID Structure

```
{domain}-{category}-{condition}-{sequence}
```

**Components:**

- **domain**: cardiology, oncology, primary-care, emergency, etc.
- **category**: diagnosis, treatment-recommendation, monitoring, risk-assessment, etc.
- **condition**: hfref, diabetes, breast-cancer, etc.
- **sequence**: 001, 002, 003... (zero-padded)

**Examples:**

- `cardiology-treatment-hfref-001`
- `oncology-monitoring-breast-cancer-002`
- `primary-care-diagnosis-diabetes-001`

### ID Management Rules

1. **Uniqueness**: IDs must be globally unique across all scenarios
2. **Stability**: Once assigned, IDs should not change
3. **Hierarchy**: Domain → Category → Condition → Sequence
4. **Versioning**: Use semantic versioning for scenario updates
5. **Registration**: Maintain a central registry of assigned IDs
```

**Components:**
- **domain**: cardiology, oncology, primary-care, emergency, etc.
- **category**: diagnosis, treatment-recommendation, monitoring, risk-assessment, etc.
- **condition**: hfref, diabetes, breast-cancer, etc.
- **sequence**: 001, 002, 003... (zero-padded)

**Examples:**
- `cardiology-treatment-hfref-001`
- `oncology-monitoring-breast-cancer-002`
- `primary-care-diagnosis-diabetes-001`

### ID Management Rules
1. **Uniqueness**: IDs must be globally unique across all scenarios
2. **Stability**: Once assigned, IDs should not change
3. **Hierarchy**: Domain → Category → Condition → Sequence
4. **Versioning**: Use semantic versioning for scenario updates
5. **Registration**: Maintain a central registry of assigned IDs

## Implementation Guidelines for AI

### Scenario Generation Process

1. **Clinical Input Analysis**
   - Parse clinical scenario YAML for key parameters
   - Extract patient demographics, vitals, labs, history
   - Identify clinical context and guidelines

2. **Gherkin Scenario Creation**
   - Generate human-readable Given-When-Then scenarios
   - Focus on clinical decision points and outcomes
   - Include multiple scenarios per clinical situation

3. **Validation Rule Development**
   - Create FHIRPath assertions for key recommendations
   - Define monitoring requirements
   - Specify contraindication checks

4. **Quality Assurance**
   - Validate clinical accuracy against guidelines
   - Ensure Gherkin syntax correctness
   - Test assertion logic

### AI Training Recommendations

1. **Clinical Knowledge Base**
   - Access to current clinical guidelines
   - Understanding of standard clinical workflows
   - Knowledge of common clinical scenarios

2. **Format Consistency**
   - Strict adherence to YAML schema for clinical inputs
   - Standardized Gherkin scenario patterns
   - Consistent assertion structures

3. **Quality Metrics**
   - Clinical accuracy validation
   - Guideline adherence checking
   - Scenario completeness assessment

## Migration Plan

### Phase 1: Format Standardization

1. Convert existing examples to new format
2. Create YAML clinical scenario definitions
3. Update Gherkin scenarios for readability
4. Standardize assertion files

### Phase 2: ID System Implementation

1. Assign unique IDs to all scenarios
2. Create ID registry and management process
3. Update all references and cross-links

### Phase 3: Quality Enhancement

1. Clinical review of all scenarios
2. Guideline compliance verification
3. Testing and validation improvements

## Success Metrics

- **Consistency**: 100% of scenarios follow standardized format
- **Clinical Accuracy**: All scenarios verified against current guidelines
- **ID Uniqueness**: Zero ID conflicts across all scenarios
- **Maintainability**: Clear separation between clinical and technical concerns
- **Reusability**: Scenarios can be easily adapted for different testing contexts

## Recommendations for Agent Implementation

1. **Create conversion scripts** to migrate existing examples to new format
2. **Implement ID generation system** with conflict detection
3. **Build clinical scenario templates** for common patterns
4. **Develop validation tools** for format compliance
5. **Create documentation** for the new standard

This standardized approach will ensure consistency, maintainability, and clinical accuracy across all BDD test scenarios while clearly separating human-readable clinical content from technical implementation details.

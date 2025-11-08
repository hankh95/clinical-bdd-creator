# Standardized BDD Test Scenarios

This directory contains BDD test scenarios following the standardized format as defined in `../BDD_FORMAT_STANDARDIZATION.md`.

## Directory Structure

Each scenario consists of three files with a common scenario ID:

```
{scenario-id}.yaml          # Clinical scenario definition (key-value pairs)
{scenario-id}.feature       # Human-readable BDD test (Gherkin)
{scenario-id}.assert.yaml   # Validation assertions (FHIRPath)
```

## Scenario ID Format

Scenario IDs follow a hierarchical structure:

```
{domain}-{category}-{condition}-{sequence}
```

**Components:**
- **domain**: Clinical domain (e.g., `cardiology`, `oncology`, `primary-care`, `emergency`)
- **category**: Scenario category (e.g., `treatment-recommendation`, `diagnosis`, `monitoring`, `risk-assessment`)
- **condition**: Medical condition (e.g., `hfref`, `afib`, `diabetes`, `breast-cancer`)
- **sequence**: Sequential number (e.g., `001`, `002`, `003`)

**Examples:**
- `cardiology-treatment-hfref-001` - First heart failure treatment scenario
- `oncology-treatment-breast-cancer-001` - First breast cancer treatment scenario
- `primary-care-treatment-diabetes-001` - First diabetes treatment scenario

## Current Scenarios

### Cardiology

#### cardiology-treatment-hfref-001
**Title:** Heart Failure with Reduced Ejection Fraction - Quadruple Therapy Initiation  
**Guidelines:** 2022 AHA/ACC/HFSA Heart Failure Guideline  
**Complexity:** Advanced | **Fidelity:** High | **Priority:** P1  
**Description:** Comprehensive GDMT initiation for newly diagnosed HFrEF with all four foundational therapies (ARNI, beta-blocker, MRA, SGLT2i).

#### cardiology-treatment-afib-001
**Title:** Atrial Fibrillation with COPD and Obesity - Anticoagulation and Rate Control  
**Guidelines:** AHA/ACC/HRS Atrial Fibrillation Management Guidelines  
**Complexity:** Expert | **Fidelity:** High | **Priority:** P2  
**Description:** AFib management with multiple comorbidities requiring specialized anticoagulation and rate control strategies.

### Primary Care

#### primary-care-treatment-diabetes-001
**Title:** Type 2 Diabetes with ASCVD - Cardioprotective Therapy Initiation  
**Guidelines:** ADA 2025 Standards of Care in Diabetes - Section 9  
**Complexity:** Advanced | **Fidelity:** Medium | **Priority:** P2  
**Description:** T2DM management emphasizing cardioprotective agents (SGLT2i/GLP-1 RA) for patients with established ASCVD.

### Oncology

#### oncology-treatment-breast-cancer-001
**Title:** Stage II Breast Cancer - Anthracycline-Based Chemotherapy Cycle 1  
**Guidelines:** NCCN Breast Cancer Guidelines  
**Complexity:** Advanced | **Fidelity:** Medium | **Priority:** P2  
**Description:** Adjuvant chemotherapy management with comprehensive monitoring for hematologic toxicity and supportive care.

#### oncology-treatment-prostate-cancer-001
**Title:** Metastatic Castration-Resistant Prostate Cancer - Docetaxel Chemotherapy  
**Guidelines:** NCCN/AUA Prostate Cancer Guidelines, SWOG 0421 Trial  
**Complexity:** Expert | **Fidelity:** High | **Priority:** P2  
**Description:** Advanced prostate cancer management with chemotherapy and bone protection for patients with bone metastases.

## File Format Specifications

### 1. Clinical Scenario YAML (`{scenario-id}.yaml`)

**Purpose:** Human-readable clinical scenario with key-value pairs for all clinical inputs.

**Key Sections:**
- `scenario`: Metadata (ID, title, domain, category, guidelines)
- `clinical`: Clinical context (patient, diagnosis, vitals, labs, medications, comorbidities)
- `expectations`: Expected actions (recommendations, monitoring, education, alerts)
- `testing`: Test metadata (complexity, fidelity, priority, tags, decision points)
- `source`: Source mapping and migration information

**Key Principles:**
- Use key-value pairs for clinical data (NOT embedded FHIR)
- Human-readable and clinically focused
- Separate from technical FHIR structures
- Complete clinical context for scenario understanding

### 2. Gherkin Feature File (`{scenario-id}.feature`)

**Purpose:** Human-readable BDD tests representing clinical workflows.

**Structure:**
- Header comments with metadata
- Feature description with As-I want-So that format
- Background section with scenario setup
- Multiple scenarios covering different clinical situations
- Given-When-Then steps in plain clinical language

**Key Principles:**
- Multiple scenarios per feature (not just one stub)
- Focus on clinical decision points
- Human-readable language (avoid technical jargon)
- Cover positive cases, edge cases, and alerts

### 3. Assertions YAML (`{scenario-id}.assert.yaml`)

**Purpose:** Technical validation rules using FHIRPath expressions.

**Key Sections:**
- `scenario_id`: Reference to scenario
- `validation_level`: Type of validation (e.g., clinical-outcome)
- `guideline`: Reference to clinical guideline
- `assertions`: Array of validation rules
- `contraindications`: Array of safety checks

**Assertion Structure:**
```yaml
- id: unique-assertion-id
  description: Human-readable description
  severity: error|warning|info
  fhirpath: FHIRPath expression
  expect: true|false
  rationale: Clinical reasoning
```

## Creating New Scenarios

### Option 1: Use Conversion Script

```bash
python convert_to_standardized_format.py \
  --input path/to/original.feature \
  --output scenarios/ \
  --domain cardiology \
  --category treatment-recommendation \
  --condition afib
```

Or use interactive mode:

```bash
python convert_to_standardized_format.py \
  --input path/to/original.feature \
  --output scenarios/ \
  --interactive
```

### Option 2: Manual Creation

1. **Determine Scenario ID:**
   - Choose domain, category, and condition
   - Check existing IDs to determine next sequence number
   - Format: `{domain}-{category}-{condition}-{sequence}`

2. **Create Clinical YAML:**
   - Use existing scenarios as templates
   - Fill in all clinical details with key-value pairs
   - Separate clinical content from FHIR technical details

3. **Write Gherkin Scenarios:**
   - Create multiple scenarios covering clinical workflows
   - Use plain, human-readable language
   - Focus on clinical decision points and expected outcomes

4. **Define Assertions:**
   - Create FHIRPath expressions for technical validation
   - Include both positive assertions and contraindication checks
   - Document rationale for each assertion

5. **Review and Validate:**
   - Verify clinical accuracy against guidelines
   - Ensure Gherkin syntax correctness
   - Test FHIRPath expressions if possible

## Quality Checklist

Before finalizing a new scenario:

- [ ] Scenario ID follows hierarchical format and is unique
- [ ] Clinical YAML contains complete key-value pairs (no embedded FHIR)
- [ ] Gherkin feature has multiple scenarios covering different cases
- [ ] All scenarios use clear, human-readable clinical language
- [ ] Assertions file has comprehensive FHIRPath validation rules
- [ ] All TODOs have been resolved
- [ ] Clinical accuracy verified against current guidelines
- [ ] Guideline references are complete and accurate
- [ ] Source mapping documents original file location

## Migration from Unsorted

Scenarios in `../unsorted/` can be migrated to this standardized format:

1. Identify domain, category, and condition
2. Generate unique scenario ID
3. Extract clinical details and convert to key-value format
4. Create human-readable Gherkin scenarios (expand beyond simple stubs)
5. Adapt assertions to standardized format
6. Document source mapping

Original files can remain in `unsorted/` for reference.

## Guidelines Referenced

- **Cardiology:**
  - 2022 AHA/ACC/HFSA Heart Failure Guideline
  - AHA/ACC/HRS Atrial Fibrillation Management Guidelines

- **Primary Care:**
  - ADA 2025 Standards of Care in Diabetes

- **Oncology:**
  - NCCN Breast Cancer Guidelines
  - NCCN/AUA Prostate Cancer Guidelines
  - SWOG Clinical Trial Protocols

## Contributing

When adding new scenarios:

1. Follow the standardized format strictly
2. Use the conversion script or templates provided
3. Ensure clinical accuracy and guideline adherence
4. Include comprehensive test coverage
5. Document all clinical decision points
6. Update this README with new scenario details

## Questions?

Refer to:
- `../BDD_FORMAT_STANDARDIZATION.md` - Complete specification
- `../README.md` - General BDD testing documentation
- `convert_to_standardized_format.py` - Conversion script documentation

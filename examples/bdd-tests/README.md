# BDD Test Examples

This folder contains example BDD test scenarios demonstrating the Clinical BDD Creator system.

## Organization Structure

Examples are organized in multiple ways to support different use cases:

### Standardized Format (`scenarios/`)
**PRIMARY ORGANIZATION** - All new scenarios should use this standardized format:
- **scenarios/** - Standardized BDD tests following the format defined in `BDD_FORMAT_STANDARDIZATION.md`
  - Each scenario has 3 files: clinical YAML, Gherkin feature, and assertions YAML
  - Uses hierarchical ID system: `{domain}-{category}-{condition}-{sequence}`
  - Separates clinical content (key-value pairs) from technical FHIR structures
  - Human-readable Gherkin scenarios with multiple test cases per feature
  - See `scenarios/README.md` for complete documentation

### Legacy Organization (Deprecated)

The following organizational structures are maintained for backwards compatibility but should not be used for new scenarios:

#### 1. By Clinical Domain (`by-domain/`)
Organized by clinical specialty for domain-specific browsing:
- **cardiology/** - Cardiovascular conditions (HFrEF, atrial fibrillation)
- **oncology/** - Cancer care scenarios (prostate, breast)
- **primary-care/** - Primary care conditions (diabetes with ASCVD)

#### 2. By Generation Mode (`by-mode/`)
Organized by complexity level:
- **basic/** - Simple scenarios with few steps (gap: needs examples)
- **advanced/** - Multi-step clinical workflows (3 examples)
- **expert/** - Complex decision support with multiple considerations (2 examples)

#### 3. By Fidelity Level (`by-fidelity/`)
Organized by level of detail and realism:
- **low/** - Basic clinical concepts without specific details (gap: needs examples)
- **medium/** - Realistic patient scenarios with standard data (2 examples)
- **high/** - Comprehensive scenarios with detailed context (3 examples)

## File Naming Convention

Pattern: `{domain}-{mode}-{fidelity}-{condition}-{id}.feature`

Examples:
- `cardiology-advanced-high-hfref-001.feature` - Heart failure with detailed protocol
- `oncology-expert-high-prostate-001.feature` - Metastatic prostate cancer
- `primary-care-advanced-medium-diabetes-001.feature` - Diabetes with ASCVD

## Standardized Format Examples (Current)

All examples now in `scenarios/` directory following the standardized format:

### Cardiology Examples
1. **cardiology-treatment-hfref-001** - Heart Failure with Reduced Ejection Fraction
   - Quadruple GDMT therapy initiation (sacubitril/valsartan, metoprolol, spironolactone, dapagliflozin)
   - Alert system for incomplete guideline-directed medical therapy
   - Based on 2022 AHA/ACC/HFSA guidelines
   - **Format:** 3 files (clinical YAML, feature, assertions)

2. **cardiology-treatment-afib-001** - Atrial Fibrillation with Comorbidities
   - Complex scenario with AFib, COPD, and obesity
   - Anticoagulation strategy (DOAC) with bleeding risk assessment
   - Rate control considering COPD (diltiazem vs beta-blockers)
   - **Format:** 3 files (clinical YAML, feature, assertions)

### Primary Care Examples
3. **primary-care-treatment-diabetes-001** - Type 2 Diabetes with ASCVD
   - Newly diagnosed T2DM (HbA1c 8.5%) with history of MI
   - Cardioprotective medication selection (SGLT2i or GLP-1 agonist priority)
   - Risk stratification and glycemic goal management
   - **Format:** 3 files (clinical YAML, feature, assertions)

### Oncology Examples
4. **oncology-treatment-breast-cancer-001** - Breast Cancer Chemotherapy
   - Stage II breast cancer, cycle 1 anthracycline-based therapy
   - Doxorubicin with 21-day cycles
   - Comprehensive toxicity monitoring (CBC, ANC, LFTs, renal function)
   - **Format:** 3 files (clinical YAML, feature, assertions)

5. **oncology-treatment-prostate-cancer-001** - Metastatic Castration-Resistant Prostate Cancer
   - Advanced prostate cancer with bone metastases
   - Clinical trial enrollment (SWOG 0421)
   - Docetaxel chemotherapy with bone protection (zoledronic acid)
   - **Format:** 3 files (clinical YAML, feature, assertions)

## Legacy Examples (Deprecated)

The following examples exist in the legacy organizational structure but are superseded by the standardized format versions in `scenarios/`:

### Cardiology Examples
1. **cardiology-advanced-high-hfref-001** (Legacy)
   - Heart failure with reduced ejection fraction
   - Now superseded by `scenarios/cardiology-treatment-hfref-001`

2. **cardiology-expert-high-afib-001** (Legacy)
   - Atrial fibrillation with comorbidities
   - Now superseded by `scenarios/cardiology-treatment-afib-001`

### Oncology Examples
3. **oncology-expert-high-prostate-001** (Legacy)
   - Metastatic castration-resistant prostate cancer
   - Now superseded by `scenarios/oncology-treatment-prostate-cancer-001`

4. **oncology-advanced-medium-breast-001** (Legacy)
   - Breast cancer chemotherapy
   - Now superseded by `scenarios/oncology-treatment-breast-cancer-001`

### Primary Care Examples
5. **primary-care-advanced-medium-diabetes-001** (Legacy)
   - Type 2 diabetes with ASCVD
   - Now superseded by `scenarios/primary-care-treatment-diabetes-001`

## Standardized Format File Structure

Each standardized scenario consists of 3 files:

### 1. Clinical YAML (`{scenario-id}.yaml`)
- **Purpose:** Human-readable clinical scenario with key-value pairs
- **Content:** Patient demographics, clinical context, diagnosis, labs, medications, expected actions
- **Key Principle:** Separates clinical content from technical FHIR structures

### 2. Gherkin Feature (`{scenario-id}.feature`)
- **Purpose:** Human-readable BDD test representing clinical workflows
- **Content:** Multiple Given-When-Then scenarios covering different clinical situations
- **Key Principle:** Focus on clinical decision points, not technical implementation

### 3. Assertions YAML (`{scenario-id}.assert.yaml`)
- **Purpose:** Technical validation rules using FHIRPath expressions
- **Content:** Assertions for recommendations, monitoring, contraindications
- **Key Principle:** Technical validation separate from clinical narrative

## Legacy File Structure (Deprecated)

Legacy examples may include:
- `.feature` - Gherkin BDD scenario (required)
- `.assert.yaml` - FHIRPath assertions for validation
- `.fsh` - FHIR Shorthand patient data
- `.yaml` - Case metadata and expected outputs
- `.expected.md` - Expected markdown output
- `.expected.fsh` - Expected FHIR Shorthand output

## Coverage Gaps

Based on current analysis:
- **Basic mode examples needed** - Simple, single-condition scenarios
- **Low fidelity examples needed** - Simplified concept-validation scenarios
- **Additional domains** - Emergency medicine, pediatrics, psychiatry, etc.

## Usage

These examples serve multiple purposes:
1. **Validation** - Verify system generates clinically accurate BDD scenarios
2. **Training** - Provide reference for AI model fine-tuning
3. **Demonstration** - Show stakeholders how guidelines translate to tests
4. **Testing** - Validate FHIR resource generation and clinical logic
5. **Standards** - Demonstrate the standardized format for new scenarios

## Creating New Examples

**All new scenarios must follow the standardized format:**

1. **Use the conversion script:**
   ```bash
   python convert_to_standardized_format.py \
     --input unsorted/example.feature \
     --output scenarios/ \
     --domain cardiology \
     --category treatment-recommendation \
     --condition afib
   ```

2. **Or create manually following the template in `scenarios/README.md`**

3. **Key requirements:**
   - Create all 3 files (clinical YAML, feature, assertions)
   - Use hierarchical ID: `{domain}-{category}-{condition}-{sequence}`
   - Register ID in `scenarios/ID_REGISTRY.md`
   - Separate clinical content from FHIR technical details
   - Include multiple Gherkin scenarios per feature
   - Cite authoritative clinical guidelines
   - Ensure clinical accuracy

4. **Do NOT use legacy organizational structures** (`by-domain/`, `by-mode/`, `by-fidelity/`)

## Adding New Examples (Deprecated)

When contributing new examples:
1. Review existing examples for style and structure
2. Add clinical context comments at the top of .feature files
3. Follow the naming convention: `{domain}-{mode}-{fidelity}-{condition}-{id}`
4. Place files in all three organizational folders (by-domain, by-mode, by-fidelity)
5. Include relevant assertion and supporting files
6. Update README files in each organizational folder
7. Ensure clinical accuracy and cite guidelines

## Documentation

- **`scenarios/README.md`** - Complete documentation of the standardized format
- **`scenarios/ID_REGISTRY.md`** - Central registry of all scenario IDs
- **`BDD_FORMAT_STANDARDIZATION.md`** - Full specification and examples
- **`convert_to_standardized_format.py`** - Script to convert legacy examples
- **`COVERAGE_ANALYSIS.md`** - Coverage analysis (legacy)

## Migration from Legacy Format

If you have existing examples in the legacy format:

1. Use the conversion script: `convert_to_standardized_format.py`
2. Manually enhance the generated templates with clinical details
3. Expand Gherkin scenarios beyond simple stubs
4. Register the new ID in `scenarios/ID_REGISTRY.md`
5. Original files can remain in `unsorted/` for reference

## Clinical Accuracy

All examples should:
- Cite authoritative clinical guidelines (AHA, ACC, ADA, NCCN, etc.)
- Use correct medical terminology and coding systems (ICD-10, SNOMED, LOINC, RxNorm)
- Follow current standards of care
- Include appropriate contraindications and safety considerations
- Reflect realistic clinical workflows

# BDD Test Examples

This folder contains example BDD test scenarios demonstrating the Clinical BDD Creator system.

## Organization Structure

Examples are organized in three complementary ways to support different use cases:

### 1. By Clinical Domain (`by-domain/`)
Organized by clinical specialty for domain-specific browsing:
- **cardiology/** - Cardiovascular conditions (HFrEF, atrial fibrillation)
- **oncology/** - Cancer care scenarios (prostate, breast)
- **primary-care/** - Primary care conditions (diabetes with ASCVD)

### 2. By Generation Mode (`by-mode/`)
Organized by complexity level:
- **basic/** - Simple scenarios with few steps (gap: needs examples)
- **advanced/** - Multi-step clinical workflows (3 examples)
- **expert/** - Complex decision support with multiple considerations (2 examples)

### 3. By Fidelity Level (`by-fidelity/`)
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

## Current Examples

### Cardiology Examples
1. **cardiology-advanced-high-hfref-001** - Heart Failure with Reduced Ejection Fraction
   - Quadruple GDMT therapy initiation (sacubitril/valsartan, metoprolol, spironolactone, dapagliflozin)
   - Alert system for incomplete guideline-directed medical therapy
   - Based on 2022 AHA/ACC/HFSA guidelines

2. **cardiology-expert-high-afib-001** - Atrial Fibrillation with Comorbidities
   - Complex scenario with AFib, COPD, and obesity
   - Anticoagulation strategy (DOAC) with bleeding risk assessment
   - Rate control considering COPD (diltiazem vs beta-blockers)

### Oncology Examples
3. **oncology-expert-high-prostate-001** - Metastatic Castration-Resistant Prostate Cancer
   - Advanced prostate cancer with bone metastases
   - Clinical trial enrollment (SWOG 0421)
   - Docetaxel chemotherapy with bone protection (zoledronic acid)

4. **oncology-advanced-medium-breast-001** - Breast Cancer Chemotherapy
   - Stage II breast cancer, cycle 1 anthracycline-based therapy
   - Doxorubicin with 21-day cycles
   - Comprehensive toxicity monitoring (CBC, ANC, LFTs, renal function)

### Primary Care Examples
5. **primary-care-advanced-medium-diabetes-001** - Type 2 Diabetes with ASCVD
   - Newly diagnosed T2DM (HbA1c 8.5%) with history of MI
   - Cardioprotective medication selection (SGLT2i or GLP-1 agonist priority)
   - Risk stratification and glycemic goal management

## Associated Files

Each example may include:
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

## Adding New Examples

When contributing new examples:
1. Review existing examples for style and structure
2. Add clinical context comments at the top of .feature files
3. Follow the naming convention: `{domain}-{mode}-{fidelity}-{condition}-{id}`
4. Place files in all three organizational folders (by-domain, by-mode, by-fidelity)
5. Include relevant assertion and supporting files
6. Update README files in each organizational folder
7. Ensure clinical accuracy and cite guidelines

## Clinical Accuracy

All examples should:
- Cite authoritative clinical guidelines (AHA, ACC, ADA, NCCN, etc.)
- Use correct medical terminology and coding systems (ICD-10, SNOMED, LOINC, RxNorm)
- Follow current standards of care
- Include appropriate contraindications and safety considerations
- Reflect realistic clinical workflows

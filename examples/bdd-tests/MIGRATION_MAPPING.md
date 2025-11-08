# Migration Mapping: Unsorted to Standardized Format

This document tracks the conversion of scenarios from the `unsorted/` directory to the standardized format in `scenarios/`.

## Conversion Summary

| Original File | New Scenario ID | Status | Date |
|---------------|----------------|--------|------|
| `1.1.2-treatment-recommendation-hfref-quadruple-therapy.feature` | `cardiology-treatment-hfref-001` | ✅ Complete | 2025-11-08 |
| `RobertJohnson_Afib_CPOE_Obese.*` | `cardiology-treatment-afib-001` | ✅ Complete | 2025-11-08 |
| `JohnSmith_Diabetes_ASCVD.*` | `primary-care-treatment-diabetes-001` | ✅ Complete | 2025-11-08 |
| `JaniceDoe_BreastCancer.*` | `oncology-treatment-breast-cancer-001` | ✅ Complete | 2025-11-08 |
| `2011_AdamEveryman_Prostate_Cancer_GrokFromPDF.*` | `oncology-treatment-prostate-cancer-001` | ✅ Complete | 2025-11-08 |

## Conversion Details

### 1. HFrEF Quadruple Therapy

**Original:** `1.1.2-treatment-recommendation-hfref-quadruple-therapy.feature`
**New ID:** `cardiology-treatment-hfref-001`

**Changes:**
- Preserved rich clinical format from original
- Created clinical YAML with key-value pairs for patient data
- Expanded Gherkin scenarios from 2 to 5 comprehensive scenarios
- Created standardized assertions with FHIRPath expressions
- Maintained clinical accuracy per 2022 AHA/ACC/HFSA guidelines

**Files Created:**
- `scenarios/cardiology-treatment-hfref-001.yaml` (5.4 KB)
- `scenarios/cardiology-treatment-hfref-001.feature` (4.3 KB)
- `scenarios/cardiology-treatment-hfref-001.assert.yaml` (7.3 KB)

### 2. AFib with COPD and Obesity

**Original:** `RobertJohnson_Afib_CPOE_Obese.*`
**New ID:** `cardiology-treatment-afib-001`

**Changes:**
- Extracted clinical details from original .yaml notes section
- Created structured clinical YAML with demographics, comorbidities, and treatment plans
- Expanded from reference-based stub to 7 comprehensive Gherkin scenarios
- Created detailed assertions covering anticoagulation, rate control, and monitoring
- Added contraindication checks for beta-blockers with COPD

**Files Created:**
- `scenarios/cardiology-treatment-afib-001.yaml` (6.1 KB)
- `scenarios/cardiology-treatment-afib-001.feature` (4.6 KB)
- `scenarios/cardiology-treatment-afib-001.assert.yaml` (7.5 KB)

### 3. Type 2 Diabetes with ASCVD

**Original:** `JohnSmith_Diabetes_ASCVD.*`
**New ID:** `primary-care-treatment-diabetes-001`

**Changes:**
- Extracted clinical context from original .assert.yaml summary
- Created clinical YAML emphasizing cardioprotective therapy per ADA 2025
- Expanded from reference stub to 8 comprehensive Gherkin scenarios
- Created assertions focusing on SGLT2i/GLP-1 RA recommendations
- Added contraindications for renal function and SGLT2i use

**Files Created:**
- `scenarios/primary-care-treatment-diabetes-001.yaml` (6.2 KB)
- `scenarios/primary-care-treatment-diabetes-001.feature` (5.4 KB)
- `scenarios/primary-care-treatment-diabetes-001.assert.yaml` (7.7 KB)

### 4. Breast Cancer Chemotherapy

**Original:** `JaniceDoe_BreastCancer.*`
**New ID:** `oncology-treatment-breast-cancer-001`

**Changes:**
- Extracted clinical context from original .assert.yaml summary
- Created clinical YAML with chemotherapy cycle details and monitoring plans
- Expanded from reference stub to 10 comprehensive Gherkin scenarios
- Created assertions for chemotherapy orders, monitoring, and risk assessments
- Added contraindications for adequate baseline counts and organ function

**Files Created:**
- `scenarios/oncology-treatment-breast-cancer-001.yaml` (6.9 KB)
- `scenarios/oncology-treatment-breast-cancer-001.feature` (5.6 KB)
- `scenarios/oncology-treatment-breast-cancer-001.assert.yaml` (8.0 KB)

### 5. Metastatic Prostate Cancer

**Original:** `2011_AdamEveryman_Prostate_Cancer_GrokFromPDF.*`
**New ID:** `oncology-treatment-prostate-cancer-001`

**Changes:**
- Extracted clinical context from original .yaml notes section
- Created clinical YAML with mCRPC details, trial enrollment, and treatment plans
- Expanded from reference stub to 12 comprehensive Gherkin scenarios
- Created assertions for docetaxel, prednisone, zoledronic acid, and monitoring
- Added contraindications for adequate counts, renal function, and performance status

**Files Created:**
- `scenarios/oncology-treatment-prostate-cancer-001.yaml` (7.0 KB)
- `scenarios/oncology-treatment-prostate-cancer-001.feature` (6.5 KB)
- `scenarios/oncology-treatment-prostate-cancer-001.assert.yaml` (9.3 KB)

## Format Improvements

### Key-Value Clinical Data

**Before:** Clinical data was either:
- Embedded in FHIR structures (FSH files)
- Described in narrative notes
- Referenced from external fixtures

**After:**
- Structured key-value pairs in YAML
- Human-readable clinical terminology
- Separated from technical FHIR implementation
- Complete clinical context in one file

### Gherkin Scenarios

**Before:**
- Often single reference-based stub: "Execute guideline logic and validate clinical intent"
- Minimal Given-When-Then structure
- Technical fixture references

**After:**
- Multiple (5-12) comprehensive scenarios per feature
- Clinical decision points clearly articulated
- Human-readable Given-When-Then steps
- Covers positive cases, edge cases, and alerts
- Focuses on clinical workflows, not technical implementation

### Assertions

**Before:**
- Mixed format in .assert.yaml
- Some FHIRPath, some text-based
- Inconsistent structure

**After:**
- Standardized structure with id, description, severity, fhirpath, expect, rationale
- Separate sections for assertions and contraindications
- Comprehensive coverage of recommendations and safety checks

## Unique ID System

All scenarios now use hierarchical IDs:

```
{domain}-{category}-{condition}-{sequence}
```

**Domains Used:**
- `cardiology` - Cardiovascular scenarios
- `primary-care` - Primary care scenarios
- `oncology` - Cancer scenarios

**Categories Used:**
- `treatment-recommendation` - All 5 scenarios focus on treatment decisions

**Conditions Used:**
- `hfref` - Heart failure with reduced ejection fraction
- `afib` - Atrial fibrillation
- `diabetes` - Type 2 diabetes
- `breast-cancer` - Breast cancer
- `prostate-cancer` - Prostate cancer

**Sequences:**
- All start with `001` as first scenario for each domain-category-condition combination

## Original Files

Original files remain in `unsorted/` for reference and can be:
- Kept as historical reference
- Used for comparison and validation
- Removed in future cleanup if no longer needed

The unsorted directory README has been updated to note that these files have been processed and organized.

## Quality Metrics

### Scenario Completeness

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Average Gherkin scenarios per feature | 1.0 | 8.4 | +740% |
| Clinical YAML files | 2 partial | 5 complete | +150% |
| Assertions with rationale | ~50% | 100% | +100% |
| Contraindication checks | Minimal | Comprehensive | Significant |

### File Size Comparison

| Type | Original Avg | New Avg | Change |
|------|-------------|---------|--------|
| Feature files | 0.6 KB | 5.3 KB | +783% |
| Clinical data | Embedded | 6.4 KB | New |
| Assertions | 3.5 KB | 8.0 KB | +129% |

The increased size reflects significantly more comprehensive clinical content and test coverage.

## Tools Created

1. **Conversion Script:** `convert_to_standardized_format.py`
   - Automates generation of 3-file structure
   - Interactive and command-line modes
   - Template generation with TODO placeholders

2. **ID Registry:** `scenarios/ID_REGISTRY.md`
   - Central tracking of all scenario IDs
   - Prevents conflicts
   - Documents creation dates and guidelines

3. **Documentation:** `scenarios/README.md`
   - Complete format specification
   - Examples and templates
   - Quality checklist

## Validation

All converted scenarios have been validated for:
- ✅ Clinical accuracy against referenced guidelines
- ✅ Unique ID assignment with no conflicts
- ✅ Complete 3-file structure (YAML, feature, assertions)
- ✅ Separation of clinical content from FHIR technical details
- ✅ Multiple comprehensive Gherkin scenarios
- ✅ Standardized assertion structure with rationale
- ✅ Contraindication checks included

## Next Steps

With the standardization complete:

1. **Future Scenarios:** Use `convert_to_standardized_format.py` or manual templates
2. **ID Management:** Always update `ID_REGISTRY.md` when creating new scenarios
3. **Legacy Cleanup:** Consider archiving or removing old organizational structures
4. **Expansion:** Add scenarios for additional domains and conditions
5. **Integration:** Use standardized format for all BDD test generation

## References

- **Specification:** `../BDD_FORMAT_STANDARDIZATION.md`
- **Conversion Script:** `convert_to_standardized_format.py`
- **New Scenarios:** `scenarios/` directory
- **ID Registry:** `scenarios/ID_REGISTRY.md`
- **Documentation:** `scenarios/README.md`

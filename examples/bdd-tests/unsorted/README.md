# Unsorted BDD Test Examples (Staging Area)

## Purpose

This folder serves as a staging area for new BDD test examples before they are reviewed, validated, and organized into the structured folders (`by-domain/`, `by-mode/`, `by-fidelity/`).

## Current Contents

The following examples have already been processed and organized:
- ✅ `1.1.2-treatment-recommendation-hfref-quadruple-therapy.feature` → `cardiology-advanced-high-hfref-001`
- ✅ `2011_AdamEveryman_Prostate_Cancer_GrokFromPDF.*` → `oncology-expert-high-prostate-001`
- ✅ `JaniceDoe_BreastCancer.*` → `oncology-advanced-medium-breast-001`
- ✅ `JohnSmith_Diabetes_ASCVD.*` → `primary-care-advanced-medium-diabetes-001`
- ✅ `RobertJohnson_Afib_CPOE_Obese.*` → `cardiology-expert-high-afib-001`

These files remain here as originals and can be used as reference or removed in future cleanup.

## Workflow for New Examples

When adding new BDD test examples to this repository:

### 1. Initial Placement
Place new examples in this `unsorted/` folder with their original naming:
- `.feature` file (required)
- `.assert.yaml` file (assertions for validation)
- `.fsh` file (FHIR Shorthand patient data, if applicable)
- `.yaml` file (case metadata, if applicable)
- `.expected.*` files (expected outputs, if applicable)

### 2. Review Process
Before organizing, review each example for:

**Clinical Accuracy:**
- Verify clinical terminology and coding (ICD-10, SNOMED, LOINC, RxNorm)
- Confirm guideline citations and external evidence
- Check for clinical plausibility and accuracy

**Gherkin Syntax:**
- Ensure proper Feature/Scenario/Given-When-Then structure
- Verify all steps are clearly written
- Check that Background sections are appropriate

**File Completeness:**
- Confirm all supporting files are present
- Verify FHIR Shorthand is syntactically correct
- Ensure assertion files properly test the scenarios

### 3. Categorization
Determine the appropriate categorization:

**Clinical Domain:**
- cardiology, oncology, primary-care, emergency, pediatrics, etc.
- Based on primary clinical specialty

**Generation Mode (Complexity):**
- **basic**: Simple scenarios, single condition, few steps
- **advanced**: Multi-step workflows, standard clinical complexity
- **expert**: Complex decision support, multiple considerations

**Fidelity Level:**
- **low**: Basic concepts without specific details
- **medium**: Realistic scenarios with standard clinical data
- **high**: Comprehensive with detailed context and edge cases

### 4. Naming Convention
Rename files following the pattern:
```
{domain}-{mode}-{fidelity}-{condition}-{id}.{extension}
```

Examples:
- `cardiology-advanced-high-hfref-001.feature`
- `primary-care-basic-low-hypertension-001.feature`
- `emergency-expert-high-stemi-001.feature`

### 5. Add Clinical Context
Add clinical context comments to the .feature file:
```gherkin
# Clinical Context: [Brief description]
# Domain: [Clinical domain]
# Complexity: [Mode] - [Brief explanation]
# Fidelity: [Level] - [Brief explanation]
# Guidelines: [Relevant clinical guidelines]
#
# Clinical Summary:
# - [Key clinical points]
# - [Important considerations]
# - [Expected outcomes]

Feature: [Descriptive feature name]
  
  As a clinical decision support system
  I want to [goal]
  So that [benefit]
  
  ...
```

### 6. Organization
Copy the renamed files to all three organizational structures:
- `by-domain/{domain}/` - Organized by clinical specialty
- `by-mode/{mode}/` - Organized by complexity level
- `by-fidelity/{fidelity}/` - Organized by detail level

### 7. Documentation
Update relevant README files:
- `by-domain/README.md` - Add to domain section
- `by-mode/README.md` - Update mode statistics
- `by-fidelity/README.md` - Update fidelity statistics
- `README.md` - Add to examples list
- `COVERAGE_ANALYSIS.md` - Update coverage metrics

## Validation Checklist

Before organizing examples from unsorted/ to structured folders:

- [ ] Clinical accuracy verified (terminology, guidelines, clinical logic)
- [ ] Gherkin syntax validated (Feature, Scenario, Given-When-Then)
- [ ] All supporting files present and correct
- [ ] Domain categorization determined
- [ ] Mode (complexity) level assigned
- [ ] Fidelity level assigned
- [ ] Files renamed following convention
- [ ] Clinical context comments added
- [ ] Files copied to all three organizational structures
- [ ] README files updated
- [ ] Coverage analysis updated

## Questions?

If unsure about categorization:
- Review existing examples in each category
- Consult `COVERAGE_ANALYSIS.md` for guidance
- Check README files in each organizational folder
- When in doubt, start with moderate classifications (advanced mode, medium fidelity) and adjust after review

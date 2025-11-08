# Clinical Context: Type 2 Diabetes with Atherosclerotic Cardiovascular Disease (ASCVD)
# Domain: Primary Care
# Complexity: Advanced - Risk stratification with cardioprotective medication selection
# Fidelity: Medium - Realistic patient scenario with standard clinical data
# Guidelines: ADA 2025 Standards of Care for Diabetes
#
# Clinical Summary:
# - 65-year-old male with undiagnosed Type 2 Diabetes (HbA1c 8.5%) and history of MI
# - High cardiovascular risk requires preferential use of SGLT2 inhibitors or GLP-1 agonists
# - Risk stratification based on CHA2DS2-VASc score and ASCVD history
# - Glycemic goals target HbA1c <7% with focus on cardiorenal protection
# - Monitoring includes HbA1c follow-up and eGFR assessment for medication safety

Feature: Diabetes Management with High Cardiovascular Risk

  As a clinical decision support system
  I want to guide diabetes treatment in patients with ASCVD following ADA guidelines
  So that cardioprotective medications are prioritized to reduce cardiovascular events

  Background:
    Given a patient fixture "tests/data/patients/diabetes/primary-care-advanced-medium-diabetes-001.fsh"
    And terminology lock "tests/terminology/diabetes.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "primary-care-advanced-medium-diabetes-001" on bundleId "Bundle-primary-care-advanced-medium-diabetes-001"
    Then the assertions in "tests/assertions/diabetes/primary-care-advanced-medium-diabetes-001.assert.yaml" all pass
    And no contraindication assertions fail

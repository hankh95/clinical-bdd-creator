# Clinical Context: Atrial Fibrillation with Multiple Comorbidities
# Domain: Cardiology
# Complexity: Expert - Complex decision-making with multiple interacting conditions
# Fidelity: High - Comprehensive scenario with detailed clinical context and edge cases
# Guidelines: AHA/ACC/HRS Atrial Fibrillation Management Guidelines
#
# Clinical Summary:
# - 70-year-old male with newly diagnosed atrial fibrillation, COPD, and obesity (BMI 35)
# - Requires anticoagulation for stroke prevention (CHA2DS2-VASc score ≥2)
# - Rate control strategy must account for COPD (avoid beta-blockers, use diltiazem)
# - DOAC anticoagulation (apixaban) preferred over warfarin for obese patients
# - Comprehensive management includes lifestyle interventions for obesity and ongoing COPD management
# - Monitoring plan addresses heart rate, bleeding risk, and cardiorenal status

Feature: Atrial Fibrillation Management with COPD and Obesity

  As a clinical decision support system
  I want to guide AFib treatment accounting for multiple comorbidities following AHA/ACC/HRS guidelines
  So that optimal stroke prevention, rate control, and comorbidity management are achieved

  Background:
    Given a patient fixture "tests/data/patients/afib/cardiology-expert-high-afib-001.fsh"
    And terminology lock "tests/terminology/afib.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "cardiology-expert-high-afib-001" on bundleId "Bundle-cardiology-expert-high-afib-001"
    Then the assertions in "tests/assertions/afib/cardiology-expert-high-afib-001.assert.yaml" all pass
    And no contraindication assertions fail

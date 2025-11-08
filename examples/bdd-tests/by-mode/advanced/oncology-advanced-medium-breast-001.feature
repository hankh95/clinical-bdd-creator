# Clinical Context: Breast Cancer Chemotherapy Management
# Domain: Oncology
# Complexity: Advanced - Multi-step chemotherapy cycle management with monitoring
# Fidelity: Medium - Realistic patient scenario with standard oncology protocols
# Guidelines: Breast cancer chemotherapy - anthracycline-based regimen
#
# Clinical Summary:
# - 48-year-old female with stage II breast cancer initiating cycle 1 of anthracycline-based chemotherapy
# - Treatment includes doxorubicin with 21-day cycles requiring close monitoring
# - Comprehensive toxicity surveillance: CBC, ANC, hemoglobin, liver and renal function
# - Weekly labs x3 per cycle to monitor for neutropenia, anemia, and organ toxicity
# - Supportive care includes nutrition counseling and goal-driven management

Feature: Breast Cancer Anthracycline-Based Chemotherapy Protocol

  As a clinical decision support system
  I want to guide safe administration of breast cancer chemotherapy with appropriate monitoring
  So that treatment efficacy is maximized while minimizing toxicity risks

  Background:
    Given a patient fixture "tests/data/patients/breast/oncology-advanced-medium-breast-001.fsh"
    And terminology lock "tests/terminology/breast.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "oncology-advanced-medium-breast-001" on bundleId "Bundle-oncology-advanced-medium-breast-001"
    Then the assertions in "tests/assertions/breast/oncology-advanced-medium-breast-001.assert.yaml" all pass
    And no contraindication assertions fail

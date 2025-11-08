# Clinical Context: Metastatic Castration-Resistant Prostate Cancer (mCRPC)
# Domain: Oncology
# Complexity: Expert - Complex decision support with clinical trial enrollment
# Fidelity: High - Comprehensive scenario with bone metastases, trial enrollment
# Guidelines: NCCN Prostate Cancer Guidelines, SWOG 0421 trial protocol
#
# Clinical Summary:
# - 67-year-old male with mCRPC post-prostatectomy, radiation, and hormone therapy failure
# - Rising PSA indicating disease progression with bone metastases
# - Enrolled in SWOG 0421 trial receiving docetaxel-based chemotherapy regimen
# - Requires careful monitoring of PSA, bone health, and pain management
# - Demonstrates multi-modal treatment approach typical of advanced prostate cancer

Feature: Metastatic Castration-Resistant Prostate Cancer Management

  As a clinical decision support system
  I want to guide treatment of mCRPC with bone metastases following NCCN guidelines
  So that appropriate chemotherapy, bone protection, and monitoring are implemented

  Background:
    Given a patient fixture "tests/data/patients/prostate/oncology-expert-high-prostate-001.fsh"
    And terminology lock "tests/terminology/prostate.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "oncology-expert-high-prostate-001" on bundleId "Bundle-oncology-expert-high-prostate-001"
    Then the assertions in "tests/assertions/prostate/oncology-expert-high-prostate-001.assert.yaml" all pass
    And no contraindication assertions fail

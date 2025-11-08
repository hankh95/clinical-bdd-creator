Feature: 2011_AdamEveryman_Prostate_Cancer_GrokFromPDF scenario

  Background:
    Given a patient fixture "tests/data/patients/prostate/2011_AdamEveryman_Prostate_Cancer_GrokFromPDF.fsh"
    And terminology lock "tests/terminology/prostate.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "2011_AdamEveryman_Prostate_Cancer_GrokFromPDF" on bundleId "Bundle-2011-AdamEveryman-Prostate-Cancer-GrokFromPDF"
    Then the assertions in "tests/assertions/prostate/2011_AdamEveryman_Prostate_Cancer_GrokFromPDF.assert.yaml" all pass
    And no contraindication assertions fail

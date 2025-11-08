Feature: RobertJohnson_Afib_CPOE_Obese scenario

  Background:
    Given a patient fixture "tests/data/patients/afib/RobertJohnson_Afib_CPOE_Obese.fsh"
    And terminology lock "tests/terminology/afib.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "RobertJohnson_Afib_CPOE_Obese" on bundleId "Bundle-RobertJohnson-Afib-CPOE-Obese"
    Then the assertions in "tests/assertions/afib/RobertJohnson_Afib_CPOE_Obese.assert.yaml" all pass
    And no contraindication assertions fail

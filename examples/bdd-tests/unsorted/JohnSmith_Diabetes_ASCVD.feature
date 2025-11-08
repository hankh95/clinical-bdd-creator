Feature: JohnSmith_Diabetes_ASCVD scenario

  Background:
    Given a patient fixture "tests/data/patients/diabetes/JohnSmith_Diabetes_ASCVD.fsh"
    And terminology lock "tests/terminology/diabetes.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "JohnSmith_Diabetes_ASCVD" on bundleId "Bundle-JohnSmith-Diabetes-ASCVD"
    Then the assertions in "tests/assertions/diabetes/JohnSmith_Diabetes_ASCVD.assert.yaml" all pass
    And no contraindication assertions fail

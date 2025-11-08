Feature: JaniceDoe_BreastCancer scenario

  Background:
    Given a patient fixture "tests/data/patients/breast/JaniceDoe_BreastCancer.fsh"
    And terminology lock "tests/terminology/breast.lock.yaml"

  Scenario: Execute guideline logic and validate clinical intent
    When I apply the relevant PlanDefinition for "JaniceDoe_BreastCancer" on bundleId "Bundle-JaniceDoe-BreastCancer"
    Then the assertions in "tests/assertions/breast/JaniceDoe_BreastCancer.assert.yaml" all pass
    And no contraindication assertions fail

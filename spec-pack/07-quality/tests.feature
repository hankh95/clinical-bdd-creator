Feature: Recommendations
  Scenario: Basic
    Given a patient with "type-2-diabetes"
    When I request recommendations
    Then I get at least 1 result

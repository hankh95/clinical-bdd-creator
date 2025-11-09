Feature: Head and Neck Cancer
  Clinical BDD scenarios generated from Head and Neck Cancer guideline

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_therapy
    Given a patient with patient condition
    When the head and neck cancer guideline is applied
    Then prescribe therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_therapy
    Given a patient without patient condition
    When the head and neck cancer guideline is applied
    Then prescribe therapy should not be initiated


Feature: NSCL Cancer
  Clinical BDD scenarios generated from NSCL Cancer guideline

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_treatment
    Given a patient with patient condition
    When the nscl cancer guideline is applied
    Then prescribe treatment should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_treatment
    Given a patient without patient condition
    When the nscl cancer guideline is applied
    Then prescribe treatment should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_therapy
    Given a patient with patient condition
    When the nscl cancer guideline is applied
    Then prescribe therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_therapy
    Given a patient without patient condition
    When the nscl cancer guideline is applied
    Then prescribe therapy should not be initiated


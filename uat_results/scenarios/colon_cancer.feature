Feature: Colon Cancer
  Clinical BDD scenarios generated from Colon Cancer guideline

  @positive @treatment
  Scenario: Patient meets criteria for should be_therapy_therapy
    Given a patient with patient condition
    When the colon cancer guideline is applied
    Then should be therapy therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_therapy_therapy
    Given a patient without patient condition
    When the colon cancer guideline is applied
    Then should be therapy therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for should be_intervention
    Given a patient with patient condition
    When the colon cancer guideline is applied
    Then should be intervention should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_intervention
    Given a patient without patient condition
    When the colon cancer guideline is applied
    Then should be intervention should not be initiated


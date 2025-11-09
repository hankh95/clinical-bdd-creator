Feature: Hodgkins Lymphoma
  Clinical BDD scenarios generated from Hodgkins Lymphoma guideline

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_therapy
    Given a patient with patient condition
    When the hodgkins lymphoma guideline is applied
    Then prescribe therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_therapy
    Given a patient without patient condition
    When the hodgkins lymphoma guideline is applied
    Then prescribe therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for should be_intervention
    Given a patient with patient condition
    When the hodgkins lymphoma guideline is applied
    Then should be intervention should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_intervention
    Given a patient without patient condition
    When the hodgkins lymphoma guideline is applied
    Then should be intervention should not be initiated


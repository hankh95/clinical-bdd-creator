Feature: Breast Cancer
  Clinical BDD scenarios generated from Breast Cancer guideline

  @positive @treatment
  Scenario: Patient meets criteria for should be_therapy_therapy
    Given a patient with patient condition
    When the breast cancer guideline is applied
    Then should be therapy therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_therapy_therapy
    Given a patient without patient condition
    When the breast cancer guideline is applied
    Then should be therapy therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_therapy
    Given a patient with patient condition
    When the breast cancer guideline is applied
    Then prescribe therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_therapy
    Given a patient without patient condition
    When the breast cancer guideline is applied
    Then prescribe therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for prescribe_therapy
    Given a patient with patient condition
    When the breast cancer guideline is applied
    Then prescribe therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for prescribe_therapy
    Given a patient without patient condition
    When the breast cancer guideline is applied
    Then prescribe therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for should be_therapy_therapy
    Given a patient with patient condition
    When the breast cancer guideline is applied
    Then should be therapy therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_therapy_therapy
    Given a patient without patient condition
    When the breast cancer guideline is applied
    Then should be therapy therapy should not be initiated


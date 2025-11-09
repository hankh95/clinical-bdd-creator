Feature: ACC-AFIB
  Clinical BDD scenarios generated from ACC-AFIB guideline

  @positive @treatment
  Scenario: Patient meets criteria for initiate_therapy_therapy
    Given a patient with patient condition
    When the acc-afib guideline is applied
    Then initiate therapy therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for initiate_therapy_therapy
    Given a patient without patient condition
    When the acc-afib guideline is applied
    Then initiate therapy therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for clinical_action
    Given a patient with patient condition
    When the acc-afib guideline is applied
    Then clinical action should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for clinical_action
    Given a patient without patient condition
    When the acc-afib guideline is applied
    Then clinical action should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for should be_intervention
    Given a patient with patient condition
    When the acc-afib guideline is applied
    Then should be intervention should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for should be_intervention
    Given a patient without patient condition
    When the acc-afib guideline is applied
    Then should be intervention should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for clinical_action
    Given a patient with patient condition
    When the acc-afib guideline is applied
    Then clinical action should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for clinical_action
    Given a patient without patient condition
    When the acc-afib guideline is applied
    Then clinical action should not be initiated


Feature: Diabetes Management
  Clinical BDD scenarios generated from Diabetes Management guideline

  @positive @treatment
  Scenario: Patient meets criteria for clinical_action
    Given a patient with type 2 diabetes AND HbA1c > 7.0 AND HbA1c > 7.0
    When the diabetes management guideline is applied
    Then clinical action should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for clinical_action
    Given a patient without type 2 diabetes AND HbA1c > 7.0 AND HbA1c > 7.0
    When the diabetes management guideline is applied
    Then clinical action should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for initiate_metformin_therapy
    Given a patient with patient condition
    When the diabetes management guideline is applied
    Then initiate metformin therapy should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for initiate_metformin_therapy
    Given a patient without patient condition
    When the diabetes management guideline is applied
    Then initiate metformin therapy should not be initiated

  @positive @treatment
  Scenario: Patient meets criteria for clinical_action
    Given a patient with patient condition
    When the diabetes management guideline is applied
    Then clinical action should be initiated

  @negative @treatment
  Scenario: Patient does not meet criteria for clinical_action
    Given a patient without patient condition
    When the diabetes management guideline is applied
    Then clinical action should not be initiated


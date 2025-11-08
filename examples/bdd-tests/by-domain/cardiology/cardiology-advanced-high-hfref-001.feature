# FishNet-BDD-Test-Framework
# Scenario-Category: 1 - Patient Encounter
# Scenario-Sub-Category: 1.1.2 - Treatment Recommendation
# Disease: Heart Failure with Reduced Ejection Fraction
# Guideline-Source: LittleFish v10 - 61_treatment_approach_littlefish.md (points 1-10); LittleFish v10 - 61_monitoring_littlefish.md (lines 1-14)
# Source-Document: source_sections/treatment_approach.txt
# External-Evidence: 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure (https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063)
# Creator: Hank Head - AI Analysis created
# CreatedOn: 2025-10-31
# Updated: 2025-10-31

Feature: 1.1.2 Treatment Recommendation - Rapid Quadruple GDMT Initiation for HFrEF

  As a clinical decision support system
  I want to ensure patients with newly diagnosed HFrEF are started on the four foundational therapies without delay
  So that mortality and hospitalization risk are reduced

  Background:
    Given an adult with chronic symptomatic HFrEF (LVEF ≤ 35%) and NYHA class II symptoms
    And there is no history of angioedema, advanced kidney failure (eGFR < 30 mL/min/1.73 m^2), or intolerance to GDMT agents
    And baseline labs show serum potassium 4.6 mmol/L and creatinine 1.2 mg/dL

  Scenario: Recommend initiating the full quadruple regimen during a single encounter when stable
    Given the patient is not currently receiving renin-angiotensin inhibition, evidence-based beta-blocker, MRA, or SGLT2 inhibitor
    And blood pressure is 118/72 mmHg without orthostatic symptoms
    When completing the visit medication review
    Then the system should recommend starting sacubitril/valsartan 49/51 mg twice daily (with 36-hour ACE inhibitor washout if applicable)
    And it should recommend metoprolol succinate 12.5 mg daily with a plan to uptitrate every 2 weeks as tolerated
    And it should recommend spironolactone 12.5 mg daily with potassium and renal monitoring in 3 to 7 days
    And it should recommend dapagliflozin 10 mg daily regardless of diabetes status
    And it should document patient education around lifestyle, sodium restriction, and daily weights

  Scenario: Flag incomplete GDMT when SGLT2 inhibitor is omitted without contraindication
    Given a clinician ordered sacubitril/valsartan, metoprolol succinate, and spironolactone
    And eGFR is 58 mL/min/1.73 m^2 with no history of euglycemic ketoacidosis
    When the system evaluates discharge medications prior to finalizing orders
    Then it should alert that an SGLT2 inhibitor is still indicated to complete quadruple therapy
    And it should provide dosing options (dapagliflozin 10 mg daily or empagliflozin 10 mg daily)
    And it should capture clinician acknowledgement if the class is declined so the gap appears on the rounding checklist

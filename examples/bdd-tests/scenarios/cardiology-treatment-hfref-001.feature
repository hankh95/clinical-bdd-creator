# Clinical Scenario ID: cardiology-treatment-hfref-001
# Title: Heart Failure with Reduced Ejection Fraction - Quadruple Therapy Initiation
# Domain: Cardiology | Category: Treatment Recommendation
# Guidelines: 2022 AHA/ACC/HFSA Heart Failure Guideline
# Complexity: Advanced | Fidelity: High | Priority: P1

Feature: Quadruple GDMT Initiation for Newly Diagnosed HFrEF

  As a clinical decision support system
  I want to ensure patients with newly diagnosed HFrEF receive all four foundational therapies without delay
  So that mortality and hospitalization risk are reduced according to evidence-based guidelines

  Background:
    Given a 65-year-old male with chronic symptomatic HFrEF (LVEF ≤ 35%)
    And NYHA class II symptoms with dyspnea on exertion
    And no contraindications to GDMT (no angioedema, eGFR > 30 mL/min/1.73 m², no intolerance)
    And baseline labs show serum potassium 4.6 mmol/L and creatinine 1.2 mg/dL
    And blood pressure is 118/72 mmHg without orthostatic symptoms
    And patient is not currently receiving any HFrEF medications

  Scenario: Complete quadruple therapy initiation during single encounter when stable
    When completing the initial visit medication review for a treatment-naive HFrEF patient
    Then recommend starting sacubitril/valsartan 49/51 mg twice daily
    And include note about 36-hour ACE inhibitor washout if applicable
    And recommend metoprolol succinate 12.5 mg daily with uptitration every 2 weeks as tolerated
    And recommend spironolactone 12.5 mg daily with potassium and renal monitoring in 3-7 days
    And recommend dapagliflozin 10 mg daily regardless of diabetes status
    And document patient education on lifestyle, sodium restriction, and daily weight monitoring

  Scenario: Flag incomplete GDMT when SGLT2 inhibitor omitted without contraindication
    Given a clinician ordered sacubitril/valsartan, metoprolol succinate, and spironolactone
    And eGFR is > 30 mL/min/1.73 m² with no history of euglycemic ketoacidosis
    And no documented contraindication to SGLT2 inhibitors exists
    When the system evaluates discharge medications prior to finalizing orders
    Then alert that an SGLT2 inhibitor is still indicated to complete quadruple therapy
    And provide dosing options (dapagliflozin 10 mg daily or empagliflozin 10 mg daily)
    And capture clinician acknowledgement if the class is declined
    And ensure the gap appears on the rounding checklist for follow-up

  Scenario: Appropriate monitoring plan establishment with quadruple therapy
    Given quadruple GDMT has been initiated with all four medication classes
    When establishing the monitoring and follow-up plan
    Then schedule potassium and renal function labs in 3-7 days
    And schedule follow-up visit in 2 weeks for beta-blocker titration
    And document instructions for daily weight monitoring by patient
    And document instructions for reporting weight gain > 2-3 lbs in 1-2 days
    And include education on symptom recognition and when to seek care

  Scenario: Verify all components of GDMT are addressed in treatment plan
    Given a treatment plan is being finalized for a HFrEF patient
    When reviewing for completeness of guideline-directed medical therapy
    Then verify presence of ARNI (sacubitril/valsartan) or ACE-I/ARB with documented reason
    And verify presence of evidence-based beta-blocker (carvedilol, metoprolol succinate, or bisoprolol)
    And verify presence of MRA (spironolactone or eplerenone) with appropriate monitoring
    And verify presence of SGLT2 inhibitor (dapagliflozin or empagliflozin)
    And document rationale for any omissions with contraindications or patient preferences

  Scenario: Patient education encompasses all critical self-management elements
    When providing patient education for newly initiated HFrEF therapy
    Then educate on daily weight monitoring and specific thresholds for concern
    And educate on sodium restriction (< 2g/day or per clinical guidelines)
    And educate on appropriate fluid management
    And educate on exercise as tolerated with gradual increases
    And educate on recognition of worsening symptoms (increased dyspnea, edema, fatigue)
    And educate on medication adherence importance and timing
    And provide clear instructions on when and how to contact healthcare team

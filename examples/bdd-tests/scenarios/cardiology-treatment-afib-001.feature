# Clinical Scenario ID: cardiology-treatment-afib-001
# Title: Atrial Fibrillation with COPD and Obesity - Anticoagulation and Rate Control
# Domain: Cardiology | Category: Treatment Recommendation
# Guidelines: AHA/ACC/HRS Atrial Fibrillation Management Guidelines
# Complexity: Expert | Fidelity: High | Priority: P2

Feature: Atrial Fibrillation Management with Multiple Comorbidities

  As a clinical decision support system
  I want to guide comprehensive AFib treatment accounting for COPD and obesity
  So that optimal stroke prevention, rate control, and comorbidity management are achieved

  Background:
    Given a 70-year-old male with newly diagnosed atrial fibrillation
    And established COPD currently treated with tiotropium inhaler
    And obesity with BMI 35
    And CHA2DS2-VASc score ≥ 2 indicating high stroke risk
    And adequate renal and hepatic function for anticoagulation

  Scenario: Comprehensive treatment plan for newly diagnosed AFib with comorbidities
    When developing initial treatment plan for newly diagnosed AFib
    Then recommend anticoagulation with DOAC (apixaban) for stroke prevention
    And adjust anticoagulation dosing for obesity and renal function
    And recommend rate control with diltiazem (non-beta-blocker) due to COPD
    And avoid beta-blockers given active COPD
    And continue tiotropium inhaler for COPD management
    And recommend lifestyle interventions for weight loss
    And recommend exercise program as tolerated with COPD
    And order nutrition counseling referral

  Scenario: Stroke prevention with appropriate anticoagulation selection
    Given CHA2DS2-VASc score ≥ 2 from age and obesity
    When selecting anticoagulation therapy
    Then recommend DOAC over warfarin
    And specifically recommend apixaban adjusted for obesity and renal function
    And explain rationale that DOAC is preferred for obese patients
    And document baseline renal and hepatic function
    And educate patient on bleeding precautions and adherence importance

  Scenario: Rate control strategy with COPD considerations
    Given patient requires rate control for atrial fibrillation
    And patient has active COPD treated with tiotropium
    When selecting rate control medication
    Then recommend diltiazem as non-beta-blocker option
    And document that beta-blockers are avoided due to COPD
    And set target heart rate goals
    And plan for rhythm assessment if patient remains symptomatic
    And continue COPD management without interference

  Scenario: Comprehensive monitoring plan addressing all clinical concerns
    Given patient is on anticoagulation and rate control medications
    And has multiple comorbidities requiring monitoring
    When establishing monitoring schedule
    Then order renal function panel every 3-6 months for anticoagulation safety
    And order CBC every 3 months to monitor for bleeding risk
    And order HbA1c every 3 months to screen for metabolic complications
    And monitor heart rate and rhythm regularly for rate control goals
    And educate patient on recognizing bleeding and stroke symptoms

  Scenario: Lifestyle modification plan for obesity management
    Given patient has obesity with BMI 35
    And obesity contributes to cardiovascular risk
    When developing comprehensive care plan
    Then recommend structured weight loss program
    And provide nutrition counseling referral
    And recommend exercise program tailored for COPD limitations
    And set realistic weight loss goals
    And explain cardiovascular benefits of weight reduction
    And schedule follow-up to assess progress

  Scenario: Patient education encompasses multiple conditions
    When providing patient education for AFib with comorbidities
    Then educate on anticoagulation therapy adherence
    And educate on bleeding precautions and warning signs
    And educate on stroke symptom recognition
    And educate on rate control medication adherence
    And educate on COPD management and inhaler technique
    And educate on weight loss strategies and dietary modifications
    And educate on exercise recommendations appropriate for COPD
    And provide clear instructions on when to seek emergency care

  Scenario: Rhythm versus rate control decision making
    Given initial rate control strategy has been implemented
    When patient remains symptomatic despite adequate rate control
    Then consider rhythm control strategy as alternative
    And assess candidacy for cardioversion or antiarrhythmic therapy
    And discuss risks and benefits with patient
    And ensure COPD is considered in antiarrhythmic selection
    And coordinate with cardiology if rhythm control pursued

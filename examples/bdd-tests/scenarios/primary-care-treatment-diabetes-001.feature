# Clinical Scenario ID: primary-care-treatment-diabetes-001
# Title: Type 2 Diabetes with ASCVD - Cardioprotective Therapy Initiation
# Domain: Primary Care | Category: Treatment Recommendation
# Guidelines: ADA 2025 Standards of Care, Section 9
# Complexity: Advanced | Fidelity: Medium | Priority: P2

Feature: Type 2 Diabetes with ASCVD - Cardioprotective Agent Selection

  As a clinical decision support system
  I want to ensure patients with T2DM and established ASCVD receive cardioprotective therapies
  So that cardiovascular outcomes are improved per ADA 2025 guidelines

  Background:
    Given a 65-year-old male with newly diagnosed Type 2 Diabetes Mellitus
    And HbA1c of 8.5% indicating inadequate glycemic control
    And established ASCVD evidenced by history of myocardial infarction
    And adequate renal function (eGFR adequate for SGLT2i and GLP-1 RA)
    And no history of euglycemic ketoacidosis

  Scenario: Prioritize cardioprotective agents over traditional metformin monotherapy
    When developing initial treatment plan for newly diagnosed T2DM with ASCVD
    Then recommend SGLT2 inhibitor or GLP-1 RA as first-line therapy
    And explain cardiovascular benefit evidence from clinical trials
    And deprioritize metformin-only approach for this high-risk patient
    And consider dual therapy given HbA1c 8.5% and ASCVD
    And document rationale based on ADA 2025 Section 9 guidelines

  Scenario: SGLT2 inhibitor recommendation for cardioprotective benefit
    Given patient has established ASCVD and newly diagnosed T2DM
    When selecting diabetes medication with proven cardiovascular benefit
    Then recommend SGLT2 inhibitor (empagliflozin, dapagliflozin, or canagliflozin)
    And explain cardiorenal protection benefit regardless of glycemic control
    And reference supporting evidence (EMPA-REG, CANVAS, DECLARE-TIMI trials)
    And verify adequate renal function (eGFR > 30 mL/min/1.73m²)
    And educate patient on SGLT2i mechanism and benefits

  Scenario: GLP-1 RA recommendation as alternative cardioprotective option
    Given patient has established ASCVD and newly diagnosed T2DM
    When considering alternative or additional cardioprotective agent
    Then recommend GLP-1 receptor agonist (liraglutide, semaglutide, or dulaglutide)
    And explain cardiovascular benefit evidence from clinical trials
    And reference supporting evidence (LEADER, SUSTAIN-6, REWIND trials)
    And consider as alternative if SGLT2i not tolerated or contraindicated
    And consider as addition to SGLT2i for enhanced glycemic control

  Scenario: Comprehensive monitoring plan for diabetes with ASCVD
    Given patient is initiated on cardioprotective diabetes therapy
    When establishing monitoring schedule
    Then order HbA1c every 3 months to assess glycemic control
    And target HbA1c < 7% while monitoring for treatment response
    And order baseline and periodic eGFR and creatinine monitoring
    And order periodic lipid panel for comprehensive CV risk management
    And monitor blood pressure and weight at each visit
    And assess ASCVD status and cardiac symptoms ongoing
    And adjust therapy based on glycemic response and tolerability

  Scenario: Risk stratification flags urgent need for cardioprotective therapy
    Given patient has both elevated HbA1c (8.5%) and established ASCVD
    When system performs risk stratification
    Then flag as high cardiovascular risk requiring urgent intervention
    And alert that traditional stepwise approach is inappropriate
    And recommend aggressive cardioprotective agent initiation
    And suggest dual therapy approach if needed for glycemic target
    And document high-risk status for care coordination

  Scenario: Patient education emphasizes cardiovascular protection
    When providing patient education for newly diagnosed T2DM with ASCVD
    Then educate on Type 2 diabetes diagnosis and long-term implications
    And emphasize cardiovascular risk and importance of cardioprotective therapy
    And explain how SGLT2i or GLP-1 RA protects heart and kidneys
    And educate on medication adherence importance
    And educate on lifestyle modifications (diet, exercise, weight management)
    And educate on ASCVD secondary prevention strategies
    And educate on recognition of hyperglycemia and hypoglycemia symptoms
    And provide clear guidance on when to seek medical attention

  Scenario: Contraindication checking for SGLT2 inhibitor safety
    Given patient is being considered for SGLT2 inhibitor therapy
    When validating SGLT2i is appropriate
    Then verify eGFR is adequate (typically > 30 mL/min/1.73m²)
    And verify no history of euglycemic ketoacidosis
    And verify no active diabetic ketoacidosis
    And document baseline renal function
    And plan for renal function monitoring
    And educate patient on rare but serious SGLT2i adverse effects

  Scenario: Alert when traditional metformin-only approach selected for high-risk patient
    Given patient has established ASCVD and elevated HbA1c
    When treatment plan includes only metformin without cardioprotective agents
    Then alert that ADA guidelines recommend SGLT2i or GLP-1 RA for ASCVD
    And display evidence for cardiovascular benefit of SGLT2i/GLP-1 RA
    And suggest adding or switching to cardioprotective agent
    And require documentation if clinician overrides recommendation
    And capture rationale for guideline deviation

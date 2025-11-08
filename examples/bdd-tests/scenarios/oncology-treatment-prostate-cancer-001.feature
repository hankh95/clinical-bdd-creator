# Clinical Scenario ID: oncology-treatment-prostate-cancer-001
# Title: Metastatic Castration-Resistant Prostate Cancer - Docetaxel Chemotherapy
# Domain: Oncology | Category: Treatment Recommendation
# Guidelines: NCCN/AUA Prostate Cancer Guidelines, SWOG 0421 Trial
# Complexity: Expert | Fidelity: High | Priority: P2

Feature: Metastatic Castration-Resistant Prostate Cancer Management

  As a clinical decision support system
  I want to guide comprehensive mCRPC treatment following NCCN/AUA guidelines and trial protocols
  So that optimal oncologic outcomes and quality of life are achieved

  Background:
    Given a 67-year-old male with metastatic castration-resistant prostate cancer
    And Gleason score 8 indicating high-risk disease
    And history of prostatectomy, radiation, and hormone therapy with progression
    And bone metastases confirmed on imaging
    And rising PSA despite androgen deprivation therapy
    And enrolled in SWOG 0421 trial for docetaxel-based regimen
    And adequate performance status for chemotherapy

  Scenario: Comprehensive treatment plan for mCRPC with bone metastases
    When developing treatment plan for mCRPC after hormone therapy failure
    Then recommend docetaxel 75 mg/m² IV every 3 weeks per SWOG 0421 protocol
    And recommend prednisone 5 mg orally twice daily as adjunct
    And recommend zoledronic acid 4 mg IV every 4 weeks for bone health
    And continue pain management with hydrocodone as required
    And administer trial agent (atrasentan or placebo) per randomization
    And establish comprehensive monitoring plan

  Scenario: Docetaxel chemotherapy administration per SWOG 0421 protocol
    When prescribing chemotherapy for symptomatic mCRPC
    Then order docetaxel 75 mg/m² IV
    And specify 3-week cycle schedule (q3w)
    And combine with prednisone 5 mg PO BID
    And document trial participation (SWOG 0421)
    And explain expected survival benefit from docetaxel in mCRPC
    And obtain informed consent for chemotherapy and trial

  Scenario: Bone health management with zoledronic acid for metastases
    Given patient has multiple bone metastases from prostate cancer
    When implementing bone protective therapy
    Then order zoledronic acid 4 mg IV every 4 weeks
    And assess renal function before each dose
    And monitor for skeletal-related events
    And educate on importance of bone health in metastatic disease
    And consider denosumab as alternative if renal function declines

  Scenario: Comprehensive monitoring plan for mCRPC treatment
    When establishing monitoring schedule for mCRPC patient on chemotherapy
    Then order PSA monitoring every 3-6 months for disease response
    And order bone scans as needed for progression assessment
    And order CT scans as needed for disease burden evaluation
    And monitor renal function before each zoledronic acid dose
    And monitor CBC and liver function each chemotherapy cycle
    And assess pain, performance status, and neuropathy at each visit

  Scenario: PSA monitoring for disease response and progression
    Given patient on docetaxel chemotherapy for mCRPC
    When monitoring treatment response
    Then order PSA level every 3-6 months
    And trend PSA values to assess response or progression
    And correlate PSA with clinical symptoms and imaging
    And adjust treatment plan if PSA progression documented
    And educate patient on PSA as disease marker

  Scenario: Pain management strategy for bone metastases
    Given patient has painful bone metastases
    When managing cancer-related pain
    Then continue hydrocodone as required for pain control
    And assess pain level at each visit
    And adjust pain medication as needed
    And consider additional modalities if pain worsens
    And educate on pain management options
    And consider referral to palliative care if needed

  Scenario: Alternative therapy considerations if disease progresses
    Given patient on first-line docetaxel for mCRPC
    When considering options for progression
    Then document denosumab as alternative bone agent if renal issues develop
    And document radium-223 as option for symptomatic bone metastases
    And consider cabazitaxel as second-line chemotherapy
    And consider newer agents (abiraterone, enzalutamide) if not previously used
    And coordinate with oncology for treatment sequencing

  Scenario: Clinical trial management and documentation
    Given patient enrolled in SWOG 0421 trial
    When managing trial participation
    Then administer docetaxel per trial protocol (75 mg/m² q3w)
    And administer prednisone per protocol (5 mg BID)
    And administer randomized agent (atrasentan or placebo)
    And document all trial-related procedures and assessments
    And ensure compliance with trial monitoring requirements
    And report adverse events per trial protocol

  Scenario: Quality of life and supportive care integration
    When providing comprehensive care for mCRPC patient
    Then assess quality of life at each visit
    And address symptoms impacting daily function
    And integrate pain management effectively
    And provide psychosocial support
    And coordinate with palliative care if needed
    And address nutrition and functional status
    And educate family on supportive care needs

  Scenario: Patient and family education for advanced disease
    When educating patient with mCRPC
    Then explain disease status as metastatic castration-resistant
    And discuss treatment goals (palliation, quality of life, survival)
    And educate on docetaxel chemotherapy expectations and side effects
    And explain trial participation implications (SWOG 0421)
    And educate on bone health and skeletal-related events
    And discuss pain management strategies and expectations
    And explain importance of PSA and imaging monitoring
    And educate on signs of disease progression
    And provide clear guidance on when to contact team
    And discuss quality of life considerations and advance care planning

  Scenario: Monitoring for chemotherapy toxicity and dose adjustments
    Given patient receiving docetaxel every 3 weeks
    When monitoring for treatment-related toxicity
    Then assess CBC for neutropenia before each cycle
    And assess for peripheral neuropathy progression
    And assess for fluid retention
    And monitor liver function for hepatotoxicity
    And consider dose reduction if grade 3-4 toxicity occurs
    And hold treatment if neutropenia severe
    And document all toxicities and interventions

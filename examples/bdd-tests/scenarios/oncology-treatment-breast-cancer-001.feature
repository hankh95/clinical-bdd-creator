# Clinical Scenario ID: oncology-treatment-breast-cancer-001
# Title: Stage II Breast Cancer - Anthracycline-Based Chemotherapy Cycle 1
# Domain: Oncology | Category: Treatment Recommendation
# Guidelines: NCCN Breast Cancer Guidelines
# Complexity: Advanced | Fidelity: Medium | Priority: P2

Feature: Stage II Breast Cancer Adjuvant Chemotherapy Management

  As a clinical decision support system
  I want to ensure appropriate chemotherapy administration and monitoring for breast cancer patients
  So that treatment efficacy is maximized while toxicity is minimized

  Background:
    Given a 48-year-old female with stage II breast cancer
    And starting cycle 1 of anthracycline-based chemotherapy regimen
    And adequate baseline labs (ANC, hemoglobin, liver function, renal function)
    And no historical neutropenia (neutropenia flags = 0)
    And no historical sepsis (sepsis flags = 0)
    And performance status adequate for chemotherapy

  Scenario: Comprehensive chemotherapy care plan for cycle 1
    When initiating cycle 1 of anthracycline-based chemotherapy
    Then order doxorubicin IV per protocol on 21-day cycle schedule
    And create comprehensive chemotherapy care plan
    And include supportive care measures (antiemetics, hydration)
    And establish monitoring schedule for toxicity
    And document patient education on chemotherapy management

  Scenario: Anthracycline chemotherapy administration with proper schedule
    When prescribing doxorubicin for breast cancer
    Then specify dose per protocol (typically 60 mg/m² IV)
    And specify 21-day cycle schedule (q21d)
    And verify adequate cardiac function (baseline LVEF)
    And plan for cardiac monitoring due to anthracycline cardiotoxicity risk
    And document informed consent for chemotherapy

  Scenario: Comprehensive weekly hematologic monitoring during cycle
    When establishing monitoring plan for chemotherapy cycle 1
    Then order CBC with differential every 7 days
    And specify count of 3 (days 7, 14, 21 of 21-day cycle)
    And specifically monitor absolute neutrophil count (ANC)
    And specifically monitor hemoglobin with target >= 10 g/dL
    And order liver function tests for hepatotoxicity monitoring
    And order renal function panel (metabolic panel) each cycle
    And document monitoring rationale and targets

  Scenario: Risk assessment for neutropenia and febrile neutropenia
    Given patient is receiving anthracycline chemotherapy cycle 1
    When performing risk assessment for hematologic complications
    Then document neutropenia risk assessment
    And consider prophylactic growth factors if high risk
    And educate patient on infection prevention strategies
    And educate on fever threshold (> 100.4°F) requiring immediate care
    And document neutropenia risk factors and mitigation strategies

  Scenario: Hemoglobin monitoring goal to prevent severe anemia
    When establishing treatment goals for chemotherapy patient
    Then set goal to maintain hemoglobin >= 10 g/dL
    And monitor hemoglobin weekly during cycle
    And consider erythropoiesis-stimulating agents if indicated
    And document goal in care plan with target value
    And educate patient on anemia symptoms and management

  Scenario: Cardiac toxicity risk assessment and monitoring plan
    Given patient is receiving anthracycline (doxorubicin) chemotherapy
    When assessing cardiotoxicity risk
    Then document baseline LVEF before treatment initiation
    And establish periodic cardiac monitoring schedule
    And assess for cumulative anthracycline dose
    And educate patient on cardiac symptoms to report
    And document cardiotoxicity risk assessment and monitoring plan

  Scenario: Nutrition counseling referral for treatment support
    When developing comprehensive supportive care plan
    Then order nutrition counseling referral
    And specify timing as early in treatment course
    And document rationale for nutritional support during chemotherapy
    And coordinate with nutrition services for appointment

  Scenario: Comprehensive patient education for chemotherapy cycle 1
    When providing patient education for first chemotherapy cycle
    Then educate on chemotherapy schedule and what to expect
    And educate on common side effects (nausea, fatigue, alopecia, myelosuppression)
    And educate on infection prevention and fever threshold (> 100.4°F)
    And educate on bleeding precautions with thrombocytopenia
    And educate on importance of nutrition and hydration
    And educate on symptom management strategies
    And educate on importance of scheduled lab monitoring
    And provide clear instructions on when to contact oncology team
    And provide 24/7 contact information for urgent concerns

  Scenario: Follow-up schedule for 21-day chemotherapy cycle
    When scheduling follow-up for chemotherapy cycle 1
    Then schedule CBC on day 7 of cycle
    And schedule CBC on day 14 of cycle
    And schedule CBC on day 21 of cycle (pre-next cycle)
    And schedule clinic visit for next cycle planning
    And coordinate with laboratory for timely result reporting
    And establish process for dose adjustments based on counts

  Scenario: Comprehensive symptom monitoring throughout cycle
    When monitoring patient during chemotherapy cycle
    Then monitor for signs of infection continuously
    And monitor for bleeding or bruising
    And monitor for mucositis or oral complications
    And monitor for peripheral neuropathy
    And monitor for cardiac symptoms
    And monitor for gastrointestinal toxicity
    And document all adverse events and interventions

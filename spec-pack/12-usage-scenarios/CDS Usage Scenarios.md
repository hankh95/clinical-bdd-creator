# CDS Use Case

This is an informal document created as an update to a known list of CDS Competitors in clinical decision support (CDS) in it’s many forms:

Usage Scenario is the most important view as the CDS drives assistance for a specific user at a specific point in one or more workflows. It is described as Actor / Workflow

# **Comprehensive Clinical Decision Support (CDS) Use Cases**

This document outlines a comprehensive set of Clinical Decision Support (CDS) use cases, aligned with FHIR Clinical Practice Guidelines (FHIR-CPG) and Integrating the Healthcare Enterprise (IHE) Computable Care Guidelines (CCG). The use cases are categorized into four key areas to reflect their application in clinical workflows, population health, patient engagement, and information retrieval. 

## Decision Question Mapping
- **In-workflow prompts (CDS Hooks/BPA)** → `DecisionQuestion` options: `treatment_now`, `tests_now`.
- **Risk and stratification scenarios** → `DecisionQuestion` options: `refer_now`, `treatment_now` (when risk triggers immediate therapy).
- **Contraindication and safety checks** → `DecisionQuestion`: `treatment_now` with required negative assertions.
- **Escalation and referral workflows** → `DecisionQuestion`: `treatment_now` or `refer_now` depending on the action.
- **Monitoring cadence** → `DecisionQuestion`: `monitoring_frequency` with explicit timing assertions.
- **SDOH modifiers** → Attach via `PatientFixtureDelta` plus negative/exception handling when social context blocks standard care.

From the knowledge / CDS Tool Perspective

## **1\. Patient Encounter: In-Workflow Decision Support**

CDS tools integrated into clinician workflows within electronic health records (EHRs) to provide real-time, actionable guidance.

### **1.1 Pre-Action Guidance (Preventative and Actionable)**

- **1.1.1 Differential Diagnosis**: Suggests possible diagnoses based on patient symptoms and history, often paired with diagnostic test or treatment recommendations.  
- **1.1.2 Treatment Recommendation**: Provides evidence-based treatment options for specific conditions, including non-pharmacologic interventions.  
- **1.1.3 Drug Recommendation**: Suggests medications, including dosage and administration, based on patient conditions and guidelines.  
- **1.1.4 Cancer Treatment Recommendation**: Offers tailored multi-modal treatment that may include surgery, medications, and other procedures (e.g., cancer therapy).  
- **1.1.5 Diagnostic Test Recommendation**: Recommends appropriate diagnostic tests (e.g., lab tests, imaging) based on clinical guidelines.  
- **1.1.6 Genetic Test Recommendation**: Suggests genetic or pharmacogenomic testing to guide personalized treatment.  
- **1.1.7 Next Best Action**: Provides prioritized actions upon opening a patient chart, such as ordering preventive screenings.  
- **1.1.8 Value-Based Care Alerts**: Notifies providers of opportunities to meet quality metrics or value-based care goals (e.g., preventive care reminders).  
- **1.1.9 Lifestyle / Patient Education**: Delivers behavior-change guidance and educational resources tailored to the patient.

Typical User interaction \- On Chart Open, evaluate the patient data against applicable guidelines and give a list of actionable tasks for the care team member. (MD/APP)

### **1.2 Post-Action Error Prevention**

- **1.2.1 Drug Interaction Checking**: Alerts for potential drug-drug, drug-allergy, or drug-condition interactions, leveraging databases like First Databank (FDB).  
- **1.2.2 Diagnostic Test Appropriateness Check**: Ensures imaging or tests meet Appropriate Use Criteria (AUC), e.g., via CareSelect (Optum).  
- **1.2.3 Adverse Event Monitoring**: Generates real-time alerts for potential adverse events, such as hospital-acquired infections or medication errors.

## **2\. Population-Based CDS**

CDS applications focused on managing populations, often for case management, value-based care, or quality improvement.

- **2.1.1 Case Management**: Identifies patients requiring ongoing monitoring or intervention (e.g., chronic disease management for diabetes or hypertension).  
- **2.2.1 Quality Metrics Reporting**: Supports electronic Clinical Quality Measures (eCQMs) to track and improve care quality across populations.   
- **2.3.1 Risk Stratification**: Uses predictive analytics to identify high-risk patients for targeted interventions (e.g., readmission prevention).  
- **2.4.1 Public Health Reporting**: Automates case reporting for infectious diseases or public health surveillance using FHIR-based data exchange.

## **3\. Patient-Centered CDS**

CDS tools that engage patients and caregivers, incorporating patient-specific data and preferences.

- **3.1.1 Shared Decision-Making Support**: Provides patient-specific recommendations that incorporate preferences, social determinants of health (SDOH), or patient-reported outcomes, often via SMART on FHIR apps.  
- **3.2.1 SDOH Integration**: Incorporates data on food security, housing stability, or transportation access to tailor interventions and address health equity.  
- **3.3.1 Patient Education and Reminders**: Delivers personalized education or follow-up reminders to patients (e.g., vaccination schedules).

## **4\. Information Retrieval and Protocol Support**

CDS tools that provide on-demand information or automate clinical protocols, used within or outside patient encounters.

- **4.1.1 Guideline-Driven Information Retrieval**: Enables clinicians to query evidence-based guidelines or knowledge bases for decision support (e.g., via CDS Hooks or FHIR Clinical Reasoning).  
- **4.2.1 Protocol-Driven Care**: Automates clinical protocols (e.g., sepsis management) triggered by patient events or conditions.  
- **4.3.1 Documentation Support**: Generates documentation templates to ensure guideline compliance and streamline reporting.  
- **4.4.1 Care Coordination Alerts**: Notifies providers of care transitions, such as discharge planning or follow-up needs, to ensure continuity across settings.

## CDS Scenario Glossary

| CDS Scenario | Decision Question Family | Notes |
|--------------|-------------------------|-------|
| 1.1.1 Differential Diagnosis | Diagnostic reasoning | Guides which conditions/tests to prioritize; typically pairs with `tests_now`. |
| 1.1.2 Treatment Recommendation | Therapy selection | Chooses evidence-based interventions; maps to `treatment_now`. |
| 1.1.3 Drug Recommendation | Medication selection | Narrows drug choices, dosing, and contraindications; `treatment_now`. |
| 1.1.4 Cancer Treatment Recommendation | Oncology pathway | Multimodal planning across timelines; `treatment_now` with staging context. |
| 1.1.5 Diagnostic Test Recommendation | Diagnostic workflow | Determines next investigations; `tests_now`. |
| 1.1.6 Genetic Test Recommendation | Precision testing | Flags pharmacogenomic or hereditary panels; `tests_now`. |
| 1.1.7 Next Best Action | Task prioritisation | Presents actionable worklists; typically `treatment_now` or scheduling tasks. |
| 1.1.8 Value-Based Care Alerts | Quality gap closure | Highlights measure-driven actions; `treatment_now`. |
| 1.1.9 Lifestyle / Patient Education | Behaviour change | Delivers tailored coaching; often logged as `education_now` decisions. |
| 1.2.1 Drug Interaction Checking | Safety guardrail | Blocks unsafe orders; `treatment_now` with negative assertions. |
| 1.2.2 Diagnostic Test Appropriateness Check | Safety/appropriateness | Validates imaging/lab necessity; `tests_now`. |
| 1.2.3 Adverse Event Monitoring | Monitoring cadence | Watches for deterioration or complications; `monitoring_frequency`. |
| 2.1.1 Case Management | Population oversight | Surfaces high-need cohorts; typically `refer_now` to care managers. |
| 2.2.1 Quality Metrics Reporting | Quality tracking | Aggregates measure performance; supports `monitoring_frequency` reviews. |
| 2.3.1 Risk Stratification | Predictive analytics | Scores patients for escalation; leads to `refer_now` or intensified therapy. |
| 2.4.1 Public Health Reporting | Regulatory reporting | Automates notifications; treat as `report_now` style actions. |
| 3.1.1 Shared Decision-Making Support | Collaborative planning | Balances options with patient preferences; combines `treatment_now` + `education_now`. |
| 3.2.1 SDOH Integration | Social context adjustment | Applies social modifiers to plans; typically adjusts `treatment_now`. |
| 3.3.1 Patient Education and Reminders | Engagement | Issues follow-up reminders; `education_now`. |
| 4.1.1 Guideline-Driven Information Retrieval | Knowledge lookup | Provides on-demand evidence; support for `tests_now`/`treatment_now`. |
| 4.2.1 Protocol-Driven Care | Workflow automation | Orchestrates standing orders; `treatment_now`. |
| 4.3.1 Documentation Support | Documentation | Ensures compliant narratives; aligns with `documentation_now` handoffs. |
| 4.4.1 Care Coordination Alerts | Escalation/handoff | Notifies teams of transitions; typically `refer_now`. |

# Use Cases from Actor / Task / Workflow / Value perspective

There are a few moments during a patient encounter (or right before) where we have the opportunity to significantly influence provider decision making. The CDS use cases are the most valuable and can be measured in software to prove effectiveness for 

1. Behavior change  
2. Concordance to evidence  
3. Clinical outcomes (comparing combinations of the above) 

## **1\. Doctor**

**Role**: Diagnoses conditions, orders tests/treatments, and makes clinical decisions during patient encounters.

* **Task/Workflow Step**: When opening a patient chart, identify if changed data since the last encounter indicates actions such as ordering a test or changing the treatment plan.  
  * **CDS Use Case 1.1.7**: Next Best Action  
    * Provides prioritized actions (e.g., order preventive screenings, adjust treatment) based on updated patient data.  
  * **CDS Use Case 1.1.1**: Differential Diagnosis  
    * Suggests possible diagnoses based on new symptoms or data changes.  
  * **CDS Use Case 1.1.8**: Value-Based Care Alerts  
    * Notifies of quality metrics or preventive care opportunities triggered by updated patient data.  
* **Task/Workflow Step**: During the ordering workflow, ensure appropriate and safe orders.  
  * **CDS Use Case 1.1.3**: Drug Recommendation  
    * Suggests medications, including dosage, based on patient conditions and guidelines.  
  * **CDS Use Case 1.2.1**: Drug Interaction Checking  
    * Alerts for potential drug-drug, drug-allergy, or drug-condition interactions.  
  * **CDS Use Case 1.1.5**: Diagnostic Test Recommendation  
    * Recommends appropriate tests (e.g., lab, imaging) based on clinical guidelines.  
  * **CDS Use Case 1.2.2**: Diagnostic Test Appropriateness Check  
    * Ensures imaging/tests meet Appropriate Use Criteria (AUC), e.g., via CareSelect.  
  * **CDS Use Case 1.1.4**: Cancer Treatment Recommendation  
    * Suggests tailored multi-modal cancer therapy (e.g., chemotherapy, surgery) based on cancer type and patient factors.  
  * **CDS Use Case 1.1.6**: Genetic Test Recommendation  
    * Recommends genetic/pharmacogenomic testing to guide personalized treatment.  
* **Task/Workflow Step**: During treatment planning, provide evidence-based guidance.  
  * **CDS Use Case 1.1.2**: Treatment Recommendation  
    * Offers evidence-based treatment options, including non-pharmacologic interventions.  
  * **CDS Use Case 4.2.1**: Protocol-Driven Care  
    * Automates clinical protocols (e.g., sepsis management) triggered by patient conditions.  
* **Task/Workflow Step**: When reviewing patient data, incorporate social determinants or genomic data.  
  * **CDS Use Case 3.2.1**: SDOH Integration  
    * Incorporates social determinants of health (e.g., housing stability) to tailor interventions.  
  * **CDS Use Case 1.1.6**: Genetic Test Recommendation  
    * Provides personalized recommendations based on genetic and pharmacogenomic data.

## **2\. Nurse**

**Role**: Delivers patient care, monitors conditions, and supports care coordination.

* **Task/Workflow Step**: During patient monitoring, identify changes requiring intervention.  
  * **CDS Use Case 1.2.3**: Adverse Event Monitoring  
    * Alerts for potential adverse events (e.g., hospital-acquired infections, medication errors).  
  * **CDS Use Case 4.2.1**: Protocol-Driven Care  
    * Automates clinical protocols (e.g., sepsis alerts) for timely nursing interventions.  
* **Task/Workflow Step**: During care transitions, ensure continuity of care.  
  * **CDS Use Case 4.4.1**: Care Coordination Alerts  
    * Notifies of discharge planning or follow-up needs to ensure seamless transitions.  
* **Task/Workflow Step**: When documenting care, streamline compliance with guidelines.  
  * **CDS Use Case 4.3.1**: Documentation Support  
    * Generates templates to ensure guideline-compliant documentation.

## **3\. Doctor and Nurse (Shared)**

**Role**: Both actors collaborate in patient care, especially in complex workflows.

* **Task/Workflow Step**: When engaging with patients, support shared decision-making.  
  * **CDS Use Case 3.1.1**: Shared Decision-Making Support  
    * Provides patient-specific recommendations incorporating preferences or SDOH, often via SMART on FHIR apps.  
* **Task/Workflow Step**: During patient encounters, provide real-time alerts for safety.  
  * **CDS Use Case 1.2.3**: Adverse Event Monitoring  
    * Alerts for potential adverse events relevant to both clinical roles.  
  * **CDS Use Case 1.1.8**: Value-Based Care Alerts  
    * Notifies both actors of preventive care or quality metric opportunities.  
* **Task/Workflow Step**: During clinical documentation, reduce manual effort and ensure compliance.  
  * **CDS Use Case 4.3.1**: Documentation Support  
    * Uses clinical knowledge to prompt for missing regulatory, billing, or clinical details while assisting with note completion. 

## **4\. Care Manager**

**Role**: Manages population health, case management, and quality reporting.

* **Task/Workflow Step**: When analyzing population data, identify patients for intervention.  
  * **CDS Use Case 2.1.1**: Case Management  
    * Identifies patients needing ongoing monitoring (e.g., chronic disease management).  
  * **CDS Use Case 2.3.1**: Risk Stratification  
    * Uses predictive analytics to identify high-risk patients for targeted interventions.  
* **Task/Workflow Step**: When reporting quality metrics, ensure compliance with standards.  
  * **CDS Use Case 2.2.1**: Quality Metrics Reporting  
    * Supports electronic Clinical Quality Measures (eCQMs) for population-level quality tracking.

## **5\. Patient**

**Role**: Engages in shared decision-making and receives tailored guidance.

* **Task/Workflow Step**: When accessing health information, receive personalized guidance.  
  * **CDS Use Case 3.3.1**: Patient Education and Reminders  
    * Delivers tailored education or reminders (e.g., vaccination schedules) via patient portals.  
  * **CDS Use Case 3.1.1**: Shared Decision-Making Support  
    * Provides patient-specific recommendations incorporating preferences or SDOH.

## **6\. Health IT System**

**Role**: Automates CDS processes and supports interoperability across systems.

* **Task/Workflow Step**: When queried, provide guideline-driven information.  
  * **CDS Use Case 4.1**: Guideline-Driven Information Retrieval  
    * Enables on-demand access to evidence-based guidelines via CDS Hooks or FHIR Clinical Reasoning.  
* **Task/Workflow Step**: When triggered by events, automate reporting or alerts.  
  * **CDS Use Case 2.4.1**: Public Health Reporting  
    * Automates case reporting for infectious diseases or public health surveillance.  
  * **CDS Use Case 4.4.1**: Care Coordination Alerts  
    * Generates notifications for care transitions across systems.

### Additional cases to be categorized:  

### Move Personas to a separate Doc or more formal personas link to this doc

### APP (Advanced Practice Practitioner)

Most of the same ones as Provider (unless APP is restricted on certain decisions based on Country Regulations. In the US they can prescribe and order most tests

### Care Manager (often Nurse/MPH)

Worklists based on CDS rules run against population

### Caregiver Information Retrieval

I want to lookup learn by condition  
I want to lookup (knowledge) for this patient (Best Practice)

### Clinical Quality Measures

1. Measuring Evidence based care  
   1. Behavior Change for CDS  
   2. Concordance with guidance  
   3. Outcomes for these sub-branches (combinations of changed behavior / followed guidance / clinical outcomes  
2. Broad Accepted Measures  
   1. NCQA HEDIS  
   2. CMS MIPS  
   3. UK / EU \- NICE, QOF

### Patient

1. Information Lookup \- how to treat (condition), what does this lab test mean. How to manage comorbid conditions (not searched using that word, but “I have both…”   
- Drug lookup ([Drugs.com](http://Drugs.com) or [medscape.com](http://medscape.com)) \- AI has made this much more than information retrieval. They now ask sophisticated questions. I have migraines and sleep issues. What medication or diet change would help with both? 

BMJ \- BP \- Patient Summaries (similar are printed for patients on discharge from hospital or in a visit the doctor orders it within the EHR) 

Other (to be categorized)

* Authoring (aka codification of policies) and sharing of **Clinical Practice Guidelines (CPGs)**  
* Automating **Prior Authorization (PA)**  
* Conducting prospective **Care Gaps Management**  
* Running real-time **Quality Measures (eCQMs, dQMs)**  
* Delivering **Cognitive Support**

## Others to evaluate or categorize

* Financial data analyst at a value based care organization  
* Provider with a clinical hypothesis \- I think we are seeing an increase of X, if we do Y we will improve quality, costs or both  
* I think something is wrong with the guideline itself \- please change it  
* All of the internal roles in the production, maintenance, quality, deployment and operationalization of the knowledge  
  * Authoring roles  
  * Quality roles


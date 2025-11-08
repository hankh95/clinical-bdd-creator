# Expected Outcomes — RobertJohnson_Afib_CPOE_Obese

## Extracted from legacy FSH comments

- Treatment (BDD-style commented expectation):

## Derived from legacy YAML notes

Summary: This patient (70-year-old male with newly diagnosed atrial fibrillation, COPD treated with tiotropium inhaler, and obesity with BMI 35) is meant to test CIKG v8's handling of AFib guidelines (e.g., AHA/ACC), considering comorbidities. Specifically: L1 semantic relationships (e.g., AFib increasesRiskOf stroke, treatedWith anticoagulation; COPD treatedWith LAMA inhaler); L2 reusable logic (e.g., CHA2DS2-VASc score for stroke risk stratification prompting anticoagulation, goals for rate control avoiding beta-blockers due to COPD); L3 workflows (e.g., temporal sequencing for initiating DOAC anticoagulation, rhythm/rate control, and lifestyle interventions for obesity); and CDS use cases like Treatment Recommendation (prefer apixaban over warfarin for obese patients, diltiazem for rate control in COPD), Risk Stratification (high CHA2DS2-VASc due to age/obesity), and Next Best Action (monitor for bleeding risk).
Expected Treatment (BDD-style commented expectation):
Given newly diagnosed AFib with COPD and obesity,
When evaluating per guidelines,
Then recommend:
- Anticoagulation with DOAC (e.g., apixaban, adjusted for obesity/renal function) for stroke prevention (CHA2DS2-VASc >=2).
- Rate control with non-beta-blocker (e.g., diltiazem) due to COPD.
- Continue COPD management with tiotropium; assess for rhythm control if symptomatic.
- Lifestyle interventions for obesity (weight loss, exercise).
- Monitor HR, bleeding, and cardiorenal status over 3-6 months.

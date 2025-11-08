// Summary: This patient (70-year-old male with newly diagnosed atrial fibrillation, COPD treated with tiotropium inhaler, and obesity with BMI 35) is meant to test CIKG v8's handling of AFib guidelines (e.g., AHA/ACC), considering comorbidities. Specifically: L1 semantic relationships (e.g., AFib increasesRiskOf stroke, treatedWith anticoagulation; COPD treatedWith LAMA inhaler); L2 reusable logic (e.g., CHA2DS2-VASc score for stroke risk stratification prompting anticoagulation, goals for rate control avoiding beta-blockers due to COPD); L3 workflows (e.g., temporal sequencing for initiating DOAC anticoagulation, rhythm/rate control, and lifestyle interventions for obesity); and CDS use cases like Treatment Recommendation (prefer apixaban over warfarin for obese patients, diltiazem for rate control in COPD), Risk Stratification (high CHA2DS2-VASc due to age/obesity), and Next Best Action (monitor for bleeding risk).

// Expected Treatment (BDD-style commented expectation):
// Given newly diagnosed AFib with COPD and obesity,
// When evaluating per guidelines,
// Then recommend: 
// - Anticoagulation with DOAC (e.g., apixaban, adjusted for obesity/renal function) for stroke prevention (CHA2DS2-VASc >=2).
// - Rate control with non-beta-blocker (e.g., diltiazem) due to COPD.
// - Continue COPD management with tiotropium; assess for rhythm control if symptomatic.
// - Lifestyle interventions for obesity (weight loss, exercise).
// - Monitor HR, bleeding, and cardiorenal status over 3-6 months.

Alias: Example = http://example.org
Alias: SNOMED = http://snomed.info/sct
Alias: LOINC = http://loinc.org
Alias: RXNORM = http://www.nlm.nih.gov/research/umls/rxnorm
Alias: ICD10 = http://hl7.org/fhir/sid/icd-10

Instance: RobertJohnsonBundle
InstanceOf: Bundle
Description: "FHIR Bundle for patient Robert Johnson, simulating newly diagnosed AFib with COPD (on tiotropium) and obesity for testing CIKG v8 recommendations."
* type = #collection
* timestamp = "2025-09-04T00:00:00Z"
* entry[+].resource = RobertJohnsonPatient
* entry[+].resource = AtrialFibrillationCondition
* entry[+].resource = COPDCondition
* entry[+].resource = ObesityCondition
* entry[+].resource = HeightObservation
* entry[+].resource = WeightObservation
* entry[+].resource = BMIObservation
* entry[+].resource = HeartRateObservation
* entry[+].resource = TiotropiumRequest
* entry[+].resource = AFibManagementCarePlan

Instance: RobertJohnsonPatient
InstanceOf: Patient
* identifier[0].system = "http://example.org/mrn"
* identifier[0].value = "3000303"
* name[0].family = "Johnson"
* name[0].given[0] = "Robert"
* gender = #male
* birthDate = "1955-09-04"  // Age 70 as of 2025-09-04

Instance: AtrialFibrillationCondition
InstanceOf: Condition
* subject = Reference(RobertJohnsonPatient)
* code.coding[0].system = ICD10
* code.coding[0].code = "I48.91"
* code.coding[+].system = SNOMED
* code.coding[=].code = "49436004"
* code.text = "Atrial fibrillation (newly diagnosed)"
* onsetDateTime = "2025-08-15"  // Recent diagnosis
* clinicalStatus.coding.system = "http://terminology.hl7.org/CodeSystem/condition-clinical"
* clinicalStatus.coding.code = "active"

Instance: COPDCondition
InstanceOf: Condition
* subject = Reference(RobertJohnsonPatient)
* code.coding[0].system = ICD10
* code.coding[0].code = "J44.9"
* code.coding[+].system = SNOMED
* code.coding[=].code = "13645005"
* code.text = "Chronic obstructive pulmonary disease"
* onsetDateTime = "2020-01-01"
* clinicalStatus.coding.system = "http://terminology.hl7.org/CodeSystem/condition-clinical"
* clinicalStatus.coding.code = "active"

Instance: ObesityCondition
InstanceOf: Condition
* subject = Reference(RobertJohnsonPatient)
* code.coding[0].system = ICD10
* code.coding[0].code = "E66.9"
* code.coding[+].system = SNOMED
* code.coding[=].code = "414916001"
* code.text = "Obesity"
* onsetDateTime = "2015-01-01"
* clinicalStatus.coding.system = "http://terminology.hl7.org/CodeSystem/condition-clinical"
* clinicalStatus.coding.code = "active"

Instance: HeightObservation
InstanceOf: Observation
* status = #final
* subject = Reference(RobertJohnsonPatient)
* effectiveDateTime = "2025-09-04"
* code.coding.system = LOINC
* code.coding.code = "8302-2"
* code.text = "Body height"
* valueQuantity.value = 170
* valueQuantity.unit = "cm"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "cm"

Instance: WeightObservation
InstanceOf: Observation
* status = #final
* subject = Reference(RobertJohnsonPatient)
* effectiveDateTime = "2025-09-04"
* code.coding.system = LOINC
* code.coding.code = "29463-7"
* code.text = "Body weight"
* valueQuantity.value = 102
* valueQuantity.unit = "kg"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "kg"

Instance: BMIObservation
InstanceOf: Observation
* status = #final
* subject = Reference(RobertJohnsonPatient)
* effectiveDateTime = "2025-09-04"
* code.coding.system = LOINC
* code.coding.code = "39156-5"
* code.text = "Body mass index (BMI) [Ratio]"
* valueQuantity.value = 35.3  // Obese (BMI >30)
* valueQuantity.unit = "kg/m2"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "kg/m2"

Instance: HeartRateObservation
InstanceOf: Observation
* status = #final
* subject = Reference(RobertJohnsonPatient)
* effectiveDateTime = "2025-09-04"
* code.coding.system = LOINC
* code.coding.code = "8867-4"
* code.text = "Heart rate"
* valueQuantity.value = 110
* valueQuantity.unit = "/min"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "/min"  // Irregularly irregular, elevated for AFib

Instance: TiotropiumRequest
InstanceOf: MedicationRequest
* status = #active
* intent = #order
* subject = Reference(RobertJohnsonPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "155200"  // Tiotropium (common LAMA for COPD)
* medicationCodeableConcept.text = "Tiotropium inhalation"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "447052006"  // Inhalation
* dosageInstruction[0].route.text = "Inhalation"
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 18
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mcg"
* dosageInstruction[0].doseAndRate[0].doseQuantity.system = "http://unitsofmeasure.org"
* dosageInstruction[0].doseAndRate[0].doseQuantity.code = "ug"
* authoredOn = "2025-09-04"

Instance: AFibManagementCarePlan
InstanceOf: CarePlan
* status = #draft  // Simulated for testing workflow initiation
* intent = #proposal
* subject = Reference(RobertJohnsonPatient)
* title = "Management for Newly Diagnosed Atrial Fibrillation with COPD and Obesity"
* description = "Initiate evaluation and treatment per guidelines for AFib in comorbid patient; test CIKG for appropriate anticoagulation and rate control recommendations."
* period.start = "2025-09-04"
* activity[+].detail.kind = #ServiceRequest
* activity[=].detail.code.text = "Assess CHA2DS2-VASc, initiate anticoagulation and rate control avoiding beta-blockers"
* activity[=].detail.status = #in-progress
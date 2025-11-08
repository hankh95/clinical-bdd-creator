// Summary: This patient (67-year-old male with metastatic castration-resistant prostate cancer [mCRPC], history of prostatectomy, radiation, hormone therapy failure, rising PSA, bone metastases, and enrollment in SWOG 0421 trial with docetaxel-based regimen) is meant to test CIKG v8's handling of NCCN/AUA guidelines for advanced prostate cancer. Specifically: L1 semantic relationships (e.g., prostate cancer treatedWith docetaxel, increasesRiskOf bone mets); L2 reusable logic (e.g., PSA monitoring goals, Gleason score risk stratification via CQL, measures for disease progression); L3 workflows (e.g., temporal sequencing post-hormone failure: trial enrollment, chemo cycles q3w, bisphosphonate for bone health); and CDS use cases like Treatment Recommendation (docetaxel for symptomatic mCRPC), Risk Stratification (high Gleason 8 prompting aggressive therapy), and Diagnostic Test Recommendation (serial PSA/bone scans).

// Expected Recommendations (BDD-style commented expectation, verified per NCCN Prostate Cancer guidelines and SWOG 0421 details):
// Given mCRPC with bone mets and trial enrollment,
// When managing per guidelines,
// Then recommend: 
// - Continue zoledronic acid 4 mg IV q4w for bone health.
// - Administer docetaxel 75 mg/m² IV q3w + prednisone 5 mg PO BID (per trial; atrasentan/placebo randomized).
// - Monitor PSA q3-6 months, bone scans/CT as needed for progression.
// - Pain management with hydrocodone as required.
// - Consider denosumab alternative if renal issues; radium-223 for symptomatic bone mets if progression.

Alias: Example = http://example.org
Alias: SNOMED = http://snomed.info/sct
Alias: LOINC = http://loinc.org
Alias: RXNORM = http://www.nlm.nih.gov/research/umls/rxnorm
Alias: ICD10 = http://hl7.org/fhir/sid/icd-10

Instance: AdamEverymanBundle
InstanceOf: Bundle
Description: "FHIR Bundle for patient Adam Everyman, simulating mCRPC with treatment history for testing CIKG v8 prostate cancer guidelines."
* type = #collection
* timestamp = "2011-05-01T00:00:00Z"  // Approximate trial enrollment date
* entry[+].resource = AdamEverymanPatient
* entry[+].resource = ProstateCancerCondition
* entry[+].resource = BoneMetastasesCondition
* entry[+].resource = HeightObservation
* entry[+].resource = WeightObservation
* entry[+].resource = PSAObservationInitial
* entry[+].resource = PSAObservationPostOp
* entry[+].resource = PSAObservationNadir
* entry[+].resource = PSAObservationRising1
* entry[+].resource = PSAObservationRising2
* entry[+].resource = PSAObservationRising3
* entry[+].resource = PSAObservationRising4
* entry[+].resource = PSAObservationRising5
* entry[+].resource = BoneScanObservation
* entry[+].resource = CTScanObservation
* entry[+].resource = ProstatectomyProcedure
* entry[+].resource = RadiationTherapyProcedure
* entry[+].resource = GoserelinRequest
* entry[+].resource = BicalutamideRequest
* entry[+].resource = HydrocodoneRequest
* entry[+].resource = ZoledronicAcidRequest
* entry[+].resource = DocetaxelRequest  // Trial drug
* entry[+].resource = ProstateCancerCarePlan

Instance: AdamEverymanPatient
InstanceOf: Patient
* identifier[0].system = "http://example.org/mrn"
* identifier[0].value = "4000404"
* name[0].family = "Everyman"
* name[0].given[0] = "Adam"
* gender = #male
* birthDate = "1944-05-01"  // Age 67 in 2011

Instance: ProstateCancerCondition
InstanceOf: Condition
* subject = Reference(AdamEverymanPatient)
* code.coding[0].system = ICD10
* code.coding[0].code = "C61"
* code.coding[+].system = SNOMED
* code.coding[=].code = "126906006"  // Neoplasm of prostate
* code.text = "Metastatic hormone-refractory prostate cancer (Stage IV, T3N1M0, Gleason 4+4)"
* onsetDateTime = "2008-04-12"
* clinicalStatus.coding.system = "http://terminology.hl7.org/CodeSystem/condition-clinical"
* clinicalStatus.coding.code = "active"
* stage[0].summary.coding.system = SNOMED
* stage[0].summary.coding.code = "261638004"
* stage[0].summary.text = "Stage IV"
* note.text = "Gleason grade 4+4; castration-resistant"

Instance: BoneMetastasesCondition
InstanceOf: Condition
* subject = Reference(AdamEverymanPatient)
* code.coding.system = SNOMED
* code.coding.code = "94222008"
* code.text = "Secondary malignant neoplasm of bone"
* onsetDateTime = "2011-04-24"
* clinicalStatus.coding.system = "http://terminology.hl7.org/CodeSystem/condition-clinical"
* clinicalStatus.coding.code = "active"
* bodySite[0].coding.system = SNOMED
* bodySite[0].coding.code = "73438004"  // Rib
* bodySite[0].text = "Left anterior 5th/8th ribs, posterior left 9th rib, right anterior 4th/7th ribs, T3/T9/L2"

Instance: HeightObservation
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-05-01"
* code.coding.system = LOINC
* code.coding.code = "8302-2"
* code.text = "Body height"
* valueQuantity.value = 173
* valueQuantity.unit = "cm"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "cm"

Instance: WeightObservation
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-05-01"
* code.coding.system = LOINC
* code.coding.code = "29463-7"
* code.text = "Body weight"
* valueQuantity.value = 81
* valueQuantity.unit = "kg"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "kg"

Instance: PSAObservationInitial
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2008-04-03"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* code.text = "Prostate specific Ag [Mass/volume] in Serum or Plasma"
* valueQuantity.value = 4.7
* valueQuantity.unit = "ng/mL"
* valueQuantity.system = "http://unitsofmeasure.org"
* valueQuantity.code = "ng/mL"

Instance: PSAObservationPostOp
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2008-05-26"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 0.8
* valueQuantity.unit = "ng/mL"

Instance: PSAObservationNadir
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2008-10-15"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 0.01
* valueQuantity.unit = "ng/mL"
* valueQuantity.comparator = #<

Instance: PSAObservationRising1
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2009-09-22"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 0.02
* valueQuantity.unit = "ng/mL"

Instance: PSAObservationRising2
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2009-10-19"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 0.04
* valueQuantity.unit = "ng/mL"

Instance: PSAObservationRising3
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2009-12-23"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 1.2
* valueQuantity.unit = "ng/mL"

Instance: PSAObservationRising4
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-02-27"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 3.6
* valueQuantity.unit = "ng/mL"

Instance: PSAObservationRising5
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-04-06"
* code.coding.system = LOINC
* code.coding.code = "2857-1"
* valueQuantity.value = 7.9
* valueQuantity.unit = "ng/mL"

Instance: BoneScanObservation
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-04-24"
* code.coding.system = LOINC
* code.coding.code = "39126-8"
* code.text = "Bone scan"
* valueCodeableConcept.text = "Increased uptake at left anterior 5th/8th ribs, posterior left 9th rib, right anterior 4th/7th ribs, T3, T9, L2"

Instance: CTScanObservation
InstanceOf: Observation
* status = #final
* subject = Reference(AdamEverymanPatient)
* effectiveDateTime = "2011-04-26"
* code.coding.system = LOINC
* code.coding.code = "70979-3"
* code.text = "CT Chest and Abdomen and Pelvis WO contrast"
* valueCodeableConcept.text = "Normal"

Instance: ProstatectomyProcedure
InstanceOf: Procedure
* status = #completed
* subject = Reference(AdamEverymanPatient)
* code.coding.system = SNOMED
* code.coding.code = "26294005"
* code.text = "Radical prostatectomy"
* performedDateTime = "2008-04-12"
* note.text = "Margins microscopically involved; 1/12 positive lymph nodes"

Instance: RadiationTherapyProcedure
InstanceOf: Procedure
* status = #completed
* subject = Reference(AdamEverymanPatient)
* code.coding.system = SNOMED
* code.coding.code = "33195004"
* code.text = "External beam radiation therapy procedure"
* performedPeriod.start = "2008-06-15"
* performedPeriod.end = "2008-08-03"
* note.text = "5000 cGy to whole pelvis + 1800 cGy boost to prostatic bed"

Instance: GoserelinRequest
InstanceOf: MedicationRequest
* status = #completed
* intent = #order
* subject = Reference(AdamEverymanPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "1115490"
* medicationCodeableConcept.text = "Goserelin"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "34206005"
* dosageInstruction[0].route.text = "Subcutaneous"
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 10.8
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mg"
* dosageInstruction[0].timing.repeat.frequency = 1
* dosageInstruction[0].timing.repeat.period = 12
* dosageInstruction[0].timing.repeat.periodUnit = #wk
* authoredOn = "2010-01-12"

Instance: BicalutamideRequest
InstanceOf: MedicationRequest
* status = #stopped
* intent = #order
* subject = Reference(AdamEverymanPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "194508"
* medicationCodeableConcept.text = "Bicalutamide"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "26643006"
* dosageInstruction[0].route.text = "Oral"
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 50
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mg"
* dosageInstruction[0].timing.repeat.frequency = 1
* dosageInstruction[0].timing.repeat.period = 1
* dosageInstruction[0].timing.repeat.periodUnit = #d
* authoredOn = "2010-10-19"
* dispenseRequest.validityPeriod.end = "2011-01-22"  // Stopped

Instance: HydrocodoneRequest
InstanceOf: MedicationRequest
* status = #active
* intent = #order
* subject = Reference(AdamEverymanPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "856903"
* medicationCodeableConcept.text = "Hydrocodone"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "26643006"
* dosageInstruction[0].route.text = "Oral"
* authoredOn = "2011-04-06"

Instance: ZoledronicAcidRequest
InstanceOf: MedicationRequest
* status = #active
* intent = #order
* subject = Reference(AdamEverymanPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "1546263"
* medicationCodeableConcept.text = "Zoledronic acid"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "47625008"
* dosageInstruction[0].route.text = "Intravenous"
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 4
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mg"
* dosageInstruction[0].timing.repeat.frequency = 1
* dosageInstruction[0].timing.repeat.period = 4
* dosageInstruction[0].timing.repeat.periodUnit = #wk
* authoredOn = "2011-04-24"

Instance: DocetaxelRequest
InstanceOf: MedicationRequest
* status = #active
* intent = #order
* subject = Reference(AdamEverymanPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = "1736374"
* medicationCodeableConcept.text = "Docetaxel"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = "47625008"
* dosageInstruction[0].route.text = "Intravenous"
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 75  // Standard per trial
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mg/m2"
* dosageInstruction[0].timing.repeat.frequency = 1
* dosageInstruction[0].timing.repeat.period = 3
* dosageInstruction[0].timing.repeat.periodUnit = #wk
* authoredOn = "2011-05-01"

Instance: ProstateCancerCarePlan
InstanceOf: CarePlan
* status = #active
* intent = #plan
* subject = Reference(AdamEverymanPatient)
* title = "Management for Metastatic Castration-Resistant Prostate Cancer"
* description = "Enrolled in SWOG 0421 trial: Docetaxel + Atrasentan/Placebo; monitor PSA, bone health, and symptoms."
* period.start = "2011-05-01"
* activity[+].detail.kind = #MedicationRequest
* activity[=].detail.reference = Reference(DocetaxelRequest)
* activity[+].detail.kind = #MedicationRequest
* activity[=].detail.reference = Reference(ZoledronicAcidRequest)
* activity[+].detail.kind = #ServiceRequest
* activity[=].detail.code.text = "Serial PSA monitoring and imaging for progression"
* activity[=].detail.status = #in-progress
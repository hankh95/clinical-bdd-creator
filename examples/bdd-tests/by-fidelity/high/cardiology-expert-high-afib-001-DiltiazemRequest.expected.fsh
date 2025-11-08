Alias: RXNORM = http://www.nlm.nih.gov/research/umls/rxnorm
Alias: SNOMED = http://snomed.info/sct
Alias: UCUM = http://unitsofmeasure.org

Instance: DiltiazemRequest
InstanceOf: MedicationRequest
* status = #active
* intent = #order
* subject = Reference(RobertJohnsonPatient)
* medicationCodeableConcept.coding.system = RXNORM
* medicationCodeableConcept.coding.code = #34366
* medicationCodeableConcept.text = "Diltiazem 120 mg extended-release capsule"
* dosageInstruction[0].route.coding.system = SNOMED
* dosageInstruction[0].route.coding.code = #26643006
* dosageInstruction[0].doseAndRate[0].doseQuantity.value = 120
* dosageInstruction[0].doseAndRate[0].doseQuantity.unit = "mg"
* dosageInstruction[0].doseAndRate[0].doseQuantity.system = UCUM
* dosageInstruction[0].timing.repeat.frequency = 1
* dosageInstruction[0].timing.repeat.period = 1
* dosageInstruction[0].timing.repeat.periodUnit = #d
* authoredOn = "2025-09-04"
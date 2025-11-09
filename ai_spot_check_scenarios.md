# Clinical Decision Support (CDS) Test Scenarios - AI Review

This document contains 20 clinical test scenarios generated from our BDD test creation system. Each scenario represents a provider decision-making situation based on CDS usage scenarios and clinical guidelines.

**Instructions for AI Reviewer:**
Please review each clinical situation and provide the most appropriate clinical decision/action. Consider:
- What treatment/test should the provider order?
- What are the next steps in patient management?
- What clinical reasoning supports the decision?

Fill in the "AI Recommended Action" column with your clinical recommendation. Return the completed markdown table.

## Test Scenarios

| Scenario ID | Clinical Context (GIVEN/WHEN) | AI Recommended Action |
|-------------|------------------------------|----------------------|
| ACC-AFIB-001 | GIVEN a 65-year-old patient with newly diagnosed atrial fibrillation AND no significant comorbidities<br>WHEN assessing stroke risk and anticoagulation needs | |
| ACC-AFIB-002 | GIVEN a patient with atrial fibrillation AND CHA2DS2-VASc score of 3<br>WHEN deciding on anticoagulation strategy | |
| ACC-AFIB-003 | GIVEN a patient with atrial fibrillation AND high bleeding risk (HAS-BLED score ≥3)<br>WHEN selecting anticoagulation therapy | |
| ACC-AFIB-004 | GIVEN a patient with atrial fibrillation AND recent ischemic stroke<br>WHEN determining urgent anticoagulation needs | |
| ACC-AFIB-005 | GIVEN a patient with atrial fibrillation AND planned electrical cardioversion<br>WHEN preparing for procedure | |
| HODGKINS-001 | GIVEN a 28-year-old patient with stage II Hodgkin's lymphoma<br>WHEN planning initial chemotherapy regimen | |
| HODGKINS-002 | GIVEN a patient with Hodgkin's lymphoma AND bulky mediastinal disease<br>WHEN deciding on radiation therapy | |
| HODGKINS-003 | GIVEN a patient completing ABVD chemotherapy for Hodgkin's lymphoma<br>WHEN planning response assessment | |
| HODGKINS-004 | GIVEN a patient with relapsed Hodgkin's lymphoma<br>WHEN considering salvage therapy options | |
| HODGKINS-005 | GIVEN a patient with Hodgkin's lymphoma AND treatment-related cardiotoxicity<br>WHEN modifying treatment plan | |
| DIABETES-001 | GIVEN a 55-year-old patient with newly diagnosed type 2 diabetes AND HbA1c 9.2%<br>WHEN initiating glucose-lowering therapy | |
| DIABETES-002 | GIVEN a patient with type 2 diabetes AND diabetic nephropathy (eGFR 45 mL/min)<br>WHEN selecting appropriate medications | |
| DIABETES-003 | GIVEN a patient with type 2 diabetes AND recent cardiovascular event<br>WHEN managing cardiovascular risk | |
| DIABETES-004 | GIVEN a patient with type 2 diabetes AND obesity (BMI 35)<br>WHEN planning comprehensive management | |
| DIABETES-005 | GIVEN a patient with type 2 diabetes AND hypoglycemia unawareness<br>WHEN adjusting treatment regimen | |
| DIABETES-006 | GIVEN a 12-year-old patient with newly diagnosed type 2 diabetes<br>WHEN planning initial treatment approach | |
| DIABETES-007 | GIVEN a pregnant patient with gestational diabetes<br>WHEN managing blood glucose during pregnancy | |
| DIABETES-008 | GIVEN a patient with type 1 diabetes AND frequent hypoglycemia<br>WHEN optimizing insulin regimen | |
| DIABETES-009 | GIVEN a patient with diabetes AND severe hyperglycemia (glucose 400 mg/dL)<br>WHEN providing urgent management | |
| DIABETES-010 | GIVEN a patient with diabetes AND peripheral neuropathy<br>WHEN planning preventive care | |

## CDS Usage Scenario Coverage

These scenarios test the following CDS usage scenarios:
- **1.1.2**: What treatment should I order?
- **1.1.3**: What medication should I order?
- **1.1.5**: What test should I order?
- **1.1.7**: What are the next steps?
- **1.2.3**: What should I think about (monitoring)?

## Expected Quality Metrics

- **Clinical Relevance**: Scenarios should reflect real provider decision points
- **CDS Alignment**: Actions should map to appropriate CDS usage scenarios
- **Specialty Appropriateness**: Cardiology, oncology, and endocrinology contexts
- **Decision Complexity**: Mix of straightforward and complex clinical situations</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/clinical-bdd-creator/ai_spot_check_scenarios.md
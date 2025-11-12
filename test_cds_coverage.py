#!/usr/bin/env python3
"""
Test script for expanded CDS scenario coverage in GuidelineAnalyzer
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import guideline_analyzer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from guideline_analyzer import GuidelineAnalyzer

def test_cds_scenario_coverage():
    """Test that GuidelineAnalyzer now detects all 23 CDS scenarios"""

    analyzer = GuidelineAnalyzer()

    # Test with mock guideline content that should trigger all CDS scenarios
    test_guideline = """
    For patients with atrial fibrillation, recommend anticoagulation with DOAC.
    For patients with atrial fibrillation and high bleeding risk, recommend anticoagulation with warfarin.
    Order CHA2DS2-VASc score for stroke risk assessment.
    Monitor patients with atrial fibrillation for bleeding complications.
    Consider differential diagnosis including atrial flutter and other supraventricular tachycardias.
    Assess for drug interactions with warfarin and common medications.
    Test is appropriate for patients with symptoms suggestive of atrial fibrillation.
    For patients with Hodgkin's lymphoma stage I-II, recommend ABVD chemotherapy.
    For patients with Hodgkin's lymphoma stage III-IV, recommend escalated BEACOPP chemotherapy.
    Order PET-CT scan for staging and response assessment.
    Monitor patients with Hodgkin's lymphoma for treatment response.
    Consider differential diagnosis including non-Hodgkin lymphoma and other malignancies.
    Assess for drug interactions with chemotherapy agents and supportive medications.
    Contraindicated in patients with severe cardiac dysfunction.
    Order genetic testing for BRCA mutations in high-risk patients.
    Evaluate next best steps for complex cases requiring multidisciplinary care.
    Recommend cardiac rehabilitation for heart failure patients.
    Consider quality metrics for anticoagulation therapy.
    Discuss treatment options with patient.
    Assess social determinants for medication adherence.
    Follow protocol for anticoagulation management.
    Document anticoagulation plan in the record.
    Coordinate care for complex atrial fibrillation cases.
    Recommend lifestyle modifications for all patients.
    Counsel patients about smoking cessation and diet.
    Provide education on diabetes management.
    Refer to case management for high-risk patients.
    Manage complex cases with multidisciplinary teams.
    Track quality measures for hypertension control.
    Report quality outcomes for diabetes management.
    Assess risk for cardiovascular disease.
    Stratify patients by risk for stroke.
    Calculate risk score for heart failure.
    Report to public health for notifiable diseases.
    Notify authorities of communicable disease cases.
    Remind patients to schedule follow-up appointments.
    Schedule follow-up reminder for medication review.
    Send reminder for annual screening.
    Consult guideline for complex treatment decisions.
    Refer to guideline for diagnostic criteria.
    Review recommendations for cancer screening.
    """

    # Analyze the guideline
    analysis = analyzer.analyze_guideline("test_expanded_coverage", test_guideline)

    print("CDS Scenario Coverage Report:")
    print("=" * 50)

    total_scenarios = 0
    for scenario_type, count in analysis.coverage_report.items():
        print(f"{scenario_type.value}: {count} scenarios")
        total_scenarios += count

    print(f"Total scenarios detected: {total_scenarios}")
    print(f"Unique CDS categories covered: {len(analysis.coverage_report)}/23")

    # Check if we now cover all 23 scenarios
    expected_scenarios = {
        '1.1.1',  # DIFFERENTIAL_DX
        '1.1.2',  # TREATMENT_RECOMMENDATION
        '1.1.3',  # DRUG_RECOMMENDATION
        '1.1.4',  # CANCER_TREATMENT
        '1.1.5',  # DIAGNOSTIC_TEST
        '1.1.6',  # GENETIC_TEST
        '1.1.7',  # NEXT_BEST_ACTION
        '1.1.8',  # VALUE_BASED_CARE
        '1.1.9',  # LIFESTYLE_EDUCATION
        '1.2.1',  # DRUG_INTERACTION
        '1.2.2',  # TEST_APPROPRIATENESS
        '1.2.3',  # ADVERSE_EVENT
        '2.1.1',  # CASE_MANAGEMENT
        '2.2.1',  # QUALITY_METRICS
        '2.3.1',  # RISK_STRATIFICATION
        '2.4.1',  # PUBLIC_HEALTH_REPORTING
        '3.1.1',  # SHARED_DECISION_MAKING
        '3.2.1',  # SDOH_INTEGRATION
        '3.3.1',  # PATIENT_REMINDERS
        '4.1.1',  # GUIDELINE_RETRIEVAL
        '4.2.1',  # PROTOCOL_DRIVEN_CARE
        '4.3.1',  # DOCUMENTATION_SUPPORT
        '4.4.1',  # CARE_COORDINATION
    }

    covered_scenarios = {scenario.value for scenario in analysis.coverage_report.keys()}

    missing_scenarios = expected_scenarios - covered_scenarios
    if missing_scenarios:
        print(f"\n❌ Still missing scenarios: {sorted(missing_scenarios)}")
        return False
    else:
        print("\n✅ SUCCESS: All 23 CDS scenarios are now covered!")
        return True

if __name__ == "__main__":
    success = test_cds_scenario_coverage()
    sys.exit(0 if success else 1)
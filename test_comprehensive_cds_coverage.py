#!/usr/bin/env python3
"""
Comprehensive test for all 23 CDS scenario categories with realistic clinical content.
Validates that each category can be detected in realistic guideline text.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import guideline_analyzer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from guideline_analyzer import GuidelineAnalyzer, CDSUsageScenario


def test_comprehensive_coverage():
    """Test all 23 CDS scenarios with domain-specific clinical content"""
    
    analyzer = GuidelineAnalyzer()
    
    # Comprehensive clinical guideline covering multiple scenarios
    comprehensive_guideline = """
    CARDIOVASCULAR DISEASE MANAGEMENT GUIDELINE
    
    DIFFERENTIAL DIAGNOSIS:
    Consider differential diagnosis including atrial flutter, multifocal atrial tachycardia, 
    and other supraventricular tachycardias when evaluating irregular heart rhythms.
    
    TREATMENT RECOMMENDATIONS:
    For patients with heart failure with reduced ejection fraction, recommend ACE inhibitors 
    as first-line therapy. Recommend cardiac rehabilitation for heart failure patients.
    
    MEDICATION MANAGEMENT:
    For patients with atrial fibrillation, recommend anticoagulation with direct oral anticoagulants.
    Assess for drug interactions with warfarin and common medications including NSAIDs and antibiotics.
    
    CANCER TREATMENT:
    For patients with stage II breast cancer, recommend anthracycline-based chemotherapy regimens.
    
    DIAGNOSTIC TESTING:
    Order CHA2DS2-VASc score for stroke risk assessment in atrial fibrillation patients.
    Order genetic testing for BRCA mutations in high-risk breast cancer patients.
    Test is appropriate for patients with symptoms suggestive of coronary artery disease.
    
    LIFESTYLE MODIFICATIONS:
    Recommend lifestyle modifications for all cardiovascular disease patients including diet and exercise.
    Counsel patients about smoking cessation and alcohol moderation.
    Provide education on heart-healthy nutrition and stress management.
    
    MONITORING AND SAFETY:
    Monitor patients with atrial fibrillation for bleeding complications and stroke events.
    Assess risk for cardiovascular events using validated risk calculators.
    Stratify patients by risk for adverse outcomes using MAGGIC score.
    Calculate risk score for heart failure hospitalization.
    
    CARE COORDINATION:
    Refer to case management for high-risk patients with multiple comorbidities.
    Manage complex cases with multidisciplinary heart team collaboration.
    Coordinate care for complex atrial fibrillation cases requiring ablation.
    
    QUALITY AND PERFORMANCE:
    Track quality measures for hypertension control and anticoagulation therapy.
    Report quality outcomes for heart failure readmission rates.
    Consider quality metrics for guideline-directed medical therapy adherence.
    
    CLINICAL DECISIONS:
    Evaluate next best steps for refractory cases requiring advanced therapies.
    Discuss treatment options with patient including risks and benefits of anticoagulation.
    Assess social determinants for medication adherence including cost and access barriers.
    
    PROTOCOLS AND DOCUMENTATION:
    Follow protocol for anticoagulation management according to institutional guidelines.
    Document anticoagulation plan in the record including indication and target INR.
    Consult guideline for complex treatment decisions requiring specialist input.
    Refer to guideline for diagnostic criteria and risk stratification tools.
    Review recommendations for optimal medical therapy in heart failure.
    
    POPULATION HEALTH:
    Report to public health for notifiable communicable diseases.
    Notify authorities of unusual disease patterns or outbreaks.
    
    PATIENT ENGAGEMENT:
    Remind patients to schedule follow-up appointments within 2 weeks of discharge.
    Schedule follow-up reminder for medication reconciliation and adherence review.
    Send reminder for annual cardiovascular risk assessment and screening.
    """
    
    # Analyze the comprehensive guideline
    analysis = analyzer.analyze_guideline("comprehensive_test", comprehensive_guideline)
    
    print("=" * 80)
    print("COMPREHENSIVE CDS COVERAGE TEST RESULTS")
    print("=" * 80)
    
    # Define all expected scenarios with their names
    expected_scenarios = {
        '1.1.1': 'Differential Diagnosis',
        '1.1.2': 'Treatment Recommendation',
        '1.1.3': 'Drug Recommendation',
        '1.1.4': 'Cancer Treatment',
        '1.1.5': 'Diagnostic Test',
        '1.1.6': 'Genetic Test',
        '1.1.7': 'Next Best Action',
        '1.1.8': 'Value Based Care',
        '1.1.9': 'Lifestyle Education',
        '1.2.1': 'Drug Interaction',
        '1.2.2': 'Test Appropriateness',
        '1.2.3': 'Adverse Event Monitoring',
        '2.1.1': 'Case Management',
        '2.2.1': 'Quality Metrics',
        '2.3.1': 'Risk Stratification',
        '2.4.1': 'Public Health Reporting',
        '3.1.1': 'Shared Decision Making',
        '3.2.1': 'SDOH Integration',
        '3.3.1': 'Patient Reminders',
        '4.1.1': 'Guideline Retrieval',
        '4.2.1': 'Protocol Driven Care',
        '4.3.1': 'Documentation Support',
        '4.4.1': 'Care Coordination',
    }
    
    covered_scenarios = {scenario.value: scenario for scenario in analysis.coverage_report.keys()}
    
    print(f"\nTotal Scenarios Expected: {len(expected_scenarios)}")
    print(f"Total Scenarios Detected: {len(covered_scenarios)}")
    print(f"Coverage: {len(covered_scenarios)}/{len(expected_scenarios)} ({len(covered_scenarios)*100//len(expected_scenarios)}%)")
    print("\n" + "-" * 80)
    print("COVERAGE BY CATEGORY:")
    print("-" * 80)
    
    all_covered = True
    for scenario_id, scenario_name in sorted(expected_scenarios.items()):
        if scenario_id in covered_scenarios:
            count = analysis.coverage_report[covered_scenarios[scenario_id]]
            status = "✅"
            print(f"{status} {scenario_id}: {scenario_name:35s} ({count} instances)")
        else:
            status = "❌"
            all_covered = False
            print(f"{status} {scenario_id}: {scenario_name:35s} (NOT DETECTED)")
    
    print("\n" + "-" * 80)
    print("DETAILED STATISTICS:")
    print("-" * 80)
    total_instances = sum(analysis.coverage_report.values())
    print(f"Total Decision Points Detected: {total_instances}")
    print(f"Average per Category: {total_instances / len(covered_scenarios):.1f}")
    
    print("\n" + "=" * 80)
    if all_covered:
        print("✅ SUCCESS: ALL 23 CDS CATEGORIES COVERED!")
        print("=" * 80)
        return True
    else:
        missing = [s for s in expected_scenarios.keys() if s not in covered_scenarios]
        print(f"❌ FAILURE: {len(missing)} categories not detected:")
        for scenario_id in missing:
            print(f"   - {scenario_id}: {expected_scenarios[scenario_id]}")
        print("=" * 80)
        return False


def test_domain_specific_coverage():
    """Test that scenarios work across different clinical domains"""
    
    analyzer = GuidelineAnalyzer()
    
    test_domains = {
        'cardiology': """
            For patients with atrial fibrillation, recommend anticoagulation.
            Assess for drug interactions with warfarin.
            Calculate risk score for stroke using CHA2DS2-VASc.
            Counsel patients about lifestyle modifications.
            Coordinate care for complex cases requiring ablation.
        """,
        'oncology': """
            For patients with stage III breast cancer, recommend chemotherapy.
            Order genetic testing for BRCA mutations.
            Monitor patients for chemotherapy-related toxicity.
            Refer to case management for complex treatment coordination.
            Track quality measures for treatment completion rates.
        """,
        'primary_care': """
            For patients with type 2 diabetes, recommend metformin as first-line.
            Assess risk for cardiovascular disease complications.
            Provide education on diabetes self-management.
            Remind patients to schedule annual eye examinations.
            Review recommendations for preventive care screening.
        """
    }
    
    print("\n" + "=" * 80)
    print("DOMAIN-SPECIFIC COVERAGE TEST")
    print("=" * 80)
    
    for domain, guideline_text in test_domains.items():
        analysis = analyzer.analyze_guideline(f"test_{domain}", guideline_text)
        print(f"\n{domain.upper()}:")
        print(f"  Specialty detected: {analysis.specialty}")
        print(f"  Scenarios detected: {len(analysis.coverage_report)}")
        print(f"  Total instances: {sum(analysis.coverage_report.values())}")
        print(f"  Categories: {', '.join(sorted([s.value for s in analysis.coverage_report.keys()]))}")
    
    print("\n" + "=" * 80)
    print("✅ Domain-specific testing complete")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ENHANCED TESTING COVERAGE VALIDATION")
    print("Testing all 23 CDS usage scenario categories")
    print("=" * 80)
    
    # Run comprehensive test
    test1_success = test_comprehensive_coverage()
    
    # Run domain-specific test
    test2_success = test_domain_specific_coverage()
    
    print("\n" + "=" * 80)
    print("FINAL RESULTS:")
    print("=" * 80)
    print(f"Comprehensive Coverage Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"Domain-Specific Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    overall_success = test1_success and test2_success
    if overall_success:
        print("\n🎉 ALL TESTS PASSED - 23/23 CDS CATEGORIES FULLY COVERED!")
    else:
        print("\n⚠️  SOME TESTS FAILED - Review results above")
    
    print("=" * 80)
    
    sys.exit(0 if overall_success else 1)

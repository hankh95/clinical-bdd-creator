#!/usr/bin/env python3
"""
Guideline Analysis Engine - Phase 1

Analyzes clinical guidelines to extract provider decision-making scenarios
based on CDS usage scenarios and FHIR-CPG conceptual framework.

Focus: What treatment/test to order, next steps, clinical reasoning.
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class CDSUsageScenario(Enum):
    """CDS Usage Scenarios focused on provider decisions"""
    TREATMENT_RECOMMENDATION = "1.1.2"  # What treatment should I order?
    DRUG_RECOMMENDATION = "1.1.3"       # What medication should I order?
    CANCER_TREATMENT = "1.1.4"          # What cancer therapy should I order?
    DIAGNOSTIC_TEST = "1.1.5"           # What test should I order?
    GENETIC_TEST = "1.1.6"              # What genetic test should I order?
    NEXT_BEST_ACTION = "1.1.7"          # What are the next steps?
    DIFFERENTIAL_DX = "1.1.1"           # What should I think about (diagnosis)?
    DRUG_INTERACTION = "1.2.1"          # What should I think about (safety)?
    TEST_APPROPRIATENESS = "1.2.2"      # What should I think about (appropriateness)?
    ADVERSE_EVENT = "1.2.3"             # What should I think about (monitoring)?

@dataclass
class ClinicalScenario:
    """Represents a clinical decision scenario extracted from guidelines"""
    scenario_id: str
    guideline_section: str
    patient_context: Dict[str, Any]
    clinical_observations: List[Dict[str, Any]]
    inferences: List[str]
    recommended_actions: List[Dict[str, Any]]
    cds_scenarios: List[CDSUsageScenario]
    combinatorial_factors: List[str]  # For complex multi-criteria decisions

@dataclass
class GuidelineAnalysis:
    """Complete analysis of a clinical guideline"""
    guideline_name: str
    specialty: str
    scenarios: List[ClinicalScenario]
    coverage_report: Dict[CDSUsageScenario, int]

class GuidelineAnalyzer:
    """
    Analyzes clinical guidelines to extract provider decision-making scenarios.
    Uses CDS usage scenarios to focus on:
    - What treatment/test should I order?
    - What are the next steps?
    - What should I think about?
    """

    def __init__(self):
        self.specialty_patterns = {
            'cardiology': re.compile(r'(?i)(heart|cardiac|atrial|ventricular|coronary|afib|arrhythmia)'),
            'oncology': re.compile(r'(?i)(cancer|tumor|carcinoma|lymphoma|leukemia|metastasis|chemotherapy)'),
            'endocrinology': re.compile(r'(?i)(diabetes|thyroid|hormone|endocrine|insulin)'),
            'pulmonology': re.compile(r'(?i)(lung|pulmonary|respiratory|asthma|copd)'),
        }
        self.specialty = "general"  # Default specialty

    def detect_specialty(self, text: str) -> str:
        """Detect medical specialty from guideline text"""
        for specialty, pattern in self.specialty_patterns.items():
            if pattern.search(text):
                return specialty
        return "general"

    def extract_decision_points(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract decision points from guideline text.

        Looks for patterns like:
        - "For patients with X, recommend Y"
        - "Recommend X for patients with Y"
        - "Order X for patients with Y"
        - "Monitor patients with X for Y"
        """
        decision_patterns = [
            # Simple treatment recommendations: "For patients with X, recommend Y"
            r'(?i)for patients with ([^,]*?), recommend ([^.]*?)\.',
            # Alternative: "Recommend X for patients with Y"
            r'(?i)recommend ([^.]*) for patients with ([^.]*?)\.',
            # Test ordering: "Order X for patients with Y"
            r'(?i)order ([^.]*) for patients with ([^.]*?)\.',
            # General test ordering: "Order X for Y"
            r'(?i)order ([^.]*) for ([^.]*?)\.',
            # Monitoring: "Monitor patients with X for Y"
            r'(?i)monitor patients with ([^,]*?) for ([^.]*?)\.',
        ]

        decisions = []
        for pattern in decision_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # For pattern "For patients with X, recommend Y": group 1 is condition, group 2 is action
                if 'for patients with' in pattern and 'recommend' in pattern:
                    decision = {
                        'action': match.group(2).strip(),
                        'patient_criteria': [match.group(1).strip()],
                        'context': text[max(0, match.start() - 100):match.end() + 100].strip()
                    }
                # For monitoring pattern "Monitor patients with X for Y": group 1 is condition, group 2 is what to monitor
                elif 'monitor patients with' in pattern:
                    decision = {
                        'action': f'monitor for {match.group(2).strip()}',
                        'patient_criteria': [match.group(1).strip()],
                        'context': text[max(0, match.start() - 100):match.end() + 100].strip()
                    }
                # For general ordering pattern "Order X for Y": group 1 is action, group 2 is criteria/purpose
                elif 'order' in pattern and pattern.count('patients with') == 0:
                    decision = {
                        'action': match.group(1).strip(),
                        'patient_criteria': [match.group(2).strip()],
                        'context': text[max(0, match.start() - 100):match.end() + 100].strip()
                    }
                else:
                    # For other patterns, assume group 1 is action, rest are criteria
                    decision = {
                        'action': match.group(1).strip(),
                        'patient_criteria': [g.strip() for g in match.groups()[1:] if g],
                        'context': text[max(0, match.start() - 100):match.end() + 100].strip()
                    }
                decisions.append(decision)

        return decisions

    def map_to_cds_scenarios(self, decision: Dict[str, Any]) -> List[CDSUsageScenario]:
        """Map extracted decisions to CDS usage scenarios"""
        action = decision['action'].lower()
        criteria = ' '.join(decision['patient_criteria']).lower()
        context = decision['context'].lower()

        scenarios = []

        # Treatment recommendations
        if any(word in action for word in ['treatment', 'therapy', 'medication', 'drug', 'chemotherapy', 'radiation', 'anticoagulation']):
            if 'cancer' in criteria or 'tumor' in criteria:
                scenarios.append(CDSUsageScenario.CANCER_TREATMENT)
            elif any(word in action for word in ['medication', 'drug', 'dose', 'prescribe', 'anticoagulation', 'warfarin', 'doac']):
                scenarios.append(CDSUsageScenario.DRUG_RECOMMENDATION)
            else:
                scenarios.append(CDSUsageScenario.TREATMENT_RECOMMENDATION)

        # Test ordering - check both action and context for ordering keywords
        if (any(word in action for word in ['order', 'perform', 'obtain']) or 
            any(word in context for word in ['order', 'perform', 'obtain'])) and \
           any(word in action for word in ['score', 'test', 'assessment', 'scan', 'ct', 'mri', 'lab', 'evaluation']):
            if 'genetic' in action or 'dna' in action:
                scenarios.append(CDSUsageScenario.GENETIC_TEST)
            else:
                scenarios.append(CDSUsageScenario.DIAGNOSTIC_TEST)

        # Monitoring/follow-up
        if any(word in action for word in ['monitor', 'follow', 'assess', 'evaluate']):
            scenarios.append(CDSUsageScenario.ADVERSE_EVENT)

        # Next best action (catch-all for complex decisions)
        if not scenarios:
            scenarios.append(CDSUsageScenario.NEXT_BEST_ACTION)

        return scenarios

    def create_clinical_scenarios(self, decisions: List[Dict[str, Any]], specialty: str) -> List[ClinicalScenario]:
        """Create clinical scenarios from extracted decisions"""
        scenarios = []

        for i, decision in enumerate(decisions):
            # Map decision to CDS scenarios
            cds_scenarios = self.map_to_cds_scenarios(decision)

            # Create patient context from criteria
            patient_context = {
                'specialty': specialty,
                'conditions': decision['patient_criteria'],
                'context': decision['context']
            }

            # Create clinical observations (simplified)
            clinical_observations = [
                {
                    'observation_type': 'condition',
                    'value': condition,
                    'interpretation': 'present'
                } for condition in decision['patient_criteria']
            ]

            # Create recommended actions
            recommended_actions = [
                {
                    'action_type': 'recommendation',
                    'description': decision['action'],
                    'rationale': decision['context']
                }
            ]

            scenario = ClinicalScenario(
                scenario_id=f"{specialty}_scenario_{i+1}",
                guideline_section="main_guidelines",
                patient_context=patient_context,
                clinical_observations=clinical_observations,
                inferences=[f"Patient presents with {', '.join(decision['patient_criteria'])}"],
                recommended_actions=recommended_actions,
                cds_scenarios=cds_scenarios,
                combinatorial_factors=[]
            )

            scenarios.append(scenario)

        return scenarios

    def analyze_guideline(self, guideline_name: str, guideline_text: str) -> GuidelineAnalysis:
        """Complete guideline analysis pipeline"""
        # Detect specialty
        specialty = self.detect_specialty(guideline_text)

        # Extract decisions
        decisions = self.extract_decision_points(guideline_text)

        # Create clinical scenarios
        scenarios = self.create_clinical_scenarios(decisions, specialty)

        # Generate coverage report
        coverage_report = {}
        for scenario in scenarios:
            for cds_scenario in scenario.cds_scenarios:
                coverage_report[cds_scenario] = coverage_report.get(cds_scenario, 0) + 1

        return GuidelineAnalysis(
            guideline_name=guideline_name,
            specialty=specialty,
            scenarios=scenarios,
            coverage_report=coverage_report
        )

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF (placeholder - would use pypdf or similar)"""
        # For now, return mock content based on filename
        if 'acc-afib' in str(pdf_path).lower():
            return """
            For patients with atrial fibrillation, recommend anticoagulation with DOAC.
            For patients with atrial fibrillation and high bleeding risk, recommend anticoagulation with warfarin.
            Order CHA2DS2-VASc score for stroke risk assessment.
            Monitor patients with atrial fibrillation for bleeding complications.
            """
        elif 'hodgkin' in str(pdf_path).lower():
            return """
            For patients with Hodgkin's lymphoma stage I-II, recommend ABVD chemotherapy.
            For patients with Hodgkin's lymphoma stage III-IV, recommend escalated BEACOPP chemotherapy.
            Order PET-CT scan for staging and response assessment.
            Monitor patients with Hodgkin's lymphoma for treatment response.
            """
        elif 'diabetes' in str(pdf_path).lower() or 'ADA' in pdf_path.name:
            return """
            For patients with type 2 diabetes and HbA1c > 9%, recommend initiating metformin therapy.
            For patients with type 2 diabetes and cardiovascular disease, recommend SGLT2 inhibitors.
            Order HbA1c testing every 3 months for glycemic control assessment.
            For patients with type 2 diabetes and diabetic kidney disease, recommend ACE inhibitors.
            Monitor patients with diabetes for hypoglycemia and hyperglycemia.
            For patients with type 1 diabetes, recommend intensive insulin therapy.
            Order lipid profile for cardiovascular risk assessment in diabetic patients.
            """
        else:
            return f"Mock guideline content for {pdf_path.name}"

    def analyze_guideline_from_file(self, pdf_path: Path) -> GuidelineAnalysis:
        """Analyze guideline from PDF file"""
        guideline_text = self.extract_text_from_pdf(pdf_path)
        return self.analyze_guideline(pdf_path.stem, guideline_text)
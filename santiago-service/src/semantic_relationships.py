#!/usr/bin/env python3
"""
Santiago Layer 1: Core Semantic Relationships

Defines the fundamental semantic relationships for clinical knowledge representation.
These relationships form the basis for structured knowledge extraction and reasoning
in the Santiago NeuroSymbolic knowledge graph.

Based on clinical ontologies and standards including:
- SNOMED CT relationships
- HL7 FHIR relationships
- Clinical practice guidelines
- Medical knowledge bases

Author: GitHub Copilot
Date: November 10, 2025
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RelationshipType(Enum):
    """Core semantic relationship types for clinical knowledge"""

    # Treatment relationships
    TREATS = "treats"                    # Medication/therapy treats condition
    PREVENTS = "prevents"                # Intervention prevents condition
    MITIGATES = "mitigates"              # Intervention mitigates symptom/sign
    MANAGES = "manages"                  # Intervention manages chronic condition

    # Diagnostic relationships
    INVESTIGATES = "investigates"        # Test investigates condition
    DIAGNOSES = "diagnoses"              # Test diagnoses condition
    SCREENS_FOR = "screens_for"          # Test screens for condition
    MONITORS = "monitors"                # Test monitors condition/treatment

    # Pathophysiology relationships
    COMPLICATES = "complicates"          # Condition complicates another condition
    CAUSES = "causes"                    # Condition causes another condition
    PREDISPOSES = "predisposes"          # Condition predisposes to another condition
    CO_OCCURS_WITH = "co_occurs_with"    # Conditions frequently co-occur

    # Risk relationships
    RISK_FACTOR = "risk_factor"          # Factor is risk factor for condition
    PROTECTS_AGAINST = "protects_against" # Factor protects against condition
    INCREASES_RISK = "increases_risk"    # Factor increases risk of condition
    DECREASES_RISK = "decreases_risk"    # Factor decreases risk of condition

    # Anatomical relationships
    AFFECTS = "affects"                  # Condition affects anatomical structure
    LOCATED_IN = "located_in"            # Condition located in anatomical structure
    SPREADS_TO = "spreads_to"            # Condition spreads to anatomical structure

    # Pharmacological relationships
    INTERACTS_WITH = "interacts_with"    # Drug interacts with drug/condition
    CONTRAINDICATED_IN = "contraindicated_in" # Drug contraindicated in condition
    METABOLIZED_BY = "metabolized_by"    # Drug metabolized by enzyme
    INHIBITS = "inhibits"                # Drug inhibits enzyme/pathway

    # Clinical presentation relationships
    PRESENTS_WITH = "presents_with"          # Condition presents with symptom/sign
    INDICATES = "indicates"                  # Sign/symptom indicates condition
    MANIFESTS_AS = "manifests_as"            # Condition manifests as sign/symptom

    # Temporal relationships
    PRECEDES = "precedes"                    # Condition typically precedes another
    FOLLOWS = "follows"                     # Condition typically follows another

    # SNOMED CT core relationships (selected key types)
    FINDING_SITE = "finding_site"            # Anatomical location of clinical finding
    CAUSATIVE_AGENT = "causative_agent"      # Agent causing the condition
    SEVERITY = "severity"                    # Severity level of condition
    METHOD = "method"                        # Method by which procedure is performed
    PROCEDURE_SITE = "procedure_site"        # Anatomical site of procedure
    CHARACTERIZES = "characterizes"          # What an observable entity characterizes

    # FHIR-CPG relationships (Clinical Practice Guidelines)
    CASE_INFORMS_PLAN = "case_informs_plan"                  # Patient case informs clinical plan
    PLAN_INSTANTIATES_CAREPLAN = "plan_instantiates_careplan" # Plan becomes patient-specific care plan
    RECOMMENDATION_GENERATES_PROPOSAL = "recommendation_generates_proposal" # Recommendation becomes proposal
    PROPOSAL_GENERATES_REQUEST = "proposal_generates_request" # Proposal leads to clinical request
    REQUEST_FULFILLED_BY_EVENT = "request_fulfilled_by_event" # Request fulfilled by clinical event
    STRATEGY_CONTAINS_RECOMMENDATION = "strategy_contains_recommendation" # Strategy groups recommendations
    PATHWAY_CONTAINS_STRATEGY = "pathway_contains_strategy" # Pathway coordinates strategies
    ACTIVITY_DEFINED_BY_DEFINITION = "activity_defined_by_definition" # Activity defined by ActivityDefinition
    PATIENT_ENROLLED_IN_PATHWAY = "patient_enrolled_in_pathway" # Patient enrolled in clinical pathway

@dataclass
class RelationshipDefinition:
    """Definition of a semantic relationship with properties and constraints"""

    type: RelationshipType
    name: str
    description: str
    domain: str  # Source entity type (e.g., "medication", "condition")
    range: str   # Target entity type (e.g., "condition", "symptom")
    inverse: Optional[RelationshipType] = None
    symmetric: bool = False
    transitive: bool = False
    properties: Dict[str, Any] = None
    examples: List[Dict[str, str]] = None
    validation_rules: List[str] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.examples is None:
            self.examples = []
        if self.validation_rules is None:
            self.validation_rules = []

class SemanticRelationships:
    """
    Core semantic relationships for Santiago Layer 1

    Defines and manages the fundamental relationship types used for
    clinical knowledge representation and reasoning.
    """

    def __init__(self):
        self.relationships: Dict[RelationshipType, RelationshipDefinition] = {}
        self._initialize_relationships()

    def _initialize_relationships(self):
        """Initialize all core semantic relationships"""

        # TREATS relationship
        self.relationships[RelationshipType.TREATS] = RelationshipDefinition(
            type=RelationshipType.TREATS,
            name="Treats",
            description="A medication, therapy, or intervention treats a medical condition",
            domain="intervention",
            range="condition",
            properties={
                "evidence_levels": ["A", "B", "C", "D", "E"],
                "strength": ["first_line", "second_line", "adjunct", "alternative"],
                "indications": ["approved", "off_label", "investigational"]
            },
            examples=[
                {"source": "metformin", "target": "type_2_diabetes", "evidence": "A"},
                {"source": "aspirin", "target": "myocardial_infarction", "evidence": "A"},
                {"source": "insulin", "target": "diabetic_ketoacidosis", "evidence": "A"}
            ],
            validation_rules=[
                "Source must be a valid intervention (medication, procedure, therapy)",
                "Target must be a valid medical condition",
                "Evidence level must be specified (A-E)"
            ]
        )

        # INVESTIGATES relationship
        self.relationships[RelationshipType.INVESTIGATES] = RelationshipDefinition(
            type=RelationshipType.INVESTIGATES,
            name="Investigates",
            description="A diagnostic test or procedure investigates a medical condition",
            domain="diagnostic_test",
            range="condition",
            properties={
                "sensitivity": "float",  # 0.0-1.0
                "specificity": "float",  # 0.0-1.0
                "test_type": ["laboratory", "imaging", "clinical", "pathology"],
                "purpose": ["diagnosis", "screening", "monitoring", "staging"]
            },
            examples=[
                {"source": "hemoglobin_a1c", "target": "diabetes_mellitus", "sensitivity": 0.85},
                {"source": "echocardiogram", "target": "heart_failure", "specificity": 0.92},
                {"source": "colonoscopy", "target": "colorectal_cancer", "purpose": "screening"}
            ],
            validation_rules=[
                "Source must be a valid diagnostic test or procedure",
                "Target must be a valid medical condition",
                "Sensitivity and specificity should be within 0.0-1.0 range"
            ]
        )

        # COMPLICATES relationship
        self.relationships[RelationshipType.COMPLICATES] = RelationshipDefinition(
            type=RelationshipType.COMPLICATES,
            name="Complicates",
            description="A medical condition complicates or worsens another condition",
            domain="condition",
            range="condition",
            properties={
                "severity": ["mild", "moderate", "severe", "life_threatening"],
                "frequency": ["rare", "uncommon", "common", "very_common"],
                "mechanisms": ["direct", "indirect", "iatrogenic", "progression"]
            },
            examples=[
                {"source": "diabetes_mellitus", "target": "coronary_artery_disease", "severity": "severe"},
                {"source": "chronic_kidney_disease", "target": "hypertension", "frequency": "very_common"},
                {"source": "obesity", "target": "sleep_apnea", "mechanisms": "direct"}
            ],
            validation_rules=[
                "Both source and target must be valid medical conditions",
                "Source and target should be different conditions",
                "Severity level should be specified"
            ]
        )

        # RISK_FACTOR relationship
        self.relationships[RelationshipType.RISK_FACTOR] = RelationshipDefinition(
            type=RelationshipType.RISK_FACTOR,
            name="Risk Factor",
            description="A factor increases the risk of developing a medical condition",
            domain="risk_factor",
            range="condition",
            properties={
                "relative_risk": "float",  # Risk ratio > 1.0
                "odds_ratio": "float",     # Odds ratio > 1.0
                "attributable_fraction": "float",  # 0.0-1.0
                "factor_type": ["modifiable", "non_modifiable", "genetic", "environmental"]
            },
            examples=[
                {"source": "smoking", "target": "lung_cancer", "relative_risk": 10.0, "factor_type": "modifiable"},
                {"source": "family_history", "target": "breast_cancer", "odds_ratio": 2.5, "factor_type": "genetic"},
                {"source": "hypertension", "target": "stroke", "attributable_fraction": 0.35, "factor_type": "modifiable"}
            ],
            validation_rules=[
                "Source must be a valid risk factor",
                "Target must be a valid medical condition",
                "Relative risk should be > 1.0 for risk factors"
            ]
        )

        # PREVENTS relationship
        self.relationships[RelationshipType.PREVENTS] = RelationshipDefinition(
            type=RelationshipType.PREVENTS,
            name="Prevents",
            description="An intervention prevents the occurrence of a medical condition",
            domain="intervention",
            range="condition",
            properties={
                "prevention_type": ["primary", "secondary", "tertiary"],
                "efficacy": "float",  # 0.0-1.0
                "number_needed_to_treat": "int"
            },
            examples=[
                {"source": "vaccination", "target": "influenza", "prevention_type": "primary", "efficacy": 0.7},
                {"source": "statin_therapy", "target": "cardiovascular_events", "prevention_type": "secondary"},
                {"source": "aspirin", "target": "colorectal_cancer", "prevention_type": "primary"}
            ]
        )

        # AFFECTS relationship
        self.relationships[RelationshipType.AFFECTS] = RelationshipDefinition(
            type=RelationshipType.AFFECTS,
            name="Affects",
            description="A condition affects a specific anatomical structure or system",
            domain="condition",
            range="anatomical_structure",
            properties={
                "affected_system": ["cardiovascular", "respiratory", "neurological", "endocrine", "gastrointestinal"],
                "severity": ["mild", "moderate", "severe"],
                "laterality": ["left", "right", "bilateral", "unilateral"]
            },
            examples=[
                {"source": "myocardial_infarction", "target": "heart", "affected_system": "cardiovascular"},
                {"source": "stroke", "target": "brain", "affected_system": "neurological", "laterality": "left"},
                {"source": "pneumonia", "target": "lung", "affected_system": "respiratory"}
            ]
        )

        # INTERACTS_WITH relationship
        self.relationships[RelationshipType.INTERACTS_WITH] = RelationshipDefinition(
            type=RelationshipType.INTERACTS_WITH,
            name="Interacts With",
            description="A medication interacts with another medication or condition",
            domain="medication",
            range="medication|condition",
            symmetric=True,  # Drug A interacts with Drug B implies Drug B interacts with Drug A
            properties={
                "interaction_type": ["pharmacokinetic", "pharmacodynamic", "unknown"],
                "severity": ["minor", "moderate", "major", "contraindicated"],
                "evidence": ["established", "theoretical", "case_report"]
            },
            examples=[
                {"source": "warfarin", "target": "aspirin", "interaction_type": "pharmacodynamic", "severity": "major"},
                {"source": "digoxin", "target": "amiodarone", "interaction_type": "pharmacokinetic"},
                {"source": "lithium", "target": "bipolar_disorder", "interaction_type": "pharmacodynamic"}
            ]
        )

        # CO_OCCURS_WITH relationship
        self.relationships[RelationshipType.CO_OCCURS_WITH] = RelationshipDefinition(
            type=RelationshipType.CO_OCCURS_WITH,
            name="Co-occurs With",
            description="Two conditions frequently occur together",
            domain="condition",
            range="condition",
            symmetric=True,  # Comorbidities are bidirectional
            properties={
                "prevalence": "float",  # 0.0-1.0
                "association_strength": ["weak", "moderate", "strong"],
                "mechanistic_link": ["shared_risk_factors", "causal", "independent"]
            },
            examples=[
                {"source": "hypertension", "target": "diabetes_mellitus", "prevalence": 0.3, "association_strength": "strong"},
                {"source": "depression", "target": "anxiety_disorder", "prevalence": 0.6, "mechanistic_link": "shared_risk_factors"}
            ]
        )

        # PRESENTS_WITH relationship
        self.relationships[RelationshipType.PRESENTS_WITH] = RelationshipDefinition(
            type=RelationshipType.PRESENTS_WITH,
            name="Presents With",
            description="A condition typically presents with a specific symptom or sign",
            domain="condition",
            range="symptom|sign",
            properties={
                "frequency": ["rare", "occasional", "common", "hallmark"],
                "specificity": "float",  # 0.0-1.0
                "sensitivity": "float"   # 0.0-1.0
            },
            examples=[
                {"source": "pneumonia", "target": "fever", "frequency": "common", "specificity": 0.3},
                {"source": "myocardial_infarction", "target": "chest_pain", "frequency": "hallmark", "specificity": 0.7},
                {"source": "diabetic_ketoacidosis", "target": "fruity_breath", "frequency": "hallmark", "specificity": 0.95}
            ]
        )

        # INDICATES relationship
        self.relationships[RelationshipType.INDICATES] = RelationshipDefinition(
            type=RelationshipType.INDICATES,
            name="Indicates",
            description="A sign or symptom indicates the presence of a condition",
            domain="symptom|sign|test_result",
            range="condition",
            properties={
                "diagnostic_value": ["suggestive", "highly_suggestive", "pathognomonic"],
                "positive_predictive_value": "float",  # 0.0-1.0
                "negative_predictive_value": "float"   # 0.0-1.0
            },
            examples=[
                {"source": "elevated_troponin", "target": "myocardial_infarction", "diagnostic_value": "highly_suggestive"},
                {"source": "jaundice", "target": "liver_disease", "diagnostic_value": "suggestive"},
                {"source": "kussmaul_respiration", "target": "diabetic_ketoacidosis", "diagnostic_value": "pathognomonic"}
            ]
        )

        # PRECEDES relationship
        self.relationships[RelationshipType.PRECEDES] = RelationshipDefinition(
            type=RelationshipType.PRECEDES,
            name="Precedes",
            description="One condition typically precedes another in temporal sequence",
            domain="condition",
            range="condition",
            properties={
                "temporal_gap": ["immediate", "days", "weeks", "months", "years"],
                "causal_relationship": ["direct", "indirect", "associative"],
                "frequency": ["rare", "occasional", "common", "almost_always"]
            },
            examples=[
                {"source": "impaired_glucose_tolerance", "target": "type_2_diabetes", "temporal_gap": "years", "causal_relationship": "direct"},
                {"source": "barrett_esophagus", "target": "esophageal_cancer", "temporal_gap": "years", "causal_relationship": "direct"},
                {"source": "chronic_hepatitis", "target": "cirrhosis", "temporal_gap": "years", "causal_relationship": "direct"}
            ]
        )

        # SNOMED CT: FINDING_SITE relationship
        self.relationships[RelationshipType.FINDING_SITE] = RelationshipDefinition(
            type=RelationshipType.FINDING_SITE,
            name="Finding Site",
            description="Anatomical location where a clinical finding is present (SNOMED CT core relationship)",
            domain="condition|finding",
            range="anatomical_structure",
            properties={
                "laterality": ["left", "right", "bilateral", "unilateral"],
                "specificity": ["exact", "approximate", "regional"],
                "primary_site": "bool"
            },
            examples=[
                {"source": "pneumonia", "target": "lung", "laterality": "bilateral", "primary_site": True},
                {"source": "myocardial_infarction", "target": "heart", "laterality": "left", "specificity": "exact"},
                {"source": "skin_rash", "target": "upper_extremity", "laterality": "bilateral", "specificity": "regional"}
            ]
        )

        # SNOMED CT: CAUSATIVE_AGENT relationship
        self.relationships[RelationshipType.CAUSATIVE_AGENT] = RelationshipDefinition(
            type=RelationshipType.CAUSATIVE_AGENT,
            name="Causative Agent",
            description="Agent that causes or contributes to a clinical condition (SNOMED CT core relationship)",
            domain="condition|finding",
            range="organism|substance|event",
            properties={
                "causation_type": ["infectious", "toxic", "genetic", "environmental", "iatrogenic"],
                "evidence_level": ["A", "B", "C", "D", "E"],
                "prevalence": "float"  # 0.0-1.0
            },
            examples=[
                {"source": "pneumonia", "target": "streptococcus_pneumoniae", "causation_type": "infectious", "evidence_level": "A"},
                {"source": "lung_cancer", "target": "cigarette_smoke", "causation_type": "toxic", "evidence_level": "A"},
                {"source": "diabetes_mellitus", "target": "genetic_predisposition", "causation_type": "genetic", "evidence_level": "B"}
            ]
        )

        # SNOMED CT: SEVERITY relationship
        self.relationships[RelationshipType.SEVERITY] = RelationshipDefinition(
            type=RelationshipType.SEVERITY,
            name="Severity",
            description="Severity level of a clinical condition (SNOMED CT core relationship)",
            domain="condition|finding",
            range="severity_concept",
            properties={
                "scale": ["mild", "moderate", "severe", "life_threatening", "fatal"],
                "measurement_type": ["ordinal", "quantitative"],
                "grading_system": "str"  # e.g., "WHO", "CTCAE", "NYHA"
            },
            examples=[
                {"source": "hypertension", "target": "moderate", "scale": "moderate", "grading_system": "JNC_8"},
                {"source": "heart_failure", "target": "class_iii", "scale": "severe", "grading_system": "NYHA"},
                {"source": "diabetic_neuropathy", "target": "severe", "scale": "severe", "measurement_type": "ordinal"}
            ]
        )

        # SNOMED CT: METHOD relationship
        self.relationships[RelationshipType.METHOD] = RelationshipDefinition(
            type=RelationshipType.METHOD,
            name="Method",
            description="Method by which a procedure is performed (SNOMED CT core relationship)",
            domain="procedure|intervention",
            range="action|technique",
            properties={
                "invasiveness": ["non_invasive", "minimally_invasive", "invasive"],
                "approach": ["open", "laparoscopic", "endoscopic", "percutaneous"],
                "complexity": ["simple", "moderate", "complex"]
            },
            examples=[
                {"source": "appendectomy", "target": "excision", "approach": "open", "invasiveness": "invasive"},
                {"source": "colonoscopy", "target": "endoscopic_examination", "approach": "endoscopic", "invasiveness": "minimally_invasive"},
                {"source": "echocardiogram", "target": "ultrasound", "approach": "non_invasive", "invasiveness": "non_invasive"}
            ]
        )

        # SNOMED CT: PROCEDURE_SITE relationship
        self.relationships[RelationshipType.PROCEDURE_SITE] = RelationshipDefinition(
            type=RelationshipType.PROCEDURE_SITE,
            name="Procedure Site",
            description="Anatomical site where a procedure is performed (SNOMED CT core relationship)",
            domain="procedure|intervention",
            range="anatomical_structure",
            properties={
                "laterality": ["left", "right", "bilateral", "unilateral"],
                "access_type": ["direct", "indirect", "remote"],
                "primary_target": "bool"
            },
            examples=[
                {"source": "appendectomy", "target": "appendix", "laterality": "right", "access_type": "direct"},
                {"source": "coronary_angioplasty", "target": "coronary_artery", "laterality": "left", "access_type": "remote"},
                {"source": "knee_arthroscopy", "target": "knee_joint", "laterality": "right", "access_type": "minimally_invasive"}
            ]
        )

        # SNOMED CT: CHARACTERIZES relationship
        self.relationships[RelationshipType.CHARACTERIZES] = RelationshipDefinition(
            type=RelationshipType.CHARACTERIZES,
            name="Characterizes",
            description="What an observable entity or measurement characterizes (SNOMED CT core relationship)",
            domain="observable|measurement",
            range="condition|property|quality",
            properties={
                "measurement_type": ["qualitative", "quantitative", "ordinal"],
                "clinical_significance": ["diagnostic", "prognostic", "monitoring"],
                "reference_range": "str"
            },
            examples=[
                {"source": "hemoglobin_a1c", "target": "glycemic_control", "measurement_type": "quantitative", "clinical_significance": "diagnostic"},
                {"source": "blood_pressure", "target": "cardiovascular_status", "measurement_type": "quantitative", "reference_range": "90-120/60-80"},
                {"source": "pain_scale", "target": "pain_intensity", "measurement_type": "ordinal", "clinical_significance": "monitoring"}
            ]
        )

        # FHIR-CPG: CASE_INFORMS_PLAN relationship
        self.relationships[RelationshipType.CASE_INFORMS_PLAN] = RelationshipDefinition(
            type=RelationshipType.CASE_INFORMS_PLAN,
            name="Case Informs Plan",
            description="Patient case (current state, history, risks) informs the clinical plan (decision-making and care processes) (FHIR-CPG conceptual architecture)",
            domain="case",
            range="plan",
            properties={
                "case_features_used": "list",  # List of case features considered
                "plan_scope": ["comprehensive", "focused", "emergency"],
                "decision_support": ["automated", "semi_automated", "manual"]
            },
            examples=[
                {"source": "diabetes_case", "target": "diabetes_management_plan", "case_features_used": ["hba1c", "complications"], "plan_scope": "comprehensive"},
                {"source": "heart_failure_case", "target": "heart_failure_plan", "case_features_used": ["nyha_class", "ef"], "decision_support": "semi_automated"}
            ]
        )

        # FHIR-CPG: PLAN_INSTANTIATES_CAREPLAN relationship
        self.relationships[RelationshipType.PLAN_INSTANTIATES_CAREPLAN] = RelationshipDefinition(
            type=RelationshipType.PLAN_INSTANTIATES_CAREPLAN,
            name="Plan Instantiates CarePlan",
            description="Definitional clinical plan becomes instantiated as a patient-specific care plan (FHIR-CPG conceptual architecture)",
            domain="plan",
            range="careplan",
            properties={
                "instantiation_type": ["automatic", "prompted", "manual"],
                "patient_specific_goals": "list",
                "timeline": ["immediate", "short_term", "long_term"]
            },
            examples=[
                {"source": "diabetes_management_plan", "target": "john_doe_diabetes_careplan", "instantiation_type": "automatic", "timeline": "long_term"},
                {"source": "hypertension_plan", "target": "jane_smith_bp_careplan", "instantiation_type": "prompted", "patient_specific_goals": ["bp_control"]}
            ]
        )

        # FHIR-CPG: RECOMMENDATION_GENERATES_PROPOSAL relationship
        self.relationships[RelationshipType.RECOMMENDATION_GENERATES_PROPOSAL] = RelationshipDefinition(
            type=RelationshipType.RECOMMENDATION_GENERATES_PROPOSAL,
            name="Recommendation Generates Proposal",
            description="Clinical practice guideline recommendation becomes a patient-specific proposal in a care plan (FHIR-CPG)",
            domain="recommendation",
            range="proposal",
            properties={
                "applicability": ["applicable", "not_applicable", "conditional"],
                "strength": ["strong", "weak", "conditional"],
                "evidence_quality": ["high", "moderate", "low"]
            },
            examples=[
                {"source": "statin_recommendation", "target": "atorvastatin_proposal", "applicability": "applicable", "strength": "strong"},
                {"source": "metformin_recommendation", "target": "metformin_proposal", "applicability": "conditional", "evidence_quality": "high"}
            ]
        )

        # FHIR-CPG: PROPOSAL_GENERATES_REQUEST relationship
        self.relationships[RelationshipType.PROPOSAL_GENERATES_REQUEST] = RelationshipDefinition(
            type=RelationshipType.PROPOSAL_GENERATES_REQUEST,
            name="Proposal Generates Request",
            description="Patient-specific proposal leads to a clinical request (order, prescription, referral) (FHIR-CPG)",
            domain="proposal",
            range="request",
            properties={
                "request_type": ["medication", "procedure", "diagnostic", "referral", "lifestyle"],
                "priority": ["routine", "urgent", "asap", "stat"],
                "authorization_required": "bool"
            },
            examples=[
                {"source": "atorvastatin_proposal", "target": "atorvastatin_prescription", "request_type": "medication", "priority": "routine"},
                {"source": "colonoscopy_proposal", "target": "colonoscopy_order", "request_type": "procedure", "priority": "urgent"}
            ]
        )

        # FHIR-CPG: REQUEST_FULFILLED_BY_EVENT relationship
        self.relationships[RelationshipType.REQUEST_FULFILLED_BY_EVENT] = RelationshipDefinition(
            type=RelationshipType.REQUEST_FULFILLED_BY_EVENT,
            name="Request Fulfilled by Event",
            description="Clinical request is fulfilled by a corresponding clinical event (administration, procedure, observation) (FHIR-CPG)",
            domain="request",
            range="event",
            properties={
                "fulfillment_status": ["completed", "partially_completed", "cancelled", "failed"],
                "timing": ["on_time", "delayed", "early"],
                "outcome": ["successful", "unsuccessful", "complications"]
            },
            examples=[
                {"source": "atorvastatin_prescription", "target": "atorvastatin_administration", "fulfillment_status": "completed", "timing": "on_time"},
                {"source": "colonoscopy_order", "target": "colonoscopy_procedure", "fulfillment_status": "completed", "outcome": "successful"}
            ]
        )

        # FHIR-CPG: STRATEGY_CONTAINS_RECOMMENDATION relationship
        self.relationships[RelationshipType.STRATEGY_CONTAINS_RECOMMENDATION] = RelationshipDefinition(
            type=RelationshipType.STRATEGY_CONTAINS_RECOMMENDATION,
            name="Strategy Contains Recommendation",
            description="Clinical strategy groups and coordinates multiple recommendations for a specific condition or clinical scenario (FHIR-CPG)",
            domain="strategy",
            range="recommendation",
            properties={
                "strategy_role": ["primary", "adjunct", "alternative", "sequential"],
                "condition_focus": "str",
                "coordination_type": ["parallel", "sequential", "conditional"]
            },
            examples=[
                {"source": "diabetes_management_strategy", "target": "metformin_recommendation", "strategy_role": "primary", "coordination_type": "parallel"},
                {"source": "heart_failure_strategy", "target": "ace_inhibitor_recommendation", "strategy_role": "primary", "condition_focus": "heart_failure"}
            ]
        )

        # FHIR-CPG: PATHWAY_CONTAINS_STRATEGY relationship
        self.relationships[RelationshipType.PATHWAY_CONTAINS_STRATEGY] = RelationshipDefinition(
            type=RelationshipType.PATHWAY_CONTAINS_STRATEGY,
            name="Pathway Contains Strategy",
            description="Clinical pathway coordinates multiple strategies across the patient journey (FHIR-CPG)",
            domain="pathway",
            range="strategy",
            properties={
                "pathway_phase": ["acute", "chronic", "preventive", "palliative"],
                "temporal_sequence": ["initial", "followup", "maintenance", "end_of_life"],
                "patient_state": ["stable", "unstable", "critical"]
            },
            examples=[
                {"source": "diabetes_pathway", "target": "glycemic_control_strategy", "pathway_phase": "chronic", "temporal_sequence": "maintenance"},
                {"source": "cancer_pathway", "target": "chemotherapy_strategy", "pathway_phase": "acute", "patient_state": "unstable"}
            ]
        )

        # FHIR-CPG: ACTIVITY_DEFINED_BY_DEFINITION relationship
        self.relationships[RelationshipType.ACTIVITY_DEFINED_BY_DEFINITION] = RelationshipDefinition(
            type=RelationshipType.ACTIVITY_DEFINED_BY_DEFINITION,
            name="Activity Defined by Definition",
            description="Clinical activity is defined by an ActivityDefinition specifying how it should be performed (FHIR-CPG)",
            domain="activity",
            range="activity_definition",
            properties={
                "activity_type": ["medication", "procedure", "communication", "assessment", "enrollment"],
                "definition_scope": ["guideline", "institution", "protocol"],
                "customization_allowed": "bool"
            },
            examples=[
                {"source": "medication_administration", "target": "insulin_administration_definition", "activity_type": "medication", "definition_scope": "guideline"},
                {"source": "patient_assessment", "target": "diabetes_assessment_definition", "activity_type": "assessment", "customization_allowed": True}
            ]
        )

        # FHIR-CPG: PATIENT_ENROLLED_IN_PATHWAY relationship
        self.relationships[RelationshipType.PATIENT_ENROLLED_IN_PATHWAY] = RelationshipDefinition(
            type=RelationshipType.PATIENT_ENROLLED_IN_PATHWAY,
            name="Patient Enrolled in Pathway",
            description="Patient is enrolled in a clinical pathway for management of their condition (FHIR-CPG)",
            domain="patient",
            range="pathway",
            properties={
                "enrollment_type": ["automatic", "prompted", "manual", "patient_initiated"],
                "enrollment_date": "date",
                "exit_criteria": "str"
            },
            examples=[
                {"source": "john_doe", "target": "diabetes_management_pathway", "enrollment_type": "automatic", "enrollment_date": "2024-01-15"},
                {"source": "jane_smith", "target": "heart_failure_pathway", "enrollment_type": "prompted", "exit_criteria": "ef_improved"}
            ]
        )

    def get_relationship(self, rel_type: RelationshipType) -> RelationshipDefinition:
        """Get relationship definition by type"""
        return self.relationships.get(rel_type)

    def get_relationships_by_domain(self, domain: str) -> List[RelationshipDefinition]:
        """Get all relationships with a specific domain"""
        return [rel for rel in self.relationships.values() if rel.domain == domain]

    def get_relationships_by_range(self, range_type: str) -> List[RelationshipDefinition]:
        """Get all relationships with a specific range"""
        return [rel for rel in self.relationships.values() if rel.range == range_type]

    def validate_relationship(self, rel_type: RelationshipType,
                            source_entity: str, target_entity: str,
                            properties: Dict[str, Any] = None) -> List[str]:
        """
        Validate a relationship instance against its definition

        Args:
            rel_type: Type of relationship
            source_entity: Source entity
            target_entity: Target entity
            properties: Relationship properties

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        rel_def = self.get_relationship(rel_type)

        if not rel_def:
            errors.append(f"Unknown relationship type: {rel_type}")
            return errors

        # Check domain/range constraints (simplified - would need entity type checking)
        # In a full implementation, this would validate against ontologies

        # Check required properties
        if properties:
            for prop_name, prop_type in rel_def.properties.items():
                if prop_name in properties:
                    value = properties[prop_name]
                    if prop_type == "float" and not isinstance(value, (int, float)):
                        errors.append(f"Property {prop_name} must be numeric")
                    elif prop_type == "int" and not isinstance(value, int):
                        errors.append(f"Property {prop_name} must be integer")

        return errors

    def get_core_relationships(self) -> List[RelationshipType]:
        """Get the core relationships including SNOMED CT and FHIR-CPG aligned types"""
        return [
            RelationshipType.TREATS,
            RelationshipType.INVESTIGATES,
            RelationshipType.COMPLICATES,
            RelationshipType.RISK_FACTOR,
            RelationshipType.PRESENTS_WITH,
            RelationshipType.INDICATES,
            RelationshipType.PRECEDES,
            # SNOMED CT core relationships
            RelationshipType.FINDING_SITE,
            RelationshipType.CAUSATIVE_AGENT,
            RelationshipType.SEVERITY,
            RelationshipType.METHOD,
            RelationshipType.PROCEDURE_SITE,
            RelationshipType.CHARACTERIZES,
            # FHIR-CPG relationships
            RelationshipType.CASE_INFORMS_PLAN,
            RelationshipType.PLAN_INSTANTIATES_CAREPLAN,
            RelationshipType.RECOMMENDATION_GENERATES_PROPOSAL,
            RelationshipType.PROPOSAL_GENERATES_REQUEST,
            RelationshipType.REQUEST_FULFILLED_BY_EVENT,
            RelationshipType.STRATEGY_CONTAINS_RECOMMENDATION,
            RelationshipType.PATHWAY_CONTAINS_STRATEGY,
            RelationshipType.ACTIVITY_DEFINED_BY_DEFINITION,
            RelationshipType.PATIENT_ENROLLED_IN_PATHWAY
        ]

    def export_to_json(self, filepath: str):
        """Export relationship definitions to JSON file"""
        export_data = {}
        for rel_type, rel_def in self.relationships.items():
            export_data[rel_type.value] = asdict(rel_def)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(self.relationships)} relationships to {filepath}")

    def import_from_json(self, filepath: str):
        """Import relationship definitions from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            import_data = json.load(f)

        # Convert back to RelationshipDefinition objects
        for rel_name, rel_data in import_data.items():
            rel_type = RelationshipType(rel_name)
            # Remove 'type' from data and create enum
            rel_data_copy = rel_data.copy()
            rel_data_copy['type'] = rel_type
            self.relationships[rel_type] = RelationshipDefinition(**rel_data_copy)

        logger.info(f"Imported {len(self.relationships)} relationships from {filepath}")

# Global instance for easy access
semantic_relationships = SemanticRelationships()

if __name__ == "__main__":
    # Example usage and testing
    relationships = SemanticRelationships()

    print("Santiago Layer 1: Core Semantic Relationships")
    print("=" * 50)

    # Show core relationships
    core_rels = relationships.get_core_relationships()
    print(f"Core Relationships ({len(core_rels)}):")
    for rel in core_rels:
        rel_def = relationships.get_relationship(rel)
        print(f"• {rel_def.name}: {rel_def.description}")
        print(f"  Domain: {rel_def.domain} → Range: {rel_def.range}")
        print(f"  Examples: {len(rel_def.examples)}")
        print()

    # Test validation
    print("Validation Examples:")
    print("-" * 30)

    # Valid relationship
    errors = relationships.validate_relationship(
        RelationshipType.TREATS,
        "metformin",
        "diabetes",
        {"evidence": "A"}
    )
    print(f"TREATS validation: {'✓ Valid' if not errors else '✗ Errors: ' + str(errors)}")

    # Invalid relationship (wrong property type)
    errors = relationships.validate_relationship(
        RelationshipType.INVESTIGATES,
        "blood_test",
        "anemia",
        {"sensitivity": "high"}  # Should be float
    )
    print(f"INVESTIGATES validation: {'✓ Valid' if not errors else '✗ Errors: ' + str(errors)}")

    print("\nLayer 1 semantic relationships initialized successfully!")
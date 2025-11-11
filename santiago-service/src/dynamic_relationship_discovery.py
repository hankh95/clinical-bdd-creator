#!/usr/bin/env python3
"""
Dynamic Relationship Discovery Engine

This module implements the Dynamic Relationship Discovery and Evaluation (DRDE)
feature for Santiago Layer 1. It enables the knowledge graph to automatically
evaluate new clinical knowledge and determine if new semantic relationships
need to be appended to the ontology.

Key Components:
- Entity Pair Extraction: Identifies potential relationship candidates from text
- Context Analysis: Analyzes clinical context and relationship significance
- Pattern Matching: Compares new patterns against existing ontology
- Clinical Validation: Ensures clinical validity and consistency
- Proposal Generation: Creates detailed proposals for new relationships

Author: GitHub Copilot
Date: November 10, 2025
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import re
import logging
from datetime import datetime
import json

from semantic_relationships import SemanticRelationships, RelationshipType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscoveryConfidence(Enum):
    """Confidence levels for relationship discovery"""
    LOW = "low"           # <0.3 - Requires manual review
    MEDIUM = "medium"     # 0.3-0.7 - Suggests review
    HIGH = "high"         # 0.7-0.9 - Auto-approve candidate
    VERY_HIGH = "very_high" # >0.9 - High confidence discovery

class ClinicalValidity(Enum):
    """Clinical validity assessment levels"""
    INVALID = "invalid"           # Contradicts established knowledge
    QUESTIONABLE = "questionable" # Uncertain clinical validity
    PROBABLE = "probable"         # Likely clinically valid
    ESTABLISHED = "established"   # Well-established clinical relationship

@dataclass
class RelationshipCandidate:
    """Represents a potential new relationship discovered from clinical text"""
    id: str
    source_entity: str
    target_entity: str
    relationship_type: str
    confidence_score: float
    clinical_validity: ClinicalValidity
    context: str
    evidence_sources: List[str]
    similar_existing_rels: List[Tuple[RelationshipType, float]]
    proposed_properties: Dict[str, Any]
    clinical_examples: List[str]
    discovered_at: datetime
    reviewed: bool = False
    approved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['discovered_at'] = self.discovered_at.isoformat()
        data['clinical_validity'] = self.clinical_validity.value
        data['similar_existing_rels'] = [(rel.value, score) for rel, score in self.similar_existing_rels]
        return data

@dataclass
class RelationshipProposal:
    """Formal proposal for adding a new relationship to the ontology"""
    id: str
    candidate: RelationshipCandidate
    proposed_name: str
    proposed_description: str
    domain: str
    range: str
    properties: Dict[str, Any]
    validation_rules: List[str]
    clinical_examples: List[Dict[str, str]]
    integration_notes: str
    created_at: datetime
    reviewed_by: Optional[str] = None
    approved: bool = False
    approved_at: Optional[datetime] = None

class EntityPairExtractor:
    """
    Extracts potential entity pairs from clinical text that may represent relationships
    """

    def __init__(self):
        # Clinical entity patterns
        self.condition_patterns = [
            r'\b(?:diabetes|hypertension|cancer|heart failure|stroke|pneumonia)\b',
            r'\b(?:infection|inflammation|fracture|depression|anxiety)\b',
            r'\b(?:myocardial infarction|chronic kidney disease|COPD|asthma)\b'
        ]

        self.medication_patterns = [
            r'\b(?:metformin|insulin|aspirin|warfarin|atorvastatin)\b',
            r'\b(?:lisinopril|amlodipine|losartan|hydrochlorothiazide)\b',
            r'\b(?:prednisone|albuterol|omeprazole|sertraline)\b'
        ]

        self.procedure_patterns = [
            r'\b(?:endoscopy|colonoscopy|echocardiogram|MRI|CT scan)\b',
            r'\b(?:biopsy|surgery|angioplasty|stent placement)\b',
            r'\b(?:vaccination|immunization|physical therapy)\b'
        ]

        # Relationship indicator patterns
        self.relationship_indicators = {
            'treatment': [
                r'\b(?:treats?|treated|treatment|therapy|medication for)\b',
                r'\b(?:used to treat|indicated for|prescribed for)\b',
                r'\b(?:effective against|helps with|manages)\b'
            ],
            'diagnosis': [
                r'\b(?:diagnoses?|diagnostic|indicates?|suggests?)\b',
                r'\b(?:screening for|test for|marker for)\b',
                r'\b(?:associated with|linked to|correlated with)\b'
            ],
            'causation': [
                r'\b(?:causes?|caused by|leads to|results in)\b',
                r'\b(?:due to|because of|secondary to)\b',
                r'\b(?:complicates?|worsens?|exacerbates?)\b'
            ],
            'prevention': [
                r'\b(?:prevents?|prevention|reduces risk|lowers chance)\b',
                r'\b(?:protects against|guards against|decreases)\b'
            ]
        }

    def extract_entity_pairs(self, text: str) -> List[Tuple[str, str, str, str]]:
        """
        Extract potential entity pairs from clinical text

        Returns:
            List of tuples: (source_entity, target_entity, relationship_context, evidence_text)
        """
        pairs = []

        # Find all clinical entities
        conditions = self._find_entities(text, self.condition_patterns, "condition")
        medications = self._find_entities(text, self.medication_patterns, "medication")
        procedures = self._find_entities(text, self.procedure_patterns, "procedure")

        all_entities = conditions + medications + procedures

        # Look for relationships between entities
        for i, (entity1, type1, pos1) in enumerate(all_entities):
            for j, (entity2, type2, pos2) in enumerate(all_entities):
                if i >= j:  # Avoid duplicate pairs and self-pairs
                    continue

                # Check if entities are close enough in text (within 200 characters)
                if abs(pos1 - pos2) > 200:
                    continue

                # Extract context between entities
                start_pos = min(pos1, pos2)
                end_pos = max(pos1 + len(entity1), pos2 + len(entity2))
                context = text[max(0, start_pos - 50):min(len(text), end_pos + 50)]

                # Check for relationship indicators
                relationship_type = self._identify_relationship_type(context)

                if relationship_type:
                    # Determine which entity is source vs target based on relationship
                    source, target = self._determine_direction(entity1, entity2, type1, type2, relationship_type, context)
                    pairs.append((source, target, relationship_type, context))

        return pairs

    def _find_entities(self, text: str, patterns: List[str], entity_type: str) -> List[Tuple[str, str, int]]:
        """Find entities matching given patterns"""
        entities = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append((match.group(), entity_type, match.start()))
        return entities

    def _identify_relationship_type(self, context: str) -> Optional[str]:
        """Identify the type of relationship from context"""
        context_lower = context.lower()

        for rel_type, patterns in self.relationship_indicators.items():
            for pattern in patterns:
                if re.search(pattern, context_lower):
                    return rel_type

        return None

    def _determine_direction(self, entity1: str, entity2: str, type1: str, type2: str,
                           rel_type: str, context: str) -> Tuple[str, str]:
        """Determine which entity is the source and which is the target"""
        # Simple heuristic: medications and procedures typically act on conditions
        if rel_type in ['treatment', 'prevention', 'diagnosis']:
            if type1 in ['medication', 'procedure']:
                return entity1, entity2
            elif type2 in ['medication', 'procedure']:
                return entity2, entity1
            else:
                # Both are conditions - use position in text
                return entity1, entity2
        elif rel_type == 'causation':
            # Conditions typically cause other conditions
            return entity1, entity2
        else:
            return entity1, entity2

class ContextAnalyzer:
    """
    Analyzes clinical context to assess relationship significance and validity
    """

    def __init__(self):
        self.clinical_domains = {
            'cardiovascular': ['heart', 'cardiac', 'cardiovascular', 'hypertension', 'myocardial'],
            'endocrine': ['diabetes', 'thyroid', 'endocrine', 'metformin', 'insulin'],
            'respiratory': ['lung', 'respiratory', 'pneumonia', 'asthma', 'COPD'],
            'neurological': ['brain', 'neurological', 'stroke', 'seizure', 'headache'],
            'gastrointestinal': ['liver', 'kidney', 'GI', 'gastrointestinal', 'hepatitis']
        }

        self.evidence_strength_indicators = {
            'strong': ['randomized controlled trial', 'meta-analysis', 'systematic review', 'level A evidence'],
            'moderate': ['cohort study', 'case-control', 'level B evidence', 'prospective study'],
            'weak': ['case report', 'expert opinion', 'level C evidence', 'anecdotal']
        }

    def analyze_context(self, source_entity: str, target_entity: str,
                       relationship_type: str, context: str) -> Dict[str, Any]:
        """
        Analyze clinical context to assess relationship significance

        Returns:
            Dictionary with analysis results including confidence score and clinical validity
        """
        analysis = {
            'domain': self._identify_domain(source_entity, target_entity, context),
            'evidence_strength': self._assess_evidence_strength(context),
            'clinical_relevance': self._assess_clinical_relevance(relationship_type, context),
            'consistency_score': self._check_consistency(relationship_type, source_entity, target_entity),
            'confidence_score': 0.0,
            'clinical_validity': ClinicalValidity.QUESTIONABLE,
            'supporting_factors': [],
            'concerning_factors': []
        }

        # Calculate confidence score based on multiple factors
        confidence_factors = [
            analysis['evidence_strength'] * 0.3,
            analysis['clinical_relevance'] * 0.3,
            analysis['consistency_score'] * 0.4
        ]

        analysis['confidence_score'] = sum(confidence_factors) / len(confidence_factors)

        # Determine clinical validity
        if analysis['confidence_score'] >= 0.8:
            analysis['clinical_validity'] = ClinicalValidity.ESTABLISHED
        elif analysis['confidence_score'] >= 0.6:
            analysis['clinical_validity'] = ClinicalValidity.PROBABLE
        elif analysis['confidence_score'] >= 0.3:
            analysis['clinical_validity'] = ClinicalValidity.QUESTIONABLE
        else:
            analysis['clinical_validity'] = ClinicalValidity.INVALID

        return analysis

    def _identify_domain(self, source: str, target: str, context: str) -> str:
        """Identify the clinical domain of the relationship"""
        text_to_check = f"{source} {target} {context}".lower()

        for domain, keywords in self.clinical_domains.items():
            if any(keyword in text_to_check for keyword in keywords):
                return domain

        return "general"

    def _assess_evidence_strength(self, context: str) -> float:
        """Assess the strength of evidence in the context"""
        context_lower = context.lower()
        score = 0.5  # Base score

        for strength, indicators in self.evidence_strength_indicators.items():
            if any(indicator in context_lower for indicator in indicators):
                if strength == 'strong':
                    score = 0.9
                elif strength == 'moderate':
                    score = 0.7
                elif strength == 'weak':
                    score = 0.3
                break

        return score

    def _assess_clinical_relevance(self, rel_type: str, context: str) -> float:
        """Assess clinical relevance of the relationship"""
        # Check for clinical keywords and context
        clinical_indicators = [
            'patient', 'treatment', 'diagnosis', 'prevention', 'management',
            'clinical', 'medical', 'therapy', 'intervention', 'outcome'
        ]

        context_lower = context.lower()
        indicator_count = sum(1 for indicator in clinical_indicators if indicator in context_lower)

        # Higher relevance if more clinical indicators present
        relevance = min(0.9, 0.3 + (indicator_count * 0.1))
        return relevance

    def _check_consistency(self, rel_type: str, source: str, target: str) -> float:
        """Check consistency with known clinical relationships"""
        # Simple consistency checks based on entity types and relationship types
        consistency_score = 0.5

        # Treatment relationships should involve medications/procedures and conditions
        if rel_type == 'treatment':
            if ('medication' in source.lower() or 'procedure' in source.lower()) and 'condition' in target.lower():
                consistency_score = 0.9
            elif ('condition' in source.lower() and
                  ('medication' in target.lower() or 'procedure' in target.lower())):
                consistency_score = 0.8

        # Causation relationships between conditions are common
        elif rel_type == 'causation':
            if 'condition' in source.lower() and 'condition' in target.lower():
                consistency_score = 0.8

        # Diagnostic relationships should involve tests and conditions
        elif rel_type == 'diagnosis':
            if 'procedure' in source.lower() and 'condition' in target.lower():
                consistency_score = 0.9

        return consistency_score

class DynamicRelationshipDiscovery:
    """
    Main engine for dynamic relationship discovery and evaluation
    """

    def __init__(self):
        self.extractor = EntityPairExtractor()
        self.analyzer = ContextAnalyzer()
        self.semantic_relationships = SemanticRelationships()
        self.discovered_candidates: List[RelationshipCandidate] = []
        self.proposals: List[RelationshipProposal] = []

    def discover_relationships(self, clinical_text: str, source_id: str = "unknown") -> List[RelationshipCandidate]:
        """
        Discover potential new relationships from clinical text

        Args:
            clinical_text: The clinical text to analyze
            source_id: Identifier for the source of the text

        Returns:
            List of relationship candidates discovered
        """
        logger.info(f"Analyzing clinical text from source: {source_id}")

        # Extract entity pairs
        entity_pairs = self.extractor.extract_entity_pairs(clinical_text)
        logger.info(f"Found {len(entity_pairs)} potential entity pairs")

        candidates = []

        for source_entity, target_entity, rel_type, context in entity_pairs:
            # Analyze context
            analysis = self.analyzer.analyze_context(
                source_entity, target_entity, rel_type, context
            )

            # Debug: Show analysis results
            print(f"  Analysis for {source_entity} → {target_entity}: confidence={analysis['confidence_score']:.2f}, validity={analysis['clinical_validity'].value}")

            # Check similarity with existing relationships
            similar_rels = self._find_similar_relationships(source_entity, target_entity, rel_type)

            # Create candidate if confidence is sufficient
            if analysis['confidence_score'] >= 0.3:  # Minimum threshold
                candidate = RelationshipCandidate(
                    id=f"candidate_{len(self.discovered_candidates) + len(candidates) + 1}",
                    source_entity=source_entity,
                    target_entity=target_entity,
                    relationship_type=rel_type,
                    confidence_score=analysis['confidence_score'],
                    clinical_validity=analysis['clinical_validity'],
                    context=context,
                    evidence_sources=[source_id],
                    similar_existing_rels=similar_rels,
                    proposed_properties=self._generate_proposed_properties(rel_type, analysis),
                    clinical_examples=self._generate_examples(source_entity, target_entity, rel_type),
                    discovered_at=datetime.now()
                )
                candidates.append(candidate)

        # Add to discovered candidates
        self.discovered_candidates.extend(candidates)
        logger.info(f"Generated {len(candidates)} relationship candidates")

        return candidates

    def _find_similar_relationships(self, source: str, target: str, rel_type: str) -> List[Tuple[RelationshipType, float]]:
        """Find existing relationships similar to the candidate"""
        similar_rels = []

        # Simple similarity check based on relationship type keywords
        type_mapping = {
            'treatment': ['TREATS', 'PREVENTS', 'MITIGATES', 'MANAGES'],
            'diagnosis': ['INVESTIGATES', 'DIAGNOSES', 'SCREENS_FOR', 'MONITORS'],
            'causation': ['CAUSES', 'COMPLICATES', 'PREDISPOSES'],
            'prevention': ['PREVENTS', 'PROTECTS_AGAINST']
        }

        candidate_types = type_mapping.get(rel_type, [])

        for rel_type_enum in RelationshipType:
            if rel_type_enum.value in candidate_types:
                # Calculate simple similarity score
                similarity = 0.8 if rel_type_enum.value in candidate_types else 0.0
                if similarity > 0.4:  # Only include moderately similar
                    similar_rels.append((rel_type_enum, similarity))

        return similar_rels

    def _generate_proposed_properties(self, rel_type: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate proposed properties for a new relationship"""
        properties = {}

        if rel_type == 'treatment':
            properties = {
                "evidence_levels": ["A", "B", "C", "D", "E"],
                "strength": ["first_line", "second_line", "adjunct"],
                "indications": ["approved", "off_label"]
            }
        elif rel_type == 'diagnosis':
            properties = {
                "sensitivity": "float",
                "specificity": "float",
                "test_type": ["laboratory", "imaging", "clinical"]
            }
        elif rel_type == 'causation':
            properties = {
                "causation_type": ["direct", "indirect", "iatrogenic"],
                "evidence_level": ["A", "B", "C", "D", "E"]
            }

        return properties

    def _generate_examples(self, source: str, target: str, rel_type: str) -> List[str]:
        """Generate clinical examples for the relationship"""
        examples = []

        if rel_type == 'treatment':
            examples = [
                f"{source} is used to treat {target}",
                f"Patients with {target} may benefit from {source}",
                f"{source} shows efficacy in managing {target}"
            ]
        elif rel_type == 'diagnosis':
            examples = [
                f"{source} helps diagnose {target}",
                f"{source} is indicated when {target} is suspected",
                f"Abnormal {source} results may indicate {target}"
            ]
        elif rel_type == 'causation':
            examples = [
                f"{source} can lead to {target}",
                f"{target} may be caused by {source}",
                f"There is an association between {source} and {target}"
            ]

        return examples

    def generate_proposal(self, candidate: RelationshipCandidate) -> RelationshipProposal:
        """
        Generate a formal proposal for a relationship candidate
        """
        # Generate proposal details
        proposed_name = self._generate_relationship_name(candidate)
        proposed_description = self._generate_relationship_description(candidate)

        proposal = RelationshipProposal(
            id=f"proposal_{candidate.id}",
            candidate=candidate,
            proposed_name=proposed_name,
            proposed_description=proposed_description,
            domain=self._infer_domain(candidate.source_entity, candidate.relationship_type),
            range=self._infer_range(candidate.target_entity, candidate.relationship_type),
            properties=candidate.proposed_properties,
            validation_rules=self._generate_validation_rules(candidate),
            clinical_examples=self._generate_detailed_examples(candidate),
            integration_notes=self._generate_integration_notes(candidate),
            created_at=datetime.now()
        )

        self.proposals.append(proposal)
        return proposal

    def _generate_relationship_name(self, candidate: RelationshipCandidate) -> str:
        """Generate a human-readable name for the relationship"""
        rel_type = candidate.relationship_type
        if rel_type == 'treatment':
            return f"Treats {candidate.target_entity}"
        elif rel_type == 'diagnosis':
            return f"Diagnoses {candidate.target_entity}"
        elif rel_type == 'causation':
            return f"Causes {candidate.target_entity}"
        elif rel_type == 'prevention':
            return f"Prevents {candidate.target_entity}"
        else:
            return f"Related to {candidate.target_entity}"

    def _generate_relationship_description(self, candidate: RelationshipCandidate) -> str:
        """Generate a detailed description for the relationship"""
        rel_type = candidate.relationship_type
        source = candidate.source_entity
        target = candidate.target_entity

        if rel_type == 'treatment':
            return f"{source} is used in the treatment or management of {target}"
        elif rel_type == 'diagnosis':
            return f"{source} is used to diagnose or investigate {target}"
        elif rel_type == 'causation':
            return f"{source} can cause or contribute to the development of {target}"
        elif rel_type == 'prevention':
            return f"{source} helps prevent the occurrence of {target}"
        else:
            return f"{source} is related to {target} in a clinically significant way"

    def _infer_domain(self, source_entity: str, rel_type: str) -> str:
        """Infer the domain entity type"""
        # Simple inference based on entity name patterns
        if any(keyword in source_entity.lower() for keyword in ['metformin', 'insulin', 'aspirin']):
            return "medication"
        elif any(keyword in source_entity.lower() for keyword in ['endoscopy', 'biopsy', 'echocardiogram']):
            return "procedure"
        else:
            return "condition"

    def _infer_range(self, target_entity: str, rel_type: str) -> str:
        """Infer the range entity type"""
        # Similar logic for target entity
        if any(keyword in target_entity.lower() for keyword in ['diabetes', 'hypertension', 'cancer']):
            return "condition"
        elif any(keyword in target_entity.lower() for keyword in ['metformin', 'insulin']):
            return "medication"
        else:
            return "condition"

    def _generate_validation_rules(self, candidate: RelationshipCandidate) -> List[str]:
        """Generate validation rules for the proposed relationship"""
        rules = [
            f"Source entity must be a valid {self._infer_domain(candidate.source_entity, candidate.relationship_type)}",
            f"Target entity must be a valid {self._infer_range(candidate.target_entity, candidate.relationship_type)}",
            "Relationship must be supported by clinical evidence",
            "Confidence score must be above threshold for approval"
        ]
        return rules

    def _generate_detailed_examples(self, candidate: RelationshipCandidate) -> List[Dict[str, str]]:
        """Generate detailed clinical examples"""
        examples = []
        for example_text in candidate.clinical_examples:
            examples.append({
                "description": example_text,
                "source": candidate.source_entity,
                "target": candidate.target_entity,
                "context": candidate.context[:100] + "..." if len(candidate.context) > 100 else candidate.context
            })
        return examples

    def _generate_integration_notes(self, candidate: RelationshipCandidate) -> str:
        """Generate notes about integration with existing ontology"""
        notes = "New relationship proposal for integration into Santiago Layer 1 ontology."

        if candidate.similar_existing_rels:
            similar_names = [rel.value for rel, _ in candidate.similar_existing_rels]
            notes += f" Similar to existing relationships: {', '.join(similar_names)}."

        notes += f" Discovered with confidence score: {candidate.confidence_score:.2f}."
        return notes

    def approve_proposal(self, proposal_id: str, reviewer: str) -> bool:
        """
        Approve a relationship proposal for integration

        Returns:
            True if successfully integrated, False otherwise
        """
        proposal = next((p for p in self.proposals if p.id == proposal_id), None)
        if not proposal:
            logger.error(f"Proposal {proposal_id} not found")
            return False

        # Mark as approved
        proposal.approved = True
        proposal.approved_at = datetime.now()
        proposal.reviewed_by = reviewer

        # TODO: Integrate into semantic relationships ontology
        # This would involve updating the SemanticRelationships class
        logger.info(f"Proposal {proposal_id} approved by {reviewer}")

        return True

    def export_candidates(self, filepath: str):
        """Export discovered candidates to JSON file"""
        data = [candidate.to_dict() for candidate in self.discovered_candidates]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Exported {len(data)} candidates to {filepath}")

    def export_proposals(self, filepath: str):
        """Export proposals to JSON file"""
        data = []
        for proposal in self.proposals:
            proposal_dict = asdict(proposal)
            proposal_dict['candidate'] = proposal.candidate.to_dict()
            proposal_dict['created_at'] = proposal.created_at.isoformat()
            if proposal.approved_at:
                proposal_dict['approved_at'] = proposal.approved_at.isoformat()
            data.append(proposal_dict)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Exported {len(data)} proposals to {filepath}")

# Global instance for easy access
drde_engine = DynamicRelationshipDiscovery()

if __name__ == "__main__":
    # Example usage
    engine = DynamicRelationshipDiscovery()

    # Sample clinical text
    sample_text = """
    Metformin is commonly used to treat type 2 diabetes mellitus.
    The medication helps control blood glucose levels and is considered first-line therapy.
    Regular monitoring of hemoglobin A1c is essential for patients on metformin.
    Some patients may experience gastrointestinal side effects.
    """

    print("Dynamic Relationship Discovery Engine")
    print("=" * 50)

    # Discover relationships
    candidates = engine.discover_relationships(sample_text, "sample_clinical_text")

    print(f"\nDiscovered {len(candidates)} relationship candidates:")

    # Debug: Show what entity pairs were found
    entity_pairs = engine.extractor.extract_entity_pairs(sample_text)
    print(f"\nDebug: Found {len(entity_pairs)} entity pairs:")
    for source, target, rel_type, context in entity_pairs:
        print(f"  {source} → {target} ({rel_type}): {context[:100]}...")

    for candidate in candidates:
        print(f"\n• {candidate.source_entity} → {candidate.target_entity}")
        print(f"  Type: {candidate.relationship_type}")
        print(f"  Confidence: {candidate.confidence_score:.2f}")
        print(f"  Validity: {candidate.clinical_validity.value}")
        if candidate.similar_existing_rels:
            print(f"  Similar to: {[rel.value for rel, _ in candidate.similar_existing_rels]}")

    # Generate proposal for first candidate if any
    if candidates:
        proposal = engine.generate_proposal(candidates[0])
        print(f"\nGenerated proposal: {proposal.proposed_name}")
        print(f"Description: {proposal.proposed_description}")
        print(f"Domain: {proposal.domain} → Range: {proposal.range}")

    print("\nDRDE engine initialized successfully!")
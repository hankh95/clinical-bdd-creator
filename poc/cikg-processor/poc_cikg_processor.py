#!/usr/bin/env python3
"""
CIKG Processing POC - L0 to L1 Transformation

This POC demonstrates the transformation of clinical guideline text (L0) 
into structured GSRL triples (L1) following the CIKG 4-layer model.

CIKG Layers:
- L0: Prose (raw clinical guideline text)
- L1: GSRL Triples (Guideline-Situation-Recommendation-Logic)
- L2: RALL Assets (not implemented in POC)
- L3: WATL Workflows (not implemented in POC)

Author: GitHub Copilot
Date: 2025-11-09
"""

import json
import re
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ClinicalEntity:
    """Represents a clinical entity extracted from text"""
    text: str
    entity_type: str  # condition, measurement, medication, action
    value: Optional[str] = None
    unit: Optional[str] = None


@dataclass
class GSRLTriple:
    """
    GSRL Triple: Guideline-Situation-Recommendation-Logic
    
    Represents a structured clinical decision rule
    """
    guideline: str
    situation: str
    recommendation: str
    logic: str
    confidence: float = 1.0


@dataclass
class CIKGOutput:
    """Complete CIKG processing output"""
    layer0: Dict[str, any]
    layer1: Dict[str, List[Dict]]


class CIKGProcessor:
    """
    Process clinical guideline text through CIKG layers
    
    Demonstrates L0 → L1 transformation:
    - Extract clinical entities from text
    - Identify conditions, measurements, actions
    - Generate GSRL triples
    """
    
    # Simple patterns for clinical entity recognition
    CONDITION_PATTERNS = [
        r'(type \d+ diabetes|diabetes mellitus|hypertension|heart failure|sepsis|stroke)',
        r'(elevated \w+|high \w+|low \w+)'
    ]
    
    MEASUREMENT_PATTERNS = [
        r'(HbA1c|blood pressure|BP|systolic|diastolic|glucose|cholesterol|creatinine)',
        r'(\w+)\s*([><=]+)\s*(\d+\.?\d*)\s*(%|mmHg|mg/dL|mmol/L)?'
    ]
    
    MEDICATION_PATTERNS = [
        r'(metformin|insulin|ACE inhibitor|beta blocker|statin|aspirin|antibiotic)',
        r'(therapy|treatment|medication)'
    ]
    
    ACTION_PATTERNS = [
        r'(initiate|start|begin|prescribe|administer|order|discontinue|stop)',
        r'(should be|must be|shall be)'
    ]
    
    def __init__(self):
        self.entities_extracted = 0
        self.triples_generated = 0
    
    def process_text(self, clinical_text: str) -> CIKGOutput:
        """
        Process clinical guideline text through CIKG layers
        
        Args:
            clinical_text: Raw clinical guideline text (L0)
            
        Returns:
            CIKGOutput with L0 and L1 representations
        """
        # Layer 0: Store original text
        layer0 = self._create_layer0(clinical_text)
        
        # Layer 1: Extract entities and generate GSRL triples
        entities = self._extract_entities(clinical_text)
        triples = self._generate_gsrl_triples(clinical_text, entities)
        
        layer1 = {
            "entities": [asdict(e) for e in entities],
            "triples": [asdict(t) for t in triples]
        }
        
        return CIKGOutput(layer0=layer0, layer1=layer1)
    
    def _create_layer0(self, text: str) -> Dict:
        """Create Layer 0 representation (prose)"""
        return {
            "text": text,
            "length": len(text),
            "sentences": len(text.split('.')),
            "source": "clinical_guideline"
        }
    
    def _extract_entities(self, text: str) -> List[ClinicalEntity]:
        """Extract clinical entities from text"""
        entities = []
        
        # Extract conditions
        for pattern in self.CONDITION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = ClinicalEntity(
                    text=match.group(1),
                    entity_type="condition"
                )
                entities.append(entity)
                self.entities_extracted += 1
        
        # Extract measurements with values
        measurement_pattern = r'(\w+)\s*([><=]+)\s*(\d+\.?\d*)\s*(%|mmHg|mg/dL|mmol/L)?'
        matches = re.finditer(measurement_pattern, text, re.IGNORECASE)
        for match in matches:
            entity = ClinicalEntity(
                text=match.group(1),
                entity_type="measurement",
                value=match.group(3),
                unit=match.group(4) if match.lastindex >= 4 else None
            )
            entities.append(entity)
            self.entities_extracted += 1
        
        # Extract medications
        for pattern in self.MEDICATION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = ClinicalEntity(
                    text=match.group(1) if match.lastindex >= 1 else match.group(0),
                    entity_type="medication"
                )
                entities.append(entity)
                self.entities_extracted += 1
        
        # Extract actions
        for pattern in self.ACTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = ClinicalEntity(
                    text=match.group(1) if match.lastindex >= 1 else match.group(0),
                    entity_type="action"
                )
                entities.append(entity)
                self.entities_extracted += 1
        
        return entities
    
    def _generate_gsrl_triples(self, text: str, entities: List[ClinicalEntity]) -> List[GSRLTriple]:
        """
        Generate GSRL triples from text and entities
        
        GSRL = Guideline-Situation-Recommendation-Logic
        """
        triples = []
        
        # Simple heuristic: Look for sentence patterns
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        for sentence in sentences:
            # Look for conditional patterns (if/when -> then/should)
            if self._is_decision_sentence(sentence):
                triple = self._extract_gsrl_from_sentence(sentence, entities)
                if triple:
                    triples.append(triple)
                    self.triples_generated += 1
        
        return triples
    
    def _is_decision_sentence(self, sentence: str) -> bool:
        """Check if sentence contains a clinical decision rule"""
        decision_keywords = [
            'if', 'when', 'for patients', 'should', 'must', 'shall',
            'recommend', 'indicated', 'appropriate', 'contraindicated'
        ]
        return any(keyword in sentence.lower() for keyword in decision_keywords)
    
    def _extract_gsrl_from_sentence(self, sentence: str, entities: List[ClinicalEntity]) -> Optional[GSRLTriple]:
        """Extract GSRL triple from a single sentence"""
        # Extract guideline context
        guideline = self._extract_guideline_context(sentence)
        
        # Extract situation (condition)
        situation = self._extract_situation(sentence, entities)
        
        # Extract recommendation (action)
        recommendation = self._extract_recommendation(sentence, entities)
        
        # Extract logic (reasoning)
        logic = self._extract_logic(sentence)
        
        if situation and recommendation:
            return GSRLTriple(
                guideline=guideline,
                situation=situation,
                recommendation=recommendation,
                logic=logic,
                confidence=0.8  # Simple heuristic confidence
            )
        
        return None
    
    def _extract_guideline_context(self, sentence: str) -> str:
        """Extract guideline/domain context"""
        # Look for disease/condition mentions
        for entity_type in ['diabetes', 'hypertension', 'sepsis', 'stroke', 'heart failure']:
            if entity_type in sentence.lower():
                return f"{entity_type}_management"
        
        return "clinical_guideline"
    
    def _extract_situation(self, sentence: str, entities: List[ClinicalEntity]) -> str:
        """Extract the clinical situation/condition"""
        conditions = []
        measurements = []
        
        # Find relevant entities in this sentence
        for entity in entities:
            if entity.text.lower() in sentence.lower():
                if entity.entity_type == "condition":
                    conditions.append(entity.text)
                elif entity.entity_type == "measurement" and entity.value:
                    comp = self._extract_comparison(sentence, entity.text)
                    measurements.append(f"{entity.text} {comp} {entity.value}")
        
        # Combine into situation string
        parts = conditions + measurements
        return " AND ".join(parts) if parts else "patient_condition"
    
    def _extract_recommendation(self, sentence: str, entities: List[ClinicalEntity]) -> str:
        """Extract the recommended action"""
        actions = []
        medications = []
        
        for entity in entities:
            if entity.text.lower() in sentence.lower():
                if entity.entity_type == "action":
                    actions.append(entity.text)
                elif entity.entity_type == "medication":
                    medications.append(entity.text)
        
        # Combine action + medication
        if actions and medications:
            return f"{actions[0]}_{medications[0]}_therapy"
        elif actions:
            return f"{actions[0]}_intervention"
        elif medications:
            return f"prescribe_{medications[0]}"
        
        return "clinical_action"
    
    def _extract_logic(self, sentence: str) -> str:
        """Extract the clinical reasoning/logic"""
        if 'unless contraindicated' in sentence.lower():
            return "first_line_unless_contraindicated"
        elif 'if indicated' in sentence.lower():
            return "when_clinically_indicated"
        elif 'should be initiated' in sentence.lower() or 'should be' in sentence.lower():
            return "standard_of_care"
        else:
            return "clinical_judgment_required"
    
    def _extract_comparison(self, sentence: str, measurement: str) -> str:
        """Extract comparison operator near measurement"""
        # Look for >= <= > < near the measurement
        pattern = f"{measurement}\\s*([><=]+)"
        match = re.search(pattern, sentence, re.IGNORECASE)
        if match:
            return match.group(1)
        return ">"
    
    def process_from_file(self, input_path: Path, output_path: Optional[Path] = None) -> CIKGOutput:
        """
        Process clinical text from file
        
        Args:
            input_path: Path to input text file (JSON with clinical text)
            output_path: Optional path to save output JSON
            
        Returns:
            CIKGOutput with L0 and L1 representations
        """
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Handle array or single text
        if isinstance(data, list):
            clinical_text = data[0]['text'] if 'text' in data[0] else data[0]
        elif isinstance(data, dict):
            clinical_text = data.get('text', str(data))
        else:
            clinical_text = str(data)
        
        result = self.process_text(clinical_text)
        
        if output_path:
            output_dict = asdict(result)
            with open(output_path, 'w') as f:
                json.dump(output_dict, f, indent=2)
            print(f"✓ CIKG output saved to: {output_path}")
        
        return result


def main():
    """Command-line interface for CIKG Processor POC"""
    if len(sys.argv) < 2:
        print("Usage: python poc_cikg_processor.py <input.json> [output.json]")
        print("\nExample:")
        print("  python poc_cikg_processor.py clinical_texts.json cikg_output.json")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    processor = CIKGProcessor()
    
    try:
        result = processor.process_from_file(input_file, output_file)
        
        if not output_file:
            print("\n" + "=" * 80)
            print("CIKG PROCESSING OUTPUT:")
            print("=" * 80)
            print(json.dumps(asdict(result), indent=2))
            print("=" * 80)
        
        print(f"\n✓ Extracted {processor.entities_extracted} entities")
        print(f"✓ Generated {processor.triples_generated} GSRL triples")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

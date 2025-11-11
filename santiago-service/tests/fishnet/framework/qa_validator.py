"""
QA Validator for Fishnet Testing Framework

Validates clinical question answering accuracy and evidence traceability.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class QAValidationResult:
    """Result of clinical QA validation"""
    scenario_id: str
    question: str
    
    # Answer validation
    answer: str = ""
    answer_accuracy: float = 0.0
    answer_complete: bool = True
    missing_elements: List[str] = field(default_factory=list)
    
    # Evidence validation
    evidence_sources: List[Dict[str, str]] = field(default_factory=list)
    evidence_complete: bool = True
    missing_evidence: List[str] = field(default_factory=list)
    
    # Reasoning validation
    reasoning_path: List[str] = field(default_factory=list)
    reasoning_path_valid: bool = True
    reasoning_errors: List[str] = field(default_factory=list)
    
    # Confidence calibration
    confidence: float = 0.0
    confidence_calibrated: bool = True
    confidence_error: float = 0.0
    
    # Performance
    response_time_ms: float = 0.0


class QAValidator:
    """Validates clinical question answering"""
    
    def __init__(self, santiago_service=None):
        """
        Initialize QA validator
        
        Args:
            santiago_service: Optional Santiago service instance
        """
        self.santiago_service = santiago_service
    
    def validate_question(self, question: str, scenario, expected_answer: Optional[Dict[str, Any]] = None) -> QAValidationResult:
        """
        Validate a clinical question answer
        
        Args:
            question: Clinical question to ask
            scenario: ClinicalScenario object or scenario ID
            expected_answer: Optional expected answer for validation
        
        Returns:
            QAValidationResult with validation metrics
        """
        import time
        start_time = time.time()
        
        scenario_id = scenario if isinstance(scenario, str) else scenario.scenario_id
        
        result = QAValidationResult(
            scenario_id=scenario_id,
            question=question,
        )
        
        # Get answer from Santiago service
        if self.santiago_service:
            # Would query actual service here
            pass
        else:
            # Placeholder answer
            result.answer = "Placeholder answer for: " + question
            result.answer_accuracy = 0.90
            result.confidence = 0.85
        
        # Validate against expected answer if provided
        if expected_answer:
            result = self._validate_against_expected(result, expected_answer)
        
        result.response_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def validate_qa_assertions(self, scenario) -> List[QAValidationResult]:
        """
        Validate all QA assertions for a scenario
        
        Args:
            scenario: ClinicalScenario object
        
        Returns:
            List of QAValidationResult for each QA assertion
        """
        results = []
        
        if not scenario.santiago_assertions or 'qa_assertions' not in scenario.santiago_assertions:
            return results
        
        for assertion in scenario.santiago_assertions['qa_assertions']:
            question = assertion.get('question', '')
            
            # Build expected answer from assertion
            expected_answer = {
                'answer_contains': assertion.get('expected_answer_contains', []),
                'evidence': assertion.get('expected_evidence', []),
                'confidence_threshold': assertion.get('confidence_threshold', 0.0),
            }
            
            result = self.validate_question(question, scenario, expected_answer)
            results.append(result)
        
        return results
    
    def _validate_against_expected(self, result: QAValidationResult, expected: Dict[str, Any]) -> QAValidationResult:
        """Validate result against expected answer"""
        
        # Check for expected content in answer
        answer_contains = expected.get('answer_contains', [])
        for content in answer_contains:
            if content.lower() not in result.answer.lower():
                result.answer_complete = False
                result.missing_elements.append(content)
        
        # Calculate answer accuracy
        if answer_contains:
            matched = len(answer_contains) - len(result.missing_elements)
            result.answer_accuracy = matched / len(answer_contains) if answer_contains else 1.0
        
        # Validate evidence
        expected_evidence = expected.get('evidence', [])
        if expected_evidence:
            # Check if expected evidence sources are present
            for exp_ev in expected_evidence:
                guideline = exp_ev.get('guideline', '')
                found = any(guideline in str(ev) for ev in result.evidence_sources)
                if not found:
                    result.evidence_complete = False
                    result.missing_evidence.append(guideline)
        
        # Validate confidence threshold
        confidence_threshold = expected.get('confidence_threshold', 0.0)
        if result.confidence < confidence_threshold:
            result.confidence_calibrated = False
            result.confidence_error = confidence_threshold - result.confidence
        
        return result

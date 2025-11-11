"""
Reasoning Tester for Fishnet Testing Framework

Tests neurosymbolic reasoning capabilities including symbolic, neural, and hybrid reasoning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class ReasoningType(Enum):
    """Types of reasoning to test"""
    SYMBOLIC = "symbolic"
    NEURAL = "neural"
    HYBRID = "hybrid"


@dataclass
class ReasoningTestResult:
    """Result of a reasoning test"""
    scenario_id: str
    reasoning_type: ReasoningType
    
    # Accuracy metrics
    accuracy: float
    confidence: float
    
    # Reasoning components
    symbolic_weight: float = 0.0
    neural_weight: float = 0.0
    
    # Outputs
    recommendations: List[str] = field(default_factory=list)
    reasoning_path: List[str] = field(default_factory=list)
    matched_concepts: List[str] = field(default_factory=list)
    
    # Validation
    reasoning_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    # Metrics
    similarity_score: float = 0.0
    execution_time_ms: float = 0.0


class ReasoningTester:
    """Tests neurosymbolic reasoning capabilities"""
    
    def __init__(self, santiago_service=None):
        """
        Initialize reasoning tester
        
        Args:
            santiago_service: Optional Santiago service instance for reasoning tests
        """
        self.santiago_service = santiago_service
    
    def test_symbolic_reasoning(self, scenario, reasoning_type: str = "diagnosis_to_treatment") -> ReasoningTestResult:
        """
        Test symbolic reasoning capabilities
        
        Args:
            scenario: ClinicalScenario object or scenario ID
            reasoning_type: Type of reasoning to test
        
        Returns:
            ReasoningTestResult with symbolic reasoning metrics
        """
        import time
        start_time = time.time()
        
        scenario_id = scenario if isinstance(scenario, str) else scenario.scenario_id
        
        result = ReasoningTestResult(
            scenario_id=scenario_id,
            reasoning_type=ReasoningType.SYMBOLIC,
            accuracy=0.95,  # Placeholder
            confidence=0.95,
            symbolic_weight=1.0,
            neural_weight=0.0,
        )
        
        # Load scenario if needed
        if isinstance(scenario, str):
            from .scenario_loader import ScenarioLoader
            loader = ScenarioLoader()
            scenario = loader.load_scenario(scenario)
        
        # Execute symbolic reasoning
        if self.santiago_service:
            # Would execute actual symbolic reasoning here
            pass
        else:
            # Placeholder results
            if hasattr(scenario, 'expectations'):
                recommendations = scenario.expectations.get('recommendations', [])
                result.recommendations = [r.get('drug_class', '') for r in recommendations if isinstance(r, dict)]
            result.reasoning_path = ["diagnosis_check", "contraindication_check", "guideline_lookup"]
        
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def test_neural_reasoning(self, scenario, query: str) -> ReasoningTestResult:
        """
        Test neural reasoning capabilities
        
        Args:
            scenario: ClinicalScenario object or scenario ID
            query: Natural language query for neural matching
        
        Returns:
            ReasoningTestResult with neural reasoning metrics
        """
        import time
        start_time = time.time()
        
        scenario_id = scenario if isinstance(scenario, str) else scenario.scenario_id
        
        result = ReasoningTestResult(
            scenario_id=scenario_id,
            reasoning_type=ReasoningType.NEURAL,
            accuracy=0.85,  # Placeholder
            confidence=0.85,
            symbolic_weight=0.0,
            neural_weight=1.0,
            similarity_score=0.88,
        )
        
        # Load scenario if needed
        if isinstance(scenario, str):
            from .scenario_loader import ScenarioLoader
            loader = ScenarioLoader()
            scenario = loader.load_scenario(scenario)
        
        # Execute neural reasoning
        if self.santiago_service:
            # Would execute actual neural reasoning here
            pass
        else:
            # Placeholder results
            result.matched_concepts = ["ARNI", "beta-blocker", "MRA", "SGLT2i"]
        
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def test_hybrid_reasoning(self, scenario) -> ReasoningTestResult:
        """
        Test hybrid neurosymbolic reasoning
        
        Args:
            scenario: ClinicalScenario object or scenario ID
        
        Returns:
            ReasoningTestResult with hybrid reasoning metrics
        """
        import time
        start_time = time.time()
        
        scenario_id = scenario if isinstance(scenario, str) else scenario.scenario_id
        
        result = ReasoningTestResult(
            scenario_id=scenario_id,
            reasoning_type=ReasoningType.HYBRID,
            accuracy=0.92,  # Placeholder
            confidence=0.90,
            symbolic_weight=0.7,  # Symbolic should dominate for guideline-based
            neural_weight=0.3,
        )
        
        # Load scenario if needed
        if isinstance(scenario, str):
            from .scenario_loader import ScenarioLoader
            loader = ScenarioLoader()
            scenario = loader.load_scenario(scenario)
        
        # Execute hybrid reasoning
        if self.santiago_service:
            # Would execute actual hybrid reasoning here
            pass
        else:
            # Placeholder results combining symbolic and neural
            if hasattr(scenario, 'expectations'):
                recommendations = scenario.expectations.get('recommendations', [])
                result.recommendations = [r.get('drug_class', '') for r in recommendations if isinstance(r, dict)]
            result.reasoning_path = ["neural_similarity", "symbolic_validation", "guideline_match"]
            result.matched_concepts = ["ARNI", "beta-blocker", "MRA", "SGLT2i"]
        
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def validate_reasoning_assertions(self, scenario) -> List[ReasoningTestResult]:
        """
        Validate all reasoning assertions for a scenario
        
        Args:
            scenario: ClinicalScenario object
        
        Returns:
            List of ReasoningTestResult for each assertion
        """
        results = []
        
        if not scenario.santiago_assertions or 'reasoning_assertions' not in scenario.santiago_assertions:
            return results
        
        for assertion in scenario.santiago_assertions['reasoning_assertions']:
            reasoning_type_str = assertion.get('reasoning_type', 'symbolic')
            
            try:
                reasoning_type = ReasoningType(reasoning_type_str)
            except ValueError:
                # Unknown reasoning type
                continue
            
            # Execute appropriate test
            if reasoning_type == ReasoningType.SYMBOLIC:
                result = self._test_symbolic_assertion(scenario, assertion)
            elif reasoning_type == ReasoningType.NEURAL:
                result = self._test_neural_assertion(scenario, assertion)
            elif reasoning_type == ReasoningType.HYBRID:
                result = self._test_hybrid_assertion(scenario, assertion)
            else:
                continue
            
            results.append(result)
        
        return results
    
    def _test_symbolic_assertion(self, scenario, assertion: Dict[str, Any]) -> ReasoningTestResult:
        """Test a symbolic reasoning assertion"""
        result = self.test_symbolic_reasoning(scenario)
        
        # Validate expected output
        expected_output = assertion.get('expected_output', {})
        if 'recommendation' in expected_output:
            expected_rec = expected_output['recommendation']
            if expected_rec not in ' '.join(result.recommendations).lower():
                result.reasoning_valid = False
                result.validation_errors.append(f"Expected recommendation '{expected_rec}' not found")
        
        if 'confidence' in expected_output:
            expected_conf_str = expected_output['confidence']
            if expected_conf_str.startswith('>='):
                min_conf = float(expected_conf_str[2:])
                if result.confidence < min_conf:
                    result.reasoning_valid = False
                    result.validation_errors.append(f"Confidence {result.confidence} below threshold {min_conf}")
        
        return result
    
    def _test_neural_assertion(self, scenario, assertion: Dict[str, Any]) -> ReasoningTestResult:
        """Test a neural reasoning assertion"""
        query = assertion.get('query', '')
        result = self.test_neural_reasoning(scenario, query)
        
        # Validate expected concepts
        expected_concepts = assertion.get('expected_concepts', [])
        for concept in expected_concepts:
            if concept not in result.matched_concepts:
                result.reasoning_valid = False
                result.validation_errors.append(f"Expected concept '{concept}' not matched")
        
        # Validate similarity threshold
        threshold = assertion.get('similarity_threshold', 0.0)
        if result.similarity_score < threshold:
            result.reasoning_valid = False
            result.validation_errors.append(f"Similarity {result.similarity_score} below threshold {threshold}")
        
        return result
    
    def _test_hybrid_assertion(self, scenario, assertion: Dict[str, Any]) -> ReasoningTestResult:
        """Test a hybrid reasoning assertion"""
        result = self.test_hybrid_reasoning(scenario)
        
        # Validate hybrid-specific properties
        # (Similar to symbolic and neural combined)
        
        return result

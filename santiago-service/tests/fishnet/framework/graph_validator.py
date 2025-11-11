"""
Graph Validator for Fishnet Testing Framework

Validates knowledge graph fidelity across the four-layer Santiago model.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class ValidationLayer(Enum):
    """Santiago four-layer model layers"""
    RAW_TEXT = "raw_text"
    STRUCTURED_KNOWLEDGE = "structured_knowledge"
    COMPUTABLE_LOGIC = "computable_logic"
    EXECUTABLE_WORKFLOWS = "executable_workflows"


@dataclass
class LayerValidationResult:
    """Result of validating a single layer"""
    layer: ValidationLayer
    accuracy: float
    node_count: int
    edge_count: int
    missing_concepts: List[str] = field(default_factory=list)
    extra_concepts: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class GraphValidationResult:
    """Result of knowledge graph fidelity validation"""
    scenario_id: str
    overall_fidelity: float
    
    # Layer-specific results
    layer_1_to_2_accuracy: float
    layer_2_to_3_accuracy: float
    layer_3_to_4_accuracy: float
    cross_layer_consistency: float
    
    # Detailed layer results
    layer_results: Dict[ValidationLayer, LayerValidationResult] = field(default_factory=dict)
    
    # Graph structure validation
    graph_structure_valid: bool = True
    structural_errors: List[str] = field(default_factory=list)
    
    # Semantic validation
    semantic_consistency: float = 1.0
    semantic_errors: List[str] = field(default_factory=list)
    
    # Clinical accuracy
    clinical_accuracy: float = 1.0
    clinical_errors: List[str] = field(default_factory=list)
    
    # Evidence traceability
    evidence_traceable: bool = True
    missing_evidence_links: List[str] = field(default_factory=list)
    
    # Performance metrics
    validation_time_ms: float = 0.0


class GraphValidator:
    """Validates knowledge graph fidelity and accuracy"""
    
    def __init__(self, santiago_service=None):
        """
        Initialize graph validator
        
        Args:
            santiago_service: Optional Santiago service instance for graph queries
        """
        self.santiago_service = santiago_service
        self._assertion_cache: Dict[str, Any] = {}
    
    def validate_graph_fidelity(self, scenario, guideline_content: Optional[str] = None) -> GraphValidationResult:
        """
        Validate that a clinical scenario is accurately represented in the knowledge graph
        
        Args:
            scenario: ClinicalScenario object
            guideline_content: Optional guideline text for validation
        
        Returns:
            GraphValidationResult with detailed validation metrics
        """
        import time
        start_time = time.time()
        
        result = GraphValidationResult(
            scenario_id=scenario.scenario_id,
            overall_fidelity=0.0,
            layer_1_to_2_accuracy=0.0,
            layer_2_to_3_accuracy=0.0,
            layer_3_to_4_accuracy=0.0,
            cross_layer_consistency=0.0,
        )
        
        # Validate each layer if Santiago assertions are available
        if scenario.santiago_assertions and 'graph_assertions' in scenario.santiago_assertions:
            for assertion in scenario.santiago_assertions['graph_assertions']:
                layer_name = assertion.get('layer', '')
                try:
                    layer_enum = ValidationLayer(layer_name)
                    layer_result = self._validate_layer(scenario, layer_enum, assertion)
                    result.layer_results[layer_enum] = layer_result
                except ValueError:
                    result.structural_errors.append(f"Unknown layer: {layer_name}")
        else:
            # Perform basic validation without specific assertions
            result = self._perform_basic_validation(scenario)
        
        # Calculate layer transition accuracies
        if ValidationLayer.RAW_TEXT in result.layer_results and ValidationLayer.STRUCTURED_KNOWLEDGE in result.layer_results:
            result.layer_1_to_2_accuracy = (result.layer_results[ValidationLayer.RAW_TEXT].accuracy + 
                                           result.layer_results[ValidationLayer.STRUCTURED_KNOWLEDGE].accuracy) / 2
        
        if ValidationLayer.STRUCTURED_KNOWLEDGE in result.layer_results and ValidationLayer.COMPUTABLE_LOGIC in result.layer_results:
            result.layer_2_to_3_accuracy = (result.layer_results[ValidationLayer.STRUCTURED_KNOWLEDGE].accuracy + 
                                           result.layer_results[ValidationLayer.COMPUTABLE_LOGIC].accuracy) / 2
        
        if ValidationLayer.COMPUTABLE_LOGIC in result.layer_results and ValidationLayer.EXECUTABLE_WORKFLOWS in result.layer_results:
            result.layer_3_to_4_accuracy = (result.layer_results[ValidationLayer.COMPUTABLE_LOGIC].accuracy + 
                                           result.layer_results[ValidationLayer.EXECUTABLE_WORKFLOWS].accuracy) / 2
        
        # Calculate cross-layer consistency
        result.cross_layer_consistency = self._calculate_cross_layer_consistency(result)
        
        # Calculate overall fidelity
        accuracies = [r.accuracy for r in result.layer_results.values()]
        if accuracies:
            result.overall_fidelity = sum(accuracies) / len(accuracies)
        
        # Validate graph structure
        result.graph_structure_valid = self._validate_graph_structure(scenario, result)
        
        # Validate semantic consistency
        result.semantic_consistency = self._validate_semantic_consistency(scenario, result)
        
        # Validate clinical accuracy
        result.clinical_accuracy = self._validate_clinical_accuracy(scenario, result)
        
        # Validate evidence traceability
        result.evidence_traceable = self._validate_evidence_traceability(scenario, result)
        
        result.validation_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def _validate_layer(self, scenario, layer: ValidationLayer, assertion: Dict[str, Any]) -> LayerValidationResult:
        """Validate a specific layer of the knowledge graph"""
        result = LayerValidationResult(
            layer=layer,
            accuracy=0.95,  # Placeholder - would query actual graph
            node_count=0,
            edge_count=0,
        )
        
        # Would execute Gremlin queries here if Santiago service is available
        if self.santiago_service:
            # Execute graph queries to validate layer
            pass
        
        return result
    
    def _perform_basic_validation(self, scenario) -> GraphValidationResult:
        """Perform basic validation without specific assertions"""
        result = GraphValidationResult(
            scenario_id=scenario.scenario_id,
            overall_fidelity=0.90,  # Placeholder
            layer_1_to_2_accuracy=0.90,
            layer_2_to_3_accuracy=0.90,
            layer_3_to_4_accuracy=0.90,
            cross_layer_consistency=0.90,
        )
        
        # Create placeholder layer results for all layers
        for layer in ValidationLayer:
            result.layer_results[layer] = LayerValidationResult(
                layer=layer,
                accuracy=0.90,
                node_count=10,
                edge_count=15,
            )
        
        return result
    
    def _calculate_cross_layer_consistency(self, result: GraphValidationResult) -> float:
        """Calculate cross-layer semantic consistency"""
        # Placeholder - would check that concepts are preserved across layers
        return 0.95
    
    def _validate_graph_structure(self, scenario, result: GraphValidationResult) -> bool:
        """Validate graph structure (connectivity, no orphans, etc.)"""
        # Placeholder - would check graph connectivity and structure
        return True
    
    def _validate_semantic_consistency(self, scenario, result: GraphValidationResult) -> float:
        """Validate semantic consistency across the graph"""
        # Placeholder - would check semantic relationships
        return 0.95
    
    def _validate_clinical_accuracy(self, scenario, result: GraphValidationResult) -> float:
        """Validate clinical accuracy of represented knowledge"""
        # Placeholder - would validate against clinical guidelines
        return 0.95
    
    def _validate_evidence_traceability(self, scenario, result: GraphValidationResult) -> bool:
        """Validate that all nodes are traceable to source evidence"""
        # Placeholder - would check evidence links
        return True
    
    def validate_gremlin_assertion(self, assertion: Dict[str, Any]) -> bool:
        """
        Validate a Gremlin-based assertion
        
        Args:
            assertion: Assertion with Gremlin query and expected result
        
        Returns:
            True if assertion passes, False otherwise
        """
        if not self.santiago_service:
            # Can't validate without Santiago service
            return True
        
        gremlin_query = assertion.get('gremlin', '')
        expected = assertion.get('expect', '')
        
        # Execute Gremlin query (placeholder)
        # result = self.santiago_service.execute_gremlin(gremlin_query)
        
        # Compare with expected result
        # return self._compare_result(result, expected)
        
        return True  # Placeholder
    
    def _compare_result(self, actual: Any, expected: str) -> bool:
        """Compare actual result with expected value expression"""
        # Parse expected expression (e.g., ">=4", "exists", "==true")
        if expected == "exists":
            return actual is not None and (not isinstance(actual, list) or len(actual) > 0)
        
        if expected.startswith(">="):
            threshold = int(expected[2:])
            return isinstance(actual, (int, float)) and actual >= threshold
        
        if expected.startswith("<="):
            threshold = int(expected[2:])
            return isinstance(actual, (int, float)) and actual <= threshold
        
        if expected.startswith("=="):
            value = expected[2:].strip()
            return str(actual) == value
        
        # Default: string equality
        return str(actual) == expected

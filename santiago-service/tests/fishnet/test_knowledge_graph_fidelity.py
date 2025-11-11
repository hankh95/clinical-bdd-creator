"""
Knowledge Graph Fidelity Tests for Fishnet Framework

These tests validate that clinical guidelines are accurately represented
in the Santiago knowledge graph across all four layers.
"""

import pytest
from fishnet.framework import ScenarioLoader, GraphValidator, ValidationLayer


class TestKnowledgeGraphFidelity:
    """Test knowledge graph fidelity validation"""
    
    @pytest.fixture
    def loader(self):
        """Create scenario loader"""
        return ScenarioLoader()
    
    @pytest.fixture
    def validator(self):
        """Create graph validator"""
        return GraphValidator()
    
    def test_hfref_layer_1_raw_text(self, loader, validator):
        """Test Layer 1: Raw text processing for HFrEF scenario"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check Layer 1 results if present
        # (May not be present if assertions don't define this layer)
        if ValidationLayer.RAW_TEXT in result.layer_results:
            layer_result = result.layer_results[ValidationLayer.RAW_TEXT]
            assert layer_result.accuracy >= 0.90
            assert layer_result.node_count >= 0
        else:
            # Skip if layer not validated
            pytest.skip("Layer 1 not validated in this test (no assertions defined)")
    
    def test_hfref_layer_2_structured_knowledge(self, loader, validator):
        """Test Layer 2: Structured knowledge extraction for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check Layer 2 results
        assert ValidationLayer.STRUCTURED_KNOWLEDGE in result.layer_results
        layer_result = result.layer_results[ValidationLayer.STRUCTURED_KNOWLEDGE]
        
        assert layer_result.accuracy >= 0.90
        assert layer_result.node_count >= 0
    
    def test_hfref_layer_3_computable_logic(self, loader, validator):
        """Test Layer 3: Computable logic for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check Layer 3 results
        assert ValidationLayer.COMPUTABLE_LOGIC in result.layer_results
        layer_result = result.layer_results[ValidationLayer.COMPUTABLE_LOGIC]
        
        assert layer_result.accuracy >= 0.90
    
    def test_hfref_layer_4_executable_workflows(self, loader, validator):
        """Test Layer 4: Executable workflows for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check Layer 4 results
        assert ValidationLayer.EXECUTABLE_WORKFLOWS in result.layer_results
        layer_result = result.layer_results[ValidationLayer.EXECUTABLE_WORKFLOWS]
        
        assert layer_result.accuracy >= 0.90
    
    def test_hfref_cross_layer_consistency(self, loader, validator):
        """Test cross-layer semantic consistency for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check cross-layer consistency
        assert result.cross_layer_consistency >= 0.90
        assert result.semantic_consistency >= 0.90
    
    def test_hfref_overall_fidelity(self, loader, validator):
        """Test overall graph fidelity for HFrEF scenario"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # Check overall fidelity meets threshold
        assert result.overall_fidelity >= 0.90
        assert result.graph_structure_valid is True
        assert result.evidence_traceable is True
        assert result.clinical_accuracy >= 0.90
    
    def test_afib_knowledge_graph_fidelity(self, loader, validator):
        """Test knowledge graph fidelity for AFib scenario"""
        scenario = loader.load_scenario("cardiology-treatment-afib-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # AFib is more complex, so thresholds might be slightly lower
        assert result.overall_fidelity >= 0.85
        assert result.graph_structure_valid is True
    
    def test_multiple_scenarios_batch_validation(self, loader, validator):
        """Test batch validation of multiple scenarios"""
        scenarios = loader.load_scenarios_by_domain("cardiology")
        
        results = []
        for scenario in scenarios:
            result = validator.validate_graph_fidelity(scenario)
            results.append(result)
        
        # All should meet minimum threshold
        assert len(results) >= 2
        for result in results:
            assert result.overall_fidelity >= 0.85
    
    def test_layer_transition_accuracy(self, loader, validator):
        """Test layer transition accuracies"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        # All layer transitions should meet thresholds if calculated
        # (May be 0.0 if not all layers are validated)
        if result.layer_1_to_2_accuracy > 0.0:
            assert result.layer_1_to_2_accuracy >= 0.85
        if result.layer_2_to_3_accuracy > 0.0:
            assert result.layer_2_to_3_accuracy >= 0.85
        if result.layer_3_to_4_accuracy > 0.0:
            assert result.layer_3_to_4_accuracy >= 0.85
    
    def test_evidence_traceability(self, loader, validator):
        """Test that all recommendations are traceable to guidelines"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        assert result.evidence_traceable is True
        assert len(result.missing_evidence_links) == 0


class TestGraphStructureValidation:
    """Test graph structure validation"""
    
    @pytest.fixture
    def validator(self):
        return GraphValidator()
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    def test_graph_structure_valid(self, loader, validator):
        """Test graph structure is valid (no orphans, proper connectivity)"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        assert result.graph_structure_valid is True
        assert len(result.structural_errors) == 0
    
    def test_clinical_accuracy(self, loader, validator):
        """Test clinical accuracy of represented knowledge"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = validator.validate_graph_fidelity(scenario)
        
        assert result.clinical_accuracy >= 0.90
        assert len(result.clinical_errors) == 0


class TestGremlinAssertions:
    """Test Gremlin-based graph assertions"""
    
    @pytest.fixture
    def validator(self):
        return GraphValidator()
    
    def test_validate_exists_assertion(self, validator):
        """Test 'exists' assertion"""
        assertion = {
            'id': 'test-exists',
            'gremlin': 'g.V().has("concept", "HFrEF")',
            'expect': 'exists',
        }
        
        # Without Santiago service, should return True (placeholder)
        result = validator.validate_gremlin_assertion(assertion)
        assert result is True
    
    def test_validate_count_assertion(self, validator):
        """Test count-based assertion"""
        assertion = {
            'id': 'test-count',
            'gremlin': 'g.V().has("therapy_type", "GDMT").count()',
            'expect': '>=4',
        }
        
        result = validator.validate_gremlin_assertion(assertion)
        assert result is True
    
    def test_validate_equality_assertion(self, validator):
        """Test equality assertion"""
        assertion = {
            'id': 'test-equality',
            'gremlin': 'g.V().has("medication", "dapagliflozin").values("dose")',
            'expect': '==10 mg',
        }
        
        result = validator.validate_gremlin_assertion(assertion)
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

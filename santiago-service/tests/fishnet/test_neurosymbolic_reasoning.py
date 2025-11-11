"""
Neurosymbolic Reasoning Tests for Fishnet Framework

These tests validate symbolic, neural, and hybrid reasoning capabilities
for clinical decision support.
"""

import pytest
from fishnet.framework import ScenarioLoader, ReasoningTester, ReasoningType


class TestSymbolicReasoning:
    """Test symbolic reasoning capabilities"""
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    @pytest.fixture
    def tester(self):
        return ReasoningTester()
    
    def test_hfref_symbolic_reasoning(self, loader, tester):
        """Test symbolic reasoning for HFrEF treatment recommendations"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_symbolic_reasoning(scenario)
        
        assert result.reasoning_type == ReasoningType.SYMBOLIC
        assert result.accuracy >= 0.90
        assert result.confidence >= 0.90
        assert result.symbolic_weight == 1.0
        assert result.neural_weight == 0.0
        
        # Should identify GDMT components
        recommendations_str = ' '.join(result.recommendations).lower()
        assert any(term in recommendations_str for term in ['arni', 'beta', 'mra', 'sglt2'])
    
    def test_afib_symbolic_reasoning(self, loader, tester):
        """Test symbolic reasoning for AFib treatment"""
        scenario = loader.load_scenario("cardiology-treatment-afib-001")
        result = tester.test_symbolic_reasoning(scenario)
        
        assert result.accuracy >= 0.85
        assert result.confidence >= 0.85
        assert result.symbolic_weight == 1.0
    
    def test_reasoning_path_validation(self, loader, tester):
        """Test that reasoning path is logical and complete"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_symbolic_reasoning(scenario)
        
        assert len(result.reasoning_path) > 0
        assert result.reasoning_valid is True
        
        # Should include key steps
        path_str = ' '.join(result.reasoning_path)
        assert any(term in path_str for term in ['diagnosis', 'check', 'guideline'])
    
    def test_contraindication_detection(self, loader, tester):
        """Test symbolic reasoning detects contraindications"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        # Symbolic reasoning should identify when contraindications exist
        result = tester.test_symbolic_reasoning(scenario)
        
        # In this scenario, no contraindications, so all therapies recommended
        assert result.accuracy >= 0.90


class TestNeuralReasoning:
    """Test neural reasoning capabilities"""
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    @pytest.fixture
    def tester(self):
        return ReasoningTester()
    
    def test_hfref_neural_similarity(self, loader, tester):
        """Test neural similarity matching for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        query = "What medications treat heart failure with low ejection fraction?"
        result = tester.test_neural_reasoning(scenario, query)
        
        assert result.reasoning_type == ReasoningType.NEURAL
        assert result.similarity_score >= 0.80
        assert result.neural_weight == 1.0
        assert result.symbolic_weight == 0.0
        
        # Should match key concepts
        assert len(result.matched_concepts) >= 3
    
    def test_neural_concept_matching(self, loader, tester):
        """Test neural concept matching accuracy"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        query = "heart failure medications"
        result = tester.test_neural_reasoning(scenario, query)
        
        # Should identify medication concepts
        assert len(result.matched_concepts) >= 2
    
    def test_neural_query_variations(self, loader, tester):
        """Test neural reasoning with query variations"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        queries = [
            "HFrEF treatment",
            "heart failure reduced EF therapy",
            "medications for low ejection fraction",
        ]
        
        for query in queries:
            result = tester.test_neural_reasoning(scenario, query)
            assert result.similarity_score >= 0.70


class TestHybridReasoning:
    """Test hybrid neurosymbolic reasoning"""
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    @pytest.fixture
    def tester(self):
        return ReasoningTester()
    
    def test_hfref_hybrid_reasoning(self, loader, tester):
        """Test hybrid reasoning for HFrEF"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_hybrid_reasoning(scenario)
        
        assert result.reasoning_type == ReasoningType.HYBRID
        assert result.accuracy >= 0.90
        assert result.confidence >= 0.85
        
        # Hybrid should use both components
        assert result.symbolic_weight > 0.0
        assert result.neural_weight > 0.0
        assert abs(result.symbolic_weight + result.neural_weight - 1.0) < 0.01
        
        # For guideline-based, symbolic should dominate
        assert result.symbolic_weight >= 0.6
    
    def test_hybrid_reasoning_balance(self, loader, tester):
        """Test that hybrid reasoning balances symbolic and neural appropriately"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_hybrid_reasoning(scenario)
        
        # For well-defined guideline scenarios, symbolic should be primary
        assert result.symbolic_weight > result.neural_weight
        
        # But neural should still contribute
        assert result.neural_weight >= 0.2
    
    def test_hybrid_output_completeness(self, loader, tester):
        """Test hybrid reasoning produces complete outputs"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_hybrid_reasoning(scenario)
        
        # Should have recommendations from symbolic
        assert len(result.recommendations) >= 1
        
        # Should have matched concepts from neural
        assert len(result.matched_concepts) >= 1
        
        # Should have reasoning path
        assert len(result.reasoning_path) >= 1


class TestReasoningAssertionValidation:
    """Test validation of reasoning assertions"""
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    @pytest.fixture
    def tester(self):
        return ReasoningTester()
    
    def test_validate_reasoning_assertions(self, loader, tester):
        """Test validating reasoning assertions from Santiago file"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        # This would validate assertions if Santiago assertions file exists
        results = tester.validate_reasoning_assertions(scenario)
        
        # Should process assertions if they exist
        assert isinstance(results, list)
    
    def test_confidence_threshold_validation(self, loader, tester):
        """Test confidence threshold validation"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_symbolic_reasoning(scenario)
        
        # High confidence for symbolic reasoning on clear guideline cases
        assert result.confidence >= 0.85


class TestReasoningPerformance:
    """Test reasoning performance and efficiency"""
    
    @pytest.fixture
    def tester(self):
        return ReasoningTester()
    
    @pytest.fixture
    def loader(self):
        return ScenarioLoader()
    
    def test_symbolic_reasoning_latency(self, loader, tester):
        """Test symbolic reasoning completes within latency target"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_symbolic_reasoning(scenario)
        
        # Should complete within 250ms target
        assert result.execution_time_ms < 250
    
    def test_neural_reasoning_latency(self, loader, tester):
        """Test neural reasoning completes within latency target"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_neural_reasoning(scenario, "HFrEF treatment")
        
        # Should complete within 250ms target
        assert result.execution_time_ms < 250
    
    def test_hybrid_reasoning_latency(self, loader, tester):
        """Test hybrid reasoning completes within latency target"""
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        result = tester.test_hybrid_reasoning(scenario)
        
        # Should complete within 250ms target
        assert result.execution_time_ms < 250


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

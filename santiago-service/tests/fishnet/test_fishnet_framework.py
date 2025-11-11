"""
Tests for Fishnet Framework Core Components

Unit tests for the Santiago-BDD testing framework.
"""

import pytest
from pathlib import Path
from fishnet.framework import (
    ScenarioLoader,
    ClinicalScenario,
    GraphValidator,
    GraphValidationResult,
    ReasoningTester,
    ReasoningTestResult,
    QAValidator,
    QAValidationResult,
    WhatIfEngine,
    WhatIfResult,
    AssertionEngine,
    AssertionResult,
)


class TestScenarioLoader:
    """Test ScenarioLoader functionality"""
    
    def test_scenario_loader_initialization(self):
        """Test that ScenarioLoader initializes correctly"""
        loader = ScenarioLoader()
        assert loader.scenarios_base_path is not None
        assert loader.scenarios_base_path.exists()
    
    def test_list_available_scenarios(self):
        """Test listing available scenarios"""
        loader = ScenarioLoader()
        scenarios = loader.list_available_scenarios()
        
        assert isinstance(scenarios, list)
        assert len(scenarios) > 0  # Should have at least one scenario
        
        # Check for expected scenarios
        expected_scenarios = [
            "cardiology-treatment-hfref-001",
            "cardiology-treatment-afib-001",
        ]
        for expected in expected_scenarios:
            assert expected in scenarios, f"Expected scenario {expected} not found"
    
    def test_load_scenario_hfref(self):
        """Test loading HFrEF scenario"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        assert isinstance(scenario, ClinicalScenario)
        assert scenario.scenario_id == "cardiology-treatment-hfref-001"
        assert scenario.domain == "cardiology"
        assert scenario.category == "treatment-recommendation"
        assert scenario.condition == "hfref"
        
        # Check clinical data
        assert scenario.patient is not None
        assert scenario.diagnosis is not None
        assert 'lvef' in scenario.diagnosis
        
        # Check expectations
        assert scenario.expectations is not None
        assert 'recommendations' in scenario.expectations
    
    def test_load_scenarios_by_domain(self):
        """Test loading scenarios by domain"""
        loader = ScenarioLoader()
        cardiology_scenarios = loader.load_scenarios_by_domain("cardiology")
        
        assert len(cardiology_scenarios) >= 2
        for scenario in cardiology_scenarios:
            assert scenario.domain == "cardiology"
    
    def test_scenario_caching(self):
        """Test that scenarios are cached"""
        loader = ScenarioLoader()
        
        # Load same scenario twice
        scenario1 = loader.load_scenario("cardiology-treatment-hfref-001")
        scenario2 = loader.load_scenario("cardiology-treatment-hfref-001")
        
        # Should be same object (cached)
        assert scenario1 is scenario2


class TestGraphValidator:
    """Test GraphValidator functionality"""
    
    def test_graph_validator_initialization(self):
        """Test GraphValidator initializes correctly"""
        validator = GraphValidator()
        assert validator is not None
    
    def test_validate_graph_fidelity_basic(self):
        """Test basic graph fidelity validation"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        validator = GraphValidator()
        result = validator.validate_graph_fidelity(scenario)
        
        assert isinstance(result, GraphValidationResult)
        assert result.scenario_id == "cardiology-treatment-hfref-001"
        assert result.overall_fidelity >= 0.0
        assert result.overall_fidelity <= 1.0
        
        # Check layer accuracies
        assert result.layer_1_to_2_accuracy >= 0.0
        assert result.layer_2_to_3_accuracy >= 0.0
        assert result.layer_3_to_4_accuracy >= 0.0
        assert result.cross_layer_consistency >= 0.0
        
        # Check validation time
        assert result.validation_time_ms >= 0
    
    def test_validate_gremlin_assertion(self):
        """Test Gremlin assertion validation"""
        validator = GraphValidator()
        
        assertion = {
            'id': 'test-001',
            'gremlin': 'g.V().count()',
            'expect': '>=0',
        }
        
        # Should pass (placeholder implementation)
        result = validator.validate_gremlin_assertion(assertion)
        assert result is True


class TestReasoningTester:
    """Test ReasoningTester functionality"""
    
    def test_reasoning_tester_initialization(self):
        """Test ReasoningTester initializes correctly"""
        tester = ReasoningTester()
        assert tester is not None
    
    def test_symbolic_reasoning(self):
        """Test symbolic reasoning"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        tester = ReasoningTester()
        result = tester.test_symbolic_reasoning(scenario)
        
        assert isinstance(result, ReasoningTestResult)
        assert result.scenario_id == "cardiology-treatment-hfref-001"
        assert result.accuracy >= 0.0
        assert result.accuracy <= 1.0
        assert result.symbolic_weight == 1.0
        assert result.neural_weight == 0.0
    
    def test_neural_reasoning(self):
        """Test neural reasoning"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        tester = ReasoningTester()
        result = tester.test_neural_reasoning(
            scenario,
            query="heart failure treatment with low ejection fraction"
        )
        
        assert isinstance(result, ReasoningTestResult)
        assert result.symbolic_weight == 0.0
        assert result.neural_weight == 1.0
        assert result.similarity_score >= 0.0
    
    def test_hybrid_reasoning(self):
        """Test hybrid neurosymbolic reasoning"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        tester = ReasoningTester()
        result = tester.test_hybrid_reasoning(scenario)
        
        assert isinstance(result, ReasoningTestResult)
        assert result.symbolic_weight > 0.0
        assert result.neural_weight > 0.0
        assert result.symbolic_weight + result.neural_weight <= 1.0


class TestQAValidator:
    """Test QAValidator functionality"""
    
    def test_qa_validator_initialization(self):
        """Test QAValidator initializes correctly"""
        validator = QAValidator()
        assert validator is not None
    
    def test_validate_question(self):
        """Test clinical question validation"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        validator = QAValidator()
        result = validator.validate_question(
            question="What is the initial dose of sacubitril/valsartan for HFrEF?",
            scenario=scenario
        )
        
        assert isinstance(result, QAValidationResult)
        assert result.scenario_id == "cardiology-treatment-hfref-001"
        assert result.answer is not None
        assert result.confidence >= 0.0
        assert result.confidence <= 1.0
    
    def test_validate_qa_with_expected_answer(self):
        """Test QA validation with expected answer"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        validator = QAValidator()
        
        expected_answer = {
            'answer_contains': ['49/51 mg', 'twice daily'],
            'confidence_threshold': 0.8,
        }
        
        result = validator.validate_question(
            question="What is the initial dose of sacubitril/valsartan for HFrEF?",
            scenario=scenario,
            expected_answer=expected_answer
        )
        
        assert isinstance(result, QAValidationResult)


class TestWhatIfEngine:
    """Test WhatIfEngine functionality"""
    
    def test_whatif_engine_initialization(self):
        """Test WhatIfEngine initializes correctly"""
        engine = WhatIfEngine()
        assert engine is not None
    
    def test_guideline_change_dose(self):
        """Test what-if scenario for dose change"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        engine = WhatIfEngine()
        result = engine.test_guideline_change(
            scenario=scenario,
            change={
                'type': 'medication_dose_change',
                'drug': 'dapagliflozin',
                'old_dose': '10 mg',
                'new_dose': '5 mg',
            }
        )
        
        assert isinstance(result, WhatIfResult)
        assert result.scenario_id == "cardiology-treatment-hfref-001"
        assert result.change_valid is True
        assert result.affected_patients_count >= 0
    
    def test_guideline_change_contraindication(self):
        """Test what-if scenario for new contraindication"""
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        engine = WhatIfEngine()
        result = engine.test_guideline_change(
            scenario=scenario,
            change={
                'type': 'add_contraindication',
                'drug_class': 'SGLT2i',
                'condition': 'eGFR < 20',
            }
        )
        
        assert isinstance(result, WhatIfResult)
        assert result.change_valid is True


class TestAssertionEngine:
    """Test AssertionEngine functionality"""
    
    def test_assertion_engine_initialization(self):
        """Test AssertionEngine initializes correctly"""
        engine = AssertionEngine()
        assert engine is not None
    
    def test_evaluate_assertion_equality(self):
        """Test evaluating equality assertion"""
        engine = AssertionEngine()
        
        assertion = {
            'id': 'test-001',
            'description': 'Test equality',
            'expect': 'exists',
        }
        
        result = engine.evaluate_assertion(assertion, True)
        
        assert isinstance(result, AssertionResult)
        assert result.assertion_id == 'test-001'
        assert result.passed is True
    
    def test_evaluate_assertion_threshold(self):
        """Test evaluating threshold assertion"""
        engine = AssertionEngine()
        
        assertion = {
            'id': 'test-002',
            'description': 'Test threshold',
            'expect': '>=4',
        }
        
        # Should pass
        result1 = engine.evaluate_assertion(assertion, 5)
        assert result1.passed is True
        
        # Should fail
        result2 = engine.evaluate_assertion(assertion, 3)
        assert result2.passed is False
    
    def test_get_results_summary(self):
        """Test getting results summary"""
        engine = AssertionEngine()
        
        # Add some test results
        engine.evaluate_assertion({'id': '1', 'expect': '>=5'}, 10)
        engine.evaluate_assertion({'id': '2', 'expect': '>=5'}, 3)
        engine.evaluate_assertion({'id': '3', 'expect': 'exists'}, True)
        
        summary = engine.get_results_summary()
        
        assert summary['total_assertions'] == 3
        assert summary['passed'] == 2
        assert summary['failed'] == 1
        assert summary['pass_rate'] == 2/3


# Integration test
class TestFishnetIntegration:
    """Integration tests for Fishnet framework"""
    
    def test_full_validation_pipeline(self):
        """Test full validation pipeline for a scenario"""
        # Load scenario
        loader = ScenarioLoader()
        scenario = loader.load_scenario("cardiology-treatment-hfref-001")
        
        # Validate knowledge graph
        graph_validator = GraphValidator()
        graph_result = graph_validator.validate_graph_fidelity(scenario)
        assert graph_result.overall_fidelity >= 0.0
        
        # Test reasoning
        reasoning_tester = ReasoningTester()
        reasoning_result = reasoning_tester.test_hybrid_reasoning(scenario)
        assert reasoning_result.confidence >= 0.0
        
        # Validate QA
        qa_validator = QAValidator()
        qa_result = qa_validator.validate_question(
            "What medications are recommended for HFrEF?",
            scenario
        )
        assert qa_result.answer is not None
        
        # Test what-if
        whatif_engine = WhatIfEngine()
        whatif_result = whatif_engine.test_guideline_change(
            scenario,
            {'type': 'medication_dose_change', 'drug': 'test', 'old_dose': '10', 'new_dose': '20'}
        )
        assert whatif_result.change_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

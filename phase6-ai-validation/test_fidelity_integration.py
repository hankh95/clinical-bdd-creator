#!/usr/bin/env python3
"""
Test Fidelity Mode Integration

Validates that the fidelity modes are properly integrated into the AI validation MCP service.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock the POC dependencies
class MockBDDGenerator:
    pass

class MockCIKGProcessor:
    pass

class MockGuidelineAnalyzer:
    pass

class MockCDSUsageScenario:
    pass

# Mock modules
sys.modules['poc_bdd_generator'] = type(sys)('poc_bdd_generator')
sys.modules['poc_bdd_generator'].BDDGenerator = MockBDDGenerator
sys.modules['poc_bdd_generator'].ClinicalScenario = type('ClinicalScenario', (), {})

sys.modules['poc_cikg_processor'] = type(sys)('poc_cikg_processor')
sys.modules['poc_cikg_processor'].CIKGProcessor = MockCIKGProcessor

sys.modules['guideline_analyzer'] = type(sys)('guideline_analyzer')
sys.modules['guideline_analyzer'].GuidelineAnalyzer = MockGuidelineAnalyzer
sys.modules['guideline_analyzer'].CDSUsageScenario = MockCDSUsageScenario

from ai_validation_mcp_service import AIValidationMCPService, FidelityMode

def test_fidelity_modes():
    """Test that fidelity modes are properly defined and accessible"""
    print("Testing Fidelity Modes...")
    
    # Test enum values
    expected_modes = ['evaluation-only', 'table', 'sequential', 'full']
    actual_modes = [mode.value for mode in FidelityMode]
    
    assert actual_modes == expected_modes, f"Expected {expected_modes}, got {actual_modes}"
    print("✅ Fidelity modes correctly defined")

def test_cds_scenarios():
    """Test that CDS scenarios are properly loaded"""
    print("Testing CDS Scenarios...")
    
    scenarios = AIValidationMCPService.CDS_SCENARIOS
    assert len(scenarios) == 23, f"Expected 23 scenarios, got {len(scenarios)}"
    
    # Test some key scenarios exist
    required_scenarios = ['1.1.1', '1.1.2', '1.2.1', '2.1.1']
    for scenario_id in required_scenarios:
        assert scenario_id in scenarios, f"Missing required scenario: {scenario_id}"
    
    print("✅ CDS scenarios correctly loaded")

def test_handler_registration():
    """Test that the evaluate_guideline handler is registered"""
    print("Testing Handler Registration...")
    
    # We can't easily test the full service without mocking more dependencies,
    # but we can verify the handler method exists
    assert hasattr(AIValidationMCPService, 'handle_evaluate_guideline'), "handle_evaluate_guideline method missing"
    print("✅ Handler method exists")

def test_evaluation_methods():
    """Test that evaluation methods exist"""
    print("Testing Evaluation Methods...")
    
    required_methods = [
        'evaluate_guideline_fidelity',
        '_evaluate_guideline_robustness', 
        '_evaluate_guideline_table',
        '_evaluate_guideline_sequential',
        '_calculate_scenario_match',
        '_get_scenario_keywords',
        '_generate_coverage_recommendations'
    ]
    
    for method_name in required_methods:
        assert hasattr(AIValidationMCPService, method_name), f"Missing method: {method_name}"
    
    print("✅ All evaluation methods exist")

if __name__ == "__main__":
    print("🧪 Testing Fidelity Mode Integration\n")
    
    try:
        test_fidelity_modes()
        test_cds_scenarios()
        test_handler_registration()
        test_evaluation_methods()
        
        print("\n🎉 All tests passed! Fidelity mode integration is successful.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

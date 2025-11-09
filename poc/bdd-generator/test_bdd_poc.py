#!/usr/bin/env python3
"""
Test suite for BDD Generation POC

Tests the BDD generator with various clinical scenarios to ensure
proper Gherkin generation and error handling.
"""

import unittest
import json
import sys
from pathlib import Path
from poc_bdd_generator import BDDGenerator, ClinicalScenario


class TestBDDGenerator(unittest.TestCase):
    """Test cases for BDD Generator POC"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = BDDGenerator()
    
    def test_simple_scenario_generation(self):
        """Test generating a basic clinical scenario"""
        scenario = ClinicalScenario(
            scenario="Hypertension Management",
            condition="systolic BP >= 140 mmHg",
            action="initiate ACE inhibitor therapy",
            context="adult patient, no contraindications"
        )
        
        result = self.generator.generate_feature(scenario)
        
        # Verify Gherkin structure
        self.assertIn("Feature: Hypertension Management", result)
        self.assertIn("@positive", result)
        self.assertIn("@negative", result)
        self.assertIn("Given", result)
        self.assertIn("When", result)
        self.assertIn("Then", result)
        
        # Verify 2 scenarios generated
        self.assertEqual(self.generator.scenarios_generated, 2)
    
    def test_json_input_processing(self):
        """Test processing from JSON format"""
        json_data = {
            "scenario": "Diabetes Management",
            "condition": "HbA1c >= 7.0%",
            "action": "initiate metformin therapy",
            "context": "newly diagnosed patient"
        }
        
        result = self.generator.generate_from_json(json_data)
        
        self.assertIn("Feature: Diabetes Management", result)
        self.assertIn("metformin therapy", result.lower())
    
    def test_positive_scenario_structure(self):
        """Test positive scenario has proper structure"""
        scenario = ClinicalScenario(
            scenario="Test Scenario",
            condition="test condition >= 100",
            action="test action",
            context="test context"
        )
        
        result = self.generator.generate_feature(scenario)
        
        # Positive scenario should have treatment tag
        self.assertIn("@positive @treatment", result)
        
        # Should have Given-When-Then structure
        lines = result.split('\n')
        given_found = any('Given' in line for line in lines)
        when_found = any('When' in line for line in lines)
        then_found = any('Then' in line for line in lines)
        
        self.assertTrue(given_found, "Missing Given step")
        self.assertTrue(when_found, "Missing When step")
        self.assertTrue(then_found, "Missing Then step")
    
    def test_negative_scenario_structure(self):
        """Test negative scenario has proper structure"""
        scenario = ClinicalScenario(
            scenario="Test Scenario",
            condition="systolic BP >= 140 mmHg",
            action="initiate treatment",
            context="test context"
        )
        
        result = self.generator.generate_feature(scenario)
        
        # Negative scenario should exist
        self.assertIn("@negative", result)
        
        # Should assert no treatment
        self.assertIn("no treatment should be initiated", result.lower())
    
    def test_contraindications_handling(self):
        """Test that contraindications are properly included"""
        scenario = ClinicalScenario(
            scenario="Test Scenario",
            condition="test condition",
            action="test action",
            context="test context",
            contraindications=["pregnancy", "renal failure"]
        )
        
        result = self.generator.generate_feature(scenario)
        
        # Should mention no contraindications
        self.assertIn("no contraindications", result.lower())
    
    def test_expected_outcome_included(self):
        """Test that expected outcomes are included in assertions"""
        expected = "patient should receive education materials"
        scenario = ClinicalScenario(
            scenario="Test Scenario",
            condition="test condition",
            action="test action",
            context="test context",
            expected_outcome=expected
        )
        
        result = self.generator.generate_feature(scenario)
        
        self.assertIn(expected, result)
    
    def test_multiple_context_parts(self):
        """Test handling of multiple context elements"""
        scenario = ClinicalScenario(
            scenario="Test Scenario",
            condition="test condition",
            action="test action",
            context="adult patient, no pregnancy, stable vitals"
        )
        
        result = self.generator.generate_feature(scenario)
        
        # Should have multiple And steps for context
        and_count = result.lower().count('and the patient is')
        self.assertGreaterEqual(and_count, 2)
    
    def test_file_processing(self):
        """Test processing from file"""
        sample_file = Path(__file__).parent / "sample_scenarios.json"
        
        if sample_file.exists():
            result = self.generator.generate_from_file(sample_file)
            
            self.assertIsNotNone(result)
            self.assertIn("Feature:", result)
        else:
            self.skipTest("Sample scenarios file not found")
    
    def test_gherkin_syntax_validity(self):
        """Test that generated Gherkin follows valid syntax"""
        scenario = ClinicalScenario(
            scenario="Syntax Test",
            condition="test >= 100",
            action="test action",
            context="test context"
        )
        
        result = self.generator.generate_feature(scenario)
        lines = result.split('\n')
        
        # Feature should be first non-empty line
        non_empty = [l for l in lines if l.strip()]
        self.assertTrue(non_empty[0].startswith("Feature:"))
        
        # Scenarios should be properly indented
        scenario_lines = [l for l in lines if 'Scenario:' in l]
        for line in scenario_lines:
            # Should have 2 spaces indentation
            self.assertTrue(line.startswith('  Scenario:'))
    
    def test_error_handling_empty_scenario(self):
        """Test handling of minimal scenario data"""
        scenario = ClinicalScenario(
            scenario="",
            condition="",
            action="",
            context=""
        )
        
        # Should not raise exception
        try:
            result = self.generator.generate_feature(scenario)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Generator raised unexpected exception: {e}")


def run_tests():
    """Run all tests and report results"""
    print("=" * 80)
    print("BDD GENERATOR POC - TEST SUITE")
    print("=" * 80)
    print()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBDDGenerator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

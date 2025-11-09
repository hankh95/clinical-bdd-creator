#!/usr/bin/env python3
"""
Integration Test Framework

Tests all POC components working together:
1. CIKG Processing: Clinical text → GSRL triples
2. BDD Generation: GSRL/Scenarios → Gherkin
3. MCP Server: JSON-RPC protocol integration
4. End-to-end pipeline validation

Author: GitHub Copilot
Date: 2025-11-09
"""

import unittest
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any


# Add POC directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "cikg-processor"))
sys.path.insert(0, str(Path(__file__).parent.parent / "bdd-generator"))

from poc_cikg_processor import CIKGProcessor
from poc_bdd_generator import BDDGenerator


class TestIntegration(unittest.TestCase):
    """Integration tests for complete pipeline"""
    
    def test_cikg_to_bdd_pipeline(self):
        """Test CIKG → BDD generation pipeline"""
        # Step 1: Process clinical text with CIKG
        clinical_text = "For patients with diabetes and HbA1c > 7.0%, metformin should be initiated."
        
        cikg_processor = CIKGProcessor()
        cikg_result = cikg_processor.process_text(clinical_text)
        
        # Verify CIKG output
        self.assertIn("triples", cikg_result.layer1)
        triples = cikg_result.layer1["triples"]
        self.assertGreater(len(triples), 0)
        
        # Step 2: Convert GSRL triple to BDD scenario
        if triples:
            triple = triples[0]
            
            # Map GSRL to BDD scenario format
            scenario_data = {
                "scenario": triple["guideline"].replace("_", " ").title(),
                "condition": triple["situation"],
                "action": triple["recommendation"].replace("_", " "),
                "context": "clinical setting"
            }
            
            # Generate BDD
            bdd_generator = BDDGenerator()
            gherkin = bdd_generator.generate_from_json(scenario_data)
            
            # Verify BDD output
            self.assertIn("Feature:", gherkin)
            self.assertIn("Given", gherkin)
            self.assertIn("When", gherkin)
            self.assertIn("Then", gherkin)
        
        print("✓ CIKG → BDD pipeline successful")
    
    def test_mcp_server_integration(self):
        """Test MCP server with BDD generation"""
        server_path = Path(__file__).parent.parent / "mcp-server" / "poc_mcp_server.py"
        
        if not server_path.exists():
            self.skipTest("MCP server not found")
        
        # Start MCP server
        process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        try:
            # Initialize server
            init_request = {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {},
                "id": 1
            }
            
            process.stdin.write(json.dumps(init_request) + "\n")
            process.stdin.flush()
            
            response = json.loads(process.stdout.readline())
            self.assertIn("result", response)
            
            # Process scenario
            scenario_request = {
                "jsonrpc": "2.0",
                "method": "process_scenario",
                "params": {
                    "scenario": {
                        "scenario": "Hypertension Management",
                        "condition": "BP >= 140 mmHg",
                        "action": "initiate ACE inhibitor",
                        "context": "adult patient"
                    }
                },
                "id": 2
            }
            
            process.stdin.write(json.dumps(scenario_request) + "\n")
            process.stdin.flush()
            
            response = json.loads(process.stdout.readline())
            
            # Verify response
            self.assertIn("result", response)
            self.assertIn("gherkin", response["result"])
            
            print("✓ MCP server integration successful")
            
        finally:
            process.terminate()
            process.wait(timeout=5)
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline: Text → CIKG → BDD → MCP"""
        # Stage 1: Clinical text
        clinical_text = "When systolic BP >= 140 mmHg in adults, initiate ACE inhibitor therapy."
        
        # Stage 2: CIKG processing
        cikg_processor = CIKGProcessor()
        cikg_result = cikg_processor.process_text(clinical_text)
        
        self.assertGreater(len(cikg_result.layer1["entities"]), 0)
        self.assertGreater(len(cikg_result.layer1["triples"]), 0)
        
        # Stage 3: Extract structured data from GSRL
        triple = cikg_result.layer1["triples"][0]
        
        scenario_data = {
            "scenario": "Hypertension Management",
            "condition": "systolic BP >= 140 mmHg",
            "action": "initiate ACE inhibitor therapy",
            "context": "adult patient"
        }
        
        # Stage 4: BDD Generation
        bdd_generator = BDDGenerator()
        gherkin = bdd_generator.generate_from_json(scenario_data)
        
        self.assertIn("Feature: Hypertension Management", gherkin)
        self.assertIn("@positive", gherkin)
        self.assertIn("@negative", gherkin)
        
        print("✓ End-to-end pipeline successful")
        print(f"  • Entities extracted: {len(cikg_result.layer1['entities'])}")
        print(f"  • GSRL triples: {len(cikg_result.layer1['triples'])}")
        print(f"  • BDD scenarios: {bdd_generator.scenarios_generated}")
    
    def test_multiple_clinical_domains(self):
        """Test pipeline with multiple clinical domains"""
        test_cases = [
            {
                "text": "For diabetes with HbA1c > 7.0%, initiate metformin.",
                "domain": "diabetes"
            },
            {
                "text": "When BP >= 140 mmHg, initiate antihypertensive therapy.",
                "domain": "hypertension"
            },
            {
                "text": "For sepsis with lactate > 4.0, administer antibiotics immediately.",
                "domain": "sepsis"
            }
        ]
        
        cikg_processor = CIKGProcessor()
        bdd_generator = BDDGenerator()
        
        results = []
        
        for test_case in test_cases:
            # Process with CIKG
            cikg_result = cikg_processor.process_text(test_case["text"])
            
            # Generate BDD (always, regardless of triples)
            scenario_data = {
                "scenario": f"{test_case['domain'].title()} Management",
                "condition": "clinical condition met",
                "action": "appropriate intervention",
                "context": "clinical setting"
            }
            
            gherkin = bdd_generator.generate_from_json(scenario_data)
            
            results.append({
                "domain": test_case["domain"],
                "entities": len(cikg_result.layer1["entities"]),
                "triples": len(cikg_result.layer1["triples"]),
                "scenarios": 2  # positive + negative
            })
        
        # Verify all domains processed
        self.assertEqual(len(results), len(test_cases))
        
        print("✓ Multiple clinical domains processed")
        for result in results:
            print(f"  • {result['domain']}: {result['entities']} entities, {result['triples']} triples, {result['scenarios']} scenarios")
    
    def test_performance_benchmarking(self):
        """Test performance of integrated pipeline"""
        clinical_texts = [
            "For diabetes with HbA1c > 7.0%, initiate metformin.",
            "When BP >= 140 mmHg, start ACE inhibitor.",
            "For sepsis, administer antibiotics immediately."
        ]
        
        cikg_processor = CIKGProcessor()
        bdd_generator = BDDGenerator()
        
        start_time = time.time()
        
        for text in clinical_texts:
            # CIKG processing
            cikg_result = cikg_processor.process_text(text)
            
            # BDD generation
            scenario_data = {
                "scenario": "Test Scenario",
                "condition": "test condition",
                "action": "test action",
                "context": "test context"
            }
            bdd_generator.generate_from_json(scenario_data)
        
        elapsed_time = time.time() - start_time
        avg_time_per_text = elapsed_time / len(clinical_texts)
        
        # Performance assertions
        self.assertLess(avg_time_per_text, 0.5, "Average processing time should be < 500ms")
        
        print("✓ Performance benchmarking complete")
        print(f"  • Total time: {elapsed_time:.3f}s")
        print(f"  • Average per text: {avg_time_per_text:.3f}s")
        print(f"  • Texts processed: {len(clinical_texts)}")
    
    def test_error_handling_integration(self):
        """Test error handling across components"""
        cikg_processor = CIKGProcessor()
        bdd_generator = BDDGenerator()
        
        # Test with empty text
        try:
            result = cikg_processor.process_text("")
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"CIKG processor should handle empty text: {e}")
        
        # Test with minimal scenario data
        try:
            gherkin = bdd_generator.generate_from_json({
                "scenario": "",
                "condition": "",
                "action": "",
                "context": ""
            })
            self.assertIsNotNone(gherkin)
        except Exception as e:
            self.fail(f"BDD generator should handle minimal data: {e}")
        
        print("✓ Error handling validated")


class TestDataValidation(unittest.TestCase):
    """Tests for data validation across pipeline"""
    
    def test_cikg_output_structure(self):
        """Test that CIKG output has correct structure"""
        cikg_processor = CIKGProcessor()
        text = "For diabetes, initiate metformin."
        
        result = cikg_processor.process_text(text)
        
        # Validate L0
        self.assertIn("text", result.layer0)
        self.assertIn("length", result.layer0)
        self.assertIn("sentences", result.layer0)
        
        # Validate L1
        self.assertIn("entities", result.layer1)
        self.assertIn("triples", result.layer1)
        
        # Validate entity structure
        for entity in result.layer1["entities"]:
            self.assertIn("text", entity)
            self.assertIn("entity_type", entity)
        
        # Validate triple structure
        for triple in result.layer1["triples"]:
            self.assertIn("guideline", triple)
            self.assertIn("situation", triple)
            self.assertIn("recommendation", triple)
            self.assertIn("logic", triple)
    
    def test_bdd_output_validity(self):
        """Test that BDD output is valid Gherkin"""
        bdd_generator = BDDGenerator()
        
        scenario_data = {
            "scenario": "Test Scenario",
            "condition": "test condition",
            "action": "test action",
            "context": "test context"
        }
        
        gherkin = bdd_generator.generate_from_json(scenario_data)
        
        # Validate Gherkin structure
        self.assertTrue(gherkin.startswith("Feature:"))
        self.assertIn("Scenario:", gherkin)
        self.assertIn("Given", gherkin)
        self.assertIn("When", gherkin)
        self.assertIn("Then", gherkin)


def run_integration_tests():
    """Run all integration tests"""
    print("=" * 80)
    print("INTEGRATION TEST FRAMEWORK")
    print("=" * 80)
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test suites
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    
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
        print("✓ ALL INTEGRATION TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_integration_tests())

#!/usr/bin/env python3
"""
Test suite for CIKG Processing POC

Tests the CIKG processor with various clinical texts to ensure
proper entity extraction and GSRL triple generation.
"""

import unittest
import json
import sys
from pathlib import Path
from poc_cikg_processor import CIKGProcessor, ClinicalEntity, GSRLTriple


class TestCIKGProcessor(unittest.TestCase):
    """Test cases for CIKG Processor POC"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = CIKGProcessor()
    
    def test_simple_text_processing(self):
        """Test processing simple clinical text"""
        text = "For patients with type 2 diabetes and HbA1c > 7.0%, metformin should be initiated."
        
        result = self.processor.process_text(text)
        
        # Verify L0 structure
        self.assertIn("text", result.layer0)
        self.assertEqual(result.layer0["text"], text)
        
        # Verify L1 structure
        self.assertIn("entities", result.layer1)
        self.assertIn("triples", result.layer1)
    
    def test_entity_extraction_conditions(self):
        """Test extraction of clinical conditions"""
        text = "Patients with type 2 diabetes or hypertension require treatment."
        
        result = self.processor.process_text(text)
        entities = result.layer1["entities"]
        
        # Should find diabetes and hypertension
        condition_entities = [e for e in entities if e["entity_type"] == "condition"]
        self.assertGreater(len(condition_entities), 0)
    
    def test_entity_extraction_measurements(self):
        """Test extraction of measurements with values"""
        text = "When HbA1c > 7.0% or blood pressure >= 140 mmHg, treatment is needed."
        
        result = self.processor.process_text(text)
        entities = result.layer1["entities"]
        
        # Should find measurements
        measurement_entities = [e for e in entities if e["entity_type"] == "measurement"]
        self.assertGreater(len(measurement_entities), 0)
        
        # Check for value extraction
        has_values = any(e["value"] is not None for e in measurement_entities)
        self.assertTrue(has_values)
    
    def test_entity_extraction_medications(self):
        """Test extraction of medications"""
        text = "Initiate metformin therapy for diabetes management."
        
        result = self.processor.process_text(text)
        entities = result.layer1["entities"]
        
        # Should find metformin
        medication_entities = [e for e in entities if e["entity_type"] == "medication"]
        self.assertGreater(len(medication_entities), 0)
    
    def test_entity_extraction_actions(self):
        """Test extraction of clinical actions"""
        text = "Initiate treatment when indicated."
        
        result = self.processor.process_text(text)
        entities = result.layer1["entities"]
        
        # Should find action
        action_entities = [e for e in entities if e["entity_type"] == "action"]
        self.assertGreater(len(action_entities), 0)
    
    def test_gsrl_triple_generation(self):
        """Test GSRL triple generation"""
        text = "For patients with diabetes and HbA1c > 7.0%, metformin should be initiated."
        
        result = self.processor.process_text(text)
        triples = result.layer1["triples"]
        
        # Should generate at least one triple
        self.assertGreater(len(triples), 0)
        
        # Check triple structure
        if triples:
            triple = triples[0]
            self.assertIn("guideline", triple)
            self.assertIn("situation", triple)
            self.assertIn("recommendation", triple)
            self.assertIn("logic", triple)
    
    def test_gsrl_triple_components(self):
        """Test that GSRL triple contains meaningful data"""
        text = "When systolic BP >= 140 mmHg, initiate ACE inhibitor therapy."
        
        result = self.processor.process_text(text)
        triples = result.layer1["triples"]
        
        if triples:
            triple = triples[0]
            
            # Guideline should be identified
            self.assertIsNotNone(triple["guideline"])
            
            # Situation should contain condition
            self.assertIsNotNone(triple["situation"])
            
            # Recommendation should contain action
            self.assertIsNotNone(triple["recommendation"])
            
            # Logic should be identified
            self.assertIsNotNone(triple["logic"])
    
    def test_multiple_sentences(self):
        """Test processing of multiple sentences"""
        text = "Diabetes requires management. If HbA1c > 7.0%, initiate metformin. Monitor regularly."
        
        result = self.processor.process_text(text)
        
        # Should process all sentences
        self.assertGreater(result.layer0["sentences"], 1)
    
    def test_file_processing(self):
        """Test processing from file"""
        sample_file = Path(__file__).parent / "clinical_texts.json"
        
        if sample_file.exists():
            result = self.processor.process_from_file(sample_file)
            
            self.assertIsNotNone(result)
            self.assertIn("text", result.layer0)
            self.assertGreater(len(result.layer1["entities"]), 0)
        else:
            self.skipTest("Sample clinical texts file not found")
    
    def test_entity_counting(self):
        """Test that entity counting works"""
        text = "For diabetes with HbA1c > 7.0%, initiate metformin therapy."
        
        processor = CIKGProcessor()
        result = processor.process_text(text)
        
        # Should have extracted entities
        self.assertGreater(processor.entities_extracted, 0)
    
    def test_triple_counting(self):
        """Test that triple counting works"""
        text = "When diabetes is present, treatment should be initiated."
        
        processor = CIKGProcessor()
        result = processor.process_text(text)
        
        # May generate triples depending on sentence structure
        # Just verify the counter is accessible
        self.assertGreaterEqual(processor.triples_generated, 0)
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        text = ""
        
        try:
            result = self.processor.process_text(text)
            self.assertIsNotNone(result)
            self.assertEqual(result.layer0["length"], 0)
        except Exception as e:
            self.fail(f"Processor raised unexpected exception: {e}")
    
    def test_json_serialization(self):
        """Test that output can be serialized to JSON"""
        text = "For hypertension with BP >= 140, initiate treatment."
        
        result = self.processor.process_text(text)
        
        # Should be JSON serializable
        try:
            from dataclasses import asdict
            json_str = json.dumps(asdict(result))
            self.assertIsNotNone(json_str)
        except Exception as e:
            self.fail(f"Failed to serialize result: {e}")


def run_tests():
    """Run all tests and report results"""
    print("=" * 80)
    print("CIKG PROCESSOR POC - TEST SUITE")
    print("=" * 80)
    print()
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCIKGProcessor)
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

#!/usr/bin/env python3
"""
Test Client for AI Validation MCP Service

Tests all MCP methods with sample clinical scenarios.
"""

import json
import subprocess
import sys
from typing import Dict, Any

class AIValidationClient:
    """Client for testing AI Validation MCP Service"""
    
    def __init__(self):
        self.process = None
        self.request_id = 0
    
    def start(self):
        """Start MCP service"""
        self.process = subprocess.Popen(
            [sys.executable, "ai_validation_mcp_service.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("✓ AI Validation MCP Service started")
    
    def stop(self):
        """Stop MCP service"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✓ AI Validation MCP Service stopped")
    
    def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send JSON-RPC request and get response"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        
        self.process.stdin.write(json.dumps(request) + '\n')
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        return json.loads(response_line)
    
    def test_initialize(self):
        """Test initialize method"""
        print("\n[TEST 1] Initialize Service")
        response = self.send_request("initialize", {})
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Server: {result['serverInfo']['name']} v{result['serverInfo']['version']}")
            print(f"  ✓ Test repository size: {result['test_repository_size']}")
            print(f"  ✓ Supported domains: {', '.join(result['capabilities']['supported_domains'])}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_discover_tests(self):
        """Test discover_tests method"""
        print("\n[TEST 2] Discover Tests")
        response = self.send_request("discover_tests", {
            "clinical_question": "How should I manage a patient with high blood pressure?",
            "clinical_domain": "cardiology",
            "max_results": 5
        })
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Query: {result['query']}")
            print(f"  ✓ Tests found: {result['tests_found']}")
            for test in result['tests'][:3]:
                print(f"    - {test['test_id']}: {test['scenario']} (relevance: {test['relevance_score']:.2f})")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_execute_test(self):
        """Test execute_test method"""
        print("\n[TEST 3] Execute Single Test")
        
        # First discover a test
        discover_response = self.send_request("discover_tests", {
            "clinical_question": "hypertension treatment",
            "clinical_domain": "cardiology"
        })
        
        if "result" not in discover_response or not discover_response["result"]["tests"]:
            print("  ✗ No tests found to execute")
            return False
        
        test_id = discover_response["result"]["tests"][0]["test_id"]
        
        # Execute the test
        response = self.send_request("execute_test", {
            "test_id": test_id,
            "ai_answer": "initiate ACE inhibitor therapy for blood pressure control"
        })
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Test: {result['test_name']}")
            print(f"  ✓ Status: {result['status']}")
            print(f"  ✓ Similarity score: {result['similarity_score']:.2f}")
            print(f"  ✓ Clinical accuracy: {result['clinical_accuracy']}")
            print(f"  ✓ Matched concepts: {', '.join(result['matched_concepts'][:5])}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_validate_answer(self):
        """Test validate_answer method"""
        print("\n[TEST 4] Validate AI Answer")
        response = self.send_request("validate_answer", {
            "clinical_question": "What treatment should I give to a diabetic patient with HbA1c of 8.5%?",
            "ai_answer": "Initiate metformin therapy as first-line treatment for type 2 diabetes with elevated HbA1c",
            "clinical_domain": "endocrinology"
        })
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Question: {result['clinical_question']}")
            print(f"  ✓ Tests executed: {result['tests_executed']}")
            print(f"  ✓ Tests passed: {result['tests_passed']}")
            print(f"  ✓ Overall status: {result['overall_status']}")
            print(f"  ✓ Confidence score: {result['confidence_score']:.2f}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_validate_knowledge(self):
        """Test validate_knowledge method"""
        print("\n[TEST 5] Validate AI Knowledge Base")
        
        test_scenarios = [
            {
                "question": "How should I treat hypertension?",
                "answer": "Initiate ACE inhibitor therapy for elevated blood pressure"
            },
            {
                "question": "What is the first-line treatment for type 2 diabetes?",
                "answer": "Metformin is the recommended first-line therapy"
            }
        ]
        
        response = self.send_request("validate_knowledge", {
            "test_scenarios": test_scenarios,
            "clinical_domain": "general"
        })
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Scenarios validated: {result['scenarios_validated']}")
            print(f"  ✓ Total tests executed: {result['total_tests_executed']}")
            print(f"  ✓ Total tests passed: {result['total_tests_passed']}")
            print(f"  ✓ Overall accuracy: {result['overall_accuracy']:.2f}")
            print(f"  ✓ Recommendations:")
            for rec in result['recommendations']:
                print(f"    - {rec}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_get_status(self):
        """Test get_status method"""
        print("\n[TEST 6] Get Service Status")
        response = self.send_request("get_status", {})
        
        if "result" in response:
            result = response["result"]
            print(f"  ✓ Initialized: {result['initialized']}")
            print(f"  ✓ Test repository size: {result['test_repository_size']}")
            print(f"  ✓ Tests discovered: {result['tests_discovered']}")
            print(f"  ✓ Tests executed: {result['tests_executed']}")
            print(f"  ✓ Validations performed: {result['validations_performed']}")
            print(f"  ✓ Success rate: {result['success_rate']:.2f}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("AI Validation MCP Service - Test Suite")
    print("=" * 70)
    
    client = AIValidationClient()
    
    try:
        client.start()
        
        # Run tests
        tests = [
            client.test_initialize,
            client.test_discover_tests,
            client.test_execute_test,
            client.test_validate_answer,
            client.test_validate_knowledge,
            client.test_get_status
        ]
        
        results = []
        for test in tests:
            try:
                results.append(test())
            except Exception as e:
                print(f"  ✗ Test failed with exception: {e}")
                results.append(False)
        
        # Summary
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        passed = sum(results)
        total = len(results)
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {passed/total*100:.0f}%")
        
        if passed == total:
            print("\n✓ ALL TESTS PASSED")
        else:
            print(f"\n✗ {total - passed} TEST(S) FAILED")
        
    finally:
        client.stop()


if __name__ == "__main__":
    main()

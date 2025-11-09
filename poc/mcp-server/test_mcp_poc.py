#!/usr/bin/env python3
"""
Integration tests for MCP Server POC

Tests the MCP server with various scenarios and validates responses.
"""

import unittest
import subprocess
import json
import sys
from pathlib import Path


class TestMCPServer(unittest.TestCase):
    """Test cases for MCP Server POC"""
    
    @classmethod
    def setUpClass(cls):
        """Start MCP server once for all tests"""
        server_path = Path(__file__).parent / "poc_mcp_server.py"
        cls.process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        cls.request_id = 0
        cls.initialized = False
    
    @classmethod
    def tearDownClass(cls):
        """Stop MCP server"""
        if cls.process:
            cls.process.terminate()
            cls.process.wait(timeout=5)
    
    def send_request(self, method, params=None):
        """Send JSON-RPC request and get response"""
        self.__class__.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.__class__.request_id
        }
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        return json.loads(response_line)
    
    def ensure_initialized(self):
        """Ensure server is initialized"""
        if not self.__class__.initialized:
            response = self.send_request("initialize")
            self.__class__.initialized = True
    
    def test_initialize(self):
        """Test server initialization"""
        response = self.send_request("initialize")
        
        self.assertIn("result", response)
        self.assertIn("capabilities", response["result"])
        self.assertIn("serverInfo", response["result"])
    
    def test_configure_coverage_valid(self):
        """Test coverage configuration with valid parameters"""
        self.ensure_initialized()
        
        params = {
            "strategy": "tiered",
            "default_tier": "medium",
            "category_mappings": {"test_category": "high"}
        }
        
        response = self.send_request("configure_coverage", params)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["status"], "configured")
    
    def test_configure_coverage_invalid_strategy(self):
        """Test coverage configuration with invalid strategy"""
        self.ensure_initialized()
        
        params = {
            "strategy": "invalid_strategy",
            "default_tier": "medium"
        }
        
        response = self.send_request("configure_coverage", params)
        
        self.assertIn("error", response)
        self.assertIn("Invalid strategy", response["error"]["message"])
    
    def test_process_scenario_success(self):
        """Test successful scenario processing"""
        self.ensure_initialized()
        
        params = {
            "scenario": {
                "scenario": "Test Scenario",
                "condition": "test condition >= 100",
                "action": "test action",
                "context": "test context"
            }
        }
        
        response = self.send_request("process_scenario", params)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["status"], "success")
        self.assertIn("gherkin", response["result"])
        self.assertIn("metadata", response["result"])
    
    def test_process_scenario_missing_param(self):
        """Test scenario processing with missing parameters"""
        self.ensure_initialized()
        
        params = {}
        
        response = self.send_request("process_scenario", params)
        
        self.assertIn("error", response)
        self.assertIn("Missing scenario", response["error"]["message"])
    
    def test_get_status(self):
        """Test status retrieval"""
        self.ensure_initialized()
        
        response = self.send_request("get_status")
        
        self.assertIn("result", response)
        self.assertIn("initialized", response["result"])
        self.assertIn("active_jobs", response["result"])
        self.assertIn("scenarios_processed", response["result"])
    
    def test_invalid_method(self):
        """Test handling of invalid method"""
        self.ensure_initialized()
        
        response = self.send_request("invalid_method")
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)
    
    def test_json_rpc_version(self):
        """Test JSON-RPC version validation"""
        request = {
            "jsonrpc": "1.0",  # Wrong version
            "method": "get_status",
            "id": 999
        }
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        response = json.loads(response_line)
        
        self.assertIn("error", response)


def run_tests():
    """Run all tests and report results"""
    print("=" * 80)
    print("MCP SERVER POC - INTEGRATION TEST SUITE")
    print("=" * 80)
    print()
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMCPServer)
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

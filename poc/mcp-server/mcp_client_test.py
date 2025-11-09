#!/usr/bin/env python3
"""
MCP Client Test - Simple client for testing MCP Server POC

This client sends JSON-RPC 2.0 requests to the MCP server via stdin/stdout
and displays responses.

Author: GitHub Copilot
Date: 2025-11-09
"""

import json
import subprocess
import sys
from typing import Dict, Any, Optional
from pathlib import Path


class MCPClient:
    """Simple MCP client for testing"""
    
    def __init__(self, server_path: Path):
        self.server_path = server_path
        self.process = None
        self.request_id = 0
    
    def start(self):
        """Start MCP server process"""
        self.process = subprocess.Popen(
            [sys.executable, str(self.server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("✓ MCP Server started")
    
    def stop(self):
        """Stop MCP server process"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✓ MCP Server stopped")
    
    def send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send JSON-RPC 2.0 request and get response"""
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.request_id
        }
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from server")
        
        response = json.loads(response_line)
        return response
    
    def test_initialize(self):
        """Test initialize method"""
        print("\n[TEST] Initialize")
        response = self.send_request("initialize", {})
        
        if "result" in response:
            print("  ✓ Server initialized")
            print(f"  Protocol Version: {response['result'].get('protocolVersion')}")
            print(f"  Server: {response['result']['serverInfo']['name']}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_configure_coverage(self):
        """Test configure_coverage method"""
        print("\n[TEST] Configure Coverage")
        params = {
            "strategy": "tiered",
            "default_tier": "high",
            "category_mappings": {
                "treatment_recommendation": "high",
                "diagnostic_test": "medium"
            }
        }
        
        response = self.send_request("configure_coverage", params)
        
        if "result" in response:
            print("  ✓ Coverage configured")
            print(f"  Strategy: {response['result']['configuration']['strategy']}")
            print(f"  Default Tier: {response['result']['configuration']['default_tier']}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_process_scenario(self):
        """Test process_scenario method"""
        print("\n[TEST] Process Scenario")
        params = {
            "scenario": {
                "scenario": "Hypertension Management",
                "condition": "systolic BP >= 140 mmHg",
                "action": "initiate ACE inhibitor therapy",
                "context": "adult patient, no contraindications"
            }
        }
        
        response = self.send_request("process_scenario", params)
        
        if "result" in response:
            print("  ✓ Scenario processed")
            print(f"  Status: {response['result']['status']}")
            print(f"  Scenarios Generated: {response['result']['metadata']['scenarios_generated']}")
            print(f"  Format: {response['result']['metadata']['format']}")
            print("\n  Generated Gherkin (first 200 chars):")
            gherkin_preview = response['result']['gherkin'][:200]
            print(f"  {gherkin_preview}...")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def test_get_status(self):
        """Test get_status method"""
        print("\n[TEST] Get Status")
        response = self.send_request("get_status", {})
        
        if "result" in response:
            print("  ✓ Status retrieved")
            print(f"  Initialized: {response['result']['initialized']}")
            print(f"  Active Jobs: {response['result']['active_jobs']}")
            print(f"  Scenarios Processed: {response['result']['scenarios_processed']}")
            print(f"  Server Healthy: {response['result']['server_healthy']}")
            return True
        else:
            print(f"  ✗ Error: {response.get('error', {}).get('message')}")
            return False
    
    def run_all_tests(self):
        """Run all test cases"""
        print("=" * 80)
        print("MCP SERVER POC - CLIENT TEST SUITE")
        print("=" * 80)
        
        self.start()
        
        try:
            results = []
            
            # Test sequence
            results.append(("Initialize", self.test_initialize()))
            results.append(("Configure Coverage", self.test_configure_coverage()))
            results.append(("Process Scenario", self.test_process_scenario()))
            results.append(("Get Status", self.test_get_status()))
            
            # Summary
            print("\n" + "=" * 80)
            print("TEST SUMMARY")
            print("=" * 80)
            
            passed = sum(1 for _, result in results if result)
            total = len(results)
            
            for test_name, result in results:
                status = "✓ PASS" if result else "✗ FAIL"
                print(f"  {status}: {test_name}")
            
            print(f"\nTotal: {passed}/{total} tests passed")
            
            if passed == total:
                print("\n✓ ALL TESTS PASSED")
                return 0
            else:
                print("\n✗ SOME TESTS FAILED")
                return 1
            
        finally:
            self.stop()


def main():
    """Main test function"""
    server_path = Path(__file__).parent / "poc_mcp_server.py"
    
    if not server_path.exists():
        print(f"Error: Server not found at {server_path}")
        sys.exit(1)
    
    client = MCPClient(server_path)
    return client.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())

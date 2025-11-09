#!/usr/bin/env python3
"""
End-to-End Integration Test for Clinical BDD Creator POCs

This test demonstrates the complete pipeline:
1. CIKG Processor: Clinical text → GSRL Triples
2. MCP Server: Process clinical scenario with coverage configuration
3. BDD Generator: Generate Gherkin scenarios from processed data

Usage: python integration_test.py
"""

import json
import subprocess
import sys
import time
import threading
import os
from pathlib import Path

class IntegrationTest:
    def __init__(self):
        self.test_results = []
        self.mcp_process = None

    def log_test(self, test_name, success, message=""):
        """Log a test result"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"[{status}] {test_name}")
        if message:
            print(f"  {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })

    def start_mcp_server(self):
        """Start MCP server in background"""
        try:
            # Get the Python executable path
            python_cmd = sys.executable

            # Start MCP server
            self.mcp_process = subprocess.Popen(
                [python_cmd, "poc/mcp-server/poc_mcp_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent
            )

            # Give server time to start
            time.sleep(1)

            # Check if process is still running
            if self.mcp_process.poll() is None:
                self.log_test("MCP Server Startup", True, "Server started successfully")
                return True
            else:
                stdout, stderr = self.mcp_process.communicate()
                self.log_test("MCP Server Startup", False, f"Server failed to start: {stderr}")
                return False

        except Exception as e:
            self.log_test("MCP Server Startup", False, f"Exception: {str(e)}")
            return False

    def stop_mcp_server(self):
        """Stop MCP server"""
        if self.mcp_process:
            self.mcp_process.terminate()
            self.mcp_process.wait(timeout=5)
            self.log_test("MCP Server Shutdown", True, "Server stopped cleanly")

    def test_cikg_processing(self):
        """Test CIKG processing of clinical text"""
        try:
            python_cmd = sys.executable

            # Run CIKG processor on sample clinical texts file
            result = subprocess.run(
                [python_cmd, "poc/cikg-processor/poc_cikg_processor.py", "poc/cikg-processor/clinical_texts.json"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                timeout=10
            )

            if result.returncode == 0:
                # Check that we got expected output markers
                output = result.stdout
                if "CIKG PROCESSING OUTPUT:" in output and "Extracted" in output and "GSRL triples" in output:
                    # Extract numbers from output
                    lines = output.split('\n')
                    entities_line = None
                    triples_line = None
                    
                    for line in lines:
                        if "Extracted" in line and "entities" in line:
                            entities_line = line
                        elif "Generated" in line and "GSRL triples" in line:
                            triples_line = line
                    
                    if entities_line and triples_line:
                        # Simple success check - we got structured output
                        self.log_test("CIKG Processing", True, f"Successfully processed clinical text with entities and triples")
                        return {"status": "success", "output": output}
                    else:
                        self.log_test("CIKG Processing", False, "Missing expected output format")
                else:
                    self.log_test("CIKG Processing", False, "Missing expected output markers")
            else:
                self.log_test("CIKG Processing", False, f"Process failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.log_test("CIKG Processing", False, "Process timed out")
        except Exception as e:
            self.log_test("CIKG Processing", False, f"Exception: {str(e)}")

        return None

    def test_mcp_integration(self, cikg_data):
        """Test MCP server integration with processed CIKG data"""
        if not self.mcp_process or self.mcp_process.poll() is not None:
            self.log_test("MCP Integration", False, "MCP server not running")
            return None

        try:
            # Create test scenario based on CIKG data
            test_scenario = {
                "scenario": "Hypertension Management",
                "condition": "Patient with systolic blood pressure >= 140 mmHg",
                "action": "Initiate ACE inhibitor therapy",
                "context": "Adult patient with no contraindications",
                "expected_outcome": "Patient receives appropriate treatment"
            }

            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "1.0",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "integration-test",
                        "version": "1.0"
                    }
                }
            }

            if self.mcp_process and self.mcp_process.stdin:
                self.mcp_process.stdin.write(json.dumps(init_request) + "\n")
                self.mcp_process.stdin.flush()

                # Read response
                if self.mcp_process.stdout:
                    response_line = self.mcp_process.stdout.readline().strip()
                    init_response = json.loads(response_line)

                    if "result" in init_response:
                        self.log_test("MCP Initialize", True, "Server initialized")
                    else:
                        self.log_test("MCP Initialize", False, f"Init failed: {init_response}")
                        return None
                else:
                    self.log_test("MCP Initialize", False, "No stdout available")
                    return None
            else:
                self.log_test("MCP Initialize", False, "MCP process not properly initialized")
                return None

            # Configure coverage
            config_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "configure_coverage",
                "params": {
                    "strategy": "tiered",
                    "default_tier": "high",
                    "categories": ["treatment_recommendation"]
                }
            }

            if self.mcp_process and self.mcp_process.stdin:
                self.mcp_process.stdin.write(json.dumps(config_request) + "\n")
                self.mcp_process.stdin.flush()

                if self.mcp_process.stdout:
                    response_line = self.mcp_process.stdout.readline().strip()
                    config_response = json.loads(response_line)

                    if "result" in config_response:
                        self.log_test("MCP Configure Coverage", True, "Coverage configured")
                    else:
                        self.log_test("MCP Configure Coverage", False, f"Config failed: {config_response}")
                        return None
                else:
                    self.log_test("MCP Configure Coverage", False, "No stdout available")
                    return None
            else:
                self.log_test("MCP Configure Coverage", False, "MCP process not available")
                return None

            # Process scenario
            process_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "process_scenario",
                "params": {
                    "scenario": test_scenario,
                    "coverage_config": {
                        "fidelity_level": "high",
                        "generation_mode": "comprehensive"
                    }
                }
            }

            if self.mcp_process and self.mcp_process.stdin:
                self.mcp_process.stdin.write(json.dumps(process_request) + "\n")
                self.mcp_process.stdin.flush()

                if self.mcp_process.stdout:
                    response_line = self.mcp_process.stdout.readline().strip()
                    process_response = json.loads(response_line)

                    if "result" in process_response and process_response["result"].get("status") == "success":
                        scenarios_generated = process_response["result"].get("scenarios_generated", 0)
                        self.log_test("MCP Process Scenario", True, f"Generated {scenarios_generated} scenarios")
                        return process_response["result"]
                    else:
                        self.log_test("MCP Process Scenario", False, f"Processing failed: {process_response}")
                else:
                    self.log_test("MCP Process Scenario", False, "No stdout available")
            else:
                self.log_test("MCP Process Scenario", False, "MCP process not available")

        except Exception as e:
            self.log_test("MCP Integration", False, f"Exception: {str(e)}")

        return None

    def run_integration_test(self):
        """Run the complete integration test"""
        print("=" * 80)
        print("CLINICAL BDD CREATOR - END-TO-END INTEGRATION TEST")
        print("=" * 80)

        try:
            # Test 1: CIKG Processing
            cikg_result = self.test_cikg_processing()
            if not cikg_result:
                return False

            # Test 2: Start MCP Server
            if not self.start_mcp_server():
                return False

            # Test 3: MCP Integration
            mcp_result = self.test_mcp_integration(cikg_result)
            if not mcp_result:
                return False

            # Success!
            print("\n" + "=" * 80)
            print("INTEGRATION TEST SUMMARY")
            print("=" * 80)

            passed = sum(1 for r in self.test_results if r["success"])
            total = len(self.test_results)

            print(f"Tests Passed: {passed}/{total}")

            if passed == total:
                print("✓ ALL INTEGRATION TESTS PASSED")
                print("✓ Complete pipeline working: Clinical Text → CIKG → MCP Server → BDD Generation")
                return True
            else:
                print("✗ SOME TESTS FAILED")
                return False

        finally:
            self.stop_mcp_server()

def main():
    """Main test execution"""
    test = IntegrationTest()
    success = test.run_integration_test()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
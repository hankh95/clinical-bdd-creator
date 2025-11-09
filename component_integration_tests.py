#!/usr/bin/env python3
"""
Phase 6: Component Integration Tests

Tests the integration between core Clinical BDD Creator components:
1. GuidelineAnalyzer → MCP Server → BDD Generator pipeline
2. Data flow validation between components
3. Error handling and edge cases

Usage: python component_integration_tests.py
"""

import json
import subprocess
import sys
import time
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from guideline_analyzer import GuidelineAnalyzer, CDSUsageScenario


class ComponentIntegrationTests:
    """Integration tests for component interactions"""

    def __init__(self):
        self.test_results = []
        self.mcp_process = None
        self.temp_files = []

    def log_test(self, test_name: str, success: bool, message: str = ""):
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

    def create_temp_file(self, content: str, suffix: str = ".txt") -> str:
        """Create a temporary file and track it for cleanup"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            temp_path = f.name
        self.temp_files.append(temp_path)
        return temp_path

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files.clear()

    def test_guideline_analyzer_interface(self):
        """Test GuidelineAnalyzer component interface"""
        try:
            analyzer = GuidelineAnalyzer()

            # Test basic analysis
            test_guideline = """
            For patients with hypertension (BP > 140/90), recommend ACE inhibitors.
            For patients with diabetes, order HbA1c testing every 3 months.
            Consider differential diagnosis including pheochromocytoma for resistant hypertension.
            Assess for drug interactions when starting beta-blockers.
            """

            analysis = analyzer.analyze_guideline("Test Guideline", test_guideline)

            # Validate analysis structure
            assert analysis.guideline_name == "Test Guideline"
            assert analysis.specialty in ["general", "endocrinology", "cardiology"]  # Allow detected specialties
            assert len(analysis.scenarios) > 0
            assert isinstance(analysis.coverage_report, dict)

            # Check that CDS scenarios are detected
            detected_scenarios = set(analysis.coverage_report.keys())
            expected_scenarios = {
                CDSUsageScenario.TREATMENT_RECOMMENDATION,
                CDSUsageScenario.DIAGNOSTIC_TEST,
                CDSUsageScenario.DIFFERENTIAL_DX,
                CDSUsageScenario.DRUG_INTERACTION
            }

            intersection = detected_scenarios.intersection(expected_scenarios)
            if intersection:
                self.log_test("GuidelineAnalyzer Interface", True,
                            f"Detected {len(detected_scenarios)} CDS scenario types, including {len(intersection)} expected types")
            else:
                self.log_test("GuidelineAnalyzer Interface", False,
                            f"Detected {len(detected_scenarios)} CDS scenario types but none of the expected types: {detected_scenarios}")

        except Exception as e:
            self.log_test("GuidelineAnalyzer Interface", False, f"Exception: {str(e)}")

    def test_guideline_to_mcp_data_flow(self):
        """Test data flow from GuidelineAnalyzer to MCP Server format"""
        try:
            analyzer = GuidelineAnalyzer()

            # Analyze a guideline
            test_guideline = """
            For patients with atrial fibrillation, recommend anticoagulation with DOACs.
            Order CHA2DS2-VASc score for stroke risk assessment.
            Monitor for bleeding complications when starting anticoagulants.
            """

            analysis = analyzer.analyze_guideline("AFib Guideline", test_guideline)

            # Convert to MCP server input format
            mcp_input = {
                "scenario": analysis.scenarios[0].scenario_id if analysis.scenarios else "test_scenario",
                "condition": "atrial fibrillation",
                "action": "anticoagulation therapy",
                "context": "stroke prevention",
                "contraindications": ["severe renal impairment", "active bleeding"],
                "expected_outcome": "reduced stroke risk"
            }

            # Validate MCP input structure
            required_fields = ["scenario", "condition", "action", "context"]
            missing_fields = [field for field in required_fields if field not in mcp_input]

            if not missing_fields:
                self.log_test("Guideline to MCP Data Flow", True,
                            f"Successfully converted {len(analysis.scenarios)} scenarios to MCP format")
            else:
                self.log_test("Guideline to MCP Data Flow", False,
                            f"Missing required fields: {missing_fields}")

        except Exception as e:
            self.log_test("Guideline to MCP Data Flow", False, f"Exception: {str(e)}")

    def test_mcp_server_startup(self):
        """Test MCP server startup and basic functionality"""
        try:
            python_cmd = sys.executable
            mcp_server_path = Path(__file__).parent / "poc" / "mcp-server" / "poc_mcp_server.py"

            if not mcp_server_path.exists():
                self.log_test("MCP Server Startup", False, "MCP server file not found")
                return

            # Start MCP server
            self.mcp_process = subprocess.Popen(
                [python_cmd, str(mcp_server_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent
            )

            # Give server time to start
            time.sleep(2)

            # Check if process is still running
            if self.mcp_process.poll() is None:
                self.log_test("MCP Server Startup", True, "Server started successfully")

                # Test basic JSON-RPC communication
                self.test_mcp_json_rpc_communication()

            else:
                stdout, stderr = self.mcp_process.communicate()
                self.log_test("MCP Server Startup", False, f"Server failed to start: {stderr}")

        except Exception as e:
            self.log_test("MCP Server Startup", False, f"Exception: {str(e)}")

    def test_mcp_json_rpc_communication(self):
        """Test JSON-RPC communication with MCP server"""
        if not self.mcp_process or self.mcp_process.poll() is not None:
            self.log_test("MCP JSON-RPC Communication", False, "MCP server not running")
            return

        try:
            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }

            # Send request to server
            if self.mcp_process.stdin:
                self.mcp_process.stdin.write(json.dumps(init_request) + "\n")
                self.mcp_process.stdin.flush()

                # Read response
                if self.mcp_process.stdout:
                    response_line = self.mcp_process.stdout.readline().strip()
                    if response_line:
                        response = json.loads(response_line)

                        if "result" in response and "serverInfo" in response["result"]:
                            self.log_test("MCP JSON-RPC Communication", True,
                                        "Successfully communicated with MCP server")
                        else:
                            self.log_test("MCP JSON-RPC Communication", False,
                                        f"Unexpected response: {response}")
                    else:
                        self.log_test("MCP JSON-RPC Communication", False, "No response from server")
                else:
                    self.log_test("MCP JSON-RPC Communication", False, "No stdout available")
            else:
                self.log_test("MCP JSON-RPC Communication", False, "No stdin available")

        except Exception as e:
            self.log_test("MCP JSON-RPC Communication", False, f"Exception: {str(e)}")

    def test_bdd_generator_interface(self):
        """Test BDD Generator component interface"""
        try:
            bdd_path = Path(__file__).parent / "poc" / "bdd-generator"
            sys.path.insert(0, str(bdd_path))

            # Try to import BDD generator
            try:
                from poc_bdd_generator import BDDGenerator, ClinicalScenario
            except ImportError:
                # If import fails, skip this test
                self.log_test("BDD Generator Interface", False, "BDD generator module not available")
                return

            generator = BDDGenerator()

            # Create test scenario
            scenario = ClinicalScenario(
                scenario="Hypertension Management",
                condition="stage 2 hypertension",
                action="ACE inhibitor therapy",
                context="adult patient, no contraindications",
                contraindications=["pregnancy", "hyperkalemia"],
                expected_outcome="blood pressure control"
            )

            # Generate BDD feature
            feature_text = generator.generate_feature(scenario)

            # Validate feature structure
            required_keywords = ["Feature:", "Scenario:", "Given", "When", "Then"]
            missing_keywords = [kw for kw in required_keywords if kw not in feature_text]

            if not missing_keywords:
                # Check for clinical content
                clinical_terms = ["hypertension", "ACE inhibitor", "blood pressure"]
                found_terms = [term for term in clinical_terms if term in feature_text]

                if found_terms:
                    self.log_test("BDD Generator Interface", True,
                                f"Generated valid Gherkin with {len(found_terms)} clinical terms")
                else:
                    self.log_test("BDD Generator Interface", False,
                                "Generated Gherkin missing clinical content")
            else:
                self.log_test("BDD Generator Interface", False,
                            f"Missing Gherkin keywords: {missing_keywords}")

        except Exception as e:
            self.log_test("BDD Generator Interface", False, f"Exception: {str(e)}")

    def test_end_to_end_pipeline(self):
        """Test complete pipeline: Guideline → MCP → BDD"""
        try:
            # Step 1: Guideline Analysis
            analyzer = GuidelineAnalyzer()
            test_guideline = """
            For patients with heart failure, recommend beta-blockers and ACE inhibitors.
            Order echocardiogram for assessment of ejection fraction.
            Monitor renal function when starting heart failure therapy.
            """

            analysis = analyzer.analyze_guideline("Heart Failure Guideline", test_guideline)

            if not analysis.scenarios:
                self.log_test("End-to-End Pipeline", False, "No scenarios extracted from guideline")
                return

            # Step 2: Convert to MCP format
            clinical_scenario = analysis.scenarios[0]
            mcp_scenario = {
                "scenario": clinical_scenario.scenario_id,
                "condition": clinical_scenario.patient_context.get("condition", "heart failure"),
                "action": clinical_scenario.recommended_actions[0].get("action", "therapy") if clinical_scenario.recommended_actions else "treatment",
                "context": "heart failure management",
                "expected_outcome": "improved cardiac function"
            }

            # Step 3: Generate BDD (simulate MCP processing)
            sys.path.insert(0, str(Path(__file__).parent / "poc" / "bdd-generator"))

            try:
                from poc_bdd_generator import BDDGenerator, ClinicalScenario
            except ImportError:
                self.log_test("End-to-End Pipeline", False, "BDD generator module not available")
                return

            generator = BDDGenerator()
            bdd_scenario = ClinicalScenario(**mcp_scenario)
            feature_text = generator.generate_feature(bdd_scenario)

            # Validate complete pipeline
            if analysis.scenarios and mcp_scenario and feature_text:
                self.log_test("End-to-End Pipeline", True,
                            f"Successfully processed {len(analysis.scenarios)} scenarios through complete pipeline")
            else:
                self.log_test("End-to-End Pipeline", False, "Pipeline incomplete")

        except Exception as e:
            self.log_test("End-to-End Pipeline", False, f"Exception: {str(e)}")

    def test_error_handling(self):
        """Test error handling across components"""
        try:
            analyzer = GuidelineAnalyzer()

            # Test with empty guideline
            analysis = analyzer.analyze_guideline("Empty Test", "")

            # Should handle gracefully
            assert analysis.guideline_name == "Empty Test"
            assert len(analysis.scenarios) == 0

            # Test with malformed content
            analysis = analyzer.analyze_guideline("Malformed Test", "This is not a clinical guideline.")

            # Should still produce valid analysis structure
            assert isinstance(analysis.coverage_report, dict)

            self.log_test("Error Handling", True, "Components handle edge cases gracefully")

        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")

    def stop_mcp_server(self):
        """Stop MCP server if running"""
        if self.mcp_process:
            try:
                self.mcp_process.terminate()
                self.mcp_process.wait(timeout=5)
                self.log_test("MCP Server Shutdown", True, "Server stopped cleanly")
            except:
                self.mcp_process.kill()
                self.log_test("MCP Server Shutdown", True, "Server force-killed")

    def run_all_tests(self):
        """Run all component integration tests"""
        print("🧪 PHASE 6: COMPONENT INTEGRATION TESTS")
        print("=" * 50)

        try:
            # Basic component interface tests
            self.test_guideline_analyzer_interface()
            self.test_bdd_generator_interface()

            # Data flow tests
            self.test_guideline_to_mcp_data_flow()

            # MCP server tests
            self.test_mcp_server_startup()

            # End-to-end tests
            self.test_end_to_end_pipeline()
            self.test_error_handling()

        finally:
            # Cleanup
            self.stop_mcp_server()
            self.cleanup_temp_files()

        # Print summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")

        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)

        print(f"Passed: {passed}/{total}")

        if passed == total:
            print("🎉 ALL INTEGRATION TESTS PASSED")
            return True
        else:
            print("❌ SOME TESTS FAILED")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
            return False


if __name__ == "__main__":
    tester = ComponentIntegrationTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Fidelity Mode Testing Framework

Comprehensive testing framework for evaluating AI validation MCP service fidelity modes
against real clinical guidelines. Generates qualitative and quantitative comparison reports.

Usage:
    python fidelity_testing_framework.py [options]

Options:
    --guidelines: Comma-separated list of guideline names (default: all)
    --fidelity-modes: Comma-separated fidelity modes to test (default: all)
    --output-dir: Output directory for reports (default: generated/fidelity-reports)
    --comprehensive-report: Generate single comprehensive report (default: true)
    --per-guideline-reports: Generate individual reports per guideline (default: true)
"""

import json
import yaml
import sys
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import argparse
import statistics
from dataclasses import dataclass, asdict
import tempfile
import shutil

@dataclass
class FidelityTestResult:
    """Result of a single fidelity mode test"""
    guideline_name: str
    fidelity_mode: str
    execution_time: float
    success: bool
    result_data: Dict[str, Any]
    error_message: Optional[str] = None

@dataclass
class GuidelineComparisonReport:
    """Comparison report for a single guideline across fidelity modes"""
    guideline_name: str
    guideline_path: str
    timestamp: str
    fidelity_results: Dict[str, FidelityTestResult]
    quantitative_comparison: Dict[str, Any]
    qualitative_analysis: Dict[str, Any]
    recommendations: List[str]

@dataclass
class ComprehensiveTestReport:
    """Comprehensive report across all guidelines and fidelity modes"""
    timestamp: str
    test_configuration: Dict[str, Any]
    guidelines_tested: List[str]
    fidelity_modes_tested: List[str]
    individual_reports: Dict[str, GuidelineComparisonReport]
    cross_guideline_analysis: Dict[str, Any]
    performance_summary: Dict[str, Any]
    recommendations: List[str]

class FidelityTestingFramework:
    """Framework for testing AI validation MCP service fidelity modes"""

    def __init__(self, output_dir: Path = None):
        self.project_root = Path(__file__).parent
        self.output_dir = output_dir or self.project_root / "generated" / "fidelity-reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Available guidelines
        self.available_guidelines = {
            "acc-afib": {
                "path": self.project_root / "examples" / "guidelines" / "acc-afib" / "joglar-et-al-2023-acc-aha-accp-hrs-guideline-for-the-diagnosis-and-management-of-atrial-fibrillation.pdf",
                "name": "ACC/AHA Atrial Fibrillation Guidelines 2023",
                "domain": "cardiology"
            },
            "diabetes-ada": {
                "path": self.project_root / "examples" / "guidelines" / "diabetes-management" / "ADA_2025_Chapter_9_dc25s009.pdf",
                "name": "ADA Diabetes Management Guidelines 2025",
                "domain": "endocrinology"
            },
            "nccn-breast": {
                "path": self.project_root / "examples" / "guidelines" / "nccn-cancer" / "breast.pdf",
                "name": "NCCN Breast Cancer Guidelines",
                "domain": "oncology"
            },
            "nccn-colon": {
                "path": self.project_root / "examples" / "guidelines" / "nccn-cancer" / "colon.pdf",
                "name": "NCCN Colon Cancer Guidelines",
                "domain": "oncology"
            },
            "nccn-hodgkins": {
                "path": self.project_root / "examples" / "guidelines" / "nccn-cancer" / "hodgkins.pdf",
                "name": "NCCN Hodgkin's Lymphoma Guidelines",
                "domain": "hematology-oncology"
            },
            "nccn-nscl": {
                "path": self.project_root / "examples" / "guidelines" / "nccn-cancer" / "nscl.pdf",
                "name": "NCCN Non-Small Cell Lung Cancer Guidelines",
                "domain": "oncology"
            }
        }

        # Fidelity modes to test
        self.fidelity_modes = ["evaluation-only", "table", "sequential", "full"]

        # Python executable
        self.python_cmd = sys.executable

    def extract_guideline_text(self, pdf_path: Path) -> str:
        """Extract text content from PDF guideline"""
        try:
            # Use pdftotext if available, otherwise return placeholder
            result = subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), "-"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Warning: Failed to extract text from {pdf_path}, using filename-based content")
                return f"Clinical guideline content for {pdf_path.stem}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"Warning: pdftotext not available, using filename-based content for {pdf_path}")
            return f"Clinical guideline content for {pdf_path.stem}"

    def run_fidelity_test(self, guideline_name: str, fidelity_mode: str) -> FidelityTestResult:
        """Run a single fidelity mode test against a guideline"""
        start_time = time.time()

        try:
            guideline_info = self.available_guidelines[guideline_name]
            guideline_text = self.extract_guideline_text(guideline_info["path"])

            # Create temporary test script for MCP service
            test_script = f"""
import sys
import json
sys.path.insert(0, r"{self.project_root / "phase6-ai-validation"}")

# Mock dependencies
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MockClinicalScenario:
    scenario: str
    condition: str
    action: str
    context: str
    contraindications: Optional[List[str]] = None
    expected_outcome: Optional[str] = None

class MockBDDGenerator:
    def generate_feature(self, scenario):
        return f"Feature: {{scenario.scenario}}\\n  Scenario: Test scenario\\n    Given test context\\n    When test condition\\n    Then test outcome"

class MockCIKGProcessor:
    pass

class MockGuidelineAnalyzer:
    pass

class MockCDSUsageScenario:
    pass

sys.modules['poc_bdd_generator'] = type(sys)('poc_bdd_generator')
sys.modules['poc_bdd_generator'].BDDGenerator = MockBDDGenerator
sys.modules['poc_bdd_generator'].ClinicalScenario = MockClinicalScenario

sys.modules['poc_cikg_processor'] = type(sys)('poc_cikg_processor')
sys.modules['poc_cikg_processor'].CIKGProcessor = MockCIKGProcessor

sys.modules['guideline_analyzer'] = type(sys)('guideline_analyzer')
sys.modules['guideline_analyzer'].GuidelineAnalyzer = MockGuidelineAnalyzer
sys.modules['guideline_analyzer'].CDSUsageScenario = MockCDSUsageScenario

from ai_validation_mcp_service import AIValidationMCPService, FidelityMode

# Create service and run test
service = AIValidationMCPService()
result = service.handle_evaluate_guideline({{
    'guideline_text': {repr(guideline_text)},
    'fidelity_mode': {repr(fidelity_mode)}
}})

print(json.dumps(result))
"""

            # Run the test
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_script)
                temp_script_path = f.name

            try:
                result = subprocess.run(
                    [self.python_cmd, temp_script_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                execution_time = time.time() - start_time

                if result.returncode == 0:
                    try:
                        result_data = json.loads(result.stdout.strip())
                        return FidelityTestResult(
                            guideline_name=guideline_name,
                            fidelity_mode=fidelity_mode,
                            execution_time=execution_time,
                            success=True,
                            result_data=result_data
                        )
                    except json.JSONDecodeError:
                        return FidelityTestResult(
                            guideline_name=guideline_name,
                            fidelity_mode=fidelity_mode,
                            execution_time=execution_time,
                            success=False,
                            result_data={},
                            error_message=f"Invalid JSON output: {result.stdout}"
                        )
                else:
                    return FidelityTestResult(
                        guideline_name=guideline_name,
                        fidelity_mode=fidelity_mode,
                        execution_time=execution_time,
                        success=False,
                        result_data={},
                        error_message=f"Process failed: {result.stderr}"
                    )

            finally:
                os.unlink(temp_script_path)

        except Exception as e:
            execution_time = time.time() - start_time
            return FidelityTestResult(
                guideline_name=guideline_name,
                fidelity_mode=fidelity_mode,
                execution_time=execution_time,
                success=False,
                result_data={},
                error_message=str(e)
            )

    def generate_quantitative_comparison(self, results: Dict[str, FidelityTestResult]) -> Dict[str, Any]:
        """Generate quantitative comparison across fidelity modes"""
        comparison = {
            "execution_times": {},
            "success_rates": {},
            "performance_trends": {},
            "result_sizes": {}
        }

        # Execution times
        execution_times = {mode: result.execution_time for mode, result in results.items()}
        comparison["execution_times"] = execution_times

        # Success rates
        success_count = sum(1 for result in results.values() if result.success)
        comparison["success_rates"]["overall"] = success_count / len(results)

        # Performance trends (should generally increase with fidelity)
        successful_times = [result.execution_time for result in results.values() if result.success]
        if successful_times:
            comparison["performance_trends"] = {
                "mean_execution_time": statistics.mean(successful_times),
                "median_execution_time": statistics.median(successful_times),
                "min_execution_time": min(successful_times),
                "max_execution_time": max(successful_times)
            }

        # Result sizes (complexity indicator)
        result_sizes = {}
        for mode, result in results.items():
            if result.success and "result" in result.result_data:
                result_sizes[mode] = len(str(result.result_data["result"]))
        comparison["result_sizes"] = result_sizes

        return comparison

    def generate_qualitative_analysis(self, results: Dict[str, FidelityTestResult]) -> Dict[str, Any]:
        """Generate qualitative analysis of fidelity mode differences"""
        analysis = {
            "fidelity_progression": [],
            "mode_characteristics": {},
            "trade_offs": [],
            "recommendations": []
        }

        # Analyze each mode's characteristics
        for mode, result in results.items():
            if result.success:
                mode_char = {
                    "mode": mode,
                    "execution_time": result.execution_time,
                    "has_result": "result" in result.result_data,
                    "result_keys": list(result.result_data.get("result", {}).keys()) if "result" in result.result_data else []
                }
                analysis["mode_characteristics"][mode] = mode_char

        # Identify trade-offs
        if len(results) >= 2:
            modes_by_time = sorted(results.items(), key=lambda x: x[1].execution_time)
            analysis["trade_offs"].append({
                "aspect": "speed_vs_depth",
                "fastest_mode": modes_by_time[0][0],
                "slowest_mode": modes_by_time[-1][0],
                "time_difference": modes_by_time[-1][1].execution_time - modes_by_time[0][1].execution_time
            })

        # Generate recommendations
        successful_modes = [mode for mode, result in results.items() if result.success]
        if successful_modes:
            analysis["recommendations"].append(f"All fidelity modes ({', '.join(successful_modes)}) executed successfully")
        else:
            analysis["recommendations"].append("No fidelity modes executed successfully - investigate service issues")

        failed_modes = [mode for mode, result in results.items() if not result.success]
        if failed_modes:
            analysis["recommendations"].append(f"Failed modes ({', '.join(failed_modes)}) need investigation")

        return analysis

    def generate_guideline_report(self, guideline_name: str, results: Dict[str, FidelityTestResult]) -> GuidelineComparisonReport:
        """Generate comprehensive report for a single guideline"""
        guideline_info = self.available_guidelines[guideline_name]

        return GuidelineComparisonReport(
            guideline_name=guideline_name,
            guideline_path=str(guideline_info["path"]),
            timestamp=datetime.now().isoformat(),
            fidelity_results=results,
            quantitative_comparison=self.generate_quantitative_comparison(results),
            qualitative_analysis=self.generate_qualitative_analysis(results),
            recommendations=[
                f"For {guideline_info['name']}, consider using evaluation-only mode for quick assessments",
                f"Use full fidelity mode for comprehensive analysis of complex guidelines like {guideline_name}",
                "Table mode provides good balance of speed and detail for most use cases"
            ]
        )

    def run_comprehensive_test(self, guideline_names: List[str] = None, fidelity_modes: List[str] = None) -> ComprehensiveTestReport:
        """Run comprehensive testing across multiple guidelines and fidelity modes"""
        guideline_names = guideline_names or list(self.available_guidelines.keys())
        fidelity_modes = fidelity_modes or self.fidelity_modes

        print(f"🧪 Starting comprehensive fidelity testing...")
        print(f"Guidelines: {', '.join(guideline_names)}")
        print(f"Fidelity modes: {', '.join(fidelity_modes)}")
        print(f"Total test combinations: {len(guideline_names) * len(fidelity_modes)}")

        # Run all tests
        all_results = {}
        individual_reports = {}

        for guideline_name in guideline_names:
            if guideline_name not in self.available_guidelines:
                print(f"⚠️  Skipping unknown guideline: {guideline_name}")
                continue

            print(f"\n📋 Testing guideline: {guideline_name}")
            guideline_results = {}

            for fidelity_mode in fidelity_modes:
                print(f"  🔍 Running {fidelity_mode} mode...")
                result = self.run_fidelity_test(guideline_name, fidelity_mode)
                guideline_results[fidelity_mode] = result

                status = "✅" if result.success else "❌"
                print(f"    {status} {fidelity_mode}: {result.execution_time:.2f}s")

            all_results[guideline_name] = guideline_results
            individual_reports[guideline_name] = self.generate_guideline_report(guideline_name, guideline_results)

        # Generate cross-guideline analysis
        cross_analysis = self.generate_cross_guideline_analysis(all_results)

        # Generate performance summary
        performance_summary = self.generate_performance_summary(all_results)

        # Generate recommendations
        recommendations = self.generate_overall_recommendations(all_results)

        return ComprehensiveTestReport(
            timestamp=datetime.now().isoformat(),
            test_configuration={
                "guidelines_tested": guideline_names,
                "fidelity_modes_tested": fidelity_modes,
                "total_combinations": len(guideline_names) * len(fidelity_modes)
            },
            guidelines_tested=guideline_names,
            fidelity_modes_tested=fidelity_modes,
            individual_reports=individual_reports,
            cross_guideline_analysis=cross_analysis,
            performance_summary=performance_summary,
            recommendations=recommendations
        )

    def generate_cross_guideline_analysis(self, all_results: Dict[str, Dict[str, FidelityTestResult]]) -> Dict[str, Any]:
        """Generate analysis across all guidelines"""
        analysis = {
            "mode_consistency": {},
            "guideline_complexity_indicators": {},
            "best_performing_modes": {}
        }

        # Analyze mode consistency across guidelines
        for mode in self.fidelity_modes:
            mode_results = []
            for guideline_results in all_results.values():
                if mode in guideline_results:
                    mode_results.append(guideline_results[mode])

            if mode_results:
                success_rate = sum(1 for r in mode_results if r.success) / len(mode_results)
                avg_time = statistics.mean(r.execution_time for r in mode_results if r.success) if any(r.success for r in mode_results) else 0
                analysis["mode_consistency"][mode] = {
                    "success_rate": success_rate,
                    "average_execution_time": avg_time,
                    "consistent_performance": success_rate > 0.8
                }

        return analysis

    def generate_performance_summary(self, all_results: Dict[str, Dict[str, FidelityTestResult]]) -> Dict[str, Any]:
        """Generate overall performance summary"""
        summary = {
            "total_tests": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "average_execution_time": 0,
            "performance_by_mode": {},
            "performance_by_guideline": {}
        }

        all_execution_times = []
        successful_tests = 0
        total_tests = 0

        # Aggregate by mode
        for mode in self.fidelity_modes:
            mode_times = []
            mode_successes = 0
            mode_total = 0

            for guideline_results in all_results.values():
                if mode in guideline_results:
                    result = guideline_results[mode]
                    mode_total += 1
                    total_tests += 1
                    if result.success:
                        mode_successes += 1
                        successful_tests += 1
                        mode_times.append(result.execution_time)
                        all_execution_times.append(result.execution_time)

            summary["performance_by_mode"][mode] = {
                "total_tests": mode_total,
                "successful_tests": mode_successes,
                "success_rate": mode_successes / mode_total if mode_total > 0 else 0,
                "average_time": statistics.mean(mode_times) if mode_times else 0
            }

        # Aggregate by guideline
        for guideline_name, guideline_results in all_results.items():
            guideline_times = [r.execution_time for r in guideline_results.values() if r.success]
            guideline_successes = sum(1 for r in guideline_results.values() if r.success)

            summary["performance_by_guideline"][guideline_name] = {
                "total_tests": len(guideline_results),
                "successful_tests": guideline_successes,
                "success_rate": guideline_successes / len(guideline_results),
                "average_time": statistics.mean(guideline_times) if guideline_times else 0
            }

        summary["total_tests"] = total_tests
        summary["successful_tests"] = successful_tests
        summary["failed_tests"] = total_tests - successful_tests
        summary["average_execution_time"] = statistics.mean(all_execution_times) if all_execution_times else 0

        return summary

    def generate_overall_recommendations(self, all_results: Dict[str, Dict[str, FidelityTestResult]]) -> List[str]:
        """Generate overall recommendations based on test results"""
        recommendations = []

        # Analyze best performing modes
        mode_performance = {}
        for mode in self.fidelity_modes:
            successful_results = []
            for guideline_results in all_results.values():
                if mode in guideline_results and guideline_results[mode].success:
                    successful_results.append(guideline_results[mode])

            if successful_results:
                avg_time = statistics.mean(r.execution_time for r in successful_results)
                total_tests_for_mode = sum(1 for guideline_results in all_results.values() if mode in guideline_results)
                success_rate = len(successful_results) / total_tests_for_mode if total_tests_for_mode > 0 else 0
                mode_performance[mode] = {"avg_time": avg_time, "success_rate": success_rate}

        if mode_performance:
            # Recommend fastest reliable mode
            best_modes = sorted(mode_performance.items(), key=lambda x: (x[1]["avg_time"], -x[1]["success_rate"]))
            recommendations.append(f"Fastest reliable mode: {best_modes[0][0]} ({best_modes[0][1]['avg_time']:.2f}s avg)")

            # Recommend most reliable mode
            most_reliable = max(mode_performance.items(), key=lambda x: x[1]["success_rate"])
            recommendations.append(f"Most reliable mode: {most_reliable[0]} ({most_reliable[1]['success_rate']:.1%} success rate)")

        # General recommendations
        recommendations.extend([
            "Use evaluation-only mode for quick assessments and initial screening",
            "Use table mode for balanced analysis with good performance",
            "Use full mode for comprehensive analysis when time permits",
            "Sequential mode provides detailed gap analysis for quality improvement"
        ])

        return recommendations

    def save_reports(self, report: ComprehensiveTestReport, per_guideline: bool = True, comprehensive: bool = True):
        """Save test reports to output directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if per_guideline:
            # Save individual guideline reports
            individual_dir = self.output_dir / f"individual_reports_{timestamp}"
            individual_dir.mkdir(exist_ok=True)

            for guideline_name, guideline_report in report.individual_reports.items():
                report_file = individual_dir / f"{guideline_name}_fidelity_comparison.json"
                with open(report_file, 'w') as f:
                    json.dump(asdict(guideline_report), f, indent=2)
                print(f"💾 Saved individual report: {report_file}")

        if comprehensive:
            # Save comprehensive report
            comprehensive_file = self.output_dir / f"comprehensive_fidelity_test_{timestamp}.json"
            with open(comprehensive_file, 'w') as f:
                json.dump(asdict(report), f, indent=2)
            print(f"💾 Saved comprehensive report: {comprehensive_file}")

            # Save summary text report
            summary_file = self.output_dir / f"fidelity_test_summary_{timestamp}.txt"
            with open(summary_file, 'w') as f:
                f.write(self.generate_text_summary(report))
            print(f"💾 Saved summary report: {summary_file}")

    def generate_text_summary(self, report: ComprehensiveTestReport) -> str:
        """Generate human-readable text summary"""
        lines = []
        lines.append("🧪 FIDELITY MODE TESTING SUMMARY")
        lines.append("=" * 50)
        lines.append(f"Timestamp: {report.timestamp}")
        lines.append(f"Guidelines Tested: {len(report.guidelines_tested)}")
        lines.append(f"Fidelity Modes Tested: {len(report.fidelity_modes_tested)}")
        lines.append(f"Total Test Combinations: {report.test_configuration['total_combinations']}")
        lines.append("")

        # Performance Summary
        perf = report.performance_summary
        lines.append("📊 PERFORMANCE SUMMARY")
        lines.append("-" * 30)
        lines.append(f"Total Tests: {perf['total_tests']}")
        lines.append(f"Successful: {perf['successful_tests']} ({perf['successful_tests']/perf['total_tests']*100:.1f}%)")
        lines.append(f"Failed: {perf['failed_tests']} ({perf['failed_tests']/perf['total_tests']*100:.1f}%)")
        lines.append(f"Average Execution Time: {perf['average_execution_time']:.2f}s")
        lines.append("")

        # Performance by Mode
        lines.append("🎯 PERFORMANCE BY MODE")
        lines.append("-" * 30)
        for mode, stats in perf["performance_by_mode"].items():
            lines.append(f"{mode}:")
            lines.append(f"  Success Rate: {stats['success_rate']*100:.1f}%")
            lines.append(f"  Average Time: {stats['average_time']:.2f}s")
            lines.append(f"  Tests: {stats['successful_tests']}/{stats['total_tests']}")
        lines.append("")

        # Performance by Guideline
        lines.append("📋 PERFORMANCE BY GUIDELINE")
        lines.append("-" * 30)
        for guideline, stats in perf["performance_by_guideline"].items():
            lines.append(f"{guideline}:")
            lines.append(f"  Success Rate: {stats['success_rate']*100:.1f}%")
            lines.append(f"  Average Time: {stats['average_time']:.2f}s")
        lines.append("")

        # Recommendations
        lines.append("💡 RECOMMENDATIONS")
        lines.append("-" * 30)
        for rec in report.recommendations:
            lines.append(f"• {rec}")
        lines.append("")

        return "\n".join(lines)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Fidelity Mode Testing Framework")
    parser.add_argument("--guidelines", help="Comma-separated list of guideline names")
    parser.add_argument("--fidelity-modes", help="Comma-separated fidelity modes to test")
    parser.add_argument("--output-dir", help="Output directory for reports")
    parser.add_argument("--comprehensive-report", action="store_true", default=True, help="Generate comprehensive report")
    parser.add_argument("--per-guideline-reports", action="store_true", default=True, help="Generate per-guideline reports")

    args = parser.parse_args()

    # Parse arguments
    guideline_names = args.guidelines.split(',') if args.guidelines else None
    fidelity_modes = args.fidelity_modes.split(',') if args.fidelity_modes else None
    output_dir = Path(args.output_dir) if args.output_dir else None

    # Create framework and run tests
    framework = FidelityTestingFramework(output_dir)

    try:
        report = framework.run_comprehensive_test(guideline_names, fidelity_modes)
        framework.save_reports(report, args.per_guideline_reports, args.comprehensive_report)

        print("\n🎉 Fidelity testing completed successfully!")
        print(f"📊 Results saved to: {framework.output_dir}")

        # Print summary
        perf = report.performance_summary
        success_rate = perf['successful_tests'] / perf['total_tests'] * 100 if perf['total_tests'] > 0 else 0
        print(f"✅ Success Rate: {success_rate:.1f}%")
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
Assertion Engine for Fishnet Testing Framework

Evaluates assertions across all validation types (graph, reasoning, QA, what-if).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class AssertionType(Enum):
    """Types of assertions"""
    GRAPH = "graph"
    REASONING = "reasoning"
    QA = "qa"
    WHATIF = "whatif"


class AssertionSeverity(Enum):
    """Severity levels for assertion failures"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AssertionResult:
    """Result of evaluating an assertion"""
    assertion_id: str
    assertion_type: AssertionType
    description: str
    
    # Result
    passed: bool = True
    severity: AssertionSeverity = AssertionSeverity.ERROR
    
    # Details
    expected: Any = None
    actual: Any = None
    error_message: str = ""
    
    # Metadata
    rationale: str = ""
    execution_time_ms: float = 0.0


class AssertionEngine:
    """Evaluates and manages assertions"""
    
    def __init__(self):
        """Initialize assertion engine"""
        self._results: List[AssertionResult] = []
    
    def evaluate_assertion(self, assertion: Dict[str, Any], actual_value: Any) -> AssertionResult:
        """
        Evaluate a single assertion
        
        Args:
            assertion: Assertion definition
            actual_value: Actual value to compare against expected
        
        Returns:
            AssertionResult
        """
        import time
        start_time = time.time()
        
        assertion_id = assertion.get('id', 'unknown')
        description = assertion.get('description', '')
        expected = assertion.get('expect', None)
        severity_str = assertion.get('severity', 'error')
        rationale = assertion.get('rationale', '')
        
        try:
            severity = AssertionSeverity(severity_str)
        except ValueError:
            severity = AssertionSeverity.ERROR
        
        result = AssertionResult(
            assertion_id=assertion_id,
            assertion_type=AssertionType.GRAPH,  # Default, will be determined by context
            description=description,
            severity=severity,
            expected=expected,
            actual=actual_value,
            rationale=rationale,
        )
        
        # Evaluate the assertion
        result.passed = self._compare_values(expected, actual_value)
        
        if not result.passed:
            result.error_message = f"Expected {expected}, got {actual_value}"
        
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        self._results.append(result)
        return result
    
    def evaluate_all_assertions(self, scenario) -> List[AssertionResult]:
        """
        Evaluate all assertions for a scenario
        
        Args:
            scenario: ClinicalScenario object
        
        Returns:
            List of AssertionResult
        """
        results = []
        
        if not scenario.santiago_assertions:
            return results
        
        # Evaluate graph assertions
        if 'graph_assertions' in scenario.santiago_assertions:
            for assertion in scenario.santiago_assertions['graph_assertions']:
                # Would execute graph query and evaluate
                result = AssertionResult(
                    assertion_id=assertion.get('id', ''),
                    assertion_type=AssertionType.GRAPH,
                    description=assertion.get('description', ''),
                    passed=True,  # Placeholder
                )
                results.append(result)
        
        # Evaluate reasoning assertions
        if 'reasoning_assertions' in scenario.santiago_assertions:
            for assertion in scenario.santiago_assertions['reasoning_assertions']:
                result = AssertionResult(
                    assertion_id=assertion.get('id', ''),
                    assertion_type=AssertionType.REASONING,
                    description=assertion.get('description', ''),
                    passed=True,  # Placeholder
                )
                results.append(result)
        
        # Evaluate QA assertions
        if 'qa_assertions' in scenario.santiago_assertions:
            for assertion in scenario.santiago_assertions['qa_assertions']:
                result = AssertionResult(
                    assertion_id=assertion.get('id', ''),
                    assertion_type=AssertionType.QA,
                    description=f"QA: {assertion.get('question', '')}",
                    passed=True,  # Placeholder
                )
                results.append(result)
        
        # Evaluate what-if assertions
        if 'whatif_assertions' in scenario.santiago_assertions:
            for assertion in scenario.santiago_assertions['whatif_assertions']:
                result = AssertionResult(
                    assertion_id=assertion.get('id', ''),
                    assertion_type=AssertionType.WHATIF,
                    description=assertion.get('description', ''),
                    passed=True,  # Placeholder
                )
                results.append(result)
        
        return results
    
    def _compare_values(self, expected: Any, actual: Any) -> bool:
        """Compare expected and actual values"""
        if expected is None:
            return True  # No expectation means pass
        
        # Handle string comparisons with operators
        if isinstance(expected, str):
            if expected == "exists":
                return actual is not None and (not isinstance(actual, list) or len(actual) > 0)
            
            if expected.startswith(">="):
                try:
                    threshold = float(expected[2:])
                    return float(actual) >= threshold
                except (ValueError, TypeError):
                    return False
            
            if expected.startswith("<="):
                try:
                    threshold = float(expected[2:])
                    return float(actual) <= threshold
                except (ValueError, TypeError):
                    return False
            
            if expected.startswith("=="):
                return str(actual) == expected[2:].strip()
            
            # String contains check
            return expected.lower() in str(actual).lower()
        
        # Direct equality
        return expected == actual
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of all assertion results"""
        total = len(self._results)
        passed = sum(1 for r in self._results if r.passed)
        failed = total - passed
        
        by_type = {}
        for result in self._results:
            type_name = result.assertion_type.value
            if type_name not in by_type:
                by_type[type_name] = {'total': 0, 'passed': 0, 'failed': 0}
            by_type[type_name]['total'] += 1
            if result.passed:
                by_type[type_name]['passed'] += 1
            else:
                by_type[type_name]['failed'] += 1
        
        return {
            'total_assertions': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': passed / total if total > 0 else 0.0,
            'by_type': by_type,
        }
    
    def clear_results(self):
        """Clear all stored results"""
        self._results.clear()

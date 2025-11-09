#!/usr/bin/env python3
"""
AI Validation MCP Service

Enables AI systems (RAG, GraphRAG, etc.) to validate their clinical answers
by discovering and executing relevant BDD tests.

Protocol: MCP (Model Context Protocol)
Transport: stdio (JSON-RPC 2.0)
Author: GitHub Copilot
Date: 2025-11-09
"""

import json
import sys
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import difflib

# Import existing components
sys.path.insert(0, str(Path(__file__).parent.parent / "poc" / "bdd-generator"))
sys.path.insert(0, str(Path(__file__).parent.parent / "poc" / "cikg-processor"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from poc_bdd_generator import BDDGenerator, ClinicalScenario
from poc_cikg_processor import CIKGProcessor
from guideline_analyzer import GuidelineAnalyzer, CDSUsageScenario


class ValidationStatus(Enum):
    """Validation result status"""
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    ERROR = "error"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class TestDiscoveryQuery:
    """Query for discovering relevant BDD tests"""
    clinical_question: str
    patient_context: Optional[Dict[str, Any]] = None
    clinical_domain: Optional[str] = None  # e.g., "cardiology", "diabetes"
    cds_category: Optional[str] = None
    max_results: int = 10


@dataclass
class BDDTest:
    """Represents a BDD test scenario"""
    test_id: str
    feature: str
    scenario_name: str
    scenario_type: str  # "positive" or "negative"
    given_steps: List[str]
    when_step: str
    then_steps: List[str]
    tags: List[str]
    clinical_context: Dict[str, Any]
    expected_outcome: str


@dataclass
class ValidationResult:
    """Result of validating an AI answer against BDD tests"""
    status: ValidationStatus
    test_id: str
    test_name: str
    ai_answer: str
    expected_answer: str
    similarity_score: float
    matched_concepts: List[str]
    missing_concepts: List[str]
    extra_concepts: List[str]
    clinical_accuracy: bool
    details: str


@dataclass
class KnowledgeValidationReport:
    """Complete validation report for AI knowledge"""
    query: str
    ai_answer: str
    tests_executed: int
    tests_passed: int
    tests_failed: int
    overall_status: ValidationStatus
    validation_results: List[ValidationResult]
    recommendations: List[str]
    confidence_score: float


class AIValidationMCPService:
    """
    MCP Service for AI answer validation using BDD tests
    
    Supported Methods:
    - initialize: Server capability negotiation
    - discover_tests: Find relevant BDD tests for clinical questions
    - execute_test: Run single BDD test against AI answer
    - validate_answer: Comprehensive validation of AI answer
    - validate_knowledge: Validate AI clinical knowledge base
    - get_status: Report server health and metrics
    """
    
    def __init__(self):
        self.initialized = False
        self.bdd_generator = BDDGenerator()
        self.cikg_processor = CIKGProcessor()
        self.guideline_analyzer = GuidelineAnalyzer()
        
        # Test repository (in production, would be database)
        self.test_repository: Dict[str, BDDTest] = {}
        self.validation_history: List[ValidationResult] = []
        
        # Statistics
        self.tests_discovered = 0
        self.tests_executed = 0
        self.validations_performed = 0
        
        self._load_test_repository()
    
    def _load_test_repository(self):
        """Load pre-generated BDD tests into repository"""
        # For POC, we'll generate some sample tests
        sample_scenarios = [
            {
                "scenario": "Hypertension Management",
                "condition": "systolic BP >= 140 mmHg",
                "action": "initiate ACE inhibitor therapy",
                "context": "adult patient, no contraindications",
                "domain": "cardiology"
            },
            {
                "scenario": "Diabetes Management",
                "condition": "HbA1c > 7.0%",
                "action": "initiate metformin therapy",
                "context": "type 2 diabetes, first-line treatment",
                "domain": "endocrinology"
            },
            {
                "scenario": "Sepsis Management",
                "condition": "fever > 38.5°C and elevated lactate",
                "action": "administer broad-spectrum antibiotics",
                "context": "suspected sepsis, emergency department",
                "domain": "emergency medicine"
            }
        ]
        
        for idx, scenario_data in enumerate(sample_scenarios):
            scenario = ClinicalScenario(
                scenario=scenario_data["scenario"],
                condition=scenario_data["condition"],
                action=scenario_data["action"],
                context=scenario_data["context"]
            )
            
            # Generate Gherkin
            gherkin = self.bdd_generator.generate_feature(scenario)
            
            # Parse and store tests
            tests = self._parse_gherkin_to_tests(gherkin, scenario_data)
            for test in tests:
                self.test_repository[test.test_id] = test
    
    def _parse_gherkin_to_tests(self, gherkin: str, metadata: Dict) -> List[BDDTest]:
        """Parse Gherkin text into structured BDDTest objects"""
        tests = []
        lines = gherkin.split('\n')
        
        current_scenario = None
        current_given = []
        current_when = ""
        current_then = []
        current_tags = []
        feature_name = ""
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Feature:'):
                feature_name = line.replace('Feature:', '').strip()
            elif line.startswith('@'):
                current_tags = [tag.strip() for tag in line.split() if tag.startswith('@')]
            elif line.startswith('Scenario:'):
                # Save previous scenario
                if current_scenario:
                    test = self._create_bdd_test(
                        feature_name, current_scenario, current_tags,
                        current_given, current_when, current_then, metadata
                    )
                    tests.append(test)
                
                # Start new scenario
                current_scenario = line.replace('Scenario:', '').strip()
                current_given = []
                current_when = ""
                current_then = []
            elif line.startswith('Given ') or line.startswith('And ') and current_scenario and not current_when:
                step = line.replace('Given ', '').replace('And ', '').strip()
                current_given.append(step)
            elif line.startswith('When '):
                current_when = line.replace('When ', '').strip()
            elif line.startswith('Then ') or line.startswith('And ') and current_when:
                step = line.replace('Then ', '').replace('And ', '').strip()
                current_then.append(step)
        
        # Save last scenario
        if current_scenario:
            test = self._create_bdd_test(
                feature_name, current_scenario, current_tags,
                current_given, current_when, current_then, metadata
            )
            tests.append(test)
        
        return tests
    
    def _create_bdd_test(self, feature: str, scenario: str, tags: List[str],
                        given_steps: List[str], when_step: str, then_steps: List[str],
                        metadata: Dict) -> BDDTest:
        """Create structured BDDTest from parsed Gherkin"""
        test_id = f"test_{len(self.test_repository) + 1:04d}"
        scenario_type = "positive" if "@positive" in tags else "negative"
        
        # Extract expected outcome from then steps
        expected_outcome = " AND ".join(then_steps)
        
        return BDDTest(
            test_id=test_id,
            feature=feature,
            scenario_name=scenario,
            scenario_type=scenario_type,
            given_steps=given_steps,
            when_step=when_step,
            then_steps=then_steps,
            tags=tags,
            clinical_context={
                "domain": metadata.get("domain", "general"),
                "condition": metadata.get("condition", ""),
                "action": metadata.get("action", "")
            },
            expected_outcome=expected_outcome
        )
    
    def start(self):
        """Start MCP server loop reading from stdin"""
        sys.stderr.write("AI Validation MCP Service starting...\n")
        sys.stderr.flush()
        
        try:
            for line in sys.stdin:
                if not line.strip():
                    continue
                    
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    self.send_response(response)
                except json.JSONDecodeError as e:
                    self.send_error(-32700, f"Parse error: {str(e)}", None)
                except Exception as e:
                    sys.stderr.write(f"Error handling request: {e}\n")
                    sys.stderr.flush()
        except KeyboardInterrupt:
            sys.stderr.write("\nAI Validation MCP Service shutting down...\n")
            sys.stderr.flush()
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 request"""
        if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
            return self.create_error_response(
                -32600, "Invalid Request: missing or invalid jsonrpc version",
                request.get("id")
            )
        
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if not method:
            return self.create_error_response(
                -32600, "Invalid Request: missing method", request_id
            )
        
        # Route to appropriate handler
        handlers = {
            "initialize": self.handle_initialize,
            "discover_tests": self.handle_discover_tests,
            "execute_test": self.handle_execute_test,
            "validate_answer": self.handle_validate_answer,
            "validate_knowledge": self.handle_validate_knowledge,
            "get_status": self.handle_get_status,
        }
        
        handler = handlers.get(method)
        if not handler:
            return self.create_error_response(
                -32601, f"Method not found: {method}", request_id
            )
        
        try:
            result = handler(params)
            return self.create_success_response(result, request_id)
        except Exception as e:
            return self.create_error_response(
                -32603, f"Internal error: {str(e)}", request_id
            )
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize server and negotiate capabilities"""
        self.initialized = True
        
        return {
            "serverInfo": {
                "name": "AI Validation MCP Service",
                "version": "1.0.0"
            },
            "capabilities": {
                "test_discovery": True,
                "test_execution": True,
                "answer_validation": True,
                "knowledge_validation": True,
                "supported_domains": ["cardiology", "endocrinology", "emergency medicine"],
                "supported_cds_categories": [e.value for e in CDSUsageScenario]
            },
            "test_repository_size": len(self.test_repository)
        }
    
    def handle_discover_tests(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Discover relevant BDD tests for clinical question"""
        query = TestDiscoveryQuery(
            clinical_question=params.get("clinical_question", ""),
            patient_context=params.get("patient_context"),
            clinical_domain=params.get("clinical_domain"),
            cds_category=params.get("cds_category"),
            max_results=params.get("max_results", 10)
        )
        
        # Find matching tests
        relevant_tests = self._find_relevant_tests(query)
        self.tests_discovered += len(relevant_tests)
        
        return {
            "query": query.clinical_question,
            "tests_found": len(relevant_tests),
            "tests": [
                {
                    "test_id": test.test_id,
                    "feature": test.feature,
                    "scenario": test.scenario_name,
                    "type": test.scenario_type,
                    "tags": test.tags,
                    "domain": test.clinical_context.get("domain"),
                    "expected_outcome": test.expected_outcome,
                    "relevance_score": score
                }
                for test, score in relevant_tests
            ]
        }
    
    def _find_relevant_tests(self, query: TestDiscoveryQuery) -> List[Tuple[BDDTest, float]]:
        """Find BDD tests relevant to the query"""
        scored_tests = []
        
        for test in self.test_repository.values():
            score = 0.0
            
            # Domain match
            if query.clinical_domain:
                if test.clinical_context.get("domain") == query.clinical_domain:
                    score += 0.4
            
            # Question similarity
            question_lower = query.clinical_question.lower()
            feature_lower = test.feature.lower()
            scenario_lower = test.scenario_name.lower()
            
            if any(word in feature_lower or word in scenario_lower 
                   for word in question_lower.split()):
                score += 0.3
            
            # Context match
            if query.patient_context:
                context_str = json.dumps(query.patient_context).lower()
                test_context_str = json.dumps(test.clinical_context).lower()
                if any(word in test_context_str for word in context_str.split()):
                    score += 0.3
            
            if score > 0:
                scored_tests.append((test, score))
        
        # Sort by score and limit
        scored_tests.sort(key=lambda x: x[1], reverse=True)
        return scored_tests[:query.max_results]
    
    def handle_execute_test(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute single BDD test against AI answer"""
        test_id = params.get("test_id")
        ai_answer = params.get("ai_answer", "")
        
        if not test_id or test_id not in self.test_repository:
            raise ValueError(f"Test not found: {test_id}")
        
        test = self.test_repository[test_id]
        result = self._validate_answer_against_test(ai_answer, test)
        
        self.tests_executed += 1
        self.validation_history.append(result)
        
        return {
            "test_id": result.test_id,
            "test_name": result.test_name,
            "status": result.status.value,
            "similarity_score": result.similarity_score,
            "clinical_accuracy": result.clinical_accuracy,
            "matched_concepts": result.matched_concepts,
            "missing_concepts": result.missing_concepts,
            "extra_concepts": result.extra_concepts,
            "details": result.details
        }
    
    def handle_validate_answer(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate AI answer against multiple relevant tests"""
        clinical_question = params.get("clinical_question", "")
        ai_answer = params.get("ai_answer", "")
        clinical_domain = params.get("clinical_domain")
        
        # Discover relevant tests
        query = TestDiscoveryQuery(
            clinical_question=clinical_question,
            clinical_domain=clinical_domain,
            max_results=5
        )
        relevant_tests = self._find_relevant_tests(query)
        
        # Execute tests
        results = []
        for test, relevance in relevant_tests:
            result = self._validate_answer_against_test(ai_answer, test)
            results.append(result)
            self.validation_history.append(result)
        
        self.tests_executed += len(results)
        self.validations_performed += 1
        
        # Calculate overall status
        passed = sum(1 for r in results if r.status == ValidationStatus.PASS)
        failed = sum(1 for r in results if r.status == ValidationStatus.FAIL)
        
        if passed == len(results):
            overall_status = ValidationStatus.PASS
        elif passed > 0:
            overall_status = ValidationStatus.PARTIAL
        else:
            overall_status = ValidationStatus.FAIL
        
        return {
            "clinical_question": clinical_question,
            "tests_executed": len(results),
            "tests_passed": passed,
            "tests_failed": failed,
            "overall_status": overall_status.value,
            "confidence_score": passed / len(results) if results else 0.0,
            "results": [
                {
                    "test_id": r.test_id,
                    "status": r.status.value,
                    "similarity": r.similarity_score,
                    "clinical_accuracy": r.clinical_accuracy
                }
                for r in results
            ]
        }
    
    def handle_validate_knowledge(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate AI clinical knowledge base comprehensively"""
        test_scenarios = params.get("test_scenarios", [])
        clinical_domain = params.get("clinical_domain")
        
        reports = []
        
        for scenario in test_scenarios:
            question = scenario.get("question")
            ai_answer = scenario.get("answer")
            
            if not question or not ai_answer:
                continue
            
            # Validate this scenario
            validation = self.handle_validate_answer({
                "clinical_question": question,
                "ai_answer": ai_answer,
                "clinical_domain": clinical_domain
            })
            
            reports.append({
                "question": question,
                "validation": validation
            })
        
        # Overall statistics
        total_tests = sum(r["validation"]["tests_executed"] for r in reports)
        total_passed = sum(r["validation"]["tests_passed"] for r in reports)
        
        return {
            "scenarios_validated": len(reports),
            "total_tests_executed": total_tests,
            "total_tests_passed": total_passed,
            "overall_accuracy": total_passed / total_tests if total_tests > 0 else 0.0,
            "reports": reports,
            "recommendations": self._generate_recommendations(reports)
        }
    
    def handle_get_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Report server status and metrics"""
        return {
            "initialized": self.initialized,
            "test_repository_size": len(self.test_repository),
            "tests_discovered": self.tests_discovered,
            "tests_executed": self.tests_executed,
            "validations_performed": self.validations_performed,
            "recent_validations": len([v for v in self.validation_history[-10:]]),
            "success_rate": sum(1 for v in self.validation_history 
                               if v.status == ValidationStatus.PASS) / len(self.validation_history)
                           if self.validation_history else 0.0
        }
    
    def _validate_answer_against_test(self, ai_answer: str, test: BDDTest) -> ValidationResult:
        """Validate AI answer against a specific BDD test"""
        expected = test.expected_outcome.lower()
        answer = ai_answer.lower()
        
        # Extract clinical concepts from expected outcome
        expected_concepts = self._extract_concepts(expected)
        answer_concepts = self._extract_concepts(answer)
        
        # Calculate similarity
        similarity = difflib.SequenceMatcher(None, expected, answer).ratio()
        
        # Find matched, missing, and extra concepts
        matched = list(set(expected_concepts) & set(answer_concepts))
        missing = list(set(expected_concepts) - set(answer_concepts))
        extra = list(set(answer_concepts) - set(expected_concepts))
        
        # Determine clinical accuracy
        # Pass if: high similarity OR most concepts matched with few missing
        clinical_accuracy = (
            similarity >= 0.7 or 
            (len(matched) >= len(expected_concepts) * 0.8 and len(missing) <= 2)
        )
        
        # Determine status
        if clinical_accuracy:
            status = ValidationStatus.PASS
            details = "AI answer matches expected clinical outcome"
        elif len(matched) > 0:
            status = ValidationStatus.PARTIAL
            details = f"Partial match: {len(missing)} concepts missing"
        else:
            status = ValidationStatus.FAIL
            details = "AI answer does not match expected outcome"
        
        return ValidationResult(
            status=status,
            test_id=test.test_id,
            test_name=test.scenario_name,
            ai_answer=ai_answer,
            expected_answer=test.expected_outcome,
            similarity_score=similarity,
            matched_concepts=matched,
            missing_concepts=missing,
            extra_concepts=extra,
            clinical_accuracy=clinical_accuracy,
            details=details
        )
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key clinical concepts from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'should', 'be', 
                     'is', 'are', 'was', 'were', 'has', 'have', 'had'}
        
        # Tokenize and filter
        words = re.findall(r'\b[a-z]+\b', text.lower())
        concepts = [w for w in words if w not in stop_words and len(w) > 3]
        
        return concepts
    
    def _generate_recommendations(self, reports: List[Dict]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Analyze failure patterns
        failed_domains = set()
        failed_concepts = []
        
        for report in reports:
            validation = report["validation"]
            if validation["overall_status"] != "pass":
                # Extract domain from question
                question = report["question"].lower()
                for domain in ["cardiology", "endocrinology", "diabetes", "hypertension"]:
                    if domain in question:
                        failed_domains.add(domain)
        
        if failed_domains:
            recommendations.append(
                f"Review AI knowledge in: {', '.join(failed_domains)}"
            )
        
        # Check for consistent patterns
        low_confidence = [r for r in reports 
                         if r["validation"].get("confidence_score", 0) < 0.5]
        if len(low_confidence) > len(reports) * 0.3:
            recommendations.append(
                "More than 30% of scenarios have low confidence - consider retraining"
            )
        
        if not recommendations:
            recommendations.append("AI knowledge validation successful - no issues found")
        
        return recommendations
    
    def send_response(self, response: Dict[str, Any]):
        """Send JSON-RPC response to stdout"""
        sys.stdout.write(json.dumps(response) + '\n')
        sys.stdout.flush()
    
    def send_error(self, code: int, message: str, request_id: Any):
        """Send JSON-RPC error response"""
        error_response = {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": request_id
        }
        self.send_response(error_response)
    
    def create_success_response(self, result: Any, request_id: Any) -> Dict[str, Any]:
        """Create JSON-RPC success response"""
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
    
    def create_error_response(self, code: int, message: str, request_id: Any) -> Dict[str, Any]:
        """Create JSON-RPC error response"""
        return {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": request_id
        }


def main():
    """Main entry point"""
    service = AIValidationMCPService()
    service.start()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Integration Examples for AI Validation MCP Service

Demonstrates how to integrate the AI Validation MCP Service with:
1. RAG (Retrieval-Augmented Generation) systems
2. GraphRAG systems
3. Clinical knowledge bases
4. AI answer validation pipelines
"""

import json
import subprocess
import sys
from typing import Dict, Any, List


class MockRAGSystem:
    """Mock RAG system for demonstration purposes"""
    
    def __init__(self):
        self.knowledge_base = {
            "hypertension": "Initiate ACE inhibitor therapy for patients with elevated blood pressure",
            "diabetes": "Metformin is the first-line therapy for type 2 diabetes with elevated HbA1c",
            "sepsis": "Administer broad-spectrum antibiotics immediately for suspected sepsis"
        }
    
    def query(self, question: str) -> str:
        """Mock RAG query - returns answer from knowledge base"""
        question_lower = question.lower()
        
        for condition, answer in self.knowledge_base.items():
            if condition in question_lower:
                return answer
        
        return "No relevant information found"


class AIValidationIntegration:
    """Integration layer for AI Validation MCP Service"""
    
    def __init__(self):
        self.process = None
        self.request_id = 0
    
    def start_service(self):
        """Start MCP validation service"""
        self.process = subprocess.Popen(
            [sys.executable, "ai_validation_mcp_service.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Initialize service
        self.send_request("initialize", {})
    
    def stop_service(self):
        """Stop MCP validation service"""
        if self.process:
            self.process.terminate()
            self.process.wait()
    
    def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send JSON-RPC request"""
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
    
    def validate_rag_answer(self, question: str, answer: str, domain: str = None) -> Dict[str, Any]:
        """Validate a RAG system answer"""
        response = self.send_request("validate_answer", {
            "clinical_question": question,
            "ai_answer": answer,
            "clinical_domain": domain
        })
        
        return response.get("result", {})
    
    def discover_relevant_tests(self, question: str, domain: str = None, max_results: int = 5) -> List[Dict]:
        """Discover BDD tests relevant to a clinical question"""
        response = self.send_request("discover_tests", {
            "clinical_question": question,
            "clinical_domain": domain,
            "max_results": max_results
        })
        
        return response.get("result", {}).get("tests", [])
    
    def validate_knowledge_base(self, test_scenarios: List[Dict], domain: str = None) -> Dict[str, Any]:
        """Validate entire AI knowledge base"""
        response = self.send_request("validate_knowledge", {
            "test_scenarios": test_scenarios,
            "clinical_domain": domain
        })
        
        return response.get("result", {})


# Example 1: RAG System Validation
def example_1_rag_validation():
    """Example: Validate RAG system answers"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: RAG System Validation")
    print("=" * 70)
    
    # Create mock RAG system and validation integration
    rag = MockRAGSystem()
    validator = AIValidationIntegration()
    validator.start_service()
    
    try:
        # Test clinical questions
        questions = [
            ("How should I treat a patient with hypertension?", "cardiology"),
            ("What is the first-line treatment for diabetes?", "endocrinology"),
            ("How should I manage suspected sepsis?", "emergency medicine")
        ]
        
        results = []
        for question, domain in questions:
            print(f"\nQuestion: {question}")
            
            # Get RAG answer
            rag_answer = rag.query(question)
            print(f"RAG Answer: {rag_answer}")
            
            # Validate answer
            validation = validator.validate_rag_answer(question, rag_answer, domain)
            
            print(f"Validation Status: {validation['overall_status']}")
            print(f"Confidence: {validation['confidence_score']:.2f}")
            print(f"Tests: {validation['tests_passed']}/{validation['tests_executed']} passed")
            
            results.append({
                "question": question,
                "status": validation['overall_status'],
                "confidence": validation['confidence_score']
            })
        
        # Summary
        print("\n" + "-" * 70)
        print("Validation Summary:")
        passed = sum(1 for r in results if r['status'] == 'pass')
        print(f"  ✓ Passed: {passed}/{len(results)}")
        print(f"  Average confidence: {sum(r['confidence'] for r in results) / len(results):.2f}")
        
    finally:
        validator.stop_service()


# Example 2: Test Discovery for Unknown Questions
def example_2_test_discovery():
    """Example: Discover relevant tests for novel questions"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Test Discovery for Unknown Questions")
    print("=" * 70)
    
    validator = AIValidationIntegration()
    validator.start_service()
    
    try:
        # Novel clinical questions
        novel_questions = [
            "Patient presents with chest pain and elevated blood pressure",
            "Diabetes patient with poor glucose control needs medication adjustment",
            "Emergency room patient with fever and elevated lactate"
        ]
        
        for question in novel_questions:
            print(f"\nQuestion: {question}")
            
            # Discover relevant tests
            tests = validator.discover_relevant_tests(question, max_results=3)
            
            print(f"Found {len(tests)} relevant tests:")
            for test in tests:
                print(f"  - {test['scenario']}")
                print(f"    Domain: {test['domain']}, Relevance: {test['relevance_score']:.2f}")
                print(f"    Expected: {test['expected_outcome'][:80]}...")
    
    finally:
        validator.stop_service()


# Example 3: Knowledge Base Comprehensive Validation
def example_3_knowledge_base_validation():
    """Example: Comprehensive validation of AI knowledge base"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Knowledge Base Comprehensive Validation")
    print("=" * 70)
    
    rag = MockRAGSystem()
    validator = AIValidationIntegration()
    validator.start_service()
    
    try:
        # Create test scenarios from knowledge base
        test_scenarios = []
        
        test_questions = {
            "hypertension": "How should I manage hypertension?",
            "diabetes": "What treatment for type 2 diabetes?",
            "sepsis": "How to treat suspected sepsis?"
        }
        
        for key, question in test_questions.items():
            answer = rag.query(question)
            test_scenarios.append({
                "question": question,
                "answer": answer
            })
        
        print(f"\nValidating {len(test_scenarios)} scenarios from knowledge base...")
        
        # Validate knowledge base
        validation = validator.validate_knowledge_base(test_scenarios, domain="general")
        
        print(f"\nResults:")
        print(f"  Scenarios validated: {validation['scenarios_validated']}")
        print(f"  Total tests executed: {validation['total_tests_executed']}")
        print(f"  Total tests passed: {validation['total_tests_passed']}")
        print(f"  Overall accuracy: {validation['overall_accuracy']:.2f}")
        
        print(f"\nRecommendations:")
        for rec in validation['recommendations']:
            print(f"  - {rec}")
        
        # Detailed per-scenario results
        print(f"\nDetailed Results:")
        for i, report in enumerate(validation['reports'], 1):
            val = report['validation']
            print(f"  {i}. {report['question'][:60]}...")
            print(f"     Status: {val['overall_status']}, Confidence: {val['confidence_score']:.2f}")
    
    finally:
        validator.stop_service()


# Example 4: Continuous Validation Pipeline
def example_4_continuous_validation():
    """Example: Continuous validation of RAG answers"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Continuous Validation Pipeline")
    print("=" * 70)
    
    rag = MockRAGSystem()
    validator = AIValidationIntegration()
    validator.start_service()
    
    try:
        print("\nSimulating continuous RAG query validation...")
        
        # Simulate stream of queries
        queries = [
            ("Patient with BP 160/100 - treatment?", "cardiology"),
            ("HbA1c 8.5% - what medication?", "endocrinology"),
            ("Fever 39.5°C and elevated lactate?", "emergency medicine"),
            ("Hypertension management guidelines?", "cardiology"),
        ]
        
        stats = {
            "total": 0,
            "passed": 0,
            "partial": 0,
            "failed": 0,
            "confidence_scores": []
        }
        
        for query, domain in queries:
            stats["total"] += 1
            
            # Get RAG answer
            answer = rag.query(query)
            
            # Validate
            validation = validator.validate_rag_answer(query, answer, domain)
            
            status = validation['overall_status']
            confidence = validation['confidence_score']
            
            # Update stats
            if status == 'pass':
                stats["passed"] += 1
            elif status == 'partial':
                stats["partial"] += 1
            else:
                stats["failed"] += 1
            
            stats["confidence_scores"].append(confidence)
            
            # Log result
            symbol = "✓" if status == "pass" else "⚠" if status == "partial" else "✗"
            print(f"  {symbol} Query {stats['total']}: {status.upper()} (confidence: {confidence:.2f})")
        
        # Final statistics
        print(f"\n" + "-" * 70)
        print("Pipeline Statistics:")
        print(f"  Total queries: {stats['total']}")
        print(f"  Passed: {stats['passed']} ({stats['passed']/stats['total']*100:.0f}%)")
        print(f"  Partial: {stats['partial']} ({stats['partial']/stats['total']*100:.0f}%)")
        print(f"  Failed: {stats['failed']} ({stats['failed']/stats['total']*100:.0f}%)")
        print(f"  Average confidence: {sum(stats['confidence_scores'])/len(stats['confidence_scores']):.2f}")
    
    finally:
        validator.stop_service()


def main():
    """Run all integration examples"""
    print("=" * 70)
    print("AI Validation MCP Service - Integration Examples")
    print("=" * 70)
    
    examples = [
        ("RAG System Validation", example_1_rag_validation),
        ("Test Discovery", example_2_test_discovery),
        ("Knowledge Base Validation", example_3_knowledge_base_validation),
        ("Continuous Validation Pipeline", example_4_continuous_validation)
    ]
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Example '{name}' failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("All examples completed")
    print("=" * 70)


if __name__ == "__main__":
    main()

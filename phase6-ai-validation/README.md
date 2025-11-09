# AI Validation MCP Service

MCP service that enables AI systems (RAG, GraphRAG, etc.) to validate their clinical answers using BDD tests.

## Overview

The AI Validation MCP Service provides a JSON-RPC 2.0 interface for AI systems to:
- **Discover relevant BDD tests** for clinical questions
- **Execute tests** against AI-generated answers
- **Validate answers** comprehensively across multiple tests
- **Validate knowledge bases** to assess overall AI clinical accuracy

## Features

✅ **Test Discovery** - Find relevant BDD tests by clinical question, domain, or context  
✅ **Test Execution** - Run individual BDD scenarios against AI answers  
✅ **Answer Validation** - Comprehensive validation with similarity scoring  
✅ **Knowledge Validation** - Batch validation of AI clinical knowledge  
✅ **Concept Matching** - Extract and compare clinical concepts  
✅ **Integration Ready** - Works with existing GuidelineAnalyzer and BDD Generator

## Quick Start

### Installation

```bash
cd phase6-ai-validation

# No additional dependencies required - uses existing POC components
```

### Start Service

```bash
# Interactive mode (stdio)
python3 ai_validation_mcp_service.py
```

### Run Tests

```bash
# Test all MCP methods
python3 test_ai_validation_client.py
```

Expected output:
```
======================================================================
AI Validation MCP Service - Test Suite
======================================================================
✓ AI Validation MCP Service started

[TEST 1] Initialize Service
  ✓ Server: AI Validation MCP Service v1.0.0
  ✓ Test repository size: 6
  ✓ Supported domains: cardiology, endocrinology, emergency medicine

[TEST 2] Discover Tests
  ✓ Query: How should I manage a patient with high blood pressure?
  ✓ Tests found: 2
    - test_0001: Patient with systolic bp... (relevance: 0.70)

[TEST 3] Execute Single Test
  ✓ Test: Patient with systolic bp...
  ✓ Status: pass
  ✓ Similarity score: 0.75
  ✓ Clinical accuracy: True

[TEST 4] Validate AI Answer
  ✓ Question: What treatment should I give...
  ✓ Tests executed: 2
  ✓ Tests passed: 2
  ✓ Overall status: pass
  ✓ Confidence score: 1.00

[TEST 5] Validate AI Knowledge Base
  ✓ Scenarios validated: 2
  ✓ Total tests executed: 4
  ✓ Total tests passed: 4
  ✓ Overall accuracy: 1.00

[TEST 6] Get Service Status
  ✓ Initialized: True
  ✓ Tests executed: 6
  ✓ Success rate: 1.00

======================================================================
Tests passed: 6/6
Success rate: 100%

✓ ALL TESTS PASSED
```

## MCP Methods

### 1. initialize

Initialize service and negotiate capabilities.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "serverInfo": {
      "name": "AI Validation MCP Service",
      "version": "1.0.0"
    },
    "capabilities": {
      "test_discovery": true,
      "test_execution": true,
      "answer_validation": true,
      "knowledge_validation": true,
      "supported_domains": ["cardiology", "endocrinology", "emergency medicine"],
      "supported_cds_categories": ["1.1.2", "1.1.3", ...]
    },
    "test_repository_size": 6
  }
}
```

### 2. discover_tests

Find relevant BDD tests for a clinical question.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "discover_tests",
  "params": {
    "clinical_question": "How should I manage a patient with high blood pressure?",
    "clinical_domain": "cardiology",
    "max_results": 5
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "query": "How should I manage...",
    "tests_found": 2,
    "tests": [
      {
        "test_id": "test_0001",
        "feature": "Hypertension Management",
        "scenario": "Patient with systolic bp of 140 mmhg receives...",
        "type": "positive",
        "tags": ["@positive", "@treatment"],
        "domain": "cardiology",
        "expected_outcome": "initiate ace inhibitor therapy should be initiated AND...",
        "relevance_score": 0.7
      }
    ]
  }
}
```

### 3. execute_test

Execute a single BDD test against an AI answer.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "execute_test",
  "params": {
    "test_id": "test_0001",
    "ai_answer": "Initiate ACE inhibitor therapy for blood pressure control"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "test_id": "test_0001",
    "test_name": "Patient with systolic bp...",
    "status": "pass",
    "similarity_score": 0.75,
    "clinical_accuracy": true,
    "matched_concepts": ["initiate", "inhibitor", "therapy", "pressure"],
    "missing_concepts": [],
    "extra_concepts": ["control"],
    "details": "AI answer matches expected clinical outcome"
  }
}
```

### 4. validate_answer

Validate AI answer against multiple relevant tests.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "validate_answer",
  "params": {
    "clinical_question": "What treatment for diabetes with HbA1c 8.5%?",
    "ai_answer": "Initiate metformin therapy as first-line treatment",
    "clinical_domain": "endocrinology"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "clinical_question": "What treatment...",
    "tests_executed": 2,
    "tests_passed": 2,
    "tests_failed": 0,
    "overall_status": "pass",
    "confidence_score": 1.0,
    "results": [
      {
        "test_id": "test_0003",
        "status": "pass",
        "similarity": 0.82,
        "clinical_accuracy": true
      }
    ]
  }
}
```

### 5. validate_knowledge

Validate AI clinical knowledge base comprehensively.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "validate_knowledge",
  "params": {
    "test_scenarios": [
      {
        "question": "How should I treat hypertension?",
        "answer": "Initiate ACE inhibitor therapy"
      },
      {
        "question": "What is first-line treatment for type 2 diabetes?",
        "answer": "Metformin is recommended"
      }
    ],
    "clinical_domain": "general"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "scenarios_validated": 2,
    "total_tests_executed": 4,
    "total_tests_passed": 4,
    "overall_accuracy": 1.0,
    "reports": [...],
    "recommendations": [
      "AI knowledge validation successful - no issues found"
    ]
  }
}
```

### 6. get_status

Get service status and metrics.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "get_status",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "initialized": true,
    "test_repository_size": 6,
    "tests_discovered": 10,
    "tests_executed": 6,
    "validations_performed": 2,
    "recent_validations": 6,
    "success_rate": 1.0
  }
}
```

## Integration Examples

### Example 1: RAG System Validation

```python
# RAG system generates answer from clinical guideline
question = "What is the recommended treatment for hypertension?"
rag_answer = rag_system.query(question)

# Validate answer using MCP service
validation_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "validate_answer",
    "params": {
        "clinical_question": question,
        "ai_answer": rag_answer,
        "clinical_domain": "cardiology"
    }
}

# Send to MCP service
response = mcp_client.send(validation_request)

# Check results
if response["result"]["overall_status"] == "pass":
    print("✓ RAG answer validated")
else:
    print("✗ RAG answer needs review")
    print(f"Confidence: {response['result']['confidence_score']}")
```

### Example 2: Knowledge Base Testing

```python
# Test multiple clinical scenarios
test_cases = [
    {"question": "Treat hypertension?", "answer": rag.query(...)},
    {"question": "Treat diabetes?", "answer": rag.query(...)},
    {"question": "Treat sepsis?", "answer": rag.query(...)}
]

validation_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "validate_knowledge",
    "params": {
        "test_scenarios": test_cases,
        "clinical_domain": "general"
    }
}

response = mcp_client.send(validation_request)

print(f"Overall accuracy: {response['result']['overall_accuracy']}")
print(f"Recommendations: {response['result']['recommendations']}")
```

### Example 3: Test Discovery for Unknown Questions

```python
# Discover relevant tests for novel clinical question
discovery_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "discover_tests",
    "params": {
        "clinical_question": "Patient with chest pain and elevated troponin?",
        "clinical_domain": "cardiology",
        "max_results": 10
    }
}

response = mcp_client.send(discovery_request)

# Review relevant tests
for test in response["result"]["tests"]:
    print(f"Relevance {test['relevance_score']}: {test['scenario']}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AI System (RAG/GraphRAG)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ JSON-RPC 2.0
                         ▼
┌─────────────────────────────────────────────────────────────┐
│          AI Validation MCP Service (stdio/HTTP)             │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Test         │  │ Test         │  │ Answer          │  │
│  │ Discovery    │  │ Execution    │  │ Validation      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Concept      │  │ Similarity   │  │ Knowledge       │  │
│  │ Extraction   │  │ Scoring      │  │ Validation      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ BDD          │  │ CIKG         │  │ Guideline    │
│ Generator    │  │ Processor    │  │ Analyzer     │
│ (POC 1)      │  │ (POC 3)      │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Validation Algorithm

1. **Test Discovery**
   - Match clinical question to test scenarios
   - Score by domain, context, and keyword overlap
   - Return ranked list of relevant tests

2. **Concept Extraction**
   - Tokenize AI answer and expected outcome
   - Remove stop words
   - Extract clinical concepts (medications, conditions, actions)

3. **Similarity Scoring**
   - Calculate text similarity (SequenceMatcher)
   - Compare concept overlap
   - Identify matched, missing, and extra concepts

4. **Clinical Accuracy**
   - Pass if: high similarity (≥70%) OR
   - Most concepts matched (≥80%) with few missing (≤2)

5. **Status Determination**
   - PASS: Clinical accuracy achieved
   - PARTIAL: Some concepts matched
   - FAIL: No significant match
   - ERROR: Processing error

## Test Repository

The service maintains a repository of BDD tests:

- **6 BDD tests** loaded from 3 clinical scenarios
- Each scenario generates positive + negative tests
- Tests include:
  - Hypertension Management (2 tests)
  - Diabetes Management (2 tests)
  - Sepsis Management (2 tests)

### Adding New Tests

To add new tests to the repository:

1. Add scenario to `_load_test_repository()` in `ai_validation_mcp_service.py`
2. Or load from external file/database
3. Service will automatically parse and index tests

## Performance

- **Test Discovery:** < 10ms (in-memory search)
- **Test Execution:** < 5ms per test
- **Answer Validation:** < 50ms (5 tests)
- **Knowledge Validation:** < 100ms (10 scenarios)

## Limitations & Future Work

**Current Limitations:**
- Basic keyword-based concept extraction (no NLP)
- Simple text similarity scoring
- Small test repository (6 tests)
- No terminology system integration

**Future Enhancements:**
- Medical NLP (scispaCy, ClinicalBERT) for concept extraction
- SNOMED CT/LOINC/RxNorm terminology matching
- Larger test repository from clinical guidelines
- Machine learning similarity models
- Ontology-based reasoning
- Integration with FHIR-CPG artifacts

## Files

- `ai_validation_mcp_service.py` (650 lines) - Main MCP service
- `test_ai_validation_client.py` (300 lines) - Test client
- `README.md` - This documentation

## Standards Compliance

✅ **MCP Protocol** - JSON-RPC 2.0 over stdio  
✅ **BDD Format** - Gherkin syntax  
✅ **Clinical Domains** - Cardiology, Endocrinology, Emergency Medicine  
✅ **Integration** - Uses existing GuidelineAnalyzer, BDD Generator, CIKG Processor

## Support

For issues or questions:
- Check test output: `python3 test_ai_validation_client.py`
- Review server logs (stderr)
- Verify POC components are accessible

## License

Part of Clinical BDD Creator project.

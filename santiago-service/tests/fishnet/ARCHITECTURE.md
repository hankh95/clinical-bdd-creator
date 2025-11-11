# Fishnet Santiago-BDD Testing Framework - Architecture Document

## Executive Summary

The **Fishnet** framework is a comprehensive BDD testing system specifically designed for validating clinical knowledge graphs, neurosymbolic reasoning, and clinical decision support in the Santiago service. Named to fit the "Old Man and the Sea" theme, Fishnet represents the net that captures and validates every node and connection in the clinical knowledge graph.

## Architecture Overview

### Design Principles

1. **Separation of Concerns**: Clinical scenarios (what to test) separate from technical validation (how to test)
2. **Layered Validation**: Test each Santiago layer (L1-L4) independently and together
3. **Reusability**: Leverage existing BDD scenarios from `examples/bdd-tests/scenarios/`
4. **Extensibility**: Easy to add new validation types and assertions
5. **Performance**: Fast feedback loops with efficient test execution

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fishnet Testing Framework                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Scenario    │  │    Graph     │  │  Reasoning   │          │
│  │   Loader     │  │  Validator   │  │    Tester    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │      QA      │  │   What-If    │  │  Assertion   │          │
│  │  Validator   │  │    Engine    │  │    Engine    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                         Test Scenarios                          │
│  Knowledge Graph | Reasoning | QA | What-If Scenarios          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Scenario Loader (`scenario_loader.py`)

**Purpose**: Load and manage clinical BDD scenarios

**Key Features**:
- Loads scenarios from standardized YAML format
- Supports Santiago-specific assertions via `.santiago.yaml` files
- Caches scenarios for performance
- Supports domain-based filtering

**Classes**:
- `ClinicalScenario`: Data class representing a clinical test scenario
- `ScenarioLoader`: Loader with caching and filtering capabilities

**Usage**:
```python
loader = ScenarioLoader()
scenario = loader.load_scenario("cardiology-treatment-hfref-001")
cardiology_scenarios = loader.load_scenarios_by_domain("cardiology")
```

### 2. Graph Validator (`graph_validator.py`)

**Purpose**: Validate knowledge graph fidelity across the four-layer model

**Key Features**:
- Layer-by-layer validation (L1→L2, L2→L3, L3→L4)
- Cross-layer consistency checking
- Gremlin query execution for graph assertions
- Semantic preservation validation
- Evidence traceability verification

**Classes**:
- `GraphValidator`: Main validator with layer-specific methods
- `GraphValidationResult`: Comprehensive validation results
- `LayerValidationResult`: Per-layer validation metrics
- `ValidationLayer`: Enum for Santiago layers

**Metrics**:
- Overall fidelity (0-1 scale)
- Layer transition accuracies
- Cross-layer consistency
- Clinical accuracy
- Semantic consistency

### 3. Reasoning Tester (`reasoning_tester.py`)

**Purpose**: Test neurosymbolic reasoning capabilities

**Key Features**:
- Symbolic reasoning validation (logic-based)
- Neural reasoning validation (similarity-based)
- Hybrid reasoning validation (combined)
- Confidence scoring validation
- Reasoning path verification

**Classes**:
- `ReasoningTester`: Main tester with method for each reasoning type
- `ReasoningTestResult`: Results with accuracy and confidence metrics
- `ReasoningType`: Enum (SYMBOLIC, NEURAL, HYBRID)

**Test Types**:
```python
# Symbolic: Rule-based, high confidence
symbolic_result = tester.test_symbolic_reasoning(scenario)

# Neural: Pattern matching, similarity scores
neural_result = tester.test_neural_reasoning(scenario, query)

# Hybrid: Combined approach
hybrid_result = tester.test_hybrid_reasoning(scenario)
```

### 4. QA Validator (`qa_validator.py`)

**Purpose**: Validate clinical question answering accuracy

**Key Features**:
- Answer correctness validation
- Evidence traceability checking
- Reasoning path validation
- Confidence calibration testing
- Response time monitoring

**Classes**:
- `QAValidator`: Question answering validator
- `QAValidationResult`: Detailed QA validation results

**Validation Areas**:
- Answer contains expected elements
- Evidence links to source guidelines
- Reasoning path is valid
- Confidence matches accuracy

### 5. What-If Engine (`whatif_engine.py`)

**Purpose**: Test guideline changes and clinical scenario variations

**Key Features**:
- Guideline change impact analysis
- Safety violation detection
- Clinical impact scoring
- Affected patient counting
- Recommendation change tracking

**Classes**:
- `WhatIfEngine`: Main engine for scenario testing
- `WhatIfResult`: Impact analysis results
- `ChangeType`: Enum for change types

**Change Types**:
- `ADD_CONTRAINDICATION`: New safety constraints
- `MEDICATION_DOSE_CHANGE`: Dosing updates
- `NEW_RECOMMENDATION`: New treatment options
- `UPDATE_CRITERIA`: Eligibility changes
- `FORMULARY_CHANGE`: Medication availability changes

### 6. Assertion Engine (`assertion_engine.py`)

**Purpose**: Evaluate assertions across all validation types

**Key Features**:
- Unified assertion evaluation
- Supports multiple comparison operators (>=, <=, ==, exists)
- Assertion result tracking
- Summary statistics generation
- Severity-based categorization

**Classes**:
- `AssertionEngine`: Central assertion evaluator
- `AssertionResult`: Single assertion result
- `AssertionType`: Enum (GRAPH, REASONING, QA, WHATIF)
- `AssertionSeverity`: Enum (ERROR, WARNING, INFO)

## Santiago Assertions Format

### File Structure

Each scenario can have a `.santiago.yaml` file with Santiago-specific assertions:

```yaml
scenario_id: "cardiology-treatment-hfref-001"
validation_type: "santiago-bdd"

graph_assertions:
  - id: "graph-001"
    description: "Validate node exists"
    layer: "structured_knowledge"
    gremlin: "g.V().has('concept', 'HFrEF').count()"
    expect: ">=1"
    severity: "error"

reasoning_assertions:
  - id: "reasoning-001"
    description: "Test symbolic reasoning"
    reasoning_type: "symbolic"
    input: {...}
    expected_output: {...}

qa_assertions:
  - id: "qa-001"
    question: "What is the dose?"
    expected_answer_contains: ["49/51 mg"]
    confidence_threshold: 0.9

whatif_assertions:
  - id: "whatif-001"
    description: "Test dose change"
    change: {...}
    expected_outcome: {...}
```

## Integration with Santiago Service

### Four-Layer Model Validation

Fishnet validates each layer of the Santiago model:

1. **Layer 1 (Raw Text)**: Validates text extraction and entity recognition
2. **Layer 2 (Structured Knowledge)**: Validates concept extraction and relationships
3. **Layer 3 (Computable Logic)**: Validates rules and decision criteria
4. **Layer 4 (Executable Workflows)**: Validates DAGs and workflow execution

### Knowledge Graph Queries

Uses Gremlin/TinkerPop for graph traversal:

```gremlin
// Find all GDMT recommendations for HFrEF
g.V().has('diagnosis', 'HFrEF')
     .out('recommends')
     .has('therapy_type', 'GDMT')
```

### Neurosymbolic Reasoning Integration

- **Symbolic Component**: Validates logic execution and rule application
- **Neural Component**: Validates embedding similarity and pattern matching
- **Hybrid Integration**: Validates appropriate weighting and combination

## Test Execution Workflow

### 1. Scenario-Driven Testing

```python
# Load scenario
loader = ScenarioLoader()
scenario = loader.load_scenario("cardiology-treatment-hfref-001")

# Run all validations
graph_result = graph_validator.validate_graph_fidelity(scenario)
reasoning_results = reasoning_tester.validate_reasoning_assertions(scenario)
qa_results = qa_validator.validate_qa_assertions(scenario)
whatif_results = whatif_engine.test_whatif_assertions(scenario)
```

### 2. Assertion-Driven Testing

```python
# Evaluate all assertions for a scenario
engine = AssertionEngine()
results = engine.evaluate_all_assertions(scenario)

# Get summary
summary = engine.get_results_summary()
print(f"Pass rate: {summary['pass_rate']:.2%}")
```

### 3. Continuous Integration

```bash
# Run all Fishnet tests
pytest santiago-service/tests/fishnet/ -v

# Run specific category
pytest santiago-service/tests/fishnet/test_knowledge_graph_fidelity.py -v

# Run with coverage
pytest santiago-service/tests/fishnet/ --cov=src --cov-report=html
```

## Performance Characteristics

### Target Metrics

| Validation Type | Target Latency | Complexity |
|----------------|----------------|------------|
| Scenario Load | <50ms | O(1) |
| Graph Validation | <100ms | O(n log n) |
| Reasoning Test | <250ms | O(n) |
| QA Validation | <500ms | O(n) |
| What-If Analysis | <1000ms | O(n²) |

### Optimization Strategies

1. **Caching**: Scenarios and graph structures cached
2. **Lazy Loading**: Load only what's needed for each test
3. **Parallel Execution**: Independent tests run in parallel
4. **Incremental Validation**: Validate only changed components

## Extensibility Points

### Adding New Validation Types

1. Create new validator class inheriting from base pattern
2. Implement validation methods
3. Add to `AssertionEngine` for unified evaluation
4. Create tests following existing patterns

### Adding New Assertion Types

1. Define new assertion format in Santiago YAML
2. Add parser in relevant validator
3. Implement evaluation logic
4. Add tests for new assertion type

### Adding New Scenarios

1. Create clinical scenario YAML in `examples/bdd-tests/scenarios/`
2. Create Santiago assertions YAML (`.santiago.yaml`)
3. Write pytest tests using Fishnet framework
4. Validate with clinical domain experts

## Quality Metrics

### Test Coverage Targets

- Framework code: ≥90%
- Validation logic: ≥95%
- Clinical scenarios: ≥80% of use cases

### Validation Thresholds

- Knowledge graph fidelity: ≥95%
- Reasoning accuracy: ≥95% (symbolic), ≥85% (neural), ≥90% (hybrid)
- QA accuracy: ≥90%
- Cross-layer consistency: ≥95%

## Future Enhancements

### Phase 2 Features

- [ ] Interactive what-if UI for clinicians
- [ ] Reasoning path visualization
- [ ] Batch scenario testing
- [ ] Guideline version comparison
- [ ] Performance profiling dashboard

### Phase 3 Features

- [ ] Automated scenario generation from guidelines
- [ ] Machine learning for assertion optimization
- [ ] Clinical study impact analysis
- [ ] Real-time knowledge graph monitoring
- [ ] Bias and fairness validation

## References

- **Santiago Service**: Four-layer NeuroSymbolic knowledge graph service
- **BDD Scenarios**: Standardized clinical test scenarios
- **Gremlin/TinkerPop**: Graph traversal language and framework
- **FHIR-CPG**: Clinical Practice Guidelines specification
- **Clinical Informatics**: Evidence-based medicine and knowledge representation

## Conclusion

Fishnet provides a comprehensive, extensible framework for validating clinical knowledge graphs and neurosymbolic reasoning. By separating clinical scenarios from technical validation, maintaining layered testing, and supporting multiple validation types, Fishnet ensures the Santiago service delivers accurate, safe, and evidence-based clinical decision support.

The framework is designed to grow with Santiago, supporting continuous validation as guidelines evolve, reasoning capabilities improve, and clinical requirements expand.

---

**Version**: 1.0.0  
**Date**: 2025-11-11  
**Status**: Production Ready  
**Maintainers**: Clinical BDD Creator Team

# Fishnet: Santiago-BDD Testing Framework

> *"The fishnet catches the knowledge, validates the reasoning, and ensures every connection holds." - Inspired by The Old Man and the Sea*

## Overview

**Fishnet** is the Santiago-BDD testing framework designed specifically for validating clinical knowledge graphs, neurosymbolic reasoning, and clinical decision support capabilities. Unlike traditional project-BDD tests that validate software behavior, Fishnet validates the fidelity and accuracy of clinical knowledge representation and reasoning.

## Purpose

Fishnet serves as the critical validation layer for the Santiago service, ensuring:

1. **Knowledge Graph Fidelity**: Derived graph assets accurately represent clinical guidelines
2. **Clinical Knowledge QA**: Question answering produces clinically accurate and evidence-based responses
3. **Neurosymbolic Reasoning**: Hybrid symbolic-neural reasoning produces correct clinical inferences
4. **What-If Scenarios**: Guideline changes can be tested for downstream impacts
5. **Automated Validation**: Systematic validation of all four layers of the Santiago model

## Framework Architecture

### Core Components

```
fishnet/
├── README.md                          # This file
├── __init__.py                        # Package initialization
├── framework/                         # Core framework code
│   ├── __init__.py
│   ├── scenario_loader.py            # Loads clinical scenarios from YAML
│   ├── graph_validator.py            # Validates graph knowledge fidelity
│   ├── reasoning_tester.py           # Tests neurosymbolic reasoning
│   ├── qa_validator.py               # Validates clinical question answering
│   ├── whatif_engine.py              # What-if scenario testing engine
│   └── assertion_engine.py           # Assertion evaluation engine
├── scenarios/                         # Santiago-specific BDD scenarios
│   ├── knowledge-graph/              # Knowledge graph fidelity tests
│   ├── reasoning/                    # Reasoning validation tests
│   ├── qa/                           # Clinical QA tests
│   └── whatif/                       # What-if scenario tests
├── fixtures/                          # Test fixtures and sample data
│   ├── guidelines/                   # Sample guideline documents
│   ├── graphs/                       # Sample knowledge graphs
│   └── queries/                      # Sample clinical queries
├── test_fishnet_framework.py         # Framework unit tests
├── test_knowledge_graph_fidelity.py  # Knowledge graph fidelity tests
├── test_neurosymbolic_reasoning.py   # Neurosymbolic reasoning tests
├── test_clinical_qa.py               # Clinical QA validation tests
└── test_whatif_scenarios.py          # What-if scenario tests
```

## Key Concepts

### 1. Knowledge Graph Fidelity Testing

Validates that clinical guidelines are accurately transformed through the four-layer model:

- **Layer 1 → 2**: Raw text to structured knowledge
- **Layer 2 → 3**: Structured knowledge to computable logic
- **Layer 3 → 4**: Computable logic to executable workflows
- **Cross-layer consistency**: Semantic preservation across transformations

### 2. Neurosymbolic Reasoning Validation

Tests hybrid reasoning capabilities:

- **Symbolic reasoning**: Logic execution, rule application, graph traversal
- **Neural reasoning**: Pattern recognition, similarity matching, uncertainty handling
- **Hybrid integration**: Correct combination of symbolic and neural components
- **Confidence scoring**: Appropriate confidence levels for different reasoning paths

### 3. Clinical Question Answering Validation

Ensures accurate and evidence-based responses:

- **Correctness**: Clinically accurate answers
- **Evidence traceability**: Answers linked to source guidelines
- **Reasoning transparency**: Explainable reasoning paths
- **Confidence calibration**: Confidence scores match accuracy

### 4. What-If Scenario Testing

Enables testing guideline changes and their impacts:

- **Guideline updates**: Test impact of new recommendations
- **Contraindication changes**: Verify safety constraint updates
- **Medication formulary changes**: Test alternative medication suggestions
- **Patient population changes**: Validate reasoning for different demographics

## Scenario Format

Fishnet scenarios extend the standardized BDD format with Santiago-specific assertions:

### Clinical Scenario YAML (`{scenario-id}.yaml`)

Standard clinical scenario format from `examples/bdd-tests/scenarios/`

### Santiago Assertions YAML (`{scenario-id}.santiago.yaml`)

Santiago-specific validation rules:

```yaml
scenario_id: "cardiology-treatment-hfref-001"
validation_type: "santiago-bdd"

# Knowledge Graph Assertions
graph_assertions:
  - id: "graph-001"
    description: "HFrEF diagnosis node exists in Layer 2"
    layer: "structured_knowledge"
    gremlin: "g.V().has('concept', 'HFrEF').has('layer', 'structured_knowledge')"
    expect: "exists"
    
  - id: "graph-002"
    description: "GDMT recommendations linked to HFrEF diagnosis"
    layer: "computable_logic"
    gremlin: "g.V().has('diagnosis', 'HFrEF').out('recommends').has('therapy_type', 'GDMT').count()"
    expect: ">=4"  # Four foundational therapies

# Reasoning Assertions
reasoning_assertions:
  - id: "reasoning-001"
    description: "Symbolic reasoning identifies GDMT requirement"
    reasoning_type: "symbolic"
    input: 
      patient: "HFrEF with LVEF <= 35%"
      contraindications: []
    expected_output:
      recommendation: "quadruple GDMT"
      confidence: ">=0.95"
      reasoning_path: ["diagnosis_check", "contraindication_check", "guideline_lookup"]
  
  - id: "reasoning-002"
    description: "Neural similarity matches clinical scenario"
    reasoning_type: "neural"
    query: "What medications for heart failure with low ejection fraction?"
    expected_concepts: ["ARNI", "beta-blocker", "MRA", "SGLT2i"]
    similarity_threshold: 0.85

# Clinical QA Assertions
qa_assertions:
  - id: "qa-001"
    question: "What is the initial dose of sacubitril/valsartan for HFrEF?"
    expected_answer_contains: ["49/51 mg", "twice daily"]
    expected_evidence:
      - guideline: "2022 AHA/ACC/HFSA Heart Failure Guideline"
        section: "Pharmacological Treatment"
    confidence_threshold: 0.9
  
  - id: "qa-002"
    question: "What monitoring is required after starting spironolactone?"
    expected_answer_contains: ["potassium", "renal function", "3-7 days"]
    expected_evidence:
      - guideline: "2022 AHA/ACC/HFSA Heart Failure Guideline"
    confidence_threshold: 0.85

# What-If Assertions
whatif_assertions:
  - id: "whatif-001"
    description: "Test impact of new SGLT2i contraindication"
    change:
      type: "add_contraindication"
      drug_class: "SGLT2i"
      condition: "eGFR < 20"
    test_patient:
      diagnosis: "HFrEF"
      labs:
        egfr: 18
    expected_outcome:
      sglt2i_recommended: false
      alternative_therapy: "triple therapy without SGLT2i"
      reasoning_includes: "eGFR below threshold"
```

## Usage Examples

### Basic Fishnet Test Execution

```python
import pytest
from fishnet.framework import ScenarioLoader, GraphValidator, ReasoningTester, QAValidator

def test_hfref_knowledge_graph_fidelity():
    """Test that HFrEF guideline is correctly represented in knowledge graph"""
    
    # Load clinical scenario
    loader = ScenarioLoader()
    scenario = loader.load_scenario("cardiology-treatment-hfref-001")
    
    # Validate knowledge graph
    validator = GraphValidator()
    result = validator.validate_graph_fidelity(scenario)
    
    assert result.layer_1_to_2_accuracy >= 0.95
    assert result.layer_2_to_3_accuracy >= 0.95
    assert result.layer_3_to_4_accuracy >= 0.95
    assert result.cross_layer_consistency >= 0.95

def test_neurosymbolic_reasoning_hfref():
    """Test neurosymbolic reasoning for HFrEF treatment recommendations"""
    
    # Setup reasoning tester
    tester = ReasoningTester()
    
    # Test symbolic reasoning
    symbolic_result = tester.test_symbolic_reasoning(
        scenario="cardiology-treatment-hfref-001",
        reasoning_type="diagnosis_to_treatment"
    )
    assert symbolic_result.accuracy >= 0.95
    assert "GDMT" in symbolic_result.recommendations
    
    # Test neural reasoning
    neural_result = tester.test_neural_reasoning(
        scenario="cardiology-treatment-hfref-001",
        query="heart failure treatment with low ejection fraction"
    )
    assert neural_result.similarity_score >= 0.85
    assert len(neural_result.matched_concepts) >= 4
    
    # Test hybrid reasoning
    hybrid_result = tester.test_hybrid_reasoning(
        scenario="cardiology-treatment-hfref-001"
    )
    assert hybrid_result.confidence >= 0.90
    assert hybrid_result.symbolic_weight >= 0.7  # Symbolic should dominate for guideline-based

def test_clinical_qa_validation():
    """Test clinical question answering accuracy"""
    
    qa_validator = QAValidator()
    
    # Test basic QA
    result = qa_validator.validate_question(
        question="What is the target blood pressure for HFrEF patients?",
        scenario="cardiology-treatment-hfref-001"
    )
    
    assert result.answer_accuracy >= 0.90
    assert len(result.evidence_sources) >= 1
    assert result.reasoning_path_valid is True
    assert result.confidence_calibrated is True

def test_whatif_guideline_change():
    """Test what-if scenario for guideline updates"""
    
    from fishnet.framework import WhatIfEngine
    
    engine = WhatIfEngine()
    
    # Test impact of SGLT2i dose change
    result = engine.test_guideline_change(
        scenario="cardiology-treatment-hfref-001",
        change={
            "type": "medication_dose_change",
            "drug": "dapagliflozin",
            "old_dose": "10 mg",
            "new_dose": "5 mg"
        }
    )
    
    assert result.affected_patients_count >= 0
    assert result.recommendation_changes is not None
    assert result.safety_violations == 0
```

### Running Fishnet Tests

```bash
# Run all Fishnet tests
pytest santiago-service/tests/fishnet/ -v

# Run specific test category
pytest santiago-service/tests/fishnet/test_knowledge_graph_fidelity.py -v
pytest santiago-service/tests/fishnet/test_neurosymbolic_reasoning.py -v
pytest santiago-service/tests/fishnet/test_clinical_qa.py -v
pytest santiago-service/tests/fishnet/test_whatif_scenarios.py -v

# Run tests with coverage
pytest santiago-service/tests/fishnet/ --cov=santiago-service/src --cov-report=html

# Run tests matching pattern
pytest santiago-service/tests/fishnet/ -k "hfref" -v
```

## Integration with Existing BDD Scenarios

Fishnet reuses clinical scenarios from `examples/bdd-tests/scenarios/` but adds Santiago-specific validation:

1. **Clinical Scenarios**: Use existing YAML files for clinical context
2. **Gherkin Features**: Use existing feature files for human-readable tests
3. **Santiago Assertions**: Add `.santiago.yaml` files for graph/reasoning validation
4. **Automated Conversion**: Convert standard assertions to Santiago assertions automatically

## Relationship to Project-BDD

| Aspect | Project-BDD | Santiago-BDD (Fishnet) |
|--------|-------------|------------------------|
| **Purpose** | Validate software behavior | Validate clinical knowledge and reasoning |
| **Focus** | Code correctness | Knowledge fidelity and reasoning accuracy |
| **Assertions** | FHIRPath, business logic | Graph queries, reasoning paths, QA accuracy |
| **Test Data** | Mock/synthetic | Real guidelines and clinical scenarios |
| **Execution** | CI/CD pipeline | Continuous + on-demand for guideline updates |
| **Audience** | Software engineers | Clinical informaticists + software engineers |

## Best Practices

### 1. Scenario Design

- **Clinical Accuracy**: Base scenarios on current clinical guidelines
- **Comprehensive Coverage**: Cover common cases, edge cases, and contraindications
- **Evidence-Based**: Link assertions to specific guideline references
- **Realistic Context**: Use clinically realistic patient data

### 2. Assertion Design

- **Specific**: Test specific knowledge graph properties
- **Measurable**: Use quantifiable success criteria
- **Traceable**: Link to source guidelines and clinical evidence
- **Maintainable**: Design for easy updates when guidelines change

### 3. Test Organization

- **Layered Testing**: Test each Santiago layer independently and together
- **Incremental Validation**: Build from simple to complex scenarios
- **Reproducible**: Ensure tests produce consistent results
- **Fast Feedback**: Prioritize quick tests for common scenarios

### 4. Continuous Validation

- **Automated Execution**: Run on every code change
- **Guideline Version Tracking**: Tag scenarios with guideline versions
- **Performance Monitoring**: Track test execution time
- **Quality Metrics**: Monitor test coverage and pass rates

## Contributing

### Adding New Fishnet Scenarios

1. **Start with Clinical Scenario**: Use or create scenario in `examples/bdd-tests/scenarios/`
2. **Add Santiago Assertions**: Create `.santiago.yaml` file with graph/reasoning assertions
3. **Write Test Cases**: Implement pytest test cases using Fishnet framework
4. **Validate Clinically**: Review assertions with clinical domain experts
5. **Document**: Add scenario to this README and framework documentation

### Extending the Framework

1. **Framework Extensions**: Add to `framework/` directory
2. **New Assertion Types**: Extend `assertion_engine.py`
3. **New Validators**: Add new validator classes for specialized validation
4. **Performance Tools**: Add profiling and benchmarking utilities

## Future Enhancements

### Planned Features

- [ ] **Interactive What-If UI**: Visual tool for guideline change testing
- [ ] **Reasoning Path Visualization**: Graphical display of reasoning paths
- [ ] **Batch Scenario Testing**: Test multiple scenarios simultaneously
- [ ] **Guideline Version Comparison**: Compare knowledge graphs across guideline versions
- [ ] **Performance Benchmarking**: Automated performance testing suite
- [ ] **Clinical Study Integration**: Link scenarios to clinical trial data
- [ ] **Continuous Monitoring**: Real-time knowledge graph health monitoring

### Research Integration

- **Evidence Synthesis**: Automated extraction of assertions from clinical evidence
- **Uncertainty Quantification**: Advanced confidence calibration methods
- **Bias Detection**: Identify and measure biases in reasoning
- **Fairness Validation**: Ensure equitable recommendations across populations

## References

- **Santiago Service**: `santiago-service/README.md`
- **BDD Scenarios**: `examples/bdd-tests/scenarios/README.md`
- **Four-Layer Model**: `santiago-research-plan.md`
- **Clinical Informatics**: `.github/agents/clinical.informaticist.instructions.md`

## Support

For questions or issues:
1. Review this documentation and examples
2. Check existing test cases for patterns
3. Consult Santiago service documentation
4. Open an issue with detailed description

---

**Fishnet** - *Validating clinical knowledge, one node at a time.*

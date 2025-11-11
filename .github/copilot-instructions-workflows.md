# Copilot Coding Agent Workflow Instructions

## Daily Development Workflow

### Session Management

1. **Start Session**: Review current daily notes (`daily-notes/YYYY-MM-DD.md`) and development plan
2. **Update Progress**: Update daily notes every 2-3 hours during active work sessions
3. **End Session**: Update daily notes and commit changes before ending work
4. **Documentation**: Maintain comprehensive session documentation

### Git Workflow

1. **Branch Strategy**: Use feature branches for all development work
2. **Commit Frequency**: Make atomic commits with descriptive messages
3. **Pull Requests**: Create PRs for all changes with detailed descriptions
4. **Code Review**: Participate in peer review process

## Task Assignment & Execution

### Agent Task Criteria

- **Research Tasks**: Clinical standards analysis, terminology research, architectural design
- **Implementation Tasks**: Feature development with clear specifications and acceptance criteria
- **Documentation Tasks**: Technical writing, specification development, user guides
- **Testing Tasks**: Test suite development, validation framework creation

### Task Execution Process

1. **Task Analysis**: Understand requirements, scope, and deliverables
2. **Planning**: Break down into manageable steps with time estimates
3. **Implementation**: Follow coding standards and clinical safety requirements
4. **Testing**: Comprehensive testing including clinical validation scenarios
5. **Documentation**: Complete documentation and usage examples
6. **Review**: Self-review and prepare for human review

## Clinical Informatics Workflows

### Guideline Processing Workflow

1. **Source Analysis**: Analyze clinical guideline structure and content
2. **Entity Extraction**: Identify clinical concepts, conditions, interventions
3. **Relationship Discovery**: Apply DRDE for clinical relationship identification
4. **Validation**: Clinical validation of extracted knowledge
5. **BDD Generation**: Create executable BDD scenarios from validated knowledge

### Santiago Service Integration

1. **Layer Processing**: Follow four-layer architecture (L0→L1→L2→L3)
2. **Standards Compliance**: Ensure FHIR, OpenEHR, and terminology standards compliance
3. **Knowledge Graph**: Populate graph with validated clinical knowledge
4. **NeuroSymbolic Reasoning**: Integrate symbolic and neural reasoning components
5. **Clinical QA**: Validate reasoning outputs for clinical accuracy

## Code Generation Patterns

### Python Code Standards

```python
# Example: Clinical concept extraction function
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ClinicalConceptExtractor:
    """
    Extract clinical concepts from text using pattern matching and NLP.

    This class implements the Layer 0 → Layer 1 transformation for
    clinical guideline processing in the Santiago service.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize extractor with configuration."""
        self.config = config
        self.concept_patterns = self._load_concept_patterns()

    def extract_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract clinical concepts from input text.

        Args:
            text: Clinical text to analyze

        Returns:
            List of extracted concepts with metadata
        """
        concepts = []

        # Implementation follows clinical safety patterns
        # - Validate input parameters
        # - Apply extraction logic
        # - Return structured results

        return concepts

    def _load_concept_patterns(self) -> Dict[str, List[str]]:
        """Load clinical concept patterns from configuration."""
        # Implementation details
        pass
```

### Test Generation Patterns

```python
# Example: Clinical workflow test
import pytest
from unittest.mock import Mock, patch

class TestClinicalWorkflow:
    """Test clinical workflow processing and validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.workflow_processor = ClinicalWorkflowProcessor()
        self.test_guideline = self._load_test_guideline()

    def test_guideline_processing(self):
        """Test end-to-end guideline processing."""
        # Given: A clinical guideline
        guideline = self.test_guideline

        # When: Processing the guideline
        result = self.workflow_processor.process_guideline(guideline)

        # Then: Validate clinical accuracy
        assert result.is_valid
        assert len(result.concepts) > 0
        assert result.confidence_score > 0.8

    def test_clinical_safety_validation(self):
        """Test clinical safety validation of processed guidelines."""
        # Test safety-critical validation logic
        pass
```

## Documentation Standards

### Code Documentation

- **Docstrings**: Comprehensive docstrings for all public functions/classes
- **Type Hints**: Complete type annotations
- **Clinical Context**: Include clinical relevance and safety considerations
- **Examples**: Provide usage examples where appropriate

### Technical Documentation

- **Architecture**: Document system architecture and design decisions
- **APIs**: Complete API documentation with examples
- **Deployment**: Deployment and configuration guides
- **Troubleshooting**: Common issues and resolution steps

## Quality Assurance Workflows

### Code Review Checklist

- [ ] Clinical accuracy validated
- [ ] Patient safety considerations addressed
- [ ] Test coverage > 80%
- [ ] Documentation complete
- [ ] Performance requirements met
- [ ] Security considerations addressed

### Testing Workflow

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **Clinical Validation**: Test against real clinical scenarios
4. **Performance Tests**: Validate performance requirements
5. **Security Tests**: Validate security controls

## Agent Communication Patterns

### Progress Reporting

```markdown
## Task Progress Update

**Task**: [Task Name]
**Status**: [In Progress/Completed/Blocked]
**Progress**: [Current completion percentage]
**Next Steps**: [Upcoming work items]
**Blockers**: [Any issues or dependencies]
**Clinical Validation**: [Status of clinical accuracy checks]
```

### Issue Escalation

```markdown
## 🚨 Issue Escalation Required

**Issue**: [Brief description]
**Impact**: [Patient safety, system functionality, timeline]
**Context**: [Relevant clinical/technical details]
**Proposed Resolution**: [Suggested approach]
**Urgency**: [Critical/High/Medium/Low]
```

### Knowledge Sharing

```markdown
## 📚 Clinical Informatics Learning

**Topic**: [Clinical concept or technical pattern]
**Context**: [When/why this is relevant]
**Key Insights**: [Important learnings]
**Implementation**: [How to apply in code]
**References**: [Clinical guidelines or standards]
```

## Clinical Safety Protocols

### Safety-First Development

1. **Clinical Validation**: All changes must be clinically validated
2. **Error Handling**: Comprehensive error handling for clinical scenarios
3. **Audit Trail**: Maintain traceability for clinical decisions
4. **Fail-Safe**: Default to safe behavior when uncertain

### Risk Assessment

- **Patient Safety**: Critical - immediate escalation required
- **Clinical Accuracy**: High - requires clinical expert review
- **System Reliability**: Medium - standard review process
- **Performance**: Low - optimization opportunity

## Integration Testing Patterns

### End-to-End Clinical Workflows

```python
def test_clinical_decision_support_workflow():
    """Test complete clinical decision support workflow."""
    # Setup: Clinical scenario
    patient_data = create_test_patient_data()
    clinical_context = create_clinical_context()

    # Execute: Full workflow
    assessment = cds_engine.assess_patient(patient_data, clinical_context)
    recommendations = cds_engine.generate_recommendations(assessment)

    # Validate: Clinical appropriateness
    assert_recommendations_clinically_appropriate(recommendations)
    assert_patient_safety_maintained(recommendations)
```

### FHIR Standards Compliance Testing

```python
def test_fhir_compliance():
    """Test FHIR resource generation and validation."""
    # Generate FHIR resources
    resources = santiago_service.generate_fhir_resources(guideline)

    # Validate against FHIR profiles
    for resource in resources:
        assert_fhir_valid(resource)
        assert_clinical_content_accurate(resource)
```

## Performance Optimization Workflows

### Profiling Workflow

1. **Identify Bottlenecks**: Profile clinical workflow performance
2. **Optimize Critical Paths**: Focus on patient-facing operations
3. **Cache Strategically**: Implement clinical terminology caching
4. **Monitor Continuously**: Track performance in production

### Scalability Patterns

- **Horizontal Scaling**: Design for distributed processing
- **Caching Layers**: Multi-tier caching for clinical data
- **Async Processing**: Background processing for non-critical operations
- **Load Balancing**: Distribute clinical workload across instances

## Continuous Learning Integration

### Feedback Integration

- **Clinical Feedback**: Incorporate clinician feedback into improvements
- **Performance Data**: Use performance metrics to guide optimizations
- **Error Analysis**: Learn from clinical errors and near-misses
- **Standards Updates**: Stay current with evolving clinical standards

### Knowledge Base Updates

- **Clinical Guidelines**: Regularly update to latest evidence
- **Terminology**: Maintain current clinical terminology versions
- **Best Practices**: Adopt evolving clinical informatics practices
- **Technology**: Stay current with relevant technologies

---

*These workflow instructions ensure consistent, high-quality development practices across all Copilot coding agent tasks in the Clinical BDD Creator project.*

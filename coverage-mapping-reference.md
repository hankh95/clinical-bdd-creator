# Coverage Category Mappings Reference

**Version:** 1.0.0
**Date:** 2025-11-08
**Status:** Active

This reference document maps CDS scenario identifiers to configurable coverage categories, enabling flexible taxonomy evolution while maintaining operational consistency.

## Overview

The coverage mapping system decouples the operational coverage logic from specific taxonomy identifiers. This allows:

- **Taxonomy Evolution**: Update usage scenario classifications without breaking coverage configurations
- **Organizational Flexibility**: Different organizations can map scenarios to categories based on their needs
- **API Stability**: Service interfaces remain stable even as underlying taxonomies change

## Mapping Structure

### Category Definitions

Each coverage category represents a logical grouping of clinical decision support scenarios:

| Category | Description | Clinical Focus |
|----------|-------------|----------------|
| `treatment_recommendation` | Core treatment decisions and recommendations | Clinical decision making |
| `drug_recommendation` | Medication-specific recommendations and guidelines | Pharmacology and safety |
| `cancer_treatment` | Oncology-specific treatment recommendations | Cancer care pathways |
| `diagnostic_test` | Diagnostic test ordering and interpretation | Diagnostic workflows |
| `genetic_test` | Genetic and genomic testing recommendations | Genomic medicine |
| `next_best_action` | Sequential clinical decision support | Care progression |
| `value_based_care` | Value-based care optimization alerts | Healthcare economics |
| `lifestyle_education` | Patient lifestyle and education interventions | Preventive care |
| `drug_interaction` | Drug interaction detection and alerts | Medication safety |
| `diagnostic_appropriateness` | Diagnostic test utilization and appropriateness | Resource optimization |
| `adverse_event_monitoring` | Adverse event detection and monitoring | Patient safety |
| `case_management` | Case management and coordination | Care coordination |
| `quality_metrics` | Quality measurement and reporting | Performance monitoring |
| `risk_stratification` | Patient risk assessment and stratification | Risk management |
| `public_health_reporting` | Public health surveillance and reporting | Population health |
| `shared_decision_support` | Shared decision making tools and support | Patient engagement |
| `sdoh_integration` | Social determinants of health integration | Holistic care |
| `patient_reminders` | Patient education and reminder systems | Adherence support |
| `guideline_retrieval` | Clinical guideline information retrieval | Knowledge access |
| `protocol_driven_care` | Protocol-based care pathways | Standardized care |
| `documentation_support` | Clinical documentation assistance | Administrative support |
| `care_coordination` | Care coordination and handoff support | Team coordination |

## CDS Scenario to Category Mappings

### Section 1.1: Assessment & Diagnosis

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 1.1.1 | Differential Diagnosis | diagnostic_test | Core diagnostic decision support |
| 1.1.2 | Treatment Recommendation | treatment_recommendation | Primary treatment decisions |
| 1.1.3 | Drug Recommendation | drug_recommendation | Medication-specific guidance |
| 1.1.4 | Cancer Treatment Recommendation | cancer_treatment | Specialized oncology care |
| 1.1.5 | Diagnostic Test Recommendation | diagnostic_test | Test ordering guidance |
| 1.1.6 | Genetic Test Recommendation | genetic_test | Genomic testing guidance |
| 1.1.7 | Next Best Action | next_best_action | Sequential care decisions |

### Section 1.2: Medication Management

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 1.2.1 | Drug Interaction Checking | drug_interaction | Medication safety monitoring |
| 1.2.2 | Diagnostic Test Appropriateness Check | diagnostic_appropriateness | Test utilization optimization |

### Section 1.3: Patient Safety & Monitoring

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 1.3.1 | Adverse Event Monitoring | adverse_event_monitoring | Patient safety surveillance |

### Section 2.1: Care Management

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 2.1.1 | Case Management | case_management | Care coordination support |

### Section 2.2: Quality & Performance

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 2.2.1 | Quality Metrics Reporting | quality_metrics | Performance measurement |

### Section 2.3: Risk Management

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 2.3.1 | Risk Stratification | risk_stratification | Patient risk assessment |

### Section 2.4: Public Health

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 2.4.1 | Public Health Reporting | public_health_reporting | Population health surveillance |

### Section 3.1: Patient Engagement

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 3.1.1 | Shared Decision-Making Support | shared_decision_support | Patient-centered care |

### Section 3.2: Social Determinants

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 3.2.1 | SDOH Integration | sdoh_integration | Holistic patient care |

### Section 3.3: Education & Communication

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 3.3.1 | Patient Education and Reminders | patient_reminders | Adherence and education |

### Section 4.1: Information Access

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 4.1.1 | Guideline-Driven Information Retrieval | guideline_retrieval | Knowledge management |

### Section 4.2: Care Pathways

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 4.2.1 | Protocol-Driven Care | protocol_driven_care | Standardized care delivery |

### Section 4.3: Documentation

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 4.3.1 | Documentation Support | documentation_support | Administrative efficiency |

### Section 4.4: Coordination

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 4.4.1 | Care Coordination Alerts | care_coordination | Team coordination |

## Configuration Examples

### Default Project Configuration

```yaml
# coverage-config.yaml
coverage_targets:
  strategy: tiered
  default_tier: medium
  category_mappings:
    treatment_recommendation: high
    drug_recommendation: high
    cancer_treatment: none
    diagnostic_test: high
    genetic_test: medium
    next_best_action: medium
    value_based_care: low
    lifestyle_education: low
    drug_interaction: medium
    diagnostic_appropriateness: medium
    adverse_event_monitoring: medium
    case_management: low
    quality_metrics: medium
    risk_stratification: low
    public_health_reporting: low
    shared_decision_support: low
    sdoh_integration: low
    patient_reminders: low
    guideline_retrieval: low
    protocol_driven_care: medium
    documentation_support: low
    care_coordination: low
```

### Organization-Specific Overrides

```yaml
# oncology-focused-config.yaml
coverage_targets:
  category_mappings:
    cancer_treatment: high          # Override from none to high
    genetic_test: high             # Override from medium to high
    adverse_event_monitoring: high  # Override from medium to high
    risk_stratification: medium     # Override from low to medium
```

### Emergency Department Configuration

```yaml
# ed-config.yaml
coverage_targets:
  category_mappings:
    treatment_recommendation: high
    diagnostic_test: high
    adverse_event_monitoring: high
    risk_stratification: high
    next_best_action: high
    care_coordination: medium
```

## Taxonomy Evolution Guidelines

### Adding New CDS Scenarios

When new CDS scenarios are identified:

1. **Analyze Clinical Purpose**: Determine the primary clinical intent
2. **Map to Existing Category**: Find the best matching category from the defined list
3. **Create New Category (Rare)**: Only if no existing category fits and the clinical purpose is unique
4. **Update Documentation**: Add the new mapping to this reference
5. **Test Coverage Logic**: Ensure coverage rules apply correctly

### Modifying Category Assignments

When reassigning scenarios to different categories:

1. **Document Rationale**: Explain the clinical reasoning for the change
2. **Impact Assessment**: Evaluate effects on existing coverage configurations
3. **Transition Plan**: Provide migration guidance for affected configurations
4. **Update Defaults**: Adjust project defaults if the change affects common scenarios

### Deprecating Categories

When categories are no longer needed:

1. **Identify Dependencies**: Find all configurations using the category
2. **Migration Path**: Provide replacement category recommendations
3. **Deprecation Notice**: Mark as deprecated with timeline
4. **Remove from Code**: Clean up after migration period

## Validation and Testing

### Automated Validation

```python
def validate_coverage_mappings(mappings: dict) -> bool:
    """Validate that all CDS scenarios are mapped to valid categories"""
    valid_categories = get_defined_categories()

    for scenario_id, category in mappings.items():
        if category not in valid_categories:
            raise ValueError(f"Invalid category '{category}' for scenario {scenario_id}")

    return True
```

### Coverage Logic Testing

```python
def test_category_resolution():
    """Test that CDS scenarios resolve to correct categories"""
    test_cases = [
        ("1.1.2", "treatment_recommendation"),
        ("1.1.5", "diagnostic_test"),
        ("2.1.1", "case_management"),
        ("3.2.1", "sdoh_integration")
    ]

    for scenario_id, expected_category in test_cases:
        resolved_category = resolve_scenario_category(scenario_id)
        assert resolved_category == expected_category, f"Expected {expected_category}, got {resolved_category}"
```

## Implementation Integration

### Service Layer Integration

```python
class CoverageMappingService:
    def __init__(self, mapping_config: dict):
        self.mappings = mapping_config

    def get_category_for_scenario(self, scenario_id: str) -> str:
        """Resolve CDS scenario ID to coverage category"""
        return self.mappings.get(scenario_id, "unknown")

    def get_scenarios_for_category(self, category: str) -> list:
        """Get all CDS scenarios that map to a category"""
        return [scenario for scenario, cat in self.mappings.items() if cat == category]
```

### Configuration Loading

```python
def load_coverage_mappings(config_path: str = None) -> dict:
    """Load CDS scenario to category mappings"""
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            return yaml.safe_load(f).get('scenario_mappings', {})

    # Return default mappings
    return get_default_scenario_mappings()
```

## Version History

- **1.0.0** (2025-11-08): Initial mapping reference with complete CDS scenario to category mappings</content>


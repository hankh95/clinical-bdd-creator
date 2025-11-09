# Project Coverage Defaults

**Version:** 1.0.0
**Date:** 2025-11-08
**Status:** Active

This configuration file defines the default coverage targets for the Clinical BDD Creator project. It uses the category-based mapping system to provide flexible, configurable coverage requirements.

## Configuration Overview

The project defaults establish baseline coverage expectations while allowing topic-specific and organization-specific overrides. This configuration replaces hardcoded scenario ID mappings with flexible category-based rules.

## Default Coverage Configuration

```yaml
# project-coverage-defaults.yaml
coverage_targets:
  # Overall strategy
  strategy: tiered
  default_tier: medium

  # Tier definitions with configurable parameters
  tier_definitions:
    none:
      description: "Skip scenario generation entirely"
      min_scenarios_per_category: 0
      max_scenarios_per_category: 0
      quality_threshold: 0.0
      use_case: "High-risk scenarios requiring specialist validation"

    low:
      description: "One high-value scenario per category"
      min_scenarios_per_category: 1
      max_scenarios_per_category: 3
      quality_threshold: 0.8
      use_case: "Basic coverage for stable, low-risk areas"

    medium:
      description: "Cover all recommendations with positive/safety cases"
      min_scenarios_per_category: 2
      max_scenarios_per_category: 5
      quality_threshold: 0.9
      use_case: "Standard coverage for most clinical workflows"

    high:
      description: "Multiple scenarios per recommendation including edge cases"
      min_scenarios_per_category: 3
      max_scenarios_per_category: 8
      quality_threshold: 0.95
      use_case: "Critical pathways requiring comprehensive validation"

    very_high:
      description: "Exhaustive coverage with all input/output combinations"
      min_scenarios_per_category: 5
      max_scenarios_per_category: 15
      quality_threshold: 0.98
      use_case: "Reserved for future use with guardrails"

  # Category to tier mappings (replaces hardcoded scenario IDs)
  category_mappings:
    # Core clinical decisions - highest priority
    treatment_recommendation: high
    drug_recommendation: high
    diagnostic_test: high

    # Specialized care - conditional coverage
    cancer_treatment: none        # Requires oncology specialist validation
    genetic_test: medium          # Specialized but stable requirements

    # Clinical workflow support - medium priority
    next_best_action: medium
    adverse_event_monitoring: medium
    drug_interaction: medium
    diagnostic_appropriateness: medium
    protocol_driven_care: medium
    quality_metrics: medium

    # Administrative and supportive - lower priority
    case_management: low
    risk_stratification: low
    documentation_support: low
    care_coordination: low
    patient_reminders: low
    lifestyle_education: low
    guideline_retrieval: low

    # Emerging and specialized areas - minimal coverage initially
    value_based_care: low
    public_health_reporting: low
    shared_decision_support: low
    sdoh_integration: low

  # Quality thresholds and validation rules
  quality_thresholds:
    completeness_score: 0.85
    clinical_accuracy: 0.95
    testability_score: 0.90
    min_scenario_complexity: 2    # Minimum Given/When/Then steps

  # Generation constraints
  generation_constraints:
    max_processing_time_minutes: 30
    max_scenarios_per_run: 100
    rate_limit_buffer: 0.8        # Use 80% of rate limit to avoid throttling

  # Reporting configuration
  reporting:
    include_category_breakdown: true
    include_quality_metrics: true
    include_gap_analysis: true
    report_format: "markdown"
    status_indicators:
      achieved: "✅"
      partial: "⚠️"
      failed: "❌"
```

## Category Rationale and Evolution

### High Priority Categories (Require Comprehensive Coverage)

| Category | Rationale | Evolution Notes |
|----------|-----------|-----------------|
| `treatment_recommendation` | Core clinical decisions affecting patient outcomes | Stable - fundamental to clinical care |
| `drug_recommendation` | Medication safety and efficacy decisions | May evolve with new drug classes |
| `diagnostic_test` | Test ordering and interpretation affecting diagnosis | Expands with new diagnostic technologies |

### Medium Priority Categories (Balanced Coverage)

| Category | Rationale | Evolution Notes |
|----------|-----------|-----------------|
| `next_best_action` | Sequential clinical decision support | Growing with care pathway standardization |
| `adverse_event_monitoring` | Patient safety surveillance | Critical for all care settings |
| `drug_interaction` | Medication safety checking | Essential for polypharmacy patients |
| `diagnostic_appropriateness` | Resource utilization optimization | Increasing focus on value-based care |
| `protocol_driven_care` | Standardized care delivery | Growing with clinical pathway development |
| `quality_metrics` | Performance measurement and improvement | Required for regulatory compliance |

### Low Priority Categories (Basic Coverage)

| Category | Rationale | Evolution Notes |
|----------|-----------|-----------------|
| `case_management` | Administrative care coordination | Stable administrative function |
| `risk_stratification` | Patient risk assessment | May grow with predictive analytics |
| `documentation_support` | Administrative efficiency | Stable administrative function |
| `care_coordination` | Team coordination support | May evolve with care team models |
| `patient_reminders` | Adherence and education support | May grow with patient engagement focus |
| `lifestyle_education` | Preventive care support | Growing with population health focus |
| `guideline_retrieval` | Knowledge access support | Stable reference function |

### Emerging Categories (Minimal Initial Coverage)

| Category | Rationale | Evolution Notes |
|----------|-----------|-----------------|
| `value_based_care` | Healthcare economics optimization | Emerging with payment reform |
| `public_health_reporting` | Population health surveillance | Growing with public health integration |
| `shared_decision_support` | Patient-centered care tools | Growing with patient engagement focus |
| `sdoh_integration` | Holistic patient care | Emerging focus on social determinants |

## Topic-Specific Overrides

### Cardiology Topic Example

```yaml
# cardiology-coverage-overrides.yaml
coverage_targets:
  overrides:
    rationale: "Cardiology requires enhanced monitoring and risk stratification"
    category_overrides:
      adverse_event_monitoring: high    # Increased from medium for cardiac medications
      risk_stratification: medium       # Increased from low for cardiac risk assessment
      diagnostic_test: high            # Already high, confirmed for cardiac diagnostics
    scenario_overrides:
      "1.1.4":                         # Cancer treatment in cardiology context
        tier: low
        reason: "Basic coverage for cardio-oncology cases"
```

### Emergency Department Example

```yaml
# ed-coverage-overrides.yaml
coverage_targets:
  overrides:
    rationale: "ED requires rapid decision support with high safety focus"
    category_overrides:
      treatment_recommendation: high
      diagnostic_test: high
      adverse_event_monitoring: high
      next_best_action: high
      risk_stratification: high
    generation_constraints:
      max_processing_time_minutes: 15  # Faster processing for ED use cases
```

### Primary Care Example

```yaml
# primary-care-coverage-overrides.yaml
coverage_targets:
  overrides:
    rationale: "Primary care emphasizes prevention and coordination"
    category_overrides:
      lifestyle_education: medium      # Increased from low for preventive care
      care_coordination: medium        # Increased from low for care management
      shared_decision_support: medium  # Increased from low for patient engagement
      sdoh_integration: medium         # Increased from low for holistic care
```

## Migration from Legacy Configuration

### Legacy Hardcoded Approach (Deprecated)

```yaml
# OLD APPROACH - DO NOT USE
coverage_targets:
  scenario_defaults:
    "1.1.2": "high"      # Treatment Recommendation
    "1.1.5": "high"      # Diagnostic Test Recommendation
    "1.1.4": "none"      # Cancer Treatment
    # ... 20+ hardcoded mappings
```

### New Category-Based Approach

```yaml
# NEW APPROACH - RECOMMENDED
coverage_targets:
  category_mappings:
    treatment_recommendation: high
    diagnostic_test: high
    cancer_treatment: none
    # Automatically applies to all scenarios in these categories
```

### Migration Benefits

1. **Reduced Maintenance**: Category mappings instead of individual scenario mappings
2. **Taxonomy Flexibility**: Add new scenarios without configuration changes
3. **Organizational Adaptation**: Different organizations can adjust category priorities
4. **Future-Proofing**: Configuration remains valid as taxonomy evolves

## Validation and Testing

### Configuration Validation

```python
def validate_coverage_config(config: dict) -> bool:
    """Validate coverage configuration structure and values"""
    required_keys = ['strategy', 'default_tier', 'tier_definitions', 'category_mappings']

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

    # Validate tier definitions
    for tier_name, tier_config in config['tier_definitions'].items():
        required_tier_keys = ['min_scenarios_per_category', 'quality_threshold']
        for tier_key in required_tier_keys:
            if tier_key not in tier_config:
                raise ValueError(f"Missing tier configuration: {tier_name}.{tier_key}")

    # Validate category mappings
    valid_tiers = set(config['tier_definitions'].keys())
    for category, tier in config['category_mappings'].items():
        if tier not in valid_tiers:
            raise ValueError(f"Invalid tier '{tier}' for category '{category}'")

    return True
```

### Coverage Achievement Testing

```python
def test_coverage_achievement():
    """Test that coverage requirements are properly calculated"""
    config = load_coverage_config('project-coverage-defaults.yaml')

    # Test category resolution
    assert config.get_tier_for_category('treatment_recommendation') == 'high'
    assert config.get_tier_for_category('lifestyle_education') == 'low'

    # Test tier requirements
    high_tier = config.get_tier_requirements('high')
    assert high_tier['min_scenarios_per_category'] == 3
    assert high_tier['quality_threshold'] == 0.95
```

## Implementation Notes

### Configuration Loading Priority

1. **System Defaults**: Built-in fallback configuration
2. **Project Defaults**: This file (`project-coverage-defaults.yaml`)
3. **Organization Overrides**: Organization-specific adjustments
4. **Topic Overrides**: Topic-specific requirements
5. **CLI Overrides**: Command-line parameters (highest priority)

### Performance Optimization

- **Caching**: Cache resolved category mappings to avoid repeated lookups
- **Lazy Loading**: Load tier definitions only when needed
- **Validation**: Validate configuration at startup to catch errors early

### Monitoring and Analytics

Track coverage effectiveness:

```python
def track_coverage_metrics():
    """Monitor coverage achievement across runs"""
    metrics = {
        'total_scenarios_generated': 0,
        'categories_covered': set(),
        'tier_achievement_rates': {},
        'quality_score_distribution': {},
        'processing_time_stats': {}
    }
    # Implementation tracks coverage effectiveness over time
```

## Version History

- **1.0.0** (2025-11-08): Initial project defaults configuration with category-based mappings</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/clinical-bdd-creator/project-coverage-defaults.yaml
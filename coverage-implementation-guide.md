# Coverage Implementation Guide# Coverage Implementation Guide



**Version:** 1.0.0**Version:** 1.0.0

**Date:** 2025-11-08**Date:** 2025-11-08

**Status:** Active**Status:** Active



This guide provides tool-specific implementation details for the Clinical BDD Creator coverage system. It adapts the tiered coverage approach for operational use while maintaining flexibility through configurable category mappings.This guide provides tool-specific implementation details for the Clinical BDD Creator coverage system. It adapts the tiered coverage approach for operational use while maintaining flexibility through configurable category mappings.



## Overview## Overview



The coverage system uses a tiered approach with configurable mappings to balance scenario quality, quantity, and resource constraints. This implementation guide provides the operational details for applying coverage targets in practice.The coverage system uses a tiered approach with configurable mappings to balance scenario quality, quantity, and resource constraints. This implementation guide provides the operational details for applying coverage targets in practice.



## Tier Definitions## Tier Definitions



Coverage tiers define the expected depth of scenario generation for different types of clinical decision support:Coverage tiers define the expected depth of scenario generation for different types of clinical decision support:



| Tier | Description | Min Scenarios | Quality Threshold | Use Case || Tier | Description | Min Scenarios | Quality Threshold | Use Case |

|------|-------------|---------------|-------------------|----------||------|-------------|---------------|-------------------|----------|

| none | Skip scenario generation entirely | 0 | N/A | High-risk scenarios requiring specialist validation || none | Skip scenario generation entirely | 0 | N/A | High-risk scenarios requiring specialist validation |

| low | One high-value scenario per category | 1 | ≥80% | Basic coverage for stable, low-risk areas || low | One high-value scenario per category | 1 | ≥80% | Basic coverage for stable, low-risk areas |

| medium | Cover all recommendations with positive/safety cases | 2 | ≥90% | Standard coverage for most clinical workflows || medium | Cover all recommendations with positive/safety cases | 2 | ≥90% | Standard coverage for most clinical workflows |

| high | Multiple scenarios per recommendation including edge cases | 3 | ≥95% | Critical pathways requiring comprehensive validation || high | Multiple scenarios per recommendation including edge cases | 3 | ≥95% | Critical pathways requiring comprehensive validation |

| very-high | Exhaustive coverage with all input/output combinations | 5+ | ≥98% | Reserved for future use with guardrails || very-high | Exhaustive coverage with all input/output combinations | 5+ | ≥98% | Reserved for future use with guardrails |



## Category-Based Coverage Mappings## Category-Based Coverage Mappings



Instead of hardcoded scenario IDs, coverage is applied through configurable category mappings:Instead of hardcoded scenario IDs, coverage is applied through configurable category mappings:



```yaml```yaml

# coverage-config.yaml# coverage-config.yaml

coverage_targets:coverage_targets:

  default_tier: medium  default_tier: medium

  category_mappings:  category_mappings:

    treatment_recommendation: high    treatment_recommendation: high

    diagnostic_test: high    diagnostic_test: high

    drug_recommendation: high    drug_recommendation: high

    cancer_treatment: none  # Requires specialist validation    cancer_treatment: none  # Requires specialist validation

    genetic_test: medium    genetic_test: medium

    next_best_action: medium    next_best_action: medium

    value_based_care: low    value_based_care: low

    lifestyle_education: low    lifestyle_education: low

    drug_interaction: medium    drug_interaction: medium

    diagnostic_appropriateness: medium    diagnostic_appropriateness: medium

    adverse_event_monitoring: medium    adverse_event_monitoring: medium

    case_management: low    case_management: low

    quality_metrics: medium    quality_metrics: medium

    risk_stratification: low    risk_stratification: low

    public_health_reporting: low    public_health_reporting: low

    shared_decision_support: low    shared_decision_support: low

    sdoh_integration: low    sdoh_integration: low

    patient_reminders: low    patient_reminders: low

    guideline_retrieval: low    guideline_retrieval: low

    protocol_driven_care: medium    protocol_driven_care: medium

    documentation_support: low    documentation_support: low

    care_coordination: low    care_coordination: low

``````



## Project Defaults by Category## Project Defaults by Category



| Category | Usage Scenario | Coverage Tier | Rationale || Category | Usage Scenario | Coverage Tier | Rationale |

|----------|----------------|---------------|-----------||----------|----------------|---------------|-----------|

| treatment_recommendation | Treatment Recommendation | high | Core clinical decisions requiring comprehensive coverage || treatment_recommendation | Treatment Recommendation | high | Core clinical decisions requiring comprehensive coverage |

| drug_recommendation | Drug Recommendation | high | Medication safety critical || drug_recommendation | Drug Recommendation | high | Medication safety critical |

| cancer_treatment | Cancer Treatment Recommendation | none | Requires oncology specialist validation || cancer_treatment | Cancer Treatment Recommendation | none | Requires oncology specialist validation |

| diagnostic_test | Diagnostic Test Recommendation | high | Critical for patient safety and outcomes || diagnostic_test | Diagnostic Test Recommendation | high | Critical for patient safety and outcomes |

| genetic_test | Genetic Test Recommendation | medium | Specialized but stable requirements || genetic_test | Genetic Test Recommendation | medium | Specialized but stable requirements |

| next_best_action | Next Best Action | medium | Important clinical workflow decisions || next_best_action | Next Best Action | medium | Important clinical workflow decisions |

| value_based_care | Value-Based Care Alerts | low | Emerging area, basic coverage sufficient || value_based_care | Value-Based Care Alerts | low | Emerging area, basic coverage sufficient |

| lifestyle_education | Lifestyle/Patient Education | low | Supplementary to core clinical decisions || lifestyle_education | Lifestyle/Patient Education | low | Supplementary to core clinical decisions |

| drug_interaction | Drug Interaction Checking | medium | Important safety checks || drug_interaction | Drug Interaction Checking | medium | Important safety checks |

| diagnostic_appropriateness | Diagnostic Test Appropriateness Check | medium | Resource utilization impact || diagnostic_appropriateness | Diagnostic Test Appropriateness Check | medium | Resource utilization impact |

| adverse_event_monitoring | Adverse Event Monitoring | medium | Patient safety monitoring || adverse_event_monitoring | Adverse Event Monitoring | medium | Patient safety monitoring |

| case_management | Case Management | low | Administrative workflow support || case_management | Case Management | low | Administrative workflow support |

| quality_metrics | Quality Metrics Reporting | medium | Performance measurement requirements || quality_metrics | Quality Metrics Reporting | medium | Performance measurement requirements |

| risk_stratification | Risk Stratification | low | Assessment support || risk_stratification | Risk Stratification | low | Assessment support |

| public_health_reporting | Public Health Reporting | low | Population-level requirements || public_health_reporting | Public Health Reporting | low | Population-level requirements |

| shared_decision_support | Shared Decision-Making Support | low | Emerging patient engagement || shared_decision_support | Shared Decision-Making Support | low | Emerging patient engagement |

| sdoh_integration | SDOH Integration | low | Social determinants still evolving || sdoh_integration | SDOH Integration | low | Social determinants still evolving |

| patient_reminders | Patient Education and Reminders | low | Supplementary communications || patient_reminders | Patient Education and Reminders | low | Supplementary communications |

| guideline_retrieval | Guideline-Driven Information Retrieval | low | Reference support || guideline_retrieval | Guideline-Driven Information Retrieval | low | Reference support |

| protocol_driven_care | Protocol-Driven Care | medium | Structured clinical pathways || protocol_driven_care | Protocol-Driven Care | medium | Structured clinical pathways |

| documentation_support | Documentation Support | low | Administrative support || documentation_support | Documentation Support | low | Administrative support |

| care_coordination | Care Coordination Alerts | low | Workflow coordination || care_coordination | Care Coordination Alerts | low | Workflow coordination |



## Topic-Level Overrides## Topic-Level Overrides



For specific topics requiring different coverage levels, create override files:For specific topics requiring different coverage levels, create override files:



```yaml```yaml

# generated/<org>_<topic>/<tool>/runs/<runId>/artifacts/coverage_overrides.yaml```

coverage_overrides:

  rationale: "Cardiology topic requires enhanced monitoring coverage due to complexity"## CLI Integration

  category_overrides:

    adverse_event_monitoring: high  # Increased from medium### Basic Usage

    risk_stratification: medium     # Increased from low

  scenario_overrides:```bash

    "1.1.4":                         # Specific scenario override# Use project defaults

      tier: lowdoppler run --project fishnet-automation --config stg -- \

      reason: "Basic cancer treatment coverage for this topic"  python3 -m bdd_fishnet.scripts.generate_qa <topic>

```

# Override coverage tier for all categories

## CLI Integrationdoppler run --project fishnet-automation --config stg -- \

  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-tier low

### Basic Usage

# Use custom coverage configuration

```bashdoppler run --project fishnet-automation --config stg -- \

# Use project defaults  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-config /path/to/config.yaml

doppler run --project fishnet-automation --config stg -- \```

  python3 -m bdd_fishnet.scripts.generate_qa <topic>

### Configuration File Format

# Override coverage tier for all categories

doppler run --project fishnet-automation --config stg -- \```yaml

  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-tier low# coverage-config.yaml

strategy: tiered

# Use custom coverage configurationdefault_tier: medium

doppler run --project fishnet-automation --config stg -- \category_mappings:

  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-config /path/to/config.yaml  treatment_recommendation: high

```  diagnostic_test: high

overrides:

### Configuration File Format  rationale: "Emergency department requirements"

  category_overrides:

```yaml    adverse_event_monitoring: high

# coverage-config.yaml```

strategy: tiered```

default_tier: medium

category_mappings:## CLI Integration

  treatment_recommendation: high

  diagnostic_test: high

overrides:### Basic Usage

  rationale: "Emergency department requirements"```bash

  category_overrides:# Use project defaults

    adverse_event_monitoring: highdoppler run --project fishnet-automation --config stg -- \

```  python3 -m bdd_fishnet.scripts.generate_qa <topic>



## Reporting Expectations# Override coverage tier for all categories

doppler run --project fishnet-automation --config stg -- \

Coverage reports must include category-based analysis:  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-tier low



### Required Report Structure# Use custom coverage configuration

doppler run --project fishnet-automation --config stg -- \

| Category | Usage Scenario | Target Tier | Required Min | Generated | Status | Notes |  python3 -m bdd_fishnet.scripts.generate_qa <topic> --coverage-config /path/to/config.yaml

|----------|----------------|-------------|--------------|-----------|--------|-------|```

| treatment_recommendation | Treatment Recommendation | high | ≥3 | 5 | ✅ | Comprehensive coverage achieved |

| diagnostic_test | Diagnostic Test Recommendation | high | ≥3 | 2 | ⚠️ | Missing cardiac enzyme scenarios |

| drug_interaction | Drug Interaction Checking | medium | ≥2 | 0 | ❌ | No drug interaction content found |### Configuration File Format

```yaml

### Status Indicators# coverage-config.yaml

strategy: tiered

- ✅ **Achieved**: Meets or exceeds minimum requirementsdefault_tier: medium

- ⚠️ **Partial**: Below target but minimum metcategory_mappings:

- ❌ **Failed**: Below minimum requirements  treatment_recommendation: high

  diagnostic_test: high

### Coverage Gap Analysisoverrides:

  rationale: "Emergency department requirements"

Reports should identify gaps and provide actionable recommendations:  category_overrides:

    adverse_event_monitoring: high

```markdown```

## Coverage Gaps Identified

## Reporting Expectations

### Missing Categories

- **protocol_driven_care**: No protocol-driven care content found in guidelinesCoverage reports must include category-based analysis:

- **care_coordination**: Limited care coordination requirements identified



### Under-Covered Categories### Required Report Structure

- **diagnostic_test**: Missing specialized test scenarios (genetic, advanced imaging)

- **adverse_event_monitoring**: Limited monitoring scenarios for high-risk medications| Category | Usage Scenario | Target Tier | Required Min | Generated | Status | Notes |

|----------|----------------|-------------|--------------|-----------|--------|-------|

### Recommendations| treatment_recommendation | Treatment Recommendation | high | ≥3 | 5 | ✅ | Comprehensive coverage achieved |

1. Review guideline content for protocol-driven care elements| diagnostic_test | Diagnostic Test Recommendation | high | ≥3 | 2 | ⚠️ | Missing cardiac enzyme scenarios |

2. Add specialized diagnostic test scenarios for comprehensive coverage| drug_interaction | Drug Interaction Checking | medium | ≥2 | 0 | ❌ | No drug interaction content found |

3. Enhance adverse event monitoring for critical medication classes

```

### Status Indicators

## Implementation Workflow- ✅ **Achieved**: Meets or exceeds minimum requirements

- ⚠️ **Partial**: Below target but minimum met

### 1. Configuration Loading- ❌ **Failed**: Below minimum requirements



```python

def load_coverage_config(topic_id: str) -> CoverageConfig:### Coverage Gap Analysis

    """Load coverage configuration with fallback hierarchy"""

    # 1. Topic-specific overridesReports should identify gaps and provide actionable recommendations:

    topic_config = load_topic_overrides(topic_id)

```markdown

    # 2. Project defaults## Coverage Gaps Identified

    project_config = load_project_defaults()



    # 3. System defaults### Missing Categories

    system_config = load_system_defaults()- **protocol_driven_care**: No protocol-driven care content found in guidelines

- **care_coordination**: Limited care coordination requirements identified

    # Merge with override precedence

    return merge_configs(system_config, project_config, topic_config)

```### Under-Covered Categories

- **diagnostic_test**: Missing specialized test scenarios (genetic, advanced imaging)

### 2. Category Mapping Application- **adverse_event_monitoring**: Limited monitoring scenarios for high-risk medications



```python

def apply_coverage_targets(guideline_content: dict, config: CoverageConfig) -> dict:### Recommendations

    """Apply coverage targets based on content analysis"""1. Review guideline content for protocol-driven care elements

    categories_found = analyze_content_categories(guideline_content)2. Add specialized diagnostic test scenarios for comprehensive coverage

3. Enhance adverse event monitoring for critical medication classes

    coverage_plan = {}```

    for category in categories_found:

        tier = config.get_tier_for_category(category)## Implementation Workflow

        coverage_plan[category] = {

            'tier': tier,

            'min_scenarios': config.get_min_scenarios(tier),### 1. Configuration Loading

            'quality_threshold': config.get_quality_threshold(tier)```python

        }def load_coverage_config(topic_id: str) -> CoverageConfig:

    """Load coverage configuration with fallback hierarchy"""

    return coverage_plan    # 1. Topic-specific overrides

```    topic_config = load_topic_overrides(topic_id)



### 3. Scenario Generation with Coverage Tracking    # 2. Project defaults

    project_config = load_project_defaults()

```python

def generate_scenarios_with_coverage_tracking(content: dict, plan: dict) -> dict:    # 3. System defaults

    """Generate scenarios while tracking coverage achievement"""    system_config = load_system_defaults()

    results = {'scenarios': [], 'coverage_report': {}}

    # Merge with override precedence

    for category, requirements in plan.items():    return merge_configs(system_config, project_config, topic_config)

        category_scenarios = generate_category_scenarios(content, category, requirements)```

        results['scenarios'].extend(category_scenarios)



        # Track coverage achievement### 2. Category Mapping Application

        results['coverage_report'][category] = {```python

            'target_tier': requirements['tier'],def apply_coverage_targets(guideline_content: dict, config: CoverageConfig) -> dict:

            'required_min': requirements['min_scenarios'],    """Apply coverage targets based on content analysis"""

            'generated': len(category_scenarios),    categories_found = analyze_content_categories(guideline_content)

            'status': calculate_status(len(category_scenarios), requirements)

        }    coverage_plan = {}

    for category in categories_found:

    return results        tier = config.get_tier_for_category(category)

```        coverage_plan[category] = {

            'tier': tier,

## Quality Assurance            'min_scenarios': config.get_min_scenarios(tier),

            'quality_threshold': config.get_quality_threshold(tier)

### Automated Validation        }



- **Tier Compliance**: Verify generated scenarios meet tier requirements    return coverage_plan

- **Quality Thresholds**: Validate scenarios against quality metrics```

- **Category Coverage**: Ensure all identified categories are addressed



### Manual Review Triggers### 3. Scenario Generation with Coverage Tracking

```python

- Coverage gaps in high-tier categoriesdef generate_scenarios_with_coverage_tracking(content: dict, plan: dict) -> dict:

- Quality scores below thresholds    """Generate scenarios while tracking coverage achievement"""

- Unexpected category absences    results = {'scenarios': [], 'coverage_report': {}}



## Performance Considerations    for category, requirements in plan.items():

        category_scenarios = generate_category_scenarios(content, category, requirements)

### Resource Allocation by Tier        results['scenarios'].extend(category_scenarios)



- **low/medium**: Standard model usage, normal processing time        # Track coverage achievement

- **high**: Increased model usage, longer processing time        results['coverage_report'][category] = {

- **very-high**: Reserved for future use with resource guardrails            'target_tier': requirements['tier'],

            'required_min': requirements['min_scenarios'],

### Optimization Strategies            'generated': len(category_scenarios),

            'status': calculate_status(len(category_scenarios), requirements)

- **Parallel Processing**: Generate scenarios by category in parallel        }

- **Caching**: Cache category analysis results

- **Incremental Updates**: Only regenerate changed categories    return results

```

## Troubleshooting

## Quality Assurance

### Common Issues



**No scenarios generated for category:**### Automated Validation

- Check if category content exists in guidelines- **Tier Compliance**: Verify generated scenarios meet tier requirements

- Verify category mapping configuration- **Quality Thresholds**: Validate scenarios against quality metrics

- Review content analysis logic- **Category Coverage**: Ensure all identified categories are addressed



**Quality scores below threshold:**

- Adjust model parameters for category### Manual Review Triggers

- Review scenario generation prompts- Coverage gaps in high-tier categories

- Consider tier adjustment for difficult categories- Quality scores below thresholds

- Unexpected category absences

**Processing timeouts:**

- Reduce high-tier category scope## Performance Considerations

- Implement category processing limits

- Use parallel processing where possible

### Resource Allocation by Tier

### Diagnostic Commands- **low/medium**: Standard model usage, normal processing time

- **high**: Increased model usage, longer processing time

```bash- **very-high**: Reserved for future use with resource guardrails

# Analyze content categories

python3 -m bdd_fishnet.scripts.analyze_categories <topic>

### Optimization Strategies

# Validate coverage configuration- **Parallel Processing**: Generate scenarios by category in parallel

python3 -m bdd_fishnet.scripts.validate_coverage_config <config_file>- **Caching**: Cache category analysis results

- **Incremental Updates**: Only regenerate changed categories

# Generate coverage report for existing scenarios

python3 -m bdd_fishnet.scripts.coverage_report <topic> <scenario_dir>## Troubleshooting

```



## Version History### Common Issues



- **1.0.0** (2025-11-08): Initial implementation guide with category-based coverage system</content>**No scenarios generated for category:**

<parameter name="filePath">/Users/hankhead/Projects/Personal/clinical-bdd-creator/coverage-implementation-guide.md- Check if category content exists in guidelines
- Verify category mapping configuration
- Review content analysis logic

**Quality scores below threshold:**
- Adjust model parameters for category
- Review scenario generation prompts
- Consider tier adjustment for difficult categories

**Processing timeouts:**
- Reduce high-tier category scope
- Implement category processing limits
- Use parallel processing where possible


### Diagnostic Commands
```bash
# Analyze content categories
python3 -m bdd_fishnet.scripts.analyze_categories <topic>

# Validate coverage configuration
python3 -m bdd_fishnet.scripts.validate_coverage_config <config_file>

# Generate coverage report for existing scenarios
python3 -m bdd_fishnet.scripts.coverage_report <topic> <scenario_dir>
```

## Version History

- **1.0.0** (2025-11-08): Initial implementation guide with category-based coverage system</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/clinical-bdd-creator/coverage-implementation-guide.md
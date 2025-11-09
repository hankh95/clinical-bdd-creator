# Service Configuration Parameters Guide

**Version:** 1.0.0
**Date:** 2025-11-08
**Status:** Active

This document provides detailed guidance for the four key configurable concepts that should be specifiable when calling the Clinical BDD Creator MCP service.

## Overview

The Clinical BDD Creator service supports four primary configuration parameters that control how clinical guideline content is processed and transformed into BDD test scenarios:

1. **Coverage Targets** - Define the scope and depth of scenario generation
2. **Sections to be Processed** - Specify which clinical guideline sections to analyze
3. **Fidelity Level** - Control the detail and completeness of generated outputs
4. **Generation Mode** - Select the strategy for creating test scenarios

## 1. Coverage Targets

Coverage targets define the scope, depth, and quality thresholds for scenario generation across clinical domains. The system supports multiple coverage strategies to balance quality, quantity, and resource constraints.

### Coverage Target Configuration

```json
{
  "coverage_targets": {
    "strategy": "tiered",
    "default_tier": "medium",
    "tier_definitions": {
      "low": {
        "description": "Minimum viable coverage - one high-value scenario per category",
        "min_scenarios_per_category": 1,
        "max_scenarios_per_category": 3,
        "quality_threshold": 0.8
      },
      "medium": {
        "description": "Balanced coverage - cover all recommendations with positive and safety cases",
        "min_scenarios_per_category": 2,
        "max_scenarios_per_category": 5,
        "quality_threshold": 0.9
      },
      "high": {
        "description": "Comprehensive coverage - multiple scenarios per recommendation including edge cases",
        "min_scenarios_per_category": 3,
        "max_scenarios_per_category": 8,
        "quality_threshold": 0.95
      },
      "very_high": {
        "description": "Exhaustive coverage - all input/output combinations with guardrails",
        "min_scenarios_per_category": 5,
        "max_scenarios_per_category": 15,
        "quality_threshold": 0.98
      }
    },
    "category_mappings": {
      "assessment": "medium",
      "treatment": "high",
      "diagnostic_test": "high",
      "monitoring": "medium",
      "education": "low",
      "referral": "medium"
    },
    "scenario_overrides": {
      "1.1.4": {"tier": "none", "reason": "Requires specialist validation"},
      "3.2.1": {"tier": "low", "reason": "Still evolving"}
    },
    "quality_thresholds": {
      "completeness_score": 0.85,
      "clinical_accuracy": 0.95,
      "testability_score": 0.90
    }
  }
}
```

### Alternative Coverage Strategies

**Count-Based Strategy:**

```json
{
  "coverage_targets": {
    "strategy": "count-based",
    "scenario_counts": {
      "total_minimum": 10,
      "total_target": 25,
      "per_category_minimum": {
        "treatment": 3,
        "diagnostic": 2,
        "monitoring": 2
      }
    }
  }
}
```

**Quality-Based Strategy:**

```json
{
  "coverage_targets": {
    "strategy": "quality-based",
    "quality_gates": {
      "min_coverage_score": 0.9,
      "min_clinical_fidelity": 0.95,
      "max_generation_time_minutes": 30
    }
  }
}
```

### Coverage Target Usage Examples

- **Conservative Coverage**: Use `low` tier for initial prototyping with minimal resource usage
- **Balanced Coverage**: Use `medium` tier for development testing with good clinical representation
- **Comprehensive Coverage**: Use `high` tier for production validation with extensive edge case coverage
- **Specialized Coverage**: Use scenario overrides for domain-specific requirements (e.g., skip cancer treatments requiring specialist validation)

### Coverage Target Impact on Generation

- **Strategy Selection**: Determines whether to use tiered, count-based, or quality-based approaches
- **Tier Definitions**: Configurable coverage levels allow organizations to define their own quality/quantity balance
- **Category Mappings**: Maps clinical categories to appropriate coverage levels based on risk and complexity
- **Scenario Overrides**: Allows fine-grained control for specific scenarios that need different treatment
- **Quality Thresholds**: Ensures generated scenarios meet minimum standards for clinical accuracy and completeness

## 2. Sections to be Processed

Specify which sections of clinical guidelines should be analyzed for scenario generation.

### Section Processing Configuration

```json
{
  "sections_to_process": {
    "include_sections": [
      "clinical_assessment",
      "diagnostic_criteria",
      "treatment_recommendations",
      "monitoring_requirements",
      "patient_education",
      "follow_up_care"
    ],
    "exclude_sections": [
      "references",
      "acknowledgments",
      "appendices"
    ],
    "section_priority": {
      "high": ["treatment_recommendations", "diagnostic_criteria"],
      "medium": ["clinical_assessment", "monitoring_requirements"],
      "low": ["patient_education", "follow_up_care"]
    },
    "content_filters": {
      "min_paragraph_length": 50,
      "max_section_depth": 3,
      "required_keywords": ["should", "must", "recommend"]
    }
  }
}
```

### Section Processing Usage Examples

- **Core Clinical Logic**: Focus on assessment, diagnosis, and treatment sections
- **Patient-Focused**: Include education and follow-up sections
- **Technical Validation**: Target monitoring and implementation sections

### Section Processing Impact on Generation

- Controls which parts of guidelines are analyzed
- Affects the types of clinical decisions captured
- Influences scenario relevance and applicability

## 3. Fidelity Level

Control the depth and completeness of generated artifacts and outputs.

### Fidelity Level Configuration

```json
{
  "fidelity_level": "full"
}
```

### Supported Levels

| Level | Description | Outputs | Use Case |
|-------|-------------|---------|----------|
| `none` | Skip generation | Empty results | Testing pipeline only |
| `draft` | Basic inventory | JSON/Markdown tables | Quick assessment |
| `full` | Complete scenarios | Feature files + inventory | Development testing |
| `full-fhir` | FHIR resources | All above + FHIR artifacts | Production integration |

### Fidelity Level Usage Examples

- **Draft**: Rapid prototyping and requirement validation
- **Full**: Complete test suite generation for development
- **Full-FHIR**: Production-ready artifacts with clinical system integration

### Fidelity Level Impact on Generation

- Determines output format and completeness
- Affects processing time and resource usage
- Controls integration capabilities

## 4. Generation Mode

Select the strategy and approach for creating BDD test scenarios.

### Generation Mode Configuration

```json
{
  "generation_mode": "top-down,bottom-up"
}
```

### Supported Modes

| Mode | Description | Best For | Complexity |
|------|-------------|----------|------------|
| `top-down` | Start with clinical goals, derive specific scenarios | High-level requirements | Medium |
| `bottom-up` | Start with specific guideline content, build up scenarios | Detailed specifications | Low |
| `external` | Use external knowledge and clinical reasoning | Complex decision trees | High |
| `logic-derived` | Extract from conditional logic and decision points | Structured guidelines | Medium |

### Generation Mode Usage Examples

- **Single Mode**: `top-down` for requirement-driven generation
- **Combined Modes**: `top-down,bottom-up` for comprehensive coverage
- **Specialized**: `logic-derived` for highly structured clinical pathways

### Generation Mode Impact on Generation

- Influences scenario structure and approach
- Affects clinical reasoning patterns captured
- Determines scenario variety and completeness

## API Integration

### MCP Tool Signature

```typescript
generate_scenarios(
  topic_id: string,
  mode: string,           // Comma-separated generation modes
  sections: string[],     // Array of section identifiers
  fidelity: string,       // One of: none|draft|full|full-fhir
  provider: string,       // AI provider (optional)
  model: string,          // Model name (optional)
  coverage_targets?: object // Coverage configuration (optional)
): Promise<ScenarioResult>
```

### Configuration File Format

```yaml
# clinical-bdd-config.yaml
service:
  coverage_targets:
    cds_categories: ["assessment", "order", "monitor"]
    scenario_count_per_category:
      target: 5
  sections_to_process:
    include_sections: ["treatment_recommendations", "diagnostic_criteria"]
    section_priority:
      high: ["treatment_recommendations"]
  fidelity_level: "full"
  generation_mode: "top-down,bottom-up"
```

## Best Practices

### Parameter Selection Guidelines

1. **Start Simple**: Begin with `fidelity: "draft"` and `mode: "top-down"` for initial exploration
2. **Scale Up**: Progress to `fidelity: "full"` and multiple modes for comprehensive coverage
3. **Domain-Specific**: Adjust sections and coverage targets based on clinical specialty
4. **Resource-Aware**: Use lower fidelity levels for large guideline sets

### Validation Recommendations

- Always validate configuration parameters before large generation runs
- Use dry-run mode to test parameter combinations
- Monitor coverage metrics to ensure adequate scenario generation
- Review generated scenarios for clinical accuracy and completeness

### Performance Considerations

- Higher fidelity levels require more processing time
- Multiple generation modes increase scenario diversity but also processing time
- Section filtering can significantly reduce processing scope
- Coverage targets help balance quality vs. quantity trade-offs

## Troubleshooting

### Common Issues

- **No scenarios generated**: Check section filters and coverage targets
- **Low quality scenarios**: Increase fidelity level or adjust generation modes
- **Missing clinical domains**: Add relevant CDS categories to coverage targets
- **Processing timeouts**: Reduce sections processed or use draft fidelity

### Diagnostic Steps

1. Enable dry-run mode to validate configuration
2. Check section availability in source guidelines
3. Review coverage target settings for realism
4. Monitor generation logs for mode-specific issues

## Version History

- **1.0.0** (2025-11-08): Initial release with complete parameter guidance

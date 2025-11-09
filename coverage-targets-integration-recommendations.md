# Coverage Targets Integration Recommendations

**Date:** 2025-11-08
**Status:** Review Required

## Analysis of Current Coverage Targets Document

Your coverage targets document provides excellent operational detail but creates tight coupling between the service API and your specific usage scenario taxonomy. Here are my recommendations for integration:

## Key Concerns Identified

### 1. Tight Coupling to Usage Scenarios

- The document assumes a specific CDS scenario numbering system (1.1.1, 1.1.2, etc.)
- Project defaults are hardcoded to your current usage scenario list
- Changes to usage scenarios would require updates to this reference

### 2. Operational vs. API Design

- The document mixes high-level API concepts with implementation details
- CLI integration and file paths are implementation-specific
- Reporting expectations are tool-specific rather than API-contract focused

### 3. Limited Flexibility

- Tier definitions are fixed rather than configurable
- No support for custom coverage rules per organization
- Hardcoded assumption about which scenarios need "high" vs "medium" coverage

## Recommended Integration Approach

### Phase 1: Separate API from Implementation

**Keep in Service Configuration Guide (API Level):**

```json
{
  "coverage_targets": {
    "strategy": "tiered",
    "tiers": {
      "low": {"min_scenarios_per_category": 1},
      "medium": {"min_scenarios_per_category": 2},
      "high": {"min_scenarios_per_category": 3}
    },
    "category_mappings": {
      "assessment": "medium",
      "treatment": "high",
      "monitoring": "medium"
    },
    "overrides": {
      "1.1.2": "high",
      "2.1.1": "low"
    }
  }
}
```

**Move to Implementation Guide (Tool-Specific):**

- Your detailed tier definitions and project defaults
- CLI integration specifics
- File path conventions
- Reporting formats

### Phase 2: Make Coverage More Configurable

**Recommended Structure:**

```json
{
  "coverage_targets": {
    "default_tier": "medium",
    "tier_definitions": {
      "low": {
        "description": "One high-value scenario per category",
        "min_scenarios": 1,
        "max_scenarios": 3
      },
      "medium": {
        "description": "Cover all recommendations with positive/safety cases",
        "min_scenarios": 2,
        "max_scenarios": 5
      },
      "high": {
        "description": "Two distinct scenarios per recommendation",
        "min_scenarios": 3,
        "max_scenarios": 8
      }
    },
    "category_defaults": {
      "treatment_recommendation": "high",
      "diagnostic_test": "medium",
      "monitoring": "medium"
    },
    "scenario_overrides": {
      "1.1.4": {"tier": "none", "reason": "Cancer treatments require specialist validation"},
      "3.2.1": {"tier": "low", "reason": "SDOH integration still evolving"}
    }
  }
}
```

### Phase 3: Create Mapping Layer

**Add a Coverage Mapping Document:**

- Maps your CDS scenario IDs to configurable categories
- Allows reorganization without breaking the API
- Supports multiple taxonomy systems

```markdown
# Coverage Category Mappings

| CDS Scenario | Usage Scenario | Category | Rationale |
|--------------|----------------|----------|-----------|
| 1.1.2 | Treatment Recommendation | treatment_recommendation | Core clinical decision |
| 1.1.5 | Diagnostic Test Recommendation | diagnostic_test | Critical for patient safety |
```

## Specific Recommendations for Your Document

### ✅ Keep These Sections

- **Tier Definitions**: Excellent operational clarity
- **Project Defaults Table**: Valuable for consistency
- **Reporting Expectations**: Good operational guidance

### 🔄 Modify These Sections

- **CLI Integration**: Move to implementation guide
- **Topic Overrides**: Make more flexible (allow category-based overrides)
- **File Paths**: Make configurable rather than hardcoded

### ❌ Remove/Relocate

- **Hardcoded CDS Scenario Numbers**: Replace with category mappings
- **Implementation Details**: Move to separate implementation guide

## Proposed Document Structure

### 1. Service Configuration Guide (API Contract)

- Generic coverage target configuration
- JSON schema definitions
- Usage examples

### 2. Coverage Implementation Guide (Your Document)

- Specific to your usage scenario system
- Tool-specific integration details
- Project-specific defaults and overrides

### 3. Coverage Mapping Reference

- Maps CDS scenarios to configurable categories
- Allows taxonomy evolution
- Supports multiple classification systems

## Benefits of This Approach

1. **API Stability**: Service interface remains stable even if taxonomy changes
2. **Implementation Flexibility**: Tools can adapt coverage logic without API changes
3. **Multi-System Support**: Same API can work with different usage scenario taxonomies
4. **Operational Clarity**: Your detailed operational guidance is preserved

## Next Steps

1. **Update Service Config Guide**: Add the configurable tier system
2. **Create Implementation Guide**: Adapt your document for tool-specific details
3. **Add Mapping Layer**: Create category mapping system
4. **Validate Integration**: Test that the layered approach works for your use cases

Would you like me to implement these changes to create the recommended document structure?</content>


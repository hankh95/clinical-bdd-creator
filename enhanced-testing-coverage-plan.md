# Enhanced Testing Coverage and Fidelity Levels - Implementation Plan

**Date:** November 9, 2025
**Status:** Implementation Plan
**Priority:** High

## Executive Summary

Current UAT testing achieved 100% success rate across only 3 clinical domains (cardiology, diabetes, oncology) and 4 basic CDS categories. This plan expands testing to cover all 23 CDS usage scenario categories with new fidelity levels focused on evaluation and coverage analysis rather than just generation.

## Current State Analysis

### ✅ What's Working
- **100% success rate** on 5 clinical scenarios
- **Core generation pipeline** (CIKG → BDD → MCP) functioning correctly
- **4 fidelity levels** implemented: none, draft, full, full-fhir
- **Production deployment** infrastructure ready

### ❌ Critical Gaps Identified

1. **Limited Category Coverage**: Only 4/23 CDS usage scenarios tested
   - Currently tested: treatment_recommendation, drug_recommendation, diagnostic_test, cancer_treatment
   - Missing: 19 categories including drug_interaction, adverse_event_monitoring, differential_diagnosis, etc.

2. **Generation-Focused Fidelity**: Current fidelity levels focus on output generation, not evaluation
   - No way to assess scenario robustness against guidelines
   - No coverage analysis vs usage scenarios
   - No sequential processing for gap analysis

3. **Provider CDS Bias**: Current testing focused on provider-centric CDS, missing patient-centered and population-based scenarios

## Enhanced Fidelity Levels - New Design

### Current Fidelity Levels (Generation-Focused)
- `none` - Skip generation
- `draft` - Basic inventory tables
- `full` - Full Gherkin features
- `full-fhir` - Features + FHIR resources

### New Fidelity Levels (Evaluation-Focused)

#### `evaluation-only` - Robustness Assessment
**Purpose:** Analyze guideline content against CDS usage scenarios and return match strength assessment
**Output:** JSON table showing scenario-to-guideline robustness scores
**Use Case:** Pre-generation evaluation to identify coverage gaps
**Success Criteria:** ≥85% coverage analysis accuracy

#### `table` - Enhanced Inventory with Match Scores
**Purpose:** Generate scenario inventory with strength-of-match scores for each CDS category
**Output:** JSON/Markdown tables with 15 metadata fields + match strength scores
**Use Case:** Coverage analysis and prioritization
**Success Criteria:** ≥95% field completion + valid match scores

#### `sequential` - Gap-Filling Coverage Analysis
**Purpose:** Process CDS categories sequentially, analyzing gaps and generating targeted scenarios
**Output:** Coverage analysis report + targeted scenario generation for under-represented categories
**Use Case:** Comprehensive coverage assurance
**Success Criteria:** ≥80% gap analysis accuracy, targeted scenario generation

## Expanded Testing Categories

### Current Coverage: 4/23 Categories Tested ✅
- ✅ treatment_recommendation (1.1.2)
- ✅ drug_recommendation (1.1.3)
- ✅ diagnostic_test (1.1.5)
- ✅ cancer_treatment (1.1.4)

### Missing Categories Requiring Testing ❌

#### High Priority (Safety Critical)
- ❌ differential_diagnosis (1.1.1) - Core diagnostic workflow
- ❌ drug_interaction (1.2.1) - Safety guardrail
- ❌ adverse_event_monitoring (1.2.3) - Safety monitoring
- ❌ diagnostic_appropriateness (1.2.2) - Safety validation

#### Medium Priority (Workflow Support)
- ❌ next_best_action (1.1.7) - Task prioritization
- ❌ lifestyle_education (1.1.9) - Behavior change
- ❌ value_based_care (1.1.8) - Quality gap closure
- ❌ protocol_driven_care (4.2.1) - Workflow automation
- ❌ quality_metrics (2.2.1) - Performance tracking

#### Low Priority (Administrative)
- ❌ case_management (2.1.1) - Population oversight
- ❌ risk_stratification (2.3.1) - Predictive analytics
- ❌ documentation_support (4.3.1) - Compliance templates
- ❌ care_coordination (4.4.1) - Transition alerts
- ❌ patient_reminders (3.3.1) - Engagement
- ❌ guideline_retrieval (4.1.1) - Knowledge lookup
- ❌ shared_decision_support (3.1.1) - Collaborative planning
- ❌ sdoh_integration (3.2.1) - Social context
- ❌ public_health_reporting (2.4.1) - Regulatory reporting

## Implementation Roadmap

### Phase 1: Enhanced Fidelity Levels (Week 1)
1. **Implement `evaluation-only` mode**
   - Add robustness assessment algorithm
   - Create scenario-to-guideline matching logic
   - Generate coverage analysis reports

2. **Implement `table` mode**
   - Extend inventory generation with match scores
   - Add strength-of-match calculations
   - Validate metadata field completion

3. **Implement `sequential` mode**
   - Add sequential category processing
   - Implement gap analysis algorithms
   - Create targeted scenario generation

### Phase 2: Expanded Category Testing (Week 2)
1. **High Priority Categories (4 categories)**
   - differential_diagnosis, drug_interaction, adverse_event_monitoring, diagnostic_appropriateness
   - Target: 100% coverage with all fidelity levels

2. **Medium Priority Categories (5 categories)**
   - next_best_action, lifestyle_education, value_based_care, protocol_driven_care, quality_metrics
   - Target: evaluation-only and table mode coverage

3. **Low Priority Categories (9 categories)**
   - Administrative and emerging categories
   - Target: evaluation-only assessment

### Phase 3: Comprehensive Validation (Week 3)
1. **Cross-Domain Testing**
   - Test each category across multiple clinical domains
   - Validate robustness assessment accuracy
   - Measure coverage analysis effectiveness

2. **Performance Benchmarking**
   - Compare old vs new fidelity level performance
   - Validate sequential processing efficiency
   - Assess coverage gap analysis accuracy

## Success Metrics

### Coverage Metrics
- **Category Coverage:** 23/23 CDS usage scenarios (100% vs current 4/23 = 17%)
- **Fidelity Coverage:** 7/7 fidelity levels implemented and tested
- **Domain Coverage:** Test each category across ≥3 clinical domains

### Quality Metrics
- **Evaluation Accuracy:** ≥85% for robustness assessments
- **Gap Analysis:** ≥80% accuracy in identifying coverage gaps
- **Metadata Completeness:** ≥95% field completion in table mode

### Performance Metrics
- **Sequential Processing:** <2x single category processing time
- **Evaluation-Only:** <30 seconds per guideline
- **Memory Usage:** <500MB for comprehensive analysis

## Risk Mitigation

### Technical Risks
- **Algorithm Accuracy:** Implement validation against human expert assessments
- **Performance Impact:** Add performance monitoring and optimization
- **Integration Complexity:** Maintain backward compatibility with existing API

### Operational Risks
- **Increased Test Time:** Parallel processing for large test suites
- **Result Complexity:** Enhanced reporting and visualization
- **User Training:** Documentation and examples for new fidelity levels

## User Experience Considerations

### For Clinical Informaticists
- **Progressive Disclosure:** Start with evaluation-only for quick assessment
- **Coverage Visualization:** Clear reports showing gaps and recommendations
- **Selective Testing:** Allow users to specify subset of categories to test

### For Content Authors
- **Usage Scenario Focus:** Test content against intended usage patterns
- **Gap Identification:** Clear feedback on missing scenario types
- **Prioritization:** Strength-of-match scores guide content improvement

### For CDS Developers
- **Provider vs Patient Balance:** Ensure testing covers both provider-centric and patient-centered scenarios
- **Workflow Integration:** Test scenarios in context of actual clinical workflows
- **Safety Validation:** Prioritize safety-critical categories in testing pipeline

## Conclusion

This enhanced testing approach addresses the core limitation of current UAT testing (only 17% category coverage) by:

1. **Expanding Coverage:** From 4 to 23 CDS usage scenario categories (5x increase)
2. **Adding Evaluation Focus:** New fidelity levels for assessment vs generation
3. **Improving Relevance:** Better alignment with actual CDS usage patterns
4. **Enhancing Safety:** Prioritization of safety-critical categories

The result will be comprehensive validation that ensures clinical content adequately covers the full spectrum of CDS usage scenarios, not just provider-centric treatment recommendations.
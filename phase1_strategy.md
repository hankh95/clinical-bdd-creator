# Phase 1: Clinical Context Adaptation & FHIR-CPG Integration
# New Test Strategy Framework

## Overview
Rebuilding BDD test generation from scratch with CDS usage scenarios and provider-focused clinical questions. Focus on what treatment/test to order, next steps, and clinical reasoning.

## Core Principles

### 1. Guideline Analysis → Provider Decision Questions
- **What treatment should I order?** (CDS 1.1.2, 1.1.3, 1.1.4)
- **What test should I order?** (CDS 1.1.5, 1.1.6)
- **What are the next steps?** (CDS 1.1.7, 4.2.1, 4.4.1)
- **What should I think about?** (CDS 1.1.1, 1.2.1, 1.2.2, 1.2.3)

### 2. FHIR-CPG Reasoning Framework (Conceptual, Not Implementation)
- **PlanDefinition**: Overall care plan structure
- **ActivityDefinition**: Specific actions (treatments, tests, monitoring)
- **CaseFeatureDefinition**: Patient/context characteristics
- **ObservationDefinition**: Clinical findings and measurements
- **Actions**: Treatment/test orders, referrals, monitoring

### 3. Clinical Reasoning Chain
Patient Context → Observations → Inferences → Actions → Next Steps

### 4. Combinatorial Testing
When guidelines specify multiple criteria combinations, generate tests for each valid combination.

## Implementation Strategy

### Phase 1A: Guideline Analysis Engine
1. Parse guideline content for decision points
2. Identify patient contexts and clinical scenarios
3. Extract treatment/test recommendations
4. Map to CDS usage scenarios

### Phase 1B: FHIR-CPG Conceptual Mapping
1. Break down guidelines into PlanDefinition-like structures
2. Identify ActivityDefinitions (treatments, tests, monitoring)
3. Define CaseFeatureDefinitions (patient characteristics)
4. Create ObservationDefinitions (clinical findings)

### Phase 1C: BDD Generation with Clinical Reasoning
1. Generate scenarios for each provider decision question
2. Include clinical reasoning chains
3. Support combinatorial testing
4. Create usage scenario coverage reporting

### Phase 1D: Quality & Validation
1. External AI validation with multiple providers
2. Clinical accuracy assessment
3. Usage scenario coverage analysis
4. Performance benchmarking
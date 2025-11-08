# Coverage Analysis and Gaps

## Current Coverage Summary

As of this organization effort, we have successfully categorized and organized 5 BDD test examples across clinical domains, complexity modes, and fidelity levels.

## Coverage by Dimension

### By Clinical Domain

| Domain | Count | Examples |
|--------|-------|----------|
| **Cardiology** | 2 | HFrEF quadruple therapy, AFib with comorbidities |
| **Oncology** | 2 | Metastatic prostate cancer, breast cancer chemotherapy |
| **Primary Care** | 1 | Diabetes with ASCVD |
| Emergency Medicine | 0 | **GAP** |
| Pediatrics | 0 | **GAP** |
| Psychiatry | 0 | **GAP** |
| Infectious Disease | 0 | **GAP** |
| Neurology | 0 | **GAP** |
| Pulmonology | 0 | **GAP** (COPD mentioned in AFib case but not primary focus) |
| Nephrology | 0 | **GAP** |

### By Generation Mode (Complexity)

| Mode | Count | Description | Examples |
|------|-------|-------------|----------|
| **Basic** | 0 | Simple scenarios, single condition | **GAP - Priority** |
| **Advanced** | 3 | Multi-step workflows, standard complexity | HFrEF, breast cancer, diabetes |
| **Expert** | 2 | Complex with multiple considerations | Prostate cancer, AFib |

### By Fidelity Level

| Fidelity | Count | Description | Examples |
|----------|-------|-------------|----------|
| **Low** | 0 | Basic concepts without details | **GAP - Priority** |
| **Medium** | 2 | Realistic with standard data | Breast cancer, diabetes |
| **High** | 3 | Comprehensive with detailed context | HFrEF, prostate cancer, AFib |

## Priority Gaps to Address

### 1. Basic Mode Examples (HIGH PRIORITY)
Need simple, straightforward scenarios for:
- Single condition management without comorbidities
- Direct treatment pathways
- Minimal decision points
- Examples:
  - Simple hypertension management
  - Uncomplicated urinary tract infection
  - Routine preventive care (immunizations)
  - Basic medication refill scenarios

### 2. Low Fidelity Examples (HIGH PRIORITY)
Need simplified concept validation scenarios:
- Generic patient data
- Simplified clinical logic
- Focus on testing basic workflow without clinical nuance
- Examples:
  - Concept validation for guideline logic
  - Basic CDS alert triggers
  - Simple rule-based decision points

### 3. Emergency Medicine Domain (MEDIUM PRIORITY)
Critical care scenarios needed:
- Acute myocardial infarction (STEMI/NSTEMI)
- Stroke (tPA decision-making)
- Sepsis protocols
- Trauma guidelines

### 4. Pediatrics Domain (MEDIUM PRIORITY)
Age-specific scenarios needed:
- Pediatric asthma management
- Well-child visits and immunizations
- Growth and development monitoring
- Pediatric fever protocols

### 5. Additional Primary Care Scenarios (LOW PRIORITY)
Expand primary care coverage:
- Chronic pain management
- Depression screening and management
- Preventive care (cancer screening)
- Hypertension management
- Smoking cessation

## Recommended Next Steps

### Phase 1: Fill Basic and Low Fidelity Gaps
1. Create 2-3 basic mode examples from simple clinical scenarios
2. Create 2-3 low fidelity examples for concept testing
3. Ensure these cover different domains where possible

### Phase 2: Expand Domain Coverage
1. Add at least 1 example each for:
   - Emergency Medicine (STEMI or stroke)
   - Pediatrics (asthma or well-child)
   - Infectious Disease (pneumonia or sepsis)

### Phase 3: Balance Distribution
1. Ensure each domain has examples across different modes
2. Ensure each mode has examples across different fidelities
3. Aim for a more balanced distribution overall

## Success Metrics

Target distribution for comprehensive coverage:

- **Domains**: At least 1 example per major specialty (goal: 8-10 domains)
- **Modes**: Balanced distribution
  - Basic: 25-30% of examples
  - Advanced: 40-50% of examples
  - Expert: 20-30% of examples
- **Fidelity**: Balanced distribution
  - Low: 20-30% of examples
  - Medium: 40-50% of examples
  - High: 20-30% of examples

## Current Status vs. Target

| Dimension | Current | Target | Status |
|-----------|---------|--------|--------|
| Total Examples | 5 | 15+ | 33% |
| Domains Covered | 3 | 8 | 37% |
| Basic Mode | 0 | 4-5 | 0% ⚠️ |
| Advanced Mode | 3 | 6-8 | 38-50% |
| Expert Mode | 2 | 3-5 | 40-67% |
| Low Fidelity | 0 | 3-5 | 0% ⚠️ |
| Medium Fidelity | 2 | 6-8 | 25-33% |
| High Fidelity | 3 | 3-5 | 60-100% |

## Notes

- Current examples skew toward higher complexity and fidelity
- This is likely because existing examples were created for comprehensive demonstration
- Need to intentionally create simpler examples for testing foundational logic
- Basic and low fidelity examples are critical for rapid testing and validation during development

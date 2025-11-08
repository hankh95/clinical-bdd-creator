# BDD Tests Organized by Fidelity Level

This folder organizes BDD test examples by their level of detail and realism.

## Available Fidelity Levels

### Low (`low/`)
Basic clinical concepts without specific details:
- Simplified scenarios for concept validation
- Minimal patient context
- Generic clinical data
- Currently no examples (gap to address)

### Medium (`medium/`)
Realistic patient scenarios with standard clinical data:
- **oncology-advanced-medium-breast-001** - Breast cancer with standard chemotherapy protocol
- **primary-care-advanced-medium-diabetes-001** - Diabetes with typical ASCVD presentation

Characteristics:
- Realistic patient demographics
- Standard lab values
- Common medication regimens
- Typical clinical presentations
- Expected monitoring protocols

### High (`high/`)
Comprehensive scenarios with detailed clinical context and edge cases:
- **cardiology-advanced-high-hfref-001** - HFrEF with detailed GDMT protocols
- **oncology-expert-high-prostate-001** - mCRPC with trial enrollment and bone metastases
- **cardiology-expert-high-afib-001** - AFib with multiple comorbidities

Characteristics:
- Detailed patient histories
- Specific lab values and vital signs
- Complex medication interactions
- Edge cases and contraindications
- Comprehensive monitoring plans
- Guideline-specific details

## File Naming Convention

Files follow the pattern: `{domain}-{mode}-{fidelity}-{condition}-{id}.feature`

## Fidelity Definition Guide

- **Low**: Testing basic logic flow without clinical nuance
- **Medium**: Validating realistic clinical scenarios with standard complexity
- **High**: Ensuring accuracy for production-ready guidelines with full context

## Coverage Analysis

- **Low**: 0 examples (needs coverage)
- **Medium**: 2 examples
- **High**: 3 examples

## Adding New Examples

When adding new examples:
1. Evaluate level of detail required
2. Consider target use case (testing, training, production)
3. Match to appropriate fidelity level
4. Follow naming convention
5. Update this README

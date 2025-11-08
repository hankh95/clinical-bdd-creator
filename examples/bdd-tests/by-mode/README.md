# BDD Tests Organized by Generation Mode

This folder organizes BDD test examples by their generation strategy/complexity level.

## Available Modes

### Basic (`basic/`)
Simple scenarios with few steps and straightforward clinical decision-making:
- Single condition focus
- Minimal comorbidities
- Direct treatment pathways
- Currently no examples (gap to address)

### Advanced (`advanced/`)
Multi-step clinical workflows with standard complexity:
- **cardiology-advanced-high-hfref-001** - Heart Failure quadruple therapy initiation
- **oncology-advanced-medium-breast-001** - Breast cancer chemotherapy cycles
- **primary-care-advanced-medium-diabetes-001** - Diabetes with cardiovascular risk

Characteristics:
- Multiple decision points
- Standard monitoring protocols
- Common clinical scenarios
- Realistic patient complexity

### Expert (`expert/`)
Complex decision support with multiple considerations:
- **oncology-expert-high-prostate-001** - Metastatic prostate cancer with trial enrollment
- **cardiology-expert-high-afib-001** - Atrial fibrillation with multiple comorbidities

Characteristics:
- Multiple interacting conditions
- Complex medication considerations
- Edge cases and contraindications
- Advanced risk stratification

## File Naming Convention

Files follow the pattern: `{domain}-{mode}-{fidelity}-{condition}-{id}.feature`

## Coverage Analysis

- **Basic**: 0 examples (needs coverage)
- **Advanced**: 3 examples
- **Expert**: 2 examples

## Adding New Examples

When adding new examples:
1. Assess scenario complexity
2. Match to appropriate mode level
3. Ensure balanced coverage across modes
4. Follow naming convention
5. Update this README

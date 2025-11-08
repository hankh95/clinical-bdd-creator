# BDD Tests Organized by Clinical Domain

This folder organizes BDD test examples by clinical specialty/domain.

## Available Domains

### Cardiology (`cardiology/`)
Clinical scenarios related to cardiovascular conditions:
- **cardiology-advanced-high-hfref-001** - Heart Failure with Reduced Ejection Fraction (HFrEF) quadruple therapy
- **cardiology-expert-high-afib-001** - Atrial Fibrillation with COPD and obesity

### Oncology (`oncology/`)
Clinical scenarios related to cancer care:
- **oncology-expert-high-prostate-001** - Metastatic Castration-Resistant Prostate Cancer (mCRPC)
- **oncology-advanced-medium-breast-001** - Breast cancer anthracycline-based chemotherapy

### Primary Care (`primary-care/`)
Clinical scenarios in primary care settings:
- **primary-care-advanced-medium-diabetes-001** - Type 2 Diabetes with ASCVD

## File Naming Convention

Files follow the pattern: `{domain}-{mode}-{fidelity}-{condition}-{id}.feature`

## Adding New Examples

When adding new examples to this organizational structure:

1. Identify the primary clinical domain
2. Follow the naming convention
3. Include all associated files (.assert.yaml, .fsh, .yaml, .expected.*)
4. Add clinical context comments at the top of the .feature file
5. Update this README with the new example

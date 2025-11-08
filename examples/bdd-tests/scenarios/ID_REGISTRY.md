# BDD Scenario ID Registry

This file maintains a central registry of all assigned scenario IDs to ensure uniqueness and prevent conflicts.

## ID Format

```
{domain}-{category}-{condition}-{sequence}
```

## Registered IDs

### Cardiology

| ID | Title | Status | Created | Guidelines |
|----|-------|--------|---------|------------|
| cardiology-treatment-hfref-001 | Heart Failure with Reduced Ejection Fraction - Quadruple Therapy Initiation | Active | 2025-11-08 | 2022 AHA/ACC/HFSA Heart Failure Guideline |
| cardiology-treatment-afib-001 | Atrial Fibrillation with COPD and Obesity - Anticoagulation and Rate Control | Active | 2025-11-08 | AHA/ACC/HRS Atrial Fibrillation Management Guidelines |

### Primary Care

| ID | Title | Status | Created | Guidelines |
|----|-------|--------|---------|------------|
| primary-care-treatment-diabetes-001 | Type 2 Diabetes with ASCVD - Cardioprotective Therapy Initiation | Active | 2025-11-08 | ADA 2025 Standards of Care in Diabetes |

### Oncology

| ID | Title | Status | Created | Guidelines |
|----|-------|--------|---------|------------|
| oncology-treatment-breast-cancer-001 | Stage II Breast Cancer - Anthracycline-Based Chemotherapy Cycle 1 | Active | 2025-11-08 | NCCN Breast Cancer Guidelines |
| oncology-treatment-prostate-cancer-001 | Metastatic Castration-Resistant Prostate Cancer - Docetaxel Chemotherapy | Active | 2025-11-08 | NCCN/AUA Prostate Cancer Guidelines, SWOG 0421 Trial |

## ID Assignment Process

When creating a new scenario:

1. **Determine Base ID:**
   - Choose appropriate domain, category, and condition
   - Format as: `{domain}-{category}-{condition}`

2. **Check Registry:**
   - Search this file for existing IDs with the same base
   - Identify the highest sequence number used

3. **Assign Sequence:**
   - Use next sequential number (e.g., if -001 exists, use -002)
   - Zero-pad to 3 digits (001, 002, 003, etc.)

4. **Register ID:**
   - Add new entry to appropriate domain section in this file
   - Include all required metadata
   - Commit the registry update with the scenario files

5. **Verify Uniqueness:**
   - Confirm ID does not exist anywhere in the registry
   - Check file system for any existing files with that ID

## Status Values

- **Active:** Scenario is current and in use
- **Deprecated:** Scenario is outdated but preserved for reference
- **Draft:** Scenario is under development
- **Archived:** Scenario has been retired

## Version Control

When updating a scenario:

- **DO NOT** change the scenario ID
- Update the version number in the scenario's YAML file
- Maintain ID stability for references and cross-links
- Document major changes in the scenario's YAML metadata

## Domain Categories

### Recognized Domains

- **cardiology** - Cardiovascular conditions
- **oncology** - Cancer-related scenarios
- **primary-care** - General primary care and chronic disease management
- **emergency** - Emergency department scenarios
- **pediatrics** - Pediatric scenarios
- **obstetrics** - Obstetric and gynecological scenarios
- **psychiatry** - Mental health scenarios
- **surgery** - Surgical scenarios
- **infectious-disease** - Infectious disease scenarios

### Recognized Categories

- **treatment-recommendation** - Medication and therapy recommendations
- **diagnosis** - Diagnostic decision support
- **monitoring** - Ongoing patient monitoring
- **risk-assessment** - Risk stratification and prediction
- **screening** - Preventive screening recommendations
- **referral** - Referral recommendations
- **education** - Patient education scenarios

## Common Conditions

### Cardiology
- hfref, hfpef, afib, cad, hypertension, mi, cardiomyopathy

### Oncology
- breast-cancer, prostate-cancer, lung-cancer, colon-cancer, melanoma

### Primary Care
- diabetes, hypertension, hyperlipidemia, copd, asthma

### Emergency
- sepsis, stemi, stroke, trauma, anaphylaxis

## Naming Conventions

### Best Practices

- Use lowercase for all components
- Use hyphens to separate words within a component
- Keep condition names concise but clear
- Use standard medical abbreviations when widely recognized
- Avoid special characters or spaces

### Examples

✅ **Good:**
- `cardiology-treatment-hfref-001`
- `primary-care-screening-colon-cancer-001`
- `emergency-diagnosis-stemi-001`

❌ **Avoid:**
- `Cardiology-Treatment-HFrEF-001` (don't use capital letters)
- `cardiology_treatment_hfref_001` (use hyphens, not underscores)
- `cardiology-tx-hf-1` (sequence should be zero-padded)
- `card-treat-heart-failure-001` (use standard domain names)

## Registry Maintenance

This registry should be updated:
- When creating new scenarios
- When deprecating or archiving scenarios
- When changing scenario status
- During regular audits for accuracy

Last Updated: 2025-11-08
Maintainer: Clinical BDD Creator Team

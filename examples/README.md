# Guideline Examples for BDD Testing

This folder contains sample clinical guidelines used for testing and validating the BDD scenario generation system.

## Purpose

These examples serve multiple purposes:

- **Testing**: Validate that the system can process different guideline formats and generate appropriate BDD scenarios
- **Training**: Provide reference materials for AI model fine-tuning and prompt development
- **Validation**: Ensure generated BDD scenarios accurately reflect clinical decision-making
- **Demonstration**: Show stakeholders how clinical guidelines translate to executable test cases

## Folder Structure

```bash
examples/
├── guidelines/
│   ├── acc-afib/           # American College of Cardiology - Atrial Fibrillation
│   ├── diabetes-management/ # ADA - Diabetes Management
│   ├── nccn-cancer/       # National Comprehensive Cancer Network - Cancer
│   ├── acute-coronary-syndrome/  # ACS guidelines (STEMI, NSTEMI, unstable angina)
│   ├── hypertension/      # Blood pressure management
│   ├── pneumonia/         # Community-acquired pneumonia
│   └── heart-failure/     # Congestive heart failure
└── README.md
```

## Guideline Sources

Guidelines should be sourced from reputable organizations:

- **American Heart Association (AHA)**
- **American College of Cardiology (ACC)**
- **American Diabetes Association (ADA)**
- **Infectious Diseases Society of America (IDSA)**
- **American College of Physicians (ACP)**
- **National Institute for Health and Care Excellence (NICE)**

## Format Requirements

Each guideline folder should contain:

- `source.md` - Original guideline text in Markdown format
- `metadata.json` - Guideline metadata (publisher, date, version, etc.)
- `sections.json` - Structured breakdown of guideline sections
- `expected-scenarios/` - Folder with expected BDD scenarios (for validation)

## Usage in Testing

These examples will be used to:

1. Test content ingestion from different formats
2. Validate scenario generation across multiple clinical domains
3. Benchmark AI model performance on clinical content
4. Demonstrate system capabilities to stakeholders

## Contributing

When adding new guidelines:

1. Ensure clinical accuracy and currency
2. Include proper attribution and licensing information
3. Follow the established folder structure
4. Add expected BDD scenarios for validation

# Usage Scenarios: BDD Test Categorization by User Actions

**Date Created:** November 8, 2025
**Version:** 2.0
**Purpose:** Define usage scenarios that categorize BDD tests based on user actions and workflows

## Overview

This document defines usage scenarios that categorize BDD tests according to the primary user actions and workflows they validate. Each scenario represents a distinct way users interact with the Clinical BDD Creator system, enabling systematic test organization and coverage analysis.

## Documentation Structure

This folder contains two complementary documents:

1. **`README.md`** (this file): High-level usage scenario categories for BDD test organization
2. **`CDS Usage Scenarios.md`**: Comprehensive clinical decision support use cases with detailed workflows and actor perspectives

## Relationship to CDS Use Cases

The 8 high-level categories below map to the 23 detailed CDS use cases in `CDS Usage Scenarios.md`:

| Category | Maps to CDS Use Cases | Description |
|----------|----------------------|-------------|
| Content Ingestion | 4.1.1 (Guideline-Driven Information Retrieval) | Finding and loading clinical content |
| Scenario Generation | 1.1.1-1.1.6 (Pre-Action Guidance) | Creating BDD scenarios from content |
| Output Control | 1.1.2-1.1.4 (Treatment Recommendations) | Controlling scenario output format |
| Taxonomy Classification | 1.1.1 (Differential Diagnosis) | Clinical taxonomy and classification |
| Quality Assurance | 1.2.1-1.2.3 (Post-Action Error Prevention) | Quality validation and safety checks |
| Inventory Management | 2.2.1 (Quality Metrics Reporting) | Managing generated content inventory |
| Integration & API | 4.1.1, 4.2.1 (Information Retrieval & Protocol Support) | API and system integration |
| Administration | 2.1.1, 2.3.1 (Case Management & Risk Stratification) | System administration and monitoring |

## Usage Scenario Categories

### 1. Content Ingestion & Discovery (`content-*`)

**Primary User Action:** Finding and loading clinical guideline content
**User Goal:** Access and prepare clinical content for scenario generation
**Key Workflows:**

- Source discovery and validation
- Content format detection and parsing
- Manifest generation and validation
- Quality assessment and filtering

**Example BDD Tests:**

- `content-discovery-pdf.feature` - PDF content discovery and parsing
- `content-validation-manifest.feature` - Manifest file validation
- `content-quality-thresholds.feature` - Content quality assessment
- `content-format-detection.feature` - Automatic format recognition

**Success Criteria:**

- Content loaded within 30 seconds
- ≥95% parsing success rate
- Clear error messages for invalid content
- Quality metrics reported

### 2. Scenario Generation (`generation-*`)

**Primary User Action:** Creating BDD scenarios from clinical content
**User Goal:** Generate comprehensive test scenarios across different modes
**Key Workflows:**

- Mode selection (top-down, bottom-up, external, logic-derived)
- Section-based generation
- Multi-mode combination
- Scenario deduplication and merging

**Example BDD Tests:**

- `generation-top-down-mode.feature` - Holistic document analysis
- `generation-section-based.feature` - Section-specific scenario creation
- `generation-multi-mode-merge.feature` - Combining different generation strategies
- `generation-deduplication.feature` - Removing duplicate scenarios

**Success Criteria:**

- Scenarios generated within 5 minutes
- ≥85% clinical relevance
- Zero duplicate scenarios
- Complete coverage of clinical decision points

### 3. Output Control & Formatting (`output-*`)

**Primary User Action:** Controlling output fidelity and format
**User Goal:** Generate artifacts at appropriate detail levels
**Key Workflows:**

- Fidelity level selection (draft/full/full-fhir)
- Feature file generation
- FHIR resource creation
- Output validation and formatting

**Example BDD Tests:**

- `output-fidelity-draft.feature` - Basic inventory generation
- `output-fidelity-full.feature` - Complete feature file creation
- `output-fhir-resources.feature` - FHIR artifact generation
- `output-format-validation.feature` - Output syntax validation

**Success Criteria:**

- Output generated within specified time limits
- ≥95% format compliance
- Valid FHIR resources (when applicable)
- Readable feature files

### 4. Taxonomy & Classification (`taxonomy-*`)

**Primary User Action:** Classifying scenarios by clinical decision types
**User Goal:** Organize scenarios according to CDS taxonomy
**Key Workflows:**

- Automatic CDS category assignment
- Taxonomy validation
- Classification accuracy assessment
- Category-based organization

**Example BDD Tests:**

- `taxonomy-diagnosis-classification.feature` - Differential diagnosis categorization
- `taxonomy-treatment-recommendation.feature` - Treatment scenario classification
- `taxonomy-test-ordering.feature` - Diagnostic test recommendation classification
- `taxonomy-accuracy-validation.feature` - Classification accuracy assessment

**Success Criteria:**

- ≥90% classification accuracy
- Consistent taxonomy application
- Clear category assignments
- Validation of classification logic

### 5. Quality Assurance & Validation (`qa-*`)

**Primary User Action:** Validating and improving scenario quality
**User Goal:** Ensure clinical accuracy and test effectiveness
**Key Workflows:**

- Scenario validation against guidelines
- Quality metrics calculation
- Error detection and correction
- Compliance verification

**Example BDD Tests:**

- `qa-clinical-accuracy.feature` - Guideline compliance validation
- `qa-scenario-completeness.feature` - Required field validation
- `qa-duplicate-detection.feature` - Duplicate scenario identification
- `qa-metrics-reporting.feature` - Quality metrics calculation

**Success Criteria:**

- ≥95% clinical accuracy
- Complete scenario metadata
- Clear quality metrics
- Actionable improvement recommendations

### 6. Inventory Management (`inventory-*`)

**Primary User Action:** Managing and tracking scenario collections
**User Goal:** Organize and maintain scenario libraries
**Key Workflows:**

- Scenario inventory creation
- Metadata management
- Search and filtering
- Version control and updates

**Example BDD Tests:**

- `inventory-creation.feature` - Scenario inventory generation
- `inventory-metadata-validation.feature` - Required field validation
- `inventory-search-filtering.feature` - Scenario discovery
- `inventory-version-control.feature` - Scenario updates and versioning

**Success Criteria:**

- Complete inventory within 2 minutes
- ≥98% metadata completeness
- Efficient search and filtering
- Version history preservation

### 7. Integration & Export (`integration-*`)

**Primary User Action:** Integrating with external systems and exporting results
**User Goal:** Use scenarios in broader clinical workflows
**Key Workflows:**

- Test execution integration
- Results export and reporting
- External system connectivity
- Data format conversion

**Example BDD Tests:**

- `integration-test-execution.feature` - Test runner integration
- `integration-results-export.feature` - Results formatting and export
- `integration-external-systems.feature` - Third-party system integration
- `integration-data-conversion.feature` - Format conversion and validation

**Success Criteria:**

- Successful integration with test runners
- Export in multiple formats
- Data integrity preservation
- Error handling for integration failures

### 8. Administration & Configuration (`admin-*`)

**Primary User Action:** Configuring and administering the system
**User Goal:** Customize behavior and maintain system health
**Key Workflows:**

- Configuration management
- User preference settings
- System monitoring and logging
- Performance optimization

**Example BDD Tests:**

- `admin-configuration-management.feature` - System configuration
- `admin-user-preferences.feature` - Personalization settings
- `admin-system-monitoring.feature` - Health and performance monitoring
- `admin-logging-audit.feature` - Activity logging and auditing

**Success Criteria:**

- Configuration changes applied immediately
- System health metrics available
- Comprehensive audit trails
- Performance within acceptable limits

## BDD Test Labeling Convention

### Test Tags Format

BDD tests SHALL include usage scenario tags using the following format:

```gherkin
@usage-scenarios:1.1.1,1.1.3,1.2.1
@decision-questions:treatment_now,tests_now
Scenario: [Test Description]
```

### Tag Components

1. **Usage Scenario IDs**: Comma-separated list of CDS scenario IDs from `CDS Usage Scenarios.md`
2. **Decision Questions**: Primary decision question families (treatment_now, tests_now, refer_now, monitoring_frequency, education_now, report_now, documentation_now)

### Usage Scenario ID Mapping

| ID Range | Category | Primary Use Case |
|----------|----------|------------------|
| 1.1.x | Pre-Action Guidance | Clinical decision support during patient encounters |
| 1.2.x | Post-Action Error Prevention | Safety checking and adverse event monitoring |
| 2.x.x | Population-Based CDS | Case management, quality metrics, risk stratification |
| 3.x.x | Patient-Centered CDS | Shared decision-making, SDOH integration |
| 4.x.x | Information Retrieval & Protocol Support | Guideline queries, protocol automation |

### Example Test Labels

```gherkin
@usage-scenarios:1.1.2,1.1.3,1.2.1
@decision-questions:treatment_now
Scenario: Drug recommendation with interaction checking
  Given a patient with hypertension and diabetes
  When the system analyzes medication options
  Then it recommends appropriate drugs with interaction warnings

@usage-scenarios:1.1.5,1.2.2
@decision-questions:tests_now
Scenario: Diagnostic test recommendation with appropriateness checking
  Given a patient with chest pain
  When the system evaluates test options
  Then it recommends appropriate cardiac tests with AUC validation

@usage-scenarios:2.3.1,4.4.1
@decision-questions:refer_now
Scenario: Risk stratification with care coordination
  Given a high-risk patient
  When the system assesses risk factors
  Then it generates referral alerts with care coordination
```

### Labeling Guidelines

1. **Primary Scenario First**: List the most relevant usage scenario ID first
2. **Multiple Scenarios**: Include all applicable scenarios (max 3-4 per test)
3. **Decision Question Priority**: Choose the most critical decision question family
4. **Test Coverage Tracking**: Use labels to ensure comprehensive scenario coverage
5. **Maintenance**: Update labels when new scenarios are added or test scope changes

### Implementation Benefits

- **Traceability**: Direct links between tests and clinical use cases
- **Coverage Analysis**: Automated reporting of tested scenarios
- **Requirements Validation**: Ensures tests align with clinical workflows
- **Regression Prevention**: Identifies impacted tests when scenarios change

## Coverage Analysis

### By Usage Category

- Content Ingestion: 15% of total scenarios
- Scenario Generation: 25% of total scenarios
- Output Control: 20% of total scenarios
- Taxonomy & Classification: 10% of total scenarios
- Quality Assurance: 15% of total scenarios
- Inventory Management: 5% of total scenarios
- Integration & Export: 5% of total scenarios
- Administration: 5% of total scenarios

### By User Persona

- **Clinical Knowledge Engineer**: Categories 1, 2, 3, 4, 5, 6 (85% of tests)
- **Test Automation Engineer**: Categories 3, 6, 7, 8 (60% of tests)
- **Clinical Informaticist**: Categories 2, 3, 4, 7 (50% of tests)
- **System Administrator**: Categories 6, 7, 8 (40% of tests)

## Implementation Guidelines

### Test Organization

- Group tests by usage category in separate directories
- Use consistent naming conventions
- Include category-specific setup and teardown
- Document category-specific success criteria

### Test Prioritization

- **High Priority**: Core functionality (generation, output, taxonomy)
- **Medium Priority**: Quality assurance and inventory management
- **Low Priority**: Advanced integration and administration features

### Maintenance

- Review usage categories quarterly
- Update categories based on user feedback
- Add new categories for emerging use cases
- Deprecate categories no longer relevant

## Relationship to Other Specifications

- **EARS Requirements**: Usage scenarios validate functional requirements
- **User Personas**: Each persona has primary and secondary usage categories
- **Quality Tests**: Usage scenarios inform test case design
- **MCP Tools**: Each usage category maps to specific tool capabilities

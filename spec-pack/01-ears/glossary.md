# Clinical BDD Creator - Glossary

**Version:** 1.1.0
**Date:** November 7, 2025

This glossary provides definitions for clinical, technical, and domain-specific terms used throughout the Clinical BDD Creator project.

## Clinical Terms

### Core Clinical Concepts

- **BDD (Behavior-Driven Development)**: A software development approach that uses natural language constructs to define and verify system behavior, particularly effective for clinical scenarios where stakeholder communication is critical.

- **CDS (Clinical Decision Support)**: Systems that provide clinicians with knowledge and person-specific information to enhance health decisions. Includes alerts, reminders, order sets, and documentation templates.

- **EARS (Easy Approach to Requirements Syntax)**: A requirements specification method using structured natural language patterns (WHEN...THE System SHALL...) to create testable acceptance criteria.

- **Evidence-Based Medicine**: The conscientious, explicit, and judicious use of current best evidence in making decisions about the care of individual patients.

### Healthcare Standards & Terminology

- **FHIR (Fast Healthcare Interoperability Resources)**: A standard for health care data exchange, published by HL7. Defines how healthcare information can be exchanged between different computer systems regardless of how it is stored in those systems.

- **HL7 (Health Level Seven International)**: A standards organization that provides frameworks and standards for the exchange, integration, sharing, and retrieval of electronic health information.

- **SNOMED CT (Systematized Nomenclature of Medicine Clinical Terms)**: A comprehensive clinical terminology system that provides codes, terms, synonyms, and definitions used in clinical documentation and reporting.

- **ICD-11 (International Classification of Diseases)**: The 11th revision of the WHO's global standard for health data, clinical documentation, and statistical aggregation.

- **LOINC (Logical Observation Identifiers Names and Codes)**: A universal code system for identifying laboratory and clinical observations, providing a common language for clinical data exchange.

- **RxNorm**: A normalized naming system for generic and branded drugs and a tool for supporting semantic interoperability between drug terminologies and pharmacy knowledge base systems.

### Clinical Decision Support Categories

- **CDS 1.1.1 - Differential Diagnosis**: Computer-assisted determination of possible diagnoses based on patient data and clinical knowledge.

- **CDS 1.1.2 - Treatment Recommendation**: Suggestions for appropriate treatments based on patient condition, evidence, and guidelines.

- **CDS 1.1.3 - Drug Recommendation**: Specific recommendations for medication selection, dosing, and monitoring.

- **CDS 1.1.5 - Diagnostic Test Recommendation**: Suggestions for appropriate diagnostic tests based on clinical presentation and guidelines.

### Clinical Knowledge Representation

- **CIKG (Clinical Informatics Knowledge Graph)**: A structured representation of clinical knowledge using graph-based models to capture relationships between clinical concepts, guidelines, and decision logic.

- **L0 Prose**: Raw clinical guideline text in natural language format.

- **L1 GSRL Triples**: Guideline Statement-Reasoning Link triples representing clinical logic as subject-predicate-object relationships.

- **L2 RALL Assets**: Reasoning Asset Library with structured clinical knowledge components.

- **L3 WATL Workflows**: Workflow Asset Template Library containing executable clinical decision pathways.

## Technical Terms

### MCP Protocol

- **MCP (Model Context Protocol)**: A protocol for connecting AI models to external tools and data sources, enabling seamless integration between AI assistants and computational tools.

- **JSON-RPC**: A remote procedure call protocol encoded in JSON, used for communication between MCP clients and servers.

- **WebSocket**: A communication protocol providing full-duplex communication channels over a single TCP connection, used for real-time MCP communication.

- **MCP Manifest**: A JSON configuration file describing the tools, resources, and capabilities provided by an MCP server.

### AI & Machine Learning

- **Multi-Modal AI Validation**: The process of validating AI outputs by comparing results across different AI models (e.g., GPT-4, Claude, Gemini) to ensure consistency and reduce hallucinations.

- **Prompt Engineering**: The practice of designing and optimizing text prompts to elicit desired responses from AI language models.

- **Few-Shot Learning**: A machine learning technique where a model learns from a small number of examples to perform a new task.

- **Chain-of-Thought Reasoning**: A prompting technique that encourages AI models to show their step-by-step reasoning process.

- **Retrieval-Augmented Generation (RAG)**: A technique that combines information retrieval with generative AI to produce more accurate and contextually relevant responses.

### Software Development

- **Gherkin**: A business-readable, domain-specific language that lets you describe software's behavior without detailing how that behavior is implemented.

- **Feature File**: A file written in Gherkin that describes a software feature and its acceptance criteria through scenarios.

- **Scenario**: A concrete example that illustrates a business rule, written in Gherkin with Given-When-Then structure.

- **Step Definition**: Code that connects Gherkin steps to programming code that executes the steps.

### Quality Assurance

- **Test Coverage**: A measure of the degree to which the source code of a program is executed when a particular test suite runs.

- **Code Quality Metrics**: Quantitative measures of code quality including cyclomatic complexity, maintainability index, and technical debt.

- **Static Analysis**: The analysis of computer software performed without executing the program, used to find bugs and ensure coding standards.

- **Linting**: The process of running a program that checks code for programmatic and stylistic errors.

### Security & Compliance

- **API Key Authentication**: A method of authentication where a unique key is provided to verify identity and authorize access to API resources.

- **Rate Limiting**: A technique to control the rate of requests sent or received by a network interface controller.

- **PII (Personally Identifiable Information)**: Any data that could potentially identify a specific individual, requiring special handling under privacy regulations.

- **PHI (Protected Health Information)**: Individually identifiable health information transmitted or maintained in any form or medium.

- **HIPAA (Health Insurance Portability and Accountability Act)**: A U.S. law that provides data privacy and security provisions for safeguarding medical information.

- **BAA (Business Associate Agreement)**: A contract between a healthcare provider and a business associate that ensures the business associate will appropriately safeguard protected health information.

### Data Management

- **Provenance**: Information about the origin, context, and history of data, crucial for audit trails and reproducibility.

- **Traceability**: The ability to trace the history, application, or location of an entity by means of recorded identifications.

- **Deduplication**: The process of identifying and removing duplicate records from a dataset.

- **Data Validation**: The process of ensuring that data is both correct and useful, checking for accuracy, completeness, and consistency.

### Performance & Scalability

- **Latency**: The time delay between a request and response in a system.

- **Throughput**: The rate at which a system processes requests or data.

- **RPS (Requests Per Second)**: A measure of how many requests a system can handle in one second.

- **TPM (Tokens Per Minute)**: A measure of AI model usage, where tokens represent pieces of words or punctuation.

- **95th Percentile**: A statistical measure indicating that 95% of observations fall below this value, commonly used for performance benchmarking.

## Domain-Specific Terms

### Clinical Workflow

- **Clinical Decision Point**: A moment in clinical care where a decision must be made about diagnosis, treatment, or management.

- **Patient Fixture**: A standardized patient scenario or profile used for testing clinical decision support systems.

- **Decision Target Window**: The timeframe within which a clinical decision should be made to optimize patient outcomes.

- **Evidence Anchor**: A reference to the clinical evidence or guideline supporting a particular recommendation.

### Testing Methodology

- **Scenario Inventory**: A structured catalog of all generated test scenarios with metadata for review and prioritization.

- **Fidelity Levels**: Different levels of output detail and completeness (none, draft, full, full-fhir).

- **Generation Modes**: Different strategies for creating test scenarios (top-down, bottom-up, external, logic-derived).

- **Persona**: A fictional character representing a type of user or clinical role for scenario testing.

### Integration Concepts

- **CDS Hooks**: A specification that enables clinical decision support at the point of care within EHR workflows.

- **PlanDefinition**: A FHIR resource that defines a series of actions to be performed in a clinical context.

- **ActivityDefinition**: A FHIR resource that defines an action to be performed as part of a clinical protocol.

- **Library**: A FHIR resource containing clinical knowledge artifacts such as decision support rules or quality measures.

This glossary will be expanded as new terms are introduced during development and clinical domain integration.</content>


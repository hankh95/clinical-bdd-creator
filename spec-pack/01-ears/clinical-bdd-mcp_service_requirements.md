# MCP Service Requirements (Merged)

**Generated:** 2025-11-07 19:38:21Z  

This document merges the user's baseline requirements with an MCP-oriented design so the project can be offered as a paid MCP service consumable by Kiro, Claude Desktop, Cursor, and other MCP clients.

---

## 0) Executive Summary
We will expose the system as an **MCP server** providing tools for discovery, scenario generation (EARS/BDD), FHIR artifact creation, CDS taxonomy, and analytics. The server will include API-key authentication, usage metering, Stripe billing, and enterprise deployment options.

---

## 1) Protocol & Contracts

- **Transport:** JSON-RPC over stdio and WebSocket (MCP-compatible)
- **Manifest:** `mcp.json` describing tools, resources, and model capabilities
- **Schema:** All inputs/outputs use JSON Schema references; FHIR outputs conform to R4/R5 profiles where applicable
- **Provenance:** Every response includes `provenance` block (source, hash, model, prompt_id, timestamps, checksum)
- **Versioning:** Semantic versioning for tools; deprecation policy with warning window

---

## 2) Tools (Initial Set)

- `discover_sources(uri, format, auth)` → list of documents/sections
- `ingest_guideline(uri, format, org, topic, tags[])` → asset ids + provenance
- `generate_scenarios(topic_id, mode, sections[], fidelity, provider, model)` → scenarios + mapping
- `generate_scenarios_by_section(topic_id, sections[])` → scenarios with section lineage
- `generate_feature_file(asset_id, style="EARS|Gherkin")` → feature file text + write suggestion
- `classify_cds(asset_id, taxonomy="order|assessment|monitor|education|referral")` → labels + confidence
- `generate_fhir(asset_id, target="PlanDefinition|CaseFeatureDefinition|Bundle")` → FHIR JSON
- `diagnosis_rank(case_features[], top_k)` → ranked list w/ rationales
- `list_assets(filter, page, size, sort)` / `get_asset(id)` / `delete_asset(id)`
- `dedupe_assets(scope, threshold)` → merge plan + conflicts
- `qc_validate(asset_id, ruleset="SHACL|JSONSchema")` → issues + fixes
- `metrics(scope)` → counts, coverage %, dedupe ratio, latency
- `run_tests(suite_uri)` → results + junit.xml
- `get_config()` / `set_config(patch)`
- `get_logs(correlation_id?, last_n?)`
- All write-tools accept `dry_run: true`

---

## 3) Security, Auth, and Monetization

- **Auth:** API keys (Bearer); optional OAuth for enterprise
- **Billing:** Stripe usage-based + subscriptions; per-tool metering; monthly caps
- **Rate limits:** Per-key RPS & TPM; 429 with retry-after
- **PII/PHI:** Customer-managed keys; redaction utilities; signed BAA for HIPAA workloads
- **Audit:** Immutable usage ledger; export CSV; correlation-ids

---

## 4) SLOs & Resilience

- P95 latency targets per tool; backoff and retries on provider errors
- Idempotency via `X-Idempotency-Key`
- Blue/green deploys; health endpoints; readiness checks

---

## 5) Client Configuration Examples

### Kiro (.kiro/mcp.json)
```json
{
  "servers": [
    {
      "name": "cikg-mcp",
      "command": "cikg-mcp",
      "args": ["--ws", "wss://api.example.com/mcp"],
      "env": {"MCP_API_KEY": "•••"}
    }
  ]
}
```

### Claude Desktop (~/.claude/mcp/settings.json)
```json
{
  "mcpServers": {
    "cikg-mcp": {
      "command": "node",
      "args": ["dist/server.js"],
      "env": {"MCP_API_KEY": "•••"}
    }
  }
}
```

### Cursor (settings.json > mcp)
```json
{
  "mcp": {
    "providers": [{ "name": "cikg-mcp", "url": "wss://api.example.com/mcp" }]
  }
}
```

---

## 6) Deployment

- **SaaS:** HTTPS/WebSocket with API gateway (auth/rate-limit), serverless workers for tools
- **On‑prem/Private:** Docker/K8s helm chart; no outbound internet option; bring-your-own LLM (Bedrock/Azure/OpenAI/local vLLM)
- **Observability:** OpenTelemetry traces; structured logs; dashboards

---

## 7) Roadmap

- Phase 1: Core tools + billing + provenance
- Phase 2: Advanced QC (SHACL), dedupe, scenario coverage metrics
- Phase 3: Workflow hooks, IDE hints, auto-fix PRs

---

## 8) Mapping Uploaded Requirements → MCP Design

#### Requirement 1: Content Discovery and Ingestion
- Provide tools: `discover_sources`, `ingest_guideline`; connectors for html/md/pdf; auth strategies.

#### Requirement 2: Multi-Mode Scenario Generation
- `generate_scenarios(mode=baseline|stress|edge|negative)`; return typed JSON.

#### Requirement 3: Section-Based Scenario Generation
- `generate_scenarios_by_section(sections[])`; include provenance per section.

#### Requirement 4: Fidelity-Based Output Control
- `fidelity` param (low|medium|high); provider/model passthrough; token/latency budget hints.

#### Requirement 5: CDS Taxonomy Classification
- `classify_cds` tool; returns labels + confidence; pluggable taxonomy.

#### Requirement 6: Scenario Inventory Management
- `list_assets/get_asset/delete_asset`; pagination; tagging.

#### Requirement 7: Feature File Generation
- `generate_feature_file(style=EARS|Gherkin)`; write suggestions to workspace.

#### Requirement 8: FHIR Resource Generation
- `generate_fhir(target=PlanDefinition|CaseFeatureDefinition|Bundle)`; R4/R5 profile conformance.

#### Requirement 9: Rate Limiting and Resilience
- Per-key quotas; 429/503 errors; retries with backoff; idempotency keys.

#### Requirement 10: Asset Summary and Metrics
- `metrics()` and `summarize_assets()`; coverage and dedupe stats.

#### Requirement 11: Configuration and Customization
- `get_config/set_config`; workspace and api-key scopes.

#### Requirement 12: Provenance and Traceability
- Include `provenance` block in all responses (source, hash, model, prompt_id, timestamps).

#### Requirement 16: Guideline Source Flexibility
- Accept `format` and selectors; html/md/pdf; transform to normalized internal model.

#### Requirement 17: Guideline Model Abstraction
- LLM provider abstraction; `provider` and `model` inputs; audit actual resolved model.

#### Requirement 13: Deduplication and Quality Control
- `dedupe_assets(threshold)` and `qc_validate(ruleset)`; emit SHACL/JSON Schema violations.

#### Requirement 14: Dry Run and Testing Support
- `dry_run` parameter for writes; `run_tests(suite_uri)` returns junit.xml.

#### Requirement 15: Error Handling and Logging
- Structured logs; correlation-ids; `get_logs(last_n)` tool.

---

## 9) Reference: Original Baseline Requirements (verbatim)

> The following content is included verbatim from the uploaded requirements.md to preserve original context.

---

# Requirements Document

## Introduction

This document specifies requirements for a Clinical Knowledge BDD Test Generation System that transforms clinical guideline content from any source into executable Behavior-Driven Development (BDD) test scenarios. The system analyzes clinical guideline content in various formats (structured markdown, XML, HTML, PDF, FHIR Composition) and generates comprehensive test scenarios covering clinical decision points, treatment recommendations, diagnostic tests, and patient safety considerations across multiple generation modes and fidelity levels.

The system supports the CIKG 4-Layer model (L0 Prose, L1 GSRL Triples, L2 RALL Assets, L3 WATL Workflows) and aligns with CDS usage scenarios to ensure generated tests are clinically relevant and standards-compliant.

## Glossary

- **System**: The Clinical Knowledge BDD Test Generation System
- **BDD**: Behavior-Driven Development - a software development approach using human-readable test scenarios
- **Guideline Source**: Any clinical guideline content in formats including structured markdown, XML, HTML, PDF, FHIR Composition, or proprietary formats (e.g., BMJ Best Practice, UpToDate, NICE guidelines)
- **Structured Content**: Clinical guideline content organized into sections such as diagnostic approach, investigations, treatment approach, monitoring, complications, prognosis
- **Content Manifest**: A JSON or YAML file describing available guideline sections, their locations, and metadata
- **Generation Mode**: A strategy for creating test scenarios (top-down, bottom-up, external, logic-derived)
- **Fidelity Level**: The depth of output artifacts (none, draft, full, full-fhir)
- **CDS Taxonomy**: Clinical Decision Support usage scenario classification system (e.g., 1.1.1 Differential Diagnosis, 1.1.2 Treatment Recommendation) as defined in CDS Usage Scenarios
- **Scenario Inventory**: A structured table listing all generated test scenarios with metadata
- **FHIR**: Fast Healthcare Interoperability Resources - a standard for healthcare data exchange
- **CIKG**: Clinical Intelligence Knowledge Graph - a 4-layer model for representing clinical guidelines (L0 Prose, L1 GSRL Triples, L2 RALL Assets, L3 WATL Workflows)
- **OpenEHR**: An open standard for electronic health records including archetypes (reusable clinical data models) and GDL (Guideline Definition Language)
- **FHIR-CPG**: HL7 FHIR Clinical Practice Guidelines implementation guide for computable guidelines
- **Guideline Model Adapter**: A pluggable component that translates a specific guideline representation model into a common format for scenario generation
- **PlanDefinition**: A FHIR resource representing a clinical workflow or protocol
- **ActivityDefinition**: A FHIR resource representing a specific clinical action
- **Gherkin**: A domain-specific language for writing BDD scenarios using Given/When/Then syntax
- **QA Agent**: An AI model that generates clinical test scenarios based on guideline content
- **Coverage Tier**: A quality threshold defining minimum scenario counts (low, medium, high)
- **Patient Fixture**: A structured representation of patient state used in test scenarios
- **Evidence Anchor**: A reference to the source guideline section supporting a scenario
- **Apply Readiness**: Status indicating whether a scenario can be executed (ready, blocked, needs-fixture, needs-data)
- **Decision Question**: The clinical question a scenario addresses (e.g., treatment_now, tests_now, refer_now, monitoring_frequency)

## Requirements

### Requirement 1: Content Discovery and Ingestion

**User Story:** As a clinical knowledge engineer, I want the System to discover and ingest clinical guideline content from multiple source formats, so that I can generate BDD scenarios from any guideline source without format-specific preprocessing.

#### Acceptance Criteria

1. WHEN a guideline source is provided, THE System SHALL accept content in formats including structured markdown, XML, HTML, PDF, FHIR Composition, and JSON manifests
2. WHEN a content manifest is provided, THE System SHALL parse the manifest to identify available guideline sections and their locations
3. WHEN manifest files are missing, THE System SHALL generate a content manifest by scanning the source directory for guideline files matching common patterns
4. WHEN guideline sections are incomplete or missing, THE System SHALL report content validation errors listing specific missing sections
5. WHERE content quality thresholds are defined, THE System SHALL validate that guideline content meets minimum section count and character count requirements

### Requirement 2: Multi-Mode Scenario Generation

**User Story:** As a clinical knowledge engineer, I want the System to generate test scenarios using multiple generation strategies, so that I can achieve comprehensive coverage of clinical decision points from different analytical perspectives.

#### Acceptance Criteria

1. WHERE top-down mode is enabled, THE System SHALL generate scenarios by analyzing raw guideline source documents holistically without section-level decomposition
2. WHERE bottom-up mode is enabled, THE System SHALL generate 3-5 scenarios per selected guideline section by analyzing structured clinical content at the section level
3. WHERE external mode is enabled, THE System SHALL incorporate scenarios from external risk catalysts such as FDA alerts, PubMed summaries, or other evidence sources
4. WHERE logic-derived mode is enabled, THE System SHALL infer decision pathways from guideline content and generate scenarios covering all logical paths
5. WHEN multiple modes are enabled, THE System SHALL execute each mode independently and merge results with deduplication

### Requirement 3: Section-Based Scenario Generation

**User Story:** As a clinical knowledge engineer, I want the System to generate multiple scenarios for each clinical guideline section, so that I can achieve exhaustive coverage of treatment options, diagnostic tests, and patient variations within each guideline area.

#### Acceptance Criteria

1. WHEN bottom-up mode is enabled with selected sections, THE System SHALL make separate generation calls for each selected guideline section
2. WHEN processing a guideline section, THE System SHALL generate 3-5 distinct scenarios covering different clinical decision points within that section
3. WHEN generating section-specific scenarios, THE System SHALL include the section name, type, and content in the generation prompt
4. WHEN scenarios are generated across multiple sections, THE System SHALL assign unique scenario IDs sequentially across all sections
5. WHEN section-based generation completes, THE System SHALL log the scenario count generated for each section

### Requirement 4: Fidelity-Based Output Control

**User Story:** As a clinical knowledge engineer, I want the System to support multiple output fidelity levels, so that I can control the depth of generated artifacts based on project phase and resource constraints.

#### Acceptance Criteria

1. WHERE fidelity level is "none", THE System SHALL skip all scenario generation and produce no output
2. WHERE fidelity level is "draft", THE System SHALL generate scenario inventory tables in JSON and Markdown formats only
3. WHERE fidelity level is "full", THE System SHALL generate scenario inventory plus Gherkin feature files grouped by CDS category
4. WHERE fidelity level is "full-fhir", THE System SHALL generate scenario inventory, feature files, and FHIR resources including PlanDefinition, ActivityDefinition, and Library
5. WHEN fidelity level is "draft", THE System SHALL default to top-down and external generation modes only

### Requirement 5: CDS Taxonomy Classification

**User Story:** As a clinical knowledge engineer, I want the System to automatically classify scenarios according to the CDS usage taxonomy, so that generated tests align with standard clinical decision support categories and can be organized systematically.

#### Acceptance Criteria

1. WHEN a scenario is generated, THE System SHALL analyze the decision question and expected actions to determine the appropriate CDS category
2. WHEN the decision question contains differential diagnosis keywords, THE System SHALL classify the scenario as CDS 1.1.1 Differential Diagnosis
3. WHEN the decision question contains treatment or medication keywords, THE System SHALL classify the scenario as CDS 1.1.2 Treatment Recommendation or 1.1.3 Drug Recommendation
4. WHEN the decision question contains test or investigation keywords, THE System SHALL classify the scenario as CDS 1.1.5 Diagnostic Test Recommendation
5. WHEN CDS classification is ambiguous, THE System SHALL default to the most common category (1.1.2 Treatment Recommendation) and log the classification decision

### Requirement 6: Scenario Inventory Management

**User Story:** As a clinical knowledge engineer, I want the System to produce structured scenario inventories with comprehensive metadata, so that I can review, prioritize, and track generated test scenarios before promoting them to executable tests.

#### Acceptance Criteria

1. WHEN scenario generation completes, THE System SHALL write a scenario inventory in JSON format containing all scenarios with required fields
2. WHEN scenario generation completes, THE System SHALL write a scenario inventory in Markdown table format for human review
3. WHEN writing scenario inventory, THE System SHALL include metadata fields: scenarioId, decisionQuestion, decisionTargetWindow, patientFixture, preconditions, triggers, expectedActions, timing, contraindications, evidenceAnchor, planDefinition, negativeAssertions, timingAssertions, applyReadiness, persona, status, generationMode
4. WHEN writing scenario inventory, THE System SHALL validate that applyReadiness values are limited to: ready, blocked, needs-fixture, needs-data
5. WHEN writing scenario inventory, THE System SHALL validate that status values are limited to: draft, ready, pending

### Requirement 7: Feature File Generation

**User Story:** As a clinical knowledge engineer, I want the System to generate Gherkin feature files grouped by CDS category, so that I can execute BDD tests organized by clinical decision support scenario type.

#### Acceptance Criteria

1. WHEN fidelity level is "full" or "full-fhir", THE System SHALL generate Gherkin feature files for all scenarios
2. WHEN generating feature files, THE System SHALL group scenarios by CDS category with one feature file per category
3. WHEN generating a feature file, THE System SHALL include a Feature header with the CDS category title and topic name
4. WHEN generating a scenario within a feature file, THE System SHALL format it using Gherkin syntax with Given/When/Then steps
5. WHEN generating a scenario, THE System SHALL include metadata comments with scenario ID, CDS category, generation mode, and evidence anchor

### Requirement 8: FHIR Resource Generation

**User Story:** As a clinical informaticist, I want the System to generate FHIR-compliant resources for clinical decision support scenarios, so that generated tests can be integrated with FHIR-based clinical systems and validated against FHIR specifications.

#### Acceptance Criteria

1. WHEN fidelity level is "full-fhir", THE System SHALL generate PlanDefinition resources for each CDS category group
2. WHEN generating PlanDefinition resources, THE System SHALL include actions for each scenario with condition expressions and dynamic values
3. WHEN fidelity level is "full-fhir", THE System SHALL generate ActivityDefinition resources for scenarios with specific expected actions
4. WHEN fidelity level is "full-fhir", THE System SHALL generate Library resources containing CDS logic and evidence references
5. WHEN FHIR resources are generated, THE System SHALL validate JSON structure and write a validation report with results for each resource

### Requirement 9: Rate Limiting and Resilience

**User Story:** As a clinical knowledge engineer, I want the System to handle API rate limits gracefully with automatic model fallback, so that large-scale scenario generation can complete successfully despite provider constraints.

#### Acceptance Criteria

1. WHEN an API rate limit error occurs, THE System SHALL detect the error by checking for "rate limit", "429", or "too many requests" in the error message
2. WHEN a rate limit is detected, THE System SHALL attempt to switch to a fallback model in the sequence: gpt-4o → gpt-4o-mini → gpt-3.5-turbo
3. WHEN switching to a fallback model, THE System SHALL log the model change and rate limit attempt count
4. WHEN all fallback models are exhausted, THE System SHALL implement exponential backoff with a maximum wait time of 5 minutes
5. WHEN API errors occur that are not rate limits, THE System SHALL retry with exponential backoff up to the configured maximum retry count

### Requirement 10: Asset Summary and Metrics

**User Story:** As a clinical knowledge engineer, I want the System to generate comprehensive asset summaries with enhanced metrics, so that I can assess scenario quality, identify coverage gaps, and optimize generation efficiency.

#### Acceptance Criteria

1. WHEN scenario generation completes successfully, THE System SHALL generate an asset summary report in Markdown format
2. WHEN generating an asset summary, THE System SHALL include counts for feature files, total scenarios, generation modes used, and CDS categories covered
3. WHERE enhanced metrics are enabled, THE System SHALL analyze scenario complexity by counting Given/When/Then steps and categorizing as Simple/Moderate/Complex/Very Complex
4. WHERE enhanced metrics are enabled, THE System SHALL identify coverage gaps by listing missing generation modes and CDS categories
5. WHERE enhanced metrics are enabled, THE System SHALL estimate generation efficiency including API calls, token consumption, success rate, and provide actionable recommendations

### Requirement 11: Configuration and Customization

**User Story:** As a clinical knowledge engineer, I want the System to support flexible configuration through command-line arguments and configuration files, so that I can customize generation behavior for different topics and project requirements.

#### Acceptance Criteria

1. WHEN the System is invoked, THE System SHALL accept a topic identifier as a required positional argument
2. WHEN the System is invoked, THE System SHALL accept optional arguments for version, output directory, provider, model, temperature, max tokens, and max retries
3. WHEN a sections file is provided, THE System SHALL parse the Markdown table to determine which clinical sections to process
4. WHEN a coverage file is provided, THE System SHALL load coverage targets to guide scenario generation quantity and quality
5. WHEN generation mode is specified as a comma-separated list, THE System SHALL enable only the specified modes and disable others

### Requirement 12: Provenance and Traceability

**User Story:** As a clinical knowledge engineer, I want the System to maintain complete provenance for all generated scenarios, so that I can trace each test back to its source guideline content and generation parameters.

#### Acceptance Criteria

1. WHEN generating scenarios, THE System SHALL record the generation mode used for each scenario in the generationMode field
2. WHEN writing scenario inventory, THE System SHALL include source manifest paths and guideline source identifiers
3. WHEN writing scenario inventory, THE System SHALL include the list of guideline sections and source documents used
4. WHEN generating scenarios, THE System SHALL record evidence anchors linking each scenario to specific guideline sections with paragraph-level precision where available
5. WHEN a generation run completes, THE System SHALL create a timestamped run directory containing all prompts, agent responses, and output artifacts

### Requirement 16: Guideline Source Flexibility

**User Story:** As a clinical knowledge engineer, I want the System to work with guidelines from any publisher or format, so that I can generate BDD tests for BMJ Best Practice, NICE guidelines, UpToDate, WHO guidelines, or custom organizational protocols without vendor lock-in.

#### Acceptance Criteria

1. WHEN processing guideline content, THE System SHALL not require proprietary format-specific parsers or APIs
2. WHEN a guideline source uses custom section names, THE System SHALL accept a section mapping configuration to align with standard clinical section types
3. WHEN guideline content is provided in FHIR Composition format, THE System SHALL extract narrative text from section.text.div elements
4. WHEN guideline content is provided in XML or HTML, THE System SHALL extract text content while preserving section hierarchy
5. WHEN guideline content is provided in PDF, THE System SHALL accept pre-extracted text with section markers or use OCR/text extraction tools

### Requirement 17: Guideline Model Abstraction

**User Story:** As a clinical informaticist, I want the System to support multiple guideline representation models, so that I can generate BDD tests from guidelines structured according to CIKG 4-Layer, OpenEHR archetypes with GDL, HL7 FHIR-CPG, or other computable guideline frameworks.

#### Acceptance Criteria

1. WHEN the System processes guideline content, THE System SHALL use a pluggable adapter pattern to support multiple guideline models
2. WHERE CIKG 4-Layer model is used, THE System SHALL map L0 Prose, L1 GSRL Triples, L2 RALL Assets, and L3 WATL Workflows to scenario generation inputs
3. WHERE OpenEHR model is used, THE System SHALL extract clinical content from archetypes and GDL (Guideline Definition Language) rules
4. WHERE FHIR-CPG model is used, THE System SHALL extract content from PlanDefinition, ActivityDefinition, and Library resources
5. WHEN a new guideline model is added, THE System SHALL require only a new adapter implementation without changes to core scenario generation logic

### Requirement 13: Deduplication and Quality Control

**User Story:** As a clinical knowledge engineer, I want the System to detect and prevent duplicate scenarios across generation modes and sections, so that the final scenario inventory contains only unique, high-quality test cases.

#### Acceptance Criteria

1. WHEN loading prior scenario inventories, THE System SHALL extract existing scenarios for deduplication comparison
2. WHEN generating new scenarios, THE System SHALL check for duplicate scenario IDs and log conflicts
3. WHEN generating new scenarios, THE System SHALL check for similar decision questions and log potential duplicates
4. WHEN duplicate scenarios are detected, THE System SHALL include duplicate analysis in the generation report
5. WHEN scenario quality thresholds are defined, THE System SHALL validate that generated scenarios meet minimum complexity and completeness requirements

### Requirement 14: Dry Run and Testing Support

**User Story:** As a clinical knowledge engineer, I want the System to support dry-run mode with deterministic placeholder output, so that I can test the generation pipeline without consuming API credits or waiting for model responses.

#### Acceptance Criteria

1. WHERE dry-run mode is enabled, THE System SHALL generate deterministic placeholder scenario inventory without calling the QA agent
2. WHEN dry-run mode is enabled, THE System SHALL include at least one sample scenario with all required fields populated
3. WHEN dry-run mode is enabled, THE System SHALL write output files in the same format as production runs
4. WHEN dry-run mode is enabled, THE System SHALL log that placeholder data is being used instead of real API calls
5. WHEN skip-agent flag is set, THE System SHALL generate prompts and scaffolding but skip QA agent invocation

### Requirement 15: Error Handling and Logging

**User Story:** As a clinical knowledge engineer, I want the System to provide clear error messages and structured logging, so that I can diagnose issues quickly and understand generation progress in real-time.

#### Acceptance Criteria

1. WHEN content validation fails, THE System SHALL raise a RuntimeError with a formatted list of specific validation errors
2. WHEN API calls fail after all retries, THE System SHALL raise a RuntimeError with the failure reason and retry count
3. WHEN the System executes, THE System SHALL log messages in the format: timestamp | level | message
4. WHEN processing sections, THE System SHALL log INFO messages for each section being processed and scenario counts generated
5. WHEN errors occur, THE System SHALL log WARNING or ERROR messages with sufficient context for debugging

HH 2025-11-07


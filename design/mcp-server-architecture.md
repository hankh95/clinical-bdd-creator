# MCP Server Architecture Design

## Overview

The MCP (Model Context Protocol) Server is the primary interface for the Clinical BDD Creator system, providing JSON-RPC endpoints for external clients including IDEs, automation tools, and clinical development environments. The server orchestrates the transformation of clinical decision support (CDS) content into Behavior-Driven Development (BDD) test scenarios.

## Architecture Principles

### Design Goals
- **Standards Compliance**: Full MCP protocol implementation with JSON-RPC 2.0
- **Modular Design**: Clean separation of concerns with pluggable components
- **Asynchronous Processing**: Non-blocking operations for large clinical content processing
- **Configuration Flexibility**: Runtime-configurable coverage targets and processing options
- **Error Resilience**: Comprehensive error handling with meaningful error messages
- **Performance Optimized**: Efficient resource usage with caching and connection pooling

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ RPC Router  │  │ Request     │  │ Response    │         │
│  │             │  │ Processor   │  │ Handler     │         │
│  │ • Method    │  │ • Validation │  │ • Formatting │         │
│  │ • Routing   │  │ • Parsing   │  │ • Streaming  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Coverage    │  │ CIKG        │  │ BDD        │         │
│  │ Manager     │  │ Processor   │  │ Generator  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Config      │  │ Cache       │  │ Monitoring │         │
│  │ Service     │  │ Manager     │  │ Service    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## JSON-RPC Interface Specification

### Core Methods

#### 1. `initialize`
**Purpose**: Initialize the MCP server and negotiate capabilities

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "coverage": {
        "supported": true,
        "tiers": ["basic", "standard", "comprehensive"]
      },
      "processing": {
        "async": true,
        "streaming": true
      }
    },
    "clientInfo": {
      "name": "vscode",
      "version": "1.94.0"
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "coverage": {
        "configure": true,
        "validate": true,
        "tiers": ["basic", "standard", "comprehensive"]
      },
      "processing": {
        "async": true,
        "progress": true,
        "cancellation": true
      },
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "clinical-bdd-creator",
      "version": "0.1.0"
    }
  }
}
```

#### 2. `configure_coverage`
**Purpose**: Configure coverage targets and category mappings

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "configure_coverage",
  "params": {
    "tier": "standard",
    "categories": {
      "treatment_recommendation": "high",
      "diagnostic_test": "medium",
      "medication_management": "high"
    },
    "overrides": {
      "scenario_1.1.1": {
        "priority": "critical",
        "custom_categories": ["cardiology"]
      }
    }
  }
}
```

#### 3. `process_scenario`
**Purpose**: Process a CDS scenario into BDD test specifications

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "process_scenario",
  "params": {
    "scenarioId": "1.1.1",
    "content": {
      "title": "Hypertension Management",
      "description": "Blood pressure assessment and treatment recommendations",
      "clinical_content": "When systolic BP ≥ 140 mmHg or diastolic BP ≥ 90 mmHg...",
      "context": {
        "patient_age": "18-80",
        "conditions": ["essential_hypertension"],
        "medications": []
      }
    },
    "options": {
      "format": "gherkin",
      "include_negative_scenarios": true,
      "coverage_targets": ["basic", "edge_cases"]
    }
  }
}
```

**Response** (Streaming):
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "status": "processing",
    "progress": {
      "stage": "cikg_processing",
      "percentage": 45,
      "message": "Extracting clinical concepts..."
    }
  }
}
```

**Final Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "status": "completed",
    "scenario": {
      "id": "1.1.1",
      "title": "Hypertension Management",
      "gherkin": "@hypertension @treatment_recommendation\nFeature: Hypertension Management\n\n  @basic @positive\n  Scenario: Patient with elevated blood pressure receives treatment recommendation\n    Given a patient with systolic blood pressure of 150 mmHg\n    And diastolic blood pressure of 95 mmHg\n    When the hypertension assessment is performed\n    Then a treatment recommendation should be provided\n    And the recommendation should include medication options\n\n  @edge_case @negative\n  Scenario: Patient with normal blood pressure receives no treatment\n    Given a patient with systolic blood pressure of 120 mmHg\n    And diastolic blood pressure of 80 mmHg\n    When the hypertension assessment is performed\n    Then no treatment recommendation should be provided",
      "metadata": {
        "coverage_categories": ["treatment_recommendation"],
        "clinical_concepts": ["blood_pressure", "hypertension", "medication"],
        "validation_status": "passed"
      }
    }
  }
}
```

#### 4. `validate_coverage`
**Purpose**: Validate coverage completeness for a set of scenarios

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "validate_coverage",
  "params": {
    "scenarios": ["1.1.1", "1.1.2", "2.1.1"],
    "requirements": {
      "min_coverage": 0.95,
      "required_categories": ["treatment_recommendation", "diagnostic_test"],
      "tier": "standard"
    }
  }
}
```

#### 5. `get_status`
**Purpose**: Get server status and active processing jobs

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "get_status",
  "params": {}
}
```

## Component Design

### RPC Router
**Responsibilities**:
- Method dispatch and routing
- Request validation
- Error handling and formatting
- Connection management

**Key Features**:
- Method registration system
- Parameter validation schemas
- Error code standardization
- Connection pooling

### Request Processor
**Responsibilities**:
- Parse and validate incoming requests
- Coordinate with internal components
- Manage asynchronous processing
- Handle request cancellation

**Processing Flow**:
```
Request → Validation → Routing → Processing → Response
    ↓         ↓         ↓         ↓         ↓
  Parse →  Schema →  Method →  Async →  Format
  JSON    Check    Lookup   Queue   Result
```

### Coverage Manager
**Responsibilities**:
- Load and validate coverage configurations
- Apply tier-based filtering
- Category mapping and validation
- Configuration persistence

**Configuration Sources**:
1. Default project configuration
2. Runtime parameter overrides
3. Client-specific preferences
4. Per-request customizations

### CIKG Processor
**Responsibilities**:
- Orchestrate 4-layer CIKG processing
- Clinical concept extraction
- Knowledge graph construction
- Workflow synthesis

**Integration Points**:
- Clinical terminology services
- FHIR resource processing
- Knowledge base integration
- Validation services

### BDD Generator
**Responsibilities**:
- Gherkin scenario generation
- Template application
- Test validation
- Coverage analysis

**Template System**:
- Scenario templates by CDS pattern
- Custom template support
- Template validation rules
- Dynamic template selection

## Error Handling

### Error Categories
- **Validation Errors**: Invalid request parameters or content
- **Processing Errors**: Issues during CIKG or BDD generation
- **Configuration Errors**: Invalid coverage or system configuration
- **System Errors**: Internal server or resource issues

### Error Response Format
```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "Coverage tier 'invalid' is not supported",
      "valid_values": ["basic", "standard", "comprehensive"],
      "field": "tier"
    }
  }
}
```

## Performance Considerations

### Asynchronous Processing
- Large clinical content processing
- External service calls
- Resource-intensive operations

### Caching Strategy
- Clinical concept caching
- Template caching
- Configuration caching
- Result caching with TTL

### Connection Management
- Connection pooling for external services
- Request throttling and rate limiting
- Connection health monitoring
- Automatic reconnection logic

## Security Design

### Input Validation
- JSON schema validation for all requests
- Clinical content sanitization
- Parameter bounds checking
- Content size limits

### Access Control
- Client authentication (future)
- Request authorization
- Resource access controls
- Audit logging

### Data Protection
- Clinical content encryption
- Secure configuration storage
- PHI data handling
- Compliance logging

## Implementation Plan

### Phase 1: Core Infrastructure
- [ ] Basic MCP server setup with FastAPI
- [ ] JSON-RPC method routing
- [ ] Request/response handling
- [ ] Error handling framework

### Phase 2: Core Functionality
- [ ] Coverage configuration management
- [ ] Basic CIKG processing integration
- [ ] Simple BDD generation
- [ ] Status and monitoring endpoints

### Phase 3: Advanced Features
- [ ] Asynchronous processing
- [ ] Streaming responses
- [ ] Advanced error handling
- [ ] Performance optimization

### Phase 4: Production Readiness
- [ ] Comprehensive testing
- [ ] Security hardening
- [ ] Performance benchmarking
- [ ] Documentation completion</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/clinical-bdd-creator/design/mcp-server-architecture.md
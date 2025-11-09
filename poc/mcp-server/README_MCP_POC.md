# MCP Server POC

**Status:** ✅ Complete and Tested  
**Purpose:** Demonstrate basic MCP server with coverage configuration and scenario processing

## Overview

This POC implements a minimal MCP (Model Context Protocol) server following JSON-RPC 2.0 over stdio. It provides endpoints for coverage configuration and clinical scenario processing, integrating with the BDD Generator POC.

## Features

- ✅ JSON-RPC 2.0 over stdio (MCP protocol)
- ✅ Server initialization and capability negotiation
- ✅ Coverage configuration (tiered strategy, category mappings)
- ✅ Scenario processing with BDD generation
- ✅ Status reporting and health checks
- ✅ Proper error handling and responses

## Quick Start

### Start MCP Server

```bash
# Start server (reads from stdin, writes to stdout)
python3 poc_mcp_server.py

# Server will wait for JSON-RPC requests on stdin
```

### Test with Client

```bash
# Run client test suite
python3 mcp_client_test.py

# Expected output:
# ================================================================================
# MCP SERVER POC - CLIENT TEST SUITE
# ================================================================================
# ✓ MCP Server started
# [TEST] Initialize
#   ✓ Server initialized
# ...
# ✓ ALL TESTS PASSED
```

### Run Integration Tests

```bash
# Run full integration test suite
python3 test_mcp_poc.py

# Expected: 8/8 tests passed in < 5 seconds
```

## MCP Methods

### 1. initialize

Perform server capability negotiation.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {},
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "1.0",
    "capabilities": {
      "scenarios": {
        "generation": true,
        "formats": ["gherkin"],
        "modes": ["positive", "negative"]
      },
      "coverage": {
        "tiered": true,
        "categories": true
      }
    },
    "serverInfo": {
      "name": "Clinical BDD Creator MCP Server POC",
      "version": "0.1.0"
    }
  },
  "id": 1
}
```

### 2. configure_coverage

Set coverage parameters for scenario generation.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "configure_coverage",
  "params": {
    "strategy": "tiered",
    "default_tier": "high",
    "category_mappings": {
      "treatment_recommendation": "high",
      "diagnostic_test": "medium"
    }
  },
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "configured",
    "configuration": {
      "strategy": "tiered",
      "default_tier": "high",
      "category_mappings": {
        "treatment_recommendation": "high",
        "diagnostic_test": "medium"
      }
    }
  },
  "id": 2
}
```

### 3. process_scenario

Process a clinical scenario and generate BDD.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "process_scenario",
  "params": {
    "scenario": {
      "scenario": "Hypertension Management",
      "condition": "systolic BP >= 140 mmHg",
      "action": "initiate ACE inhibitor therapy",
      "context": "adult patient, no contraindications"
    }
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "success",
    "gherkin": "Feature: Hypertension Management\n\n  @positive @treatment\n  ...",
    "metadata": {
      "scenarios_generated": 2,
      "format": "gherkin",
      "coverage_tier": "high"
    }
  },
  "id": 3
}
```

### 4. get_status

Get current server status and health.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "get_status",
  "params": {},
  "id": 4
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "initialized": true,
    "active_jobs": 0,
    "scenarios_processed": 1,
    "coverage_configured": true,
    "server_healthy": true
  },
  "id": 4
}
```

## Architecture

```
poc_mcp_server.py
├── MCPServer (class)
│   ├── start() - Main server loop
│   ├── handle_request() - Route JSON-RPC requests
│   ├── handle_initialize() - Capability negotiation
│   ├── handle_configure_coverage() - Coverage config
│   ├── handle_process_scenario() - Scenario processing
│   └── handle_get_status() - Status reporting
│
├── CoverageConfig (dataclass)
│   └── Coverage configuration parameters
│
└── ServerStatus (dataclass)
    └── Current server state
```

## Integration with BDD Generator

The MCP Server integrates with POC 1 (BDD Generator):

```python
from poc_bdd_generator import BDDGenerator

# Server uses BDD generator for scenario processing
self.bdd_generator = BDDGenerator()
gherkin = self.bdd_generator.generate_from_json(scenario)
```

## Error Handling

The server follows JSON-RPC 2.0 error codes:

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Missing required fields |
| -32601 | Method not found | Unknown method |
| -32603 | Internal error | Server-side error |

## Testing

### Test Coverage

**Client Tests (mcp_client_test.py):** 4 test scenarios
1. ✅ Initialize server
2. ✅ Configure coverage
3. ✅ Process scenario
4. ✅ Get status

**Integration Tests (test_mcp_poc.py):** 8 test cases
1. ✅ Server initialization
2. ✅ Valid coverage configuration
3. ✅ Invalid strategy handling
4. ✅ Successful scenario processing
5. ✅ Missing parameter handling
6. ✅ Status retrieval
7. ✅ Invalid method handling
8. ✅ JSON-RPC version validation

### Running Tests

```bash
# Client tests (requires server start/stop)
python3 mcp_client_test.py

# Integration tests (automated server lifecycle)
python3 test_mcp_poc.py
```

## Performance

- **Request Processing**: < 50ms per request
- **Scenario Generation**: < 100ms per scenario
- **Server Startup**: < 100ms
- **Memory Usage**: < 20MB

## Design Decisions

### 1. stdio Transport

Using stdin/stdout for JSON-RPC enables:
- Simple process-to-process communication
- Easy integration with shell scripts
- Standard MCP protocol compliance

### 2. Stateful Server

The server maintains state for:
- Initialization status
- Coverage configuration
- Active jobs count
- Processed scenarios count

### 3. Integration with POC 1

Direct integration with BDD Generator POC provides:
- Reusable components
- Consistent output format
- Reduced code duplication

## Limitations and Future Enhancements

### Current Limitations

1. **Single Process**: No concurrent request handling
2. **Memory State**: No persistent storage
3. **Limited Validation**: Basic input validation only
4. **No Authentication**: No security layer

### Potential Enhancements

1. **Async Processing**: Support concurrent requests
2. **Persistent State**: Database or file-based storage
3. **Enhanced Validation**: Schema-based input validation
4. **Authentication**: API key or token-based auth
5. **Batch Processing**: Handle multiple scenarios efficiently
6. **Monitoring**: Metrics and logging infrastructure

## Integration Points

This POC integrates with:

1. **BDD Generator POC**: Uses for scenario generation
2. **CIKG Processor POC**: Will accept CIKG output
3. **Integration Test Framework**: Validates end-to-end flow

## Dependencies

- **Standard Library**: json, sys, subprocess, pathlib, typing, dataclasses
- **POC 1**: BDD Generator (`poc_bdd_generator.py`)

## Success Criteria

✅ All success criteria met:

- [x] Runnable and testable within 5 minutes
- [x] Demonstrates MCP protocol with JSON-RPC 2.0
- [x] Integrates with BDD Generator POC
- [x] Handles configuration parameters correctly
- [x] Provides proper error responses
- [x] Well-documented with examples
- [x] All tests pass (12/12)

## Troubleshooting

### Issue: Server not responding

**Solution**: Check that server is reading from stdin:
```bash
# Test with echo
echo '{"jsonrpc":"2.0","method":"get_status","id":1}' | python3 poc_mcp_server.py
```

### Issue: Import error for BDD Generator

**Solution**: Ensure POC 1 is in parent directory:
```bash
ls -la ../bdd-generator/poc_bdd_generator.py
```

### Issue: Tests hanging

**Solution**: Use timeout with tests:
```bash
timeout 30 python3 test_mcp_poc.py
```

## Next Steps

1. **CIKG Integration**: Accept L1 GSRL triples as input
2. **Batch Processing**: Handle multiple scenarios efficiently
3. **WebSocket Transport**: Alternative to stdio for web clients
4. **State Persistence**: Save configuration and status
5. **Enhanced Error Handling**: More detailed error messages

## Contact

This POC was developed as part of Phase 5B: POC Development for the Clinical BDD Creator project.

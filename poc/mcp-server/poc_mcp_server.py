#!/usr/bin/env python3
"""
MCP Server POC - Basic Model Context Protocol Server

This POC implements a minimal MCP server following the JSON-RPC 2.0 protocol
over stdio. It provides coverage configuration and scenario processing endpoints.

Protocol: MCP (Model Context Protocol)
Transport: stdio (JSON-RPC 2.0)
Author: GitHub Copilot
Date: 2025-11-09
"""

import json
import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Import BDD generator from POC 1
sys.path.insert(0, str(Path(__file__).parent.parent / "bdd-generator"))
from poc_bdd_generator import BDDGenerator


@dataclass
class CoverageConfig:
    """Coverage configuration for scenario generation"""
    strategy: str = "tiered"  # tiered, all, minimal
    default_tier: str = "medium"  # none, low, medium, high, very-high
    category_mappings: Dict[str, str] = None
    
    def __post_init__(self):
        if self.category_mappings is None:
            self.category_mappings = {}


@dataclass
class ServerStatus:
    """Current server status"""
    initialized: bool = False
    active_jobs: int = 0
    scenarios_processed: int = 0
    coverage_config: Optional[CoverageConfig] = None


class MCPServer:
    """
    Basic MCP Server implementing JSON-RPC 2.0 over stdio
    
    Supported Methods:
    - initialize: Server capability negotiation
    - configure_coverage: Set coverage parameters
    - process_scenario: Process single scenario to BDD
    - get_status: Report server health and active jobs
    """
    
    def __init__(self):
        self.status = ServerStatus()
        self.bdd_generator = BDDGenerator()
        self.request_id = 0
        
    def start(self):
        """Start MCP server loop reading from stdin"""
        sys.stderr.write("MCP Server POC starting...\n")
        sys.stderr.flush()
        
        try:
            for line in sys.stdin:
                if not line.strip():
                    continue
                    
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    self.send_response(response)
                except json.JSONDecodeError as e:
                    self.send_error(-32700, f"Parse error: {str(e)}", None)
                except Exception as e:
                    sys.stderr.write(f"Error handling request: {e}\n")
                    sys.stderr.flush()
        except KeyboardInterrupt:
            sys.stderr.write("\nMCP Server shutting down...\n")
            sys.stderr.flush()
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 request"""
        # Validate JSON-RPC 2.0 structure
        if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
            return self.create_error_response(
                -32600, "Invalid Request: missing or invalid jsonrpc version", 
                request.get("id")
            )
        
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if not method:
            return self.create_error_response(
                -32600, "Invalid Request: missing method", request_id
            )
        
        # Route to appropriate handler
        handlers = {
            "initialize": self.handle_initialize,
            "configure_coverage": self.handle_configure_coverage,
            "process_scenario": self.handle_process_scenario,
            "get_status": self.handle_get_status,
        }
        
        handler = handlers.get(method)
        if not handler:
            return self.create_error_response(
                -32601, f"Method not found: {method}", request_id
            )
        
        try:
            result = handler(params)
            return self.create_success_response(result, request_id)
        except Exception as e:
            return self.create_error_response(
                -32603, f"Internal error: {str(e)}", request_id
            )
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request - server capability negotiation"""
        self.status.initialized = True
        
        return {
            "protocolVersion": "1.0",
            "capabilities": {
                "scenarios": {
                    "generation": True,
                    "formats": ["gherkin"],
                    "modes": ["positive", "negative"]
                },
                "coverage": {
                    "tiered": True,
                    "categories": True
                }
            },
            "serverInfo": {
                "name": "Clinical BDD Creator MCP Server POC",
                "version": "0.1.0"
            }
        }
    
    def handle_configure_coverage(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle configure_coverage request"""
        if not self.status.initialized:
            raise Exception("Server not initialized")
        
        # Extract coverage configuration
        strategy = params.get("strategy", "tiered")
        default_tier = params.get("default_tier", "medium")
        category_mappings = params.get("category_mappings", {})
        
        # Validate configuration
        valid_strategies = ["tiered", "all", "minimal"]
        valid_tiers = ["none", "low", "medium", "high", "very-high"]
        
        if strategy not in valid_strategies:
            raise Exception(f"Invalid strategy: {strategy}")
        
        if default_tier not in valid_tiers:
            raise Exception(f"Invalid tier: {default_tier}")
        
        # Update server configuration
        self.status.coverage_config = CoverageConfig(
            strategy=strategy,
            default_tier=default_tier,
            category_mappings=category_mappings
        )
        
        return {
            "status": "configured",
            "configuration": asdict(self.status.coverage_config)
        }
    
    def handle_process_scenario(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle process_scenario request"""
        if not self.status.initialized:
            raise Exception("Server not initialized")
        
        # Extract scenario data
        scenario = params.get("scenario")
        if not scenario:
            raise Exception("Missing scenario parameter")
        
        # Increment active jobs
        self.status.active_jobs += 1
        
        try:
            # Generate BDD using POC 1
            gherkin = self.bdd_generator.generate_from_json(scenario)
            
            # Update statistics
            self.status.scenarios_processed += 1
            
            result = {
                "status": "success",
                "gherkin": gherkin,
                "metadata": {
                    "scenarios_generated": self.bdd_generator.scenarios_generated,
                    "format": "gherkin",
                    "coverage_tier": self.status.coverage_config.default_tier if self.status.coverage_config else "not_configured"
                }
            }
            
            return result
            
        finally:
            self.status.active_jobs -= 1
    
    def handle_get_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_status request"""
        return {
            "initialized": self.status.initialized,
            "active_jobs": self.status.active_jobs,
            "scenarios_processed": self.status.scenarios_processed,
            "coverage_configured": self.status.coverage_config is not None,
            "server_healthy": True
        }
    
    def create_success_response(self, result: Any, request_id: Any) -> Dict[str, Any]:
        """Create JSON-RPC 2.0 success response"""
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
    
    def create_error_response(self, code: int, message: str, request_id: Any) -> Dict[str, Any]:
        """Create JSON-RPC 2.0 error response"""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }
    
    def send_response(self, response: Dict[str, Any]):
        """Send JSON-RPC response to stdout"""
        json.dump(response, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()
    
    def send_error(self, code: int, message: str, request_id: Any):
        """Send error response"""
        response = self.create_error_response(code, message, request_id)
        self.send_response(response)


def main():
    """Start MCP server"""
    server = MCPServer()
    server.start()


if __name__ == "__main__":
    main()

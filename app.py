#!/usr/bin/env python3
"""
Clinical BDD Creator - Production Web Application
Provides REST API endpoints and health checks for production deployment.
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import json
from pathlib import Path

from dataclasses import asdict

# Import our modules
from integration_test_runner import IntegrationTestRunner
from guideline_analyzer import GuidelineAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/clinical_bdd.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables
test_runner = None
guideline_analyzer = None

def initialize_services():
    """Initialize application services"""
    global test_runner, guideline_analyzer

    try:
        # Initialize test runner with monitoring
        config = {
            "monitoring_enabled": True,
            "prometheus_port": int(os.getenv('PROMETHEUS_PORT', 8000)),
            "output_dir": "/app/test-reports"
        }
        test_runner = IntegrationTestRunner(config)
        logger.info("Test runner initialized with monitoring")

        # Initialize guideline analyzer
        guideline_analyzer = GuidelineAnalyzer()
        logger.info("Guideline analyzer initialized")

        return True
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Basic health checks
        services_healthy = {
            "test_runner": test_runner is not None,
            "guideline_analyzer": guideline_analyzer is not None,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Overall health status
        all_healthy = all(services_healthy.values())

        status_code = 200 if all_healthy else 503
        status = "healthy" if all_healthy else "unhealthy"

        response = {
            "status": status,
            "services": services_healthy,
            "version": "1.0.0",
            "environment": os.getenv('ENVIRONMENT', 'development')
        }

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_guideline():
    """Analyze a clinical guideline"""
    try:
        if not guideline_analyzer:
            return jsonify({"error": "Guideline analyzer not available"}), 503

        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({"error": "Missing 'content' field in request"}), 400

        content = data['content']
        specialty = data.get('specialty', 'general')

        # Analyze guideline
        result = guideline_analyzer.analyze_guideline(content, specialty)

        return jsonify({
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Guideline analysis failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/v1/test/run', methods=['POST'])
def run_tests():
    """Run integration tests"""
    try:
        if not test_runner:
            return jsonify({"error": "Test runner not available"}), 503

        # Run tests
        results = test_runner.run_all_test_suites()

        # Generate summary
        total_tests = sum(r.tests_run for r in results)
        total_passed = sum(r.tests_passed for r in results)
        total_failed = sum(r.tests_failed for r in results)
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        return jsonify({
            "status": "completed",
            "summary": {
                "total_tests": total_tests,
                "passed": total_passed,
                "failed": total_failed,
                "success_rate": round(success_rate, 2)
            },
            "results": [asdict(r) for r in results],
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/v1/metrics', methods=['GET'])
def get_metrics():
    """Get application metrics"""
    try:
        # Collect current system metrics
        if test_runner:
            test_runner._collect_system_metrics()

        return jsonify({
            "status": "success",
            "metrics": {
                "uptime": "monitoring_enabled",  # Prometheus handles detailed metrics
                "last_test_run": getattr(test_runner, 'end_time', None),
                "environment": os.getenv('ENVIRONMENT', 'development')
            },
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Clinical BDD Creator",
        "version": "1.0.0",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "endpoints": {
            "health": "/health",
            "analyze": "POST /api/v1/analyze",
            "run_tests": "POST /api/v1/test/run",
            "metrics": "/api/v1/metrics"
        },
        "documentation": "See PRODUCTION-README.md",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/health",
            "/api/v1/analyze",
            "/api/v1/test/run",
            "/api/v1/metrics"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "timestamp": datetime.utcnow().isoformat()
    }), 500

if __name__ == '__main__':
    # Initialize services
    if not initialize_services():
        logger.error("Failed to initialize services. Exiting.")
        sys.exit(1)

    # Start the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'

    logger.info(f"Starting Clinical BDD Creator on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
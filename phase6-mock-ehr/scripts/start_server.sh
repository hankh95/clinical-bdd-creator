#!/bin/bash
#
# Start Mock EHR Server
# Phase 6 - Integration Testing
#

set -e

# Change to project directory
cd "$(dirname "$0")/.."

echo "========================================================================"
echo "Starting Mock EHR Server"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Start server
echo "Starting server on http://localhost:5000"
echo ""
echo "Available endpoints:"
echo "  - Root:              http://localhost:5000/"
echo "  - Health Check:      http://localhost:5000/health"
echo "  - CDS Services:      http://localhost:5000/cds-services"
echo "  - FHIR Metadata:     http://localhost:5000/fhir/metadata"
echo "  - FHIR Patient:      http://localhost:5000/fhir/Patient"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================================================"
echo ""

python3 server/mock_ehr_server.py

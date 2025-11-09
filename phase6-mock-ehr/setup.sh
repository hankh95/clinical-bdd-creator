#!/bin/bash
#
# Setup script for Mock EHR Server
# Phase 6 - Integration Testing
#

set -e

echo "========================================================================"
echo "Mock EHR Server - Setup"
echo "========================================================================"
echo ""

# Check Python version
echo "[1/4] Checking Python version..."
python3 --version || { echo "Error: Python 3 is required"; exit 1; }
echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "[3/4] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r config/requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Verify test data
echo "[4/4] Verifying test data..."
test_files=("patients.json" "encounters.json" "conditions.json" "observations.json" "medication_requests.json")
all_present=true
for file in "${test_files[@]}"; do
    if [ -f "test_data/$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        all_present=false
    fi
done
echo ""

if [ "$all_present" = true ]; then
    echo "========================================================================"
    echo "✓ Setup complete!"
    echo "========================================================================"
    echo ""
    echo "To start the server:"
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Run server: python3 server/mock_ehr_server.py"
    echo ""
    echo "Or use the convenience script:"
    echo "  ./scripts/start_server.sh"
    echo ""
else
    echo "========================================================================"
    echo "⚠️  Setup incomplete - some test data files are missing"
    echo "========================================================================"
    exit 1
fi

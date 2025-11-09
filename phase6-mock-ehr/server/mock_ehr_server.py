#!/usr/bin/env python3
"""
Mock EHR Server with CDS Hooks and FHIR Support

This server implements:
- CDS Hooks v1.0 specification
- FHIR R4 resource endpoints
- Mock patient and clinical data
- Integration testing support

Author: GitHub Copilot
Date: 2025-11-09
Phase: 6 - Integration Testing
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load test data fixtures
DATA_DIR = Path(__file__).parent.parent / "test_data"

# In-memory storage for simplicity
PATIENTS = {}
ENCOUNTERS = {}
CONDITIONS = {}
OBSERVATIONS = {}
MEDICATION_REQUESTS = {}


def load_test_data():
    """Load test data fixtures from JSON files"""
    global PATIENTS, ENCOUNTERS, CONDITIONS, OBSERVATIONS, MEDICATION_REQUESTS
    
    try:
        with open(DATA_DIR / "patients.json", "r") as f:
            PATIENTS = {p["id"]: p for p in json.load(f)}
        
        with open(DATA_DIR / "encounters.json", "r") as f:
            ENCOUNTERS = {e["id"]: e for e in json.load(f)}
        
        with open(DATA_DIR / "conditions.json", "r") as f:
            CONDITIONS = {c["id"]: c for c in json.load(f)}
        
        with open(DATA_DIR / "observations.json", "r") as f:
            OBSERVATIONS = {o["id"]: o for o in json.load(f)}
        
        with open(DATA_DIR / "medication_requests.json", "r") as f:
            MEDICATION_REQUESTS = {m["id"]: m for m in json.load(f)}
        
        print(f"✓ Loaded test data: {len(PATIENTS)} patients, {len(ENCOUNTERS)} encounters")
    except FileNotFoundError as e:
        print(f"⚠️  Test data not found: {e}")
        print("   Server will start with empty data stores")


# ============================================================================
# CDS Hooks Endpoints
# ============================================================================

@app.route('/cds-services', methods=['GET'])
def get_cds_services():
    """
    CDS Hooks Discovery endpoint
    Returns available CDS services
    """
    services = [
        {
            "hook": "patient-view",
            "title": "Clinical Decision Support - Patient View",
            "description": "Provides clinical decision support when viewing a patient record",
            "id": "patient-view-cds",
            "prefetch": {
                "patient": "Patient/{{context.patientId}}",
                "conditions": "Condition?patient={{context.patientId}}",
                "observations": "Observation?patient={{context.patientId}}&_sort=-date&_count=10"
            }
        },
        {
            "hook": "order-select",
            "title": "Clinical Decision Support - Order Selection",
            "description": "Provides guidance when selecting orders",
            "id": "order-select-cds",
            "prefetch": {
                "patient": "Patient/{{context.patientId}}",
                "medications": "MedicationRequest?patient={{context.patientId}}&status=active"
            }
        },
        {
            "hook": "medication-prescribe",
            "title": "Clinical Decision Support - Medication Prescribe",
            "description": "Provides guidance when prescribing medications",
            "id": "medication-prescribe-cds",
            "prefetch": {
                "patient": "Patient/{{context.patientId}}",
                "medications": "MedicationRequest?patient={{context.patientId}}&status=active",
                "conditions": "Condition?patient={{context.patientId}}"
            }
        }
    ]
    
    return jsonify({"services": services})


@app.route('/cds-services/<service_id>', methods=['POST'])
def call_cds_service(service_id):
    """
    CDS Hooks service endpoint
    Receives context and returns cards with recommendations
    """
    request_data = request.get_json()
    
    # Extract context
    hook = request_data.get("hook")
    context = request_data.get("context", {})
    prefetch = request_data.get("prefetch", {})
    
    # Get patient ID from context
    patient_id = context.get("patientId")
    
    if not patient_id:
        return jsonify({"cards": []}), 200
    
    # Generate appropriate cards based on service
    cards = []
    
    if service_id == "patient-view-cds":
        cards = generate_patient_view_cards(patient_id, prefetch)
    elif service_id == "order-select-cds":
        cards = generate_order_select_cards(patient_id, prefetch)
    elif service_id == "medication-prescribe-cds":
        cards = generate_medication_prescribe_cards(patient_id, context, prefetch)
    
    response = {
        "cards": cards
    }
    
    return jsonify(response), 200


def generate_patient_view_cards(patient_id: str, prefetch: Dict) -> List[Dict]:
    """Generate CDS cards for patient view"""
    cards = []
    
    # Get patient data
    patient = PATIENTS.get(patient_id)
    if not patient:
        return cards
    
    # Check for hypertension management
    patient_conditions = [c for c in CONDITIONS.values() if c.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    patient_observations = [o for o in OBSERVATIONS.values() if o.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    # Check for elevated BP
    bp_observations = [o for o in patient_observations if "blood pressure" in o.get("code", {}).get("text", "").lower()]
    if bp_observations:
        latest_bp = bp_observations[0]  # Assuming sorted by date
        systolic = None
        for component in latest_bp.get("component", []):
            if "systolic" in component.get("code", {}).get("text", "").lower():
                systolic = component.get("valueQuantity", {}).get("value")
        
        if systolic and systolic >= 140:
            cards.append({
                "summary": "Elevated Blood Pressure Detected",
                "indicator": "warning",
                "detail": f"Patient's systolic BP is {systolic} mmHg. Consider hypertension management.",
                "source": {
                    "label": "Clinical BDD Creator - Hypertension Guidelines"
                },
                "suggestions": [
                    {
                        "label": "Review hypertension management guideline",
                        "actions": [
                            {
                                "type": "create",
                                "description": "Order ACE inhibitor therapy evaluation"
                            }
                        ]
                    }
                ]
            })
    
    # Check for diabetes management
    hba1c_observations = [o for o in patient_observations if "hba1c" in o.get("code", {}).get("text", "").lower()]
    if hba1c_observations:
        latest_hba1c = hba1c_observations[0]
        hba1c_value = latest_hba1c.get("valueQuantity", {}).get("value")
        
        if hba1c_value and hba1c_value > 7.0:
            cards.append({
                "summary": "Elevated HbA1c - Diabetes Management Needed",
                "indicator": "warning",
                "detail": f"Patient's HbA1c is {hba1c_value}%. Consider initiating or adjusting diabetes therapy.",
                "source": {
                    "label": "Clinical BDD Creator - Diabetes Guidelines"
                },
                "suggestions": [
                    {
                        "label": "Review diabetes management guideline",
                        "actions": [
                            {
                                "type": "create",
                                "description": "Consider metformin initiation or dose adjustment"
                            }
                        ]
                    }
                ]
            })
    
    return cards


def generate_order_select_cards(patient_id: str, prefetch: Dict) -> List[Dict]:
    """Generate CDS cards for order selection"""
    cards = []
    
    # Example: Check for drug interactions
    patient_meds = [m for m in MEDICATION_REQUESTS.values() if m.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    if len(patient_meds) >= 2:
        cards.append({
            "summary": "Potential Drug Interaction",
            "indicator": "info",
            "detail": "Patient is on multiple medications. Review for potential interactions.",
            "source": {
                "label": "Clinical BDD Creator - Drug Interaction Checking"
            }
        })
    
    return cards


def generate_medication_prescribe_cards(patient_id: str, context: Dict, prefetch: Dict) -> List[Dict]:
    """Generate CDS cards for medication prescribing"""
    cards = []
    
    # Get medication being prescribed from context
    medications = context.get("medications", [])
    
    # Check for contraindications
    patient_conditions = [c for c in CONDITIONS.values() if c.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    for medication in medications:
        med_code = medication.get("medicationCodeableConcept", {}).get("text", "")
        
        # Check contraindications (simplified)
        if "ace inhibitor" in med_code.lower():
            # Check for hyperkalemia or renal disease
            has_contraindication = any(
                "hyperkalemia" in c.get("code", {}).get("text", "").lower() or
                "renal" in c.get("code", {}).get("text", "").lower()
                for c in patient_conditions
            )
            
            if has_contraindication:
                cards.append({
                    "summary": "Potential Contraindication for ACE Inhibitor",
                    "indicator": "critical",
                    "detail": "Patient may have contraindications for ACE inhibitor therapy. Review patient history.",
                    "source": {
                        "label": "Clinical BDD Creator - Medication Safety"
                    }
                })
    
    return cards


# ============================================================================
# FHIR R4 Endpoints
# ============================================================================

@app.route('/fhir/metadata', methods=['GET'])
def get_fhir_metadata():
    """FHIR Capability Statement"""
    metadata = {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": datetime.utcnow().isoformat(),
        "kind": "instance",
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {"type": "Patient", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "Encounter", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "Condition", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "Observation", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "MedicationRequest", "interaction": [{"code": "read"}, {"code": "search-type"}]}
                ]
            }
        ]
    }
    return jsonify(metadata), 200


@app.route('/fhir/Patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID"""
    patient = PATIENTS.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient), 200


@app.route('/fhir/Patient', methods=['GET'])
def search_patients():
    """Search patients"""
    # Simple search by name or ID
    name = request.args.get('name')
    identifier = request.args.get('identifier')
    
    results = list(PATIENTS.values())
    
    if name:
        results = [p for p in results if name.lower() in p.get("name", [{}])[0].get("family", "").lower()]
    
    if identifier:
        results = [p for p in results if any(i.get("value") == identifier for i in p.get("identifier", []))]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": [{"resource": p} for p in results]
    }
    
    return jsonify(bundle), 200


@app.route('/fhir/Encounter/<encounter_id>', methods=['GET'])
def get_encounter(encounter_id):
    """Get encounter by ID"""
    encounter = ENCOUNTERS.get(encounter_id)
    if not encounter:
        return jsonify({"error": "Encounter not found"}), 404
    return jsonify(encounter), 200


@app.route('/fhir/Encounter', methods=['GET'])
def search_encounters():
    """Search encounters"""
    patient_id = request.args.get('patient')
    
    results = list(ENCOUNTERS.values())
    
    if patient_id:
        results = [e for e in results if e.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": [{"resource": e} for e in results]
    }
    
    return jsonify(bundle), 200


@app.route('/fhir/Condition/<condition_id>', methods=['GET'])
def get_condition(condition_id):
    """Get condition by ID"""
    condition = CONDITIONS.get(condition_id)
    if not condition:
        return jsonify({"error": "Condition not found"}), 404
    return jsonify(condition), 200


@app.route('/fhir/Condition', methods=['GET'])
def search_conditions():
    """Search conditions"""
    patient_id = request.args.get('patient')
    
    results = list(CONDITIONS.values())
    
    if patient_id:
        results = [c for c in results if c.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": [{"resource": c} for c in results]
    }
    
    return jsonify(bundle), 200


@app.route('/fhir/Observation/<observation_id>', methods=['GET'])
def get_observation(observation_id):
    """Get observation by ID"""
    observation = OBSERVATIONS.get(observation_id)
    if not observation:
        return jsonify({"error": "Observation not found"}), 404
    return jsonify(observation), 200


@app.route('/fhir/Observation', methods=['GET'])
def search_observations():
    """Search observations"""
    patient_id = request.args.get('patient')
    code = request.args.get('code')
    sort = request.args.get('_sort')
    count = request.args.get('_count', type=int)
    
    results = list(OBSERVATIONS.values())
    
    if patient_id:
        results = [o for o in results if o.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    if code:
        results = [o for o in results if code in o.get("code", {}).get("coding", [{}])[0].get("code", "")]
    
    if sort == "-date":
        results.sort(key=lambda o: o.get("effectiveDateTime", ""), reverse=True)
    
    if count:
        results = results[:count]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": [{"resource": o} for o in results]
    }
    
    return jsonify(bundle), 200


@app.route('/fhir/MedicationRequest/<medication_id>', methods=['GET'])
def get_medication_request(medication_id):
    """Get medication request by ID"""
    medication = MEDICATION_REQUESTS.get(medication_id)
    if not medication:
        return jsonify({"error": "MedicationRequest not found"}), 404
    return jsonify(medication), 200


@app.route('/fhir/MedicationRequest', methods=['GET'])
def search_medication_requests():
    """Search medication requests"""
    patient_id = request.args.get('patient')
    status = request.args.get('status')
    
    results = list(MEDICATION_REQUESTS.values())
    
    if patient_id:
        results = [m for m in results if m.get("subject", {}).get("reference") == f"Patient/{patient_id}"]
    
    if status:
        results = [m for m in results if m.get("status") == status]
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": [{"resource": m} for m in results]
    }
    
    return jsonify(bundle), 200


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "patients": len(PATIENTS),
        "encounters": len(ENCOUNTERS),
        "conditions": len(CONDITIONS),
        "observations": len(OBSERVATIONS),
        "medications": len(MEDICATION_REQUESTS)
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API info"""
    return jsonify({
        "name": "Mock EHR Server",
        "version": "1.0.0",
        "description": "Mock EHR with CDS Hooks and FHIR R4 support for integration testing",
        "endpoints": {
            "cds_hooks": {
                "discovery": "/cds-services",
                "services": "/cds-services/{service_id}"
            },
            "fhir": {
                "metadata": "/fhir/metadata",
                "patient": "/fhir/Patient",
                "encounter": "/fhir/Encounter",
                "condition": "/fhir/Condition",
                "observation": "/fhir/Observation",
                "medication": "/fhir/MedicationRequest"
            },
            "health": "/health"
        }
    }), 200


if __name__ == '__main__':
    print("=" * 80)
    print("MOCK EHR SERVER - Phase 6 Integration Testing")
    print("=" * 80)
    print()
    print("Loading test data...")
    load_test_data()
    print()
    print("Starting server on http://localhost:5000")
    print("CDS Hooks discovery: http://localhost:5000/cds-services")
    print("FHIR metadata: http://localhost:5000/fhir/metadata")
    print("Health check: http://localhost:5000/health")
    print()
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

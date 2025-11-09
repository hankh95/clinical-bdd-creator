#!/usr/bin/env python3
"""
Test client for Mock EHR Server
Validates CDS Hooks and FHIR endpoints

Author: GitHub Copilot
Date: 2025-11-09
Phase: 6 - Integration Testing
"""

import json
import requests
from typing import Dict, List

BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test server health endpoint"""
    print("\n[TEST] Health Check")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    print(f"  ✓ Server healthy: {data['patients']} patients, {data['encounters']} encounters")
    return data


def test_cds_discovery():
    """Test CDS Hooks discovery endpoint"""
    print("\n[TEST] CDS Hooks Discovery")
    response = requests.get(f"{BASE_URL}/cds-services")
    assert response.status_code == 200
    data = response.json()
    services = data.get("services", [])
    print(f"  ✓ Found {len(services)} CDS services:")
    for service in services:
        print(f"    - {service['id']}: {service['title']}")
    return services


def test_cds_patient_view():
    """Test CDS patient-view hook"""
    print("\n[TEST] CDS Hooks - Patient View")
    
    payload = {
        "hook": "patient-view",
        "hookInstance": "test-instance-001",
        "context": {
            "patientId": "patient-hypertension-001",
            "userId": "Practitioner/practitioner-001"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/cds-services/patient-view-cds",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    data = response.json()
    cards = data.get("cards", [])
    print(f"  ✓ Received {len(cards)} cards:")
    for card in cards:
        print(f"    - {card['summary']} ({card['indicator']})")
    return cards


def test_fhir_metadata():
    """Test FHIR metadata endpoint"""
    print("\n[TEST] FHIR Metadata")
    response = requests.get(f"{BASE_URL}/fhir/metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "CapabilityStatement"
    print(f"  ✓ FHIR version: {data['fhirVersion']}")
    return data


def test_fhir_patient():
    """Test FHIR Patient read"""
    print("\n[TEST] FHIR Patient Read")
    patient_id = "patient-hypertension-001"
    response = requests.get(f"{BASE_URL}/fhir/Patient/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "Patient"
    name = data["name"][0]
    print(f"  ✓ Patient: {name['given'][0]} {name['family']}")
    return data


def test_fhir_patient_search():
    """Test FHIR Patient search"""
    print("\n[TEST] FHIR Patient Search")
    response = requests.get(f"{BASE_URL}/fhir/Patient?name=Smith")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "Bundle"
    print(f"  ✓ Found {data['total']} patient(s)")
    return data


def test_fhir_observations():
    """Test FHIR Observation search"""
    print("\n[TEST] FHIR Observation Search")
    patient_id = "patient-hypertension-001"
    response = requests.get(f"{BASE_URL}/fhir/Observation?patient={patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "Bundle"
    print(f"  ✓ Found {data['total']} observation(s) for patient")
    return data


def test_fhir_conditions():
    """Test FHIR Condition search"""
    print("\n[TEST] FHIR Condition Search")
    patient_id = "patient-diabetes-001"
    response = requests.get(f"{BASE_URL}/fhir/Condition?patient={patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "Bundle"
    print(f"  ✓ Found {data['total']} condition(s) for patient")
    return data


def test_fhir_medications():
    """Test FHIR MedicationRequest search"""
    print("\n[TEST] FHIR MedicationRequest Search")
    patient_id = "patient-sepsis-001"
    response = requests.get(f"{BASE_URL}/fhir/MedicationRequest?patient={patient_id}&status=active")
    assert response.status_code == 200
    data = response.json()
    assert data["resourceType"] == "Bundle"
    print(f"  ✓ Found {data['total']} active medication(s) for patient")
    return data


def run_all_tests():
    """Run all test cases"""
    print("=" * 80)
    print("Mock EHR Server - Integration Tests")
    print("=" * 80)
    
    try:
        # Server health
        test_health_check()
        
        # CDS Hooks tests
        test_cds_discovery()
        test_cds_patient_view()
        
        # FHIR tests
        test_fhir_metadata()
        test_fhir_patient()
        test_fhir_patient_search()
        test_fhir_observations()
        test_fhir_conditions()
        test_fhir_medications()
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server")
        print("  Make sure the server is running: ./scripts/start_server.sh")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())

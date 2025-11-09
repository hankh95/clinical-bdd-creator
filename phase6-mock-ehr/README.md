# Phase 6: Mock EHR Environment

## Overview

Complete mock Electronic Health Record (EHR) server for integration testing with CDS Hooks v1.0 and FHIR R4 compliance.

## Features

✅ **CDS Hooks v1.0** - Clinical decision support service endpoints  
✅ **FHIR R4 Resources** - Patient, Encounter, Condition, Observation, MedicationRequest  
✅ **Test Data** - 3 clinical scenarios (hypertension, diabetes, sepsis)  
✅ **RESTful API** - Easy integration with Clinical BDD Creator  
✅ **Automated Testing** - Built-in test client  

## Quick Start

```bash
# 1. Setup environment
./setup.sh

# 2. Start server
./scripts/start_server.sh

# 3. Test server (in separate terminal)
source venv/bin/activate
python3 scripts/test_server.py
```

Server runs on: **http://localhost:5000**

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API information |
| `GET /health` | Health check |
| `GET /cds-services` | CDS Hooks discovery |
| `POST /cds-services/{id}` | Invoke CDS service |
| `GET /fhir/metadata` | FHIR capability statement |
| `GET /fhir/Patient/{id}` | Read patient |
| `GET /fhir/Observation?patient={id}` | Search observations |

## Test Scenarios

### 1. Hypertension (John Smith)
- Patient ID: `patient-hypertension-001`
- BP: 158/95 mmHg (elevated)
- Medication: Lisinopril 10mg daily

### 2. Diabetes (Mary Johnson)
- Patient ID: `patient-diabetes-001`
- HbA1c: 8.2% (elevated)
- Medication: Metformin 500mg twice daily

### 3. Sepsis (Robert Williams)
- Patient ID: `patient-sepsis-001`
- Temperature: 39.5°C, WBC: 18.5, Lactate: 3.2
- Medications: Ceftriaxone + Vancomycin

## Documentation

See `docs/README.md` for complete documentation including:
- API reference
- CDS Hooks specification compliance
- FHIR R4 compliance details
- Integration testing guide
- Configuration options
- Extension points
- Troubleshooting

## Requirements

- Python 3.7+
- Flask 2.3+
- Flask-CORS 4.0+

## Directory Structure

```
phase6-mock-ehr/
├── server/                    # Flask server implementation
├── test_data/                 # FHIR test data fixtures
├── config/                    # Configuration files
├── scripts/                   # Helper scripts
├── docs/                      # Complete documentation
├── setup.sh                   # Environment setup
└── README.md                  # This file
```

## Testing

Run automated tests:
```bash
python3 scripts/test_server.py
```

Expected output:
```
✓ Health Check
✓ CDS Hooks Discovery (3 services)
✓ CDS Hooks - Patient View (2 cards)
✓ FHIR Metadata
✓ FHIR Patient Read
✓ FHIR Patient Search
✓ FHIR Observation Search
✓ FHIR Condition Search
✓ FHIR MedicationRequest Search

✓ ALL TESTS PASSED
```

## Integration with Clinical BDD Creator

Example usage:
```python
import requests

# Get patient data
patient = requests.get("http://localhost:5000/fhir/Patient/patient-hypertension-001")

# Invoke CDS Hook
cds_response = requests.post(
    "http://localhost:5000/cds-services/patient-view-cds",
    json={
        "hook": "patient-view",
        "context": {"patientId": "patient-hypertension-001"}
    }
)

# Process cards
for card in cds_response.json()["cards"]:
    print(f"{card['summary']}: {card['detail']}")
```

## Security Warning

⚠️ **This is a MOCK server for testing only**

- No authentication
- No data encryption
- No audit logging
- Not HIPAA compliant
- Do not use with real patient data

## Next Steps

1. **Phase 6 Integration**: Connect Clinical BDD Creator
2. **End-to-End Testing**: Validate complete workflows  
3. **Production Adapter**: Build real EHR connectors

## License

Part of Clinical BDD Creator project - Phase 6 deliverable

---

**Status:** ✅ Complete  
**Version:** 1.0.0  
**Date:** 2025-11-09

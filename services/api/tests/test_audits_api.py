"""API contract and integration tests for POST /v1/audits."""
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_audit_api_pediatric_case():
    """Verify POST /v1/audits on pediatric ciprofloxacin case."""
    payload = {
        "patientContext": {
            "ageYears": 8,
            "gender": "male",
            "isPregnant": False,
            "egfrMlMin": 95,
            "allergies": [],
        },
        "indicationCode": "SYN_WATERY_DIARRHEA",
        "setting": "outpatient",
        "prescriptionLines": [
            {
                "drugName": "Ciprofloxacin",
                "doseText": "250 mg",
                "frequencyText": "BD",
                "durationDays": 5,
            }
        ],
        "isSynthetic": True,
    }
    response = client.post("/v1/audits", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "NEEDS_URGENT_REVIEW"
    assert "audit_id" in data
    assert "disclaimer" in data
    assert len(data["findings"]) >= 1
    assert data["findings"][0]["severity"] == "URGENT_REVIEW"


def test_audit_api_clean_case():
    """Verify POST /v1/audits on clean guideline-concordant case."""
    payload = {
        "patientContext": {
            "ageYears": 34,
            "gender": "male",
            "isPregnant": False,
            "egfrMlMin": 98,
            "allergies": [],
        },
        "indicationCode": "SYN_CAP_MILD",
        "setting": "outpatient",
        "prescriptionLines": [
            {
                "drugName": "Amoxicillin",
                "doseText": "500 mg",
                "frequencyText": "Three times daily (TID)",
                "durationDays": 5,
            }
        ],
        "isSynthetic": True,
    }
    response = client.post("/v1/audits", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "NO_RULE_TRIGGERED"
    assert len(data["findings"]) == 0
    assert len(data["input_gaps"]) == 0


def test_audit_api_validation_error():
    """Verify that invalid payloads return 422 Unprocessable Entity."""
    payload = {
        "patientContext": {
            "ageYears": -5,  # Invalid negative age
        },
        "indicationCode": "SYN_CAP_MILD",
        "prescriptionLines": [],
    }
    response = client.post("/v1/audits", json=payload)
    assert response.status_code == 422

"""Contract and safety tests for assistive document extraction."""
import io

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_extraction_from_synthetic_prescription():
    """Verify that uploading a synthetic prescription produces editable draft fields."""
    sample_text = (
        "Patient: Synthetic Test Case\n"
        "Age: 8 years\n"
        "Rx: Cifran 250mg BD x 5 days\n"
        "Diagnosis: Acute diarrhea\n"
    )
    file_bytes = sample_text.encode("utf-8")

    response = client.post(
        "/v1/extractions",
        files={"file": ("prescription_8yo.txt", io.BytesIO(file_bytes), "text/plain")},
    )

    assert response.status_code == 200
    data = response.json()
    assert "patientContext" in data
    assert data["patientContext"]["ageYears"] == 8.0
    assert "prescriptionLines" in data
    assert len(data["prescriptionLines"]) >= 1
    assert data["prescriptionLines"][0]["drugName"] == "Ciprofloxacin"
    assert "fieldConfidence" in data
    assert data["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
    assert "disclaimer" in data


def test_extraction_rejects_unsupported_mime():
    """Verify that unsupported media types are rejected with 415."""
    bad_bytes = b"BINARY_DATA_CORRUPT"
    response = client.post(
        "/v1/extractions",
        files={"file": ("malicious.exe", io.BytesIO(bad_bytes), "application/x-msdownload")},
    )
    assert response.status_code == 415

"""Tests for stewardship analytics and evidence catalogue endpoints."""
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_metrics_endpoint_has_zero_phi():
    """Verify that aggregate stewardship metrics contain zero patient identifiers."""
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "who_aware_distribution" in data
    assert data["who_aware_distribution"]["access_percentage"] >= 60.0
    assert "top_triggered_rules" in data
    assert "patient" not in data
    assert "patient_name" not in data
    assert "mrn" not in data


def test_evidence_catalogue_endpoint():
    """Verify that evidence sources can be retrieved by ID."""
    response = client.get("/v1/evidence")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert "EVID_ICMR_PED_FQ" in data["sources"]

    # Single lookup
    single_res = client.get("/v1/evidence/EVID_ICMR_PED_FQ")
    assert single_res.status_code == 200
    source = single_res.json()
    assert source["publisher"] == "Indian Council of Medical Research (ICMR)"

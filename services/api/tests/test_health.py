"""Test suite for health endpoint."""
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check_returns_200():
    """Verify that /health returns 200 with service metadata and no PHI."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "active_rule_set_version" in data
    assert data["engine_mode"] == "deterministic_isolated"
    assert "patient" not in data
    assert "prescription" not in data


def test_health_check_has_trace_headers():
    """Verify that response contains security and trace headers."""
    response = client.get("/health")
    assert "x-trace-id" in response.headers
    assert "x-response-time-sec" in response.headers
    assert response.headers.get("x-content-type-options") == "nosniff"

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.reliability_engine import compute_water_reliability_score

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "nRF54LM20" in data["hardware_target"]

def test_water_reliability_formulation():
    # Healthy pump, high flow efficiency, normal tank recovery
    res = compute_water_reliability_score(pump_health=95.0, flow_efficiency=1.0, tank_recovery=1.0)
    assert res["water_reliability_score"] >= 90.0
    assert res["risk_level"] == "LOW"
    assert res["maintenance_priority"] == "NORMAL"

    # Severely degrading pump, low flow efficiency, sluggish tank recovery
    res_degraded = compute_water_reliability_score(pump_health=35.0, flow_efficiency=0.55, tank_recovery=0.40)
    assert res_degraded["water_reliability_score"] < 50.0
    assert res_degraded["risk_level"] in ["HIGH", "CRITICAL"]
    assert res_degraded["maintenance_priority"] in ["HIGH PRIORITY", "CRITICAL"]

def test_get_assets():
    response = client.get("/api/assets")
    assert response.status_code == 200
    assets = response.json()
    assert len(assets) >= 4
    pump_ids = [a["id"] for a in assets]
    assert "PUMP-03" in pump_ids

def test_failure_to_impact_prediction():
    response = client.get("/api/assets/PUMP-03/prediction")
    assert response.status_code == 200
    data = response.json()
    assert "water_reliability_score" in data
    assert "estimated_maintenance_window" in data
    assert "recommended_action" in data

def test_simulation_fault_injection():
    # Inject fault
    inject_res = client.post("/api/simulation/fault", json={
        "asset_id": "PUMP-03",
        "fault_type": "BEARING_DEGRADATION",
        "severity": 0.75
    })
    assert inject_res.status_code == 200
    data = inject_res.json()
    assert data["success"] is True
    assert data["new_status"] == "DEGRADING"

    # Reset
    reset_res = client.post("/api/simulation/reset")
    assert reset_res.status_code == 200

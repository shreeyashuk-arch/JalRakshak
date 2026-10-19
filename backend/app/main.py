from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import datetime
import math

from backend.app.database import get_connection, init_db
from backend.app.reliability_engine import compute_water_reliability_score

init_db()

app = FastAPI(
    title="JalRakshak API",
    description="Edge-AI Predictive Maintenance & Water Reliability Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schemas
class FaultInjectionRequest(BaseModel):
    asset_id: str = "PUMP-03"
    fault_type: str = "BEARING_DEGRADATION" # BEARING_DEGRADATION, OVERLOAD, LOW_FLOW, OVERHEATING, NORMAL
    severity: float = 0.65                  # 0.0 to 1.0

# 1. Health check
@app.get("/api/health")
def api_health():
    return {
        "status": "ONLINE",
        "system": "JalRakshak Reliability Engine",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "hardware_target": "Nordic Semiconductor nRF54LM20 DK",
        "aquamesh_protocol": "BLE Mesh v1.1 Profile"
    }

# 2. Assets list
@app.get("/api/assets")
def get_assets():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM assets").fetchall()
    conn.close()
    
    result = []
    for r in rows:
        d = dict(r)
        # Dynamic health based on current state
        if d["status"] == "HEALTHY":
            d["health_score"] = 96
            d["risk"] = "LOW"
            d["water_impact"] = "MINIMAL"
        elif d["status"] == "MONITOR":
            d["health_score"] = 81
            d["risk"] = "LOW"
            d["water_impact"] = "SLIGHT"
        elif d["status"] == "DEGRADING":
            d["health_score"] = 54
            d["risk"] = "HIGH"
            d["water_impact"] = "HIGH"
        elif d["status"] == "CRITICAL":
            d["health_score"] = 31
            d["risk"] = "CRITICAL"
            d["water_impact"] = "SEVERE"
        else:
            d["health_score"] = 92
            d["risk"] = "LOW"
            d["water_impact"] = "MINIMAL"
        result.append(d)
    return result

# 3. Asset detail
@app.get("/api/assets/{asset_id}")
def get_asset_detail(asset_id: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Asset not found")
    return dict(row)

# 4. Telemetry trend
@app.get("/api/assets/{asset_id}/telemetry")
def get_asset_telemetry(asset_id: str, limit: int = 30):
    # Generates time-series curve reflecting current asset condition
    conn = get_connection()
    asset = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    conn.close()
    
    status = asset["status"] if asset else "HEALTHY"
    base_vib = 1.0
    base_curr = 4.2
    base_temp = 42.0
    base_flow = 85.0

    if status == "DEGRADING":
        base_vib = 1.38
        base_temp = 51.2
        base_flow = 74.5
        base_curr = 4.6
    elif status == "CRITICAL":
        base_vib = 1.85
        base_temp = 66.0
        base_flow = 52.0
        base_curr = 5.9

    points = []
    now = datetime.datetime.utcnow()
    for i in range(limit):
        t = now - datetime.timedelta(seconds=(limit - i) * 10)
        noise = math.sin(i * 0.4) * 0.05
        points.append({
            "timestamp": t.strftime("%H:%M:%S"),
            "vibration_rms": round(base_vib + noise + (i * 0.005 if status == "DEGRADING" else 0), 3),
            "motor_current": round(base_curr + noise * 0.3, 2),
            "temperature": round(base_temp + (i * 0.1 if status in ["DEGRADING", "CRITICAL"] else 0), 1),
            "flow_rate": round(base_flow - (i * 0.15 if status == "DEGRADING" else 0), 1),
            "tank_level": round(80.0 - (i * 0.3 if status in ["DEGRADING", "CRITICAL"] else 0), 1)
        })
    return points

# 5. Asset Health assessment
@app.get("/api/assets/{asset_id}/health")
def get_asset_health(asset_id: str):
    conn = get_connection()
    asset = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    conn.close()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    status = asset["status"]
    score_map = {"HEALTHY": 96.0, "MONITOR": 81.0, "DEGRADING": 54.0, "CRITICAL": 31.0}
    health_score = score_map.get(status, 90.0)

    return {
        "asset_id": asset_id,
        "name": asset["name"],
        "status": status,
        "health_score": health_score,
        "anomaly_score": round((100.0 - health_score) / 100.0, 2),
        "last_assessment": datetime.datetime.utcnow().isoformat()
    }

# 6. Failure-to-Impact Prediction
@app.get("/api/assets/{asset_id}/prediction")
def get_asset_prediction(asset_id: str):
    conn = get_connection()
    asset = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    conn.close()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    status = asset["status"]
    if status == "DEGRADING":
        p_health = 54.0
        flow_eff = 0.88
        tank_rec = 0.72
        observed = [
            "Vibration: +38% from nominal baseline",
            "Current: +9% irregularity detected",
            "Flow efficiency: -12% drop",
            "Tank recovery time: +14 minutes delay"
        ]
    elif status == "CRITICAL":
        p_health = 31.0
        flow_eff = 0.61
        tank_rec = 0.40
        observed = [
            "Vibration: +85% severe mechanical impulse",
            "Temperature: +24°C severe thermal climb",
            "Flow efficiency: -39% hydraulic delivery loss",
            "Tank recovery rate: Stalled (net negative buffer)"
        ]
    elif status == "MONITOR":
        p_health = 81.0
        flow_eff = 0.96
        tank_rec = 0.90
        observed = [
            "Vibration: +12% mild elevation",
            "Current: Steady nominal draw",
            "Flow: 96% efficiency"
        ]
    else:
        p_health = 96.0
        flow_eff = 1.00
        tank_rec = 0.98
        observed = ["All parameters within nominal tolerance."]

    prediction = compute_water_reliability_score(p_health, flow_eff, tank_rec)
    prediction["asset_id"] = asset_id
    prediction["observed_deviations"] = observed
    return prediction

# 7. Maintenance recommendation
@app.get("/api/assets/{asset_id}/maintenance")
def get_asset_maintenance(asset_id: str):
    pred = get_asset_prediction(asset_id)
    return {
        "asset_id": asset_id,
        "priority": pred["maintenance_priority"],
        "risk_level": pred["risk_level"],
        "urgency": pred["urgency"],
        "recommended_action": pred["recommended_action"],
        "estimated_maintenance_window": pred["estimated_maintenance_window"],
        "opportunity_detected": True if pred["risk_level"] in ["HIGH", "CRITICAL"] else False,
        "opportunity_details": "Technician handheld gateway detected nearby on Sector 1 route. Action combined."
    }

# 8. Overall Water Reliability
@app.get("/api/water-reliability")
def get_system_water_reliability():
    conn = get_connection()
    assets = conn.execute("SELECT status FROM assets WHERE asset_type = 'PUMP'").fetchall()
    conn.close()

    scores = []
    for a in assets:
        s = a["status"]
        if s == "HEALTHY": scores.append(96)
        elif s == "MONITOR": scores.append(81)
        elif s == "DEGRADING": scores.append(54)
        elif s == "CRITICAL": scores.append(31)
    
    avg_health = sum(scores) / len(scores) if scores else 90.0
    calc = compute_water_reliability_score(avg_health, 0.91, 0.88)

    return {
        "overall_score": calc["water_reliability_score"],
        "active_assets": len(assets),
        "assets_at_risk": sum(1 for s in scores if s < 60),
        "maintenance_due": sum(1 for s in scores if s < 70),
        "system_status": "STABLE" if calc["water_reliability_score"] > 80 else ("ATTENTION REQUIRED" if calc["water_reliability_score"] > 60 else "HIGH RISK"),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "disclaimer": calc["disclaimer"]
    }

# 9. Events
@app.get("/api/events")
def get_events(limit: int = 15):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# 10. AquaMesh Nodes
@app.get("/api/mesh/nodes")
def get_mesh_nodes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM mesh_nodes").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# 11. Simulation Fault Injection
@app.post("/api/simulation/fault")
def inject_fault(req: FaultInjectionRequest):
    conn = get_connection()
    new_status = "HEALTHY"
    if req.fault_type == "NORMAL":
        new_status = "HEALTHY"
    elif req.fault_type in ["BEARING_DEGRADATION", "OVERLOAD"]:
        new_status = "DEGRADING" if req.severity < 0.8 else "CRITICAL"
    elif req.fault_type in ["LOW_FLOW", "OVERHEATING"]:
        new_status = "CRITICAL"

    conn.execute("UPDATE assets SET status = ? WHERE id = ?", (new_status, req.asset_id))
    conn.execute(
        "INSERT INTO events (asset_id, event_type, severity, message) VALUES (?, ?, ?, ?)",
        (req.asset_id, "SIMULATION_FAULT_INJECTED", "WARNING" if new_status != "CRITICAL" else "CRITICAL",
         f"Injected {req.fault_type} (severity={req.severity:.2f}) into {req.asset_id}")
    )
    conn.commit()
    conn.close()

    return {
        "success": True,
        "asset_id": req.asset_id,
        "fault_type": req.fault_type,
        "severity": req.severity,
        "new_status": new_status,
        "message": f"Successfully simulated {req.fault_type} on {req.asset_id}"
    }

# 12. Reset simulation
@app.post("/api/simulation/reset")
def reset_simulation():
    conn = get_connection()
    conn.execute("UPDATE assets SET status = 'HEALTHY' WHERE id = 'PUMP-01'")
    conn.execute("UPDATE assets SET status = 'MONITOR' WHERE id = 'PUMP-02'")
    conn.execute("UPDATE assets SET status = 'HEALTHY' WHERE id = 'PUMP-03'")
    conn.execute("UPDATE assets SET status = 'CRITICAL' WHERE id = 'PUMP-04'")
    conn.execute("INSERT INTO events (asset_id, event_type, severity, message) VALUES ('SYSTEM', 'RESET', 'INFO', 'Simulation state reset to baseline.')")
    conn.commit()
    conn.close()
    return {"success": True, "message": "Simulation reset to default state"}

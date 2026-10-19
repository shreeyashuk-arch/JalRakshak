# JalRakshak Backend Service

**Predict the Failure. Protect the Water.**

This module implements the FastAPI REST application providing multi-asset management, real-time telemetry curves, Edge-AI inference bridges, composite Water Reliability Score computation, and simulation fault injection.

---

## 1. Quick Start

### Installation
```bash
# From repository root:
pip install -r backend/requirements.txt
```

### Run Server
```bash
python -m uvicorn backend.app.main:app --port 8000 --reload
```

Interactive Swagger documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 2. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System status, hardware target (`nRF54LM20 DK`), and protocol |
| `GET` | `/api/assets` | Fleet list (pumps, storage tanks) with health and water risk |
| `GET` | `/api/assets/{id}` | Asset metadata and nominal baselines |
| `GET` | `/api/assets/{id}/telemetry` | Time-series sensor stream (vibration RMS, current, temp, flow) |
| `GET` | `/api/assets/{id}/prediction` | Failure-to-impact calculation and observed deviations |
| `GET` | `/api/assets/{id}/maintenance` | Maintenance priority, estimated window, and opportunity alerts |
| `GET` | `/api/water-reliability` | System-level composite Water Reliability Score (0–100) |
| `GET` | `/api/mesh/nodes` | AquaMesh topology status, hop count, and RSSI |
| `POST`| `/api/simulation/fault` | Injects synthetic fault (`BEARING_DEGRADATION`, `OVERLOAD`, etc.) |
| `POST`| `/api/simulation/reset` | Resets asset fleet to healthy baseline |

---

## 3. Running Unit Tests

```bash
python -m pytest backend/tests/test_backend.py -v
```
Verifies health checks, database queries, mathematical reliability scoring, and simulation state transitions.
